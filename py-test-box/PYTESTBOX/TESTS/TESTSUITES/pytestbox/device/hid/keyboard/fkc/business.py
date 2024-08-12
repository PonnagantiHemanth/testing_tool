#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.fkc.business
:brief: Hid Keyboard FKC business test suite
:author: Fred Chen <fchen7@logitech.com>
:date: 2023/03/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from copy import deepcopy
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagement
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.fkcprofileformat import FkcMainTable
from pylibrary.mcu.fkcprofileformat import RemappedKey
from pylibrary.mcu.profileformat import MacroEndCommand
from pylibrary.mcu.profileformat import PresetMacroEntry
from pylibrary.mcu.profileformat import StandardKeyCommand
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.fullkeycustomizationutils import FullKeyCustomizationTestUtils
from pytestbox.device.base.logimodifiersutils import LogiModifiersTestUtils
from pytestbox.device.base.profilemanagementutils import ProfileManagementTestUtils
from pytestbox.device.hid.keyboard.fkc.fkc import FKCTestCase


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Fred Chen"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class FKCBusinessTestCase(FKCTestCase):
    """
    Validate Keyboard FKC business TestCases
    """

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Business', 'SmokeTests')
    @services('KeyMatrix')
    def test_trigger_to_fn_remapping(self):
        """
        [Special Remapping]
        Select 3 customizable keys (exclude modifier keys). For each selected key, remap it to Fn key.
        Add below remappings to test it works as expected.

        Remapping: [Trigger -> Fn]
        Trigger1 -> Fn
        Trigger2 -> Fn
        Trigger3 -> Fn
        Fn + Trigger4 -> Key1 (Exclude the remappings as like FKC toggle hotkeys or immersive lighting hotkeys)
        Fn + 1M + Trigger5 -> Key2
        Fn + 2M + Trigger6 -> Key3
        (Select 6 triggers and 3 keys randomly.)
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        trigger_1 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY)
        trigger_2 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY, excluded_keys=[trigger_1])
        trigger_3 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY, excluded_keys=[trigger_1, trigger_2])
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.VIRTUAL_MODIFIER,
                        trigger_key=trigger_1,
                        action_key=KEY_ID.FN_KEY),
            RemappedKey(action_type=RemappedKey.ActionType.VIRTUAL_MODIFIER,
                        trigger_key=trigger_2,
                        action_key=KEY_ID.FN_KEY),
            RemappedKey(action_type=RemappedKey.ActionType.VIRTUAL_MODIFIER,
                        trigger_key=trigger_3,
                        action_key=KEY_ID.FN_KEY),
            RemappedKey(layer=FkcMainTable.Layer.FN, action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
                        action_key=RemappedKey.RandomKey.STANDARD_KEY),
            RemappedKey(layer=FkcMainTable.Layer.FN, action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_modifier_keys=[RemappedKey.RandomKey.MODIFIER_KEY],
                        trigger_key=RemappedKey.RandomKey.NON_MODIFIER_KEY,
                        action_key=RemappedKey.RandomKey.STANDARD_KEY),
            RemappedKey(layer=FkcMainTable.Layer.FN, action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_modifier_keys=[RemappedKey.RandomKey.MODIFIER_KEY, RemappedKey.RandomKey.MODIFIER_KEY],
                        trigger_key=RemappedKey.RandomKey.NON_MODIFIER_KEY,
                        action_key=RemappedKey.RandomKey.STANDARD_KEY),
        ]
        remapped_keys = self.create_remapping_in_nvs(preset_remapped_keys=preset_remapped_keys)

        # Send button stimuli and check results
        fn_layer_remapped_keys = [key for key in remapped_keys if key.layer == FkcMainTable.Layer.FN]
        self.build_key_test_sequence_and_validate_result(remapped_keys=fn_layer_remapped_keys,
                                                         fn_key=trigger_1, block=True)
        self.build_key_test_sequence_and_validate_result(remapped_keys=fn_layer_remapped_keys,
                                                         fn_key=trigger_2, block=True)
        self.build_key_test_sequence_and_validate_result(remapped_keys=fn_layer_remapped_keys,
                                                         fn_key=trigger_3, block=True)

        self.testCaseChecked("BUS_FKC_0001", _AUTHOR)
    # end def test_trigger_to_fn_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Business')
    @services('KeyMatrix')
    def test_trigger_to_gshift_remapping(self):
        """
        [Special Remapping]
        Select 3 customizable keys (exclude modifier keys). For each selected key, remap it to GShift key.
        Add below remappings to test it works as expected.

        Remapping: [Trigger -> GShift]
        Trigger1 -> GShift
        Trigger2 -> GShift
        Trigger3 -> GShift
        GShift + Trigger4 -> Key1
        GShift + 1M + Trigger5 -> Key2
        GShift + 2M + Trigger6 -> Key3
        (Select 6 triggers and 3 keys randomly.)
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        triggers = []
        for _ in range(6):
            trigger = random_generation_helper.get_random_trigger_key(
                test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY, excluded_keys=triggers)
            triggers.append(trigger)
        # end for
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.VIRTUAL_MODIFIER,
                        trigger_key=triggers[0], action_key=KEY_ID.G_SHIFT),
            RemappedKey(action_type=RemappedKey.ActionType.VIRTUAL_MODIFIER,
                        trigger_key=triggers[1], action_key=KEY_ID.G_SHIFT),
            RemappedKey(action_type=RemappedKey.ActionType.VIRTUAL_MODIFIER,
                        trigger_key=triggers[2], action_key=KEY_ID.G_SHIFT),
            RemappedKey(layer=FkcMainTable.Layer.GSHIFT, action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=triggers[3],
                        action_key=RemappedKey.RandomKey.STANDARD_KEY),
            RemappedKey(layer=FkcMainTable.Layer.GSHIFT, action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_modifier_keys=[RemappedKey.RandomKey.MODIFIER_KEY],
                        trigger_key=triggers[4],
                        action_key=RemappedKey.RandomKey.STANDARD_KEY),
            RemappedKey(layer=FkcMainTable.Layer.GSHIFT, action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_modifier_keys=[RemappedKey.RandomKey.MODIFIER_KEY, RemappedKey.RandomKey.MODIFIER_KEY],
                        trigger_key=triggers[5],
                        action_key=RemappedKey.RandomKey.STANDARD_KEY),
        ]
        remapped_keys = self.create_remapping_in_nvs(preset_remapped_keys=preset_remapped_keys)

        # Send button stimuli and check results
        gshift_layer_remapped_keys = [key for key in remapped_keys if key.layer == FkcMainTable.Layer.GSHIFT]
        self.build_key_test_sequence_and_validate_result(remapped_keys=gshift_layer_remapped_keys,
                                                         gshift_key=triggers[0], block=True)
        self.build_key_test_sequence_and_validate_result(remapped_keys=gshift_layer_remapped_keys,
                                                         gshift_key=triggers[1], block=True)
        self.build_key_test_sequence_and_validate_result(remapped_keys=gshift_layer_remapped_keys,
                                                         gshift_key=triggers[2], block=True)

        self.testCaseChecked("BUS_FKC_0002", _AUTHOR)
    # end def test_trigger_to_gshift_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Business')
    @services('SimultaneousKeystrokes')
    def test_trigger_to_modifier_remapping(self):
        """
        [Special Remapping]
        Select 8 customizable keys (exclude modifier keys) to remap to modifier keys separately.
        Add below remappings to test it works as expected.

        Remapping: [Trigger -> Modifier]
        Trigger1 -> L-Ctrl
        Trigger2 -> L-Shift
        Trigger3 -> L-Alt
        Trigger4 -> L-GUI
        Trigger5 -> R-Ctrl
        Trigger6 -> R-Shift
        Trigger7 -> R-Alt
        Trigger8 -> R-GUI
        L-Ctrl + Trigger9 -> Key1
        L-Shift + Trigger10 -> Key2
        L-Alt + Trigger11 -> Key3
        L-GUI + Trigger12 -> Key4
        R-Ctrl + Trigger13 -> Key5
        R-Shift + Trigger14 -> Key6
        R-Alt + Trigger15 -> Key7
        R-GUI + Trigger16 -> Key8
        (Select 16 triggers and 8 keys randomly.)

        :raise ``ValueError``: Unsupported modifier key id
        """
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        triggers = []
        for _ in range(16):
            trigger = random_generation_helper.get_random_trigger_key(
                test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY, excluded_keys=triggers)
            triggers.append(trigger)
        # end for
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD, trigger_key=triggers[0],
                        action_key=KEY_ID.KEYBOARD_LEFT_CONTROL),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD, trigger_key=triggers[1],
                        action_key=KEY_ID.KEYBOARD_LEFT_SHIFT),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD, trigger_key=triggers[2],
                        action_key=KEY_ID.KEYBOARD_LEFT_ALT),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD, trigger_key=triggers[3],
                        action_key=KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD, trigger_key=triggers[4],
                        action_key=KEY_ID.KEYBOARD_RIGHT_CONTROL),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD, trigger_key=triggers[5],
                        action_key=KEY_ID.KEYBOARD_RIGHT_SHIFT),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD, trigger_key=triggers[6],
                        action_key=KEY_ID.KEYBOARD_RIGHT_ALT),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD, trigger_key=triggers[7],
                        action_key=KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_modifier_keys=[KEY_ID.KEYBOARD_LEFT_CONTROL],
                        trigger_key=triggers[8],
                        action_key=RemappedKey.RandomKey.NON_MODIFIER_KEY),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_modifier_keys=[KEY_ID.KEYBOARD_LEFT_SHIFT],
                        trigger_key=triggers[9],
                        action_key=RemappedKey.RandomKey.NON_MODIFIER_KEY),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_modifier_keys=[KEY_ID.KEYBOARD_LEFT_ALT],
                        trigger_key=triggers[10],
                        action_key=RemappedKey.RandomKey.NON_MODIFIER_KEY),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_modifier_keys=[KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION],
                        trigger_key=triggers[11],
                        action_key=RemappedKey.RandomKey.NON_MODIFIER_KEY),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_modifier_keys=[KEY_ID.KEYBOARD_RIGHT_CONTROL],
                        trigger_key=triggers[12],
                        action_key=RemappedKey.RandomKey.NON_MODIFIER_KEY),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_modifier_keys=[KEY_ID.KEYBOARD_RIGHT_SHIFT],
                        trigger_key=triggers[13],
                        action_key=RemappedKey.RandomKey.NON_MODIFIER_KEY),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_modifier_keys=[KEY_ID.KEYBOARD_RIGHT_ALT],
                        trigger_key=triggers[14],
                        action_key=RemappedKey.RandomKey.NON_MODIFIER_KEY),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_modifier_keys=[KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION],
                        trigger_key=triggers[15],
                        action_key=RemappedKey.RandomKey.NON_MODIFIER_KEY),
        ]
        remapped_keys = self.create_remapping_in_ram(preset_remapped_keys=preset_remapped_keys)

        # Send button stimuli and check results
        # Check Modifier -> Modifier
        modifier_remapped_keys = [key for key in remapped_keys if len(key.trigger_modifier_keys) == 0]
        self.build_key_test_sequence_and_validate_result(remapped_keys=modifier_remapped_keys, block=True)

        # Check Modifier + Trigger -> Key
        modifier_trigger_remapped_keys = [key for key in remapped_keys if len(key.trigger_modifier_keys) == 1]
        key_test_sequence = deepcopy(modifier_trigger_remapped_keys)
        for remapped_key in key_test_sequence:
            if remapped_key.trigger_modifier_keys[0] == KEY_ID.KEYBOARD_LEFT_CONTROL:
                remapped_key.trigger_modifier_keys = [triggers[0]]
            elif remapped_key.trigger_modifier_keys[0] == KEY_ID.KEYBOARD_LEFT_SHIFT:
                remapped_key.trigger_modifier_keys = [triggers[1]]
            elif remapped_key.trigger_modifier_keys[0] == KEY_ID.KEYBOARD_LEFT_ALT:
                remapped_key.trigger_modifier_keys = [triggers[2]]
            elif remapped_key.trigger_modifier_keys[0] == KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION:
                remapped_key.trigger_modifier_keys = [triggers[3]]
            elif remapped_key.trigger_modifier_keys[0] == KEY_ID.KEYBOARD_RIGHT_CONTROL:
                remapped_key.trigger_modifier_keys = [triggers[4]]
            elif remapped_key.trigger_modifier_keys[0] == KEY_ID.KEYBOARD_RIGHT_SHIFT:
                remapped_key.trigger_modifier_keys = [triggers[5]]
            elif remapped_key.trigger_modifier_keys[0] == KEY_ID.KEYBOARD_RIGHT_ALT:
                remapped_key.trigger_modifier_keys = [triggers[6]]
            elif remapped_key.trigger_modifier_keys[0] == KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION:
                remapped_key.trigger_modifier_keys = [triggers[7]]
            else:
                raise ValueError(f'Unsupported modifier key id: {remapped_key.trigger_modifier_keys[0]!s}')
            # end if
        # end for
        self.build_key_test_sequence(remapped_keys=key_test_sequence, block=True)
        self.validate_result_for_test_sequence(remapped_keys=modifier_trigger_remapped_keys)

        self.testCaseChecked("BUS_FKC_0003", _AUTHOR)
    # end def test_trigger_to_modifier_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Business')
    @services('SimultaneousKeystrokes')
    def test_modifier_to_modifier_remapping(self):
        """
        [Special Remapping]
        Remap modifier key to modifier key. Add below remappings to test it works as expected.

        Remapping: [Modifier -> Modifier]
        L-Ctrl -> R-GUI
        L-Shift -> R-Alt
        L-Alt -> R-Shift
        L-GUI -> R-Ctrl
        R-Ctrl -> L-GUI
        R-Shift -> L-Alt
        R-Alt -> L-Shift
        R-GUI -> L-Ctrl
        L-Ctrl + Trigger1 -> Key1
        L-Shift + Trigger2 -> Key2
        L-Alt + Trigger3 -> Key3
        L-GUI + Trigger4 -> Key4
        R-Ctrl + Trigger5 -> Key5
        R-Shift + Trigger6 -> Key6
        R-Alt + Trigger7 -> Key7
        R-GUI + Trigger8 -> Key8
        (Select 16 triggers and 8 keys randomly.)
        """
        # Get all supported modifiers. Keyboard might not support all of 8 modifiers.
        all_modifier_keys = FullKeyCustomizationTestUtils.FkcTableHelper.KeyProvider.get_all_modifier_keys(
            test_case=self)
        modifier_count = len(all_modifier_keys)
        preset_remapped_keys = []
        for trigger_index in range(modifier_count):
            action_index = trigger_index + 1 if trigger_index < modifier_count - 1 else 0
            # Modifier -> Modifier
            preset_remapped_keys.append(
                RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                            trigger_key=all_modifier_keys[trigger_index],
                            action_key=all_modifier_keys[action_index]))
            # Modifier + Trigger -> Key
            preset_remapped_keys.append(
                RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                            trigger_modifier_keys=[all_modifier_keys[trigger_index]],
                            trigger_key=RemappedKey.RandomKey.NON_MODIFIER_KEY,
                            action_key=RemappedKey.RandomKey.NON_MODIFIER_KEY))
        # end for
        remapped_keys = self.create_remapping_in_ram(preset_remapped_keys=preset_remapped_keys)

        # Send button stimuli and check results
        # Check Modifier -> Modifier
        modifier_remapped_keys = [key for key in remapped_keys if len(key.trigger_modifier_keys) == 0]
        self.build_key_test_sequence_and_validate_result(remapped_keys=modifier_remapped_keys, block=True)

        # Check Modifier + Trigger -> Key
        modifier_trigger_remapped_keys = [key for key in remapped_keys if len(key.trigger_modifier_keys) == 1]
        key_test_sequence = deepcopy(modifier_trigger_remapped_keys)
        for remapped_key in key_test_sequence:
            action_index = all_modifier_keys.index(remapped_key.trigger_modifier_keys[0])
            trigger_index = action_index - 1 if action_index > 0 else modifier_count - 1
            remapped_key.trigger_modifier_keys = [all_modifier_keys[trigger_index]]
        # end for
        self.build_key_test_sequence(remapped_keys=key_test_sequence, block=True)
        self.validate_result_for_test_sequence(remapped_keys=modifier_trigger_remapped_keys)

        self.testCaseChecked("BUS_FKC_0004", _AUTHOR)
    # end def test_modifier_to_modifier_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Business')
    @services('SimultaneousKeystrokes')
    def test_modifier_to_action_remapping(self):
        """
        [Special Remapping]
        Remap modifier key to a possible action. Add below remappings to test it works as expected.

        Remapping: [Modifier -> Action]
        L-Ctrl -> Action
        L-Shift -> Action
        L-Alt -> Action
        L-GUI -> Action
        R-Ctrl -> Action
        R-Shift -> Action
        R-Alt -> Action
        R-GUI -> Action
        (Select an possible action randomly.)

        Possible actions:
        1. Standard Key (exclude modifier keys)
        2. Mouse Button
        3. Consumer code
        4. Macro (Create 2 macros with 5 standard keys by random selection)
        """
        # Get all supported modifiers. Keyboard might not support all of 8 modifiers.
        all_modifier_keys = FullKeyCustomizationTestUtils.FkcTableHelper.KeyProvider.get_all_modifier_keys(
            test_case=self)
        modifier_count = len(all_modifier_keys)
        preset_remapped_keys = []
        for trigger_index in range(modifier_count):
            # Modifier -> Action
            preset_remapped_keys.append(
                RemappedKey(action_type=RemappedKey.ActionType.RANDOM,
                            trigger_key=all_modifier_keys[trigger_index],
                            action_key=RemappedKey.RandomKey.RANDOM))
        # end for
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(
            preset_remapped_keys=preset_remapped_keys,  random_parameters=random_parameters_cls(
                macro=random_parameters_cls.Macro(entry_count=2, command_count=5)))

        # Send button stimuli and check results
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys)

        self.testCaseChecked("BUS_FKC_0005", _AUTHOR)
    # end def test_modifier_to_action_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Business')
    @services('SimultaneousKeystrokes')
    def test_trigger_to_tilt_remapping(self):
        """
        [Special Remapping]
        Remap customizable key to supported Logi function key. Add below remappings to test it works as expected.

        Remapping: [Trigger -> Logi Function Key]
        Trigger1 -> No action
        Trigger2 -> Tilt Left
        Trigger3 -> Tilt Right
        (Select 3 trigger keys randomly.)
        """
        # Configure key remapping
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.FUNCTION,
                        trigger_key=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
                        action_key=KEY_ID.NO_ACTION),
            RemappedKey(action_type=RemappedKey.ActionType.FUNCTION,
                        trigger_key=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
                        action_key=KEY_ID.TILT_LEFT),
            RemappedKey(action_type=RemappedKey.ActionType.FUNCTION,
                        trigger_key=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
                        action_key=KEY_ID.TILT_RIGHT),
        ]
        remapped_keys = self.create_remapping_in_ram(preset_remapped_keys=preset_remapped_keys)

        # Send button stimuli and check results
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys)

        self.testCaseChecked("BUS_FKC_0006", _AUTHOR)
    # end def test_trigger_to_tilt_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @features('Feature8101MultipleProfiles')
    @level('Business')
    @services('SimultaneousKeystrokes')
    def test_trigger_to_profile_button_remapping(self):
        """
        [Special Remapping]
        Remap customizable key to supported Logi function key. Add below remappings to test it works as expected.

        Remapping: [Trigger -> Logi Function Key]
        Trigger1 -> Select next onboard profile
        Trigger2 -> Select previous onboard profile
        Trigger3 -> Cycle through onboard profile
        Trigger4 -> Switch a specific onboard profile
        (Select 4 trigger keys randomly.)
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        trigger_1 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY)
        trigger_2 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
            excluded_keys=[trigger_1])
        trigger_3 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
            excluded_keys=[trigger_1, trigger_2])
        trigger_4 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
            excluded_keys=[trigger_1, trigger_2, trigger_3])
        max_profile_count = self.f.PRODUCT.FEATURES.GAMING.PROFILE_MANAGEMENT.F_NumOnboardProfiles
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.FUNCTION,
                        trigger_key=trigger_1,
                        action_key=KEY_ID.SELECT_NEXT_ONBOARD_PROFILE),
            RemappedKey(action_type=RemappedKey.ActionType.FUNCTION,
                        trigger_key=trigger_2,
                        action_key=KEY_ID.SELECT_PREV_ONBOARD_PROFILE),
            RemappedKey(action_type=RemappedKey.ActionType.FUNCTION,
                        trigger_key=trigger_3,
                        action_key=KEY_ID.CYCLE_THROUGH_ONBOARD_PROFILE),
            RemappedKey(action_type=RemappedKey.ActionType.FUNCTION,
                        trigger_key=trigger_4,
                        action_key=KEY_ID.SWITCH_TO_SPECIFIC_ONBOARD_PROFILE,
                        profile_number=max_profile_count),
        ]
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            profile_count=max_profile_count), preset_remapped_keys=preset_remapped_keys)

        current_profile_file_id = to_int(ProfileManagementTestUtils.HIDppHelper.get_set_mode(
            test_case=self, set_onboard_mode=0, onboard_mode=0).curr_profile_file_id)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Test Loop over profile by the key \"Select next onboard profile\"")
        # --------------------------------------------------------------------------------------------------------------
        while current_profile_file_id < max_profile_count:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send a keystroke for the trigger key: {trigger_1!s}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=trigger_1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the device sends expected profile changed notification")
            # ----------------------------------------------------------------------------------------------------------
            profile_changed_event = ProfileManagementTestUtils.HIDppHelper.profile_change_event(test_case=self)
            current_profile_file_id += 1
            checker = ProfileManagementTestUtils.ProfileChangeEventChecker
            check_map = checker.get_default_check_map(test_case=self)
            check_map.update({"new_profile": (checker.check_new_profile, current_profile_file_id), })
            _, feature_8101, _, _ = ProfileManagementTestUtils.HIDppHelper.get_parameters(test_case=self)
            checker.check_fields(test_case=self, message=profile_changed_event,
                                 expected_cls=feature_8101.profile_change_event_cls, check_map=check_map)
        # end while

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Test Loop over profile by the key \"Select previous onboard profile\"")
        # --------------------------------------------------------------------------------------------------------------
        while current_profile_file_id > 1:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send a keystroke for the trigger key: {trigger_2}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=trigger_2)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the device sends expected profile changed notification")
            # ----------------------------------------------------------------------------------------------------------
            profile_changed_event = ProfileManagementTestUtils.HIDppHelper.profile_change_event(test_case=self)
            current_profile_file_id -= 1
            checker = ProfileManagementTestUtils.ProfileChangeEventChecker
            check_map = checker.get_default_check_map(test_case=self)
            check_map.update({"new_profile": (checker.check_new_profile, current_profile_file_id), })
            _, feature_8101, _, _ = ProfileManagementTestUtils.HIDppHelper.get_parameters(test_case=self)
            checker.check_fields(test_case=self, message=profile_changed_event,
                                 expected_cls=feature_8101.profile_change_event_cls, check_map=check_map)
        # end while

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Test Loop over profile by the key \"Cycle through onboard profile\"")
        # --------------------------------------------------------------------------------------------------------------
        for _ in range(max_profile_count):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send a keystroke for the trigger key: {trigger_3}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=trigger_3)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the device sends expected profile changed notification")
            # ----------------------------------------------------------------------------------------------------------
            profile_changed_event = ProfileManagementTestUtils.HIDppHelper.profile_change_event(test_case=self)
            current_profile_file_id += 1
            if current_profile_file_id > max_profile_count:
                current_profile_file_id = 1
            # end if
            checker = ProfileManagementTestUtils.ProfileChangeEventChecker
            check_map = checker.get_default_check_map(test_case=self)
            check_map.update({"new_profile": (checker.check_new_profile, current_profile_file_id), })
            _, feature_8101, _, _ = ProfileManagementTestUtils.HIDppHelper.get_parameters(test_case=self)
            checker.check_fields(test_case=self, message=profile_changed_event,
                                 expected_cls=feature_8101.profile_change_event_cls, check_map=check_map)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send a keystroke to switch to a specific profile: {trigger_4}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=trigger_4)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the device sends expected profile changed notification")
        # --------------------------------------------------------------------------------------------------------------
        profile_changed_event = ProfileManagementTestUtils.HIDppHelper.profile_change_event(test_case=self)
        checker = ProfileManagementTestUtils.ProfileChangeEventChecker
        check_map = checker.get_default_check_map(test_case=self)
        check_map.update({"new_profile": (checker.check_new_profile, max_profile_count), })
        _, feature_8101, _, _ = ProfileManagementTestUtils.HIDppHelper.get_parameters(test_case=self)
        checker.check_fields(test_case=self, message=profile_changed_event,
                             expected_cls=feature_8101.profile_change_event_cls, check_map=check_map)

        self.testCaseChecked("BUS_FKC_0008", _AUTHOR)
    # end def test_trigger_to_profile_button_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Business')
    @services('SimultaneousKeystrokes')
    def test_trigger_to_battery_life_indicator_remapping(self):
        """
        [Special Remapping]
        Remap customizable key to supported Logi function key. Add below remappings to test it works as expected.

        Remapping: [Trigger -> Logi Function Key]
        Trigger1 -> Battery life indicator button
        (Select 1 trigger keys randomly.)
        """
        # Configure key remapping
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.FUNCTION,
                        trigger_key=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
                        action_key=KEY_ID.BATTERY_LIFE_INDICATOR),
        ]
        remapped_keys = self.create_remapping_in_ram(preset_remapped_keys=preset_remapped_keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send a keystroke to turn on battery life indicator: {remapped_keys[0]}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=remapped_keys[0].trigger_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the device turns on the battery LED")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Add Kosmos LED analyzer

        self.testCaseChecked("BUS_FKC_0009", _AUTHOR)
    # end def test_trigger_to_battery_life_indicator_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Business')
    @services('KeyMatrix')
    def test_modifiers_may_get_artificially_released(self):
        """
        [FKC Behavior - FKC UX 1.10]
        Check modifiers may get artificially released when pressing a customized shortcut.
        Add below remappings to test it works as expected.

        Remapping:
        Modifier1 + Trigger1 -> Key1
        Trigger2 (no remapping)
        (Select 1 modifier, 2 triggers and key randomly.)
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        modifier_1 = random_generation_helper.get_random_modifier_key(test_case=self)
        trigger_1 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY)
        trigger_2 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY, excluded_keys=[trigger_1])
        key_1 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY)
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_modifier_keys=[modifier_1],
                        trigger_key=trigger_1,
                        action_key=key_1),
        ]
        self.create_remapping_in_ram(preset_remapped_keys=preset_remapped_keys)

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold the Modifier1: {modifier_1!s}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=modifier_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Modifier1")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_1, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold the Trigger1: {trigger_1!s}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Key1: {key_1!s} "
                                  "(the Modifier1 be artificially released)")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(trigger_modifier_keys=[modifier_1],  # Suppress modifier 1
                                            action_key=key_1,
                                            state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold the Trigger2: {trigger_2!s} to check the Modifier1 be regenerated")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Modifier1 + Trigger1 + Trigger2")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_modifier_keys=[modifier_1], action_key=trigger_2, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger2: {trigger_2!s}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Modifier1 + Trigger1")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=trigger_2, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger1: {trigger_1!s}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Modifier1")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_1, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Modifier1: {modifier_1!s}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=modifier_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report with empty content")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_modifier_keys=[modifier_1], state=BREAK))

        self.testCaseChecked("BUS_FKC_0010", _AUTHOR)
    # end def test_modifiers_may_get_artificially_released

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Business')
    @services('SimultaneousKeystrokes')
    def test_no_temporary_release_of_modifier(self):
        """
        [FKC Behavior - FKC UX 1.11]
        Check there is no temporary release of modifier when a remap trigger and target include the same modifier.
        Add below remapping to test it works as expected.

        Remapping:
        Modifier1 + Trigger1 -> Modifier1 + Key1
        (Select 1 modifier, trigger and key randomly.)
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        modifier_1 = random_generation_helper.get_random_modifier_key(test_case=self)
        trigger_1 = random_generation_helper.get_random_non_modifier_key(test_case=self)
        key_1 = random_generation_helper.get_random_non_modifier_key(test_case=self)
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_modifier_keys=[modifier_1],
                        trigger_key=trigger_1,
                        action_modifier_keys=[modifier_1],
                        action_key=key_1),
        ]
        self.create_remapping_in_ram(preset_remapped_keys=preset_remapped_keys)

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold the Modifier1: {modifier_1!s}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=modifier_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Modifier1")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_1, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold the Trigger1: {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Modifier1 + Key1: {modifier_1!r}, {key_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_1, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger1: {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Modifier1")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_1, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Modifier1: {modifier_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=modifier_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report with empty content")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_modifier_keys=[modifier_1], state=BREAK))

        self.testCaseChecked("BUS_FKC_0011", _AUTHOR)
    # end def test_no_temporary_release_of_modifier

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Business')
    @services('KeyMatrix')
    def test_implicit_remaps_of_all_single_key_triggers(self):
        """
        [FKC Behavior - FKC UX 1.20]
        Check the implicit remaps of all single-key triggers. Add below remapping to test it works as expected.

        Remapping:
        Trigger1 -> Key1
        Modifier1 + Trigger1 -> Key2
        Trigger2 -> Modifier2 + Key3
        Trigger3 -> Macro1 (Random select 3 non-modifier keys)
        Trigger4 -> Modifier3
        Trigger5 -> Logi function key - Tilt Left
        Modifier4
        Modifier5
        (Select 5 modifiers, 5 triggers and 3 keys randomly.)
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        modifier_1 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.MODIFIER_KEY)
        modifier_2 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.MODIFIER_KEY,
            excluded_keys=[modifier_1])
        modifier_3 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.MODIFIER_KEY,
            excluded_keys=[modifier_1, modifier_2])
        modifier_4 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.MODIFIER_KEY,
            excluded_keys=[modifier_1, modifier_2, modifier_3])
        modifier_5 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.MODIFIER_KEY,
            excluded_keys=[modifier_1, modifier_2, modifier_3, modifier_4])
        trigger_1 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY)
        trigger_2 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY,
            excluded_keys=[trigger_1])
        trigger_3 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY,
            excluded_keys=[trigger_1, trigger_2])
        trigger_4 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY,
            excluded_keys=[trigger_1, trigger_2, trigger_3])
        trigger_5 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY,
            excluded_keys=[trigger_1, trigger_2, trigger_3, trigger_4])
        key_1 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY)
        key_2 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY, excluded_keys=[key_1])
        key_3 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY, excluded_keys=[key_1, key_2])
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_1,
                        action_key=key_1),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_modifier_keys=[modifier_1],
                        trigger_key=trigger_1,
                        action_key=key_2),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_2,
                        action_modifier_keys=[modifier_2],
                        action_key=key_3),
            RemappedKey(action_type=RemappedKey.ActionType.MACRO,
                        trigger_key=trigger_3,
                        macro_entry_index=0),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_4,
                        action_key=modifier_3),
            RemappedKey(action_type=RemappedKey.ActionType.FUNCTION,
                        trigger_key=trigger_5,
                        action_key=KEY_ID.TILT_LEFT),
        ]
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(
            preset_remapped_keys=preset_remapped_keys,  random_parameters=random_parameters_cls(
                macro=random_parameters_cls.Macro(entry_count=1, command_count=3)))

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Perform Modifier4 + Trigger1 {trigger_1!r} combination key properly")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.build_key_sequence(
            test_case=self, remapped_key=RemappedKey(trigger_modifier_keys=[modifier_4], trigger_key=trigger_1))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Modifier4 + Key1 {key_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_4, state=MAKE))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_1, state=MAKE))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_1, state=BREAK))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_4, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Perform Modifier2 + Trigger1 {trigger_1!r} combination key properly")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.build_key_sequence(
            test_case=self, remapped_key=RemappedKey(trigger_modifier_keys=[modifier_2], trigger_key=trigger_1))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report R-Shift + Key1 {key_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_2, state=MAKE))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_1, state=MAKE))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_1, state=BREAK))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_2, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Perform Modifier1 + Trigger1 {trigger_1!r} combination key properly")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.build_key_sequence(
            test_case=self, remapped_key=RemappedKey(trigger_modifier_keys=[modifier_1], trigger_key=trigger_1))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Key2 {key_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(
            test_case=self, remapped_key=RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                                                     trigger_modifier_keys=[modifier_1],
                                                     trigger_key=trigger_1, action_key=key_2))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Perform Modifier3 + Modifier1 + Trigger1 {trigger_1!r} combination key properly")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.build_key_sequence(
            test_case=self, remapped_key=RemappedKey(trigger_modifier_keys=[modifier_3, modifier_1],
                                                     trigger_key=trigger_1))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Modifier3 + Modifier1 + Key1 {key_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_3, state=MAKE))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_1, state=MAKE))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(
            test_case=self, remapped_key=RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                                                     trigger_key=trigger_1, action_key=key_1))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_1, state=BREAK))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_3, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Perform Modifier2 + Modifier1 + Trigger1 {trigger_1!r} combination key properly")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.build_key_sequence(
            test_case=self, remapped_key=RemappedKey(trigger_modifier_keys=[modifier_2, modifier_1],
                                                     trigger_key=trigger_1))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Modifier2 + Modifier1 + Key1 {key_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_2, state=MAKE))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_1, state=MAKE))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(
            test_case=self, remapped_key=RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                                                     trigger_key=trigger_1, action_key=key_1))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_1, state=BREAK))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_2, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Perform Modifier4 + Trigger2 {trigger_2!r} combination key properly")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.build_key_sequence(
            test_case=self, remapped_key=RemappedKey(trigger_modifier_keys=[modifier_4], trigger_key=trigger_2))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Modifier4 + Modifier2 + Key3 {key_3!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_4, state=MAKE))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(
            test_case=self, remapped_key=RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                                                     trigger_key=trigger_2,
                                                     action_modifier_keys=[modifier_2],
                                                     action_key=key_3))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_4, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Perform Modifier3 + Trigger3 {trigger_3!r} combination key properly")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.build_key_sequence(
            test_case=self, remapped_key=RemappedKey(trigger_modifier_keys=[modifier_3], trigger_key=trigger_3))

        trigger_3_remapped_key = None
        for remapped_key in remapped_keys:
            if remapped_key.action_type == RemappedKey.ActionType.MACRO:
                trigger_3_remapped_key = remapped_key
                break
            # end if
        # end for
        self.assertNotNone(trigger_3_remapped_key)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Modifier3 + Macro1 "
                                  f"{trigger_3_remapped_key.macro_commands}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_3, state=MAKE))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(
            test_case=self, remapped_key=trigger_3_remapped_key)
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
                    test_case=self, key=RemappedKey(action_key=modifier_3, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Perform Modifier5 + Trigger4 {trigger_4!r} combination key properly")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.build_key_sequence(
            test_case=self, remapped_key=RemappedKey(trigger_modifier_keys=[modifier_5], trigger_key=trigger_4))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Modifier5 + Modifier3")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_5, state=MAKE))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(
            test_case=self, remapped_key=RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                                                     trigger_key=trigger_4,
                                                     action_key=modifier_3))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_5, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Perform Modifier5 + Trigger5 {trigger_5!r} combination key properly")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.build_key_sequence(
            test_case=self, remapped_key=RemappedKey(trigger_modifier_keys=[modifier_5], trigger_key=trigger_5))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Modifier5 + Logi function key - Tilt Left")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_5, state=MAKE))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(
            test_case=self, remapped_key=RemappedKey(action_type=RemappedKey.ActionType.FUNCTION,
                                                     trigger_key=trigger_5,
                                                     action_key=KEY_ID.TILT_LEFT))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_5, state=BREAK))

        self.testCaseChecked("BUS_FKC_0012", _AUTHOR)
    # end def test_implicit_remaps_of_all_single_key_triggers

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Business')
    @services('KeyMatrix')
    def test_key_press_event_is_simply(self):
        """
        [FKC Behavior - FKC UX 1.22, 1.23]
        Check for single key triggers, the key press event is simply when the user presses the physical trigger key.
        Add below remapping to test it works as expected.

        Remapping:
        Modifier1 + Trigger1 -> Key1
        Modifier2 (no remapping)
        (Select 2 modifiers, 1 trigger and 1 keys randomly.)
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        modifier_1 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.MODIFIER_KEY)
        modifier_2 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.MODIFIER_KEY, excluded_keys=[modifier_1])
        trigger_1 = random_generation_helper.get_random_non_modifier_key(test_case=self)
        key_1 = random_generation_helper.get_random_non_modifier_key(test_case=self)
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_modifier_keys=[modifier_1],
                        trigger_key=trigger_1,
                        action_key=key_1),
        ]
        self.create_remapping_in_ram(preset_remapped_keys=preset_remapped_keys)

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold the Modifier1: {modifier_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=modifier_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Modifier1")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_1, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold the Trigger1: {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Key1 {key_1!r} (Modifier1 suppressed)")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(trigger_modifier_keys=[modifier_1], action_key=key_1, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Modifier1: {modifier_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=modifier_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received no HID report")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger1: {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report with empty content (all key released)")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_1, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold Modifier1 {modifier_1!r} + Modifier2 {modifier_2!r} + "
                                 f"Trigger1 {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[modifier_1, modifier_2, trigger_1], delay=0.05)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Modifier1 {modifier_1!r} + Modifier2 {modifier_2!r} + "
                                  f"Trigger1 {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_1, state=MAKE))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_2, state=MAKE))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=trigger_1, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Modifier2: {modifier_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=modifier_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Modifier1 {modifier_1!r} + Trigger1 {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_2, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Modifier1 {modifier_1!r}  + Trigger1 {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_release(key_ids=[modifier_1, trigger_1], delay=0.05)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report with empty content (all key released)")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_1, state=BREAK))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=trigger_1, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold the Trigger1: {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Trigger1: {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=trigger_1, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold the Modifier1: {modifier_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=modifier_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Modifier1 {modifier_1!r} + Trigger1 {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_1, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Modifier1 {modifier_1!r}  + Trigger1 {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_release(key_ids=[modifier_1, trigger_1], delay=0.05)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report with empty content (all key released)")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_1, state=BREAK))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=trigger_1, state=BREAK))

        self.testCaseChecked("BUS_FKC_0013", _AUTHOR)
    # end def test_key_press_event_is_simply

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Business')
    @services('SimultaneousKeystrokes')
    def test_ability_to_enter_several_shortcuts_in_sequence(self):
        """
        [FKC Behavior - FKC UX 1.24]
        Check the ability to enter several shortcuts in sequence while holding a modifier down.
        Add below remapping to test it works as expected.

        Remapping:
        Modifier1 + Trigger1 -> Key1
        Modifier1 + Trigger2 -> Key2
        Trigger3 (no remapping)
        (Select 1 modifier, 2 triggers and 2 keys randomly.)
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        modifier_1 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.MODIFIER_KEY)
        trigger_1 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY)
        trigger_2 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY, excluded_keys=[trigger_1])
        trigger_3 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY, excluded_keys=[trigger_1, trigger_2])
        key_1 = random_generation_helper.get_random_non_modifier_key(test_case=self)
        key_2 = random_generation_helper.get_random_non_modifier_key(test_case=self)
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_modifier_keys=[modifier_1],
                        trigger_key=trigger_1,
                        action_key=key_1),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_modifier_keys=[modifier_1],
                        trigger_key=trigger_2,
                        action_key=key_2),
        ]
        self.create_remapping_in_ram(preset_remapped_keys=preset_remapped_keys)

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold Modifier1 + Trigger1 {trigger_1!r} properly")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[modifier_1, trigger_1], delay=0.05)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Key1 {key_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_1, state=MAKE))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(trigger_modifier_keys=[modifier_1], action_key=key_1, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger1 {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report for Key1 {key_1!r} released")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_1, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold Trigger2 {trigger_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Key2 {key_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_2, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger2 {trigger_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report for Key2 {key_2!r} released")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_2, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold Trigger3 {trigger_3!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Modifier1 + Trigger3 {trigger_3!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=trigger_3, action_modifier_keys=[modifier_1], state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger3 {trigger_3!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report for Trigger3 {trigger_3!r} released")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=trigger_3, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Release Modifier1")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=modifier_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report for Modifier1 released")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_1, state=BREAK))

        self.testCaseChecked("BUS_FKC_0014", _AUTHOR)
    # end def test_ability_to_enter_several_shortcuts_in_sequence

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Business')
    @services('SimultaneousKeystrokes')
    def test_key_customizations_will_not_chain(self):
        """
        [FKC Behavior - FKC UX 1.28]
        Check the key customizations will not chain. Add below remapping to test it works as expected.

        Remapping:
        Trigger1 -> Key1
        Trigger2(=Key1) -> Key2
        Trigger3 -> Macro(Key3, Key4, Key5)
        Trigger4(=Key4) -> Key6
        (Select 2 triggers and 6 keys randomly and Trigger2 = Key1, Trigger4 = Key4.)
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        key_1 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY)
        key_2 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY, excluded_keys=[key_1])
        key_3 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY, excluded_keys=[key_1, key_2])
        key_4 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY, excluded_keys=[key_1, key_2, key_3])
        key_5 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY, excluded_keys=[key_1, key_2, key_3, key_4])
        key_6 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY,
            excluded_keys=[key_1, key_2, key_3, key_4, key_5])
        trigger_1 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY, excluded_keys=[key_1, key_4])
        trigger_2 = key_1
        trigger_3 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY, excluded_keys=[trigger_1, trigger_2])
        trigger_4 = key_4
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_1,
                        action_key=key_1),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_2,
                        action_key=key_2),
            RemappedKey(action_type=RemappedKey.ActionType.MACRO,
                        trigger_key=trigger_3,
                        macro_entry_index=0),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_4,
                        action_key=key_3),
        ]
        preset_macro_entries = [
            PresetMacroEntry(commands=[StandardKeyCommand(key_id=key_4),
                                       StandardKeyCommand(key_id=key_5),
                                       StandardKeyCommand(key_id=key_6),
                                       MacroEndCommand()]),
        ]
        self.create_remapping_in_nvs(preset_remapped_keys=preset_remapped_keys,
                                     preset_macro_entries=preset_macro_entries)

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send a keystroke for Trigger1 {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=trigger_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Key1 {key_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_1, state=MAKE))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_1, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send a keystroke for Trigger3 {trigger_3!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=trigger_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Macro(Key4, Key5, Key6) "
                                  f"{key_4!r}, {key_5!r}, {key_6!r}")
        # --------------------------------------------------------------------------------------------------------------
        for key in [key_4, key_5, key_6]:
            FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
                test_case=self, key=RemappedKey(action_key=key, state=MAKE))
            FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
                test_case=self, key=RemappedKey(action_key=key, state=BREAK))
        # end for

        self.testCaseChecked("BUS_FKC_0015", _AUTHOR)
    # end def test_key_customizations_will_not_chain

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Business')
    @services('SimultaneousKeystrokes')
    def test_ability_to_trigger_multiple_key_customizations_in_parallel_1(self):
        """
        [FKC Behavior - FKC UX 1.31]
        Check the ability to trigger multiple key customizations in parallel.
        Add below remapping to test it works as expected.

        Remapping:
        Trigger1 -> Key1
        Trigger2 -> Key2
        (Select 2 triggers and 2 keys randomly.)
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        trigger_1 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY)
        trigger_2 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY, excluded_keys=[trigger_1])
        key_1 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.STANDARD_KEY)
        key_2 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.STANDARD_KEY, excluded_keys=[key_1])
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_1,
                        action_key=key_1),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_2,
                        action_key=key_2),
        ]
        self.create_remapping_in_ram(preset_remapped_keys=preset_remapped_keys)

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold Trigger1 {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Key1 {key_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_1, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold the Trigger2: {trigger_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Key1 + Key2: {key_1!r} {key_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_2, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger1: {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Key2 {key_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_1, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger2: {trigger_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report with empty content")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_2, state=BREAK))

        self.testCaseChecked("BUS_FKC_0016", _AUTHOR)
    # end def test_ability_to_trigger_multiple_key_customizations_in_parallel_1

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Business')
    @services('KeyMatrix')
    def test_ability_to_trigger_multiple_key_customizations_in_parallel_2(self):
        """
        [FKC Behavior - FKC UX 1.31]
        Check the ability to trigger multiple key customizations in parallel.
        Add below remapping to test it works as expected.

        Remapping:
        Modifier1 + Trigger1 -> Key1
        Modifier1 + Trigger2 -> Key2
        (Select 1 modifier, 2 triggers and 2 keys randomly.)
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        modifier_1 = random_generation_helper.get_random_modifier_key(test_case=self)
        trigger_1 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY)
        trigger_2 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY, excluded_keys=[trigger_1])
        key_1 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.STANDARD_KEY)
        key_2 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.STANDARD_KEY, excluded_keys=[key_1])
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_modifier_keys=[modifier_1],
                        trigger_key=trigger_1,
                        action_key=key_1),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_2,
                        trigger_modifier_keys=[modifier_1],
                        action_key=key_2),
        ]
        self.create_remapping_in_ram(preset_remapped_keys=preset_remapped_keys)

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold Modifier1 {modifier_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=modifier_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Modifier1 {modifier_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_1, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold Trigger1 {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Key1 {key_1!r} (Modifier1 suppressed)")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(trigger_modifier_keys=[modifier_1], action_key=key_1, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold the Trigger2: {trigger_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Key1 + Key2: {key_1!r} {key_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_2, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger1: {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Key2 {key_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_1, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger2: {trigger_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report with empty content")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_2, state=BREAK))

        self.testCaseChecked("BUS_FKC_0017", _AUTHOR)
    # end def test_ability_to_trigger_multiple_key_customizations_in_parallel_2

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Business')
    @services('KeyMatrix')
    def test_ability_to_trigger_multiple_key_customizations_in_parallel_3(self):
        """
        [FKC Behavior - FKC UX 1.31]
        Check the ability to trigger multiple key customizations in parallel. Add below "Keypress triggers with
        different modifiers" remappings to test it works as expected.

        Remapping:
        Trigger1 -> Key1
        Modifier1 + Trigger1 -> Key2
        Modifier1 + Trigger2 -> Key3
        Modifier1 + Modifier2 + Trigger3 -> Key4
        (Select 2 modifiers, 3 triggers and 4 keys randomly.)
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        modifier_1 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.MODIFIER_KEY)
        modifier_2 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.MODIFIER_KEY, excluded_keys=[modifier_1])
        trigger_1 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY)
        trigger_2 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY, excluded_keys=[trigger_1])
        trigger_3 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY, excluded_keys=[trigger_1, trigger_2])
        key_1 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.STANDARD_KEY)
        key_3 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.STANDARD_KEY, excluded_keys=[key_1])
        key_4 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.STANDARD_KEY, excluded_keys=[key_1, key_3])
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_1,
                        action_key=key_1),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_modifier_keys=[modifier_1],
                        trigger_key=trigger_1,
                        action_key=RemappedKey.RandomKey.NON_MODIFIER_KEY),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_modifier_keys=[modifier_1],
                        trigger_key=trigger_2,
                        action_key=key_3),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_modifier_keys=[modifier_1, modifier_2],
                        trigger_key=trigger_3,
                        action_key=key_4),
        ]
        self.create_remapping_in_ram(preset_remapped_keys=preset_remapped_keys)

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold Trigger1 {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Key1 {key_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_1, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold Modifier1 {modifier_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=modifier_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Modifier1 + Key1 {modifier_1!r} {key_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_1, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold Trigger2 {trigger_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Key1 + Key3 {key_1!r} {key_3!r} (Modifier1 suppressed)")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(trigger_modifier_keys=[modifier_1], action_key=key_3, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold the Modifier2: {modifier_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=modifier_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Modifier2 + Key1 + Key3 "
                                  f"{modifier_2!r} {key_1!r} {key_3!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_2, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold the Trigger3: {trigger_3!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Key1 + Key3 + Key4 "
                                  f"{key_1!r} {key_3!r} {key_4!r} (Modifier2 suppressed)")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(trigger_modifier_keys=[modifier_2], action_key=key_4, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger3: {trigger_3!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Key1 + Key3 {key_1!r} {key_3!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_4, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Modifier1: {modifier_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=modifier_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check no HID report received")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger2: {trigger_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Key1")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_3, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger1: {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report with empty content")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_1, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Modifier2: {modifier_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=modifier_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check no HID report received")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        self.testCaseChecked("BUS_FKC_0018", _AUTHOR)
    # end def test_ability_to_trigger_multiple_key_customizations_in_parallel_3

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Business')
    @services('KeyMatrix')
    def test_ability_to_trigger_multiple_key_customizations_in_parallel_4(self):
        """
        [FKC Behavior - FKC UX 1.31]
        Check the ability to trigger multiple key customizations in parallel. Add below "Remapped targets with
        different modifiers" remappings to test it works as expected.

        Remapping:
        Trigger1 -> Key1
        Trigger2 -> Modifier1 + Key2
        Trigger3 -> Modifier2 + Key3
        Trigger4 -> Modifier2 + Key4
        (Select 2 modifiers, 4 triggers and 4 keys randomly.)
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        modifier_1 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.MODIFIER_KEY)
        modifier_2 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.MODIFIER_KEY, excluded_keys=[modifier_1])
        trigger_1 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY)
        trigger_2 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
            excluded_keys=[trigger_1])
        trigger_3 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
            excluded_keys=[trigger_1, trigger_2])
        trigger_4 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
            excluded_keys=[trigger_1, trigger_2, trigger_3])
        key_1 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY)
        key_2 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY, excluded_keys=[key_1])
        key_3 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY, excluded_keys=[key_1, key_2])
        key_4 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY, excluded_keys=[key_1, key_2, key_3])
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_1,
                        action_key=key_1),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_2,
                        action_modifier_keys=[modifier_1],
                        action_key=key_2),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_3,
                        action_modifier_keys=[modifier_2],
                        action_key=key_3),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_4,
                        action_modifier_keys=[modifier_2],
                        action_key=key_4),
        ]
        self.create_remapping_in_ram(preset_remapped_keys=preset_remapped_keys)

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold Trigger1 {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Key1 {key_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_1, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold Trigger2 {trigger_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Modifier1 + Key1 + Key2 "
                                  f"{modifier_1!r} {key_1!r} {key_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_modifier_keys=[modifier_1], action_key=key_2, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold Modifier2 {modifier_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=modifier_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Modifier1 + Modifier2 + Key1 + Key2 "
                                  f"{modifier_1!r} {modifier_2!r} {key_1!r} {key_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_2, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Modifier2 {modifier_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=modifier_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Modifier1 + Key1 + Key2 "
                                  f"{modifier_1!r} {key_1!r} {key_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_2, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold Trigger3 {trigger_3!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Modifier1 + Modifier2 + Key1 + Key2 + Key3 "
                                  f"{modifier_1!r} {modifier_2!r} {key_1!r} {key_2!r} {key_3!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_modifier_keys=[modifier_2], action_key=key_3, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold Trigger4 {trigger_4!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_4)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Modifier1 + Modifier2 + Key1 + Key2 + Key3 + Key4"
                                  f"{modifier_1!r} {modifier_2!r} {key_1!r} {key_2!r} {key_3!r} {key_4!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_4, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger4 {trigger_4!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_4)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Modifier1 + Key1 + Key2 + Key3 "
                                  f"{modifier_1!r} {key_1!r} {key_2!r} {key_3!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_modifier_keys=[modifier_2], action_key=key_4, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger2 {trigger_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Key1 + Key3 {key_1!r} {key_3!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_modifier_keys=[modifier_1], action_key=key_2, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger1 {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Key3 {key_3!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_1, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger3 {trigger_3!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report with empty content")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_3, state=BREAK))

        self.testCaseChecked("BUS_FKC_0019", _AUTHOR)
    # end def test_ability_to_trigger_multiple_key_customizations_in_parallel_4

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Business')
    @services('KeyMatrix')
    def test_pressing_multiple_trigger_keys_that_are_mapped_to_the_same_target_1(self):
        """
        [FKC Behavior - FKC UX 1.37]
        Check the behavior when pressing multiple trigger keys that are mapped to the same target.
        Add below remappings to test it works as expected.

        Remapping:
        Trigger1 -> Key1
        Trigger2 -> Key1
        Trigger3 -> Key1
        (Select 3 triggers and 1 key randomly.)
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        trigger_1 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY)
        trigger_2 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY, excluded_keys=[trigger_1])
        trigger_3 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY, excluded_keys=[trigger_1, trigger_2])
        key_1 = random_generation_helper.get_random_non_modifier_key(test_case=self)
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_1,
                        action_key=key_1),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_2,
                        action_key=key_1),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_3,
                        action_key=key_1),
        ]
        self.create_remapping_in_ram(preset_remapped_keys=preset_remapped_keys)

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold Trigger1 {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Key1 {key_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_1, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold the Trigger2: {trigger_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Key1 {key_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_1, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold the Trigger3: {trigger_3!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Key1 {key_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_1, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger3: {trigger_3!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report with empty content (Key1 {key_1!r} being released)")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_1, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger2: {trigger_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check there is no HID input received")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger1: {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check there is no HID input received")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        self.testCaseChecked("BUS_FKC_0020", _AUTHOR)
    # end def test_pressing_multiple_trigger_keys_that_are_mapped_to_the_same_target_1

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Business')
    @services('KeyMatrix')
    def test_pressing_multiple_trigger_keys_that_are_mapped_to_the_same_target_2(self):
        """
        [FKC Behavior - FKC UX 1.37]
        Check the behavior when pressing multiple trigger keys that are mapped to the same target.
        Add below remappings to test it works as expected.

        Remapping:
        Trigger1 -> Modifier1 + Key1
        Trigger2 -> Modifier1 + Key2
        Trigger3 -> Modifier1 + Key3
        (Select 1 modifier, 3 triggers and 3 keys randomly.)
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        trigger_1 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY)
        trigger_2 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY, excluded_keys=[trigger_1])
        trigger_3 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY, excluded_keys=[trigger_1, trigger_2])
        modifier_1 = random_generation_helper.get_random_modifier_key(test_case=self)
        key_1 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY)
        key_2 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY, excluded_keys=[key_1])
        key_3 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY, excluded_keys=[key_1, key_2])
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_1,
                        action_modifier_keys=[modifier_1],
                        action_key=key_1),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_2,
                        action_modifier_keys=[modifier_1],
                        action_key=key_2),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_3,
                        action_modifier_keys=[modifier_1],
                        action_key=key_3),
        ]
        self.create_remapping_in_ram(preset_remapped_keys=preset_remapped_keys)

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold Trigger1 {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Modifier1 + Key1 {modifier_1!r} {key_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_modifier_keys=[modifier_1], action_key=key_1, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold the Trigger2: {trigger_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Modifier1 + Key1 + Key2 "
                                  f"{modifier_1!r} {key_1!r} {key_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_2, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold the Trigger3: {trigger_3!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Modifier1 + Key1 + Key2 + Key3 "
                                  f"{modifier_1!r} {key_1!r} {key_2!r} {key_3!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_3, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger3: {trigger_3!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Key1 + Key2 "
                                  f"(Modifier1 {modifier_1!r} and Key3 {key_3!r} are released)")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_modifier_keys=[modifier_1], action_key=key_3, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger2: {trigger_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Key1")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_2, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger1: {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report with empty content")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_1, state=BREAK))

        self.testCaseChecked("BUS_FKC_0021", _AUTHOR)
    # end def test_pressing_multiple_trigger_keys_that_are_mapped_to_the_same_target_2

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Business')
    @services('KeyMatrix')
    def test_pressing_multiple_trigger_keys_that_are_mapped_to_the_same_target_3(self):
        """
        [FKC Behavior - FKC UX 1.37]
        Check the behavior when pressing multiple trigger keys that are mapped to the same target.
        Add below remappings to test it works as expected.

        Remapping:
        Trigger1 -> Modifier1 + Key1
        Trigger2 -> Modifier2 + Key1
        Trigger3 -> Modifier3 + Key1
        (Select 3 modifiers, 3 triggers and 1 key randomly.)
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        trigger_1 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY)
        trigger_2 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY, excluded_keys=[trigger_1])
        trigger_3 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY, excluded_keys=[trigger_1, trigger_2])
        modifier_1 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.MODIFIER_KEY)
        modifier_2 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.MODIFIER_KEY, excluded_keys=[modifier_1])
        modifier_3 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.MODIFIER_KEY, excluded_keys=[modifier_1, modifier_2])
        key_1 = random_generation_helper.get_random_non_modifier_key(test_case=self)
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_1,
                        action_modifier_keys=[modifier_1],
                        action_key=key_1),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_2,
                        action_modifier_keys=[modifier_2],
                        action_key=key_1),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_3,
                        action_modifier_keys=[modifier_3],
                        action_key=key_1),
        ]
        self.create_remapping_in_ram(preset_remapped_keys=preset_remapped_keys)

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold Trigger1 {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Modifier1 + Key1 {modifier_1!r} {key_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_modifier_keys=[modifier_1], action_key=key_1, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold the Trigger2: {trigger_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Modifier1 + Modifier2 + Key1 "
                                  f"{modifier_1!r} {modifier_2!r} {key_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_2, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold the Trigger3: {trigger_3!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Modifier1 + Modifier2 + Modifier3 + Key1 "
                                  f"{modifier_1!r} {modifier_2!r} {modifier_3!r} {key_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_3, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger3: {trigger_3!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Modifier1 + Modifier2 (Modifier3 and Key1 are released)")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_modifier_keys=[modifier_3], action_key=key_1, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger2: {trigger_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report Modifier1")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_2, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger1: {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report with empty content")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_1, state=BREAK))

        self.testCaseChecked("BUS_FKC_0022", _AUTHOR)
    # end def test_pressing_multiple_trigger_keys_that_are_mapped_to_the_same_target_3

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Business')
    @services('SimultaneousKeystrokes')
    def test_ability_to_overwrite_all_of_oob_fn_layer_remapping(self):
        """
        [Fn & GShift Layer - FKC UX 1.18]
        Check the ability to overwrite all of OOB Fn layer remapping. Add below remapping to test it works as expected.

        Remapping:
        Fn + TriggerX -> KeyX
        (Select X keys randomly. TriggerX: the combined key of OOB Fn layer remapping)
        (Exclude FKC toggle hotkeys and immersive lighting hotkeys)
        """
        # Configure key remapping
        fn_keys = FullKeyCustomizationTestUtils.FkcTableHelper.KeyProvider.get_remappable_oob_fn_keys(test_case=self)
        preset_remapped_keys = []
        for key in fn_keys:
            preset_remapped_keys.append(RemappedKey(
                layer=FkcMainTable.Layer.FN,
                action_type=RemappedKey.ActionType.KEYBOARD,
                trigger_key=key,
                action_key=RemappedKey.RandomKey.STANDARD_KEY))
        # end for
        remapped_keys = self.create_remapping_in_ram(preset_remapped_keys=preset_remapped_keys)

        # Send button stimuli and check results
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys, fn_key=KEY_ID.FN_KEY)

        self.testCaseChecked("BUS_FKC_0023", _AUTHOR)
    # end def test_ability_to_overwrite_all_of_oob_fn_layer_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Business')
    @services('KeyMatrix')
    def test_fn_gshift_layer_implicit_matching(self):
        """
        [Fn & GShift Layer - FKC UX 1.20]
        Check the implicit matching of single-key triggers will also apply to all single-key triggers in
        the FN and GShift layers. Add below remapping to test it works as expected.

        Remapping:
        Trigger1 -> GShift (Select the Trigger1 randomly)
        Fn + Trigger2 -> Key1
        Fn + Modifier1 + Trigger2 -> Key2
        GShift + Trigger2 -> Key1
        GShift + Modifier1 + Trigger2 -> Key2
        (Select 2 triggers and 2 keys randomly.)
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        modifier_1 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.MODIFIER_KEY)
        modifier_2 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.MODIFIER_KEY, excluded_keys=[modifier_1])
        trigger_1 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY)
        trigger_2 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY, excluded_keys=[trigger_1],
            fn_trigger_remapping=True)
        key_1 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.MODIFIER_KEY, excluded_keys=[modifier_1, modifier_2])
        key_2 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.STANDARD_KEY, excluded_keys=[modifier_1, modifier_2, key_1])
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.VIRTUAL_MODIFIER,
                        trigger_key=trigger_1,
                        action_key=KEY_ID.G_SHIFT),
            RemappedKey(layer=FkcMainTable.Layer.FN,
                        action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_2,
                        action_key=key_1),
            RemappedKey(layer=FkcMainTable.Layer.FN,
                        action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_modifier_keys=[modifier_1],
                        trigger_key=trigger_2,
                        action_key=key_2),
            RemappedKey(layer=FkcMainTable.Layer.GSHIFT,
                        action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_2,
                        action_key=key_1),
            RemappedKey(layer=FkcMainTable.Layer.GSHIFT,
                        action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_modifier_keys=[modifier_1],
                        trigger_key=trigger_2,
                        action_key=key_2),
        ]
        self.create_remapping_in_nvs(preset_remapped_keys=preset_remapped_keys)

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Perform Fn + Modifier2 {modifier_2!r} + Trigger2 {trigger_2!r} "
                                 "combination key properly")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.build_key_sequence(
            test_case=self, remapped_key=RemappedKey(layer=FkcMainTable.Layer.FN,
                                                     trigger_modifier_keys=[modifier_2],
                                                     trigger_key=trigger_2), fn_key=KEY_ID.FN_KEY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Modifier2 {modifier_2!r} + Key1 {key_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_2, state=MAKE))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(test_case=self,
                                                                          remapped_key=preset_remapped_keys[1])
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_2, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Perform Fn + Modifier1 {modifier_1!r} + Trigger2 {trigger_2!r} "
                                 "combination key properly")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.build_key_sequence(
            test_case=self, remapped_key=preset_remapped_keys[2], fn_key=KEY_ID.FN_KEY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Key2 {key_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(test_case=self,
                                                                          remapped_key=preset_remapped_keys[2])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Perform GShift + Modifier2 {modifier_2!r} + Trigger2 {trigger_2!r} "
                                 "combination key properly")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.build_key_sequence(
            test_case=self, remapped_key=RemappedKey(layer=FkcMainTable.Layer.GSHIFT,
                                                     trigger_modifier_keys=[modifier_2],
                                                     trigger_key=trigger_2), gshift_key=trigger_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Modifier2 {modifier_2!r} + Key1 {key_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_2, state=MAKE))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(test_case=self,
                                                                          remapped_key=preset_remapped_keys[3])
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=modifier_2, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Perform GShift + Modifier1 {modifier_1!r} + Trigger2 {trigger_2!r} "
                                 "combination key properly")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.build_key_sequence(
            test_case=self, remapped_key=preset_remapped_keys[4], gshift_key=trigger_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Key2 {key_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(test_case=self,
                                                                          remapped_key=preset_remapped_keys[4])

        self.testCaseChecked("BUS_FKC_0024", _AUTHOR)
    # end def test_fn_gshift_layer_implicit_matching

    @features('Keyboard')
    @features('FullKeyCustomization')
    @features('Feature8051')
    @level('Business')
    @services('SimultaneousKeystrokes')
    def test_fn_gshift_layer_default_behavior(self):
        """
        [Fn & GShift Layer - FKC UX 1.16.5]
        Check if the key is not customized, then the resulting behavior will revert back to a default behavior

        Remapping:
        GShift + Trigger1 -> Key1
        GShift + Trigger2 -> Key2
        Fn + Trigger3 -> Key3 (exclude FKC toggle hotkeys and immersive lighting hotkeys)
        Trigger4 -> Key4
        Trigger5 -> Key5
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        trigger_1 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY)
        trigger_2 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
            excluded_keys=[trigger_1])
        trigger_3 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
            excluded_keys=[trigger_1, trigger_2], fn_trigger_remapping=True)
        trigger_4 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.MODIFIER_KEY,
            excluded_keys=[trigger_1, trigger_2, trigger_3], fn_trigger_remapping=True)
        trigger_5 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.MODIFIER_KEY,
            excluded_keys=[trigger_1, trigger_2, trigger_3, trigger_4], fn_trigger_remapping=True)
        key_1 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.STANDARD_KEY)
        key_2 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.STANDARD_KEY, excluded_keys=[key_1])
        key_3 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.STANDARD_KEY, excluded_keys=[key_1, key_2])
        key_4 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY, excluded_keys=[key_1, key_2, key_3])
        key_5 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY, excluded_keys=[key_1, key_2, key_3, key_4])
        preset_remapped_keys = [
            RemappedKey(layer=FkcMainTable.Layer.GSHIFT,
                        action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_1,
                        action_key=key_1),
            RemappedKey(layer=FkcMainTable.Layer.GSHIFT,
                        action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_2,
                        action_key=key_2),
            RemappedKey(layer=FkcMainTable.Layer.FN,
                        action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_3,
                        action_key=key_3),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_4,
                        action_key=key_4),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_5,
                        action_key=key_5),
        ]
        self.create_remapping_in_nvs(preset_remapped_keys=preset_remapped_keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send 0x8051.setForcedPresedState with GShift = 1")
        # --------------------------------------------------------------------------------------------------------------
        LogiModifiersTestUtils.HIDppHelper.set_forced_pressed_state(test_case=self, g_shift=1, fn=0)
        get_forced_pressed_state_resp = LogiModifiersTestUtils.HIDppHelper.get_forced_pressed_state(test_case=self)
        self.assertEqual(expected=1, obtained=to_int(get_forced_pressed_state_resp.forced_pressed_state.g_shift))

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send a keystroke for Trigger1 {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.build_key_sequence(
            test_case=self, remapped_key=RemappedKey(trigger_key=trigger_1))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Key1 {key_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(test_case=self,
                                                                          remapped_key=preset_remapped_keys[0])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send a keystroke for a standard key {trigger_3!r} "
                                 f"(exclude Trigger1 {trigger_1!r} and Trigger2 {trigger_2!r})")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.build_key_sequence(
            test_case=self, remapped_key=RemappedKey(trigger_key=trigger_3))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report \"the standard key\" {trigger_3!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=trigger_3, state=MAKE))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=trigger_3, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send a keystroke for Trigger2 {trigger_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.build_key_sequence(
            test_case=self, remapped_key=RemappedKey(trigger_key=trigger_2))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Key2 {key_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(test_case=self,
                                                                          remapped_key=preset_remapped_keys[1])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press and hold Fn")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=KEY_ID.FN_KEY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send a keystroke for Trigger3 {trigger_3!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.build_key_sequence(
            test_case=self, remapped_key=RemappedKey(trigger_key=trigger_3))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Trigger3 {trigger_3!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=trigger_3, state=MAKE))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=trigger_3, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send a keystroke for Trigger4 {trigger_4!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.build_key_sequence(
            test_case=self, remapped_key=RemappedKey(trigger_key=trigger_4))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Trigger4 {trigger_4!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=trigger_4, state=MAKE))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=trigger_4, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send 0x8051.setForcedPresedState with GShift = 0")
        # --------------------------------------------------------------------------------------------------------------
        LogiModifiersTestUtils.HIDppHelper.set_forced_pressed_state(test_case=self, g_shift=0, fn=0)
        get_forced_pressed_state_resp = LogiModifiersTestUtils.HIDppHelper.get_forced_pressed_state(test_case=self)
        self.assertEqual(expected=0, obtained=to_int(get_forced_pressed_state_resp.forced_pressed_state.g_shift))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send a keystroke for Trigger3 {trigger_3!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.build_key_sequence(
            test_case=self, remapped_key=RemappedKey(trigger_key=trigger_3))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Key3 {key_3!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(test_case=self,
                                                                          remapped_key=preset_remapped_keys[2])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send a keystroke for Trigger5 {trigger_5!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.build_key_sequence(
            test_case=self, remapped_key=RemappedKey(trigger_key=trigger_5))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Trigger5 {trigger_5!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=trigger_5, state=MAKE))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=trigger_5, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Release Fn")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=KEY_ID.FN_KEY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send a keystroke for Trigger4 {trigger_4!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.build_key_sequence(
            test_case=self, remapped_key=preset_remapped_keys[3])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Key4 {key_4!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(test_case=self,
                                                                          remapped_key=preset_remapped_keys[3])

        self.testCaseChecked("BUS_FKC_0025", _AUTHOR)
    # end def test_fn_gshift_layer_default_behavior

    @features('Keyboard')
    @features('FullKeyCustomization')
    @features('Feature8051')
    @level('Business')
    @services('SimultaneousKeystrokes')
    def test_assign_gshift_by_x8051_on_onboard_mode(self):
        """
        [FKC + 0x8051 - FKC UX 4.3]
        Check the ability to assign GSHIFT to user actions on some other devices on the onboard mode.

        Remapping:
        GShift + Trigger1 -> Modifier1 + Key1
        (Select 1 modifier, 1 trigger and 1 key randomly.)
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        modifier_1 = random_generation_helper.get_random_modifier_key(test_case=self)
        trigger_1 = random_generation_helper.get_random_non_modifier_key(test_case=self)
        key_1 = random_generation_helper.get_random_non_modifier_key(test_case=self)
        preset_remapped_keys = [
            RemappedKey(layer=FkcMainTable.Layer.GSHIFT,
                        action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_1,
                        action_modifier_keys=[modifier_1],
                        action_key=key_1),
        ]
        self.create_remapping_in_nvs(preset_remapped_keys=preset_remapped_keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set to onboard mode by 0x8101.getSetMode")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.get_set_mode(test_case=self, set_onboard_mode=True,
                                                            onboard_mode=ProfileManagement.Mode.ONBOARD_MODE)
        get_set_mode = ProfileManagementTestUtils.HIDppHelper.get_set_mode(test_case=self, set_onboard_mode=False,
                                                                           onboard_mode=0)
        self.assertEqual(expected=ProfileManagement.Mode.ONBOARD_MODE,
                         obtained=to_int(get_set_mode.operating_mode_response.onboard_mode))

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send 0x8051.setForcedPresedState with GShift = 1")
        # --------------------------------------------------------------------------------------------------------------
        LogiModifiersTestUtils.HIDppHelper.set_forced_pressed_state(test_case=self, g_shift=1, fn=0)
        get_forced_pressed_state_resp = LogiModifiersTestUtils.HIDppHelper.get_forced_pressed_state(test_case=self)
        self.assertEqual(expected=1, obtained=to_int(get_forced_pressed_state_resp.forced_pressed_state.g_shift))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold Trigger1 {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_1)
        sleep(.05)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Modifier1 {modifier_1!r} +  Key1 {key_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_modifier_keys=[modifier_1], action_key=key_1, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger1 {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_1)
        sleep(.05)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report with empty content")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_modifier_keys=[modifier_1], action_key=key_1, state=BREAK))

        self.testCaseChecked("BUS_FKC_0026", _AUTHOR)
    # end def test_assign_gshift_by_x8051_on_onboard_mode

    @features('Keyboard')
    @features('FullKeyCustomization')
    @features('Feature8051')
    @level('Business')
    @services('SimultaneousKeystrokes')
    def test_assign_gshift_by_x8051_on_host_mode(self):
        """
        [FKC + 0x8051 - FKC UX 4.3]
        Check the ability to assign GSHIFT to user actions on some other devices on the host mode.

        Remapping:
        GShift + Trigger1 -> Modifier1 + Key1
        (Select 1 modifier, 1 trigger and 1 key randomly.)
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        modifier_1 = random_generation_helper.get_random_modifier_key(test_case=self)
        trigger_1 = random_generation_helper.get_random_non_modifier_key(test_case=self)
        key_1 = random_generation_helper.get_random_non_modifier_key(test_case=self)
        preset_remapped_keys = [
            RemappedKey(layer=FkcMainTable.Layer.GSHIFT,
                        action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_1,
                        action_modifier_keys=[modifier_1],
                        action_key=key_1),
        ]
        self.create_remapping_in_nvs(preset_remapped_keys=preset_remapped_keys,
                                     profile_file_type=ProfileManagement.FileTypeId.X8101.HOST_MODE_PROFILE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set to host mode by 0x8101.getSetMode")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.get_set_mode(test_case=self, set_onboard_mode=True,
                                                            onboard_mode=ProfileManagement.Mode.HOST_MODE)
        get_set_mode = ProfileManagementTestUtils.HIDppHelper.get_set_mode(
            test_case=self, set_onboard_mode=False, onboard_mode=ProfileManagement.Mode.HOST_MODE)
        self.assertEqual(expected=ProfileManagement.Mode.HOST_MODE,
                         obtained=to_int(get_set_mode.operating_mode_response.onboard_mode))

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send 0x8051.setForcedPresedState with GShift = 1")
        # --------------------------------------------------------------------------------------------------------------
        LogiModifiersTestUtils.HIDppHelper.set_forced_pressed_state(test_case=self, g_shift=1, fn=0)
        get_forced_pressed_state_resp = LogiModifiersTestUtils.HIDppHelper.get_forced_pressed_state(test_case=self)
        self.assertEqual(expected=1, obtained=to_int(get_forced_pressed_state_resp.forced_pressed_state.g_shift))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold Trigger1 {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=trigger_1)
        sleep(.05)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check received input report Modifier1 {modifier_1!r} +  Key1 {key_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_modifier_keys=[modifier_1], action_key=key_1, state=MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release Trigger1 {trigger_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=trigger_1)
        sleep(.05)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received input report with empty content")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_modifier_keys=[modifier_1], action_key=key_1, state=BREAK))

        self.testCaseChecked("BUS_FKC_0027", _AUTHOR)
    # end def test_assign_gshift_by_x8051_on_host_mode
# end class FKCBusinessTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
