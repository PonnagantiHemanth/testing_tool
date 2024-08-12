#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1b05.fullkeycustomization
:brief: Validate HID++ 2.0 ``FullKeyCustomization`` feature
:author: Masan Xu <mxu11@logitech.com>
:date: 2023/05/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddata import OS
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.fullkeycustomization import FullKeyCustomization
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagement
from pylibrary.mcu.fkcprofileformat import FkcMainTable
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.controllistutils import ControlListTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.fullkeycustomizationutils import FullKeyCustomizationTestUtils
from pytestbox.device.base.profilemanagementutils import ProfileManagementTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class FullKeyCustomizationTestCase(DeviceBaseTestCase):
    """
    Validate ``FullKeyCustomization`` TestCases in Application mode
    """
    FKC_WAKE_UP_DELAY = 1  # The delay of FKC processing when waking up the device (sec)

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x1B05 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1b05_index, self.feature_1b05, _, _ = FullKeyCustomizationTestUtils.HIDppHelper.get_parameters(
            test_case=self)

        self.config = self.f.PRODUCT.FEATURES.COMMON.FULL_KEY_CUSTOMIZATION
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites
        """
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
        super().tearDown()
    # end def tearDown

    def create_remapping_in_ram(self, preset_remapped_keys=None, random_parameters=None, notify_sw=False,
                                os_variant=OS.WINDOWS, invalid_crc=False,
                                enable_fkc=FullKeyCustomization.FKCStatus.ENABLE):
        """
        Create and activate FKC remapping in RAM buffer

        :param preset_remapped_keys: The fixed settings of remapped keys - OPTIONAL
        :type preset_remapped_keys: ``list[RemappedKey] | None``
        :param random_parameters: Random parameters - OPTIONAL
        :type random_parameters: ``FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters | None``
        :param notify_sw: Combine NotifySW in the action_bitfield - OPTIONAL
        :type notify_sw: ``bool``
        :param os_variant: OS variant - OPTIONAL
        :type os_variant: ``OS | str``
        :param invalid_crc: The flag indicates whether we should assign an invalid CRC as mandatory when
                            configuring - OPTIONAL
        :type invalid_crc: ``bool``
        :param enable_fkc: Enable FKC in the end - OPTIONAL
        :type enable_fkc: ``FullKeyCustomization.FKCStatus | bool``

        :return: A list of ``RemappedKey`` instance
        :rtype: ``list[RemappedKey]``
        """
        random_parameters = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters() \
            if random_parameters is None else random_parameters

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        preset_remapped_key_count = 0 if not preset_remapped_keys else len(preset_remapped_keys)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Create FKC main table\n"
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
            LogHelper.log_info(self, f"Write the FKC main table\n{main_table}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(main_table))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Configure 0x1B05 in RAM to take the changes")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.activate(
                test_case=self, feature_id=FullKeyCustomization.FEATURE_ID,
                file_type_id=FkcMainTable.Layer.to_file_type_id(layer),
                file_id=ProfileManagement.Partition.FileId.RAM,
                count=len(HexList(main_table)),
                crc_32=HexList(Numeral(0, byteCount=4)) if invalid_crc else main_table.crc_32)
            configured_fkc_main_table = True
        # end for

        if enable_fkc:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                self, "Enable FKC by the default toggle hot key (If the FKC enabled by default, ignore the step)")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)
            FullKeyCustomizationTestUtils.set_fkc_state_by_toggle_key(test_case=self, enable=True)
        # end if

        preset_remapped_keys = FullKeyCustomizationTestUtils.FkcTableHelper.convert_to_remapped_keys(
            test_case=self, fkc_main_tables=main_tables, os_variant=os_variant)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"remapped_keys: {preset_remapped_keys}")
        # --------------------------------------------------------------------------------------------------------------
        return preset_remapped_keys
    # end def create_remapping_in_ram

    def create_remapping_in_nvs(self, preset_remapped_keys=None, preset_macro_entries=None, random_parameters=None,
                                profile_file_type=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                disabled_keys=None, notify_sw=False, os_variant=OS.WINDOWS,
                                enable_fkc=FullKeyCustomization.FKCStatus.ENABLE):
        """
        Create and activate FKC remapping in NVS

        :param preset_remapped_keys: The preset remapped keys - OPTIONAL
        :type preset_remapped_keys: ``list[RemappedKey] | None``
        :param preset_macro_entries: Macro entry list - OPTIONAL
        :type preset_macro_entries: ``list[PresetMacroEntry]``
        :param random_parameters: Random parameters - OPTIONAL
        :type random_parameters: ``FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters | None``
        :param profile_file_type: The profile file type - OPTIONAL
        :type profile_file_type: ``ProfileManagement.FileTypeId.X8101 | int``
        :param disabled_keys: The disabled key settings in profile - OPTIONAL
        :type disabled_keys: ``HexList``
        :param notify_sw: Combine NotifySW in the action_bitfield - OPTIONAL
        :type notify_sw: ``bool``
        :param os_variant: OS variant - OPTIONAL
        :type os_variant: ``OS | str``
        :param enable_fkc: Enable FKC in the end - OPTIONAL
        :type enable_fkc: ``FullKeyCustomization.FKCStatus | bool``

        :return: A list of ``RemappedKey`` instance and profiles
        :rtype: ``list[RemappedKey] | tuple[list[RemappedKey], list[Profile]]``

        :raise ``AssertionError``: If profile_count < 1 in the random parameters
        """
        random_parameters = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters() \
            if random_parameters is None else random_parameters

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Create Profile Table")
        # --------------------------------------------------------------------------------------------------------------
        profile = None
        profiles = []
        assert random_parameters.profile_count > 0
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
        LogHelper.log_info(self, "Create Macro")
        # --------------------------------------------------------------------------------------------------------------
        macro = None
        if ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_MACRO in list(profiles[0].tag_fields.keys()):
            if preset_macro_entries:
                macro = FullKeyCustomizationTestUtils.FkcTableHelper.create_macro(
                    test_case=self, directory=directory, preset_macro_entries=preset_macro_entries)
            elif random_parameters.macro.entry_count:
                macro = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper.generate_macro(
                    test_case=self, directory=directory, random_parameters=random_parameters, os_variant=os_variant,
                    raise_buffer_overflow=False)
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
        LogHelper.log_info(self, "Create FKC modifier and main table")
        # --------------------------------------------------------------------------------------------------------------
        main_tables = None
        if ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_BASE in list(profile.tag_fields.keys()):
            fixed_remapped_key_count = 0 if not preset_remapped_keys else len(preset_remapped_keys)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Fixed remapped keys: {fixed_remapped_key_count}\n{random_parameters}")
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
        LogHelper.log_info(self, "Write tables to NVS")
        # --------------------------------------------------------------------------------------------------------------
        if macro:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Write 0x1B05 macro table to NVS\n{macro}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(macro), store_in_nvs=True,
                                             first_sector_id_lsb=macro.first_sector_id_lsb, crc_32=macro.crc_32,
                                             raise_buffer_exception=False)
        # end if
        if main_tables:
            for layer, main_table in enumerate(main_tables):
                if main_table.is_empty():
                    continue
                # end if
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"Write 0x1B05 {FkcMainTable.Layer(layer)!s} main table to NVS\n{main_table}")
                # ------------------------------------------------------------------------------------------------------
                ProfileManagementTestUtils.write(test_case=self, data=HexList(main_table), store_in_nvs=True,
                                                 first_sector_id_lsb=main_table.first_sector_id_lsb,
                                                 crc_32=main_table.crc_32)
            # end for
        # end if
        for profile in profiles:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Write 0x8101 profile to NVS\n{profiles}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(profile), store_in_nvs=True,
                                             first_sector_id_lsb=profile.first_sector_id_lsb, crc_32=profile.crc_32)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Write 0x8101 directory to NVS\n{directory}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb, crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Configure 0x8101 in NVS to take the changes")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(
            test_case=self, feature_id=ProfileManagement.FEATURE_ID,
            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
            file_id=ProfileManagement.Partition.FileId.NVS | profiles[0].file_id_lsb,
            count=len(HexList(profiles[0])),
            crc_32=profiles[0].crc_32)

        if enable_fkc:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                self, "Enable FKC by the default toggle hot key (If the FKC enabled by default, ignore the step)")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)
            FullKeyCustomizationTestUtils.set_fkc_state_by_toggle_key(test_case=self, enable=True)
        # end if

        remapped_keys = FullKeyCustomizationTestUtils.FkcTableHelper.convert_to_remapped_keys(
            test_case=self, fkc_main_tables=main_tables, macro=macro, os_variant=os_variant)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"remapped_keys: {remapped_keys}")
        # --------------------------------------------------------------------------------------------------------------

        if random_parameters.profile_count == 1:
            return remapped_keys
        else:
            return remapped_keys, profiles
        # end if
    # end def create_remapping_in_nvs

    def perform_fkc_toggle_hotkeys(self, fkc_status, toggle_key_index=0):
        """
        Emulate FKC toggle hotkeys to enable/disable FKC

        :param fkc_status: Indicate the expected FKC status after toggling
        :type fkc_status: ``FullKeyCustomization.FKCStatus``
        :param toggle_key_index: The toggle key index (0 ~ 7) - OPTIONAL
        :type toggle_key_index: ``int``
        """
        toggle_key_setting = getattr(self.f.PRODUCT.FEATURES.COMMON.FULL_KEY_CUSTOMIZATION,
                                     f'F_ToggleKey{toggle_key_index}Cidx')

        toggle_key_1 = ControlListTestUtils.cidx_to_key_id(test_case=self,
                                                           cid_index=to_int(toggle_key_setting[0]))
        toggle_key_2 = ControlListTestUtils.cidx_to_key_id(test_case=self,
                                                           cid_index=to_int(toggle_key_setting[1]))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Emulate keystrokes on FKC_toggle_hotkey[{toggle_key_index}] to "
                                 f"{'enable' if fkc_status else 'disable'} FKC")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[toggle_key_1, toggle_key_2], delay=0.05)
        self.button_stimuli_emulator.multiple_keys_release(key_ids=[toggle_key_2, toggle_key_1], delay=0.05)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Check enableDisableEvent with enabled={fkc_status} and failure=0")
        # --------------------------------------------------------------------------------------------------------------
        enable_disable_event = FullKeyCustomizationTestUtils.HIDppHelper.enable_disable_event(test_case=self)
        fkc_failure_enabled_checker = FullKeyCustomizationTestUtils.FkcFailureEnabledStateChecker
        fkc_failure_enabled_map = fkc_failure_enabled_checker.get_default_check_map(self)
        fkc_failure_enabled_map['enabled'] = (fkc_failure_enabled_checker.check_enabled, fkc_status)

        checker = FullKeyCustomizationTestUtils.EnableDisableEventChecker
        check_map = checker.get_default_check_map(self)
        check_map['fkc_failure_enabled_state'] = (checker.check_fkc_failure_enabled_state, fkc_failure_enabled_map)
        checker.check_fields(self, enable_disable_event, self.feature_1b05.enable_disable_event_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Empty HID queues")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queues(test_case=self)
    # end def perform_fkc_toggle_hotkeys
# end class FullKeyCustomizationTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
