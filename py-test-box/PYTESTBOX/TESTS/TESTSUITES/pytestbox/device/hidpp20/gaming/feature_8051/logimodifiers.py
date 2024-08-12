#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.gaming.feature_8051.logimodifiers
:brief: Validate HID++ 2.0 ``LogiModifiers`` feature
:author: Zane Lu <zlu@logitech.com>
:date: 2023/05/04
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import sample

from pyhid.hiddata import OS
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagement
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.fkcprofileformat import FkcMainTable
from pylibrary.mcu.fkcprofileformat import RemappedKey
from pylibrary.tools.hexlist import HexList
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.controllistutils import ControlListTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.fullkeycustomizationutils import FullKeyCustomizationTestUtils
from pytestbox.device.base.logimodifiersutils import LogiModifiersTestUtils
from pytestbox.device.base.profilemanagementutils import ProfileManagementTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LogiModifiersTestCase(DeviceBaseTestCase):
    """
    Validate ``LogiModifiers`` TestCases in Application mode
    """

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

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x8051 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_8051_index, self.feature_8051, _, _ = LogiModifiersTestUtils.HIDppHelper.get_parameters(self)

        self.config = self.f.PRODUCT.FEATURES.GAMING.LOGI_MODIFIERS

        self.locally_pressed_support = {
            "g_shift": self.config.F_GM_GShift,
            "fn": self.config.F_GM_Fn,
            "right_gui": self.config.F_GM_RightGui,
            "right_alt": self.config.F_GM_RightAlt,
            "right_shift": self.config.F_GM_RightShift,
            "right_ctrl": self.config.F_GM_RightCtrl,
            "left_gui": self.config.F_GM_LeftGui,
            "left_alt": self.config.F_GM_LeftAlt,
            "left_shift": self.config.F_GM_LeftShift,
            "left_ctrl": self.config.F_GM_LeftCtrl,
        }

        self.forceable_modifiers_support = {
            "g_shift": self.config.F_FM_GShift,
            "fn": self.config.F_FM_Fn,
        }
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites
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
        super().tearDown()
    # end def tearDown

    def get_random_non_modifier_keys(self, count):
        """
        Generate the random standard keys

        :param count: the number of the keys to generate
        :type count: ``int``

        :return: key_id and cidx list
        :rtype: ``list[dict]``
        """
        candidates = FullKeyCustomizationTestUtils.FkcTableHelper.KeyProvider.get_all_non_modifier_keys(test_case=self)
        elected_candidates = sample(population=candidates, k=count)

        targets = []
        for key_id in elected_candidates:
            cid_x = ControlListTestUtils.key_id_to_cidx(self, key_id=key_id)
            targets.append({"key_id": key_id, "cidx": cid_x})
        # end for
        return targets
    # end def get_random_non_modifier_keys

    def create_keys_mapping(self):
        """
        Create the random key mappings for modifier keys and standard keys

        :return: remapping keys information
        :rtype: ``dict``
        """
        # generate 21 random non-modifier keys
        # the (index 0 - 9) keys are used as modifier keys which are defined in FKC remapped keys (index 0 - 9)
        # the (index 10) key is used for FKC remapped keys (index 10, 11, 12)
        # the (index 11 - 20) keys are used for testing by test cases
        keys = self.get_random_non_modifier_keys(count=21)
        modifier_keys = {
            "fn": keys[0],
            "g_shift": keys[1],
            "left_ctrl": keys[2],
            "left_shift": keys[3],
            "left_alt": keys[4],
            "left_gui": keys[5],
            "right_ctrl": keys[6],
            "right_shift": keys[7],
            "right_alt": keys[8],
            "right_gui": keys[9],
        }

        for k, v in modifier_keys.items():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, msg=f"{k} is remapped to {v}.")
            # ----------------------------------------------------------------------------------------------------------
        # end for

        remapped_keys = [
            # fn key
            RemappedKey(action_type=RemappedKey.ActionType.VIRTUAL_MODIFIER,
                        trigger_key=modifier_keys["fn"]["key_id"],
                        action_key=KEY_ID.FN_KEY),
            # gshift key
            RemappedKey(action_type=RemappedKey.ActionType.VIRTUAL_MODIFIER,
                        trigger_key=modifier_keys["g_shift"]["key_id"],
                        action_key=KEY_ID.G_SHIFT),
            # right gui
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=modifier_keys["right_gui"]["key_id"],
                        action_key=KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION),
            # right alt
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=modifier_keys["right_alt"]["key_id"],
                        action_key=KEY_ID.KEYBOARD_RIGHT_ALT),
            # right shift
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=modifier_keys["right_shift"]["key_id"],
                        action_key=KEY_ID.KEYBOARD_RIGHT_SHIFT),
            # right control
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=modifier_keys["right_ctrl"]["key_id"],
                        action_key=KEY_ID.KEYBOARD_RIGHT_CONTROL),
            # left gui
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=modifier_keys["left_gui"]["key_id"],
                        action_key=KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION),
            # left alt
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=modifier_keys["left_alt"]["key_id"],
                        action_key=KEY_ID.KEYBOARD_LEFT_ALT),
            # left shift
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=modifier_keys["left_shift"]["key_id"],
                        action_key=KEY_ID.KEYBOARD_LEFT_SHIFT),
            # left control
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=modifier_keys["left_ctrl"]["key_id"],
                        action_key=KEY_ID.KEYBOARD_LEFT_CONTROL),
            # gshift + keys[10] -> key 'a'
            RemappedKey(layer=FkcMainTable.Layer.GSHIFT, action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=keys[10]["key_id"],
                        action_key=KEY_ID.KEYBOARD_A),
            # fn + keys[10] -> key 'a'
            RemappedKey(layer=FkcMainTable.Layer.FN, action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=keys[10]["key_id"],
                        action_key=KEY_ID.KEYBOARD_A),
            # keys[10] -> key 'b'
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=keys[10]["key_id"],
                        action_key=KEY_ID.KEYBOARD_B),

            # remapping modifiers in the gshift layer
            # right gui - gshift layer remapping
            RemappedKey(layer=FkcMainTable.Layer.GSHIFT, action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=modifier_keys["right_gui"]["key_id"],
                        action_key=KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION),
            # right alt - gshift layer remapping
            RemappedKey(layer=FkcMainTable.Layer.GSHIFT, action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=modifier_keys["right_alt"]["key_id"],
                        action_key=KEY_ID.KEYBOARD_RIGHT_ALT),
            # right shift - gshift layer remapping
            RemappedKey(layer=FkcMainTable.Layer.GSHIFT, action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=modifier_keys["right_shift"]["key_id"],
                        action_key=KEY_ID.KEYBOARD_RIGHT_SHIFT),
            # right control - gshift layer remapping
            RemappedKey(layer=FkcMainTable.Layer.GSHIFT, action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=modifier_keys["right_ctrl"]["key_id"],
                        action_key=KEY_ID.KEYBOARD_RIGHT_CONTROL),
            # left gui - gshift layer remapping
            RemappedKey(layer=FkcMainTable.Layer.GSHIFT, action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=modifier_keys["left_gui"]["key_id"],
                        action_key=KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION),
            # left alt - gshift layer remapping
            RemappedKey(layer=FkcMainTable.Layer.GSHIFT, action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=modifier_keys["left_alt"]["key_id"],
                        action_key=KEY_ID.KEYBOARD_LEFT_ALT),
            # left shift - gshift layer remapping
            RemappedKey(layer=FkcMainTable.Layer.GSHIFT, action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=modifier_keys["left_shift"]["key_id"],
                        action_key=KEY_ID.KEYBOARD_LEFT_SHIFT),
            # left control - gshift layer remapping
            RemappedKey(layer=FkcMainTable.Layer.GSHIFT, action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=modifier_keys["left_ctrl"]["key_id"],
                        action_key=KEY_ID.KEYBOARD_LEFT_CONTROL),

            # remapping modifiers in the fn layer
            # right gui - fn layer remapping
            RemappedKey(layer=FkcMainTable.Layer.FN, action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=modifier_keys["right_gui"]["key_id"],
                        action_key=KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION),
            # right alt - fn layer remapping
            RemappedKey(layer=FkcMainTable.Layer.FN, action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=modifier_keys["right_alt"]["key_id"],
                        action_key=KEY_ID.KEYBOARD_RIGHT_ALT),
            # right shift - fn layer remapping
            RemappedKey(layer=FkcMainTable.Layer.FN, action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=modifier_keys["right_shift"]["key_id"],
                        action_key=KEY_ID.KEYBOARD_RIGHT_SHIFT),
            # right control - fn layer remapping
            RemappedKey(layer=FkcMainTable.Layer.FN, action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=modifier_keys["right_ctrl"]["key_id"],
                        action_key=KEY_ID.KEYBOARD_RIGHT_CONTROL),
            # left gui - fn layer remapping
            RemappedKey(layer=FkcMainTable.Layer.FN, action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=modifier_keys["left_gui"]["key_id"],
                        action_key=KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION),
            # left alt - fn layer remapping
            RemappedKey(layer=FkcMainTable.Layer.FN, action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=modifier_keys["left_alt"]["key_id"],
                        action_key=KEY_ID.KEYBOARD_LEFT_ALT),
            # left shift - fn layer remapping
            RemappedKey(layer=FkcMainTable.Layer.FN, action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=modifier_keys["left_shift"]["key_id"],
                        action_key=KEY_ID.KEYBOARD_LEFT_SHIFT),
            # left control - fn layer remapping
            RemappedKey(layer=FkcMainTable.Layer.FN, action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=modifier_keys["left_ctrl"]["key_id"],
                        action_key=KEY_ID.KEYBOARD_LEFT_CONTROL),
        ]

        for remapped_key in remapped_keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, msg=f"{remapped_key}")
            # ----------------------------------------------------------------------------------------------------------
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, msg=f"gshift + {keys[10]} is remapped to KEY_ID.KEYBOARD_A.")
        LogHelper.log_info(self, msg=f"fn + {keys[10]} is remapped to KEY_ID.KEYBOARD_A.")
        LogHelper.log_info(self, msg=f"{keys[10]} is remapped to KEY_ID.KEYBOARD_B.")
        # --------------------------------------------------------------------------------------------------------------

        start_test_key_index = 11
        end_test_key_index = 21

        for k in keys[start_test_key_index:end_test_key_index]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, msg=f"{k} is a test key.")
            # ----------------------------------------------------------------------------------------------------------
        # end for

        return {
            "modifier_keys": modifier_keys,
            "remapped_keys": remapped_keys,
            "test_keys": keys[start_test_key_index:end_test_key_index]
        }
    # end def create_keys_mapping

    def create_remapping_in_nvs(self, preset_remapped_keys=None, preset_macro_entries=None, random_parameters=None,
                                profile_file_type=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                disabled_keys=None, notify_sw=False, os_variant=OS.WINDOWS):
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
        :param disabled_keys: The disabled key settings in profile
        :type disabled_keys: ``HexList``
        :param notify_sw: Combine NotifySW in the action_bitfield - OPTIONAL
        :type notify_sw: ``bool``
        :param os_variant: OS variant - OPTIONAL
        :type os_variant: ``OS | str``

        :return: A list of ``RemappedKey`` instance and profiles
        :rtype: ``list[RemappedKey] | tuple[list[RemappedKey], list[Profile]]``

        :raise ``AssertionError``: If profile_count < 1 in the random parameters
        """
        random_parameters = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters() \
            if random_parameters is None else random_parameters
        assert random_parameters.profile_count > 0

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create Profile Tables")
        # --------------------------------------------------------------------------------------------------------------
        profiles = []
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
        LogHelper.log_step(self, "Create FKC modifier and main tables")
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
                LogHelper.log_step(self, f"Write 0x1B05 {FkcMainTable.Layer(layer)!s} main table to NVS\n{main_table}")
                # ------------------------------------------------------------------------------------------------------
                ProfileManagementTestUtils.write(test_case=self, data=HexList(main_table), store_in_nvs=True,
                                                 first_sector_id_lsb=main_table.first_sector_id_lsb,
                                                 crc_32=main_table.crc_32)
            # end for
        # end if
        for profile in profiles:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Write 0x8101 profile to NVS\n{profiles}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(profile), store_in_nvs=True,
                                             first_sector_id_lsb=profile.first_sector_id_lsb, crc_32=profile.crc_32)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write 0x8101 directory to NVS\n{directory}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb, crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure 0x8101 in NVS to take the changes")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(
            test_case=self, feature_id=ProfileManagement.FEATURE_ID,
            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
            file_id=ProfileManagement.Partition.FileId.NVS | profiles[0].file_id_lsb,
            count=len(HexList(profiles[0])),
            crc_32=profiles[0].crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable FKC by the 0x1B05.get_set_enabled() command")
        # --------------------------------------------------------------------------------------------------------------
        rsp = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            test_case=self, set_toggle_keys_enabled=False, set_fkc_enabled=True, fkc_enabled=1)

        self.assertEqual(expected=1, obtained=rsp.fkc_state.fkc_enabled,
                         msg="FKC shall be enabled!")
    # end def create_remapping_in_nvs

    def init_fkc_profile(self):
        """
        Init a FCK profile via x8101 and enable FKC

        :return: remapping keys information
        :rtype: ``dict``
        """
        remapping_keys_info = self.create_keys_mapping()
        remapped_keys = remapping_keys_info["remapped_keys"]

        self.create_remapping_in_nvs(preset_remapped_keys=remapped_keys)

        return remapping_keys_info
    # end def init_fkc_profile
# end class LogiModifiersTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
