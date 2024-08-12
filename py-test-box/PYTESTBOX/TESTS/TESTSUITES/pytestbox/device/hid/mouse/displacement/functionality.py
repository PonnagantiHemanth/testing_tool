#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.mouse.displacement.functionality
:brief: Hid mouse XY displacement functionality test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2023/03/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import randint

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid import HID_REPORTS
from pyhid.hiddata import HidData
from pyhid.hiddispatcher import HIDDispatcher
from pylibrary.emulator.keyid import KEY_ID
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.hid.base.hidreportutils import HidReportTestUtils
from pytestbox.device.hid.mouse import EXCLUDED_BUTTONS
from pytestbox.device.hid.mouse.displacement.xydisplacement import XYDisplacementTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
# 4 bits format: 0x09 (-7) ... 0x0F (-1), 0x00, 0x01 ... 0x07 (+7)
MAX_4BITS_LONG_POSITIVE_MOTION = 0x07
MIN_5BITS_LONG_POSITIVE_MOTION = 0x08
# 8 bits format: 0x81 (-127) ... 0xF8 (-8), 0x08 (8) ... 0x7F (+127)
MAX_8BITS_LONG_POSITIVE_MOTION = 0x7F
MIN_9BITS_LONG_POSITIVE_MOTION = 0x80
# 12 bits format: 0x801 (-2047) ... 0xF80 (-128), 0x80 (128) ... 0x7F (+2047)
MAX_12BITS_LONG_POSITIVE_MOTION = 0x7FF
MIN_13BITS_LONG_POSITIVE_MOTION = 0x800

# Number of transition to be tested.
# Be aware that a higher number will generate HID report with accumulation as our USB layer could not cope with the 4kHz
PDU_FORMAT_TEST_LOOP = 2

# Displacement
SHORT_MOTION = 16
LONG_MOTION = 64

