#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hid.keyboard.analogkeys.business
:brief: ``AnalogKeys`` business test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2024/03/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import choice
from time import sleep
from unittest import skip

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagement
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.analogkeysprofileformat import ActionAssignment
from pylibrary.mcu.analogkeysprofileformat import ActionGroup
from pylibrary.mcu.fkcprofileformat import KEY_ID_TO_MODIFIER_BITFIELD
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.analogkeysutils import AnalogKeysTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.fullkeycustomizationutils import FullKeyCustomizationTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.base.profilemanagementutils import ProfileManagementTestUtils
from pytestbox.device.base.unifiedbatteryutils import UnifiedBatteryTestUtils
from pytestbox.device.hid.keyboard.analogkeys.analogkeys import AnalogKeysTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"
_WAIT_REPORT_TIME_MS = 0.1  # This delay constant is used to wait for the device to process all key release reports
_50_MS_DELAY = 0.05         # This delay constant is used to wait between key combination press to be processed


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AnalogKeysBusinessTestCase(AnalogKeysTestCase):
    """
    Validate ``AnalogKeys`` business test cases
    """

    @features("Feature1B08")
    @level("Business")
    @services('DualKeyMatrix')
    def test_key_travel_change_event(self):
        """
        Validate the analog key travel can be read from keyTravelChangeEvent

        NB: This test shall be tested under different battery levels, power modes, charging status.
        """

        def validate_key_travel_event_with_all_available_keys():
            """
            Validate the key travel event is as expected with all available keys

            :raise ``AssertionError``: If the key travel of the event does not match the key travel user performed
            """
            key_travel_range = range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT,
                                     AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT + 1)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send setKeyTravelEventState request to ENABLE key_travel_event_state")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.HIDppHelper.set_key_travel_event_state(
                test_case=self, key_travel_event_state=AnalogKeysTestUtils.Status.ENABLE)
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over all analog keys:")
            # ----------------------------------------------------------------------------------------------------------
            for key in AnalogKeysTestUtils.AnalogKeysHelper.select_standard_keys_randomly(self, num_of_keys=10):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"Test Loop over key_travel in {key_travel_range}:")
                # ------------------------------------------------------------------------------------------------------
                for key_travel in key_travel_range:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(
                        self, f"Perform a key press on the {key!r} with a random travel distance: {key_travel}")
                    # --------------------------------------------------------------------------------------------------
                    self.button_stimuli_emulator.key_displacement(key_id=key, displacement=key_travel)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, "Check the key_travel is as expected from the keyTravelChangeEvent")
                    # --------------------------------------------------------------------------------------------------
                    event = AnalogKeysTestUtils.HIDppHelper.key_travel_change_event(test_case=self)
                    self.assertEqual(expected=key_travel, obtained=to_int(event.key_travel),
                                     msg="The key travel of the event does not match the key travel user performed")

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f"Release the {key!r}")
                    # --------------------------------------------------------------------------------------------------
                    self.button_stimuli_emulator.key_release(key_id=key)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, "Check the key_travel is as expected from the keyTravelChangeEvent")
                    # --------------------------------------------------------------------------------------------------
                    event = AnalogKeysTestUtils.HIDppHelper.key_travel_change_event(test_case=self)
                    self.assertEqual(expected=0, obtained=to_int(event.key_travel),
                                     msg="The key travel of the event does not match the key travel user performed")
                # end for
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "End Test Loop")
                # ------------------------------------------------------------------------------------------------------
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end def validate_key_travel_event_with_all_available_keys

        self._test_use_case_with_all_device_states(user_scenario=validate_key_travel_event_with_all_available_keys)

        self.testCaseChecked("BUS_AKEY_0001", _AUTHOR)
    # end def test_key_travel_change_event

    @features("Feature1B08")
    @level("Business")
    @services('DualKeyMatrix')
    @skip("In development, the LED spy function via SPI is not available yet.")
    def test_key_travel_simulation_on_led(self):
        """
        Validate the analog key travel is simulating on keyboard LEDs through number row keys 1~0, while in analog
        adjustment mode.

        NB:
        - The brightness of number row keys are starting at 50% when a key has not been pressed, then presents key
        travel distance with 100% brightness while a test key press is detected
        - This test shall be tested under different battery levels, power modes, charging status.
        """
        def validate_key_travel_simulation_on_leds():
            """
            Validate the key travel simulation on LEDs of number row keys 1~0
            """
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Enter Global Actuation Point mode (FN + F6)")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.enter_exit_actuation_point_adjustment_mode(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                self, f"Test Loop over key_travel_event_state in: [ENABLE, DISABLE]")
            # ----------------------------------------------------------------------------------------------------------
            for key_travel_event_state in [AnalogKeysTestUtils.Status.ENABLE, AnalogKeysTestUtils.Status.DISABLE]:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send setKeyTravelEventState request to ENABLE key_travel_event_state")
                # ------------------------------------------------------------------------------------------------------
                AnalogKeysTestUtils.HIDppHelper.set_key_travel_event_state(
                    test_case=self, key_travel_event_state=key_travel_event_state)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(
                    self, f"Test Loop over all analog keys: {self.button_stimuli_emulator.get_key_id_list()}")
                # ------------------------------------------------------------------------------------------------------
                for key in self.button_stimuli_emulator.get_key_id_list():
                    key_travel = choice(range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT,
                                              AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT))
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(
                        self, f"Perform a key press on the {key!r} with a random travel distance: {key_travel}")
                    # --------------------------------------------------------------------------------------------------
                    self.button_stimuli_emulator.key_press(key_id=key)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, "Check the key_travel is as expected from the brightness of LEDs on"
                                              "number row keys 1~0")
                    # --------------------------------------------------------------------------------------------------
                    # TODO: Add check method once the LED spy via SPI is ready

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f"Release the {key!r}")
                    # --------------------------------------------------------------------------------------------------
                    self.button_stimuli_emulator.key_release(key_id=key)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, "Check the key_travel is as expected from the brightness of LEDs on"
                                              "number row keys 1~0")
                    # --------------------------------------------------------------------------------------------------
                    # TODO: Add check method once the LED spy via SPI is ready
                # end for
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "End Test Loop")
                # ------------------------------------------------------------------------------------------------------
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end def validate_key_travel_simulation_on_leds

        self._test_use_case_with_all_device_states(user_scenario=validate_key_travel_simulation_on_leds)

        self.testCaseChecked("BUS_AKEY_0002", _AUTHOR)
    # end def test_key_travel_simulation_on_led

    @features("Feature1B08")
    @level("Business")
    @services('DualKeyMatrix')
    @skip("In development, the LED spy function via SPI is not available yet.")
    def test_lighting_effect_stop_resume(self):
        """
        Validate the default lighting effect is stop in analog adjustment mode, and resume once the user exit the
        analog adjustment mode.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press FN key")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=KEY_ID.FN_KEY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check only LEDs of F1 to F7 and FN are ON")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Add check method once the LED spy via SPI is ready

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Release FN")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=KEY_ID.FN_KEY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the RGB lighting effect is in normal mode")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Add check method once the LED spy via SPI is ready

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enter Global Actuation Point mode (FN + F6)")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.enter_exit_actuation_point_adjustment_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check only the LEDs of configuration keys are ON")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Add check method once the LED spy via SPI is ready

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Exit Global Actuation Point mode (ESC)")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_ESCAPE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the RGB lighting effect is in normal mode")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Add check method once the LED spy via SPI is ready

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enter Global Rapid Trigger mode (FN + F7)")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.enter_exit_sensitivity_adjustment_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check only the LEDs of configuration keys are ON")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Add check method once the LED spy via SPI is ready

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Exit Global Actuation Point mode (ESC)")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_ESCAPE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the RGB lighting effect is in normal mode")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Add check method once the LED spy via SPI is ready

        self.testCaseChecked("BUS_AKEY_0003", _AUTHOR)
    # end def test_lighting_effect_stop_resume

    @features("Feature1B08")
    @level("Business")
    @services('DualKeyMatrix')
    def test_no_hid_report_in_analog_adjustment_mode(self):
        """
        In analog adjustment mode, validate HID reports won't be sent to OS when pressing analog keys.

        NB: This test shall be tested under different battery levels, power modes, charging status.
        """
        def validate_no_hid_report_sent_in_analog_adjustment_mode():
            """
            Validate no HID report is sent when pressing analog keys in analog adjustment mode
            """
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over mode in [ActuationPoint, RapidTrigger]:")
            # ----------------------------------------------------------------------------------------------------------
            for mode in ["ActuationPoint", "RapidTrigger"]:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Enter {mode} mode")
                # ------------------------------------------------------------------------------------------------------
                if mode == "ActuationPoint":
                    AnalogKeysTestUtils.enter_exit_actuation_point_adjustment_mode(test_case=self)
                else:
                    AnalogKeysTestUtils.enter_exit_sensitivity_adjustment_mode(test_case=self)
                # end if

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "Test Loop over key_travel_event_state in [ENABLE, DISABLE]:")
                # ------------------------------------------------------------------------------------------------------
                for state in [AnalogKeysTestUtils.Status.ENABLE, AnalogKeysTestUtils.Status.DISABLE]:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f"Send setKeyTravelEventState request to set {state}")
                    # --------------------------------------------------------------------------------------------------
                    AnalogKeysTestUtils.HIDppHelper.set_key_travel_event_state(
                        test_case=self, key_travel_event_state=state)
                    ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_info(
                        self, f"Test Loop over all analog keys: {self.button_stimuli_emulator.get_key_id_list()}")
                    # --------------------------------------------------------------------------------------------------
                    for key in self.button_stimuli_emulator.get_key_id_list():
                        # ESCAPE is the key to exit analog adjustment mode, it shall be skipped.
                        if key == KEY_ID.KEYBOARD_ESCAPE:
                            continue
                        # end if
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_step(self, f"Perform a key press on the {key!r}")
                        # ----------------------------------------------------------------------------------------------
                        self.button_stimuli_emulator.key_press(key_id=key)

                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_check(
                            self, f"Check there is no HID Make report of {key!r} received from the device")
                        # ----------------------------------------------------------------------------------------------
                        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_step(self, f"Release the {key!r}")
                        # ----------------------------------------------------------------------------------------------
                        self.button_stimuli_emulator.key_release(key_id=key)

                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_check(
                            self, f"Check there is no HID Break report of {key!r} received from the device")
                        # ----------------------------------------------------------------------------------------------
                        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
                    # end for
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_info(self, "End Test Loop")
                    # --------------------------------------------------------------------------------------------------
                # end for
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "End Test loop")
                # ------------------------------------------------------------------------------------------------------
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Leave {mode} by pressing ESC")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_ESCAPE)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test loop")
            # ----------------------------------------------------------------------------------------------------------
        # end def validate_no_hid_report_sent_in_analog_adjustment_mode
        self.post_requisite_reload_nvs = True
        self._test_use_case_with_all_device_states(
            user_scenario=validate_no_hid_report_sent_in_analog_adjustment_mode)

        self.testCaseChecked("BUS_AKEY_0004", _AUTHOR)
    # end def test_no_hid_report_in_analog_adjustment_mode

    @features("Feature1B08")
    @level("Business")
    @services('DualKeyMatrix')
    def test_save_base_profile_configurations(self):
        """
        Validate the global analog settings can be saved to the base profile when pressing FN+F6 / FN+F7 to exit
        analog adjustment mode / rapid trigger mode.
        """
        actuation_scaling_range_list = [int(element) for element in self.config.F_ActuationScalingRange]
        actuation_scaling_range = iter(self.config.F_ActuationScalingRange)
        sensitivity_scaling_range_list = [int(element) for element in self.config.F_SensitivityScalingRange]
        sensitivity_scaling_range = iter(self.config.F_SensitivityScalingRange)
        actuation_point = self.config.F_DefaultActuationPoint
        sensitivity = self.config.F_DefaultSensitivity
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Base Profile")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.switch_to_base_profile(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over adjustment_method in {self.ADJUSTMENT_KEYS}")
        # --------------------------------------------------------------------------------------------------------------
        for index, adjustment_key in enumerate(self.ADJUSTMENT_KEYS):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Enter Actuation Point mode (FN + F6)")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.enter_exit_actuation_point_adjustment_mode(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Adjust actuation point by performing a keystroke on {KEY_ID(adjustment_key)}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=adjustment_key)
            if adjustment_key in self.DECREASE_KEYS:
                actuation_point = actuation_scaling_range_list[actuation_scaling_range_list.index(actuation_point) - 1]
            elif adjustment_key in self.INCREASE_KEYS:
                actuation_point = actuation_scaling_range_list[actuation_scaling_range_list.index(actuation_point) + 1]
            else:
                actuation_point = int(next(actuation_scaling_range))
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Exit Actuation Point mode and save settings (FN + F6)")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.enter_exit_actuation_point_adjustment_mode(test_case=self)

            random_selected_key = choice(list(self.button_stimuli_emulator.keyboard_layout.KEYID_2_CHAINID.keys()))
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Perform a {random_selected_key!r} press with key_travel = {actuation_point}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=random_selected_key, displacement=actuation_point)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check HID Make report of {random_selected_key!r} is received from the device")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(random_selected_key, MAKE))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release the {random_selected_key!r}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key_id=random_selected_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check HID Break report of {random_selected_key!r} is received from the device")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(random_selected_key, BREAK))
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over adjustment_method in {self.ADJUSTMENT_KEYS}")
        # --------------------------------------------------------------------------------------------------------------
        for index, adjustment_key in enumerate(self.ADJUSTMENT_KEYS):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Enter Rapid Trigger mode (FN + F7)")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.enter_exit_sensitivity_adjustment_mode(test_case=self)

            if index == 0:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "Enable Rapid Trigger by pressing F7")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_F7)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Adjust sensitivity by performing a keystroke on {adjustment_key!r}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=adjustment_key)
            if adjustment_key in self.DECREASE_KEYS:
                sensitivity = sensitivity_scaling_range_list[sensitivity_scaling_range_list.index(sensitivity) - 1]
            elif adjustment_key in self.INCREASE_KEYS:
                sensitivity = sensitivity_scaling_range_list[sensitivity_scaling_range_list.index(sensitivity) + 1]
            else:
                sensitivity = int(next(sensitivity_scaling_range))
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Exit Rapid Trigger mode and save settings (FN + F7)")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.enter_exit_sensitivity_adjustment_mode(test_case=self)

            random_selected_key = choice(list(self.button_stimuli_emulator.keyboard_layout.KEYID_2_CHAINID.keys()))
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Perform a {random_selected_key!r} press with key_travel = {actuation_point}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=random_selected_key, displacement=actuation_point)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check HID Make report of {random_selected_key!r} is received from the device")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(random_selected_key, MAKE))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release the {random_selected_key!r} with key_travel = {sensitivity}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=random_selected_key,
                                                          displacement=actuation_point - sensitivity)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check HID Break report of {random_selected_key!r} is received from the device")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(random_selected_key, BREAK))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over key_travel_distance in range(setting_actuation_point,"
                                     "max_travel_distance)")
            # ----------------------------------------------------------------------------------------------------------
            for key_travel in range(actuation_point, AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT + 1):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Perform a random {random_selected_key!r} press with key_travel = {key_travel}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(key_id=random_selected_key, displacement=key_travel)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check HID Make report of {random_selected_key!r} is received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(random_selected_key, MAKE))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Release the {random_selected_key!r} with key_travel = {sensitivity}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(key_id=random_selected_key,
                                                              displacement=key_travel - sensitivity)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check HID Break report of {random_selected_key!r} is received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(random_selected_key, BREAK))
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------

            self.button_stimuli_emulator.key_press(key_id=random_selected_key)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                self, "Test Loop over key_travel_distance in range(max_travel_distance, setting_actuation_point, -1)")
            # ----------------------------------------------------------------------------------------------------------
            for key_travel in range(AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT, actuation_point, -1):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Release the {random_selected_key!r} with key_travel = {sensitivity}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(key_id=random_selected_key,
                                                              displacement=key_travel - sensitivity)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check HID Break report of {random_selected_key!r} is received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(random_selected_key, BREAK))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Perform a random {random_selected_key!r} press with key_travel = {sensitivity}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(key_id=random_selected_key, displacement=key_travel)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check HID Make report of {random_selected_key!r} is received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(random_selected_key, MAKE))
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release the {random_selected_key!r} with key_travel = {sensitivity + 1}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key_id=random_selected_key)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_AKEY_0005", _AUTHOR)
    # end def test_save_base_profile_configurations

    @features("Feature1B08")
    @level("Business")
    @services('DualKeyMatrix')
    def test_configurations_not_save_in_base_profile(self):
        """
        Validate the users are able to press ESC to exit analog adjustment mode, and all configuration are not saved
        to the base profile.
        """
        actuation_point = self.config.F_DefaultActuationPoint
        sensitivity = self.config.F_DefaultSensitivity
        actuation_scaling_range_list = [int(element) for element in self.config.F_ActuationScalingRange]
        actuation_scaling_range = iter(self.config.F_ActuationScalingRange)
        sensitivity_scaling_range_list = [int(element) for element in self.config.F_SensitivityScalingRange]
        sensitivity_scaling_range = iter(self.config.F_SensitivityScalingRange)
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Base Profile")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.switch_to_base_profile(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over adjustment_method in {self.ADJUSTMENT_KEYS}")
        # --------------------------------------------------------------------------------------------------------------
        for adjustment_key in self.ADJUSTMENT_KEYS:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Enter Actuation Point mode (FN + F6)")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.enter_exit_actuation_point_adjustment_mode(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Adjust actuation point to by performing a keystroke on {adjustment_key!r}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=adjustment_key)
            if adjustment_key in self.DECREASE_KEYS:
                actuation_point = actuation_scaling_range_list[actuation_scaling_range_list.index(actuation_point) - 1]
            elif adjustment_key in self.INCREASE_KEYS:
                actuation_point = actuation_scaling_range_list[actuation_scaling_range_list.index(actuation_point) + 1]
            else:
                actuation_point = int(next(actuation_scaling_range))
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Exit Actuation Point mode (ESC)")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_ESCAPE)

            random_selected_key = choice(list(self.button_stimuli_emulator.keyboard_layout.KEYID_2_CHAINID.keys()))
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Perform a {random_selected_key!r} press with key_travel = {actuation_point}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=random_selected_key, displacement=actuation_point)

            if actuation_point >= self.config.F_DefaultActuationPoint:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self,
                                    f"Check HID Make report of {random_selected_key!r} is received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(random_selected_key, MAKE))
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check there is no HID Make report of {random_selected_key} received from the device")
                # ------------------------------------------------------------------------------------------------------
                ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {random_selected_key!r}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key_id=random_selected_key)

            if actuation_point >= self.config.F_DefaultActuationPoint:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self,
                                    f"Check HID Break report of {random_selected_key!r} is received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(random_selected_key, BREAK))
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check there is no HID Break report of {random_selected_key!r} received from the device")
                # ------------------------------------------------------------------------------------------------------
                ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Fully press {random_selected_key!r}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key_id=random_selected_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check HID Make report of {random_selected_key!r} is received from the device")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(random_selected_key, MAKE))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Fully release {random_selected_key!r}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key_id=random_selected_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check HID Break report of {random_selected_key!r} is received from the device")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(random_selected_key, BREAK))
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over adjustment_method in {self.ADJUSTMENT_KEYS}")
        # --------------------------------------------------------------------------------------------------------------
        for adjustment_key in self.ADJUSTMENT_KEYS:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Enter Rapid Trigger mode (FN + F7)")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.enter_exit_sensitivity_adjustment_mode(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Adjust sensitivity by performing a keystroke on {adjustment_key!r}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=adjustment_key)
            if adjustment_key in self.DECREASE_KEYS:
                sensitivity = sensitivity_scaling_range_list[sensitivity_scaling_range_list.index(sensitivity) - 1]
            elif adjustment_key in self.INCREASE_KEYS:
                sensitivity = sensitivity_scaling_range_list[sensitivity_scaling_range_list.index(sensitivity) + 1]
            else:
                sensitivity = int(next(sensitivity_scaling_range))
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Enable Rapid Trigger by pressing F7")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_F7)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Exit Rapid Trigger mode (ESC)")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_ESCAPE)

            random_selected_key = choice(list(self.button_stimuli_emulator.keyboard_layout.KEYID_2_CHAINID.keys()))
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Fully press {random_selected_key!r}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key_id=random_selected_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check HID Make report of {random_selected_key!r} is received from the device")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(random_selected_key, MAKE))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {random_selected_key!r} with key_travel = "
                                     f"{AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT - sensitivity}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(
                key_id=random_selected_key,
                displacement=AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT - sensitivity)

            if AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT - sensitivity <= \
                    self.config.F_DefaultActuationPoint - AnalogKeysTestUtils.AnalogKeysHelper.RELEASE_POINT_DELTA:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self,
                                    f"Check HID Break report of {random_selected_key!r} is received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(random_selected_key, BREAK))
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check there is no HID Break report of {random_selected_key!r} received from the device")
                # ------------------------------------------------------------------------------------------------------
                ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {random_selected_key!r} with "
                                     f"key_travel = {AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(
                key_id=random_selected_key, displacement=AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT)

            if AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT - sensitivity <= \
                    self.config.F_DefaultActuationPoint - AnalogKeysTestUtils.AnalogKeysHelper.RELEASE_POINT_DELTA:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self,
                                    f"Check HID Make report of {random_selected_key!r} is received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(random_selected_key, MAKE))
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check there is no HID Make report of {random_selected_key!r} is received from the device")
                # ------------------------------------------------------------------------------------------------------
                ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Fully release {random_selected_key!r}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key_id=random_selected_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check HID Break report of {random_selected_key!r} is received from the device")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(random_selected_key, BREAK))
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_AKEY_0006", _AUTHOR)
    # end def test_configurations_not_save_in_base_profile

    @features("Feature1B08")
    @features("Feature8101")
    @level("Business")
    @services('DualKeyMatrix')
    def test_configure_onboard_profile_actuation_point_via_software(self):
        """
        Validate the users are able to adjust the global actuation point and apply it to onboard profiles via
        software.
        """
        self._test_configure_profile_actuation_point_via_software(
            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE)

        self.testCaseChecked("BUS_AKEY_0007", _AUTHOR)
    # end def test_configure_onboard_profile_actuation_point_via_software

    @features("Feature1B08")
    @features("Feature8101")
    @level("Business")
    @services('DualKeyMatrix')
    def test_configure_host_profile_actuation_point_via_software(self):
        """
        Validate the users are able to adjust the global actuation point and apply it to host profiles via software.
        """
        self._test_configure_profile_actuation_point_via_software(
            file_type_id=ProfileManagement.FileTypeId.X8101.HOST_MODE_PROFILE)

        self.testCaseChecked("BUS_AKEY_0008", _AUTHOR)
    # end def test_configure_host_profile_actuation_point_via_software

    @features("Feature1B08")
    @features("Feature8101")
    @level("Business")
    @services('DualKeyMatrix')
    def test_configure_onboard_profile_per_key_actuation_point_via_software(self):
        """
        Validate the users are able to adjust the per key actuation points and apply them to onboard profiles via
        software.
        """
        self._test_configure_profile_per_key_actuation_point_via_software(
            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE)

        self.testCaseChecked("BUS_AKEY_0009", _AUTHOR)
    # end def test_configure_onboard_profile_per_key_actuation_point_via_software

    @features("Feature1B08")
    @features("Feature8101")
    @level("Business")
    @services('DualKeyMatrix')
    def test_configure_host_profile_per_key_actuation_point_via_software(self):
        """
        Validate the users are able to adjust the per key actuation points and apply them to host profiles via
        software.
        """
        self._test_configure_profile_per_key_actuation_point_via_software(
            file_type_id=ProfileManagement.FileTypeId.X8101.HOST_MODE_PROFILE)

        self.testCaseChecked("BUS_AKEY_0010", _AUTHOR)
    # end def test_configure_host_profile_per_key_actuation_point_via_software

    @features("Feature1B08")
    @features("Feature8101")
    @level("Business")
    @services('DualKeyMatrix')
    def test_rapid_trigger_and_multi_action_settings_in_onboard_profile(self):
        """
        Validate the rapid trigger and multi-action are referring to same actuation point of the onboard profile.
        """
        self._test_rapid_trigger_and_multi_action_settings_in_profile(
            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE)

        self.testCaseChecked("BUS_AKEY_0011", _AUTHOR)
    # end def test_rapid_trigger_and_multi_action_settings_in_onboard_profile

    @features("Feature1B08")
    @features("Feature8101")
    @level("Business")
    @services('DualKeyMatrix')
    def test_rapid_trigger_and_multi_action_settings_in_host_profile(self):
        """
        Validate the rapid trigger and multi-action are referring to same actuation point of the host profile.
        """
        self._test_rapid_trigger_and_multi_action_settings_in_profile(
            file_type_id=ProfileManagement.FileTypeId.X8101.HOST_MODE_PROFILE)

        self.testCaseChecked("BUS_AKEY_0012", _AUTHOR)
    # end def test_rapid_trigger_and_multi_action_settings_in_host_profile

    @features("Feature1B08")
    @features("Feature8101")
    @level("Business")
    @services('DualKeyMatrix')
    def test_enable_disable_rapid_trigger_via_software(self):
        """
        Validate users are able to enable or disable rapid trigger via software.
        """
        random_selected_keys = AnalogKeysTestUtils.AnalogKeysHelper.select_standard_keys_randomly(self, num_of_keys=10)
        actuation_point = self.config.F_DefaultActuationPoint
        sensitivity = self.config.F_DefaultSensitivity
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create onboard profiles")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestUtils.ProfileHelper.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over onboard profiles")
        # --------------------------------------------------------------------------------------------------------------
        for profile in profiles:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Edit the Global Actuation Point of {profile} with a random AP ="
                                     f"{actuation_point}")
            # ----------------------------------------------------------------------------------------------------------
            profile.update_tag_content(
                directory=directory,
                tag_content_dict={ProfileManagement.Tag.ANALOG_GENERIC_SETTING: actuation_point << 8})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Create a Rapid Trigger configuration table and set random {sensitivity} to"
                                     f"random selected {random_selected_keys!r}")
            # ----------------------------------------------------------------------------------------------------------
            sensitivity_per_key = AnalogKeysTestUtils.AnalogKeysHelper.create_sensitivity_configuration_per_key(
                test_case=self,
                keys_and_sensitivities={random_selected_key: sensitivity
                                        for random_selected_key in random_selected_keys})
            rapid_trigger_table = AnalogKeysTestUtils.AnalogKeysHelper.create_rapid_trigger_table(
                test_case=self, directory=directory, sensitivity_per_keys=sensitivity_per_key)
            ProfileManagementTestUtils.write(test_case=self, data=HexList(rapid_trigger_table),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=rapid_trigger_table.first_sector_id_lsb,
                                             crc_32=rapid_trigger_table.crc_32)
            profile.update_tag_content(
                directory=directory,
                tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B08_RAPID_TRIGGER:
                                  rapid_trigger_table.table_id})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Write 0x8101 profile to NVS\n{profile}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=profile.first_sector_id_lsb,
                                             crc_32=profile.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Update the directory and save in the NVS\n{directory}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(directory),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=directory.first_sector_id_lsb,
                                             crc_32=directory.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Active the {profile} with the Rapid Trigger configuration table")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                                file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                                file_id=profile.file_id_lsb,
                                                count=len(HexList(profile)),
                                                crc_32=profile.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send setRapidTriggerState request to DISABLE rapid_trigger_state")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.HIDppHelper.set_rapid_trigger_state(
                test_case=self, rapid_trigger_state=AnalogKeysTestUtils.Status.DISABLE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Perform keystrokes and check reports in rapid trigger disable")
            # ----------------------------------------------------------------------------------------------------------
            self.perform_keystrokes_on_keys_and_check_reports(keys=random_selected_keys,
                                                              actuation_point=actuation_point,
                                                              sensitivity=sensitivity,
                                                              rapid_trigger_state=AnalogKeysTestUtils.Status.DISABLE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send setRapidTriggerState request to ENABLE rapid_trigger_state")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.HIDppHelper.set_rapid_trigger_state(
                test_case=self, rapid_trigger_state=AnalogKeysTestUtils.Status.ENABLE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Perform keystrokes and check reports in rapid trigger enable")
            # ----------------------------------------------------------------------------------------------------------
            self.perform_keystrokes_on_keys_and_check_reports(keys=random_selected_keys,
                                                              actuation_point=actuation_point,
                                                              sensitivity=sensitivity,
                                                              rapid_trigger_state=AnalogKeysTestUtils.Status.ENABLE)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_AKEY_0013", _AUTHOR)
    # end def test_enable_disable_rapid_trigger_via_software

    @features("Feature1B08")
    @level("Business")
    @services('DualKeyMatrix')
    def test_enable_disable_rapid_trigger_via_predefined_keys(self):
        """
        Validate users are able to enable or disable rapid trigger via pre-defined trigger keys.
        """
        random_selected_keys = AnalogKeysTestUtils.AnalogKeysHelper.select_standard_keys_randomly(self, num_of_keys=10)
        actuation_point = self.config.F_DefaultActuationPoint
        sensitivity = self.config.F_DefaultSensitivity
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Base Profile (FN + F5)")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.switch_to_base_profile(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enter Global Rapid Trigger mode (FN + F7)")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.enter_exit_sensitivity_adjustment_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Enable Rapid Trigger via {KEY_ID.KEYBOARD_F7!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_F7)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check only the LEDs of configuration keys are ON")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Add check method once the LED spy via SPI is ready

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Save settings and exit Global Rapid Trigger mode (FN + F7)")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.enter_exit_sensitivity_adjustment_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Perform keystrokes and check reports in rapid trigger enable")
        # --------------------------------------------------------------------------------------------------------------
        self.perform_keystrokes_on_keys_and_check_reports(keys=random_selected_keys,
                                                          actuation_point=actuation_point,
                                                          sensitivity=sensitivity,
                                                          rapid_trigger_state=AnalogKeysTestUtils.Status.ENABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enter Global Rapid Trigger mode (FN + F7)")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.enter_exit_sensitivity_adjustment_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Disable Rapid Trigger via F7")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_F7)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check only the LEDs of configuration keys are ON, except number row keys 1~0")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Add check method once the LED spy via SPI is ready

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Save settings and exit Global Rapid Trigger mode (FN + F7)")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.enter_exit_sensitivity_adjustment_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Perform keystrokes and check reports in rapid trigger disable")
        # --------------------------------------------------------------------------------------------------------------
        self.perform_keystrokes_on_keys_and_check_reports(keys=random_selected_keys,
                                                          actuation_point=actuation_point,
                                                          sensitivity=sensitivity,
                                                          rapid_trigger_state=AnalogKeysTestUtils.Status.DISABLE)

        self.testCaseChecked("BUS_AKEY_0014", _AUTHOR)
    # end def test_enable_disable_rapid_trigger_via_predefined_keys

    @features("Feature1B08")
    @level("Business")
    @services('DualKeyMatrix')
    def test_continuous_rapid_trigger(self):
        """
        Validate the continuous rapid trigger features as the rapid trigger default settings.
        """
        random_selected_keys = AnalogKeysTestUtils.AnalogKeysHelper.select_standard_keys_randomly(self, num_of_keys=10)
        actuation_point = self.config.F_DefaultActuationPoint
        sensitivity = self.config.F_DefaultSensitivity
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Base Profile (FN + F5)")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.switch_to_base_profile(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enter Rapid Trigger mode (FN + F7)")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.enter_exit_sensitivity_adjustment_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable Rapid Trigger via F7")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_F7)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Exit Rapid Trigger mode and save settings (FN + F7)")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.enter_exit_sensitivity_adjustment_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over selected keys: {random_selected_keys!r}")
        # --------------------------------------------------------------------------------------------------------------
        for random_selected_key in random_selected_keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Perform a key press on {random_selected_key!r} with key_travel = {actuation_point}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=random_selected_key, displacement=actuation_point)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID MAKE report is received from the device")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(random_selected_key, MAKE))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Release {random_selected_key!r} with key_travel = {actuation_point - sensitivity}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=random_selected_key,
                                                          displacement=actuation_point - sensitivity)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID BREAK report is received from the device")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(random_selected_key, BREAK))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {random_selected_key!r} with key_travel = "
                                     f"{AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(
                key_id=random_selected_key, displacement=AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check there is no HID BREAK report received from the device")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                self, f"Test Loop over validation_range in "
                      f"{range(actuation_point, AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT)} and "
                      f"{range(AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT, 0, -1)}")
            # ----------------------------------------------------------------------------------------------------------
            for validation_range, direction in \
                    zip([range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT,
                               AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT - sensitivity),
                         range(AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT - sensitivity, 0, -1)],
                        ['increase', 'decrease']):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"Test Loop over key_travel in {validation_range}")
                # ------------------------------------------------------------------------------------------------------
                for key_travel in validation_range:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(
                        self, f"Perform a random {random_selected_key!r} press with key_travel = "
                              f"{key_travel + sensitivity}")
                    # --------------------------------------------------------------------------------------------------
                    self.button_stimuli_emulator.key_displacement(key_id=random_selected_key,
                                                                  displacement=key_travel + sensitivity)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(
                        self, f"Check HID Make report of {random_selected_key!r} is received from the device")
                    # --------------------------------------------------------------------------------------------------
                    KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                                  key=KeyMatrixTestUtils.Key(random_selected_key, MAKE))

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(
                        self, f"Release the {random_selected_key!r} with key_travel = {key_travel}")
                    # --------------------------------------------------------------------------------------------------
                    self.button_stimuli_emulator.key_displacement(key_id=random_selected_key,
                                                                  displacement=key_travel)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(
                        self, f"Check HID Break report of {random_selected_key!r} is received from the device")
                    # --------------------------------------------------------------------------------------------------
                    KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                                  key=KeyMatrixTestUtils.Key(random_selected_key,
                                                                                             BREAK))
                    if direction == 'decrease':
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_step(
                            self, f"Release the {random_selected_key!r} with key_travel = {key_travel - 1}")
                        # ----------------------------------------------------------------------------------------------
                        self.button_stimuli_emulator.key_displacement(key_id=random_selected_key,
                                                                      displacement=key_travel - 1)

                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_check(self, "Check there is no HID BREAK report received from the device")
                        # ----------------------------------------------------------------------------------------------
                        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
                    # end if
                # end for
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "End Test Loop")
                # ------------------------------------------------------------------------------------------------------
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_AKEY_0015", _AUTHOR)
    # end def test_continuous_rapid_trigger

    @features("Feature1B08")
    @level("Business")
    @services('DualKeyMatrix')
    def test_configure_onboard_profile_global_sensitivity_via_software(self):
        """
        Validate the users are able to adjust the global sensitivity and apply it to onboard profiles via software.
        """
        self._test_configure_profile_global_sensitivity_via_software(
            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE)

        self.testCaseChecked("BUS_AKEY_0016", _AUTHOR)
    # end def test_configure_onboard_profile_global_sensitivity_via_software

    @features("Feature1B08")
    @level("Business")
    @services('DualKeyMatrix')
    def test_configure_host_profile_global_sensitivity_via_software(self):
        """
        Validate the users are able to adjust the global sensitivity and apply it to host profiles via software.
        """
        self._test_configure_profile_global_sensitivity_via_software(
            file_type_id=ProfileManagement.FileTypeId.X8101.HOST_MODE_PROFILE)

        self.testCaseChecked("BUS_AKEY_0017", _AUTHOR)
    # end def test_configure_host_profile_global_sensitivity_via_software

    @features("Feature1B08")
    @level("Business")
    @services('DualKeyMatrix')
    def test_configure_onboard_profile_per_key_sensitivity_via_software(self):
        """
        Validate the users are able to adjust the per key sensitivity and apply it to onboard profiles via software.
        """
        self._test_configure_profile_per_key_sensitivity_via_software(
            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE)

        self.testCaseChecked("BUS_AKEY_0018", _AUTHOR)
    # end def test_configure_onboard_profile_per_key_sensitivity_via_software

    @features("Feature1B08")
    @level("Business")
    @services('DualKeyMatrix')
    def test_configure_host_profile_per_key_sensitivity_via_software(self):
        """
        Validate the users are able to adjust the per key sensitivity and apply it to host profiles via software.
        """
        self._test_configure_profile_per_key_sensitivity_via_software(
            file_type_id=ProfileManagement.FileTypeId.X8101.HOST_MODE_PROFILE)

        self.testCaseChecked("BUS_AKEY_0019", _AUTHOR)
    # end def test_configure_host_profile_per_key_sensitivity_via_software

    @features("Feature1B08")
    @level("Business")
    @services('DualKeyMatrix')
    def test_analog_adjustment_mode_settings(self):
        """
        Validate the global analog settings adjusted in the analog adjustment mode are only applying on base profile.
        """
        base_profile_actuation_scaling_range_list = [int(element) for element in self.config.F_ActuationScalingRange]
        base_profile_sensitivity_scaling_range_list = \
            [int(element) for element in self.config.F_SensitivityScalingRange]
        base_profile_actuation_point = choice(base_profile_actuation_scaling_range_list)
        base_profile_sensitivity = choice(base_profile_sensitivity_scaling_range_list)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create onboard profiles")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestUtils.ProfileHelper.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over onboard profiles")
        # --------------------------------------------------------------------------------------------------------------
        for index, profile in enumerate(profiles):
            random_selected_keys = AnalogKeysTestUtils.AnalogKeysHelper.select_standard_keys_randomly(
                self, num_of_keys=10)
            sensitivity = choice(range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_SENSITIVITY,
                                       AnalogKeysTestUtils.AnalogKeysHelper.MAX_SENSITIVITY))
            actuation_point = choice(range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT,
                                           AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT - sensitivity))
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Edit the Actuation Point of {profile} with random {actuation_point}")
            # ----------------------------------------------------------------------------------------------------------
            profile.update_tag_content(
                directory=directory,
                tag_content_dict={ProfileManagement.Tag.ANALOG_GENERIC_SETTING: actuation_point << 8})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Create a Rapid Trigger configuration table and set sensitivity with a random"
                                     f"{sensitivity}")
            # ----------------------------------------------------------------------------------------------------------
            sensitivity_per_key = AnalogKeysTestUtils.AnalogKeysHelper.create_sensitivity_configuration_per_key(
                test_case=self,
                keys_and_sensitivities={key: sensitivity for key in random_selected_keys})
            rapid_trigger_table = AnalogKeysTestUtils.AnalogKeysHelper.create_rapid_trigger_table(
                test_case=self, directory=directory, sensitivity_per_keys=sensitivity_per_key)
            ProfileManagementTestUtils.write(test_case=self, data=HexList(rapid_trigger_table),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=rapid_trigger_table.first_sector_id_lsb,
                                             crc_32=rapid_trigger_table.crc_32)
            profile.update_tag_content(
                directory=directory,
                tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B08_RAPID_TRIGGER:
                                  rapid_trigger_table.table_id})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Write 0x8101 profile to NVS\n{profile}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=profile.first_sector_id_lsb,
                                             crc_32=profile.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Update the directory and save in the NVS\n{directory}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(directory),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=directory.first_sector_id_lsb,
                                             crc_32=directory.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Active Base Profile (FN + F5)")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.switch_to_base_profile(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Enter Global Actuation Point mode (FN + F6)")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.enter_exit_actuation_point_adjustment_mode(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Adjust actuation point to {base_profile_actuation_point}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(
                key_id=KEY_ID.KEYBOARD_1 +
                base_profile_actuation_scaling_range_list.index(base_profile_actuation_point))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Exit Global Actuation Point mode and save settings (FN + F6)")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.enter_exit_actuation_point_adjustment_mode(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Enter Global Rapid Trigger mode (FN + F7)")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.enter_exit_sensitivity_adjustment_mode(test_case=self)

            if index == 0:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Enable Rapid Trigger via F7")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_F7)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Adjust sensitivity to {base_profile_sensitivity}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(
                key_id=KEY_ID.KEYBOARD_1 +
                base_profile_sensitivity_scaling_range_list.index(base_profile_sensitivity))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Exit Global Rapid Trigger mode and save settings (FN + F7)")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.enter_exit_sensitivity_adjustment_mode(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Perform keystrokes and check reports in rapid trigger enable")
            # ----------------------------------------------------------------------------------------------------------
            self.perform_keystrokes_on_keys_and_check_reports(keys=random_selected_keys,
                                                              actuation_point=base_profile_actuation_point,
                                                              sensitivity=base_profile_sensitivity,
                                                              rapid_trigger_state=AnalogKeysTestUtils.Status.ENABLE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Active the {profile} with the Actuation Point and Rapid Trigger"
                                     "configuration tables")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                                file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                                file_id=profile.file_id_lsb,
                                                count=len(HexList(profile)),
                                                crc_32=profile.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send setRapidTriggerState request to ENABLE rapid_trigger_state")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.HIDppHelper.set_rapid_trigger_state(
                test_case=self, rapid_trigger_state=AnalogKeysTestUtils.Status.ENABLE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Perform keystrokes and check reports in rapid trigger enable")
            # ----------------------------------------------------------------------------------------------------------
            self.perform_keystrokes_on_keys_and_check_reports(keys=random_selected_keys,
                                                              actuation_point=actuation_point,
                                                              sensitivity=sensitivity,
                                                              rapid_trigger_state=AnalogKeysTestUtils.Status.ENABLE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Active Base Profile (FN + F5)")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.switch_to_base_profile(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Perform keystrokes and check reports in rapid trigger enable")
            # ----------------------------------------------------------------------------------------------------------
            self.perform_keystrokes_on_keys_and_check_reports(keys=random_selected_keys,
                                                              actuation_point=base_profile_actuation_point,
                                                              sensitivity=base_profile_sensitivity,
                                                              rapid_trigger_state=AnalogKeysTestUtils.Status.ENABLE)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_AKEY_0020", _AUTHOR)
    # end def test_analog_adjustment_mode_settings

    @features("Feature1B08")
    @level("Business")
    @services('DualKeyMatrix')
    def test_two_actuation_points(self):
        """
        Validate users are able to set two different actuation points for one key via software.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create onboard profiles")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestUtils.ProfileHelper.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over onboard profiles")
        # --------------------------------------------------------------------------------------------------------------
        for index, profile in enumerate(profiles):
            random_selected_keys = AnalogKeysTestUtils.AnalogKeysHelper.select_standard_keys_randomly(
                self, num_of_keys=1)
            actuation_point = choice(
                range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT,
                      AnalogKeysTestUtils.AnalogKeysHelper.MA_MAX_FIRST_ACTUATION_POINT))
            second_actuation_point = choice(
                range(actuation_point + AnalogKeysTestUtils.AnalogKeysHelper.MA_RELEASE_POINT_DELTA,
                      AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT + 1))
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Edit the Actuation Point of {profile} with random {actuation_point}")
            # ----------------------------------------------------------------------------------------------------------
            profile.update_tag_content(
                directory=directory,
                tag_content_dict={ProfileManagement.Tag.ANALOG_GENERIC_SETTING: actuation_point << 8})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Create a Multi-Action configuration table to set second Actuation Point with"
                                     f"{second_actuation_point} and defined assignments randomly")
            # ----------------------------------------------------------------------------------------------------------
            groups = [ActionGroup(trigger_key=random_selected_key, second_actuation_point=second_actuation_point,
                                  random_assignments=True)
                      for random_selected_key in random_selected_keys]
            multi_action_table = AnalogKeysTestUtils.AnalogKeysHelper.create_multi_action_table(test_case=self,
                                                                                                preset_groups=groups,
                                                                                                directory=directory)
            ProfileManagementTestUtils.write(test_case=self, data=HexList(multi_action_table),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=multi_action_table.first_sector_id_lsb,
                                             crc_32=multi_action_table.crc_32)
            profile.update_tag_content(
                directory=directory,
                tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B08_MULTI_ACTION:
                                  multi_action_table.table_id})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Write 0x8101 profile to NVS\n{profile}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=profile.first_sector_id_lsb,
                                             crc_32=profile.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Update the directory and save in the NVS\n{directory}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(directory),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=directory.first_sector_id_lsb,
                                             crc_32=directory.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Active the {profile} with the Multi-Action configuration table")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                                file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                                file_id=profile.file_id_lsb,
                                                count=len(HexList(profile)),
                                                crc_32=profile.crc_32)

            if index == 0:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Enable Multi-Action")
                # ------------------------------------------------------------------------------------------------------
                AnalogKeysTestUtils.enable_disable_multi_action_fkc(test_case=self)
            # end if
            sleep(_WAIT_REPORT_TIME_MS)
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Test Loop over selected keys: {random_selected_keys}")
            # ----------------------------------------------------------------------------------------------------------
            for random_selected_key in random_selected_keys:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Perform a key press on {random_selected_key!r} with key_travel = {actuation_point}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(key_id=random_selected_key, displacement=actuation_point)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check HID report(s) match the event0")
                # ------------------------------------------------------------------------------------------------------
                AnalogKeysTestUtils.MultiActionChecker.check_multi_actions(
                    test_case=self,
                    trigger_key=random_selected_key,
                    multi_action_table=multi_action_table,
                    last_actuation_point=0,
                    current_actuation_point=actuation_point,
                    global_actuation_point=actuation_point)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Perform a key press on {random_selected_key!r} with key_travel = {second_actuation_point}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(
                    key_id=random_selected_key, displacement=second_actuation_point)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check HID report(s) match the event1")
                # ------------------------------------------------------------------------------------------------------
                AnalogKeysTestUtils.MultiActionChecker.check_multi_actions(
                    test_case=self,
                    trigger_key=random_selected_key,
                    multi_action_table=multi_action_table,
                    last_actuation_point=actuation_point,
                    current_actuation_point=second_actuation_point,
                    global_actuation_point=actuation_point)

                second_actuation_release_point = \
                    min(int((second_actuation_point - actuation_point) / 2) + actuation_point,
                        second_actuation_point - AnalogKeysTestUtils.AnalogKeysHelper.MA_RELEASE_POINT_DELTA)
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Release {random_selected_key!r} with key_travel = "
                                         f"{second_actuation_release_point}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(
                    key_id=random_selected_key, displacement=second_actuation_release_point)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check HID report(s) match the event2")
                # ------------------------------------------------------------------------------------------------------
                AnalogKeysTestUtils.MultiActionChecker.check_multi_actions(
                    test_case=self,
                    trigger_key=random_selected_key,
                    multi_action_table=multi_action_table,
                    last_actuation_point=second_actuation_point,
                    current_actuation_point=second_actuation_release_point,
                    global_actuation_point=actuation_point)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Fully release the {random_selected_key!r}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_release(key_id=random_selected_key)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check HID report(s) match the event3")
                # ------------------------------------------------------------------------------------------------------
                AnalogKeysTestUtils.MultiActionChecker.check_multi_actions(
                    test_case=self,
                    trigger_key=random_selected_key,
                    multi_action_table=multi_action_table,
                    last_actuation_point=second_actuation_release_point,
                    current_actuation_point=0,
                    global_actuation_point=actuation_point)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_AKEY_0021", _AUTHOR)
    # end def test_two_actuation_points

    @features("Feature1B08")
    @level("Business")
    @services('DualKeyMatrix')
    def test_non_keyboard_assignment(self):
        """
        Validate each assignment of Multi-Action can only be assigned to keyboard keys.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create onboard profiles")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestUtils.ProfileHelper.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over onboard profiles")
        # --------------------------------------------------------------------------------------------------------------
        for profile in profiles:
            random_selected_keys = AnalogKeysTestUtils.AnalogKeysHelper.select_standard_keys_randomly(
                self, num_of_keys=10)
            actuation_point = choice(range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT,
                                           AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT))
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Edit the Actuation Point of {profile} with random {actuation_point}")
            # ----------------------------------------------------------------------------------------------------------
            profile.update_tag_content(
                directory=directory,
                tag_content_dict={ProfileManagement.Tag.ANALOG_GENERIC_SETTING: actuation_point << 8})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Create a Multi-Action configuration table and set assignment with non-keyboard"
                                     "opcode (0x80) and params (0x02)")
            # ----------------------------------------------------------------------------------------------------------
            groups = [ActionGroup(trigger_key=random_selected_key, random_assignments=True)
                      for random_selected_key in random_selected_keys]
            multi_action_table = AnalogKeysTestUtils.AnalogKeysHelper.create_multi_action_table(test_case=self,
                                                                                                preset_groups=groups,
                                                                                                directory=directory)
            valid_assignments = {ActionAssignment.Opcode.NO_ACTION, ActionAssignment.Opcode.REMAP_TO_STANDARD_KEY}
            invalid_assignments = set(range(0x0000, 0xFFFF))
            invalid_assignments.difference_update(valid_assignments)
            invalid_assignments = list(invalid_assignments)
            for group in multi_action_table.groups:
                for assignment in group.rows:
                    assignment.opcode = choice(invalid_assignments)
                # end for
            # end for
            multi_action_table.crc_32 = directory.update_file(file_id_lsb=multi_action_table.table_id,
                                                              table_in_hexlist=HexList(multi_action_table))
            ProfileManagementTestUtils.write(test_case=self, data=HexList(multi_action_table),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=multi_action_table.first_sector_id_lsb,
                                             crc_32=multi_action_table.crc_32)
            profile.update_tag_content(
                directory=directory,
                tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B08_MULTI_ACTION:
                                  multi_action_table.table_id})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Write 0x8101 profile to NVS\n{profile}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=profile.first_sector_id_lsb,
                                             crc_32=profile.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Update the directory and save in the NVS\n{directory}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(directory),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=directory.first_sector_id_lsb,
                                             crc_32=directory.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Active the {profile} with the Multi-Action configuration table")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                                file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                                file_id=profile.file_id_lsb,
                                                count=len(HexList(profile)),
                                                crc_32=profile.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Enable Multi-Action")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.enable_disable_multi_action_fkc(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Test Loop over selected keys: {random_selected_keys!r}")
            # ----------------------------------------------------------------------------------------------------------
            for random_selected_key in random_selected_keys:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Perform a key press on {random_selected_key!r} with key_travel = {actuation_point}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(key_id=random_selected_key, displacement=actuation_point)

                # FIXME: Change the expected result once we have an official specification to explain the expected
                #  behavior when the opcode is invalid.
                #  cf: https://jira.logitech.io/projects/GALVATRON/issues/GALVATRON-142
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check there is no HID MAKE report of {random_selected_key!r} received from the device")
                # ------------------------------------------------------------------------------------------------------
                ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Fully release {random_selected_key!r}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_release(key_id=random_selected_key)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check there is no HID BREAK report of {random_selected_key!r} received from the device")
                # ------------------------------------------------------------------------------------------------------
                ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_AKEY_0022", _AUTHOR)
    # end def test_non_keyboard_assignment

    @features("Feature1B08")
    @level("Business")
    @services('DualKeyMatrix')
    def test_all_event_assignment(self):
        """
        Validate events of the assignment can be MAKE, BREAK, MAKE/BREAK and IDLE
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create onboard profiles")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestUtils.ProfileHelper.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over onboard profiles")
        # --------------------------------------------------------------------------------------------------------------
        for profile in profiles:
            random_selected_keys = AnalogKeysTestUtils.AnalogKeysHelper.select_standard_keys_randomly(
                self, num_of_keys=10)
            actuation_point = choice(range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT,
                                           AnalogKeysTestUtils.AnalogKeysHelper.MA_MAX_FIRST_ACTUATION_POINT))
            second_actuation_point = choice(range(actuation_point +
                                                  AnalogKeysTestUtils.AnalogKeysHelper.MA_RELEASE_POINT_DELTA,
                                                  AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Edit the Actuation Point of {profile} with random {actuation_point}")
            # ----------------------------------------------------------------------------------------------------------
            profile.update_tag_content(
                directory=directory,
                tag_content_dict={ProfileManagement.Tag.ANALOG_GENERIC_SETTING: actuation_point << 8})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Create a Multi-Action configuration table and set {random_selected_keys} with "
                                     "different event assignments [MAKE, BREAK, MAKE/BREAK, IDLE]")
            # ----------------------------------------------------------------------------------------------------------
            groups = [ActionGroup(trigger_key=random_selected_key, second_actuation_point=second_actuation_point,
                                  random_assignments=True) for random_selected_key in random_selected_keys]
            multi_action_table = AnalogKeysTestUtils.AnalogKeysHelper.create_multi_action_table(
                test_case=self, directory=directory, preset_groups=groups)
            ProfileManagementTestUtils.write(test_case=self, data=HexList(multi_action_table),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=multi_action_table.first_sector_id_lsb,
                                             crc_32=multi_action_table.crc_32)
            profile.update_tag_content(
                directory=directory,
                tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B08_MULTI_ACTION:
                                  multi_action_table.table_id})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Write 0x8101 profile to NVS\n{profile}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=profile.first_sector_id_lsb,
                                             crc_32=profile.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Update the directory and save in the NVS\n{directory}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(directory),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=directory.first_sector_id_lsb,
                                             crc_32=directory.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Active the {profile} with the Multi-Action configuration table")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                                file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                                file_id=profile.file_id_lsb,
                                                count=len(HexList(profile)),
                                                crc_32=profile.crc_32)
            FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(test_case=self, set_fkc_enabled=1,
                                                                      fkc_enabled=1, set_toggle_keys_enabled=0)
            sleep(_WAIT_REPORT_TIME_MS)
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Test Loop over selected keys: {random_selected_keys!r}")
            # ----------------------------------------------------------------------------------------------------------
            for index, random_selected_key in enumerate(random_selected_keys):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Perform a key press on {random_selected_key!r} with key_travel = {actuation_point}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(key_id=random_selected_key, displacement=actuation_point)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check HID report(s) match the {groups[index].rows[0].event_0}")
                # -------------------------------------------------------- ---------------------------------------------
                AnalogKeysTestUtils.MultiActionChecker.check_multi_actions(
                    test_case=self, trigger_key=random_selected_key, multi_action_table=multi_action_table,
                    last_actuation_point=0, current_actuation_point=actuation_point,
                    global_actuation_point=actuation_point)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Perform a key press on {random_selected_key!r} with key_travel = {second_actuation_point}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(key_id=random_selected_key,
                                                              displacement=second_actuation_point)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check HID report(s) match the {groups[index].rows[0].event_1}")
                # ------------------------------------------------------------------------------------------------------
                AnalogKeysTestUtils.MultiActionChecker.check_multi_actions(
                    test_case=self, trigger_key=random_selected_key, multi_action_table=multi_action_table,
                    last_actuation_point=actuation_point, current_actuation_point=second_actuation_point,
                    global_actuation_point=actuation_point)

                mid_displacement = (
                    min(int((second_actuation_point - actuation_point) / 2) + actuation_point,
                        second_actuation_point - AnalogKeysTestUtils.AnalogKeysHelper.MA_RELEASE_POINT_DELTA))
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Release {random_selected_key!r} with key_travel = {mid_displacement}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(key_id=random_selected_key, displacement=mid_displacement)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check HID report(s) match the {groups[index].rows[0].event_2}")
                # ------------------------------------------------------------------------------------------------------
                AnalogKeysTestUtils.MultiActionChecker.check_multi_actions(
                    test_case=self, trigger_key=random_selected_key, multi_action_table=multi_action_table,
                    last_actuation_point=second_actuation_point,
                    current_actuation_point=mid_displacement,
                    global_actuation_point=actuation_point)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Release the {random_selected_key!r} with key_travel = "
                          f"{max(actuation_point - AnalogKeysTestUtils.AnalogKeysHelper.MA_RELEASE_POINT_DELTA, 0)}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(
                    key_id=random_selected_key,
                    displacement=max(actuation_point - AnalogKeysTestUtils.AnalogKeysHelper.MA_RELEASE_POINT_DELTA, 0))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check HID report(s) match the {groups[index].rows[0].event_3}")
                # ------------------------------------------------------------------------------------------------------
                AnalogKeysTestUtils.MultiActionChecker.check_multi_actions(
                    test_case=self, trigger_key=random_selected_key, multi_action_table=multi_action_table,
                    last_actuation_point=mid_displacement,
                    current_actuation_point=max(actuation_point -
                                                AnalogKeysTestUtils.AnalogKeysHelper.MA_RELEASE_POINT_DELTA, 0),
                    global_actuation_point=actuation_point)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Fully release {random_selected_key!r}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_release(key_id=random_selected_key)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check there is no HID report received from the device")
                # ------------------------------------------------------------------------------------------------------
                ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_AKEY_0023", _AUTHOR)
    # end def test_all_event_assignment

    @features("Feature1B08")
    @level("Business")
    @services('DualKeyMatrix')
    def test_all_keys_in_analog_adjustment_mode(self):
        """
        Validate users can only exit analog adjustment mode when the corresponding trigger keys are pressed.
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enter Global Actuation mode (FN + F6)")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.enter_exit_actuation_point_adjustment_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all available keys")
        # --------------------------------------------------------------------------------------------------------------
        for key in self.button_stimuli_emulator.get_key_id_list():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Perform a keystroke on {key!r} (Skip ESC)")
            # ----------------------------------------------------------------------------------------------------------
            if key == KEY_ID.KEYBOARD_ESCAPE:
                continue
            else:
                self.button_stimuli_emulator.keystroke(key_id=key)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check there is no HID report can be received from the device")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Perform a keystroke combination on FN + {key!r} (Skip F6)")
            # ----------------------------------------------------------------------------------------------------------
            if key == KEY_ID.KEYBOARD_F6:
                continue
            else:
                self.button_stimuli_emulator.key_press(key_id=KEY_ID.FN_KEY)
                sleep(_50_MS_DELAY)
                self.button_stimuli_emulator.keystroke(key_id=key)
                self.button_stimuli_emulator.key_release(key_id=KEY_ID.FN_KEY)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check there is no HID report can be received from the device")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Exit Global Actuation mode (FN + F6)")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.enter_exit_actuation_point_adjustment_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enter Global Rapid Trigger mode (FN + F7)")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.enter_exit_sensitivity_adjustment_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all available keys")
        # --------------------------------------------------------------------------------------------------------------
        for key in self.button_stimuli_emulator.get_key_id_list():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Perform a keystroke on {key} (Skip ESC)")
            # ----------------------------------------------------------------------------------------------------------
            if key == KEY_ID.KEYBOARD_ESCAPE:
                continue
            else:
                self.button_stimuli_emulator.keystroke(key_id=key)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check there is no HID report can be received from the device")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Perform a keystroke combination on FN + {key!r} (Skip F7)")
            # ----------------------------------------------------------------------------------------------------------
            if key == KEY_ID.KEYBOARD_F7:
                continue
            else:
                self.button_stimuli_emulator.key_press(key_id=KEY_ID.FN_KEY)
                sleep(_50_MS_DELAY)
                self.button_stimuli_emulator.keystroke(key_id=key)
                self.button_stimuli_emulator.key_release(key_id=KEY_ID.FN_KEY)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check there is no HID report can be received from the device")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_AKEY_0024", _AUTHOR)
    # end def test_all_keys_in_analog_adjustment_mode

    @features("Feature1B08")
    @level("Business")
    @services('DualKeyMatrix')
    def test_configure_onboard_profile_per_key_actuation_point_and_sensitivity_via_software(self):
        """
        Validate the users are able to adjust the per key actuation points and sensitivity then apply them to onboard
        profiles via software.
        """
        self._test_configure_profile_per_key_actuation_point_and_sensitivity_via_software(
            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE)

        self.testCaseChecked("BUS_AKEY_0025", _AUTHOR)
    # end def test_configure_onboard_profile_per_key_actuation_point_and_sensitivity_via_software

    @features("Feature1B08")
    @level("Business")
    @services('DualKeyMatrix')
    def test_configure_host_profile_per_key_actuation_point_and_sensitivity_via_software(self):
        """
        Validate the users are able to adjust the per key actuation points and sensitivity then apply them to host
        profiles via software.
        """
        self._test_configure_profile_per_key_actuation_point_and_sensitivity_via_software(
            file_type_id=ProfileManagement.FileTypeId.X8101.HOST_MODE_PROFILE)

        self.testCaseChecked("BUS_AKEY_0026", _AUTHOR)
    # end def test_configure_host_profile_per_key_actuation_point_and_sensitivity_via_software

    @features("Feature1B08")
    @level("Business")
    @services('DualKeyMatrix')
    def test_normal_trigger_make_break_points(self):
        """
        Validate normal trigger's Make and Break points in the base profile mode.
        """
        actuation_scaling_range_list = [int(element) for element in self.config.F_ActuationScalingRange]
        actuation_point = actuation_scaling_range_list[4]
        random_selected_keys = AnalogKeysTestUtils.AnalogKeysHelper.select_standard_keys_randomly(self, num_of_keys=10)
        # Release Point's definition: (AP - 3 = AP in mm - 0.3mm)
        # https://docs.google.com/document/d/1yuMIIuF8-0v5ZQzZvzKoLQ1Y3GdEchM0E3pnrNDgUfo/view#heading=h.3fd0y3miwpct
        release_point = actuation_point - 3
        non_release_point = release_point + 1
        across_release_point = release_point - 1
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Base Profile")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.switch_to_base_profile(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enter Actuation Point mode (FN + F6)")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.enter_exit_actuation_point_adjustment_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Adjust actuation point by performing a keystroke on {KEY_ID.KEYBOARD_5!r}")
        # --------------------------------------------------------------------------------------------------------------
        # Set the first actuation point to middle value
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Exit Actuation Point mode (FN + F6)")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.enter_exit_actuation_point_adjustment_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Test Loop over displacement in {[non_release_point, release_point, across_release_point]}")
        # --------------------------------------------------------------------------------------------------------------
        for release_point_displacement in [non_release_point, release_point, across_release_point]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Test Loop over key in {random_selected_keys}")
            # ----------------------------------------------------------------------------------------------------------
            for random_selected_key in random_selected_keys:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "Test Loop over in range(10) to validate continuous trigger")
                # ------------------------------------------------------------------------------------------------------
                for index in range(10):
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(
                        self, f"Perform a {random_selected_key!r} press with key_travel = {actuation_point}")
                    # --------------------------------------------------------------------------------------------------
                    self.button_stimuli_emulator.key_displacement(key_id=random_selected_key,
                                                                  displacement=actuation_point)

                    if release_point_displacement == non_release_point and index > 0:
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_check(
                            self, f"Check there is no HID Make report of {random_selected_key!r} "
                                  "received from the device")
                        # ----------------------------------------------------------------------------------------------
                        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
                    else:
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_check(
                            self, f"Check HID Make report of {random_selected_key!r} is received from the device")
                        # ----------------------------------------------------------------------------------------------
                        KeyMatrixTestUtils.check_hid_report_by_key_id(
                            test_case=self, key=KeyMatrixTestUtils.Key(random_selected_key, MAKE))
                    # end if

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(
                        self, f"Release the {random_selected_key!r} with key_travel = {release_point_displacement}")
                    # --------------------------------------------------------------------------------------------------
                    self.button_stimuli_emulator.key_displacement(key_id=random_selected_key,
                                                                  displacement=release_point_displacement)

                    if release_point_displacement == non_release_point:
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_check(
                            self, f"Check there is no HID Break report of {random_selected_key!r} "
                                  "received from the device")
                        # ----------------------------------------------------------------------------------------------
                        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
                    else:
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_check(
                            self, f"Check HID Break report of {random_selected_key!r} is received from the device")
                        # ----------------------------------------------------------------------------------------------
                        KeyMatrixTestUtils.check_hid_report_by_key_id(
                            test_case=self, key=KeyMatrixTestUtils.Key(random_selected_key, BREAK))
                    # end if
                # end for
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "End Test Loop")
                # ------------------------------------------------------------------------------------------------------
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Fully release {random_selected_key!r}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_release(key_id=random_selected_key)
                if release_point_displacement == non_release_point:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(
                        self, f"Check HID Break report of {random_selected_key!r} is received from the device")
                    # --------------------------------------------------------------------------------------------------
                    KeyMatrixTestUtils.check_hid_report_by_key_id(
                        test_case=self, key=KeyMatrixTestUtils.Key(random_selected_key, BREAK))
                else:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(
                        self, f"Check there is no HID Break report of {random_selected_key!r} "
                              "received from the device")
                    # --------------------------------------------------------------------------------------------------
                    ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
                # end if
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_AKEY_0027", _AUTHOR)
    # end def test_normal_trigger_make_break_points

    @features("Feature1B08")
    @level("Business")
    @services('DualKeyMatrix')
    def test_rapid_trigger_with_displacement_vibrations(self):
        """
        Validate rapid trigger Make, Break points are not reset by some displacement vibrations.
        """
        actuation_point = self.config.F_DefaultActuationPoint
        sensitivity = self.config.F_DefaultSensitivity
        random_selected_key = choice(list(self.button_stimuli_emulator.keyboard_layout.KEYID_2_CHAINID.keys()))
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Base Profile")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.switch_to_base_profile(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enter Rapid Trigger mode (FN + F7)")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.enter_exit_sensitivity_adjustment_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable Rapid Trigger via F7")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_F7)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Exit Rapid Trigger mode and save settings (FN + F7)")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.enter_exit_sensitivity_adjustment_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Perform a random {random_selected_key!r} press with key_travel = {actuation_point}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_displacement(key_id=random_selected_key, displacement=actuation_point)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Check HID Make report of {random_selected_key!r} is received from the device")
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                      key=KeyMatrixTestUtils.Key(random_selected_key, MAKE))

        key_travels = [actuation_point - sensitivity + 1] + \
                      [choice(range(actuation_point - sensitivity + 1, actuation_point)) for _ in range(10)]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over key_travel in {key_travels}")
        # --------------------------------------------------------------------------------------------------------------
        for key_travel in key_travels:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release the {random_selected_key!r} with key_travel = {key_travel}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=random_selected_key,
                                                          displacement=key_travel)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, f"Check there is no HID Break report of {random_selected_key!r} received from the device")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, f"Release the {random_selected_key!r} with key_travel = {actuation_point - sensitivity}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_displacement(key_id=random_selected_key,
                                                      displacement=actuation_point - sensitivity)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Check HID Break report of {random_selected_key!r} is received from the device")
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(
            test_case=self, key=KeyMatrixTestUtils.Key(random_selected_key, BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, f"Release the {random_selected_key!r} with key_travel = "
                  f"{AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_displacement(
            key_id=random_selected_key, displacement=AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Check there is no HID Break report of {random_selected_key!r} received from the device")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        key_travels = [AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT + sensitivity - 1] + \
                      [choice(range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT + 1,
                                    AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT + sensitivity))
                       for _ in range(10)]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over key_travel in {key_travels}")
        # --------------------------------------------------------------------------------------------------------------
        for key_travel in key_travels:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press the {random_selected_key!r} with key_travel = {key_travel}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=random_selected_key,
                                                          displacement=key_travel)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, f"Check there is no HID Make report of {random_selected_key!r} received from the device")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, f"Release the {random_selected_key!r} with "
                  f"key_travel = {AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT + sensitivity}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_displacement(
            key_id=random_selected_key,
            displacement=AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT + sensitivity)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Check HID Make report of {random_selected_key!r} is received from the device")
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(
            test_case=self, key=KeyMatrixTestUtils.Key(random_selected_key, MAKE))

        self.testCaseChecked("BUS_AKEY_0028", _AUTHOR)
    # end def test_rapid_trigger_with_displacement_vibrations

    @features("Feature1B08")
    @level("Business")
    @services('DualKeyMatrix')
    def test_reset_rapid_trigger_until_key_fully_released(self):
        """
        Validate the actuation point of rapid trigger is reset after fully releasing the trigger key.
        """
        random_selected_keys = AnalogKeysTestUtils.AnalogKeysHelper.select_standard_keys_randomly(self, num_of_keys=10)
        actuation_point = self.config.F_DefaultActuationPoint
        sensitivity = self.config.F_DefaultSensitivity
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Base Profile (FN + F5)")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.switch_to_base_profile(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enter Rapid Trigger mode (FN + F7)")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.enter_exit_sensitivity_adjustment_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable Rapid Trigger via F7")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_F7)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Exit Rapid Trigger mode and save settings (FN + F7)")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.enter_exit_sensitivity_adjustment_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over selected keys: {random_selected_keys!r}")
        # --------------------------------------------------------------------------------------------------------------
        for random_selected_key in random_selected_keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Perform a key press on {random_selected_key!r} with key_travel = {actuation_point}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=random_selected_key, displacement=actuation_point)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID MAKE report is received from the device")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(random_selected_key, MAKE))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Release {random_selected_key!r} with "
                      f"key_travel = {AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(
                key_id=random_selected_key, displacement=AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID BREAK report is received from the device")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(random_selected_key, BREAK))

            validation_range = range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT,
                                     AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT - sensitivity)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Test Loop over key_travel in {validation_range}")
            # ----------------------------------------------------------------------------------------------------------
            for key_travel in validation_range:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Perform a random {random_selected_key!r} press with key_travel = "
                          f"{key_travel + sensitivity}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(key_id=random_selected_key,
                                                              displacement=key_travel + sensitivity)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check HID Make report of {random_selected_key!r} is received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(random_selected_key, MAKE))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Release the {random_selected_key!r} with key_travel = {key_travel}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(key_id=random_selected_key,
                                                              displacement=key_travel)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check HID Break report of {random_selected_key!r} is received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(random_selected_key,
                                                                                         BREAK))
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Fully release {random_selected_key!r}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key_id=random_selected_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, f"Check there is no HID Break report of {random_selected_key!r} received from the device")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                self, f"Test Loop over inner_key_travel in "
                      f"{range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT, actuation_point)}")
            # ----------------------------------------------------------------------------------------------------------
            for inner_key_travel in range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT, actuation_point):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Perform a random {random_selected_key!r} press with key_travel = {inner_key_travel}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(key_id=random_selected_key,
                                                              displacement=inner_key_travel)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check there is no HID Make report of {random_selected_key!r} received from the device")
                # ------------------------------------------------------------------------------------------------------
                ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Fully release {random_selected_key!r}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_release(key_id=random_selected_key)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check there is no HID Break report of {random_selected_key!r} received from the device")
                # --------------------------------------------------------------------------------------------`----------
                ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_AKEY_0029", _AUTHOR)
    # end def test_reset_rapid_trigger_until_key_fully_released

    @features("Feature1B08")
    @level("Business")
    @services('DualKeyMatrix')
    def test_multi_press_on_keys_with_different_actuation_point(self):
        """
        Validate multiple key presses on keys which have different actuation points
        """
        number_of_keys_to_be_press_same_time = 3
        all_analog_keys = set(self.button_stimuli_emulator.keyboard_layout.KEYID_2_CHAINID.keys())
        valid_modifier_keys = list(set(KEY_ID_TO_MODIFIER_BITFIELD.keys()).intersection(all_analog_keys))
        random_picked_modifier_keys = [valid_modifier_keys.pop(choice(range(len(valid_modifier_keys))))
                                       for _ in range(number_of_keys_to_be_press_same_time)]
        directory, profiles = \
            self.create_directory_and_profiles(file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over profiles: {profiles}")
        # --------------------------------------------------------------------------------------------------------------
        for profile in profiles:
            random_selected_keys = AnalogKeysTestUtils.AnalogKeysHelper.select_standard_keys_randomly(
                self, num_of_keys=10, excluded_keys=valid_modifier_keys + random_picked_modifier_keys)
            actuation_point = choice(range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT,
                                           AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT))
            per_key_actuation_points = [choice(
                range(actuation_point + 1, AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT + 1))
                for _ in range(number_of_keys_to_be_press_same_time + len(random_picked_modifier_keys))]
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Edit the Global Actuation Point of {profile} with a random"
                                     f"AP = {actuation_point}")
            # ----------------------------------------------------------------------------------------------------------
            profile.update_tag_content(
                directory=directory,
                tag_content_dict={ProfileManagement.Tag.ANALOG_GENERIC_SETTING: actuation_point << 8})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self,
                "Create an Actuation Point Table and set "
                f"{random_selected_keys[:number_of_keys_to_be_press_same_time] + random_picked_modifier_keys!r} "
                f"with per_key_actuation_points = {per_key_actuation_points}")
            # ----------------------------------------------------------------------------------------------------------
            actuation_point_per_key_dict = {
                    random_selected_key: per_key_actuation_points[index] for index, random_selected_key in
                    enumerate(random_selected_keys[:number_of_keys_to_be_press_same_time] +
                              random_picked_modifier_keys)}
            actuation_point_per_key = AnalogKeysTestUtils.AnalogKeysHelper.create_actuation_point_configuration_per_key(
                test_case=self,
                keys_and_actuation_points=actuation_point_per_key_dict)
            actuation_point_table = AnalogKeysTestUtils.AnalogKeysHelper.create_actuation_point_table(
                test_case=self, directory=directory, actuation_point_per_keys=actuation_point_per_key)
            ProfileManagementTestUtils.write(test_case=self, data=HexList(actuation_point_table),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=actuation_point_table.first_sector_id_lsb,
                                             crc_32=actuation_point_table.crc_32)
            profile.update_tag_content(
                directory=directory,
                tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B08_ACTUATION:
                                  actuation_point_table.table_id})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Write 0x8101 profile to NVS\n{profile}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=profile.first_sector_id_lsb,
                                             crc_32=profile.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Update the directory and save in the NVS\n{directory}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(directory),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=directory.first_sector_id_lsb,
                                             crc_32=directory.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Active the {profile} with the Actuation Point Table")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                                file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                                file_id=profile.file_id_lsb,
                                                count=len(HexList(profile)),
                                                crc_32=profile.crc_32)
            sleep(_WAIT_REPORT_TIME_MS)
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

            for keys in (random_selected_keys[:number_of_keys_to_be_press_same_time], random_picked_modifier_keys,
                         random_picked_modifier_keys + [choice(random_selected_keys)],
                         random_selected_keys + random_picked_modifier_keys):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"Test Loop over analog keys: {keys!r}")
                # ------------------------------------------------------------------------------------------------------
                for key in keys:
                    _actuation_point = actuation_point \
                        if key not in actuation_point_per_key_dict.keys() else actuation_point_per_key_dict[key]
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f"Perform key press on {key!r} with key_travel = {_actuation_point}")
                    # --------------------------------------------------------------------------------------------------
                    self.button_stimuli_emulator.key_displacement(key_id=key, displacement=_actuation_point)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(
                        self, f"Check HID Make reports of {key!r} are received from the device")
                    # --------------------------------------------------------------------------------------------------
                    KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                                  key=KeyMatrixTestUtils.Key(key, MAKE))
                # end for
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"End Test Loop")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"Test Loop over analog keys: {keys!r}")
                # ------------------------------------------------------------------------------------------------------
                for key in keys:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f"Release {key}")
                    # --------------------------------------------------------------------------------------------------
                    self.button_stimuli_emulator.key_release(key_id=key)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(
                        self, f"Check HID Break reports of {key!r} are received from the device")
                    # --------------------------------------------------------------------------------------------------
                    KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                                  key=KeyMatrixTestUtils.Key(key, BREAK))
                # end for
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"End Test Loop")
                # ------------------------------------------------------------------------------------------------------
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_AKEY_0030", _AUTHOR)
    # end def test_multi_press_on_keys_with_different_actuation_point

    def _test_use_case_with_all_device_states(self, user_scenario):
        """
        Validate the user case under different battery levels, power modes, charging status.

        :param user_scenario: The user scenario to be tested
        :type user_scenario: ``function``
        """
        power_mode_helper = PowerModesTestUtils.PowerModeHelper
        charging_mode_helper = DeviceTestUtils.ChargingHelper
        all_battery_levels = ['full', 'good', 'low', 'critical']
        all_power_modes = [power_mode_helper.RUN, power_mode_helper.WALK,
                           power_mode_helper.SLEEP, power_mode_helper.DEEP_SLEEP]
        all_charging_status = [charging_mode_helper.WIRED_CHARGING, charging_mode_helper.WIRELESS_CHARGING,
                               charging_mode_helper.WIRELESS_POWERED]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over device_states in "
                                 f"{[all_battery_levels, all_power_modes, all_charging_status]}")
        # --------------------------------------------------------------------------------------------------------------
        for index, device_states in enumerate([all_battery_levels, all_power_modes, all_charging_status]):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Test Loop over device_status in {device_states}")
            # ----------------------------------------------------------------------------------------------------------
            for inner_index, device_status in enumerate(device_states):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Make the device enter {device_status}")
                # ------------------------------------------------------------------------------------------------------
                if index == 0 and self.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_Enabled:
                    state_of_charge = int(self.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_SupportedLevels[inner_index])
                    battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, state_of_charge)
                    self.reset(hardware_reset=True, starting_voltage=battery_value)
                elif index == 1 and power_mode_helper.enter_specified_power_mode(
                        test_case=self, power_mode=device_status):
                    pass
                elif index == 2 and charging_mode_helper.enter_specified_charging_power_status(
                        test_case=self, charging_status=device_status):
                    pass
                else:
                    continue
                # end if

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"Execute the user scenario: {user_scenario.__name__}")
                # ------------------------------------------------------------------------------------------------------
                user_scenario()

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Make the device exit {device_status}")
                # ------------------------------------------------------------------------------------------------------
                if index == 2:
                    DeviceTestUtils.ChargingHelper.exit_charging_mode(test_case=self, source=self.external_power_source)
                # end if
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
    # end def _test_use_case_with_all_device_states

    def _test_configure_profile_actuation_point_via_software(self, file_type_id):
        """
        Validate the users are able to adjust the global actuation point and apply it to profiles via software.

        :param file_type_id: File Type ID
        :type file_type_id: ``int | ProfileManagement.FileTypeId.X8101``
        """
        directory, profiles = self.create_directory_and_profiles(file_type_id=file_type_id)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over profiles: {profiles}")
        # --------------------------------------------------------------------------------------------------------------
        for profile in profiles:
            random_selected_key = choice(list(self.button_stimuli_emulator.keyboard_layout.KEYID_2_CHAINID.keys()))
            for actuation_point in range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT,
                                         AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT + 1):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Edit the Global Actuation Point of profile with AP = {actuation_point}")
                # ------------------------------------------------------------------------------------------------------
                profile.update_tag_content(
                    directory=directory,
                    tag_content_dict={ProfileManagement.Tag.ANALOG_GENERIC_SETTING: actuation_point << 8})

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Write 0x8101 profile to NVS\n{profile}")
                # ------------------------------------------------------------------------------------------------------
                ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                                 store_in_nvs=True,
                                                 first_sector_id_lsb=profile.first_sector_id_lsb,
                                                 crc_32=profile.crc_32)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Update the directory and save in the NVS\n{directory}")
                # ------------------------------------------------------------------------------------------------------
                ProfileManagementTestUtils.write(test_case=self, data=HexList(directory),
                                                 store_in_nvs=True,
                                                 first_sector_id_lsb=directory.first_sector_id_lsb,
                                                 crc_32=directory.crc_32)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Active the {profile}")
                # ------------------------------------------------------------------------------------------------------
                ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                                    file_type_id=file_type_id,
                                                    file_id=profile.file_id_lsb,
                                                    count=len(HexList(profile)),
                                                    crc_32=profile.crc_32)
                sleep(_WAIT_REPORT_TIME_MS)
                ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"Test Loop over key travel offset in: {[-1, 0, +1]}")
                # ------------------------------------------------------------------------------------------------------
                for offset in [-1, 0, +1]:
                    displacement = max(0, min(actuation_point + offset,
                                              AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT))
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(
                        self, f"Perform a random {random_selected_key!r} press with key_travel = {displacement}")
                    # --------------------------------------------------------------------------------------------------
                    self.button_stimuli_emulator.key_displacement(key_id=random_selected_key, displacement=displacement)

                    if offset < 0:
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_check(
                            self,
                            f"Check there is no HID Make report of {random_selected_key!r} received from the device")
                        # ----------------------------------------------------------------------------------------------
                        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
                    else:
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_check(
                            self, f"Check HID Make report of {random_selected_key!r} is received from the device")
                        # ----------------------------------------------------------------------------------------------
                        KeyMatrixTestUtils.check_hid_report_by_key_id(
                            test_case=self,
                            key=KeyMatrixTestUtils.Key(random_selected_key, MAKE))
                    # end if

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f"Release the {random_selected_key!r}")
                    # --------------------------------------------------------------------------------------------------
                    self.button_stimuli_emulator.key_release(key_id=random_selected_key)

                    if offset < 0:
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_check(
                            self,
                            f"Check there is no HID Break report of {random_selected_key!r} received from the device")
                        # ----------------------------------------------------------------------------------------------
                        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
                    else:
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_check(
                            self, f"Check HID Break report of {random_selected_key!r} is received from the device")
                        # ----------------------------------------------------------------------------------------------
                        KeyMatrixTestUtils.check_hid_report_by_key_id(
                            test_case=self,
                            key=KeyMatrixTestUtils.Key(random_selected_key, BREAK))
                    # end if
                # end for
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "End Test Loop")
                # ------------------------------------------------------------------------------------------------------
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
    # end def _test_configure_profile_actuation_point_via_software

    def _test_configure_profile_per_key_actuation_point_via_software(self, file_type_id):
        """
        Validate the users are able to adjust the per key actuation points and apply them to profiles via software.

        :param file_type_id: File Type Id
        :type file_type_id: ``int | ProfileManagement.FileTypeId.X8101``
        """
        directory, profiles = self.create_directory_and_profiles(file_type_id=file_type_id)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over profiles: {profiles}")
        # --------------------------------------------------------------------------------------------------------------
        for profile in profiles:
            random_selected_keys = AnalogKeysTestUtils.AnalogKeysHelper.select_standard_keys_randomly(
                self, num_of_keys=10)
            actuation_point = choice(range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT,
                                           AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT))
            per_key_actuation_point = choice(
                range(actuation_point + 1, AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT + 1))
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Edit the Global Actuation Point of {profile} with a random"
                                     f"AP = {actuation_point}")
            # ----------------------------------------------------------------------------------------------------------
            profile.update_tag_content(
                directory=directory,
                tag_content_dict={ProfileManagement.Tag.ANALOG_GENERIC_SETTING: actuation_point << 8})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Create an Actuation Point Table and set {random_selected_keys!r} "
                                     f"with per_key_actuation_point = {per_key_actuation_point}")
            # ----------------------------------------------------------------------------------------------------------
            actuation_point_per_key = AnalogKeysTestUtils.AnalogKeysHelper.create_actuation_point_configuration_per_key(
                test_case=self,
                keys_and_actuation_points={
                    random_selected_key: per_key_actuation_point for random_selected_key in random_selected_keys})
            actuation_point_table = AnalogKeysTestUtils.AnalogKeysHelper.create_actuation_point_table(
                test_case=self, directory=directory, actuation_point_per_keys=actuation_point_per_key)
            ProfileManagementTestUtils.write(test_case=self, data=HexList(actuation_point_table),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=actuation_point_table.first_sector_id_lsb,
                                             crc_32=actuation_point_table.crc_32)
            profile.update_tag_content(
                directory=directory,
                tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B08_ACTUATION:
                                  actuation_point_table.table_id})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Write 0x8101 profile to NVS\n{profile}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=profile.first_sector_id_lsb,
                                             crc_32=profile.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Update the directory and save in the NVS\n{directory}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(directory),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=directory.first_sector_id_lsb,
                                             crc_32=directory.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Active the {profile} with the Actuation Point Table")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                                file_type_id=file_type_id,
                                                file_id=profile.file_id_lsb,
                                                count=len(HexList(profile)),
                                                crc_32=profile.crc_32)

            all_analog_keys = list(self.button_stimuli_emulator.keyboard_layout.KEYID_2_CHAINID.keys())
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Test Loop over analog keys: {all_analog_keys}")
            # ----------------------------------------------------------------------------------------------------------
            for key in all_analog_keys:
                sleep(_WAIT_REPORT_TIME_MS)
                ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Perform key press on {key!r} with key_travel = {actuation_point}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(key_id=key, displacement=actuation_point)

                if key in random_selected_keys:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(
                        self, f"Check there is no HID Make report of {key!r} received from the device")
                    # --------------------------------------------------------------------------------------------------
                    ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
                else:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(
                        self, f"Check HID Make reports of {key!r} are received from the device")
                    # --------------------------------------------------------------------------------------------------
                    KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                                  key=KeyMatrixTestUtils.Key(key, MAKE))
                # end if

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Release {key}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_release(key_id=key)

                if key in random_selected_keys:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(
                        self, f"Check there is no HID Break report of {key!r} received from the device")
                    # --------------------------------------------------------------------------------------------------
                    ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
                else:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(
                        self, f"Check HID Break reports of {key!r} are received from the device")
                    # --------------------------------------------------------------------------------------------------
                    KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                                  key=KeyMatrixTestUtils.Key(key, BREAK))
                # end if

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Perform key press on {key!r} with key_travel = "
                                         f"{per_key_actuation_point}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(key_id=key,
                                                              displacement=per_key_actuation_point)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check HID Make reports of {key!r} are received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key, MAKE))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Release {key!r}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_release(key_id=key)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check HID Break reports of {key!r} are received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key, BREAK))

                per_key_actuation_point = \
                    choice(range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT, actuation_point))
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Edit per_key_actuation_point of {random_selected_keys!r} to {per_key_actuation_point}")
                # ------------------------------------------------------------------------------------------------------
                for index in range(len(actuation_point_table.rows)):
                    actuation_point_table.rows[index].actuation_point = per_key_actuation_point
                # end for
                actuation_point_table.crc_32 = directory.update_file(
                    file_id_lsb=actuation_point_table.table_id, table_in_hexlist=HexList(actuation_point_table))
                ProfileManagementTestUtils.write(test_case=self, data=HexList(actuation_point_table),
                                                 store_in_nvs=True,
                                                 first_sector_id_lsb=actuation_point_table.first_sector_id_lsb,
                                                 crc_32=actuation_point_table.crc_32)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Update the directory and save in the NVS\n{directory}")
                # ------------------------------------------------------------------------------------------------------
                ProfileManagementTestUtils.write(test_case=self, data=HexList(directory),
                                                 store_in_nvs=True,
                                                 first_sector_id_lsb=directory.first_sector_id_lsb,
                                                 crc_32=directory.crc_32)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Active the {profile} with the Actuation Point Table")
                # ------------------------------------------------------------------------------------------------------
                ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                                    file_type_id=file_type_id,
                                                    file_id=profile.file_id_lsb,
                                                    count=len(HexList(profile)),
                                                    crc_32=profile.crc_32)
                sleep(_WAIT_REPORT_TIME_MS)
                ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Perform key press on {key!r} with key_travel = {actuation_point}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(key_id=key, displacement=actuation_point)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check HID Make reports of {key!r} are received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key, MAKE))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Release {key!r}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_release(key_id=key)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check HID Break reports of {key!r} are received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key, BREAK))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Perform key press on {key!r} with key_travel = {per_key_actuation_point}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(key_id=key,
                                                              displacement=per_key_actuation_point)

                if key in random_selected_keys:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(
                        self, f"Check HID Make reports of {key!r} are received from the device")
                    # --------------------------------------------------------------------------------------------------
                    KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                                  key=KeyMatrixTestUtils.Key(key, MAKE))
                else:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(
                        self, f"Check there is no HID Make report of {key!r} received from the device")
                    # --------------------------------------------------------------------------------------------------
                    ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
                # end if

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Release {key!r}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_release(key_id=key)

                if key in random_selected_keys:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(
                        self, f"Check HID Break reports of {key!r} are received from the device")
                    # --------------------------------------------------------------------------------------------------
                    KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                                  key=KeyMatrixTestUtils.Key(key, BREAK))
                else:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(
                        self, f"Check there is no HID Break report of {key!r} received from the device")
                    # --------------------------------------------------------------------------------------------------
                    ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
                # end if

                per_key_actuation_point = choice(
                    range(actuation_point + 1, AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT + 1))
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Edit per_key_actuation_point of {random_selected_keys!r} to {per_key_actuation_point}")
                # ------------------------------------------------------------------------------------------------------
                for index in range(len(actuation_point_table.rows)):
                    actuation_point_table.rows[index].actuation_point = per_key_actuation_point
                # end for
                actuation_point_table.crc_32 = directory.update_file(
                    file_id_lsb=actuation_point_table.table_id, table_in_hexlist=HexList(actuation_point_table))
                ProfileManagementTestUtils.write(test_case=self, data=HexList(actuation_point_table),
                                                 store_in_nvs=True,
                                                 first_sector_id_lsb=actuation_point_table.first_sector_id_lsb,
                                                 crc_32=actuation_point_table.crc_32)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Update the directory and save in the NVS\n{directory}")
                # ------------------------------------------------------------------------------------------------------
                ProfileManagementTestUtils.write(test_case=self, data=HexList(directory),
                                                 store_in_nvs=True,
                                                 first_sector_id_lsb=directory.first_sector_id_lsb,
                                                 crc_32=directory.crc_32)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Active the {profile} with the Actuation Point Table")
                # ------------------------------------------------------------------------------------------------------
                ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                                    file_type_id=file_type_id,
                                                    file_id=profile.file_id_lsb,
                                                    count=len(HexList(profile)),
                                                    crc_32=profile.crc_32)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
    # end def _test_configure_profile_per_key_actuation_point_via_software

    def _test_rapid_trigger_and_multi_action_settings_in_profile(self, file_type_id):
        """
        Validate the rapid trigger and multi-action are referring to same actuation point of the profile.

        :param file_type_id: File Type ID
        :type file_type_id: ``int | ProfileManagement.FileTypeId.X8101``
        """
        directory, profiles = self.create_directory_and_profiles(file_type_id=file_type_id)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over profiles: {profiles}")
        # --------------------------------------------------------------------------------------------------------------
        for profile in profiles:
            random_selected_keys_ma = AnalogKeysTestUtils.AnalogKeysHelper.select_standard_keys_randomly(
                self, num_of_keys=10)
            random_selected_keys_rt = AnalogKeysTestUtils.AnalogKeysHelper.select_standard_keys_randomly(
                self, num_of_keys=10, excluded_keys=random_selected_keys_ma)
            sensitivity = choice(range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_SENSITIVITY,
                                       AnalogKeysTestUtils.AnalogKeysHelper.MAX_SENSITIVITY))
            actuation_point = choice(range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT + sensitivity,
                                           AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT - sensitivity))
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Edit the Global Actuation Point of {profile} with a random"
                                     f"AP={actuation_point}")
            # ----------------------------------------------------------------------------------------------------------
            profile.update_tag_content(
                directory=directory,
                tag_content_dict={ProfileManagement.Tag.ANALOG_GENERIC_SETTING: actuation_point << 8})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Create a Rapid Trigger configuration table and set a random sensitivity: "
                                     f"{sensitivity} with random selected keys: {random_selected_keys_rt!r}")
            # ----------------------------------------------------------------------------------------------------------
            sensitivity_per_key = AnalogKeysTestUtils.AnalogKeysHelper.create_sensitivity_configuration_per_key(
                test_case=self,
                keys_and_sensitivities={random_selected_key: sensitivity
                                        for random_selected_key in random_selected_keys_rt})
            rapid_trigger_table = AnalogKeysTestUtils.AnalogKeysHelper.create_rapid_trigger_table(
                test_case=self, directory=directory, sensitivity_per_keys=sensitivity_per_key)
            ProfileManagementTestUtils.write(test_case=self, data=HexList(rapid_trigger_table),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=rapid_trigger_table.first_sector_id_lsb,
                                             crc_32=rapid_trigger_table.crc_32)
            profile.update_tag_content(
                directory=directory,
                tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B08_RAPID_TRIGGER:
                                  rapid_trigger_table.table_id})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Create a Multi-Action configuration table and set Opcode with 0x80 and Param"
                                     f"with 0x02 on {len(random_selected_keys_ma)} random selected keys")
            # ----------------------------------------------------------------------------------------------------------
            groups = [ActionGroup(trigger_key=random_selected_key, random_assignments=True)
                      for random_selected_key in random_selected_keys_ma]
            multi_action_table = AnalogKeysTestUtils.AnalogKeysHelper.create_multi_action_table(
                test_case=self, preset_groups=groups, directory=directory)
            ProfileManagementTestUtils.write(test_case=self, data=HexList(multi_action_table),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=multi_action_table.first_sector_id_lsb,
                                             crc_32=multi_action_table.crc_32)
            profile.update_tag_content(
                directory=directory,
                tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B08_MULTI_ACTION:
                                  multi_action_table.table_id})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Write 0x8101 profile to NVS\n{profile}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=profile.first_sector_id_lsb,
                                             crc_32=profile.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Update the directory and save in the NVS\n{directory}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(directory),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=directory.first_sector_id_lsb,
                                             crc_32=directory.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Active the {profile} with the Rapid Trigger and Multi-Action tables")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                                file_type_id=file_type_id,
                                                file_id=profile.file_id_lsb,
                                                count=len(HexList(profile)),
                                                crc_32=profile.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send setKeyTravelEventState request to enable key_travel_event_state")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.HIDppHelper.set_key_travel_event_state(
                test_case=self, key_travel_event_state=AnalogKeysTestUtils.Status.ENABLE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send setRapidTriggerState request to enable rapid_trigger_state")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.HIDppHelper.set_rapid_trigger_state(
                test_case=self, rapid_trigger_state=AnalogKeysTestUtils.Status.ENABLE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                self, f"Test Loop over key in: {zip(random_selected_keys_ma, random_selected_keys_rt)!r}")
            # ----------------------------------------------------------------------------------------------------------
            for random_selected_key_ma, random_selected_key_rt in zip(random_selected_keys_ma, random_selected_keys_rt):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Enable Multi-Action")
                # ------------------------------------------------------------------------------------------------------
                AnalogKeysTestUtils.enable_disable_multi_action_fkc(test_case=self)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Perform a key press on {random_selected_key_ma!r} with key_travel = {actuation_point}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(
                    key_id=random_selected_key_ma, displacement=actuation_point)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check the HID report of Multi-Action.event0 is received from the device")
                # ------------------------------------------------------------------------------------------------------
                AnalogKeysTestUtils.MultiActionChecker.check_multi_actions(test_case=self,
                                                                           trigger_key=random_selected_key_ma,
                                                                           multi_action_table=multi_action_table,
                                                                           last_actuation_point=0,
                                                                           current_actuation_point=actuation_point,
                                                                           global_actuation_point=actuation_point)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Fully release {random_selected_key_ma!r}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_release(key_id=random_selected_key_ma)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check the HID report of Multi-Action.event3 is received from the device")
                # ------------------------------------------------------------------------------------------------------
                AnalogKeysTestUtils.MultiActionChecker.check_multi_actions(test_case=self,
                                                                           trigger_key=random_selected_key_ma,
                                                                           multi_action_table=multi_action_table,
                                                                           last_actuation_point=actuation_point,
                                                                           current_actuation_point=0,
                                                                           global_actuation_point=actuation_point)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Disable Multi-Action")
                # ------------------------------------------------------------------------------------------------------
                AnalogKeysTestUtils.enable_disable_multi_action_fkc(test_case=self)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Perform a key press on {random_selected_key_rt!r} with key_travel = {actuation_point}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(key_id=random_selected_key_rt,
                                                              displacement=actuation_point)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check HID MAKE report of {random_selected_key_rt!r} is received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(random_selected_key_rt, MAKE))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Release {random_selected_key_rt!r} with key_travel = {actuation_point -sensitivity + 1}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(key_id=random_selected_key_rt,
                                                              displacement=actuation_point - sensitivity + 1)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check there is no HID report received from the device")
                # ------------------------------------------------------------------------------------------------------
                ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Fully release {random_selected_key_rt!r}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_release(key_id=random_selected_key_rt)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check HID BREAK report of {random_selected_key_rt!r} is received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(
                    test_case=self, key=KeyMatrixTestUtils.Key(random_selected_key_rt, BREAK))
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
    # end def _test_rapid_trigger_and_multi_action_settings_in_profile

    def _test_configure_profile_global_sensitivity_via_software(self, file_type_id):
        """
        Validate the users are able to adjust the global sensitivity and apply it to profiles via software.

        :param file_type_id: File Type Id
        :type file_type_id: ``int | ProfileManagement.FileTypeId.X8101``
        """
        actuation_point = self.config.F_DefaultActuationPoint
        directory, profiles = self.create_directory_and_profiles(file_type_id=file_type_id)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over profiles: {profiles}")
        # --------------------------------------------------------------------------------------------------------------
        for profile in profiles:
            all_analog_keys = list(self.button_stimuli_emulator.keyboard_layout.KEYID_2_CHAINID.keys())
            sensitivity = choice(range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_SENSITIVITY,
                                       AnalogKeysTestUtils.AnalogKeysHelper.MAX_SENSITIVITY))
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Create a Rapid Trigger configuration table and set sensitivity: {sensitivity} "
                                     f"to all analog keys {all_analog_keys!r}")
            # ----------------------------------------------------------------------------------------------------------
            sensitivity_per_key = AnalogKeysTestUtils.AnalogKeysHelper.create_sensitivity_configuration_per_key(
                test_case=self,
                keys_and_sensitivities={key: sensitivity for key in all_analog_keys})
            rapid_trigger_table = AnalogKeysTestUtils.AnalogKeysHelper.create_rapid_trigger_table(
                test_case=self, directory=directory, sensitivity_per_keys=sensitivity_per_key)
            ProfileManagementTestUtils.write(test_case=self, data=HexList(rapid_trigger_table),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=rapid_trigger_table.first_sector_id_lsb,
                                             crc_32=rapid_trigger_table.crc_32)
            profile.update_tag_content(
                directory=directory,
                tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B08_RAPID_TRIGGER:
                                  rapid_trigger_table.table_id})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Write 0x8101 profile to NVS\n{profile}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=profile.first_sector_id_lsb,
                                             crc_32=profile.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Update the directory and save in the NVS\n{directory}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(directory),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=directory.first_sector_id_lsb,
                                             crc_32=directory.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Active the {profile} with the Rapid Trigger configuration table")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                                file_type_id=file_type_id,
                                                file_id=profile.file_id_lsb,
                                                count=len(HexList(profile)),
                                                crc_32=profile.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send setRapidTriggerState request to ENABLE rapid_trigger_state")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.HIDppHelper.set_rapid_trigger_state(
                test_case=self, rapid_trigger_state=AnalogKeysTestUtils.Status.ENABLE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Perform keystrokes and check reports in rapid trigger enable")
            # ----------------------------------------------------------------------------------------------------------
            self.perform_keystrokes_on_keys_and_check_reports(keys=all_analog_keys,
                                                              actuation_point=actuation_point,
                                                              sensitivity=sensitivity,
                                                              rapid_trigger_state=AnalogKeysTestUtils.Status.ENABLE)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
    # end def _test_configure_profile_global_sensitivity_via_software

    def _test_configure_profile_per_key_sensitivity_via_software(self, file_type_id):
        """
        Validate the users are able to adjust the per key sensitivity and apply it to profiles via software.

        :param file_type_id: File Type Id
        :type file_type_id: ``int | ProfileManagement.FileTypeId.X8101``
        """
        actuation_point = self.config.F_DefaultActuationPoint
        directory, profiles = self.create_directory_and_profiles(file_type_id=file_type_id)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over profiles: {profiles}")
        # --------------------------------------------------------------------------------------------------------------
        for profile in profiles:
            random_selected_keys = AnalogKeysTestUtils.AnalogKeysHelper.select_standard_keys_randomly(
                self, num_of_keys=10)
            subset_random_selected_keys = list({choice(random_selected_keys) for _ in range(5)})
            sensitivity = choice(range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_SENSITIVITY,
                                       AnalogKeysTestUtils.AnalogKeysHelper.MAX_SENSITIVITY))
            per_key_sensitivity = choice(range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_SENSITIVITY,
                                               AnalogKeysTestUtils.AnalogKeysHelper.MAX_SENSITIVITY))
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Create a Rapid Trigger configuration table and set sensitivity: {sensitivity} to"
                                     f": {random_selected_keys!r} and set different sensitivity: "
                                     f"{per_key_sensitivity} to: {subset_random_selected_keys}")
            # ----------------------------------------------------------------------------------------------------------
            sensitivity_per_key = AnalogKeysTestUtils.AnalogKeysHelper.create_sensitivity_configuration_per_key(
                test_case=self,
                keys_and_sensitivities={
                    random_selected_key:
                    (per_key_sensitivity if random_selected_key in subset_random_selected_keys else sensitivity)
                    for random_selected_key in random_selected_keys})
            rapid_trigger_table = AnalogKeysTestUtils.AnalogKeysHelper.create_rapid_trigger_table(
                test_case=self, directory=directory, sensitivity_per_keys=sensitivity_per_key)
            ProfileManagementTestUtils.write(test_case=self, data=HexList(rapid_trigger_table),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=rapid_trigger_table.first_sector_id_lsb,
                                             crc_32=rapid_trigger_table.crc_32)
            profile.update_tag_content(
                directory=directory,
                tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B08_RAPID_TRIGGER:
                                  rapid_trigger_table.table_id})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Write 0x8101 profile to NVS\n{profile}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=profile.first_sector_id_lsb,
                                             crc_32=profile.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Update the directory and save in the NVS\n{directory}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(directory),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=directory.first_sector_id_lsb,
                                             crc_32=directory.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Active the {profile} with the Rapid Trigger configuration table")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                                file_type_id=file_type_id,
                                                file_id=profile.file_id_lsb,
                                                count=len(HexList(profile)),
                                                crc_32=profile.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send setRapidTriggerState request to ENABLE rapid_trigger_state")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.HIDppHelper.set_rapid_trigger_state(
                test_case=self, rapid_trigger_state=AnalogKeysTestUtils.Status.ENABLE)
            sleep(_WAIT_REPORT_TIME_MS)
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

            all_analog_keys = list(self.button_stimuli_emulator.keyboard_layout.KEYID_2_CHAINID.keys())
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Test Loop over selected keys: {all_analog_keys!r}")
            # ----------------------------------------------------------------------------------------------------------
            for key in all_analog_keys:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Perform a key press on {key!r} with key_travel = {actuation_point + sensitivity}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(key_id=key,
                                                              displacement=actuation_point + sensitivity)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check HID MAKE report of {key!r} is received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key, MAKE))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Release {key!r} with key_travel = {actuation_point}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(key_id=key, displacement=actuation_point)

                if key in subset_random_selected_keys:
                    if per_key_sensitivity <= sensitivity:
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_check(
                            self, f"Check HID BREAK report of {key!r} is received from the device")
                        # ----------------------------------------------------------------------------------------------
                        KeyMatrixTestUtils.check_hid_report_by_key_id(
                            test_case=self, key=KeyMatrixTestUtils.Key(key, BREAK))
                    else:
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_check(
                            self, f"Check there is no HID BREAK report of {key!r} received from the device")
                        # ----------------------------------------------------------------------------------------------
                        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_step(self, f"Release {key!r} with key_travel = "
                                                 f"{actuation_point - (per_key_sensitivity - sensitivity)}")
                        # ----------------------------------------------------------------------------------------------
                        self.button_stimuli_emulator.key_displacement(
                            key_id=key, displacement=actuation_point - (per_key_sensitivity - sensitivity))

                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_check(
                            self, f"Check HID BREAK report of {key!r} is received from the device")
                        # ----------------------------------------------------------------------------------------------
                        KeyMatrixTestUtils.check_hid_report_by_key_id(
                            test_case=self, key=KeyMatrixTestUtils.Key(key, BREAK))
                    # end if
                else:
                    if key in random_selected_keys:
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_check(
                            self, f"Check HID BREAK report of {key!r} is received from the device")
                        # ----------------------------------------------------------------------------------------------
                        KeyMatrixTestUtils.check_hid_report_by_key_id(
                            test_case=self, key=KeyMatrixTestUtils.Key(key, BREAK))
                    else:
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_check(
                            self, f"Check there is no HID BREAK report of {key!r} received from the device")
                        # ----------------------------------------------------------------------------------------------
                        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
                    # end if
                # end if

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self,
                    f"Perform a key press on {key!r} with key_travel = {actuation_point + sensitivity}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(
                    key_id=key, displacement=actuation_point + sensitivity)

                if key in random_selected_keys:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(
                        self, f"Check HID MAKE report of {key!r} is received from the device")
                    # --------------------------------------------------------------------------------------------------
                    KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                                  key=KeyMatrixTestUtils.Key(key, MAKE))
                else:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(
                        self, f"Check there is no HID MAKE report of {key!r} received from the device")
                    # --------------------------------------------------------------------------------------------------
                    ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
                # end if

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Fully release {key!r}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_release(key_id=key)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check HID BREAK report is received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key, BREAK))
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
    # end def _test_configure_profile_per_key_sensitivity_via_software

    def _test_configure_profile_per_key_actuation_point_and_sensitivity_via_software(self, file_type_id):
        """
        Validate the users are able to adjust the per key sensitivity and apply it to profiles via software.

        :param file_type_id: File Type Id
        :type file_type_id: ``int | ProfileManagement.FileTypeId.X8101``
        """
        directory, profiles = self.create_directory_and_profiles(file_type_id=file_type_id)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over profiles: {profiles}")
        # --------------------------------------------------------------------------------------------------------------
        for profile in profiles:
            all_analog_keys = list(self.button_stimuli_emulator.keyboard_layout.KEYID_2_CHAINID.keys())
            random_selected_keys = list({choice(all_analog_keys) for _ in range(10)})
            sensitivity = choice(range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_SENSITIVITY,
                                       AnalogKeysTestUtils.AnalogKeysHelper.MAX_SENSITIVITY))
            actuation_point = choice(range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT + sensitivity,
                                           AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT + 1 - sensitivity))
            per_key_actuation_point = choice(range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT,
                                                   AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT + 1))
            per_key_sensitivity = choice(range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_SENSITIVITY,
                                               AnalogKeysTestUtils.AnalogKeysHelper.MAX_SENSITIVITY))
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Create an Actuation Point Table and set {random_selected_keys!r} "
                                     f"with per_key_actuation_point = {per_key_actuation_point}")
            # ----------------------------------------------------------------------------------------------------------
            actuation_point_per_key = AnalogKeysTestUtils.AnalogKeysHelper.create_actuation_point_configuration_per_key(
                test_case=self,
                keys_and_actuation_points={
                    random_selected_key: per_key_actuation_point for random_selected_key in random_selected_keys})
            actuation_point_table = AnalogKeysTestUtils.AnalogKeysHelper.create_actuation_point_table(
                test_case=self, directory=directory, actuation_point_per_keys=actuation_point_per_key)
            ProfileManagementTestUtils.write(test_case=self, data=HexList(actuation_point_table),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=actuation_point_table.first_sector_id_lsb,
                                             crc_32=actuation_point_table.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Create a Rapid Trigger configuration table and set sensitivity: {sensitivity} to"
                                     f": {all_analog_keys!r} and set different sensitivity: "
                                     f"{per_key_sensitivity} to: {random_selected_keys}")
            # ----------------------------------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Edit the Global Actuation Point of {profile} with a random"
                                     f"AP = {actuation_point}")
            # ----------------------------------------------------------------------------------------------------------
            sensitivity_per_key = AnalogKeysTestUtils.AnalogKeysHelper.create_sensitivity_configuration_per_key(
                test_case=self,
                keys_and_sensitivities={
                    key: (per_key_sensitivity if key in random_selected_keys else sensitivity)
                    for key in all_analog_keys})
            rapid_trigger_table = AnalogKeysTestUtils.AnalogKeysHelper.create_rapid_trigger_table(
                test_case=self, directory=directory, sensitivity_per_keys=sensitivity_per_key)
            ProfileManagementTestUtils.write(test_case=self, data=HexList(rapid_trigger_table),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=rapid_trigger_table.first_sector_id_lsb,
                                             crc_32=rapid_trigger_table.crc_32)
            profile.update_tag_content(
                directory=directory,
                tag_content_dict={
                    ProfileManagement.Tag.ANALOG_GENERIC_SETTING: actuation_point << 8,
                    ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B08_ACTUATION: actuation_point_table.table_id,
                    ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B08_RAPID_TRIGGER: rapid_trigger_table.table_id})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Write 0x8101 profile to NVS\n{profile}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=profile.first_sector_id_lsb,
                                             crc_32=profile.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Update the directory and save in the NVS\n{directory}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(directory),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=directory.first_sector_id_lsb,
                                             crc_32=directory.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Active the {profile} with the Rapid Trigger configuration table")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                                file_type_id=file_type_id,
                                                file_id=profile.file_id_lsb,
                                                count=len(HexList(profile)),
                                                crc_32=profile.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send setRapidTriggerState request to ENABLE rapid_trigger_state")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.HIDppHelper.set_rapid_trigger_state(
                test_case=self, rapid_trigger_state=AnalogKeysTestUtils.Status.ENABLE)
            sleep(_WAIT_REPORT_TIME_MS)
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

            all_analog_keys = list(self.button_stimuli_emulator.keyboard_layout.KEYID_2_CHAINID.keys())
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Test Loop over selected keys: {all_analog_keys!r}")
            # ----------------------------------------------------------------------------------------------------------
            for key in all_analog_keys:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Perform a key press on {key!r} with key_travel = {actuation_point + sensitivity}")
                # ------------------------------------------------------------------------------------------------------
                is_per_key_actuated = (actuation_point + sensitivity) >= per_key_actuation_point
                self.button_stimuli_emulator.key_displacement(key_id=key,
                                                              displacement=actuation_point + sensitivity)

                if key not in random_selected_keys or is_per_key_actuated:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(
                        self, f"Check HID MAKE report of {key!r} is received from the device")
                    # --------------------------------------------------------------------------------------------------
                    KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                                  key=KeyMatrixTestUtils.Key(key, MAKE))
                else:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, f"Check there is no HID MAKE report of {key!r} received from the device")
                    # --------------------------------------------------------------------------------------------------
                    ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
                # end if

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Release {key!r} with key_travel = {actuation_point}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(key_id=key, displacement=actuation_point)

                if key not in random_selected_keys:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(
                        self, f"Check HID BREAK report of {key!r} is received from the device")
                    # --------------------------------------------------------------------------------------------------
                    KeyMatrixTestUtils.check_hid_report_by_key_id(
                        test_case=self, key=KeyMatrixTestUtils.Key(key, BREAK))
                else:
                    if is_per_key_actuated:
                        self.check_rapid_trigger_make_break_report(
                            displacement=actuation_point, last_displacement=actuation_point + sensitivity, key=key,
                            sensitivity=sensitivity, per_key_sensitivity=per_key_sensitivity, has_per_key_setting=True)
                    else:
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_check(
                            self, f"Check there is no HID BREAK report of {key!r} received from the device")
                        # ----------------------------------------------------------------------------------------------
                        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
                    # end if
                # end if

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Perform a key press on {key!r} with key_travel = {actuation_point + sensitivity}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(
                    key_id=key, displacement=actuation_point + sensitivity)

                if key not in random_selected_keys:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(
                        self, f"Check HID MAKE report of {key!r} is received from the device")
                    # --------------------------------------------------------------------------------------------------
                    KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                                  key=KeyMatrixTestUtils.Key(key, MAKE))
                else:
                    if is_per_key_actuated:
                        self.check_rapid_trigger_make_break_report(
                            displacement=actuation_point + sensitivity, last_displacement=actuation_point, key=key,
                            sensitivity=sensitivity, per_key_sensitivity=per_key_sensitivity, has_per_key_setting=True)
                    else:
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_check(
                            self, f"Check there is no HID MAKE report of {key!r} received from the device")
                        # ----------------------------------------------------------------------------------------------
                        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
                    # end if
                # end if

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Fully release {key!r}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_release(key_id=key)

                if key not in random_selected_keys or is_per_key_actuated:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(
                        self, f"Check HID BREAK report of {key!r} is received from the device")
                    # --------------------------------------------------------------------------------------------------
                    KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                                  key=KeyMatrixTestUtils.Key(key, BREAK))
                else:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(
                        self, f"Check there is no HID MAKE report of {key!r} received from the device")
                    # --------------------------------------------------------------------------------------------------
                    ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
                # end if
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
    # end def _test_configure_profile_per_key_actuation_point_and_sensitivity_via_software

    def perform_keystrokes_on_keys_and_check_reports(self, keys, actuation_point, sensitivity, rapid_trigger_state):
        """
        Perform keystrokes on input keys and check the corresponding reports are sent / not sent.

        :param keys: Keys to be pressed / released
        :type keys: ``list[KEY_ID]``
        :param actuation_point: Actuation point
        :type actuation_point: ``int``
        :param sensitivity: Sensitivity
        :type sensitivity: ``int``
        :param rapid_trigger_state: Rapid trigger state
        :type rapid_trigger_state: ``AnalogKeysTestUtils.Status | bool``
        """
        make_displacement = actuation_point + sensitivity if \
            (actuation_point + sensitivity) <= AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT else \
            actuation_point
        break_displacement = actuation_point if \
            (actuation_point + sensitivity) <= AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT else \
            max(actuation_point - sensitivity, 0)
        # Wait 10ms to ensure all HsID reports has been sent from the device after the previous test step.
        sleep(_WAIT_REPORT_TIME_MS)
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over selected keys: {keys!r}")
        # --------------------------------------------------------------------------------------------------------------
        for key in keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Perform a key press on {key!r} with key_travel = {make_displacement}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=key, displacement=make_displacement)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check HID MAKE report of {key!r} is received from the device")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(key, MAKE))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key!r} with key_travel = {break_displacement}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=key, displacement=break_displacement)

            if rapid_trigger_state:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check HID BREAK report of {key!r} is received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key, BREAK))
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check there is no HID BREAK report of {key!r} received from the device")
                # ------------------------------------------------------------------------------------------------------
                ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Perform a key press on {key!r} with key_travel = {make_displacement}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=key, displacement=make_displacement)

            if rapid_trigger_state:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check HID MAKE report of {key!r} is received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key, MAKE))
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check there is no HID MAKE report of {key!r} received from the device")
                # ------------------------------------------------------------------------------------------------------
                ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Fully release {key!r}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key_id=key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID BREAK report is received from the device")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(key, BREAK))
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
    # end def perform_keystrokes_on_keys_and_check_reports

    def check_rapid_trigger_make_break_report(self, displacement, last_displacement,
                                              key, sensitivity, per_key_sensitivity, has_per_key_setting):
        """
        Check the HID MAKE / BREAK report of the key is received from the device.

        :param displacement: Key travel displacement
        :type displacement: ``int``
        :param last_displacement: Last key travel displacement
        :type last_displacement: ``int``
        :param key: Key ID
        :type key: ``KEY_ID``
        :param sensitivity: Sensitivity
        :type sensitivity: ``int``
        :param per_key_sensitivity: Per key sensitivity
        :type per_key_sensitivity: ``int``
        :param has_per_key_setting: Has per key setting
        :type has_per_key_setting: ``bool``
        """
        displacement_diff = displacement - last_displacement
        if has_per_key_setting:
            if abs(displacement_diff) >= per_key_sensitivity:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check HID {'MAKE' if displacement_diff >= 0 else 'BREAK'} report of "
                          f"{key!r} is received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(
                    test_case=self,
                    key=KeyMatrixTestUtils.Key(key, MAKE if displacement_diff >= 0 else BREAK))
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check there is no HID {'MAKE' if displacement_diff >= 0 else 'BREAK'} report "
                          f"of {key!r} received from the device")
                # ------------------------------------------------------------------------------------------------------
                ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
            # end if
        else:
            if abs(displacement_diff) >= sensitivity:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check HID {'MAKE' if displacement_diff >= 0 else 'BREAK'} report of "
                          f"{key!r} is received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(
                    test_case=self,
                    key=KeyMatrixTestUtils.Key(key, MAKE if displacement_diff >= 0 else BREAK))
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check there is no HID {'MAKE' if displacement_diff >= 0 else 'BREAK'} report "
                          f"of {key!r} received from the device")
                # ------------------------------------------------------------------------------------------------------
                ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
            # end if
        # end if
    # end def check_rapid_trigger_make_break_report
# end class AnalogKeysBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
