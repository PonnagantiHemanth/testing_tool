#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hid.keyboard.analogkeys.robustness
:brief: ``AnalogKeys`` robustness test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2024/03/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import choice
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagement
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.analogkeysutils import AnalogKeysTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.base.profilemanagementutils import ProfileManagementTestUtils
from pytestbox.device.hid.keyboard.analogkeys.analogkeys import AnalogKeysTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_RESERVED = "Test loop over reserved range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AnalogKeysRobustnessTestCase(AnalogKeysTestCase):
    """
    Validate ``AnalogKeys`` robustness test cases
    """

    @features("Feature1B08")
    @level("Robustness")
    @services('DualKeyMatrix')
    def test_key_travel_with_multi_presses(self):
        """
        Validate the keyTravelChangeEvents is indicating the furthest key press when multiple analog keys are
        pressing
        """
        random_selected_keys_travels = {}
        while len(random_selected_keys_travels) < 10:
            random_selected_key = choice(list(self.button_stimuli_emulator.keyboard_layout.KEYID_2_CHAINID.keys()))
            random_key_travel = choice(range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT,
                                             AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT))
            if random_selected_key in random_selected_keys_travels.keys():
                continue
            else:
                random_selected_keys_travels[random_selected_key] = random_key_travel
            # end if
        # end while
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setKeyTravelEventState request to ENABLE key_travel_event_state")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.HIDppHelper.set_key_travel_event_state(
            test_case=self, key_travel_event_state=AnalogKeysTestUtils.Status.ENABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over key and key_travel in {random_selected_keys_travels}")
        # --------------------------------------------------------------------------------------------------------------
        for index, key_and_key_travel in enumerate(random_selected_keys_travels.items()):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Perform key press on the random selected {key_and_key_travel[0]!r} "
                                     f"with random travel distances: {key_and_key_travel[1]}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=key_and_key_travel[0],
                                                          displacement=key_and_key_travel[1])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the key_travel is matching the furthest key press from the"
                                      "keyTravelChangeEvent")
            # ----------------------------------------------------------------------------------------------------------
            event = AnalogKeysTestUtils.HIDppHelper.key_travel_change_event(test_case=self, allow_no_message=True)
            if index == 0 or key_and_key_travel[1] >= max(list(random_selected_keys_travels.values())[:index]):
                self.assertEqual(expected=key_and_key_travel[1],
                                 obtained=to_int(event.key_travel),
                                 msg="The key travel of the event does not match the furthest key press")
            else:
                self.assertNone(obtained=event,
                                msg="There is no event expected to be received when there is no key travel further "
                                    "than previous")
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over key and key_travel in {random_selected_keys_travels}")
        # --------------------------------------------------------------------------------------------------------------
        for index, key_and_key_travel in enumerate(random_selected_keys_travels.items()):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key_and_key_travel[0]!r}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key_id=key_and_key_travel[0])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the key_travel is as expected from keyTravelChangeEvent")
            # ----------------------------------------------------------------------------------------------------------
            event = AnalogKeysTestUtils.HIDppHelper.key_travel_change_event(test_case=self, allow_no_message=True)
            if key_and_key_travel[1] == max(list(random_selected_keys_travels.values())[index:]):
                self.assertEqual(expected=max(list(random_selected_keys_travels.values())[index + 1:]) if
                                 index < (len(random_selected_keys_travels) - 1) else 0,
                                 obtained=to_int(event.key_travel),
                                 msg="The key travel of the event does not match the furthest key press")
            else:
                self.assertNone(obtained=event,
                                msg="There is no event expected to be received when the current released key is not "
                                    "the furthest one")
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_AKEY_0001", _AUTHOR)
    # end def test_key_travel_with_multi_presses

    @features("Feature1B08")
    @features("Feature8101")
    @level("Robustness")
    @services('DualKeyMatrix')
    def test_multi_action_at_actuation_point(self):
        """
        Validate the events of Multi-Action assignment are working as expected if the key_travel is exactly equal to
        the actuation points.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create onboard profiles")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestUtils.ProfileHelper.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over onboard profiles: {profiles}")
        # --------------------------------------------------------------------------------------------------------------
        for index, profile in enumerate(profiles):
            first_actuation_point = choice(range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT,
                                           AnalogKeysTestUtils.AnalogKeysHelper.MA_MAX_FIRST_ACTUATION_POINT))
            second_actuation_point = choice(range(first_actuation_point +
                                                  AnalogKeysTestUtils.AnalogKeysHelper.MA_RELEASE_POINT_DELTA,
                                                  AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT))
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Edit the Actuation Point of {profile} with random actuation point = "
                                     f"{first_actuation_point}")
            # ----------------------------------------------------------------------------------------------------------
            profile.update_tag_content(
                directory=directory,
                tag_content_dict={ProfileManagement.Tag.ANALOG_GENERIC_SETTING: first_actuation_point << 8})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self,
                               f"Create a Multi-Action configuration table and set 2nd AP to {second_actuation_point} "
                               "and set random assignments")
            # ----------------------------------------------------------------------------------------------------------
            multi_action_table = AnalogKeysTestUtils.AnalogKeysHelper.create_multi_action_table(
                test_case=self, number_of_key_to_be_random_generated=1, directory=directory,
                global_actuation_point=first_actuation_point)
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
            LogHelper.log_step(self, "Send setKeyTravelEventState request to ENABLE key_travel_event_state")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.HIDppHelper.set_key_travel_event_state(
                test_case=self, key_travel_event_state=AnalogKeysTestUtils.Status.ENABLE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send setRapidTriggerState request to ENABLE rapid_trigger_state")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.HIDppHelper.set_rapid_trigger_state(
                test_case=self, rapid_trigger_state=AnalogKeysTestUtils.Status.ENABLE)

            if index == 0:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Enable Multi-Action")
                # ------------------------------------------------------------------------------------------------------
                AnalogKeysTestUtils.enable_disable_multi_action_fkc(test_case=self)
            else:
                sleep(0.1)
                ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
            # end if

            random_selected_key = multi_action_table.groups[0].trigger_key
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Perform a key press on {random_selected_key!r} with key_travel = {first_actuation_point}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=random_selected_key,
                                                          displacement=first_actuation_point)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID report(s) match the event0")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.MultiActionChecker.check_multi_actions(test_case=self, trigger_key=random_selected_key,
                                                                       multi_action_table=multi_action_table,
                                                                       last_actuation_point=0,
                                                                       current_actuation_point=first_actuation_point,
                                                                       global_actuation_point=first_actuation_point)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Fully release {random_selected_key!r}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key_id=random_selected_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID report(s) match the event3")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.MultiActionChecker.check_multi_actions(test_case=self, trigger_key=random_selected_key,
                                                                       multi_action_table=multi_action_table,
                                                                       last_actuation_point=first_actuation_point,
                                                                       current_actuation_point=0,
                                                                       global_actuation_point=first_actuation_point)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Perform a key press on {random_selected_key!r} with key_travel = {second_actuation_point}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=random_selected_key,
                                                          displacement=second_actuation_point)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID report(s) match the event0 and event1")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.MultiActionChecker.check_multi_actions(test_case=self, trigger_key=random_selected_key,
                                                                       multi_action_table=multi_action_table,
                                                                       last_actuation_point=0,
                                                                       current_actuation_point=second_actuation_point,
                                                                       global_actuation_point=first_actuation_point)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Fully release {random_selected_key!r}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key_id=random_selected_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID report(s) match the event2 and event3")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.MultiActionChecker.check_multi_actions(test_case=self, trigger_key=random_selected_key,
                                                                       multi_action_table=multi_action_table,
                                                                       last_actuation_point=second_actuation_point,
                                                                       current_actuation_point=0,
                                                                       global_actuation_point=first_actuation_point)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_AKEY_0002", _AUTHOR)
    # end def test_multi_action_at_actuation_point

    @features("Feature1B08")
    @level("Robustness")
    @services('DualKeyMatrix')
    def test_key_travel_less_than_sensitivity(self):
        """
        Validate there is no HID report shall be sent when the key_travel less than sensitivity.
        """
        random_selected_keys = AnalogKeysTestUtils.AnalogKeysHelper.select_standard_keys_randomly(self, num_of_keys=10)
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
            sensitivity = choice(range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_SENSITIVITY,
                                       AnalogKeysTestUtils.AnalogKeysHelper.MAX_SENSITIVITY))
            actuation_point = choice(range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT + sensitivity,
                                           AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT - sensitivity))
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Edit the Actuation Point of {profile} with random {actuation_point}")
            # ----------------------------------------------------------------------------------------------------------
            profile.update_tag_content(
                directory=directory,
                tag_content_dict={ProfileManagement.Tag.ANALOG_GENERIC_SETTING: actuation_point << 8})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Create a Rapid Trigger configuration table and set sensitivity: {sensitivity} "
                                     f"with random selected keys: {random_selected_keys!r}")
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
            LogHelper.log_step(
                self, f"Active the {profile} with the Rapid Trigger configuration table: {rapid_trigger_table}")
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
            LogHelper.log_info(self, f"Test Loop over selected keys: {random_selected_keys}")
            # ----------------------------------------------------------------------------------------------------------
            for random_selected_key in random_selected_keys:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Perform a key press on {random_selected_key!r} with key_travel = {actuation_point}")
                # ------------------------------------------------------------------------------------------------------
                ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
                self.button_stimuli_emulator.key_displacement(key_id=random_selected_key, displacement=actuation_point)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check HID MAKE report of {random_selected_key!r} is received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(random_selected_key, MAKE))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"Test Loop sensitivity in {range(0, sensitivity)}")
                # ------------------------------------------------------------------------------------------------------
                for key_travel in range(0, sensitivity):
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f"Release {random_selected_key!r} with key_travel = {key_travel}")
                    # --------------------------------------------------------------------------------------------------
                    self.button_stimuli_emulator.key_displacement(key_id=random_selected_key,
                                                                  displacement=actuation_point - key_travel)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, "Check there is no HID report received from the device")
                    # --------------------------------------------------------------------------------------------------
                    ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f"Press {random_selected_key!r} with key_travel = {key_travel}")
                    # --------------------------------------------------------------------------------------------------
                    self.button_stimuli_emulator.key_displacement(key_id=random_selected_key,
                                                                  displacement=actuation_point)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, "Check there is no HID report received from the device")
                    # --------------------------------------------------------------------------------------------------
                    ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
                # end for
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "End Test Loop")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Fully release {random_selected_key!r}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_release(key_id=random_selected_key)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check there is only one HID BREAK report received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(random_selected_key, BREAK))
                ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Perform a key press on {random_selected_key!r} with key_travel = {actuation_point}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_displacement(key_id=random_selected_key,
                                                              displacement=actuation_point)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check HID MAKE report of {random_selected_key!r} is received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(random_selected_key, MAKE))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"Test Loop over sensitivity in {range(0, sensitivity)}")
                # ------------------------------------------------------------------------------------------------------
                for key_travel in range(0, sensitivity):
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f"Press {random_selected_key!r} with key_travel = {key_travel}")
                    # --------------------------------------------------------------------------------------------------
                    self.button_stimuli_emulator.key_displacement(key_id=random_selected_key,
                                                                  displacement=actuation_point + key_travel)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, "Check there is no HID report received from the device")
                    # --------------------------------------------------------------------------------------------------
                    ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f"Release {random_selected_key!r} with key_travel = {key_travel}")
                    # --------------------------------------------------------------------------------------------------
                    self.button_stimuli_emulator.key_displacement(key_id=random_selected_key,
                                                                  displacement=actuation_point)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, "Check there is no HID report received from the device")
                    # --------------------------------------------------------------------------------------------------
                    ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
                # end for
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "End Test Loop")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Fully release {random_selected_key!r}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_release(key_id=random_selected_key)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check there is only one HID BREAK report received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(random_selected_key, BREAK))
                ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_AKEY_0003", _AUTHOR)
    # end def test_key_travel_less_than_sensitivity

    @features("Feature1B08")
    @level("Robustness")
    @services('DualKeyMatrix')
    def test_all_available_actuation_points_on_base_profile(self):
        """
        Validate all available actuation point can be set to the base profile.
        """
        actuation_scaling_range_list = [int(element) for element in self.config.F_ActuationScalingRange]
        self.post_requisite_reload_nvs = True
        random_selected_key = choice(list(self.button_stimuli_emulator.keyboard_layout.KEYID_2_CHAINID.keys()))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Base Profile")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.switch_to_base_profile(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over actuation_point in range(min_actuation_point, max_actuation_point)")
        # --------------------------------------------------------------------------------------------------------------
        for index, actuation_point in enumerate(actuation_scaling_range_list):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Enter Global Actuation Point mode (FN + F6)")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.enter_exit_actuation_point_adjustment_mode(test_case=self)

            if index == 0:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Edit Actuation Point to {actuation_point} by pressing {KEY_ID.KEYBOARD_1!r}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_1)
            else:
                increase_key = choice(self.INCREASE_KEYS)
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Edit Actuation Point to {actuation_point} by pressing {increase_key!r}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.keystroke(key_id=increase_key)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Save settings and exit Global Actuation mode (FN + F6)")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.enter_exit_actuation_point_adjustment_mode(test_case=self)
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Press a random selected key: {random_selected_key!r} with key_travel = {actuation_point}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=random_selected_key,
                                                          displacement=actuation_point)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check HID MAKE report of {random_selected_key!r} is received from the device")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(random_selected_key, MAKE))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Fully release {random_selected_key!r}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key_id=random_selected_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check HID BREAK report of {random_selected_key!r} is received from the device")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(random_selected_key, BREAK))
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_AKEY_0004", _AUTHOR)
    # end def test_all_available_actuation_points_on_base_profile

    @features("Feature1B08")
    @level("Robustness")
    @services('DualKeyMatrix')
    def test_all_available_actuation_points_on_onboard_profiles(self):
        """
        Validate all available actuation point can be set to onboard profiles.
        """
        self._test_all_available_actuation_points_on_profiles(
            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE)

        self.testCaseChecked("ROB_AKEY_0005", _AUTHOR)
    # end def test_all_available_actuation_points_on_onboard_profiles

    @features("Feature1B08")
    @level("Robustness")
    @services('DualKeyMatrix')
    def test_all_available_actuation_points_on_host_profiles(self):
        """
        Validate all available actuation point can be set to host profiles.
        """
        self._test_all_available_actuation_points_on_profiles(
            file_type_id=ProfileManagement.FileTypeId.X8101.HOST_MODE_PROFILE)

        self.testCaseChecked("ROB_AKEY_0006", _AUTHOR)
    # end def test_all_available_actuation_points_on_host_profiles

    @features("Feature1B08")
    @level("Robustness")
    @services('DualKeyMatrix')
    def test_perform_keystrokes_as_fast_as_possible(self):
        """
        Validate there is no HID report missed when the user is pressing any keys as fast as possible.
        """
        random_selected_keys = AnalogKeysTestUtils.AnalogKeysHelper.select_standard_keys_randomly(self, num_of_keys=10)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over selected keys: {random_selected_keys}")
        # --------------------------------------------------------------------------------------------------------------
        for random_selected_key in random_selected_keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Fully press {random_selected_key!r}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key_id=random_selected_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Fully release {random_selected_key!r}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key_id=random_selected_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check HID MAKE report of {random_selected_key!r} is received from the device")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(random_selected_key, MAKE))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check HID BREAK report of {random_selected_key!r} is received from the device")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(random_selected_key, BREAK))
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_AKEY_0007", _AUTHOR)
    # end def test_perform_keystrokes_as_fast_as_possible

    @features("Feature1B08")
    @level("Robustness")
    @services('DualKeyMatrix')
    def test_key_travel_equal_actuation_point(self):
        """
        Validate there is no HID report missed when the user is pressing any keys with key travels exactly equal to
        the actuation point.
        """
        random_selected_keys = AnalogKeysTestUtils.AnalogKeysHelper.select_standard_keys_randomly(self, num_of_keys=10)
        default_actuation_point = self.config.F_DefaultActuationPoint
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over selected keys: {random_selected_keys}")
        # --------------------------------------------------------------------------------------------------------------
        for random_selected_key in random_selected_keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {random_selected_key!r} with key_travel = {default_actuation_point}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=random_selected_key,
                                                          displacement=default_actuation_point)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check HID MAKE report of {random_selected_key!r} is received from the device")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(random_selected_key, MAKE))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Fully release {random_selected_key!r}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key_id=random_selected_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check HID BREAK report of {random_selected_key!r} is received from the device")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(random_selected_key, BREAK))
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_AKEY_0008", _AUTHOR)
    # end def test_key_travel_equal_actuation_point

    @features("Feature1B08")
    @level("Robustness")
    @services('DualKeyMatrix')
    def test_key_travel_less_than_actuation_point(self):
        """
        Validate there is no HID report can be received when the user is pressing any keys with key travels less than
        the actuation point.
        """
        random_selected_keys = AnalogKeysTestUtils.AnalogKeysHelper.select_standard_keys_randomly(self, num_of_keys=10)
        default_actuation_point = self.config.F_DefaultActuationPoint
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over selected keys: {random_selected_keys}")
        # --------------------------------------------------------------------------------------------------------------
        for random_selected_key in random_selected_keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self,
                               f"Press {random_selected_key!r} with key_travel = "
                               f"{default_actuation_point - AnalogKeysTestUtils.AnalogKeysHelper.RESOLUTION_PER_STEP}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(
                key_id=random_selected_key,
                displacement=default_actuation_point - AnalogKeysTestUtils.AnalogKeysHelper.RESOLUTION_PER_STEP)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check there is no HID report received from the device")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Fully release {random_selected_key!r}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key_id=random_selected_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check there is no HID report received from the device")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_AKEY_0009", _AUTHOR)
    # end def test_key_travel_less_than_actuation_point

    def _test_all_available_actuation_points_on_profiles(self, file_type_id):
        """
        Validate all available actuation point can be set to profiles.

        :param file_type_id: File Type Id
        :type file_type_id: ``int | ProfileManagement.FileTypeId.X8101``
        """
        random_selected_key = choice(list(self.button_stimuli_emulator.keyboard_layout.KEYID_2_CHAINID.keys()))

        directory, profiles = self.create_directory_and_profiles(file_type_id=file_type_id)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over profiles")
        # --------------------------------------------------------------------------------------------------------------
        for profile in profiles:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                self, "Test Loop over actuation_point in range(min_actuation_point, max_actuation_point)")
            # ----------------------------------------------------------------------------------------------------------
            for actuation_point in range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT,
                                         AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT + 1):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Edit Actuation Point of profile to {actuation_point}")
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
                LogHelper.log_step(self, f"Active {profile}")
                # ------------------------------------------------------------------------------------------------------
                ProfileManagementTestUtils.activate(
                    test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                    file_type_id=file_type_id,
                    file_id=profile.file_id_lsb,
                    count=len(HexList(profile)),
                    crc_32=profile.crc_32)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Press a random selected key: {random_selected_key!r} with key_travel = {actuation_point}")
                # ------------------------------------------------------------------------------------------------------
                sleep(0.1)
                ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
                self.button_stimuli_emulator.key_displacement(key_id=random_selected_key, displacement=actuation_point)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check HID MAKE report of {random_selected_key!r} is received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(random_selected_key, MAKE))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Fully release {random_selected_key!r}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_release(key_id=random_selected_key)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Check HID BREAK report of {random_selected_key!r} is received from the device")
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(random_selected_key, BREAK))
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
    # end def _test_all_available_actuation_points_on_profiles
# end class AnalogKeysRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
