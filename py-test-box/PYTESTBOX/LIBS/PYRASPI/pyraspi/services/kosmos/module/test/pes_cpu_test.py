#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.test.pes_cpu_test
:brief: Kosmos PES CPU Module Test Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2022/01/05
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from random import getrandbits

from pyraspi.services.kosmos.kosmos import FPGA_CURRENT_CLOCK_FREQ
from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.kosmos.module.pestimer import TIMER
from pyraspi.services.kosmos.module.test.module_test import AbstractTestClass
from pyraspi.services.kosmos.module.test.module_test import require_kosmos_device
from pyraspi.services.kosmos.protocol.generated.messages import PES_CPU_ACTION_BIT
from pyraspi.services.kosmos.protocol.generated.messages import pes_cpu_action_e
from pyraspi.services.kosmos.protocol.generated.messages import pes_cpu_action_t


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
@require_kosmos_device(DeviceName.PES_CPU)
class PesCpuModuleTestCase(AbstractTestClass.UploadModuleInterfaceTestCase):
    """
    Kosmos PES CPU Action Module Test Class.
    """

    @classmethod
    def _get_module_under_test(cls):
        """
        Return the module instance to be tested.
        Override `AbstractTestClass.ModuleInterfaceTestCase._get_module_under_test()`.

        :return: The module instance to be tested.
        :rtype: ``PesCpuModule``
        """
        return cls.kosmos.dt.pes_cpu
    # end def _get_module_under_test

    def test_cpu_events(self):
        """
        Call all PES CPU Events
        """
        for cpu_event in self.kosmos.dt.pes_cpu.cpu_events.cpu_event:
            self.kosmos.dt.timers[TIMER.LOCAL].reset()
            self.kosmos.dt.pes_cpu.action(cpu_event)
            self.kosmos.dt.timers[TIMER.LOCAL].save()
            self.kosmos.dt.sequencer.play_sequence()
            ticks = self.kosmos.dt.timers[TIMER.LOCAL].download()[0]
            duration_us = 10**6 * ticks / FPGA_CURRENT_CLOCK_FREQ
            stat_str = f'{cpu_event} interrupt duration: {ticks} tick, {duration_us} us.'

            # FPGA/Microblaze regression test: check interrupt duration (empirical value)
            self.assertLess(duration_us, 4, stat_str + '\nDid something change on the Microblaze side?')
            print(stat_str)
        # end for
    # end def test_cpu_events

    def test_cpu_event_parameter(self):
        """
        Test passing a parameter with a PES CPU Event.
        This a verification test that does not involve Microblaze/FPGA.
        """
        for cpu_event in self.kosmos.dt.pes_cpu.cpu_events.cpu_event:
            param = getrandbits(PES_CPU_ACTION_BIT)

            self.kosmos.dt.pes_cpu.action(cpu_event=cpu_event)
            self.assertEqual(self.kosmos.dt.pes_cpu._buffer[0].action.raw, cpu_event.event)
            self.assertEqual(self.kosmos.dt.pes_cpu._buffer[0].param, 0)
            self.assertEqual(self.kosmos.dt.pes_cpu._buffer[0],
                             pes_cpu_action_t(module=cpu_event.module_id,
                                              action=pes_cpu_action_e(raw=cpu_event.event),
                                              param=0))
            self.kosmos.dt.pes_cpu.clear()

            self.kosmos.dt.pes_cpu.action(cpu_event=cpu_event.with_param(param))
            self.assertEqual(self.kosmos.dt.pes_cpu._buffer[0].action.raw, cpu_event.event)
            self.assertEqual(self.kosmos.dt.pes_cpu._buffer[0].param, param)
            self.assertEqual(self.kosmos.dt.pes_cpu._buffer[0],
                             pes_cpu_action_t(module=cpu_event.module_id,
                                              action=pes_cpu_action_e(raw=cpu_event.event),
                                              param=param))
            self.kosmos.dt.pes_cpu.clear()
        # end for
        self.kosmos.dt.pes.clear()
    # end def test_cpu_event_parameter

    def test_pes_cpu_event_direct_call(self):
        """
        Test the shorthand notation to set up a PES CPU Event
        """
        # The following call using shorthand notation ...
        self.kosmos.dt.pes_cpu.cpu_event.NOP_EVENT()
        # ... should be equivalent to the standard PES_CPU notation
        self.kosmos.dt.pes_cpu.action(cpu_event=self.kosmos.dt.pes_cpu.cpu_event.NOP_EVENT)

        # Verify results in buffer
        self.assertEqual(self.kosmos.pes._buffer[2], self.kosmos.pes._buffer[0])  # PES:EXEC:CPU_REQ
        self.assertEqual(self.kosmos.pes._buffer[3], self.kosmos.pes._buffer[1])  # PES:WAIT:CPU_RET
        self.assertEqual(self.kosmos.pes_cpu._buffer[1], self.kosmos.pes_cpu._buffer[0])  # PES_CPU:NOP
        self.kosmos.pes_cpu.clear()

        # Same as the simple use case above, but across all known PES CPU Events
        for cpu_event in self.kosmos.dt.pes_cpu.cpu_events.cpu_event:
            cpu_event()                                         # using shorthand notation
            self.kosmos.dt.pes_cpu.action(cpu_event=cpu_event)  # standard PES_CPU notation
            # Verify results in buffer
            self.assertEqual(self.kosmos.pes_cpu._buffer[1], self.kosmos.pes_cpu._buffer[0], msg=cpu_event)
            self.kosmos.pes_cpu.clear()
        # end for

        # Repeat test using a PES CPU Event parameter
        for cpu_event in self.kosmos.dt.pes_cpu.cpu_events.cpu_event:
            param = getrandbits(PES_CPU_ACTION_BIT)
            cpu_event.with_param(param=param)()                                         # using shorthand notation #1
            cpu_event(param=param)                                                      # using shorthand notation #2
            self.kosmos.dt.pes_cpu.action(cpu_event=cpu_event.with_param(param=param))  # standard PES_CPU notation
            # Verify results in buffer
            self.assertEqual(self.kosmos.pes_cpu._buffer[2], self.kosmos.pes_cpu._buffer[0], msg=cpu_event)
            self.assertEqual(self.kosmos.pes_cpu._buffer[2], self.kosmos.pes_cpu._buffer[1], msg=cpu_event)
            self.kosmos.pes_cpu.clear()
        # end for
        self.kosmos.pes.clear()
    # end def test_pes_cpu_event_direct_call
# end class PesCpuModuleTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