# Delay
DELAY_1_MS = 1000000


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class XYDisplacementFunctionalityTestCase(XYDisplacementTestCase):
    """
    Validate Mouse XY displacement functionality TestCases
    """

    @features('Mice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_move_right(self):
        """
        Verify that X displacement field could go up to its maximum when the mouse moves to the right (i.e. X axis)
        """
        bit_count = self.motion_emulator.limits.DELTA_BIT_COUNT
        motions = [1 << x for x in range(bit_count-1)]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Test Loop for right motion with {bit_count}-bit resolution: {motions}')
        # --------------------------------------------------------------------------------------------------------------
        for motion in motions:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Move right x={motion} position")
            # ----------------------------------------------------------------------------------------------------------
            self.motion_emulator.xy_motion(dx=motion)
            self.motion_emulator.commit_actions()
            self.motion_emulator.prepare_sequence()

            expected_motion = self.clip(motion)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check the HID Mouse report with X displacement field set to {expected_motion}")
            # ----------------------------------------------------------------------------------------------------------
            HidReportTestUtils.check_motion_accumulation(
                test_case=self, events=[HidReportTestUtils.Event(event_type=HidReportTestUtils.EventId.X_MOTION,
                                                                 value=expected_motion)])
        # end for

        self.testCaseChecked("FUN_HID_MOTION_0001")
    # end def test_move_right

    @features('Mice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_move_left(self):
        """
        Verify that X displacement field could go down to its minimum when the mouse moves to the left (i.e. X axis)
        """
        bit_count = self.motion_emulator.limits.DELTA_BIT_COUNT
        motions = [-(1 << y) for y in range(bit_count-1)]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Test Loop for left motion with {bit_count}-bit resolution: {motions}')
        # --------------------------------------------------------------------------------------------------------------
        for motion in motions:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Move left x={motion} position")
            # ----------------------------------------------------------------------------------------------------------
            self.motion_emulator.xy_motion(dx=motion)
            self.motion_emulator.commit_actions()
            self.motion_emulator.prepare_sequence()

            expected_motion = self.clip(motion)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check the HID Mouse report with X displacement field set to {expected_motion}")
            # ----------------------------------------------------------------------------------------------------------
            HidReportTestUtils.check_motion_accumulation(
                test_case=self, events=[HidReportTestUtils.Event(event_type=HidReportTestUtils.EventId.X_MOTION,
                                                                 value=expected_motion)])
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_HID_MOTION_0002")
    # end def test_move_left

    @features('Mice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_move_up(self):
        """
        Verify that Y displacement field could go up to its maximum when the mouse moves up (i.e. Y axis)
        """
        bit_count = self.motion_emulator.limits.DELTA_BIT_COUNT
        motions = [1 << x for x in range(bit_count-1)]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Test Loop for up motion with {bit_count}-bit resolution: {motions}')
        # --------------------------------------------------------------------------------------------------------------
        for motion in motions:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Move up y={motion} position")
            # ----------------------------------------------------------------------------------------------------------
            self.motion_emulator.xy_motion(dy=motion)
            self.motion_emulator.commit_actions()
            self.motion_emulator.prepare_sequence()

            expected_motion = self.clip(motion)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check the HID Mouse report with Y displacement field set to {expected_motion}")
            # ----------------------------------------------------------------------------------------------------------
            HidReportTestUtils.check_motion_accumulation(
                test_case=self, events=[HidReportTestUtils.Event(event_type=HidReportTestUtils.EventId.Y_MOTION,
                                                                 value=expected_motion)])
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_HID_MOTION_0003")
    # end def test_move_up

    @features('Mice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_move_down(self):
        """
        Verify that Y displacement field could go down to its minimum when the mouse moves down (i.e. Y axis)
        """
        bit_count = self.motion_emulator.limits.DELTA_BIT_COUNT
        motions = [-(1 << y) for y in range(bit_count-1)]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Test Loop for down motion with {bit_count}-bit resolution: {motions}')
        # --------------------------------------------------------------------------------------------------------------
        for motion in motions:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Move down y={motion} position")
            # ----------------------------------------------------------------------------------------------------------
            self.motion_emulator.xy_motion(dy=motion)
            self.motion_emulator.commit_actions()
            self.motion_emulator.prepare_sequence()

            expected_motion = self.clip(motion)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check the HID Mouse report with Y displacement field set to {expected_motion}")
            # ----------------------------------------------------------------------------------------------------------
            HidReportTestUtils.check_motion_accumulation(
                test_case=self, events=[HidReportTestUtils.Event(event_type=HidReportTestUtils.EventId.Y_MOTION,
                                                                 value=expected_motion)])
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_HID_MOTION_0004")
    # end def test_move_down

    @features('Mice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_motion_button(self):
        """
        Verify button & XY displacement events could be packed in the same HID report
        """
        # Test inputs
        x_motion = randint(1, MIN_5BITS_LONG_POSITIVE_MOTION)
        y_motion = randint(1, MIN_5BITS_LONG_POSITIVE_MOTION)
        motion_count = randint(SHORT_MOTION, LONG_MOTION)
        LogHelper.log_info(self, f'Test inputs: {x_motion}, {y_motion}, loop={motion_count}, '
                                 f'expected_x={x_motion*motion_count}, expected_y={y_motion*motion_count}')

        for key_id in [x for x in self.button_stimuli_emulator.get_key_id_list()
                       if x not in EXCLUDED_BUTTONS and x < KEY_ID.BUTTON_1]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Click on the {str(key_id)!s} and move at the same time")
            # ----------------------------------------------------------------------------------------------------------

            # Prepare Optical Sensor Emulator motion sequence
            self.motion_emulator.xy_motion(dx=x_motion, dy=y_motion, repetition=motion_count - 1)
            self.motion_emulator.commit_actions()

            # Prepare test sequence
            self.kosmos.sequencer.offline_mode = True
            self.button_stimuli_emulator.key_press(key_id=key_id)
            self.kosmos.pes.execute(action=self.motion_emulator.module.action_event.START)
            self.kosmos.pes.wait(action=self.motion_emulator.module.resume_event.FIFO_UNDERRUN)
            self.kosmos.pes.delay(delay_ns=DELAY_1_MS)
            self.button_stimuli_emulator.key_release(key_id=key_id)

            # Run test sequence
            self.kosmos.sequencer.offline_mode = False
            self.kosmos.sequencer.play_sequence()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check the HID Mouse report with "
                                      f"{str(key_id)!s} and X displacement fields set")
            # ----------------------------------------------------------------------------------------------------------
            HidReportTestUtils.check_motion_accumulation(test_case=self, events=[
                HidReportTestUtils.Event(event_type=HidReportTestUtils.EventId.X_MOTION, value=x_motion * motion_count),
                HidReportTestUtils.Event(event_type=HidReportTestUtils.EventId.Y_MOTION, value=y_motion * motion_count),
                HidReportTestUtils.Event(event_type=HidReportTestUtils.KEY_ID_EVENT_MAP[key_id], value=1)])

            # Empty hid_message_queue
            ChannelUtils.clean_messages(
                test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                class_type=HID_REPORTS)
        # end for

        self.testCaseChecked("FUN_HID_MOTION_0010")
    # end def test_motion_button

    @features('Mice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_motion_multiple_buttons(self):
        """
        Verify multiple keystrokes & XY displacement events could be packed in the same HID report
        """
        # Test inputs
        x_motion = randint(1, MIN_5BITS_LONG_POSITIVE_MOTION)
        y_motion = randint(1, MIN_5BITS_LONG_POSITIVE_MOTION)
        motion_count = randint(SHORT_MOTION, LONG_MOTION)
        LogHelper.log_info(self, f'Test inputs: {x_motion}, {y_motion}, loop={motion_count}, '
                                 f'expected_x={x_motion*motion_count}, expected_y={y_motion*motion_count}')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press on all supported buttons, retrieve  HID make report, then move the mouse "
                                 "and finally release all buttons")
        # --------------------------------------------------------------------------------------------------------------
        self.pressed_key_ids = []
        self.pressed_key_ids.extend([x for x in self.button_stimuli_emulator.get_key_id_list() if x not in
                                     EXCLUDED_BUTTONS and x < KEY_ID.BUTTON_1])
        self.button_stimuli_emulator.multiple_keys_press(key_ids=self.pressed_key_ids)
        for _ in range(max(1, len(self.button_stimuli_emulator.get_hybrid_key_id_list()))):
            # Retreive HID make report : multiple reports can happen on mice with multiple hybrid switch
            make_packet = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                                allow_no_message=True)
            if make_packet is None:
                break
            # end if
        # end for

        # Prepare Optical Sensor Emulator motion sequence
        self.motion_emulator.xy_motion(dx=x_motion, dy=y_motion, repetition=motion_count - 1)
        self.motion_emulator.commit_actions()

        # Prepare test sequence
        self.kosmos.sequencer.offline_mode = True
        self.kosmos.pes.execute(action=self.motion_emulator.module.action_event.START)
        self.kosmos.pes.wait(action=self.motion_emulator.module.resume_event.FIFO_UNDERRUN)
        self.kosmos.pes.delay(delay_ns=DELAY_1_MS)
        self.button_stimuli_emulator.multiple_keys_release(key_ids=self.pressed_key_ids)

        # Run test sequence
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the HID Mouse report with all supported buttons pressed plus X and Y "
                                  "displacement fields set")
        # --------------------------------------------------------------------------------------------------------------
        events = [
            HidReportTestUtils.Event(event_type=HidReportTestUtils.EventId.X_MOTION, value=x_motion * motion_count),
            HidReportTestUtils.Event(event_type=HidReportTestUtils.EventId.Y_MOTION, value=y_motion * motion_count)]
        for key_id in self.pressed_key_ids:
            events.append(HidReportTestUtils.Event(event_type=HidReportTestUtils.KEY_ID_EVENT_MAP[key_id], value=1))
        # end for
        HidReportTestUtils.check_motion_accumulation(test_case=self, events=events)

        self.testCaseChecked("FUN_HID_MOTION_0011")
    # end def test_motion_multiple_buttons

    @features('Mice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_pdu_format_4_5_bits(self):
        """
        Verify that X/Y displacement fields are always coherent with the value put in the sensor registers
        during transition between the 4 and 5 bits long PDU format
         - Test all 4 <-> 5 bits transitions on X and Y fields
         - Test all 4 <-> 5 bits transitions when the left button is pressed
        """
        for loop_index in range(2):
            if loop_index > 0:
                self.pressed_key_ids = KEY_ID.LEFT_BUTTON
                self.button_stimuli_emulator.key_press(key_id=KEY_ID.LEFT_BUTTON)
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Test 4 <-> 5 bits transitions with a positive value in X field")
            # ----------------------------------------------------------------------------------------------------------
            self._test_pdu_format_transitions(
                first_x_motion=MAX_4BITS_LONG_POSITIVE_MOTION, second_x_motion=MIN_5BITS_LONG_POSITIVE_MOTION)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Test 4 <-> 5 bits transitions with a positive value in Y field")
            # ----------------------------------------------------------------------------------------------------------
            self._test_pdu_format_transitions(
                first_y_motion=MAX_4BITS_LONG_POSITIVE_MOTION, second_y_motion=MIN_5BITS_LONG_POSITIVE_MOTION)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Test 4 <-> 5 bits transitions with a negative value in X field")
            # ----------------------------------------------------------------------------------------------------------
            self._test_pdu_format_transitions(
                first_x_motion=-MAX_4BITS_LONG_POSITIVE_MOTION, second_x_motion=-MIN_5BITS_LONG_POSITIVE_MOTION)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Test 4 <-> 5 bits transitions with a negative value in Y field")
            # ----------------------------------------------------------------------------------------------------------
            self._test_pdu_format_transitions(
                first_y_motion=-MAX_4BITS_LONG_POSITIVE_MOTION, second_y_motion=-MIN_5BITS_LONG_POSITIVE_MOTION)

            if loop_index > 0:
                self.button_stimuli_emulator.key_release(key_id=KEY_ID.LEFT_BUTTON)
                self.pressed_key_ids = None
            # end if
        # end for

        self.testCaseChecked("FUN_HID_MOTION_0012")
    # end def test_pdu_format_4_5_bits

    @features('Mice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_pdu_format_8_9_bits(self):
        """
        Verify that X/Y displacement fields are always coherent with the value put in the sensor registers
        during transition between the 8 and 9 bits long PDU format
         - Test all 8 <-> 9 bits transitions on X and Y fields
         - Test all 8 <-> 9 bits transitions when the left button is pressed
        """
        for loop_index in range(2):
            if loop_index > 0:
                self.pressed_key_ids = KEY_ID.LEFT_BUTTON
                self.button_stimuli_emulator.key_press(key_id=KEY_ID.LEFT_BUTTON)
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Test 8 <-> 9 bits transitions with a positive value in X field")
            # ----------------------------------------------------------------------------------------------------------
            self._test_pdu_format_transitions(
                first_x_motion=MAX_8BITS_LONG_POSITIVE_MOTION, second_x_motion=MIN_9BITS_LONG_POSITIVE_MOTION)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Test 8 <-> 9 bits transitions with a positive value in Y field")
            # ----------------------------------------------------------------------------------------------------------
            self._test_pdu_format_transitions(
                first_y_motion=MAX_8BITS_LONG_POSITIVE_MOTION, second_y_motion=MIN_9BITS_LONG_POSITIVE_MOTION)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Test 8 <-> 9 bits transitions with a negative value in X field")
            # ----------------------------------------------------------------------------------------------------------
            self._test_pdu_format_transitions(
                first_x_motion=-MAX_8BITS_LONG_POSITIVE_MOTION, second_x_motion=-MIN_9BITS_LONG_POSITIVE_MOTION)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Test 8 <-> 9 bits transitions with a negative value in Y field")
            # ----------------------------------------------------------------------------------------------------------
            self._test_pdu_format_transitions(
                first_y_motion=-MAX_8BITS_LONG_POSITIVE_MOTION, second_y_motion=-MIN_9BITS_LONG_POSITIVE_MOTION)

            if loop_index > 0:
                self.button_stimuli_emulator.key_release(key_id=KEY_ID.LEFT_BUTTON)
                self.pressed_key_ids = None
            # end if
        # end for
        self.testCaseChecked("FUN_HID_MOTION_0013")
    # end def test_pdu_format_8_9_bits

    @features('Mice')
    @features('GamingDevice')
    @level('Functionality')
    @services('OpticalSensor16bits')
    def test_pdu_format_12_13_bits(self):
        """
        Verify that X/Y displacement fields are always coherent with the value put in the sensor registers
        during transition between the 12 and 13 bits long PDU format
         - Test all 12 <-> 13 bits transitions on X and Y fields
         - Test all 12 <-> 13 bits transitions when the left button is pressed
        """
        for loop_index in range(2):
            if loop_index > 0:
                self.pressed_key_ids = KEY_ID.LEFT_BUTTON
                self.button_stimuli_emulator.key_press(key_id=KEY_ID.LEFT_BUTTON)
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Test 12 <-> 13 bits transitions with a positive value in X field")
            # ----------------------------------------------------------------------------------------------------------
            self._test_pdu_format_transitions(
                first_x_motion=MAX_12BITS_LONG_POSITIVE_MOTION, second_x_motion=MIN_13BITS_LONG_POSITIVE_MOTION)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Test 12 <-> 13 bits transitions with a positive value in Y field")
            # ----------------------------------------------------------------------------------------------------------
            self._test_pdu_format_transitions(
                first_y_motion=MAX_12BITS_LONG_POSITIVE_MOTION, second_y_motion=MIN_13BITS_LONG_POSITIVE_MOTION)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Test 12 <-> 13 bits transitions with a negative value in X field")
            # ----------------------------------------------------------------------------------------------------------
            self._test_pdu_format_transitions(
                first_x_motion=-MAX_12BITS_LONG_POSITIVE_MOTION, second_x_motion=-MIN_13BITS_LONG_POSITIVE_MOTION)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Test 12 <-> 13 bits transitions with a negative value in Y field")
            # ----------------------------------------------------------------------------------------------------------
            self._test_pdu_format_transitions(
                first_y_motion=-MAX_12BITS_LONG_POSITIVE_MOTION, second_y_motion=-MIN_13BITS_LONG_POSITIVE_MOTION)

            if loop_index > 0:
                self.button_stimuli_emulator.key_release(key_id=KEY_ID.LEFT_BUTTON)
                self.pressed_key_ids = None
            # end if
        # end for
        self.testCaseChecked("FUN_HID_MOTION_0014")
    # end def test_pdu_format_12_13_bits

    def _test_pdu_format_transitions(self, first_x_motion=0, second_x_motion=0, first_y_motion=0, second_y_motion=0):
        """
        Verify that X/Y displacement fields are always coherent with the value put in the sensor registers
        during transition between multiple PDU format
         - Test all transitions on X and Y fields

        :param first_x_motion: X displacement value to inject in steps 1 and 3 - OPTIONAL
        :type first_x_motion: ``int``
        :param second_x_motion: X displacement value to inject in step 2 - OPTIONAL
        :type second_x_motion: ``int``
        :param first_y_motion: Y displacement value to inject in steps 1 and 3 - OPTIONAL
        :type first_y_motion: ``int``
        :param second_y_motion: Y displacement value to inject in step 2 - OPTIONAL
        :type second_y_motion: ``int``
        """
        for _ in range(PDU_FORMAT_TEST_LOOP):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Inject the maximum motion value matching the short PDU format: "
                                     f"X displacement = {first_x_motion} and Y displacement = {first_y_motion}")
            # ----------------------------------------------------------------------------------------------------------
            self.motion_emulator.xy_motion(dx=first_x_motion, dy=first_y_motion, skip=2)
            self.motion_emulator.commit_actions()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Inject the minimum motion value matching the long PDU format: "
                                     f"X displacement = {second_x_motion} and Y displacement = {second_y_motion}")
            # ----------------------------------------------------------------------------------------------------------
            self.motion_emulator.xy_motion(dx=second_x_motion, dy=second_y_motion, skip=2)
            self.motion_emulator.commit_actions()
        # end for
        self.motion_emulator.prepare_sequence()

        expected_first_x_motion = self.clip(first_x_motion)
        expected_first_y_motion = self.clip(first_y_motion)
        expected_second_x_motion = self.clip(second_x_motion)
        expected_second_y_motion = self.clip(second_y_motion)

        for _ in range(PDU_FORMAT_TEST_LOOP):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check the HID Mouse report with X displacement = {expected_first_x_motion} and "
                                      f"Y displacement = {expected_first_y_motion}")
            # ----------------------------------------------------------------------------------------------------------
            HidReportTestUtils.check_motion_accumulation(
                test_case=self, events=[HidReportTestUtils.Event(event_type=HidReportTestUtils.EventId.X_MOTION,
                                                                 value=expected_first_x_motion),
                                        HidReportTestUtils.Event(event_type=HidReportTestUtils.EventId.Y_MOTION,
                                                                 value=expected_first_y_motion)])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check the HID Mouse report with X displacement = {expected_second_x_motion} and "
                                      f"Y displacement = {expected_second_y_motion}")
            # ----------------------------------------------------------------------------------------------------------
            HidReportTestUtils.check_motion_accumulation(
                test_case=self, events=[HidReportTestUtils.Event(event_type=HidReportTestUtils.EventId.X_MOTION,
                                                                 value=expected_second_x_motion),
                                        HidReportTestUtils.Event(event_type=HidReportTestUtils.EventId.Y_MOTION,
                                                                 value=expected_second_y_motion)])
        # end for

    # end def _test_pdu_format_transitions
# end class XYDisplacementFunctionalityTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
