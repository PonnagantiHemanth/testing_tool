#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.fkc.functionality
:brief: Hid Keyboard FKC business test suite
:author: Fred Chen <fchen7@logitech.com>
:date: 2023/03/30
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import sample

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.keyboard.keyboardinternationallayouts import KeyboardInternationalLayouts
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.fkcprofileformat import FkcMainTable
from pylibrary.mcu.fkcprofileformat import RemappedKey
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.controllistutils import ControlListTestUtils
from pytestbox.device.base.disablecontrolsbycidxutils import DisableControlsByCIDXTestUtils
from pytestbox.device.base.fullkeycustomizationutils import FullKeyCustomizationTestUtils
from pytestbox.device.base.layoututils import LayoutTestUtils
from pytestbox.device.hid.keyboard.fkc.fkc import FKCTestCase


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Fred Chen"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class FKCFunctionalityTestCase(FKCTestCase):
    """
    Validate Keyboard FKC functionality TestCases
    """

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    def test_trigger_to_action_remapping(self):
        """
        [Full-key remapping]
        For each customizable key, remap it to a possible target action.

        Possible actions:
        1. Standard Key
        2. Mouse Button
        3. Consumer code
        4. Macro (Create 10 macros with 5 standard keys by random selection)

        Remapping:
        Trigger -> Action (Random select an action for each trigger)
        """
        # Configure key remapping
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(
                full_keys=True,
                trigger_key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
                action_key_type=RemappedKey.RandomKey.STANDARD_KEY,
                action_types=(RemappedKey.ActionType.KEYBOARD, RemappedKey.ActionType.MOUSE,
                              RemappedKey.ActionType.CONSUMER, RemappedKey.ActionType.MACRO)),
            macro=random_parameters_cls.Macro(entry_count=10, command_count=5)))

        # Send button stimuli and check results
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys)

        self.testCaseChecked("FUN_FKC_0001", _AUTHOR)
    # end def test_trigger_to_action_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    def test_trigger_to_1m_key_remapping(self):
        """
        [Full-key remapping]
        For each customizable key, remap it to an action as 1 modifier + standard key (exclude modifier keys).

        Remapping:
        Trigger -> 1M + Key (Random select a modifier and a standard key for each trigger)
        """
        # Configure key remapping
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_ram(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(
                full_keys=True,
                trigger_key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
                action_key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY,
                action_modifiers=(1,))))

        # Send button stimuli and check results
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys)

        self.testCaseChecked("FUN_FKC_0002", _AUTHOR)
    # end def test_trigger_to_1m_key_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    def test_trigger_to_2m_key_remapping(self):
        """
        [Full-key remapping]
        For each customizable key, remap it to an action as 2 modifiers + standard key (exclude modifier keys).

        Remapping:
        Trigger -> 2M + Key (Random select 2 modifiers and a standard key for each trigger)
        """
        # Configure key remapping
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_ram(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(
                full_keys=True,
                trigger_key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
                action_key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY,
                action_modifiers=(2,))))

        # Send button stimuli and check results
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys)

        self.testCaseChecked("FUN_FKC_0003", _AUTHOR)
    # end def test_trigger_to_2m_key_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    def test_1m_trigger_to_action_remapping(self):
        """
        [Full-key remapping]
        For each customizable key with 1 modifier key, remap it to a possible target action.

        Possible actions:
        1. Standard Key
        2. Mouse Button
        3. Consumer code
        4. Macro (Create 10 macros with 5 standard keys by random selection)

        Remapping:
        1M + Trigger -> Action (Random select a modifier and a standard key for each trigger)
        """
        # Configure key remapping
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(
                full_keys=True, trigger_modifiers=(1,),
                trigger_key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY,
                action_key_type=RemappedKey.RandomKey.STANDARD_KEY,
                action_types=(RemappedKey.ActionType.KEYBOARD, RemappedKey.ActionType.MOUSE,
                              RemappedKey.ActionType.CONSUMER, RemappedKey.ActionType.MACRO)),
            macro=random_parameters_cls.Macro(entry_count=10, command_count=5)))

        # Send button stimuli and check results
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys)

        self.testCaseChecked("FUN_FKC_0004", _AUTHOR)
    # end def test_1m_trigger_to_action_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Functionality')
    @services('KeyMatrix')
    def test_2m_trigger_to_action_remapping(self):
        """
        Full-key remapping
        For each customizable key with 2 modifiers key, remap it to a possible target action.

        Possible actions:
        1. Standard Key
        2. Mouse Button
        3. Consumer code
        4. Macro (Create 10 macros with 5 standard keys by random selection)

        Remapping:
        2M + Trigger -> Action (Random select 2 modifiers and a standard key for each trigger)
        """
        # Configure key remapping
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(
                full_keys=True, trigger_modifiers=(2,),
                trigger_key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY,
                action_key_type=RemappedKey.RandomKey.STANDARD_KEY,
                action_types=(RemappedKey.ActionType.KEYBOARD, RemappedKey.ActionType.MOUSE,
                              RemappedKey.ActionType.CONSUMER, RemappedKey.ActionType.MACRO)),
            macro=random_parameters_cls.Macro(entry_count=10, command_count=5)))

        # Send button stimuli and check results
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys)

        self.testCaseChecked("FUN_FKC_0005", _AUTHOR)
    # end def test_2m_trigger_to_action_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    def test_1m_trigger_to_1m_key_remapping(self):
        """
        [Full-key remapping]
        For each customizable key with 1 modifier key, remap it to an action as 1 modifier + standard key
        (exclude modifier keys).

        Remapping:
        1M + Trigger -> 1M + Key (Random select 2 modifiers and a standard key for each trigger)
        """
        # Configure key remapping
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_ram(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(
                full_keys=True,
                trigger_modifiers=(1,), action_modifiers=(1,),
                trigger_key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY,
                action_key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY)))

        # Send button stimuli and check results
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys)

        self.testCaseChecked("FUN_FKC_0006", _AUTHOR)
    # end def test_1m_trigger_to_1m_key_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    def test_1m_trigger_to_2m_key_remapping(self):
        """
        [Full-key remapping]
        For each customizable key with 2 modifier keys, remap it to an action as 2 modifiers + standard key
        (exclude modifier keys).

        Remapping:
        2M + Trigger -> 2M + Key (Random select 4 modifiers and a standard key for each trigger)
        """
        # Configure key remapping
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_ram(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(
                full_keys=True,
                trigger_modifiers=(1,), action_modifiers=(2,),
                trigger_key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY,
                action_key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY)))

        # Send button stimuli and check results
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys)

        self.testCaseChecked("FUN_FKC_0007", _AUTHOR)
    # end def test_1m_trigger_to_2m_key_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    def test_fn_trigger_to_action_remapping(self):
        """
        [Full-key remapping]
        For each customizable key with Fn key, remap it to a possible target action.

        Possible actions:
        1. Standard Key
        2. Mouse Button
        3. Consumer code
        4. Macro (Create 10 macros with 5 standard keys by random selection)

        Remapping:
        Fn + Trigger -> Action (Random select an action for each trigger)
                               (Exclude the remappings of FKC toggle hotkeys and immersive lighting hotkeys)
        """
        # Configure key remapping
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            layer=FkcMainTable.Layer.FN,
            button=random_parameters_cls.Button(
                full_keys=True,
                trigger_key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
                action_key_type=RemappedKey.RandomKey.STANDARD_KEY,
                action_types=(RemappedKey.ActionType.KEYBOARD, RemappedKey.ActionType.MOUSE,
                              RemappedKey.ActionType.CONSUMER, RemappedKey.ActionType.MACRO)),
            macro=random_parameters_cls.Macro(entry_count=10, command_count=5)))

        # Send button stimuli and check results
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys, fn_key=KEY_ID.FN_KEY)

        self.testCaseChecked("FUN_FKC_0008", _AUTHOR)
    # end def test_fn_trigger_to_action_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    def test_fn_trigger_to_1m_key_remapping(self):
        """
        [Full-key remapping]
        For each customizable key with Fn key, remap it to an action as 1 modifier + standard key
        (exclude modifier keys).

        Remapping:
        Fn + Trigger -> 1M + Key (Random select a modifier and a standard key for each trigger)
                                 (Exclude the remappings as like FKC toggle hotkeys or immersive lighting hotkeys)
        """
        # Configure key remapping
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_ram(random_parameters=random_parameters_cls(
            layer=FkcMainTable.Layer.FN,
            button=random_parameters_cls.Button(
                full_keys=True, action_modifiers=(1,),
                trigger_key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
                action_key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY)))

        # Send button stimuli and check results
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys, fn_key=KEY_ID.FN_KEY)

        self.testCaseChecked("FUN_FKC_0009", _AUTHOR)
    # end def test_fn_trigger_to_1m_key_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    def test_fn_trigger_to_2m_key_remapping(self):
        """
        [Full-key remapping]
        For each customizable key with Fn key, remap it to an action as 2 modifiers + standard key
        (exclude modifier keys).

        Remapping:
        Fn + Trigger -> 2M + Key (Random select 2 modifiers and a standard key for each trigger)
                                 (Exclude the remappings as like FKC toggle hotkeys or immersive lighting hotkeys)
        """
        # Configure key remapping
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_ram(random_parameters=random_parameters_cls(
            layer=FkcMainTable.Layer.FN,
            button=random_parameters_cls.Button(
                full_keys=True, action_modifiers=(2,),
                trigger_key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
                action_key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY)))

        # Send button stimuli and check results
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys, fn_key=KEY_ID.FN_KEY)

        self.testCaseChecked("FUN_FKC_0010", _AUTHOR)
    # end def test_fn_trigger_to_2m_key_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Functionality')
    @services('KeyMatrix')
    def test_fn_1m_trigger_to_action_remapping(self):
        """
        [Full-key remapping]
        For each customizable key with Fn + 1 modifier key, remap it to a possible target action.

        Possible actions:
        1. Standard Key (exclude modifier keys)
        2. Mouse Button
        3. Consumer code
        4. Macro (Create 10 macros with 5 standard keys by random selection)

        Remapping:
        Fn + 1M + Trigger -> Action (Random select a modifier and an action for each trigger)
        """
        # Configure key remapping
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            layer=FkcMainTable.Layer.FN,
            button=random_parameters_cls.Button(
                full_keys=True, trigger_modifiers=(1,),
                trigger_key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY,
                action_key_type=RemappedKey.RandomKey.STANDARD_KEY,
                action_types=(RemappedKey.ActionType.KEYBOARD, RemappedKey.ActionType.MOUSE,
                              RemappedKey.ActionType.CONSUMER, RemappedKey.ActionType.MACRO)),
            macro=random_parameters_cls.Macro(entry_count=10, command_count=5)))

        # Send button stimuli and check results
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys, fn_key=KEY_ID.FN_KEY)

        self.testCaseChecked("FUN_FKC_0011", _AUTHOR)
    # end def test_fn_1m_trigger_to_action_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Functionality')
    @services('KeyMatrix')
    def test_fn_2m_trigger_to_action_remapping(self):
        """
        [Full-key remapping]
        For each customizable key with Fn + 2 modifiers key, remap it to a possible target action.

        Possible actions:
        1. Standard Key (exclude modifier keys)
        2. Mouse Button
        3. Consumer code
        4. Macro (Create 10 macros with 5 standard keys by random selection)

        Remapping:
        Fn + 2M + Trigger -> Action (Random select 2 modifiers and an action for each trigger)
        """
        # Configure key remapping
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            layer=FkcMainTable.Layer.FN,
            button=random_parameters_cls.Button(
                full_keys=True, trigger_modifiers=(2,),
                trigger_key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY,
                action_key_type=RemappedKey.RandomKey.STANDARD_KEY,
                action_types=(RemappedKey.ActionType.KEYBOARD, RemappedKey.ActionType.MOUSE,
                              RemappedKey.ActionType.CONSUMER, RemappedKey.ActionType.MACRO)),
            macro=random_parameters_cls.Macro(entry_count=10, command_count=5)))

        # Send button stimuli and check results
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys, fn_key=KEY_ID.FN_KEY)

        self.testCaseChecked("FUN_FKC_0012", _AUTHOR)
    # end def test_fn_2m__trigger_to_action_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Functionality')
    @services('KeyMatrix')
    def test_fn_1m_trigger_to_1m_key_remapping(self):
        """
        [Full-key remapping]
        For each customizable key with Fn + 1 modifier key, remap it to an action as 1 modifier + standard key
        (exclude modifier keys).

        Remapping:
        Fn + 1M + Trigger -> 1M + Key (Random select 2 modifiers and a standard key for each trigger)
        """
        # Configure key remapping
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_ram(random_parameters=random_parameters_cls(
            layer=FkcMainTable.Layer.FN,
            button=random_parameters_cls.Button(
                full_keys=True, trigger_modifiers=(1,), action_modifiers=(1,),
                trigger_key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY,
                action_key_type=RemappedKey.RandomKey.STANDARD_KEY)))

        # Send button stimuli and check results
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys, fn_key=KEY_ID.FN_KEY)

        self.testCaseChecked("FUN_FKC_0013", _AUTHOR)
    # end def test_fn_1m_trigger_to_1m_key_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Functionality')
    @services('KeyMatrix')
    def test_fn_2m_trigger_to_2m_key_remapping(self):
        """
        [Full-key remapping]
        For each customizable key with Fn + 2 modifier keys, remap it to an action as 2 modifiers + standard key
        (exclude modifier keys).

        Remapping:
        Fn + 2M + Trigger -> 2M + Key (Random select 4 modifiers and a standard key for each trigger)
        """
        # Configure key remapping
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_ram(random_parameters=random_parameters_cls(
            layer=FkcMainTable.Layer.FN,
            button=random_parameters_cls.Button(
                full_keys=True, trigger_modifiers=(2,), action_modifiers=(2,),
                trigger_key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY,
                action_key_type=RemappedKey.RandomKey.STANDARD_KEY)))

        # Send button stimuli and check results
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys, fn_key=KEY_ID.FN_KEY)

        self.testCaseChecked("FUN_FKC_0014", _AUTHOR)
    # end def test_fn_2m_trigger_to_2m_key_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    def test_gshift_trigger_to_action_remapping(self):
        """
        [Full-key remapping]
        For each customizable key with GShift key, remap it to a possible target action.

        Possible actions:
        1. Standard Key
        2. Mouse Button
        3. Consumer code
        4. Macro (Create 10 macros with 5 standard keys by random selection)

        Remapping:
        Trigger1 -> GShift (Select the Trigger1 randomly from non-modifier keys)
        GShift + Trigger -> Action (Random select an action for each trigger)
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        trigger_1 = random_generation_helper.get_random_non_modifier_key(test_case=self)
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.VIRTUAL_MODIFIER,
                        trigger_key=trigger_1, action_key=KEY_ID.G_SHIFT),
        ]
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            layer=FkcMainTable.Layer.GSHIFT,
            button=random_parameters_cls.Button(
                full_keys=True,
                trigger_key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
                action_key_type=RemappedKey.RandomKey.STANDARD_KEY,
                action_types=(RemappedKey.ActionType.KEYBOARD, RemappedKey.ActionType.MOUSE,
                              RemappedKey.ActionType.CONSUMER, RemappedKey.ActionType.MACRO)),
            macro=random_parameters_cls.Macro(entry_count=10, command_count=5)),
            preset_remapped_keys=preset_remapped_keys,)

        # Send button stimuli and check results
        # Remove the Trigger1 remapped key in the remapped_keys list
        for remapped_key in remapped_keys:
            if remapped_key.trigger_key == trigger_1:
                remapped_keys.remove(remapped_key)
                break
            # end if
        # end for
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys, gshift_key=trigger_1)

        self.testCaseChecked("FUN_FKC_0015", _AUTHOR)
    # end def test_gshift_trigger_to_action_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    def test_gshift_trigger_to_1m_key_remapping(self):
        """
        [Full-key remapping]
        For each customizable key with GShift key, remap it to an action as 1 modifier + standard key
        (exclude modifier keys).

        Remapping:
        Trigger1 -> GShift (Select the Trigger1 randomly from non-modifier keys)
        GShift + Trigger -> 1M + Key (Random select a modifier and a standard key for each trigger)
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        trigger_1 = random_generation_helper.get_random_non_modifier_key(test_case=self)
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.VIRTUAL_MODIFIER,
                        trigger_key=trigger_1, action_key=KEY_ID.G_SHIFT),
        ]
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            layer=FkcMainTable.Layer.GSHIFT,
            button=random_parameters_cls.Button(
                full_keys=True, action_modifiers=(1,),
                trigger_key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
                action_key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY)),
            preset_remapped_keys=preset_remapped_keys, )

        # Send button stimuli and check results
        # Remove the Trigger1 remapped key in the remapped_keys list
        for remapped_key in remapped_keys:
            if remapped_key.trigger_key == trigger_1:
                remapped_keys.remove(remapped_key)
                break
            # end if
        # end for
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys, gshift_key=trigger_1)

        self.testCaseChecked("FUN_FKC_0016", _AUTHOR)
    # end def test_gshift_trigger_to_1m_key_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    def test_gshift_trigger_to_2m_key_remapping(self):
        """
        [Full-key remapping]
        For each customizable key with GShift key, remap it to an action as 2 modifiers + standard key
        (exclude modifier keys).

        Remapping:
        Trigger1 -> GShift (Select the Trigger1 randomly from non-modifier keys)
        GShift + Trigger -> 2M + Key (Random select 2 modifiers and a standard key for each trigger)
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        trigger_1 = random_generation_helper.get_random_non_modifier_key(test_case=self)
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.VIRTUAL_MODIFIER,
                        trigger_key=trigger_1, action_key=KEY_ID.G_SHIFT),
        ]
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            layer=FkcMainTable.Layer.GSHIFT,
            button=random_parameters_cls.Button(
                full_keys=True, action_modifiers=(2,),
                trigger_key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
                action_key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY)),
            preset_remapped_keys=preset_remapped_keys, )

        # Send button stimuli and check results
        # Remove the Trigger1 remapped key in the remapped_keys list
        for remapped_key in remapped_keys:
            if remapped_key.trigger_key == trigger_1:
                remapped_keys.remove(remapped_key)
                break
            # end if
        # end for
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys, gshift_key=trigger_1)

        self.testCaseChecked("FUN_FKC_0017", _AUTHOR)
    # end def test_gshift_trigger_to_2m_key_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Functionality')
    @services('KeyMatrix')
    def test_gshift_1m_trigger_to_action_remapping(self):
        """
        [Full-key remapping]
        For each customizable key with GShift + 1 modifier key, remap it to a possible target action.

        Possible actions:
        1. Standard Key
        2. Mouse Button
        3. Consumer code
        4. Macro (Create 10 macros with 5 standard keys by random selection)

        Remapping:
        Trigger1 -> GShift (Select the Trigger1 randomly from non-modifier keys)
        GShift + 1M + Trigger -> Action (Random select a modifier and an action for each trigger)
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        trigger_1 = random_generation_helper.get_random_non_modifier_key(test_case=self)
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.VIRTUAL_MODIFIER,
                        trigger_key=trigger_1, action_key=KEY_ID.G_SHIFT),
        ]
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            layer=FkcMainTable.Layer.GSHIFT,
            button=random_parameters_cls.Button(
                full_keys=True, trigger_modifiers=(1,),
                trigger_key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY,
                action_key_type=RemappedKey.RandomKey.STANDARD_KEY,
                action_types=(RemappedKey.ActionType.KEYBOARD, RemappedKey.ActionType.MOUSE,
                              RemappedKey.ActionType.CONSUMER, RemappedKey.ActionType.MACRO)),
            macro=random_parameters_cls.Macro(entry_count=10, command_count=5)),
            preset_remapped_keys=preset_remapped_keys,)

        # Send button stimuli and check results
        # Remove the Trigger1 remapped key in the remapped_keys list
        for remapped_key in remapped_keys:
            if remapped_key.trigger_key == trigger_1:
                remapped_keys.remove(remapped_key)
                break
            # end if
        # end for
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys, gshift_key=trigger_1)

        self.testCaseChecked("FUN_FKC_0018", _AUTHOR)
    # end def test_gshift_1m_trigger_to_action_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Functionality')
    @services('KeyMatrix')
    def test_gshift_2m_trigger_to_action_remapping(self):
        """
        [Full-key remapping]
        For each customizable key with GShift + 2 modifier key, remap it to a possible target action.

        Possible actions:
        1. Standard Key
        2. Mouse Button
        3. Consumer code
        4. Macro (Create 10 macros with 5 standard keys by random selection)

        Remapping:
        Trigger1 -> GShift (Select the Trigger1 randomly from non-modifier keys)
        GShift + 2M + Trigger -> Action (Random select 2 modifiers and an action for each trigger)
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        trigger_1 = random_generation_helper.get_random_non_modifier_key(test_case=self)
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.VIRTUAL_MODIFIER,
                        trigger_key=trigger_1, action_key=KEY_ID.G_SHIFT),
        ]
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            layer=FkcMainTable.Layer.GSHIFT,
            button=random_parameters_cls.Button(
                full_keys=True, trigger_modifiers=(2,),
                trigger_key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY,
                action_key_type=RemappedKey.RandomKey.STANDARD_KEY,
                action_types=(RemappedKey.ActionType.KEYBOARD, RemappedKey.ActionType.MOUSE,
                              RemappedKey.ActionType.CONSUMER, RemappedKey.ActionType.MACRO)),
            macro=random_parameters_cls.Macro(entry_count=10, command_count=5)),
            preset_remapped_keys=preset_remapped_keys,)

        # Send button stimuli and check results
        # Remove the Trigger1 remapped key in the remapped_keys list
        for remapped_key in remapped_keys:
            if remapped_key.trigger_key == trigger_1:
                remapped_keys.remove(remapped_key)
                break
            # end if
        # end for
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys, gshift_key=trigger_1)

        self.testCaseChecked("FUN_FKC_0019", _AUTHOR)
    # end def test_gshift_2m__trigger_to_action_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Functionality')
    @services('KeyMatrix')
    def test_gshift_1m_trigger_to_1m_key_remapping(self):
        """
        [Full-key remapping]
        For each customizable key with GShift + 1 modifier key, remap it to an action as 1 modifier + standard key
        (exclude modifier keys).

        Possible actions:
        1. Standard Key (exclude modifier keys)
        2. Mouse Button
        3. Consumer code
        4. Macro (Create 10 macros with 5 standard keys by random selection)

        Remapping:
        Trigger1 -> GShift (Select the Trigger1 randomly from non-modifier keys)
        GShift + 1M + Trigger -> 1M + Key (Random select 2 modifiers and a standard key for each trigger)
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        trigger_1 = random_generation_helper.get_random_non_modifier_key(test_case=self)
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.VIRTUAL_MODIFIER,
                        trigger_key=trigger_1, action_key=KEY_ID.G_SHIFT),
        ]
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            layer=FkcMainTable.Layer.GSHIFT,
            button=random_parameters_cls.Button(
                full_keys=True, trigger_modifiers=(1,), action_modifiers=(1,),
                trigger_key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY,
                action_key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY)),
            preset_remapped_keys=preset_remapped_keys,)

        # Send button stimuli and check results
        # Remove the Trigger1 remapped key in the remapped_keys list
        for remapped_key in remapped_keys:
            if remapped_key.trigger_key == trigger_1:
                remapped_keys.remove(remapped_key)
                break
            # end if
        # end for
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys, gshift_key=trigger_1)

        self.testCaseChecked("FUN_FKC_0020", _AUTHOR)
    # end def test_gshift_1m_trigger_to_1m_key_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Functionality')
    @services('KeyMatrix')
    def test_gshift_2m_trigger_to_2m_key_remapping(self):
        """
        [Full-key remapping]
        For each customizable key with GShift + 2 modifier keys, remap it to an action as 2 modifiers + standard key
        (exclude modifier keys).

        Possible actions:
        1. Standard Key (exclude modifier keys)
        2. Mouse Button
        3. Consumer code
        4. Macro (Create 10 macros with 5 standard keys by random selection)

        Remapping:
        Trigger1 -> GShift (Select the Trigger1 randomly from non-modifier keys)
        GShift + 2M + Trigger -> 2M + Key (Random select 4 modifiers and a standard key for each trigger)
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        trigger_1 = random_generation_helper.get_random_non_modifier_key(test_case=self)
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.VIRTUAL_MODIFIER,
                        trigger_key=trigger_1, action_key=KEY_ID.G_SHIFT),
        ]
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            layer=FkcMainTable.Layer.GSHIFT,
            button=random_parameters_cls.Button(
                full_keys=True, trigger_modifiers=(2,), action_modifiers=(2,),
                trigger_key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY,
                action_key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY)),
            preset_remapped_keys=preset_remapped_keys,)

        # Send button stimuli and check results
        # Remove the Trigger1 remapped key in the remapped_keys list
        for remapped_key in remapped_keys:
            if remapped_key.trigger_key == trigger_1:
                remapped_keys.remove(remapped_key)
                break
            # end if
        # end for
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys, gshift_key=trigger_1)

        self.testCaseChecked("FUN_FKC_0021", _AUTHOR)
    # end def test_gshift_2m_trigger_to_2m_key_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    def test_jpn_trigger_to_action_remapping(self):
        """
        [FKC + Keyboard layout - JPN]
        For each customizable key in the Japanese key layout, remap it to a possible target action.

        Possible actions:
        1. Standard Key
        2. Mouse Button
        3. Consumer code
        4. Macro (Create 10 macros with 5 standard keys by random selection)

        Remapping:
        Trigger -> Action (Random select an action for each trigger)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to JPN")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        self.post_requisite_refresh_cid_list = True
        LayoutTestUtils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.JAPANESE)
        ControlListTestUtils.refresh_cid_list(test_case=self)

        # Configure key remapping
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(
                full_keys=True,
                trigger_key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
                action_key_type=RemappedKey.RandomKey.STANDARD_KEY,
                action_types=(RemappedKey.ActionType.KEYBOARD, RemappedKey.ActionType.MOUSE,
                              RemappedKey.ActionType.CONSUMER, RemappedKey.ActionType.MACRO)),
            macro=random_parameters_cls.Macro(entry_count=10, command_count=5)))

        # Send button stimuli and check results
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys)

        self.testCaseChecked("FUN_FKC_0022", _AUTHOR)
    # end def test_jpn_trigger_to_action_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    def test_jpn_fn_trigger_to_action_remapping(self):
        """
        [FKC + Keyboard layout - JPN]
        For each customizable key with Fn key in the Japanese key layout, remap it to a possible target action.

        Possible actions:
        1. Standard Key
        2. Mouse Button
        3. Consumer code
        4. Macro (Create 10 macros with 5 standard keys by random selection)

        Remapping:
        Fn + Trigger -> Action (Random select an action for each trigger)
                               (Exclude the remappings as like FKC toggle hotkeys or immersive lighting hotkeys)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to JPN")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        self.post_requisite_refresh_cid_list = True
        LayoutTestUtils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.JAPANESE)
        ControlListTestUtils.refresh_cid_list(test_case=self)

        # Configure key remapping
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            layer=FkcMainTable.Layer.FN,
            button=random_parameters_cls.Button(
                full_keys=True,
                trigger_key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
                action_key_type=RemappedKey.RandomKey.STANDARD_KEY,
                action_types=(RemappedKey.ActionType.KEYBOARD, RemappedKey.ActionType.MOUSE,
                              RemappedKey.ActionType.CONSUMER, RemappedKey.ActionType.MACRO)),
            macro=random_parameters_cls.Macro(entry_count=10, command_count=5)))

        # Send button stimuli and check results
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys, fn_key=KEY_ID.FN_KEY)

        self.testCaseChecked("FUN_FKC_0023", _AUTHOR)
    # end def test_jpn_fn_trigger_to_action_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    def test_jpn_gshift_trigger_to_action_remapping(self):
        """
        [FKC + Keyboard layout - JPN]
        For each customizable key with GShift key in the Japanese key layout, remap it to a possible target action.

        Possible actions:
        1. Standard Key
        2. Mouse Button
        3. Consumer code
        4. Macro (Create 10 macros with 5 standard keys by random selection)

        Remapping:
        GShift + Trigger -> Action (Random select an action for each trigger)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to JPN")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        self.post_requisite_refresh_cid_list = True
        LayoutTestUtils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.JAPANESE)
        ControlListTestUtils.refresh_cid_list(test_case=self)

        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        trigger_1 = random_generation_helper.get_random_modifier_key(test_case=self)
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.VIRTUAL_MODIFIER,
                        trigger_key=trigger_1, action_key=KEY_ID.G_SHIFT),
        ]
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            layer=FkcMainTable.Layer.GSHIFT,
            button=random_parameters_cls.Button(
                full_keys=True,
                trigger_key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
                action_key_type=RemappedKey.RandomKey.STANDARD_KEY,
                action_types=(RemappedKey.ActionType.KEYBOARD, RemappedKey.ActionType.MOUSE,
                              RemappedKey.ActionType.CONSUMER, RemappedKey.ActionType.MACRO)),
            macro=random_parameters_cls.Macro(entry_count=10, command_count=5)),
            preset_remapped_keys=preset_remapped_keys,)

        # Send button stimuli and check results
        # Remove the Trigger1 remapped key in the remapped_keys list
        for remapped_key in remapped_keys:
            if remapped_key.trigger_key == trigger_1:
                remapped_keys.remove(remapped_key)
                break
            # end if
        # end for
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys, gshift_key=trigger_1)

        self.testCaseChecked("FUN_FKC_0024", _AUTHOR)
    # end def test_jpn_gshift_trigger_to_action_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    def test_uk_trigger_to_action_remapping(self):
        """
        [FKC + Keyboard layout - UK]
        For each customizable key in the United Kingdom key layout, remap it to a possible target action.

        Possible actions:
        1. Standard Key
        2. Mouse Button
        3. Consumer code
        4. Macro (Create 10 macros with 5 standard keys by random selection)

        Remapping:
        Trigger -> Action (Random select an action for each trigger)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to UK")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        self.post_requisite_refresh_cid_list = True
        LayoutTestUtils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.UK)
        ControlListTestUtils.refresh_cid_list(test_case=self)

        # Configure key remapping
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(
                full_keys=True,
                trigger_key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
                action_key_type=RemappedKey.RandomKey.STANDARD_KEY,
                action_types=(RemappedKey.ActionType.KEYBOARD, RemappedKey.ActionType.MOUSE,
                              RemappedKey.ActionType.CONSUMER, RemappedKey.ActionType.MACRO)),
            macro=random_parameters_cls.Macro(entry_count=10, command_count=5)))

        # Send button stimuli and check results
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys)

        self.testCaseChecked("FUN_FKC_0025", _AUTHOR)
    # end def test_uk_trigger_to_action_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    def test_uk_fn_trigger_to_action_remapping(self):
        """
        [FKC + Keyboard layout - UK]
        For each customizable key in the United Kingdom key layout, remap it to a possible target action.

        Possible actions:
        1. Standard Key
        2. Mouse Button
        3. Consumer code
        4. Macro (Create 10 macros with 5 standard keys by random selection)

        Remapping:
        Fn + Trigger -> Action (Random select an action for each trigger)
                               (Exclude the remappings as like FKC toggle hotkeys or immersive lighting hotkeys)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to UK")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        self.post_requisite_refresh_cid_list = True
        LayoutTestUtils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.UK)
        ControlListTestUtils.refresh_cid_list(test_case=self)

        # Configure key remapping
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            layer=FkcMainTable.Layer.FN,
            button=random_parameters_cls.Button(
                full_keys=True,
                trigger_key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
                action_key_type=RemappedKey.RandomKey.STANDARD_KEY,
                action_types=(RemappedKey.ActionType.KEYBOARD, RemappedKey.ActionType.MOUSE,
                              RemappedKey.ActionType.CONSUMER, RemappedKey.ActionType.MACRO)),
            macro=random_parameters_cls.Macro(entry_count=10, command_count=5)))

        # Send button stimuli and check results
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys, fn_key=KEY_ID.FN_KEY)

        self.testCaseChecked("FUN_FKC_0026", _AUTHOR)
    # end def test_uk_fn_trigger_to_action_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    def test_uk_gshift_trigger_to_action_remapping(self):
        """
        [FKC + Keyboard layout - UK]
        For each customizable key with GShift key in the United Kingdom key layout, remap it to a possible target
        action.

        Possible actions:
        1. Standard Key
        2. Mouse Button
        3. Consumer code
        4. Macro (Create 10 macros with 5 standard keys by random selection)

        Remapping:
        GShift + Trigger -> Action (Random select an action for each trigger)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to UK")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        self.post_requisite_refresh_cid_list = True
        LayoutTestUtils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.UK)
        ControlListTestUtils.refresh_cid_list(test_case=self)

        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        trigger_1 = random_generation_helper.get_random_modifier_key(test_case=self)
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.VIRTUAL_MODIFIER,
                        trigger_key=trigger_1, action_key=KEY_ID.G_SHIFT),
        ]
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            layer=FkcMainTable.Layer.GSHIFT,
            button=random_parameters_cls.Button(
                full_keys=True,
                trigger_key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
                action_key_type=RemappedKey.RandomKey.STANDARD_KEY,
                action_types=(RemappedKey.ActionType.KEYBOARD, RemappedKey.ActionType.MOUSE,
                              RemappedKey.ActionType.CONSUMER, RemappedKey.ActionType.MACRO)),
            macro=random_parameters_cls.Macro(entry_count=10, command_count=5)),
            preset_remapped_keys=preset_remapped_keys,)

        # Send button stimuli and check results
        # Remove the Trigger1 remapped key in the remapped_keys list
        for remapped_key in remapped_keys:
            if remapped_key.trigger_key == trigger_1:
                remapped_keys.remove(remapped_key)
                break
            # end if
        # end for
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys, gshift_key=trigger_1)

        self.testCaseChecked("FUN_FKC_0027", _AUTHOR)
    # end def test_uk_gshift_trigger_to_action_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @features('Feature4523')
    @level('Functionality')
    @services('GameModeButton')
    @services('SimultaneousKeystrokes')
    def test_priority_order_disable_keys(self):
        """
        [FKC Priority Order with 0x4523 + Game Mode UX.1]
        For each customizable key, remap it to a standard key. Then select 10 customizable keys and set as
        disabled key. Validate the disable keys have higher priority while enabled the Game mode.

        Remapping:
        Trigger -> Key

        Disabled keys:
        Select 10 standard keys randomly
        """
        all_remappable_keys = FullKeyCustomizationTestUtils.FkcTableHelper.KeyProvider.trigger_key_get_key_list(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY)
        disabled_keys = sample(all_remappable_keys, 10)
        disabled_cidx_list = [ControlListTestUtils.key_id_to_cidx(test_case=self, key_id=key) for key in disabled_keys]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Disabled Control Id list: {disabled_cidx_list}")
        # --------------------------------------------------------------------------------------------------------------
        # Configure key remapping
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(
                full_keys=True,
                trigger_key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY,
                action_key_type=RemappedKey.RandomKey.STANDARD_KEY,
                action_types=(RemappedKey.ActionType.KEYBOARD,))),
            disabled_keys=DisableControlsByCIDXTestUtils.convert_to_hexlist(disabled_cidx_list=disabled_cidx_list))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Turn on Game mode by game mode button/slide switch")
        # --------------------------------------------------------------------------------------------------------------
        DisableControlsByCIDXTestUtils.HIDppHelper.get_parameters(test_case=self)  # To update the feature mapping table
        self.game_mode_emulator.set_mode(activate_game_mode=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait 0x4523.gameModeEvent then check the enabled state is True")
        # --------------------------------------------------------------------------------------------------------------
        game_mode_event = DisableControlsByCIDXTestUtils.HIDppHelper.game_mode_event(test_case=self)
        self.assertEqual(expected=True, obtained=game_mode_event.game_mode_state.enabled)

        # Send button stimuli and check results
        disabled_remapped_keys = [key for key in remapped_keys if key.trigger_cidx in disabled_cidx_list]
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        self.build_key_test_sequence(remapped_keys=disabled_remapped_keys, block=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check no HID report after sent keystroke for disable remapped keys")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        available_remapped_keys = [key for key in remapped_keys if key.trigger_cidx not in disabled_cidx_list]
        self.build_key_test_sequence_and_validate_result(remapped_keys=available_remapped_keys)

        self.testCaseChecked("FUN_FKC_0028", _AUTHOR)
    # end def test_priority_order_disable_keys
# end class FKCFunctionalityTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
