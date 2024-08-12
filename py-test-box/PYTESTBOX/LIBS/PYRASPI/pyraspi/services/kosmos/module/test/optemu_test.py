#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.test.optemu_test
:brief: Kosmos Optical Sensor Emulator Module Test Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2023/03/28
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABCMeta
from abc import abstractmethod
from ctypes import c_uint16
from dataclasses import asdict
from dataclasses import astuple
from dataclasses import dataclass
from enum import Enum
from enum import IntFlag
from itertools import chain
from itertools import count
from random import gauss
from random import randint
from statistics import mean
from statistics import stdev
from textwrap import indent
from time import perf_counter
from time import sleep
from typing import Dict
from typing import Generator
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union

from pylibrary.emulator.emulatorinterfaces import SEQUENCER_TIMEOUT_S
from pylibrary.tools.util import NotImplementedAbstractMethodError
from pyraspi.services.kosmos.buttonemulator import KosmosButtonEmulator
from pyraspi.services.kosmos.kosmos import FPGA_CURRENT_CLOCK_FREQ
from pyraspi.services.kosmos.module.model.optemu.base import OptEmuRegisterMapBase
from pyraspi.services.kosmos.module.model.registermap import MaskedRegister
from pyraspi.services.kosmos.module.model.registermap import Register
from pyraspi.services.kosmos.module.model.registermap import reg_val_type
from pyraspi.services.kosmos.module.optemu import Action
from pyraspi.services.kosmos.module.optemu import OptEmuModuleMixin
from pyraspi.services.kosmos.module.optemu_12bits import OptEmu12BitsModuleMixin
from pyraspi.services.kosmos.module.optemu_16bits import OptEmu16BitsModuleMixin
from pyraspi.services.kosmos.module.pestimer import TIMER
from pyraspi.services.kosmos.module.test.module_test import AbstractTestClass
from pyraspi.services.kosmos.powerslideremulator import KosmosPowerSliderEmulator
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_DAC_CH_ALL
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_SEL_DAC_0
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_SEL_DAC_1
from pyraspi.services.kosmos.protocol.generated.messages import OPT_EMU_CMP_DX_MAX
from pyraspi.services.kosmos.protocol.generated.messages import OPT_EMU_CMP_DX_MIN
from pyraspi.services.kosmos.protocol.generated.messages import opt_emu_data_t
from pyraspi.services.kosmos.test.keymatrixemulator_test import KBD_FW_ID
from pyraspi.services.kosmos.utils import all_permutations
from pyraspi.services.kosmos.utils import pretty_dict


# ------------------------------------------------------------------------------
# Test case utils
# ------------------------------------------------------------------------------


class IDEM:
    """
    Token used in ``TestBase`` class to indicate Compressed instructions list is the same the Raw instructions list.
    """
    pass
# end class IDEM


@dataclass
class TestBase(metaclass=ABCMeta):
    """
    Dataclass representing test case input/output expectations.
    """
    # Test outputs
    o_raw: List[opt_emu_data_t]  # Expected RAW instruction list
    o_cmp: Union[List[opt_emu_data_t], Type[IDEM]]  # Set to `IDEM` to indicate Compressed instructions are same a Raw
# end class TestBase


@dataclass
class HighLevelInput:
    """
    Dataclass representing a High-level test case input data.
    """
    # Test inputs
    action: Action
    value: Union[int, bool, None]
# end class HighLevelInput


@dataclass
class HighLevelTest(TestBase):
    """
    Dataclass representing High-level test case input/output expectations.
    """
    # Test inputs: Action map
    i_actions: List[HighLevelInput]
# end class HighLevelTest


@dataclass
class LowLevelInput:
    """
    Dataclass representing a Low-level test case input data.
    """
    # Test inputs: Register
    addr: int
    val: Optional[reg_val_type]
    mask: int
# end class LowLevelInput


@dataclass
class LowLevelTest(TestBase):
    """
    Dataclass representing Low-level test case input/output expectations.
    """
    # Test inputs: Register list
    i_reg: List[LowLevelInput]
# end class LowLevelTest


