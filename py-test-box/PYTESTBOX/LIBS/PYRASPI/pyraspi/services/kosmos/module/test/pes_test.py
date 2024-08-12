#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.test.pes_test
:brief: Kosmos PES Module Test Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2022/01/05
"""

# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from warnings import catch_warnings

from math import ceil

from pylibrary.emulator.emulatorinterfaces import EventInterface
from pyraspi.services.kosmos.kosmos import FPGA_CLOCK_PERIOD_NS
from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.kosmos.module.devicetree import DeviceTreeModuleBaseClass
from pyraspi.services.kosmos.module.module import BufferModuleBaseClass
from pyraspi.services.kosmos.module.module import ConsumerModuleBaseClass
from pyraspi.services.kosmos.module.module import ModuleBaseClass
from pyraspi.services.kosmos.module.module import StatusResetModuleBaseClass
from pyraspi.services.kosmos.module.module import UploadModuleBaseClass
from pyraspi.services.kosmos.module.pes import PES_MARKER
from pyraspi.services.kosmos.module.pes import PesModule
from pyraspi.services.kosmos.module.pesevents import LED_PIN_EVENT_NAME
from pyraspi.services.kosmos.module.pesevents import PES_ACTION_EVENT_NOP
from pyraspi.services.kosmos.module.pesevents import PesActionEventBase
from pyraspi.services.kosmos.module.pesevents import PesEventBase
from pyraspi.services.kosmos.module.pesevents import PesEventModuleInterface
from pyraspi.services.kosmos.module.pesevents import PesResumeEventBase
from pyraspi.services.kosmos.module.test.module_test import AbstractTestClass
from pyraspi.services.kosmos.module.test.module_test import require_kosmos_device
from pyraspi.services.kosmos.protocol.generated.messages import MSG_PAYLOAD_RAW_UINT32_COUNT
from pyraspi.services.kosmos.protocol.generated.messages import PES_ISA_MARKER_OP_ENUM_MAX_VALUE
from pyraspi.services.kosmos.protocol.generated.messages import PES_ISA_MARKER_OP_RESERVED_BITS
from pyraspi.services.kosmos.protocol.generated.messages import PES_ISA_MARKER_OP_RESET_STOPWATCH_2_TIME_MARK
from pyraspi.services.kosmos.protocol.generated.messages import PES_ISA_MARKER_OP_SAVE_GLOBAL_TIME_MARK
from pyraspi.services.kosmos.protocol.generated.messages import PES_ISA_MARKER_OP_STOPWATCH_2_STOP
from pyraspi.services.kosmos.protocol.generated.messages import PES_OPCODE_EXECUTE
from pyraspi.services.kosmos.protocol.generated.messages import PES_OPCODE_MARKER
from pyraspi.services.kosmos.protocol.generated.messages import PES_OPCODE_SUBDELAY_05_TICKS
from pyraspi.services.kosmos.protocol.generated.messages import PES_OPCODE_SUBDELAY_10_TICKS
from pyraspi.services.kosmos.protocol.generated.messages import PES_OPCODE_WAIT
from pyraspi.services.kosmos.protocol.generated.messages import PES_OPERAND_BITS
from pyraspi.services.kosmos.protocol.generated.messages import pes_isa_marker_operation_e__enumvalues
from pyraspi.services.kosmos.utils import pretty_list


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
def PAE(value):
    """
    Shorthand notation for instantiating a PesActionEventBase object

    :param value: PES Action Event operand value
    :type value: ``int``

    :return: PesActionEventBase object, with name 'TEST' and given value
    :rtype: ``PesActionEventBase``
    """
    return PesActionEventBase(name='TEST', value=value)
# end def PAE


def PRE(value):
    """
    Shorthand notation for instantiating a PesResumeEventBase object

    :param value: PES Resume Event operand value
    :type value: ``int``

    :return: PesResumeEventBase object, with name 'TEST' and given value
    :rtype: ``PesResumeEventBase``
    """
    return PesResumeEventBase(name='TEST', value=value)
# end def PRE


@require_kosmos_device(DeviceName.PES)
class PesModuleTestCase(AbstractTestClass.UploadModuleInterfaceTestCase):
    """
    Kosmos PES Module Test Class
    """

    @classmethod
    def _get_module_under_test(cls):
        """
        Return the module instance to be tested.
        Override `AbstractTestClass.ModuleInterfaceTestCase._get_module_under_test()`.

        :return: The module instance to be tested.
        :rtype: ``PesModule``
        """
        return cls.kosmos.dt.pes
    # end def _get_module_under_test

    def test_class_inheritance(self):
        """
        Non-regression test: Validate interface class composition.
        """
        mro = self.kosmos.pes.__class__.mro()
        expected_mro = [PesModule,
                        ConsumerModuleBaseClass,
                        UploadModuleBaseClass,
                        BufferModuleBaseClass,
                        StatusResetModuleBaseClass,
                        ModuleBaseClass,
                        EventInterface,
                        PesEventModuleInterface,
                        DeviceTreeModuleBaseClass,
                        object]

        max_diff_cache = self.maxDiff
        self.maxDiff = None  # Allow full diff to be displayed in case of failure

        self.assertListEqual(expected_mro, mro, msg='\nPython Method Resolution Order (mro) is unexpected.')

        self.maxDiff = max_diff_cache  # Restore maxDiff setting
    # end def test_class_inheritance

    def test_get_instructions(self):
        """
        Validate construction of instruction buffer with various union types
        """
        # instruction 0 PES:EXEC
        self.kosmos.pes.append(self.kosmos.pes.get_execute_instruction(action=PAE(0x1234)))
        # instruction 1 PES:WAIT
        self.kosmos.pes.append(self.kosmos.pes.get_wait_instruction(action=PRE(0x5678)))
        # instruction 2 PES:EXEC:NOP
        self.kosmos.pes.extend(self.kosmos.pes.get_delay_instructions(delay_ticks=1))
        # instruction 3 PES:SUBDELAY:05
        self.kosmos.pes.extend(self.kosmos.pes.get_delay_instructions(delay_ticks=5, action=PAE(0xABC2)))
        # instruction 4 PES:SUBDELAY:10
        self.kosmos.pes.extend(self.kosmos.pes.get_delay_instructions(delay_ticks=10, action=PAE(0xABC3)))
        # instruction 5 PES:DELAY:100
        self.kosmos.pes.extend(self.kosmos.pes.get_delay_instructions(delay_ticks=100, action=PAE(0xABC4)))
        # instruction 6 PES:MARKER
        self.kosmos.pes.append(self.kosmos.pes.get_marker_instruction(action=0x0321))

        instruction_count = 7
        self.assertEqual(instruction_count, self.kosmos.pes.length())

        # Validate transformation of instruction buffer to MessageFrames
        tx_frames = self.kosmos.pes.messages()
        self.assertEqual(ceil(instruction_count/MSG_PAYLOAD_RAW_UINT32_COUNT), len(tx_frames))
        pes = tx_frames[0].frame.payload.pes

        # instruction 0 PES:EXEC
        self.assertEqual(PES_OPCODE_EXECUTE, pes[0].execute.opcode)
        self.assertEqual(0x1234, pes[0].execute.action_event)
        # instruction 1 PES:WAIT
        self.assertEqual(PES_OPCODE_WAIT, pes[1].wait.opcode)
        self.assertEqual(0x5678, pes[1].wait.resume_event)
        # instruction 2 PES:EXEC:NOP
        self.assertEqual(PES_OPCODE_EXECUTE, pes[2].execute.opcode)
        self.assertEqual(PES_ACTION_EVENT_NOP.value, pes[2].execute.action_event)
        # instruction 3 PES:SUBDELAY:05
        self.assertEqual(PES_OPCODE_SUBDELAY_05_TICKS, pes[3].field.opcode)
        self.assertEqual(0xABC2, pes[3].subdelay.action_event)
        # instruction 4 PES:SUBDELAY:10
        self.assertEqual(PES_OPCODE_SUBDELAY_10_TICKS, pes[4].field.opcode)
        self.assertEqual(0xABC3, pes[4].subdelay.action_event)
        # instruction 5 PES:DELAY:100
        self.assertEqual(0, pes[5].delay.opcode.exponent)
        self.assertEqual(1, pes[5].delay.opcode.mantissa)
        self.assertEqual(0xABC4, pes[5].delay.action_event)
        # instruction 6 PES:MARKER
        self.assertEqual(PES_OPCODE_MARKER, pes[6].marker.opcode)
        self.assertEqual(0x0321, pes[6].marker.operand.raw)

        self.kosmos.pes.clear()
    # end def test_get_instructions

    def test_instructions(self):
        """
        Validate construction of instruction buffer with various instructions
        """
        # instruction 0 PES:EXEC
        self.kosmos.pes.execute(action=PAE(0x1234))
        # instruction 1 PES:WAIT
        self.kosmos.pes.wait(action=PRE(0x5678))
        # instruction 2 PES:EXEC:NOP
        self.kosmos.pes.delay(delay_ticks=1)
        # instruction 3 PES:SUBDELAY:05
        self.kosmos.pes.delay(delay_ticks=5, action=PAE(0xABC2))
        # instruction 4 PES:SUBDELAY:10
        self.kosmos.pes.delay(delay_ticks=10, action=PAE(0xABC3))
        # instruction 5 PES:DELAY:100
        self.kosmos.pes.delay(delay_ticks=100, action=PAE(0xABC4))
        # instruction 6 PES:MARKER
        self.kosmos.pes.marker(action=0x0321)

        instruction_count = 7
        self.assertEqual(instruction_count, self.kosmos.pes.length())

        # Validate transformation of instruction buffer to MessageFrames
        tx_frames = self.kosmos.pes.messages()
        self.assertEqual(ceil(instruction_count/MSG_PAYLOAD_RAW_UINT32_COUNT), len(tx_frames))
        pes = tx_frames[0].frame.payload.pes

        # instruction 0 PES:EXEC
        self.assertEqual(PES_OPCODE_EXECUTE, pes[0].execute.opcode)
        self.assertEqual(0x1234, pes[0].execute.action_event)
        # instruction 1 PES:WAIT
        self.assertEqual(PES_OPCODE_WAIT, pes[1].wait.opcode)
        self.assertEqual(0x5678, pes[1].wait.resume_event)
        # instruction 2 PES:EXEC:NOP
        self.assertEqual(PES_OPCODE_EXECUTE, pes[2].execute.opcode)
        self.assertEqual(PES_ACTION_EVENT_NOP.value, pes[2].execute.action_event)
        # instruction 3 PES:SUBDELAY:05
        self.assertEqual(PES_OPCODE_SUBDELAY_05_TICKS, pes[3].field.opcode)
        self.assertEqual(0xABC2, pes[3].subdelay.action_event)
        # instruction 4 PES:SUBDELAY:10
        self.assertEqual(PES_OPCODE_SUBDELAY_10_TICKS, pes[4].field.opcode)
        self.assertEqual(0xABC3, pes[4].subdelay.action_event)
        # instruction 5 PES:DELAY:100
        self.assertEqual(0, pes[5].delay.opcode.exponent)
        self.assertEqual(1, pes[5].delay.opcode.mantissa)
        self.assertEqual(0xABC4, pes[5].delay.action_event)
        # instruction 6 PES:MARKER
        self.assertEqual(PES_OPCODE_MARKER, pes[6].marker.opcode)
        self.assertEqual(0x0321, pes[6].marker.operand.raw)

        self.kosmos.pes.clear()
    # end def test_instructions

    def test_pes_action_event_operand(self):
        """
        Test accepted type for PesActionEvent objects.
        """
        # Should PASS
        self.kosmos.pes.execute(action=PAE(0x1234))
        self.kosmos.pes.delay(delay_ticks=1, action=PAE(0xABC2))
        for action_event in self.kosmos.pes.events.action_event:
            self.kosmos.pes.execute(action=action_event)
            self.kosmos.pes.delay(delay_ticks=1, action=action_event)
        # end for

        # Should raise TypeError
        with self.assertRaisesRegex(TypeError, 'PesActionEventBase|PesResumeEventBase'):
            self.kosmos.pes.execute(action=PRE(0x1234))
        # end with
        with self.assertRaisesRegex(TypeError, 'PesActionEventBase|PesResumeEventBase'):
            self.kosmos.pes.delay(delay_ticks=1, action=PRE(0xABC2))
        # end with
        with self.assertRaisesRegex(TypeError, 'PesActionEventBase|PesEventBase'):
            self.kosmos.pes.execute(action=PesEventBase('TEST', 0x42))
        # end with
        with self.assertRaisesRegex(TypeError, 'PesActionEventBase|PesResumeEventBase'):
            self.kosmos.pes.delay(delay_ticks=1, action=PesEventBase('TEST', 0xABC2))
        # end with
        for resume_event in self.kosmos.pes.events.resume_event:
            with self.assertRaisesRegex(TypeError, 'PesActionEventBase|PesResumeEventBase'):
                self.kosmos.pes.execute(action=resume_event)
            # end with
            with self.assertRaisesRegex(TypeError, 'PesActionEventBase|PesResumeEventBase'):
                self.kosmos.pes.delay(delay_ticks=1, action=resume_event)
            # end with
        # end for

        self.kosmos.pes.clear()
    # end def test_pes_action_event_operand

    def test_pes_resume_event_operand(self):
        """
        Test accepted type for PesResumeEvent objects.
        """
        # Should PASS
        self.kosmos.pes.wait(action=PRE(0x5678))
        for resume_event in self.kosmos.pes.events.resume_event:
            self.kosmos.pes.wait(action=resume_event)
        # end for

        # Should raise TypeError
        with self.assertRaisesRegex(TypeError, 'PesResumeEventBase|PesActionEventBase'):
            self.kosmos.pes.wait(action=PAE(0x5678))
        # end with
        with self.assertRaisesRegex(TypeError, 'PesResumeEventBase|PesEventBase'):
            self.kosmos.pes.wait(action=PesEventBase(name='TEST', value=0x42))
        # end with
        for action_event in self.kosmos.pes.events.action_event:
            with self.assertRaisesRegex(TypeError, 'PesResumeEventBase|PesActionEventBase'):
                self.kosmos.pes.wait(action=action_event)
            # end with
        # end for

        self.kosmos.pes.clear()
    # end def test_pes_resume_event_operand

    def test_pes_action_event_direct_call(self):
        """
        Test the shorthand notation to set up a PES Action Event
        """
        # The following call using shorthand notation ...
        self.kosmos.dt.pes.action_event.NOP_EVENT()
        # ... should be equivalent to the standard PES:EXEC:NOP notation
        self.kosmos.dt.pes.execute(action=self.kosmos.dt.pes.action_event.NOP_EVENT)

        # Verify results in buffer
        self.assertEqual(self.kosmos.pes._buffer[1], self.kosmos.pes._buffer[0])  # PES:EXEC:NOP
        self.kosmos.pes.clear()

        # Same as the simple use case above, but across all known PES Action Events
        for action_event in self.kosmos.dt.pes.events.action_event:
            action_event()                                   # using shorthand notation
            self.kosmos.dt.pes.execute(action=action_event)  # standard PES:EXEC notation
            self.assertEqual(self.kosmos.pes._buffer[1], self.kosmos.pes._buffer[0], msg=action_event)
            self.kosmos.pes.clear()
        # end for
    # end def test_pes_action_event_direct_call

    def test_pes_resume_event_direct_call(self):
        """
        Test the shorthand notation to set up a PES Resume Event
        """
        # The following call using shorthand notation ...
        self.kosmos.dt.pes.resume_event.NOP_EVENT()
        # ... should be equivalent to the standard PES:WAIT:NOP notation
        self.kosmos.dt.pes.wait(action=self.kosmos.dt.pes.resume_event.NOP_EVENT)

        # Verify results in buffer
        self.assertEqual(self.kosmos.pes._buffer[1], self.kosmos.pes._buffer[0])  # PES:WAIT:NOP
        self.kosmos.pes.clear()

        # Same as the simple use case above, but across all known PES Resume Events
        for resume_event in self.kosmos.dt.pes.events.resume_event:
            resume_event()                                # using shorthand notation
            self.kosmos.dt.pes.wait(action=resume_event)  # standard PES:WAIT notation
            self.assertEqual(self.kosmos.pes._buffer[1], self.kosmos.pes._buffer[0], msg=resume_event)
            self.kosmos.pes.clear()
        # end for
    # end def test_pes_resume_event_direct_call

    def test_pes_resume_event_led_pin(self):
        """
        Test the initialization of LED PIN resume events
        """
        self.assertEqual(PES_OPERAND_BITS + 1,  # +1 to account for initial NOP event
                         len(self.kosmos.dt.pes.events.resume_event),
                         msg=self.kosmos.dt.pes.events.resume_event)

        for led_pin_index, resume_event in self.kosmos.dt.pes.events.led_pin_resume_events.items():
            self.assertEqual(f'{LED_PIN_EVENT_NAME}{led_pin_index:02}', resume_event.name, msg=resume_event)
            self.assertEqual(f'PES_{LED_PIN_EVENT_NAME}{led_pin_index:02}', resume_event.canonical_name,
                             msg=resume_event)
            self.assertEqual(1 << (led_pin_index - PES_OPERAND_BITS), resume_event.value, msg=resume_event)
            self.assertIs(self.kosmos.dt.pes.events.resume_event[led_pin_index - PES_OPERAND_BITS + 1],
                          resume_event, msg=pretty_list(self.kosmos.dt.pes.events.resume_event))
        # end for
    # end def test_pes_resume_event_led_pin

    def test_delay_instructions(self):
        """
        Validate conversion of a delay duration (given in second or clock tick) into a list of PES instruction.
        """
        ticks_list = [1, 5, 10, 50, 100, 500, 88888, 88888888]

        # Validate nanoseconds against ticks
        for ticks in ticks_list:
            a = self.kosmos.pes.get_delay_instructions(delay_ns=FPGA_CLOCK_PERIOD_NS * ticks)
            b = self.kosmos.pes._get_delay_instructions_from_ticks(ticks=ticks)
            self.assertEqual(ticks, PesModule.get_execution_duration_ticks(a))
            self.assertEqual(a, b)
        # end for

        # Validate seconds against ticks
        for ticks in ticks_list:
            a = self.kosmos.pes.get_delay_instructions(delay_s=FPGA_CLOCK_PERIOD_NS * ticks / 10**9)
            b = self.kosmos.pes._get_delay_instructions_from_ticks(ticks=ticks)
            self.assertEqual(ticks, PesModule.get_execution_duration_ticks(a))
            self.assertEqual(a, b)
        # end for

        # Validate invalid delay duration values
        with self.assertWarnsRegex(UserWarning, f'Effective delay is shorter by {FPGA_CLOCK_PERIOD_NS * .5}'):
            a = self.kosmos.pes.get_delay_instructions(delay_ns=FPGA_CLOCK_PERIOD_NS * 1.5)
            b = self.kosmos.pes.get_delay_instructions(delay_ns=FPGA_CLOCK_PERIOD_NS)
            self.assertEqual(a, b)
        # end with

        # Validate rounding up of delay duration values, no warning should be raised
        with catch_warnings(record=True) as warning_list:
            delay_ns = self.kosmos.pes.roundup_delay_ns_to_clock_period(delay_ns=FPGA_CLOCK_PERIOD_NS * 1.5)
            self.assertEqual(delay_ns, FPGA_CLOCK_PERIOD_NS * 2)
            a = self.kosmos.pes.get_delay_instructions(delay_ns=delay_ns)
            b = self.kosmos.pes.get_delay_instructions(delay_ns=FPGA_CLOCK_PERIOD_NS * 2)
            self.assertEqual(a, b)
            self.assertEqual(0, len(warning_list), msg=warning_list)  # no warning raised
        # end with

        invalid_ticks = [-1, 0, 0.5, 1.5]
        for ticks in invalid_ticks:
            with self.assertRaisesRegex(AssertionError, r'must be a strictly positive integer'):
                self.kosmos.pes._get_delay_instructions_from_ticks(ticks=ticks)
            # end with
        # end for

        self.kosmos.pes.clear()
    # end def test_delay_instructions

    def test_pes_marker_instructions(self):
        """
        Validate `PES_MARKER` enumeration class.
        """
        self.assertEqual(len(PES_MARKER.__members__),
                         len([e for e in pes_isa_marker_operation_e__enumvalues
                              if e not in (PES_ISA_MARKER_OP_RESERVED_BITS, PES_ISA_MARKER_OP_ENUM_MAX_VALUE)]))

        # Validate marker values
        for value in pes_isa_marker_operation_e__enumvalues.keys():
            self.assertEqual(value, PES_MARKER(value))
        # end for

        # Validate marker names
        for flag in PES_MARKER.__members__.values():
            self.assertEqual(f'PES_ISA_MARKER_OP_{flag.name}', pes_isa_marker_operation_e__enumvalues[flag])
        # end for

        # Validate combinations
        marker = PES_MARKER.SAVE_GLOBAL_TIME_MARK
        self.assertEqual(PES_ISA_MARKER_OP_SAVE_GLOBAL_TIME_MARK, marker)

        marker |= PES_ISA_MARKER_OP_RESET_STOPWATCH_2_TIME_MARK
        self.assertEqual(PES_ISA_MARKER_OP_SAVE_GLOBAL_TIME_MARK +
                         PES_ISA_MARKER_OP_RESET_STOPWATCH_2_TIME_MARK, marker)

        marker |= PES_ISA_MARKER_OP_STOPWATCH_2_STOP
        self.assertEqual(PES_ISA_MARKER_OP_SAVE_GLOBAL_TIME_MARK +
                         PES_ISA_MARKER_OP_RESET_STOPWATCH_2_TIME_MARK +
                         PES_ISA_MARKER_OP_STOPWATCH_2_STOP, marker)

        # Validate detection of invalid values
        for value in [-1, PES_ISA_MARKER_OP_ENUM_MAX_VALUE + 1, PES_ISA_MARKER_OP_RESERVED_BITS,
                      PES_ISA_MARKER_OP_SAVE_GLOBAL_TIME_MARK | PES_ISA_MARKER_OP_RESERVED_BITS]:
            with self.assertRaises(AssertionError, msg=f'Input value is {value:#x}.'):
                PesModule.get_marker_instruction(value)
            # end with
            with self.assertRaises(AssertionError, msg=f'Input value is {value:#x}.'):
                PesModule.get_marker_instruction(PES_MARKER(value))
            # end with
        # end for
    # end def test_pes_marker_instructions

    def test_combined_events(self):
        """
        Test passing multiple PES Event at a time.
        This a verification test that does not involve Microblaze/FPGA.
        """
        event_list = []
        expect_bitmask = 0
        for action_event in self.kosmos.dt.pes.events.action_event:
            event_list.append(action_event)
            expect_bitmask |= action_event.value

            self.kosmos.dt.pes.execute(action=event_list)
            self.kosmos.dt.pes.delay(delay_ticks=1, action=event_list)
            self.assertEqual(self.kosmos.dt.pes._buffer[0].action_event, expect_bitmask)
            self.assertEqual(self.kosmos.dt.pes._buffer[1].action_event, expect_bitmask)
            self.kosmos.dt.pes.clear()
        # end for

        event_list = []
        expect_bitmask = 0
        for resume_event in self.kosmos.dt.pes.events.resume_event:
            event_list.append(resume_event)
            expect_bitmask |= resume_event.value

            self.kosmos.dt.pes.wait(action=event_list)
            self.assertEqual(self.kosmos.dt.pes._buffer[0].resume_event, expect_bitmask)
            self.kosmos.dt.pes.clear()
        # end for

        with self.assertRaisesRegex(TypeError, 'PesActionEventBase'):
            self.kosmos.dt.pes.execute(action=(self.kosmos.dt.pes.action_event.NOP_EVENT,
                                               self.kosmos.dt.pes.resume_event.NOP_EVENT))
        # end with

        with self.assertRaisesRegex(TypeError, 'PesResumeEventBase'):
            self.kosmos.dt.pes.wait(action=(self.kosmos.dt.pes.action_event.NOP_EVENT,
                                            self.kosmos.dt.pes.resume_event.NOP_EVENT))
        # end with
    # end def test_combined_events
# end class PesModuleTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
