#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.fkc.fkc
:brief: Hid Keyboard FKC test case
:author: Fred Chen <fchen7@logitech.com>
:date: 2023/03/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddata import OS
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.fullkeycustomization import FullKeyCustomization
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagement
from pylibrary.mcu.fkcprofileformat import FkcMainTable
from pylibrary.mcu.fkcprofileformat import Profile
from pylibrary.mcu.fkcprofileformat import RemappedKey
from pylibrary.mcu.profileformat import PresetMacroEntry
from pylibrary.tools.hexlist import HexList
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.controllistutils import ControlListTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.fullkeycustomizationutils import FullKeyCustomizationTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.base.profilemanagementutils import ProfileManagementTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class FKCTestCase(BaseTestCase):
    """
    Validate Keyboard Full Key Customization
    """
    SEQUENCER_TIMEOUT_S = 60

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()
        self.post_requisite_refresh_cid_list = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
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
            if self.post_requisite_reload_nvs:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.NvsHelper.restore_nvs(self)
                self.post_requisite_reload_nvs = False
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_refresh_cid_list:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Refresh CID List and restore key layout")
                # ------------------------------------------------------------------------------------------------------
                ControlListTestUtils.refresh_cid_list(test_case=self)
                self.post_requisite_refresh_cid_list = False
                self.button_stimuli_emulator.select_layout()
            # end if
        # end with

        super().tearDown()
    # end def tearDown

    def create_remapping_in_ram(self, preset_remapped_keys=None, random_parameters=None, notify_sw=False,
                                os_variant=OS.WINDOWS):
        """
        Create and activate FKC remapping in RAM buffer

        :param preset_remapped_keys: The preset remapped keys - OPTIONAL
        :type preset_remapped_keys: ``list[RemappedKey] | None``
        :param random_parameters: Random parameters - OPTIONAL
        :type random_parameters: ``FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters | None``
        :param notify_sw: Flag indicating to set NotifySW bit in the action_bitfield - OPTIONAL
        :type notify_sw: ``bool``
        :param os_variant: OS variant - OPTIONAL
        :type os_variant: ``OS | str``

        :return: A list of ``RemappedKey`` instance
        :rtype: ``list[RemappedKey]``
        """
        random_parameters = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters() \
            if random_parameters is None else random_parameters

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        preset_remapped_key_count = 0 if not preset_remapped_keys else len(preset_remapped_keys)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create FKC main tables\n"
                                 f"Preset remapped keys: {preset_remapped_key_count}\n{random_parameters}")
        # --------------------------------------------------------------------------------------------------------------
        main_tables = FullKeyCustomizationTestUtils.FkcTableHelper.create_main_tables(
            test_case=self, directory=directory, random_parameters=random_parameters,
            preset_remapped_keys=preset_remapped_keys, notify_sw=notify_sw, os_variant=os_variant)

        configured_fkc_main_table = False
        for layer, main_table in enumerate(main_tables):
            if main_table.is_empty():
                continue
            # end if
            assert configured_fkc_main_table is False, 'Have multiple FKC main tables! ' \
                                                       'Shall use create_remapping_in_nvs()'
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Write the FKC main table\n{main_table}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(main_table))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Configure 0x1B05 in RAM to take the changes")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.activate(
                test_case=self, feature_id=FullKeyCustomization.FEATURE_ID,
                file_type_id=FkcMainTable.Layer.to_file_type_id(layer),
                file_id=ProfileManagement.Partition.FileId.RAM,
                count=len(HexList(main_table)),
                crc_32=main_table.crc_32)
            configured_fkc_main_table = True
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Enable FKC by the default toggle hot key (If the FKC enabled by default, ignore the step)")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)
        FullKeyCustomizationTestUtils.set_fkc_state_by_toggle_key(test_case=self, enable=True)

        remapped_keys = FullKeyCustomizationTestUtils.FkcTableHelper.convert_to_remapped_keys(
            test_case=self, fkc_main_tables=main_tables, os_variant=os_variant)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_data(self, f"{remapped_keys})")
        # --------------------------------------------------------------------------------------------------------------

        return remapped_keys
    # end def create_remapping_in_ram

    def create_remapping_in_nvs(self, preset_remapped_keys=None, preset_macro_entries=None, random_parameters=None,
                                profile_file_type=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                disabled_keys=None, notify_sw=False, os_variant=OS.WINDOWS):
        """
        Create and activate FKC remapping in NVS

        :param preset_remapped_keys: The preset remapped keys - OPTIONAL
        :type preset_remapped_keys: ``list[RemappedKey] | None``
        :param preset_macro_entries: Macro entry list - OPTIONAL
        :type preset_macro_entries: ``list[PresetMacroEntry] | None``
        :param random_parameters: Random parameters - OPTIONAL
        :type random_parameters: ``FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters | None``
        :param profile_file_type: The profile file type - OPTIONAL
        :type profile_file_type: ``ProfileManagement.FileTypeId.X8101``
        :param disabled_keys: The disabled key setting in profile - OPTIONAL
        :type disabled_keys: ``HexList | None``
        :param notify_sw: Flag indicating to set NotifySW bit in the action_bitfield - OPTIONAL
        :type notify_sw: ``bool``
        :param os_variant: OS variant - OPTIONAL
        :type os_variant: ``OS | str``

        :return: A list of ``RemappedKey`` instance and optionally profiles
        :rtype: ``list[RemappedKey] | tuple[list[RemappedKey], list[Profile]]``

        :raise ``AssertionError``: If profile_count < 1 in the random parameters
        """
        random_parameters = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters() \
            if random_parameters is None else random_parameters
        assert random_parameters.profile_count >= 1, 'Profile count shall be >= 1'

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create Profile Table")
        # --------------------------------------------------------------------------------------------------------------
        profiles = []
        # Create all supported onboard profiles
        for profile_index in range(random_parameters.profile_count):
            profile = ProfileManagementTestUtils.ProfileHelper.create_profile_from_oob(
                test_case=self, directory=directory, file_type_id=profile_file_type)
            if disabled_keys:
                profile.update_tag_content(
                    directory=directory,
                    tag_content_dict={ProfileManagement.Tag.X4523_CIDX_BITMAP: disabled_keys})
            # end if
            profiles.append(profile)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create Macro")
        # --------------------------------------------------------------------------------------------------------------
        macro = None
        if ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_MACRO in list(profiles[0].tag_fields.keys()):
            if preset_macro_entries:
                macro = FullKeyCustomizationTestUtils.FkcTableHelper.create_macro(
                    test_case=self, directory=directory, preset_macro_entries=preset_macro_entries)
            elif random_parameters.macro.entry_count:
                macro = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper.generate_macro(
                    test_case=self, directory=directory, random_parameters=random_parameters, os_variant=os_variant)
            # end if
            if macro:
                for profile in profiles:
                    profile.update_tag_content(
                        directory=directory,
                        tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_MACRO: macro.file_id_lsb})
                # end for
            # end if
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create FKC main tables")
        # --------------------------------------------------------------------------------------------------------------
        main_tables = None
        if ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_BASE in list(profiles[0].tag_fields.keys()):
            fixed_remapped_key_count = 0 if not preset_remapped_keys else len(preset_remapped_keys)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Fixed remapped keys: {fixed_remapped_key_count}\n{random_parameters}")
            # ----------------------------------------------------------------------------------------------------------
            main_tables = FullKeyCustomizationTestUtils.FkcTableHelper.create_main_tables(
                test_case=self, directory=directory, random_parameters=random_parameters,
                preset_remapped_keys=preset_remapped_keys, macro=macro, notify_sw=notify_sw, os_variant=os_variant)

            for profile in profiles:
                for layer, main_table in enumerate(main_tables):
                    if main_table.is_empty():
                        continue
                    # end if
                    profile.update_tag_content(
                        directory=directory,
                        tag_content_dict={FkcMainTable.Layer.to_profile_tag(layer=layer): main_table.file_id_lsb})
                # end for
            # end for
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Write tables to NVS")
        # --------------------------------------------------------------------------------------------------------------
        for profile in profiles:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Write 0x8101 profile to NVS\n{profile}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(profile), store_in_nvs=True,
                                             first_sector_id_lsb=profile.first_sector_id_lsb, crc_32=profile.crc_32)
        # end for
        if macro:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Write 0x1B05 macro table to NVS\n{macro}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(macro), store_in_nvs=True,
                                             first_sector_id_lsb=macro.first_sector_id_lsb, crc_32=macro.crc_32)
        # end if
        if main_tables:
            for layer, main_table in enumerate(main_tables):
                if main_table.is_empty():
                    continue
                # end if
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Write 0x1B05 {FkcMainTable.Layer(layer)!r} main table to NVS\n{main_table}")
                # ------------------------------------------------------------------------------------------------------
                ProfileManagementTestUtils.write(test_case=self, data=HexList(main_table), store_in_nvs=True,
                                                 first_sector_id_lsb=main_table.first_sector_id_lsb,
                                                 crc_32=main_table.crc_32)
            # end for
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write 0x8101 directory to NVS\n{directory}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb, crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure 0x8101 in NVS to take the changes")
        # --------------------------------------------------------------------------------------------------------------
        activate_profile = profiles[0]
        ProfileManagementTestUtils.activate(
            test_case=self, feature_id=ProfileManagement.FEATURE_ID,
            file_type_id=profile_file_type,
            file_id=ProfileManagement.Partition.FileId.NVS | activate_profile.file_id_lsb,
            count=len(HexList(activate_profile)),
            crc_32=activate_profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Enable FKC by the default toggle hot key (If the FKC enabled by default, ignore the step)")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)
        FullKeyCustomizationTestUtils.set_fkc_state_by_toggle_key(test_case=self, enable=True)

        remapped_keys = FullKeyCustomizationTestUtils.FkcTableHelper.convert_to_remapped_keys(
            test_case=self, fkc_main_tables=main_tables, macro=macro, os_variant=os_variant)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_data(self, f"{remapped_keys})")
        # --------------------------------------------------------------------------------------------------------------

        if random_parameters.profile_count == 1:
            return remapped_keys
        else:
            return remapped_keys, profiles
        # end if
    # end def create_remapping_in_nvs

    def build_key_test_sequence(self, remapped_keys, fn_key=None, gshift_key=None, block=False):
        """
        Build the remapped key test sequence

        :param remapped_keys: Remapped key list
        :type remapped_keys: ``list[RemappedKey]``
        :param fn_key: The combined Fn key id - OPTIONAL
        :type fn_key: ``KEY_ID | None``
        :param gshift_key: The combined GShift key id - OPTIONAL
        :type gshift_key: ``KEY_ID | None``
        :param block: Wait until the SEQUENCER state changes from RUNNING to IDLE or ERROR. - OPTIONAL
        :type block: ``bool``
        """
        self.kosmos.sequencer.offline_mode = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Build the key remapping test sequence")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        for remapped_key in remapped_keys:
            FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.build_key_sequence(test_case=self,
                                                                                remapped_key=remapped_key,
                                                                                fn_key=fn_key,
                                                                                gshift_key=gshift_key)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos Board
        self.kosmos.sequencer.play_sequence(block=block, timeout=self.SEQUENCER_TIMEOUT_S)
    # end def build_key_test_sequence

    def validate_result_for_test_sequence(self, remapped_keys):
        """
        Validate results for remapped keys

        :param remapped_keys: Remapped key list
        :type remapped_keys: ``list[RemappedKey]``
        """
        for remapped_key in remapped_keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check received HID report for the remapped key: {remapped_key}")
            # ----------------------------------------------------------------------------------------------------------
            FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(test_case=self, remapped_key=remapped_key)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')
    # end def validate_result_for_test_sequence

    def build_key_test_sequence_and_validate_result(self, remapped_keys, fn_key=None, gshift_key=None, block=False):
        """
        Build the remapped key test sequence then validate results

        :param remapped_keys: Remapped key list
        :type remapped_keys: ``list[RemappedKey]``
        :param fn_key: The combined Fn key id - OPTIONAL
        :type fn_key: ``KEY_ID | None``
        :param gshift_key: The combined GShift key id - OPTIONAL
        :type gshift_key: ``KEY_ID | None``
        :param block: Wait until the SEQUENCER state changes from RUNNING to IDLE or ERROR. - OPTIONAL
        :type block: ``bool``
        """
        self.build_key_test_sequence(remapped_keys=remapped_keys, fn_key=fn_key, gshift_key=gshift_key, block=block)
        self.validate_result_for_test_sequence(remapped_keys=remapped_keys)
    # end def build_key_test_sequence_and_validate_result
# end class FKCTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
