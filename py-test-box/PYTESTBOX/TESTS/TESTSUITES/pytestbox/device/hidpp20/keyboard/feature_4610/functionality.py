#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.keyboard.feature_4610.functionality
:brief: HID++ 2.0 ``MultiRoller`` functionality test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2023/10/03
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import choice
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid import HidConsumer
from pyhid.hid import HidMouse
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.keyboard.multiroller import RollerMode
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.multirollerutils import MultiRollerTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4610.multiroller import MultiRollerTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MultiRollerFunctionalityTestCase(MultiRollerTestCase):
    """
    Validate ``MultiRoller`` functionality test cases
    """

    @features("Feature4610")
    @level("Functionality")
    @services('MainWheel')
    def test_roller_in_oob_and_divert_mode(self):
        """
        Validate the reports of scrolling rollers in OOB, and the RotationEvent will be sent when a roller is scrolling
        if the roller mode is set divert.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over roller_index in range({self.config.F_NumRollers}):")
        # --------------------------------------------------------------------------------------------------------------
        for roller_index in range(self.config.F_NumRollers):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Scroll the roller: {roller_index}")
            # ----------------------------------------------------------------------------------------------------------
            # TODO - Implement roller emulator

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the corresponding report is received")
            # ----------------------------------------------------------------------------------------------------------
            report = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                           class_type=(HidMouse, HidConsumer), allow_no_message=True)
            self.assertNotNone(obtained=report,
                               msg=f'There is no corresponding report are received after scrolling: {roller_index}')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Send SetMode request with roller_id={roller_index}, mode={RollerMode.DIVERT!s}")
            # ----------------------------------------------------------------------------------------------------------
            MultiRollerTestUtils.HIDppHelper.set_mode(test_case=self, roller_id=roller_index,
                                                      divert=RollerMode.DIVERT)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Perform user action to scroll the rollers[{roller_index}]")
            # ----------------------------------------------------------------------------------------------------------
            # TODO - Implement roller emulator

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait RotationEvent is received and all data are as expected")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiRollerTestUtils.HIDppHelper.rotation_event(test_case=self)
            checker = MultiRollerTestUtils.RotationEventChecker
            check_map = checker.get_check_map(roller_id=roller_index)
            checker.check_fields(self, response, self.feature_4610.rotation_event_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Send SetMode request with roller_id={roller_index}, "
                      f"mode={RollerMode.DEFAULT_MODE!s}")
            # ----------------------------------------------------------------------------------------------------------
            MultiRollerTestUtils.HIDppHelper.set_mode(test_case=self, roller_id=roller_index,
                                                      divert=RollerMode.DEFAULT_MODE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Scroll the roller: {roller_index}")
            # ----------------------------------------------------------------------------------------------------------
            # TODO - Implement roller emulator

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the corresponding report is received")
            # ----------------------------------------------------------------------------------------------------------
            report = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                           class_type=(HidMouse, HidConsumer), allow_no_message=True)
            self.assertNotNone(obtained=report,
                               msg=f'There is no corresponding report are received after scrolling: {roller_index}')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_4610_0001", _AUTHOR)
    # end def test_roller_in_oob_and_divert_mode

    @features("Feature4610")
    @level("Functionality")
    @services('MainWheel')
    def test_set_roller_in_divert_individually(self):
        """
        Validate the divert mode can be set individually on each rollers
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over roller_index in range({self.config.F_NumRollers}):")
        # --------------------------------------------------------------------------------------------------------------
        for roller_index in range(self.config.F_NumRollers):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Send SetMode request with roller_id={roller_index}, mode={RollerMode.DIVERT!s}")
            # ----------------------------------------------------------------------------------------------------------
            MultiRollerTestUtils.HIDppHelper.set_mode(test_case=self, roller_id=roller_index,
                                                      divert=RollerMode.DIVERT)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Test Loop over roller in range({self.config.F_NumRollers}):")
            # ----------------------------------------------------------------------------------------------------------
            for inner_roller_index in range(self.config.F_NumRollers):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Perform user action to scroll the roller[{inner_roller_index}]")
                # ------------------------------------------------------------------------------------------------------
                # TODO - Implement roller emulator

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Wait HID/RotationEvent report is received and all data are as expected")
                # ------------------------------------------------------------------------------------------------------
                if roller_index >= inner_roller_index:
                    response = MultiRollerTestUtils.HIDppHelper.rotation_event(test_case=self)
                    checker = MultiRollerTestUtils.RotationEventChecker
                    check_map = checker.get_check_map(roller_id=roller_index)
                    checker.check_fields(self, response, self.feature_4610.rotation_event_cls, check_map)
                else:
                    response = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                                     class_type=HidMouse, allow_no_message=True)
                    self.assertNotNone(
                        obtained=response,
                        msg=f'No HID report is received when the roller[{roller_index}] is not in divert')
                # end if
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_4610_0002", _AUTHOR)
    # end def test_set_roller_in_divert_individually

    @features("Feature4610")
    @level("Functionality")
    @services('MainWheel')
    def test_rollers_count_per_rotation(self):
        """
        Validate the count per rotation is matching the roller's capability
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over roller_index in range({self.config.F_NumRollers}):")
        # --------------------------------------------------------------------------------------------------------------
        for roller_index in range(self.config.F_NumRollers):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Send SetMode request with roller_id={roller_index}, mode={RollerMode.DIVERT!s}")
            # ----------------------------------------------------------------------------------------------------------
            MultiRollerTestUtils.HIDppHelper.set_mode(test_case=self, roller_id=roller_index,
                                                      divert=RollerMode.DIVERT)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over in range(10):")
            # ----------------------------------------------------------------------------------------------------------
            for _ in range(10):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Scroll the rollers[{roller_index}] with one complete rotation (360 degrees)")
                # ------------------------------------------------------------------------------------------------------
                # TODO - Implement roller emulator

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check the RotationEvent.delta is {self.config.F_IncrementsPerRotation[roller_index]}")
                # ------------------------------------------------------------------------------------------------------
                rotation_event = MultiRollerTestUtils.HIDppHelper.rotation_event(test_case=self)
                self.assertEqual(obtained=rotation_event.delta,
                                 expected=self.config.F_IncrementsPerRotation[roller_index],
                                 msg='The delta does not match the increments per rotation')
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_4610_0003", _AUTHOR)
    # end def test_rollers_count_per_rotation

    @features("Feature4610")
    @level("Functionality")
    @services('MainWheel')
    def test_rollers_count_per_ratchet(self):
        """
        Validate the count per ratchet is matching the roller's capability
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over roller_index in range({self.config.F_NumRollers}):")
        # --------------------------------------------------------------------------------------------------------------
        for roller_index in range(self.config.F_NumRollers):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Send SetMode request with roller_id={roller_index}, mode={RollerMode.DIVERT!s}")
            # ----------------------------------------------------------------------------------------------------------
            MultiRollerTestUtils.HIDppHelper.set_mode(test_case=self, roller_id=roller_index,
                                                      divert=RollerMode.DIVERT)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over in range(10):")
            # ----------------------------------------------------------------------------------------------------------
            for _ in range(10):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Scroll the rollers[{roller_index}] with one ratchet")
                # ------------------------------------------------------------------------------------------------------
                # TODO - Implement roller emulator

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check the RotationEvent.delta is {self.config.F_IncrementsPerRatchet[roller_index]}")
                # ------------------------------------------------------------------------------------------------------
                rotation_event = MultiRollerTestUtils.HIDppHelper.rotation_event(test_case=self)
                self.assertEqual(obtained=rotation_event.delta,
                                 expected=self.config.F_IncrementsPerRatchet[roller_index],
                                 msg='The delta does not match the increments per ratchet')
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_4610_0004", _AUTHOR)
    # end def test_rollers_count_per_ratchet

    @features("Feature4610")
    @level("Functionality")
    @services('MainWheel')
    def test_delta_of_roller_movement(self):
        """
        Validate the RotationEvent.delta is positive when the roller is moving away from, or toward the right of,
        the user, negative for opposite
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over roller_index in range({self.config.F_NumRollers}):")
        # --------------------------------------------------------------------------------------------------------------
        for roller_index in range(self.config.F_NumRollers):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Send SetMode request with roller_id={roller_index}, mode={RollerMode.DIVERT!s}")
            # ----------------------------------------------------------------------------------------------------------
            MultiRollerTestUtils.HIDppHelper.set_mode(test_case=self, roller_id=roller_index,
                                                      divert=RollerMode.DIVERT)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over in range(10):")
            # ----------------------------------------------------------------------------------------------------------
            for _ in range(10):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Scroll the rollers[{roller_index}] with random direction and movement")
                # ------------------------------------------------------------------------------------------------------
                # TODO - Implement roller emulator
                expected_delta = choice(range(1, self.config.F_IncrementsPerRotation[roller_index] * 2))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check the RotationEvent.delta is corresponding to the action")
                # ------------------------------------------------------------------------------------------------------
                rotation_event = MultiRollerTestUtils.HIDppHelper.rotation_event(test_case=self)
                self.assertEqual(obtained=rotation_event.delta,
                                 expected=expected_delta,
                                 msg='The delta does not match the actual movement of scrolling roller')

            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_4610_0005", _AUTHOR)
    # end def test_delta_of_roller_movement

    @features("Feature4610")
    @level("Functionality")
    @services('MainWheel')
    def test_timestamp_accuracy_by_rolling_roller_continuously(self):
        """
        Validate the accuracy of timestamp by rolling rollers continuously (Rolling the roller less than or equal to
        1 ms interval)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over roller_index in range({self.config.F_NumRollers}):")
        # --------------------------------------------------------------------------------------------------------------
        for roller_index in range(self.config.F_NumRollers):
            if self.config.F_TimestampReport[roller_index]:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Send SetMode request with roller_id={roller_index}, mode={RollerMode.DIVERT!s}")
                # ------------------------------------------------------------------------------------------------------
                MultiRollerTestUtils.HIDppHelper.set_mode(test_case=self, roller_id=roller_index,
                                                          divert=RollerMode.DIVERT)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Scroll the rollers[{roller_index}] continuously with 5 seconds")
                # ------------------------------------------------------------------------------------------------------
                # TODO - Implement roller emulator

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "Start a loop to collect rotation events")
                # ------------------------------------------------------------------------------------------------------
                rotation_events = []
                while True:
                    rotation_event = MultiRollerTestUtils.HIDppHelper.rotation_event(test_case=self,
                                                                                     allow_no_message=True)
                    if rotation_event is None:
                        break
                    else:
                        rotation_events.append(rotation_event)
                    # end if
                # end while
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "End Loop")
                # ------------------------------------------------------------------------------------------------------
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, "Check the timestamp difference between the last report and the first report is 5000ms")
                # ------------------------------------------------------------------------------------------------------
                # TODO: add a tolerance for time interval checking if needed.
                self.assertEqual(obtained=rotation_events[-1].report_timestamp - rotation_events[0].report_timestamp,
                                 expected=5000,
                                 msg='The timestamp interval does not match the actual duration of scrolling roller')
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_4610_0006", _AUTHOR)
    # end def test_timestamp_accuracy_by_rolling_roller_continuously

    @features("Feature4610")
    @level("Functionality")
    @services('MainWheel')
    def test_timestamp_accuracy(self):
        """
        Validate the accuracy of timestamp by rolling rollers intermittently
        """
        rolling_iteration = 10
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over roller_index in range({self.config.F_NumRollers}):")
        # --------------------------------------------------------------------------------------------------------------
        for roller_index in range(self.config.F_NumRollers):
            if self.config.F_TimestampReport[roller_index]:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Send SetMode request with roller_id={roller_index}, mode={RollerMode.DIVERT!s}")
                # ------------------------------------------------------------------------------------------------------
                MultiRollerTestUtils.HIDppHelper.set_mode(test_case=self, roller_id=roller_index,
                                                          divert=RollerMode.DIVERT)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"Test Loop over in range({rolling_iteration}):")
                # ------------------------------------------------------------------------------------------------------
                durations = []
                for iteration in range(rolling_iteration):
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f"Scroll the rollers[{roller_index}] with random direction and movement")
                    # --------------------------------------------------------------------------------------------------
                    # TODO - Implement roller emulator

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, "Wait for a random duration")
                    # --------------------------------------------------------------------------------------------------
                    durations.append(choice(range(1, 5000)))
                # end for
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "End Test Loop")
                # ------------------------------------------------------------------------------------------------------
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "Start a loop to collect rotation events")
                # ------------------------------------------------------------------------------------------------------
                rotation_events = []
                while True:
                    rotation_event = MultiRollerTestUtils.HIDppHelper.rotation_event(test_case=self,
                                                                                     allow_no_message=True)
                    if rotation_event is None:
                        break
                    else:
                        rotation_events.append(rotation_event)
                    # end if
                # end while
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "End Loop")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check the timestamp interval of each reports match the duration")
                # ------------------------------------------------------------------------------------------------------
                for iteration in range(rolling_iteration - 1):
                    # TODO: add a tolerance for time interval checking if needed.
                    self.assertEqual(
                        obtained=rotation_events[iteration + 1].report_timestamp
                        - rotation_events[iteration].report_timestamp,
                        expected=durations[iteration],
                        msg='The timestamp interval does not match the actual duration of scrolling roller')
                # end for
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_4610_0007", _AUTHOR)
    # end def test_timestamp_accuracy

    @features("Feature4610")
    @level("Functionality")
    def test_divert_mode_is_reset_after_power_cycle(self):
        """
        Validate the divert mode will be reset after device power cycle
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over roller_index in range({self.config.F_NumRollers}):")
        # --------------------------------------------------------------------------------------------------------------
        for roller_index in range(self.config.F_NumRollers):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Send SetMode request with roller_id={roller_index}, mode={RollerMode.DIVERT!s}")
            # ----------------------------------------------------------------------------------------------------------
            MultiRollerTestUtils.HIDppHelper.set_mode(test_case=self, roller_id=roller_index,
                                                      divert=RollerMode.DIVERT)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Power OFF -> ON the device")
            # ----------------------------------------------------------------------------------------------------------
            self.reset(hardware_reset=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetMode request to get the roller mode")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiRollerTestUtils.HIDppHelper.get_mode(test_case=self, roller_id=roller_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, f"Check the roller mode is {RollerMode.DEFAULT_MODE} (not divert) from the response")
            # ----------------------------------------------------------------------------------------------------------
            MultiRollerTestUtils.GetModeResponseChecker.check_fields(
                test_case=self, message=response, expected_cls=self.feature_4610.get_mode_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Scroll the rollers[{roller_index}]")
            # ----------------------------------------------------------------------------------------------------------
            # TODO - Implement roller emulator

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the HID/VolumeUpDown/Dial report is received")
            # ----------------------------------------------------------------------------------------------------------
            # TODO - Enable the below check when the roller emulator is implemented
            # response = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
            #                                  class_type=HidMouse, allow_no_message=True)
            # self.assertNotNone(
            #     obtained=response,
            #     msg=f'No HID report is received when the roller[{roller_index}] is not in divert')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_4610_0008", _AUTHOR)
    # end def test_divert_mode_is_reset_after_power_cycle

    @features("Feature4610")
    @level("Functionality")
    def test_divert_mode_is_reset_after_deep_sleep(self):
        """
        Validate the divert mode will be reset after device left deep-sleep mode
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over roller_index in range({self.config.F_NumRollers}):")
        # --------------------------------------------------------------------------------------------------------------
        for roller_index in range(self.config.F_NumRollers):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Send SetMode request with roller_id={roller_index}, mode={RollerMode.DIVERT!s}")
            # ----------------------------------------------------------------------------------------------------------
            MultiRollerTestUtils.HIDppHelper.set_mode(test_case=self, roller_id=roller_index,
                                                      divert=RollerMode.DIVERT)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set the device to deep-sleep mode via 0x1830")
            # ----------------------------------------------------------------------------------------------------------
            PowerModesTestUtils.HIDppHelper.enter_deep_sleep(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Perform an user action to wake up the device")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.user_action()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetMode request to get the roller mode")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiRollerTestUtils.HIDppHelper.get_mode(test_case=self, roller_id=roller_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, f"Check the roller mode is {RollerMode.DEFAULT_MODE} (not divert) from the response")
            # ----------------------------------------------------------------------------------------------------------
            MultiRollerTestUtils.GetModeResponseChecker.check_fields(
                test_case=self, message=response, expected_cls=self.feature_4610.get_mode_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Scroll the rollers[{roller_index}]")
            # ----------------------------------------------------------------------------------------------------------
            # TODO - Implement roller emulator

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the HID/VolumeUpDown/Dial report is received")
            # ----------------------------------------------------------------------------------------------------------
            # TODO - Enable the below check when the roller emulator is implemented
            # response = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
            #                                  class_type=HidMouse, allow_no_message=True)
            # self.assertNotNone(
            #     obtained=response,
            #     msg=f'No HID report is received when the roller[{roller_index}] is not in divert')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_4610_0009", _AUTHOR)
    # end def test_divert_mode_is_reset_after_deep_sleep

    @features("Feature4610")
    @level("Functionality")
    def test_divert_mode_is_not_reset_after_sleep(self):
        """
        Validate the divert mode won't be reset after device left sleep mode
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over roller_index in range({self.config.F_NumRollers}):")
        # --------------------------------------------------------------------------------------------------------------
        for roller_index in range(self.config.F_NumRollers):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Send SetMode request with roller_id={roller_index}, mode={RollerMode.DIVERT!s}")
            # ----------------------------------------------------------------------------------------------------------
            MultiRollerTestUtils.HIDppHelper.set_mode(test_case=self, roller_id=roller_index,
                                                      divert=RollerMode.DIVERT)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Wait enough duration to make device in sleep mode")
            # ----------------------------------------------------------------------------------------------------------
            sleep(self.f.PRODUCT.DEVICE.F_MaxWaitSleep)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Perform an user action to make the device in run mode")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.user_action()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetMode request to get the roller mode")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiRollerTestUtils.HIDppHelper.get_mode(test_case=self, roller_id=roller_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check the roller mode is {RollerMode.DIVERT!s} from the response")
            # ----------------------------------------------------------------------------------------------------------
            checker = MultiRollerTestUtils.GetModeResponseChecker
            check_map = checker.get_check_map(divert=RollerMode.DIVERT)
            checker.check_fields(test_case=self, message=response,
                                 expected_cls=self.feature_4610.get_mode_response_cls, check_map=check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Scroll the rollers[{roller_index}]")
            # ----------------------------------------------------------------------------------------------------------
            # TODO - Implement roller emulator

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the RotationEvent.delta is corresponding to the {action}")
            # ----------------------------------------------------------------------------------------------------------
            # TODO - Enable the below check when the roller emulator is implemented
            # rotation_event = MultiRollerTestUtils.HIDppHelper.rotation_event(test_case=self)
            # self.assertEqual(obtained=to_int(rotation_event.delta),
            #                  expected=expected_delta,
            #                  msg='The delta does not match the actual action')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_4610_0010", _AUTHOR)
    # end def test_divert_mode_is_not_reset_after_deep_sleep

    @features("Feature4610")
    @level("Functionality")
    def test_get_rollers_capabilities(self):
        """
        Check the capabilities of all rollers.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over roller_index in range({self.config.F_NumRollers}):")
        # --------------------------------------------------------------------------------------------------------------
        for roller_index in range(self.config.F_NumRollers):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Send GetRollerCapabilities request with roller_id={roller_index}")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiRollerTestUtils.HIDppHelper.get_roller_capabilities(test_case=self, roller_id=roller_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check the capabilities of roller {roller_index} are as expected")
            # ----------------------------------------------------------------------------------------------------------
            checker = MultiRollerTestUtils.GetRollerCapabilitiesResponseChecker
            check_map = checker.get_check_map(test_case=self, roller_id=roller_index)
            checker.check_fields(test_case=self, message=response,
                                 expected_cls=self.feature_4610.get_roller_capabilities_response_cls,
                                 check_map=check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_4610_0011", _AUTHOR)
    # end def test_get_rollers_capabilities
# end class MultiRollerFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