# ------------------------------------------------------------------------------
# Test case implementation
# ------------------------------------------------------------------------------
class OptEmuAbstractTestClass:
    """
    This class is used to wrap Abstract TestCase classes, so that they cannot be automatically discovered
    and executed by test executors (unittest, pytest...).

    Refer to ``pyraspi.services.kosmos.module.test.module_test.AbstractTestClass``
    """

    class OptEmuTestCaseMixin(AbstractTestClass.UploadModuleInterfaceTestCase, metaclass=ABCMeta):
        """
        Kosmos Optical Sensor Emulator Module Test Class Mixin.
        """
        # Update type hints
        module: OptEmuModuleMixin

        _slider_emulator: KosmosPowerSliderEmulator
        _button_emulator: KosmosButtonEmulator

        # Test expectations
        instruction_count: int = 0
        update_count: int = 0
        duration_s: float = 0.0

        # Constants that must be set in derived class
        dut_vcc_sensor: float  # Volts
        dut_sensor_polling_frequency_hz: float  # Hertz
        sensor_power_up_to_reset_done_time_s: float  # Seconds
        sensor_power_up_to_setup_done_time_s: float  # Seconds

        def __init__(self, *args, **kwargs):
            """
            :param args: Positional arguments, for ``TestCase.__init__`` method
            :type args: ``tuple[Any]``
            :param kwargs: Keyword arguments, for ``TestCase.__init__`` method
            :type kwargs: ``dict[str, Any]``

            :raise ``AssertionError``: Invalid object attribute type
            """
            super().__init__(*args, **kwargs)

            assert isinstance(self.dut_vcc_sensor, (int, float)) \
                   and self.dut_vcc_sensor > 0, \
                   'DUT sensor power line voltage must be set in derived class'

            assert isinstance(self.dut_sensor_polling_frequency_hz, (int, float)) \
                   and self.dut_sensor_polling_frequency_hz > 0, \
                   'DUT sensor polling frequency must be set in derived class'

            assert isinstance(self.sensor_power_up_to_setup_done_time_s, float) \
                   and self.sensor_power_up_to_setup_done_time_s > 0, \
                   'Sensor Power-Up to Setup-done timing must be set in derived class'

            # Register custom equality test method for Optical Sensor Emulator instruction type
            self.addTypeEqualityFunc(typeobj=opt_emu_data_t, function='assert_instr_eq')
        # end def __init__

        @classmethod
        def setUpClass(cls):
            """
            Set up module test class

            :raise ``AssertionError``: Invalid module type
            """
            super().setUpClass()
            assert isinstance(cls.module, OptEmuModuleMixin), cls.module
            assert isinstance(cls.module.settings.reg_map, OptEmuRegisterMapBase), cls.reg_map

            cls._slider_emulator = KosmosPowerSliderEmulator(kosmos=cls.kosmos, fw_id=KBD_FW_ID)
            cls._button_emulator = KosmosButtonEmulator(kosmos=cls.kosmos, fw_id='MPM25')

            # First, power off the DUT (emulator initialization MUST be done before DUT is powered on)
            cls._slider_emulator.power_off()
            cls._button_emulator.release_all()
            sleep(0.1)

            # Then, send soft-reset command to sensor emulator module, to reset its state machines and emulated memories
            # This will also reset the Optical Emulator Low-level Control class.
            cls.module.reset_module()
        # end def setUpClass

        def setUp(self):
            """
            Setup Test Case
            """
            super().setUp()
            self.reset_test_expectations()

            # By default, enable conversion from Raw to Compressed instructions, whenever this is possible
            self.module.ll_ctrl.compress = True

            # Finally prepare and send the test sequence:  (refer to test method `test_square_pattern_with_pes()`)
            #  - power on the DUT
            #  - OPTIONAL STEPS:
            #    - wait for the DUT sensor setup done
            #    - start the sensor FIFO
            #    - wait for FIFO emtpy
            #    - stop the sensor FIFO
            #    - reset the sensor
        # end def setUp

        def tearDown(self):
            """
            Tear Down Test Case
            """
            try:
                super().tearDown()
            finally:
                # First, power off the DUT (emulator initialization MUST be done before DUT is powered on)
                self._slider_emulator.power_off()
                self._button_emulator.release_all()
                sleep(0.1)

                # Then, send soft-reset command to sensor emulator module, to reset its state machines and emulated memories
                # This will also reset the Optical Emulator Low-level Control class.
                self.module.reset_module()
            # end try
        # end def tearDown

        def assert_instr_eq(self, expected, actual, msg=None):
            """
            Test two Optical Sensor Emulator instructions for equality.

            Note: Use ``OptEmuTestCaseMixin.assertEqual(expected, actual, msg)`` method instead,
                  as the present method was registered through the TestCase class, for ``opt_emu_data_t`` type operands.
                  Refer to ``OptEmuTestCaseMixin.__init__`` method.

            :param expected: Expected Optical Sensor Emulator instruction
            :type expected: ``opt_emu_data_t``
            :param actual: Actual Optical Sensor Emulator instruction
            :type actual: ``opt_emu_data_t``
            :param msg: Error message prefix, defaults to None - OPTIONAL
            :type msg: ``None``

            :raise ``self.failureException``: if `expected` instruction differs from `actual` instruction
            """
            if not expected == actual:
                msg = f'{msg}\n' if msg else ''
                msg = f'{msg}Optical Sensor Emulator instructions do not match:\n' \
                      f'EXPECT: {self.module.instruction_to_str(expected)}\n' \
                      f'ACTUAL: {self.module.instruction_to_str(actual)}'
                raise self.failureException(msg)
            # end if
        # end def assert_instr_eq

        def reset_test_expectations(self):
            """
            Test case utility: Reset test case expectations variables.
            """
            self.instruction_count = 0
            self.update_count = 0
            self.duration_s = 0.0
        # end def reset_test_expectations

        def update_test_expectations(self, new_update_count=0):
            """
            Test case utility: Update test case expectations variables.

            :param new_update_count: Expected new upate count, defaults to 0 - OPTIONAL
            :type new_update_count: ``int``
            """
            self.instruction_count = self.module.length()
            self.update_count += new_update_count
            self.duration_s = self.update_count / self.dut_sensor_polling_frequency_hz
        # end def update_test_expectations

        def setup_square_pattern(self, side_length, increment=1, loop_count=1):
            """
            Generate Optical Sensor Emulator Delta X/Y instructions to simulate mouse movements drawing squares.
            Send the instruction to the local buffer.

            :param side_length: length of the square pattern, in sensor pixel unit
            :type side_length: ``int``
            :param increment: XY displacement increment absolute value - OPTIONAL
            :type increment: ``int``
            :param loop_count: number of square revolution to draw - OPTIONAL
            :type loop_count: ``int``
            """
            # Shorthand notations
            hl = self.module.hl_ctrl

            # ========= TEST STEPS =========

            # Create buffer of square motions
            for loop in range(loop_count):
                for side in range(side_length):
                    hl.update(action=Action.DX, value=+increment)   # Positive Delta X motion
                    hl.commit()
                # end for
                for side in range(side_length):
                    hl.update(action=Action.DY, value=+increment)   # Positive Delta Y motion
                    hl.commit()
                # end for
                for side in range(side_length):
                    hl.update(action=Action.DX, value=-increment)   # Negative Delta X motion
                    hl.commit()
                # end for
                for side in range(side_length):
                    hl.update(action=Action.DY, value=-increment)   # Negative Delta Y motion
                    hl.commit()
                # end for
            # end for

            # ========= TEST EXPECTATIONS =========

            self.update_test_expectations(new_update_count=4 * side_length * loop_count)
        # end def setup_square_pattern

        def setup_spiral_pattern(self, final_length=1, loop_count=1):
            """
            Generate Optical Sensor Emulator Delta X/Y instructions to simulate mouse movements drawing a spiral.
            Send the instruction to the local buffer.

            :param final_length: length of the last drawn spiral segment, in sensor pixel unit - OPTIONAL
            :type final_length: ``int``
            :param loop_count: number of spiral revolution to draw - OPTIONAL
            :type loop_count: ``int``
            """
            # Shorthand notations
            hl = self.module.hl_ctrl

            # ========= TEST STEPS =========

            # Create buffer of square motions
            for loop in range(loop_count):
                for increment in range(1, final_length + 1):
                    hl.update(action=Action.DX, value=+increment)   # Positive Delta X motion
                    hl.commit()

                    hl.update(action=Action.DY, value=+increment)   # Positive Delta Y motion
                    hl.commit()

                    hl.update(action=Action.DX, value=-increment)   # Negative Delta X motion
                    hl.commit()

                    hl.update(action=Action.DY, value=-increment)   # Negative Delta Y motion
                    hl.commit()
                # end for
            # end for

            # ========= TEST EXPECTATIONS =========

            self.update_test_expectations(new_update_count=4 * final_length * loop_count)
        # end def setup_spiral_pattern

        def setup_octagon_pattern(self, final_length, loop_count=1):
            """
            Generate Optical Sensor Emulator Delta X/Y instructions to simulate mouse movements drawing octagons.
            Send the instruction to the local buffer.

            :param final_length: length of the last drawn octagon segment, in sensor pixel unit - OPTIONAL
            :type final_length: ``int``
            :param loop_count: number of octagon revolution to draw, defaults to 1 - OPTIONAL
            :type loop_count: ``int``
            """
            # Shorthand notations
            hl = self.module.hl_ctrl

            # ========= TEST STEPS =========

            # Create buffer of square motions
            for loop in range(loop_count):
                for increment in range(1, final_length + 1):
                    hl.update(action=Action.DX, value=+increment)   # Positive Delta X motion
                    hl.commit()

                    hl.update(action=Action.DX, value=+increment)   # Positive Delta X motion
                    hl.update(action=Action.DY, value=+increment)   # Positive Delta Y motion
                    hl.commit()

                    hl.update(action=Action.DY, value=+increment)   # Positive Delta Y motion
                    hl.commit()

                    hl.update(action=Action.DY, value=+increment)   # Positive Delta Y motion
                    hl.update(action=Action.DX, value=-increment)   # Negative Delta X motion
                    hl.commit()

                    hl.update(action=Action.DX, value=-increment)   # Negative Delta X motion
                    hl.commit()

                    hl.update(action=Action.DX, value=-increment)   # Negative Delta X motion
                    hl.update(action=Action.DY, value=-increment)   # Negative Delta Y motion
                    hl.commit()

                    hl.update(action=Action.DY, value=-increment)   # Negative Delta Y motion
                    hl.commit()

                    hl.update(action=Action.DY, value=-increment)   # Negative Delta Y motion
                    hl.update(action=Action.DX, value=+increment)   # Positive Delta X motion
                    hl.commit()
                # end for
            # end for

            # ========= TEST EXPECTATIONS =========

            self.update_test_expectations(new_update_count=8 * final_length * loop_count)
        # end def setup_octagon_pattern

        def test_square_pattern_without_pes(self):
            """
            Validate manual usage of the Optical Sensor Emulator module, without using PES Sequencer.

            Validate the following methods:
             - ``start_emulator()``
            """
            # Check initial expectations
            status = self.module.status()
            self.assertEqual(0, status.buffer_count, msg=status)
            self.assertEqual(0, status.fifo_count, msg=status)
            self.assertEqual(0, status.fifo_underrun, msg=status)
            self.assertEqual(0, status.fifo_en, msg=status)
            self.assertEqual(0, status.setup_done, msg=status)
            self.assertEqual(0, status.update_count, msg=status)

            # Turn DUT power slider ON
            self._slider_emulator.power_on()

            # Loop until DUT finished setting up the emulated sensor
            status = self.module.status()
            time_start = perf_counter()
            while not status.setup_done and (perf_counter() - time_start) < 1:  # 1 second timeout
                status = self.module.status()
            # end while
            self.assertEqual(1, status.setup_done,
                             msg=f'Timeout waiting for Sensor Emulator Setup Done flag.\n{status}')

            # Create buffer of square motions
            self.setup_square_pattern(side_length=10, loop_count=3)

            # Without using PES sequencer, the buffer has to be sent manually
            self.module.send(clear=True)

            # Check pre-start expectations
            status = self.module.status()
            self.assertEqual(self.update_count, status.buffer_count + status.fifo_count, msg=status)
            self.assertEqual(0, status.fifo_count, msg=status)
            self.assertEqual(0, status.fifo_underrun, msg=status)
            self.assertEqual(0, status.fifo_en, msg=status)
            self.assertEqual(0, status.update_count, msg=status)

            # Start emulated sensor updates
            status = self.module.start_emulator()
            self.assertEqual(1, status.fifo_en, msg=status)

            # Loop until no more data is left in buffer and FIFO
            time_start = perf_counter()
            while (status.fifo_count or status.buffer_count) and (perf_counter() - time_start) < 1:  # 1 second timeout
                status = self.module.status()
            # end while
            self.assertFalse(status.fifo_count or status.buffer_count,
                             msg=f'Timeout waiting for Sensor Emulator data consumed.\n{status}')

            # Wait until last item read from fifo get consumed, then wait until next sensor data polling to trigger underrun
            sleep(2/self.dut_sensor_polling_frequency_hz)
            status = self.module.status()

            # Turn DUT power slider OFF
            self._slider_emulator.power_off()

            # Check FIFO underrun was raised soon after FIFO got empty
            self.assertEqual(0, status.buffer_count, msg=status)
            self.assertEqual(0, status.fifo_count, msg=status)
            self.assertEqual(1, status.fifo_underrun, msg=status)
            self.assertEqual(0, status.fifo_en, msg=status)
            self.assertEqual(self.update_count, status.update_count, msg=status)
        # end def test_square_pattern_without_pes

        def test_without_pes_manual_start_stop(self):
            """
            Validate manual usage of the Optical Sensor Emulator module, without using PES Sequencer.

            Validate the following methods:
             - ``start_emulator()``
             - ``stop_emulator()``
            """
            # Turn DUT power slider ON
            self._slider_emulator.power_on()

            # Create buffer of square motions, 100 pixels wide, repeated 5 times
            self.setup_square_pattern(side_length=100, loop_count=5)

            # Without using PES sequencer, the buffer has to be sent manually
            self.module.send(clear=True)

            # Enable motion emulation
            self.module.start_emulator()

            # Wait for first half of expected sequence duration
            sleep(self.duration_s / 2)

            # Pause motion emulation
            status = self.module.stop_emulator()

            # Approx. half of the samples should have been processed (verification delta arbitrarily set to +/-10%)
            self.assertAlmostEqual(self.instruction_count // 2, status.buffer_count,
                                   delta=self.instruction_count // 10, msg=status)
            self.assertAlmostEqual(self.update_count // 2, status.update_count,
                                   delta=self.update_count // 10, msg=status)
            self.assertEqual(0, status.fifo_underrun, msg=status)
            self.assertEqual(0, status.fifo_en, msg=status)

            # Wait a moment to observe that there is no Model Data update when Emulator gets stopped (FIFO disabled)
            sleep(10/self.dut_sensor_polling_frequency_hz)
            status_2 = self.module.status()
            self.assertEqual(status.update_count, status_2.update_count, msg=(status, status_2))

            # Restart motion emulation
            status = self.module.start_emulator()
            self.assertEqual(1, status.fifo_en, msg=status)

            # Loop until FIFO underrun is triggered
            while not status.fifo_underrun:
                status = self.module.status()
            # end while

            # Turn DUT power slider OFF
            self._slider_emulator.power_off()

            # Check module buffer and fifo are empty
            self.assertEqual(0, status.buffer_count, msg=status)
            self.assertEqual(0, status.fifo_count, msg=status)
            self.assertEqual(0, status.fifo_en, msg=status)
            self.assertEqual(self.update_count, status.update_count, msg=status)
        # end def test_without_pes_manual_start_stop

        def test_square_pattern_with_pes(self):
            """
            Validate standard usage of the Optical Sensor Emulator module, using PES Sequencer.

            Validate the following PES Action & Resume Events:
             - ``OptEmuModuleMixin.ResumeEvent.SETUP_DONE``
             - ``OptEmuModuleMixin.ActionEvent.START``
             - ``OptEmuModuleMixin.ResumeEvent.FIFO_EMPTY``
             - ``OptEmuModuleMixin.ActionEvent.STOP``
             - ``OptEmuModuleMixin.ActionEvent.RESET``
            """
            # Create buffer of motions
            self.setup_square_pattern(side_length=10, loop_count=10)
            self.setup_spiral_pattern(final_length=10, loop_count=10)
            self.setup_octagon_pattern(final_length=10, loop_count=10)

            print(self.module.instructions_to_str())

            # Timer used to verify time spent between Continuous Flashing mode enabled and FIFO empty
            tm = TIMER.STOPWATCH_1

            # PREPARE TEST SEQUENCE
            self.kosmos.sequencer.offline_mode = True
            # Turn DUT power slider ON
            self._slider_emulator.power_on()

            # Wait until Sensor Emulator finishes being configured by the DUT
            self.kosmos.pes.wait(action=self.module.resume_event.SETUP_DONE)
            # self.kosmos.pes.delay(delay_s=0.1)

            # Start Sensor Emulator model update
            self.kosmos.pes.execute(action=self.module.action_event.START)
            self.kosmos.timers[tm].restart()

            # Wait until Sensor Emulator finishes its sequence
            self.kosmos.pes.wait(action=self.module.resume_event.FIFO_UNDERRUN)
            self.kosmos.timers[tm].save()

            # Turn DUT power slider OFF
            self._slider_emulator.power_off()

            self.kosmos.sequencer.offline_mode = False

            # RUN TEST SEQUENCE
            self.kosmos.sequencer.play_sequence()

            # VERIFY end of test expectations
            status = self.module.status()
            self.assertEqual(0, status.buffer_count, msg=status)
            self.assertEqual(0, status.fifo_count, msg=status)
            self.assertEqual(1, status.fifo_underrun, msg=status)
            self.assertEqual(0, status.fifo_en, msg=status)
            self.assertEqual(self.update_count, status.update_count, msg=status)

            # VERIFY time spent between Continuous Flashing mode enabled and FIFO empty
            # A delta of 10% of expected duration is required to account for DUT sensor clock drift and main-loop jitter
            tm_data = self.kosmos.timers[tm].download()
            measured_duration_s = tm_data[0] / FPGA_CURRENT_CLOCK_FREQ
            self.assertAlmostEqual(self.duration_s, measured_duration_s, delta=self.duration_s * 0.10)
        # end def test_square_pattern_with_pes

        def test_dut_reset_during_emulator_operation(self):
            """
            Validate the behavior of the Emulator when the DUT power cycles and the Sensor initialization sequence is
            repeated.

            Validate the following features:
             - Sensor Model update count
            """
            # Shorthand notation
            round_s = self.kosmos.pes.roundup_delay_s_to_clock_period
            tm = TIMER.STOPWATCH_1  # Timer used to verify time spent between 'Power Up' and 'Setup Done' events.

            # Accumulate measurements: Power Up to Setup Done timings for each power_cycle_count test
            measurements: Dict[int, List[int]] = {}

            for power_cycle_count in range(10):
                # Create buffer of square motions, 50 pixels wide, repeated once
                self.setup_square_pattern(side_length=50, loop_count=1)

                # PREPARE TEST SEQUENCE
                self.kosmos.sequencer.offline_mode = True
                # Turn DUT power slider ON
                self._slider_emulator.power_on()

                # Wait until Sensor Emulator finishes being configured by the DUT
                self.kosmos.pes.wait(action=self.module.resume_event.SETUP_DONE)
                # Start Sensor Emulator model update
                self.kosmos.pes.execute(action=self.module.action_event.START)

                for i in range(power_cycle_count):
                    # Wait one third of Sequence
                    delay_s = round_s(self.duration_s / (power_cycle_count + 1))
                    self.kosmos.pes.delay(delay_s=delay_s)

                    # Power cycle DUT
                    self._slider_emulator.power_off()
                    self.kosmos.pes.delay(delay_s=0.1)
                    self._slider_emulator.power_on()

                    # Measure time spent between 'Power Up' and 'Setup Done' events.
                    self.kosmos.timers[tm].restart()
                    # Wait for DUT reset, after DUT power up, plus 10% margin
                    delay_s = round_s(self.sensor_power_up_to_reset_done_time_s * 1.1)
                    self.kosmos.pes.delay(delay_s=delay_s)
                    # Wait for DUT end of configuration (setup done)
                    self.kosmos.pes.wait(action=self.module.resume_event.SETUP_DONE)
                    self.kosmos.timers[tm].save()
                # end for

                # Wait until Sensor Emulator finishes its sequence
                self.kosmos.pes.wait(action=self.module.resume_event.FIFO_UNDERRUN)

                self.kosmos.sequencer.offline_mode = False

                # RUN TEST SEQUENCE
                self.kosmos.sequencer.play_sequence()

                # VERIFY end of test expectations
                status = self.module.status()
                self.assertEqual(1, status.setup_done, msg=status)
                self.assertEqual(0, status.fifo_en, msg=status)
                self.assertEqual(1, status.fifo_underrun, msg=status)
                self.assertEqual(0, status.buffer_overrun, msg=status)
                self.assertEqual(0, status.fifo_count, msg=status)
                self.assertEqual(0, status.buffer_count, msg=status)
                self.assertEqual(0, status.fifo_count, msg=status)
                self.assertEqual(self.update_count, status.update_count, msg=status)

                # VERIFY time spent between DUT Power Up event and sensor SETUP_DONE event
                # (verify step moved to end of test)
                tm_data = self.kosmos.timers[tm].download()
                measured_duration_s = [t / FPGA_CURRENT_CLOCK_FREQ for t in tm_data]
                measurements[power_cycle_count] = measured_duration_s

                # Turn DUT power slider OFF
                self._slider_emulator.power_off()

                # TEST CLEANUP
                self.module.reset_module()
                self.reset_test_expectations()
                sleep(0.2)
            # end for

            all_measurements = list(chain.from_iterable(measurements.values()))
            t_mean = mean(all_measurements)
            t_min = min(all_measurements)
            t_max = max(all_measurements)
            t_stdev = stdev(all_measurements)
            t_delta = max(abs(t_mean - t_min), abs(t_mean - t_max))
            stats = (f'All measured durations "Power-Up to Setup-Done", for each test cycle [s]:\n'
                     f'{pretty_dict(measurements)}\n'
                     f'mean : {t_mean:8.4f} [s]\n'
                     f'min  : {t_min:8.4f} [s]\n'
                     f'max  : {t_max:8.4f} [s]\n'
                     f'stdev: {t_stdev:8.4f} [s]\n'
                     f'delta: {t_delta:8.4f} [s]\n')

            # VERIFY time spent between DUT Power Up event and sensor SETUP_DONE event
            # A delta of 10% of expected duration is required to account for DUT sensor clock drift and main-loop jitter
            for power_cycle_count, measured_duration_s in measurements.items():
                for i in range(power_cycle_count):
                    self.assertAlmostEqual(self.sensor_power_up_to_setup_done_time_s, measured_duration_s[i],
                                           delta=self.sensor_power_up_to_setup_done_time_s * 0.10,
                                           msg=f'Power cycles count: total={power_cycle_count}, current={i}.\n'
                                               f'Stats:\n{stats}')
                # end for
            # end for

            self.printd(f'Stats:\n{stats}')
        # end def test_dut_reset_during_emulator_operation

        def test_reset_event_during_test_sequence(self):
            """
            Validate full behavior of RESET event, in the middle of a test sequence.
            """
            # Create buffer of square motions, 100 pixels wide, repeated 5 times
            self.setup_square_pattern(side_length=100, loop_count=5)

            # PREPARE TEST SEQUENCE
            self.kosmos.sequencer.offline_mode = True
            # Soft-reset sensor emulator
            self.kosmos.pes.execute(action=self.module.action_event.RESET)
            # Turn DUT power slider ON
            self._slider_emulator.power_on()
            # Wait until Sensor Emulator finishes being configured by the DUT
            self.kosmos.pes.wait(action=self.module.resume_event.SETUP_DONE)
            # Start Sensor Emulator model update
            self.kosmos.pes.execute(action=self.module.action_event.START)
            # Force emulator reset right after beginning the test sequence
            self.kosmos.pes.delay(delay_s=1, action=self.module.action_event.RESET)

            # RUN TEST SEQUENCE
            self.kosmos.sequencer.offline_mode = False
            self.kosmos.sequencer.play_sequence()

            # Check early reset expectations
            status = self.module.status()
            self.assertLess(0, status.buffer_count, msg=status)
            self.assertEqual(0, status.fifo_en, msg=status)
            self.assertEqual(0, status.fifo_underrun, msg=status)

            # Send soft-reset command to sensor emulator
            self.module.reset_module()

            # Check soft-reset expectations
            status = self.module.status()
            self.assertEqual(0, status.buffer_count, msg=status)
            self.assertEqual(0, status.fifo_count, msg=status)
            self.assertEqual(0, status.fifo_en, msg=status)
            self.assertEqual(0, status.fifo_underrun, msg=status)
            self.assertEqual(0, status.setup_done, msg=status)
            self.assertEqual(0, status.update_count, msg=status)
        # end def test_reset_event_during_test_sequence

        def test_fifo_reset_behavior(self):
            """
            Validate reset behavior: FIFO reset is triggered by the module RESET event, which leads to potential data loss.

            The current FPGA module implementation will reset the FIFO when the module RESET event is executed by PES.
            That means that inserting a module RESET event after sequence init will discard the first 31 module instructions
            (31 is the FIFO max content size).
            I am not sure if this is a bug or a feature, so I wrote this test to prove the existence of this behavior.

            For now, I would recommend to call `reset_module()` on the module before calling `sequencer.play_sequencer()`.
            Executing a module RESET PES Action Event is not recommended for the majority of use cases.
            """
            # Create buffer of square motions, 100 pixels wide, repeated once
            self.setup_square_pattern(side_length=100, loop_count=1)

            # PREPARE TEST SEQUENCE
            self.kosmos.sequencer.offline_mode = True
            # P1: Pause sequencer to evaluate module status before RESET command is executed
            self.kosmos.pes.wait(action=self.kosmos.dt.pes.resume_event.GO_RPI)
            # Soft-reset sensor emulator
            self.kosmos.pes.execute(action=self.module.action_event.RESET)
            # P2: Pause sequencer to evaluate module status after RESET command is executed
            self.kosmos.pes.wait(action=self.kosmos.dt.pes.resume_event.GO_RPI)

            # RUN TEST SEQUENCE
            self.kosmos.sequencer.offline_mode = False
            self.kosmos.sequencer.play_sequence(block=False)

            # P1: VERIFY module status, before RESET event
            status = self.module.status()
            self.assertEqual(0, status.setup_done, msg=status)
            self.assertEqual(0, status.fifo_en, msg=status)
            self.assertEqual(0, status.fifo_underrun, msg=status)
            self.assertEqual(0, status.buffer_overrun, msg=status)
            self.assertEqual(0, status.update_count, msg=status)
            self.assertEqual(self.module.settings.fifo_size, status.fifo_count, msg=status)
            self.assertEqual(self.instruction_count, status.buffer_count + status.fifo_count, msg=status)

            # Resume test sequence execution
            self.kosmos.dt.fpga.pulse_global_go_line()

            # P2: VERIFY module status, after RESET event
            status = self.module.status()
            self.assertEqual(0, status.setup_done, msg=status)
            self.assertEqual(0, status.fifo_en, msg=status)
            self.assertEqual(0, status.fifo_underrun, msg=status)
            self.assertEqual(0, status.buffer_overrun, msg=status)
            self.assertEqual(0, status.update_count, msg=status)
            self.assertEqual(self.module.settings.fifo_size, status.fifo_count, msg=status)
            self.assertEqual(self.instruction_count - 2 * status.fifo_count, status.buffer_count, msg=status)

            # Abort test sequence execution
            self.kosmos.dt.sequencer.reset_module()     # Reset Sequencer and Kosmos base modules
            self.module.reset_module()                  # Reset Optical Sensor Emulator module
        # end def test_fifo_reset_behavior

        def test_fifo_underrun_during_model_update(self):
            """
            Validate underrun behavior: if a FIFO underrun is raised during a Model data update, the Model data will not be
            committed to the emulated registers.
            """
            # Shorthand notations
            hl = self.module.hl_ctrl

            # ========= TEST STEPS =========

            # Create buffer of two arbitrary XY displacements, using RAW data format
            hl.update(action=Action.DX, value=0x123)
            hl.commit()

            hl.update(action=Action.DX, value=0x456)
            hl.commit()

            # Alter last instruction in buffer: clear RAW send bit, so that last update in hardware can never be fulfilled
            last_instr = self.module._buffer[-1]
            self.assertTrue(last_instr.raw.send, msg=self.module.instruction_to_str(last_instr))
            last_instr.raw.send = False

            # Update test expectations
            self.update_count = 1  # only one sensor update out of two should be counted

            # ========= RUN TEST SEQUENCE ON HARDWARE =========

            self.run_test_sequence()
        # end def test_fifo_underrun_during_model_update

        def test_ll_ctrl(self):
            """
            Validate Low-level Control State Updates
            """
            # Shorthand notations
            raw = self.module.get_raw_instruction
            cmp = self.module.get_compressed_instruction
            reg_map = self.module.ll_ctrl.reg_map
            r = self.module.ll_ctrl.reg_map.Registers
            t = self.module.ll_ctrl.reg_map.Types
            c = self.module.ll_ctrl.reg_map.Commands
            T = LowLevelTest
            IN = LowLevelInput

            tests: List[List[LowLevelTest]] = []
            direct_registers: Generator[Tuple[str, Register]] = (
                (name, reg_map.regs[addr])
                for name, addr in reg_map.registers.items() if isinstance(reg_map.regs[addr], Register))
            masked_registers: Generator[Tuple[str, MaskedRegister]] = (
                (name, reg_map.regs[addr])
                for name, addr in reg_map.registers.items() if isinstance(reg_map.regs[addr], MaskedRegister))

            for name, reg in direct_registers:
                cmd_idx = reg_map.reg2cmd[reg.addr]
                self.assertIsInstance(cmd_idx, int)
                self.assertEqual(reg_map.commands[name], cmd_idx)

                if issubclass(reg.type, IntFlag):
                    for bitfield in reg.type:
                        value_set = reg.type(bitfield.value)
                        value_clr = reg.type(0)
                        tests.append([
                            T(i_reg=[IN(addr=reg.addr, val=value_set, mask=value_set)],
                              o_raw=[raw(cmd_idx=cmd_idx, cmd_val=value_set, send=True)],
                              o_cmp=IDEM),
                            T(i_reg=[IN(addr=reg.addr, val=value_clr, mask=value_set)],
                              o_raw=[raw(cmd_idx=cmd_idx, cmd_val=value_clr, send=True)],
                              o_cmp=IDEM),
                        ])
                    # end for
                elif reg.type is int:
                    value_set = randint(1, 0xFF)
                    value_clr = 0
                    tests.append([
                        T(i_reg=[IN(addr=reg.addr, val=value_set, mask=0xFF)],
                          o_raw=[raw(cmd_idx=cmd_idx, cmd_val=value_set, send=True)],
                          o_cmp=IDEM),
                        T(i_reg=[IN(addr=reg.addr, val=value_clr, mask=0xFF)],
                          o_raw=[raw(cmd_idx=cmd_idx, cmd_val=value_clr, send=True)],
                          o_cmp=IDEM),
                    ])
                else:
                    raise NotImplementedError(reg.type)
                # end if
            # end for

            for name, reg in masked_registers:
                cmd_idx = reg_map.reg2cmd[reg.addr]
                cmd_set = reg_map.commands[f'{name}_SET']
                cmd_clr = reg_map.commands[f'{name}_CLR']
                self.assertTupleEqual(cmd_idx, (cmd_set, cmd_clr))

                if issubclass(reg.type, IntFlag):
                    for bitfield in reg.type:
                        value_set = reg.type(bitfield.value)
                        value_clr = reg.type(0)
                        tests.append([
                            T(i_reg=[IN(addr=reg.addr, val=value_set, mask=value_set)],
                              o_raw=[raw(cmd_idx=cmd_set, cmd_val=value_set, send=True)],
                              o_cmp=IDEM),
                            T(i_reg=[IN(addr=reg.addr, val=value_clr, mask=value_set)],
                              o_raw=[raw(cmd_idx=cmd_set, cmd_val=value_clr),
                                     raw(cmd_idx=cmd_clr, cmd_val=value_set, send=True)],
                              o_cmp=IDEM),
                            T(i_reg=[IN(addr=reg.addr, val=None, mask=value_set)],
                              o_raw=[raw(cmd_idx=cmd_clr, cmd_val=value_clr, send=True)],
                              o_cmp=IDEM),
                        ])
                    # end for
                elif reg.type is int:
                    value_set = randint(0, 0xFF)
                    value_clr = 0
                    tests.append([
                        T(i_reg=[IN(addr=reg.addr, val=value_set, mask=0xFF)],
                          o_raw=[raw(cmd_idx=cmd_set, cmd_val=value_set, send=True)],
                          o_cmp=IDEM),
                        T(i_reg=[IN(addr=reg.addr, val=value_clr, mask=0xFF)],
                          o_raw=[raw(cmd_idx=cmd_set, cmd_val=value_clr),
                                 raw(cmd_idx=cmd_clr, cmd_val=value_set, send=True)],
                          o_cmp=IDEM),
                        T(i_reg=[IN(addr=reg.addr, val=None, mask=0xFF)],
                          o_raw=[raw(cmd_idx=cmd_clr, cmd_val=value_clr, send=True)],
                          o_cmp=IDEM),
                    ])
                else:
                    raise NotImplementedError(reg.type)
                # end if
            # end for

            self.run_control_tests(tests=list(chain.from_iterable(tests)), compression={False, True})
        # end def test_ll_ctrl

        @abstractmethod
        def test_ll_ctrl_power_modes(self):
            """
            Validate Low-Level Power Modes
            """
            raise NotImplementedAbstractMethodError()
        # end def test_ll_ctrl_power_modes

        @abstractmethod
        def test_hl_ctrl(self):
            """
            Validate High-level Control Actions
            """
            raise NotImplementedAbstractMethodError()
        # end def test_hl_ctrl

        @abstractmethod
        def test_hl_ctrl_delta_xy(self):
            """
            Validate Delta X and Y High-level actions.
            """
            raise NotImplementedAbstractMethodError()
        # end def test_hl_ctrl_delta_xy

        def test_hl_ctrl_power_modes(self):
            """
            Validate setting up Sensor Operating Modes: Force Rest2 mode or Force Sleep mode
            """
            # Shorthand notations
            hl = self.module.hl_ctrl

            # ========= TEST STEPS =========

            # Force Rest2 mode: expect mode change from Rest1 to Rest2
            hl.update(action=Action.DX, value=1)
            hl.update(action=Action.POWER_MODE_REST2, value=True)
            hl.commit()
            self.instruction_count += 2
            self.update_count += 1

            # Force Sleep mode: expect mode change from Rest2 to Sleep
            hl.update(action=Action.DX, value=2)
            hl.update(action=Action.POWER_MODE_SLEEP, value=True)
            hl.commit()
            self.instruction_count += 2
            self.update_count += 1

            # Reset mode: expect mode change from Sleep to Rest1
            hl.update(action=Action.DX, value=3)
            hl.update(action=Action.POWER_MODE_REST2, value=None)
            hl.update(action=Action.POWER_MODE_SLEEP, value=None)
            hl.commit()
            self.instruction_count += 2
            self.update_count += 1

            # Force Sleep mode: expect mode change from Rest1 to Sleep
            hl.update(action=Action.DX, value=4)
            hl.update(action=Action.POWER_MODE_SLEEP, value=True)
            hl.commit()
            self.instruction_count += 2
            self.update_count += 1

            # Force Rest2 mode: expect mode change from Sleep to Rest2
            hl.update(action=Action.DX, value=5)
            hl.update(action=Action.POWER_MODE_REST2, value=True)
            hl.commit()
            self.instruction_count += 2
            self.update_count += 1

            # Reset mode: expect mode change from Rest2 to Rest1
            hl.update(action=Action.DX, value=6)
            hl.update(action=Action.POWER_MODE_REST2, value=None)
            hl.update(action=Action.POWER_MODE_SLEEP, value=None)
            hl.commit()
            self.instruction_count += 2
            self.update_count += 1

            # Last raw dX displacement, to visualize the result of the last special instruction
            hl.update(action=Action.DX, value=7)
            hl.commit()
            self.instruction_count += 1
            self.update_count += 1

            # ========= DEBUG PRINT =========

            # Expect to see the following SPI frames (using an external Signal Analyzer)
            print(self.module.instructions_to_str())
            # print(self.module.instructions_to_spi_frames(self.module._buffer))                # FIXME: restore feature

            # ========= RUN TEST SEQUENCE ON HARDWARE =========

            self.run_test_sequence()
        # end def test_hl_ctrl_power_modes

        def run_control_tests(self, tests, compression, timeout=SEQUENCER_TIMEOUT_S):
            """
            Test Utility method: Run High- and Low-level test cases in batch.

            :param tests: List of test input directives & output expectations
            :type tests: ``Iterable[TestBase]``
            :param compression: Set of compression settings to test, ie ``{False, True}``
            :type compression: ``Set[bool]``
            :param timeout: Test sequence timeout, in seconds, defaults to ``SEQUENCER_TIMEOUT_S`` - OPTIONAL
            :type timeout: ``int or float``

            :raise ``AssertionError``: Test error
            :raise ``TypeError``: `tests` type error
            """
            # Shorthand notations
            hl = self.module.hl_ctrl
            ll = self.module.ll_ctrl
            r = self.module.ll_ctrl.reg_map.Registers
            c = self.module.ll_ctrl.reg_map.Commands
            raw = self.module.get_raw_instruction

            for compress in compression:
                # Set/Clear Raw to Compressed optimization flag
                self.module.ll_ctrl.compress = compress

                for test_idx, test in enumerate(tests):
                    # ========= DEBUG PRINT =========

                    print('\n====================================')
                    print(f'\n* Test[{test_idx}] inputs :')
                    print(f' - compress = {compress}')
                    print('\n'.join(f' - {k} = {v}' for k, v in asdict(test).items()))

                    # Shorthand notations
                    p_state, c_state = self.module.ll_ctrl.previous_state, self.module.ll_ctrl.current_state
                    o_instructions = test.o_raw if not compress else test.o_raw if test.o_cmp is IDEM else test.o_cmp

                    # ========= TEST STEPS (LOW-LEVEL) =========

                    if isinstance(test, LowLevelTest):
                        # STEP 1: Prepare current state
                        for reg in test.i_reg:
                            ll.update_reg(reg_addr=reg.addr, value=reg.val, mask=reg.mask)
                        # end for

                        # STEP 2: Commit current state
                        ll.finalize_state()
                        ll.commit_state()
                        ll.init_next_state()

                        # ========= TEST STEPS (HIGH-LEVEL) =========

                    elif isinstance(test, HighLevelTest):
                        # STEP 1: Prepare current state
                        for action in test.i_actions:
                            hl.update(action=action.action, value=action.value)
                        # end for

                        # STEP 2: Commit current state
                        hl.commit()

                    else:
                        raise TypeError(test)
                    # end if

                    # ========= DEBUG PRINT =========

                    # Note: After calling hl.commit_state(), p_state and c_state now points to previous states
                    self.print_state(p_state, c_state)

                    print('\n* Instructions (expected):')
                    print(self.module.instructions_to_str(o_instructions) or None)

                    # ========= VERIFICATION =========

                    # Test current instruction list
                    self.assertEqual(len(o_instructions), len(c_state.instructions), msg=f'test_idx={test_idx}')
                    for instr_idx, (expect, actual) in enumerate(zip(o_instructions, c_state.instructions)):
                        self.assertEqual(expect, actual, msg=f'test_idx={test_idx}, instr_idx: {instr_idx}')
                    # end for

                    # Update test expectations
                    self.update_count += 1
                    self.instruction_count += len(c_state.instructions)
                    self.assertEqual(self.module.length(), self.instruction_count, msg=f'test_idx={test_idx}')
                # end for

                # ========= RUN TEST SEQUENCE ON HARDWARE =========

                self.run_test_sequence(timeout=timeout)

                # ========= TEST CLEANUP =========
                self.module.reset_module()
                self.reset_test_expectations()
            # end for
        # end def run_control_tests

        def run_test_sequence(self, timeout=SEQUENCER_TIMEOUT_S):
            """
            Test Utility method: run an Optical Sensor Emulator test sequence that was already prepared.

            :param timeout: Test sequence timeout, in seconds, defaults to ``SEQUENCER_TIMEOUT_S`` - OPTIONAL
            :type timeout: ``int or float``

            :raise ``AssertionError``: Module status error
            """
            # PREPARE TEST SEQUENCE
            self.kosmos.sequencer.offline_mode = True
            # Turn DUT power slider ON
            self._slider_emulator.power_on()
            # Wait until Sensor Emulator finishes being configured by the DUT
            self.kosmos.pes.wait(action=self.module.resume_event.SETUP_DONE)
            # Start Sensor Emulator model update
            self.kosmos.pes.execute(action=self.module.action_event.START)
            # Wait until Sensor Emulator finishes its sequence
            self.kosmos.pes.wait(action=self.module.resume_event.FIFO_UNDERRUN)

            # RUN TEST SEQUENCE
            self.kosmos.sequencer.offline_mode = False
            self.kosmos.sequencer.play_sequence(timeout=timeout)

            # VERIFY module status
            status = self.module.status()
            self.assertEqual(1, status.setup_done, msg=status)
            self.assertEqual(0, status.fifo_en, msg=status)
            self.assertEqual(0, status.fifo_count, msg=status)
            self.assertEqual(1, status.fifo_underrun, msg=status)
            self.assertEqual(0, status.buffer_count, msg=status)
            self.assertEqual(0, status.buffer_overrun, msg=status)
            self.assertEqual(self.update_count, status.update_count, msg=status)

            # Turn DUT power slider OFF
            self._slider_emulator.power_off()
        # end def run_test_sequence

        def print_state(self, p_state, c_state):
            """
            Test Utility method: print previous and current Optical Sensor Emulator Low-level States.

            :param p_state: Previous state
            :type p_state: ``OpticalSensorEmulatorState``
            :param c_state: Current state
            :type c_state: ``OpticalSensorEmulatorState``
            """
            # Shorthand notations
            reg_map_regs = self.module.ll_ctrl.reg_map.regs
            reg_map_cmds = self.module.ll_ctrl.reg_map.cmds

            print('\n* Register Updates (current state):')
            reg_diff = self.module.ll_ctrl.reg_state_diff(p_state, c_state)
            print('\n'.join(f'{reg_map_regs[reg_addr].addr:#04x}:{reg_map_regs[reg_addr].name[:12]:<12} '
                            f'{p_reg_val} -> {c_reg_val}'
                            for reg_addr, (p_reg_val, c_reg_val) in reg_diff.items()) or None)

            print('\n* Command Values (current state):')
            print('\n'.join(f'{reg_map_cmds[cmd_idx].idx:#04x}:{reg_map_cmds[cmd_idx].name[:12]:<12} '
                            f'{repr(cmd_val) if isinstance(cmd_val, Enum) else hex(cmd_val)}'
                            for cmd_idx, cmd_val in c_state.cmds.items()) or None)

            print('\n* Instructions (current state):')
            print(self.module.instructions_to_str(c_state.instructions) or None)
        # end def print_state
    # end class OptEmuTestCaseMixin

    class OptEmu12BitsTestCaseMixin(OptEmuTestCaseMixin, metaclass=ABCMeta):
        """
        Kosmos Optical Sensor Emulator Module Test Class Mixin.
        """
        # Update type hints
        module: OptEmu12BitsModuleMixin

        def test_hl_ctrl_delta_xy(self):
            # See ``OptEmuTestCaseMixin.test_hl_ctrl_delta_xy``
            # Shorthand notations
            hl = self.module.hl_ctrl
            c = self.module.ll_ctrl.reg_map.Commands
            r = self.module.ll_ctrl.reg_map.Registers
            raw = self.module.get_raw_instruction
            cmp = self.module.get_compressed_instruction
            l = self.module.ll_ctrl.reg_map.Limits
            RAW_MIN = l.DELTA_SIGNED_MIN
            RAW_MAX = l.DELTA_SIGNED_MAX
            CMP_MIN = OPT_EMU_CMP_DX_MIN
            CMP_MAX = OPT_EMU_CMP_DX_MAX

            test_bugs = [(-4, 2), (-4, 2), (-1, 2)]
            test_values = all_permutations({0, -1, +1, RAW_MIN, RAW_MAX, 0x123, 0x456, -0x123, -0x456, 0xFF}, r=2)
            test_random = [(randint(RAW_MIN, RAW_MAX), randint(RAW_MIN, RAW_MAX)) for _ in range(1000)]
            test_stddev = [(int(gauss(mu=0, sigma=0xFF)), int(gauss(mu=0, sigma=0xFF))) for _ in range(1000)]
            test_small = [(randint(CMP_MIN, CMP_MAX), randint(CMP_MIN, CMP_MAX)) for _ in range(1000)]

            @dataclass
            class Delta:
                """
                Test Data structure
                """
                dx: int = 0
                dy: int = 0
                dh: int = 0

                def __str__(self):
                    return f'dx={self.dx:#05x}, dy={self.dy:#05x}, dh={self.dh:#05x}'
                # end def __str__
            # end class Delta

            for compress in [False, True]:
                # Set/Clear Raw to Compressed optimization flag
                self.module.ll_ctrl.compress = compress
                print(f'\n====== Instruction compression enabled: {compress} ======\n')

                previous_state = Delta()
                buf_idx = count()
                buffer = self.module._buffer

                for dx, dy in chain(test_bugs, test_values, test_random, test_stddev, test_small):
                    # Shorthand notations
                    c_state = self.module.ll_ctrl.current_state

                    # Test inputs sanity checks
                    assert l.DELTA_SIGNED_MIN <= dx <= l.DELTA_SIGNED_MAX, dx
                    assert l.DELTA_SIGNED_MIN <= dy <= l.DELTA_SIGNED_MAX, dy

                    # ========= DEBUG PRINT =========

                    print(f'dx= {dx:+5} = {dx:#06x}, dy= {dy:+5} = {dy:#06x}')

                    # ========= TEST STEPS =========

                    # STEP 1: Prepare current state
                    hl.update(action=Action.DX, value=dx)
                    hl.update(action=Action.DY, value=dy)

                    # STEP 2: Commit current state
                    hl.commit()

                    # ========= DEBUG PRINT =========

                    print(indent(self.module.instructions_to_str(c_state.instructions), prefix='  '))

                    # ========= VERIFICATION =========

                    # Convert inputs to unsigned integers
                    unsigned = Delta(dx=c_uint16(dx).value & 0xFF,
                                     dy=c_uint16(dy).value & 0xFF,
                                     dh=((c_uint16(dx).value >> 4) & 0xF0) | ((c_uint16(dy).value >> 8) & 0x0F))

                    # A register update is needed only if value changes from last update
                    needed = Delta(dx=unsigned.dx != previous_state.dx,
                                   dy=unsigned.dy != previous_state.dy,
                                   dh=unsigned.dh != previous_state.dh)

                    err_msg = f'dx={dx}={dx:#06x}, dy={dy}={dy:#06x}\n' \
                              f'unsigned: {str(unsigned)}\n' \
                              f'  buffer: {str(previous_state)}\n' \
                              f'  needed: {str(needed)}'

                    if self.module.test_instruction_is_nop(c_state.instructions[-1]):
                        # === Raw NOP instruction ===

                        # Verify instruction count
                        instr_count = 1
                        self.assertEqual(instr_count, len(c_state.instructions), msg=err_msg)

                        # Verify RAW NOP instruction
                        expect = self.module.get_nop_instruction(send=True)
                        self.assertEqual(expect, buffer[next(buf_idx)], msg=err_msg)

                    elif self.module.test_instruction_is_raw(c_state.instructions[-1]):
                        # === Raw instruction ===

                        # Verify instruction count
                        instr_count = sum(astuple(needed))
                        self.assertEqual(instr_count, len(c_state.instructions), msg=err_msg)

                        # Verify each RAW instruction within buffer
                        if needed.dx:
                            expect = raw(cmd_idx=c.DELTA_X_L, cmd_val=unsigned.dx & 0xFF,
                                         send=not (needed.dy or needed.dh))
                            self.assertEqual(expect, buffer[next(buf_idx)], msg=err_msg)
                            previous_state.dx = unsigned.dx
                        # end if
                        if needed.dy:
                            expect = raw(cmd_idx=c.DELTA_Y_L, cmd_val=unsigned.dy & 0xFF,
                                         send=not needed.dh)
                            self.assertEqual(expect, buffer[next(buf_idx)], msg=err_msg)
                            previous_state.dy = unsigned.dy
                        # end if
                        if needed.dh:
                            expect = raw(cmd_idx=c.DELTA_XY_H, cmd_val=unsigned.dh,
                                         send=True)
                            self.assertEqual(expect, buffer[next(buf_idx)], msg=err_msg)
                            previous_state.dh = unsigned.dh
                        # end if
                    else:
                        # === Compressed instruction ===

                        # Verify instruction count
                        instr_count = 1
                        self.assertEqual(instr_count, len(c_state.instructions), msg=err_msg)

                        # Verify CMP instruction within buffer
                        expect = cmp(dx=dx, dy=dy)
                        self.assertEqual(expect, buffer[next(buf_idx)], msg=err_msg)
                        previous_state = unsigned
                    # end if

                    # === Verify Register Values ===

                    self.assertEqual(previous_state.dx, c_state.regvs[r.DELTA_X_L].value_unsigned, msg=c_state.regvs)
                    self.assertEqual(previous_state.dy, c_state.regvs[r.DELTA_Y_L].value_unsigned, msg=c_state.regvs)
                    self.assertEqual(previous_state.dh, c_state.regvs[r.DELTA_XY_H].value_unsigned, msg=c_state.regvs)

                    # Update test expectations
                    self.instruction_count += instr_count
                    self.update_count += 1
                # end for

                # ========= RUN TEST SEQUENCE ON HARDWARE =========

                self.run_test_sequence()

                # ========= TEST CLEANUP =========

                self.module.reset_module()
                self.reset_test_expectations()
            # end for
        # end def test_hl_ctrl_delta_xy
    # end class OptEmu12BitsTestCaseMixin

    class OptEmu16BitsTestCaseMixin(OptEmuTestCaseMixin, metaclass=ABCMeta):
        """
        Kosmos Optical Sensor Emulator Module Test Class Mixin.
        """
        # Update type hints
        module: OptEmu16BitsModuleMixin

        def test_hl_ctrl_delta_xy(self):
            # See ``OptEmuTestCaseMixin.test_hl_ctrl_delta_xy``
            # Shorthand notations
            hl = self.module.hl_ctrl
            c = self.module.ll_ctrl.reg_map.Commands
            r = self.module.ll_ctrl.reg_map.Registers
            raw = self.module.get_raw_instruction
            cmp = self.module.get_compressed_instruction
            l = self.module.ll_ctrl.reg_map.Limits
            RAW_MIN = l.DELTA_SIGNED_MIN
            RAW_MAX = l.DELTA_SIGNED_MAX
            CMP_MIN = OPT_EMU_CMP_DX_MIN
            CMP_MAX = OPT_EMU_CMP_DX_MAX

            test_bugs = [(-4, 2), (-4, 2), (-1, 2)]
            test_values = all_permutations({0, -1, +1, RAW_MIN, RAW_MAX, 0x123, 0x456, -0x123, -0x456, 0xFF}, r=2)
            test_random = [(randint(RAW_MIN, RAW_MAX), randint(RAW_MIN, RAW_MAX)) for _ in range(1000)]
            test_stddev = [(int(gauss(mu=0, sigma=0xFF)), int(gauss(mu=0, sigma=0xFF))) for _ in range(1000)]
            test_small = [(randint(CMP_MIN, CMP_MAX), randint(CMP_MIN, CMP_MAX)) for _ in range(1000)]

            @dataclass
            class Delta:
                """
                Test Data structure
                """
                dx_h: int = 0
                dx_l: int = 0
                dy_h: int = 0
                dy_l: int = 0

                def __str__(self):
                    return f'dx={self.dx_h:#04x}{self.dx_l:02x}, dy={self.dy_h:#04x}{self.dy_l:02x}'
                # end def __str__
            # end class Delta

            for compress in [False, True]:
                # Set/Clear Raw to Compressed optimization flag
                self.module.ll_ctrl.compress = compress
                print(f'\n====== Instruction compression enabled: {compress} ======\n')

                previous_state = Delta()
                buf_idx = count()
                buffer = self.module._buffer

                for dx, dy in chain(test_bugs, test_values, test_random, test_stddev, test_small):
                    # Shorthand notations
                    c_state = self.module.ll_ctrl.current_state

                    # Test inputs sanity checks
                    assert l.DELTA_SIGNED_MIN <= dx <= l.DELTA_SIGNED_MAX, dx
                    assert l.DELTA_SIGNED_MIN <= dy <= l.DELTA_SIGNED_MAX, dy

                    # ========= DEBUG PRINT =========

                    print(f'dx= {dx:+5} = {dx:#06x}, dy= {dy:+5} = {dy:#06x}')

                    # ========= TEST STEPS =========

                    # STEP 1: Prepare current state
                    hl.update(action=Action.DX, value=dx)
                    hl.update(action=Action.DY, value=dy)

                    # STEP 2: Commit current state
                    hl.commit()

                    # ========= DEBUG PRINT =========

                    print(indent(self.module.instructions_to_str(c_state.instructions), prefix='  '))

                    # ========= VERIFICATION =========

                    # Convert inputs to unsigned integers
                    unsigned = Delta(dx_h=(c_uint16(dx).value >> 8) & 0xFF,
                                     dx_l=c_uint16(dx).value & 0xFF,
                                     dy_h=(c_uint16(dy).value >> 8) & 0xFF,
                                     dy_l=c_uint16(dy).value & 0xFF)

                    # A register update is needed only if value changes from last update
                    needed = Delta(dx_h=unsigned.dx_h != previous_state.dx_h,
                                   dx_l=unsigned.dx_l != previous_state.dx_l,
                                   dy_h=unsigned.dy_h != previous_state.dy_h,
                                   dy_l=unsigned.dy_l != previous_state.dy_l)

                    err_msg = f'dx={dx}={dx:#06x}, dy={dy}={dy:#06x}\n' \
                              f'unsigned: {str(unsigned)}\n' \
                              f'  buffer: {str(previous_state)}\n' \
                              f'  needed: {str(needed)}'

                    if self.module.test_instruction_is_nop(c_state.instructions[-1]):
                        # === Raw NOP instruction ===

                        # Verify instruction count
                        instr_count = 1
                        self.assertEqual(instr_count, len(c_state.instructions), msg=err_msg)

                        # Verify RAW NOP instruction
                        expect = self.module.get_nop_instruction(send=True)
                        self.assertEqual(expect, buffer[next(buf_idx)], msg=err_msg)

                    elif self.module.test_instruction_is_raw(c_state.instructions[-1]):
                        # === Raw instruction ===

                        # Verify instruction count
                        instr_count = sum(astuple(needed))
                        self.assertEqual(instr_count, len(c_state.instructions), msg=err_msg)

                        # Split verification in two sections, depending on DX/DY registers order
                        # 1) r.DELTA_X_H < r.DELTA_X_L and r.DELTA_Y_H < r.DELTA_Y_L
                        # 2) r.DELTA_X_H > r.DELTA_X_L and r.DELTA_Y_H > r.DELTA_Y_L
                        if r.DELTA_X_H < r.DELTA_X_L:
                            assert r.DELTA_Y_H < r.DELTA_Y_L
                            # Verify each RAW instruction within buffer
                            if needed.dx_h:
                                expect = raw(cmd_idx=c.DELTA_X_H, cmd_val=unsigned.dx_h,
                                             send=not (needed.dx_l or needed.dy_h or needed.dy_l))
                                self.assertEqual(expect, buffer[next(buf_idx)], msg=err_msg)
                                previous_state.dx_h = unsigned.dx_h
                            # end if
                            if needed.dx_l:
                                expect = raw(cmd_idx=c.DELTA_X_L, cmd_val=unsigned.dx_l,
                                             send=not (needed.dy_h or needed.dy_l))
                                self.assertEqual(expect, buffer[next(buf_idx)], msg=err_msg)
                                previous_state.dx_l = unsigned.dx_l
                            # end if
                            if needed.dy_h:
                                expect = raw(cmd_idx=c.DELTA_Y_H, cmd_val=unsigned.dy_h,
                                             send=not needed.dy_l)
                                self.assertEqual(expect, buffer[next(buf_idx)], msg=err_msg)
                                previous_state.dy_h = unsigned.dy_h
                            # end if
                            if needed.dy_l:
                                expect = raw(cmd_idx=c.DELTA_Y_L, cmd_val=unsigned.dy_l,
                                             send=True)
                                self.assertEqual(expect, buffer[next(buf_idx)], msg=err_msg)
                                previous_state.dy_l = unsigned.dy_l
                            # end if
                        else:
                            assert r.DELTA_X_H > r.DELTA_X_L and r.DELTA_Y_H > r.DELTA_Y_L
                            # Verify each RAW instruction within buffer
                            if needed.dx_l:
                                expect = raw(cmd_idx=c.DELTA_X_L, cmd_val=unsigned.dx_l,
                                             send=not (needed.dx_h or needed.dy_l or needed.dy_h))
                                self.assertEqual(expect, buffer[next(buf_idx)], msg=err_msg)
                                previous_state.dx_l = unsigned.dx_l
                            # end if
                            if needed.dx_h:
                                expect = raw(cmd_idx=c.DELTA_X_H, cmd_val=unsigned.dx_h,
                                             send=not (needed.dy_l or needed.dy_h))
                                self.assertEqual(expect, buffer[next(buf_idx)], msg=err_msg)
                                previous_state.dx_h = unsigned.dx_h
                            # end if
                            if needed.dy_l:
                                expect = raw(cmd_idx=c.DELTA_Y_L, cmd_val=unsigned.dy_l,
                                             send=not needed.dy_h)
                                self.assertEqual(expect, buffer[next(buf_idx)], msg=err_msg)
                                previous_state.dy_l = unsigned.dy_l
                            # end if
                            if needed.dy_h:
                                expect = raw(cmd_idx=c.DELTA_Y_H, cmd_val=unsigned.dy_h,
                                             send=True)
                                self.assertEqual(expect, buffer[next(buf_idx)], msg=err_msg)
                                previous_state.dy_h = unsigned.dy_h
                            # end if
                        # end if
                    else:
                        # === Compressed instruction ===

                        # Verify instruction count
                        instr_count = 1
                        self.assertEqual(instr_count, len(c_state.instructions), msg=err_msg)

                        # Verify CMP instruction within buffer
                        expect = cmp(dx=dx, dy=dy)
                        self.assertEqual(expect, buffer[next(buf_idx)], msg=err_msg)
                        previous_state = unsigned
                    # end if

                    # === Verify Register Values ===

                    self.assertEqual(previous_state.dx_h, c_state.regvs[r.DELTA_X_H].value_unsigned, msg=c_state.regvs)
                    self.assertEqual(previous_state.dx_l, c_state.regvs[r.DELTA_X_L].value_unsigned, msg=c_state.regvs)
                    self.assertEqual(previous_state.dy_h, c_state.regvs[r.DELTA_Y_H].value_unsigned, msg=c_state.regvs)
                    self.assertEqual(previous_state.dy_l, c_state.regvs[r.DELTA_Y_L].value_unsigned, msg=c_state.regvs)

                    # Update test expectations
                    self.instruction_count += instr_count
                    self.update_count += 1
                # end for

                # ========= RUN TEST SEQUENCE ON HARDWARE =========

                self.run_test_sequence()

                # ========= TEST CLEANUP =========

                self.module.reset_module()
                self.reset_test_expectations()
            # end for
        # end def test_hl_ctrl_delta_xy
    # end class OptEmu16BitsTestCaseMixin
# end class OptEmuAbstractTestClass


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
