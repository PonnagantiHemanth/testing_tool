#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.gaming.feature_8101.profilemanagement
:brief: Validate HID++ 2.0 ``ProfileManagement`` feature
:author: YY Liu <yliu5@logitech.com>
:date: 2023/04/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from os.path import join

from pychannel.channelinterfaceclasses import LogitechProtocol
from pyhid.hiddata import OS
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagement
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.fkcprofileformat import DirectoryFile
from pylibrary.mcu.fkcprofileformat import FkcMainTable
from pylibrary.mcu.fkcprofileformat import Macro
from pylibrary.mcu.fkcprofileformat import Profile
from pylibrary.tools.hexlist import HexList
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.base.protocolmanagerutils import ProtocolManagerUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.fullkeycustomizationutils import FullKeyCustomizationTestUtils
from pytestbox.device.base.profilemanagementutils import ProfileManagementTestUtils
from pytestbox.shared.base.dfuutils import DfuTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ProfileManagementTestCase(DeviceBaseTestCase):
    """
    Validate ``ProfileManagement`` TestCases in Application mode
    """
    WAIT_ALL_KEY_RELEASE_EVENT_S = 0.05  # Wait for all keys release event in seconds

    # noinspection PyAttributeOutsideInit
    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()
        self.trigger_key = KEY_ID.BUTTON_1 if self.f.PRODUCT.F_IsMice else KEY_ID.KEYBOARD_A
        self.post_requisite_exit_ble_channel = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x8101 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_8101_index, self.feature_8101, _, _ = ProfileManagementTestUtils.HIDppHelper.get_parameters(self)

        self.config = self.f.PRODUCT.FEATURES.GAMING.PROFILE_MANAGEMENT
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites
        """
        with self.manage_post_requisite():
            # Reset the game mode emulator to its initial state before restoring NVS!
            if self.game_mode_emulator:
                self.game_mode_emulator.set_mode(activate_game_mode=False)
            # end if
        # end with

        with self.manage_post_requisite():
            # Be sure the full sequence was executed before quiting
            self.kosmos.sequencer.wait_end_of_sequence()
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

        with self.manage_post_requisite():
            if self.backup_dut_channel.protocol in LogitechProtocol.gaming_protocols():
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Exit USB channel")
                # ------------------------------------------------------------------------------------------------------
                # Leave from USB channel if the DUT is a gaming device, otherwise do nothing
                ProtocolManagerUtils.exit_usb_channel(self)
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_exit_ble_channel:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Exit BLE channel")
                # ------------------------------------------------------------------------------------------------------
                ProtocolManagerUtils.exit_ble_channel(self)
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_reload_nvs:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.NvsHelper.restore_nvs(self)
                self.post_requisite_reload_nvs = False
            # end if
        # end with

        super().tearDown()
    # end def tearDown

    @classmethod
    def create_profile_from_settings_and_update_profile_directory(
            cls, test_case, file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
            save_profile_in_nvs=False, save_directory_in_nvs=False, directory=None):
        """
        Create a default profile from test settings and create the profile directory

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param file_type_id: The file type id - OPTIONAL
        :type file_type_id: ``ProfileManagement.FileTypeId.X8101 | int``
        :param save_profile_in_nvs: Flag indicating if the created profile should be saved in the NVS - OPTIONAL
        :type save_profile_in_nvs: ``bool``
        :param save_directory_in_nvs: Flag indicating if the created  directory should be saved in the NVS - OPTIONAL
        :type save_directory_in_nvs: ``bool``
        :param directory: ``DirectoryFile`` instance - OPTIONAL
        :type directory: ``DirectoryFile | None``

        :return: The ``DirectoryFile`` and ``Profile`` instances
        :rtype: ``tuple[DirectoryFile, Profile]``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        if directory is None:
            directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=test_case)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case, "Create valid 0x8101 feature setting files")
        # --------------------------------------------------------------------------------------------------------------
        profile = ProfileManagementTestUtils.ProfileHelper.create_profile_from_settings(
            test_case, directory, file_type_id=file_type_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case, f"Write 0x8101 profile to NVS\n{profile}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=test_case, data=HexList(profile),
                                         store_in_nvs=save_profile_in_nvs,
                                         first_sector_id_lsb=profile.first_sector_id_lsb,
                                         crc_32=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case, f"Write 0x8101 directory to NVS\n{directory}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=test_case, data=HexList(directory),
                                         store_in_nvs=save_directory_in_nvs,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        return directory, profile
    # end def create_profile_from_settings_and_update_profile_directory

    @classmethod
    def create_onboard_profiles_from_settings_and_update_profile_directory(
            cls, test_case, save_profile_in_nvs=False, save_directory_in_nvs=False, directory=None):
        """
        Create a default profile from test settings and create the profile directory

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param save_profile_in_nvs: Flag indicating if the created profile should be saved in the NVS
        :type save_profile_in_nvs: ``bool``
        :param save_directory_in_nvs: Flag indicating if the created  directory should be saved in the NVS - OPTIONAL
        :type save_directory_in_nvs: ``bool``
        :param directory: ``DirectoryFile`` instance - OPTIONAL
        :type directory: ``DirectoryFile | None``

        :return: The ``DirectoryFile`` and ``Profile`` instances
        :rtype: ``tuple[DirectoryFile, list[Profile]]``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        if directory is None:
            directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=test_case)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case, "Create valid 0x8101 onboard profiles from settings")
        # --------------------------------------------------------------------------------------------------------------
        profiles = cls.create_onboard_profiles_and_save_in_nvs(test_case=test_case, directory=directory)

        for profile in profiles:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case, f"Write 0x8101 profile to NVS\n{profile}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=test_case, data=HexList(profile),
                                             store_in_nvs=save_profile_in_nvs,
                                             first_sector_id_lsb=profile.first_sector_id_lsb,
                                             crc_32=profile.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case, f"Write 0x8101 directory to NVS\n{directory}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=test_case, data=HexList(directory),
                                             store_in_nvs=save_directory_in_nvs,
                                             first_sector_id_lsb=directory.first_sector_id_lsb,
                                             crc_32=directory.crc_32)
        # end for

        return directory, profiles
    # end def create_onboard_profiles_from_settings_and_update_profile_directory

    @classmethod
    def create_main_tables_and_save_in_nvs(cls, test_case, directory, preset_remapped_keys, macro=None,
                                           os_variant=OS.WINDOWS, save_in_nvs=True):
        """
        Create FKC main tables by the preset and random remapped keys

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param directory: ``DirectoryFile`` instance
        :type directory: ``DirectoryFile``
        :param preset_remapped_keys: The preset remapped keys - OPTIONAL
        :type preset_remapped_keys: ``list[RemappedKey] | None``
        :param macro: Macro object - OPTIONAL
        :type macro: ``Macro | None``
        :param os_variant: OS variant - OPTIONAL
        :type os_variant: ``OS | str``
        :param save_in_nvs: Indicate to save main tables in NVS - OPTIONAL
        :type save_in_nvs: ``bool``

        :return: ``FkcMainTable`` instances for BASE, FN and G-SHIFT layers
        :rtype: ``list[FkcMainTable]``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case, "Create FKC main tables")
        # --------------------------------------------------------------------------------------------------------------
        main_tables = FullKeyCustomizationTestUtils.FkcTableHelper.create_main_tables(
            test_case=test_case, directory=directory,
            random_parameters=FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters(),
            macro=macro, preset_remapped_keys=preset_remapped_keys, os_variant=os_variant)

        if main_tables:
            for layer, main_table in enumerate(main_tables):
                if main_table.is_empty():
                    continue
                # end if
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(test_case, f"Write the FKC main table to NVS\n{main_table}")
                # ------------------------------------------------------------------------------------------------------
                ProfileManagementTestUtils.write(test_case=test_case, data=HexList(main_table),
                                                 store_in_nvs=save_in_nvs,
                                                 first_sector_id_lsb=main_table.first_sector_id_lsb,
                                                 crc_32=main_table.crc_32)
            # end for
        # end if

        return main_tables
    # end def create_main_tables_and_save_in_nvs

    @classmethod
    def create_macro_and_save_in_nvs(cls, test_case, directory, preset_macro_entries, save_in_nvs=True):
        """
        Create macro file by the preset macro entries

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param directory: ``DirectoryFile`` instance
        :type directory: ``DirectoryFile``
        :param preset_macro_entries: Preset macro entry list
        :type preset_macro_entries: ``list[PresetMacroEntry]``
        :param save_in_nvs: Indicate to save main tables in NVS
        :type save_in_nvs: ``bool``

        :return: ``Macro`` instance
        :rtype: ``Macro``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case, "Create macro file")
        # --------------------------------------------------------------------------------------------------------------
        macro = FullKeyCustomizationTestUtils.FkcTableHelper.create_macro(
            test_case=test_case, directory=directory, preset_macro_entries=preset_macro_entries)
        if macro and save_in_nvs:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, f"Write 0x1B05 macro file to NVS\n{macro}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=test_case, data=HexList(macro),
                                             store_in_nvs=True, first_sector_id_lsb=macro.first_sector_id_lsb,
                                             crc_32=macro.crc_32)
        # end if

        return macro
    # end def create_macro_and_save_in_nvs

    @classmethod
    def create_onboard_profiles_and_save_in_nvs(cls, test_case, directory, save_in_nvs=True):
        """
        Create the device supported number of onboard profiles

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param directory: ``DirectoryFile`` instance
        :type directory: ``DirectoryFile``
        :param save_in_nvs: Indicate to save onboard profiles in NVS - OPTIONAL
        :type save_in_nvs: ``bool``

        :return: The onboard profiles
        :rtype: ``list[Profile]``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case, "Test Loop: Loop over index in range("
                                      f"{test_case.f.PRODUCT.FEATURES.GAMING.PROFILE_MANAGEMENT.F_NumOnboardProfiles})")
        # --------------------------------------------------------------------------------------------------------------
        profiles = []
        for index in range(test_case.f.PRODUCT.FEATURES.GAMING.PROFILE_MANAGEMENT.F_NumOnboardProfiles):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case, f"Create a onboard profile with file_id={index} from a settings")
            # ----------------------------------------------------------------------------------------------------------
            profiles.append(ProfileManagementTestUtils.ProfileHelper.create_profile_from_settings(
                test_case, directory, file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE))
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        if save_in_nvs:
            for profile in profiles:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(test_case, f"Write 0x8101 profile to NVS\n{profile}")
                # ------------------------------------------------------------------------------------------------------
                ProfileManagementTestUtils.write(test_case=test_case, data=HexList(profile),
                                                 store_in_nvs=True,
                                                 first_sector_id_lsb=profile.first_sector_id_lsb,
                                                 crc_32=profile.crc_32)
            # end for
        # end if

        return profiles
    # end def create_onboard_profiles_and_save_in_nvs
# end class ProfileManagementTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
