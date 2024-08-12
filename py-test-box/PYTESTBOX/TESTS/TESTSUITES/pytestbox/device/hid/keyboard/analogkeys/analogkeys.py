#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hid.keyboard.analogkeys.analogkeys
:brief: Validate ``AnalogKeys`` feature
:author: YY Liu <yliu5@logitech.com>
:date: 2024/03/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import choice
from time import sleep

from pychannel.channelinterfaceclasses import LogitechProtocol
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.unifiedbattery import UnifiedBattery
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagement
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.analogkeysutils import AnalogKeysTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.base.profilemanagementutils import ProfileManagementTestUtils
from pytestbox.device.base.rgbeffectsutils import RGBEffectsTestUtils
from pytestbox.device.base.unifiedbatteryutils import UnifiedBatteryTestUtils
from pytestbox.shared.base.dfuutils import DfuTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AnalogKeysTestCase(DeviceBaseTestCase):
    """
    Validate ``AnalogKeys`` TestCases in Application mode
    """

    # TODO: Add roller into the list once the test framework support it.
    ADJUSTMENT_KEYS = ([KEY_ID.KEYBOARD_LEFT_ARROW, KEY_ID.KEYBOARD_RIGHT_ARROW,
                       KEY_ID.KEYBOARD_UP_ARROW, KEY_ID.KEYBOARD_DOWN_ARROW] +
                       list(range(KEY_ID.KEYBOARD_1, KEY_ID.KEYBOARD_0 + 1)))
    DECREASE_KEYS = [KEY_ID.KEYBOARD_LEFT_ARROW, KEY_ID.KEYBOARD_DOWN_ARROW]
    INCREASE_KEYS = [KEY_ID.KEYBOARD_RIGHT_ARROW, KEY_ID.KEYBOARD_UP_ARROW]

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()
        self.post_requisite_reload_nvs = False
        self.post_requisite_program_mcu_initial_state = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x1B08 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1b08_index, self.feature_1b08, _, _ = AnalogKeysTestUtils.HIDppHelper.get_parameters(
            test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Change KBD Functional Mode from Legacy to Analog")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.kbd.func_mode_analog()
        AnalogKeysTestUtils.MultiActionChecker.clean_key_id_and_ap_mapping_table()

        self.config = self.f.PRODUCT.FEATURES.COMMON.ANALOG_KEYS
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites

        :raise ``AssertionError``:
            if the debugger or the backup NVS is not present when programming the MCU to initial state
        :raise ``RuntimeError``: if the maximum number of retries is reached or fail to reload the NVS
        """
        with self.manage_post_requisite():
            if self.post_requisite_reload_nvs:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.NvsHelper.restore_nvs(self)
                self.post_requisite_reload_nvs = False
            # end if
        # end with

        with self.manage_post_requisite():
            # Reset all keys
            self.button_stimuli_emulator.release_all()
        # end with

        with self.manage_post_requisite():
            try_count = 0
            max_try = 3
            while try_count < max_try:
                try:
                    if self.post_requisite_program_mcu_initial_state:
                        assert self.debugger is not None, \
                            "Cannot program MCU to initial state if the debugger is not present"
                        assert self.memory_manager.backup_nvs_parser is not None, \
                            "Cannot program MCU to initial state if the backup NVS is not present"

                        if self.current_channel.protocol == LogitechProtocol.USB and self.current_channel.is_open:
                            ChannelUtils.close_channel(test_case=self)
                        # end if

                        if self.companion_debugger:
                            self.companion_debugger.stop()
                        # end if

                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_post_requisite(test_case=self, text="Program the MCU back to its initial state")
                        # ----------------------------------------------------------------------------------------------
                        # noinspection PyUnresolvedReferences
                        fw_hex = join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_HexFileName)
                        nvs_file = self.memory_manager.backup_nvs_parser.to_hex_file()
                        self.debugger.reload_file(firmware_hex_file=fw_hex, nvs_hex_file=nvs_file, no_reset=True)

                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_post_requisite(test_case=self, text="Force target on application")
                        # ----------------------------------------------------------------------------------------------
                        self.debugger.reset()
                        self.companion_debugger.reset()
                        DfuTestUtils.force_target_on_application(test_case=self, check_required=True)

                        self.post_requisite_program_mcu_initial_state = False
                    # end if

                    ChannelUtils.empty_queue(test_case=self,
                                             queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT)

                    break
                except Exception as e:
                    try_count += 1

                    self.log_traceback_as_warning(
                        supplementary_message=f"Exception in tearDown with retry counter = {try_count}:")

                    if try_count >= max_try:
                        raise RuntimeError("Max tries") from e
                    # end if

                    if self.debugger is not None:
                        if self.memory_manager.backup_nvs_parser is None:
                            # Stop trying if not possible to reload the NVS
                            raise RuntimeError("Not possible to reload NVS") from e
                        # end if
                        self.post_requisite_program_mcu_initial_state = True
                    # end if
                # end try
            # end while
        # end with

        super().tearDown()
    # end def tearDown

    def create_directory_and_profiles(self, file_type_id):
        """
        Create onboard profiles and 3 * host profiles (If the input file_type_id is HOST_MODE_PROFILE)

        :param file_type_id: File Type ID
        :type file_type_id: ``int | ProfileManagement.FileTypeId.X8101``

        :return: Directory and profiles
        :rtype: ``tuple[DirectoryFile, list[Profile]]``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create onboard profiles")
        # --------------------------------------------------------------------------------------------------------------
        directory, onboard_profiles = \
            ProfileManagementTestUtils.ProfileHelper.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)

        if file_type_id == ProfileManagement.FileTypeId.X8101.HOST_MODE_PROFILE:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send getSetMode request with set_onboard_mode=1, "
                                     f"onboard_mode={ProfileManagement.Mode.HOST_MODE}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.HIDppHelper.get_set_mode(
                test_case=self,
                onboard_mode=ProfileManagement.Mode.HOST_MODE,
                set_onboard_mode=ProfileManagementTestUtils.RequestType.SET)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Create host profiles * 3")
            # ----------------------------------------------------------------------------------------------------------
            host_profiles = [ProfileManagementTestUtils.ProfileHelper.create_profile_from_settings(
                self, directory, file_type_id=ProfileManagement.FileTypeId.X8101.HOST_MODE_PROFILE) for _ in range(3)]

            for profile in host_profiles:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"Write 0x8101 profile to NVS\n{profile}")
                # ------------------------------------------------------------------------------------------------------
                ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                                 store_in_nvs=True,
                                                 first_sector_id_lsb=profile.first_sector_id_lsb,
                                                 crc_32=profile.crc_32)
            # end for

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Update the directory and save in the NVS\n{directory}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(directory),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=directory.first_sector_id_lsb,
                                             crc_32=directory.crc_32)

            profiles = host_profiles
        else:
            profiles = onboard_profiles
        # end if

        return directory, profiles
    # end def create_directory_and_profiles
# end class AnalogKeysTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
