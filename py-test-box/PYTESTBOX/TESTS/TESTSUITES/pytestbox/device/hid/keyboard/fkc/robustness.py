#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.fkc.robustness
:brief: Hid Keyboard FKC robustness test suite
:author: Fred Chen <fchen7@logitech.com>
:date: 2023/06/17
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.rgbeffects import RGBEffects
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.fkcprofileformat import FkcMainTable
from pylibrary.mcu.fkcprofileformat import RemappedKey
from pylibrary.tools.numeral import to_int
from pylibrary.tools.threadutils import QueueEmpty
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.controllistutils import ControlListTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.fullkeycustomizationutils import FullKeyCustomizationTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.base.rgbeffectsutils import RGBEffectsTestUtils
from pytestbox.device.hid.keyboard.fkc.fkc import FKCTestCase


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Fred Chen"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class FKCRobustnessTestCase(FKCTestCase):
    """
    Validate Keyboard FKC robustness TestCases
    """

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Robustness')
    @services('SimultaneousKeystrokes')
    def test_trigger_to_8m_key_remapping(self):
        """
        [Stress Test]
        Select 5 customizable keys. For each selected key, remap it to an action as 8 modifiers + standard key
        (exclude modifier keys).

        Remapping: [Trigger -> 8M + Key]
        Trigger1 -> 8M + Key1
        Trigger2 -> 8M + Key2
        Trigger3 -> 8M + Key3
        Trigger4 -> 8M + Key4
        Trigger5 -> 8M + Key5
        (Select 5 triggers and 5 keys randomly.)
        """
        # Configure key remapping
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_ram(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(count=5,
                                                action_types=(RemappedKey.ActionType.KEYBOARD,),
                                                action_modifiers=(8,))))

        # Send button stimuli and check results
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys)

        self.testCaseChecked("ROB_FKC_0001", _AUTHOR)
    # end def test_trigger_to_8m_key_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Robustness')
    @services('KeyMatrix')
    def test_4m_trigger_to_action_remapping(self):
        """
        [Stress Test]
        Select 5 customizable keys. For each selected key with 4 modifier keys, remap the combined keys to
        a possible action.

        Possible actions:
        1. Standard Key (exclude modifier keys)
        2. Mouse Button
        3. Consumer code
        4. Macro (Create 1 macro with 5 standard keys by random selection)

        Remapping: [4M + Trigger -> Action]
        4M + Trigger1 -> Action1 (Random select 4 modifiers for each trigger)
        4M + Trigger2 -> Action2
        4M + Trigger3 -> Action3
        4M + Trigger4 -> Action4
        4M + Trigger5 -> Action5
        (Select 5 triggers and 5 actions randomly.)
        """
        # Configure key remapping
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(
                count=5, action_types=(RemappedKey.ActionType.KEYBOARD, RemappedKey.ActionType.MOUSE,
                                       RemappedKey.ActionType.CONSUMER, RemappedKey.ActionType.MACRO),
                trigger_modifiers=(4,)),
            macro=random_parameters_cls.Macro(entry_count=1, command_count=5)))

        # Send button stimuli and check results
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys)

        self.testCaseChecked("ROB_FKC_0002", _AUTHOR)
    # end def test_4m_trigger_to_action_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Robustness')
    @services('KeyMatrix')
    def test_4m_trigger_to_8m_key_remapping(self):
        """
        [Stress Test]
        Select 5 customizable keys. For each selected key with 4 modifier keys, remap it to
        8 modifiers + standard key (exclude modifier keys).

        Remapping: [4M + Trigger -> 8M + Key]
        4M + Trigger1 -> 8M + Key1 (Random select 4 modifiers for each trigger)
        4M + Trigger2 -> 8M + Key2
        4M + Trigger3 -> 8M + Key3
        4M + Trigger4 -> 8M + Key4
        4M + Trigger5 -> 8M + Key5
        (Select 5 triggers and 5 actions randomly.)
        """
        # Configure key remapping
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_ram(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(count=5,  trigger_modifiers=(4,), action_modifiers=(8,))))

        # Send button stimuli and check results
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys)

        self.testCaseChecked("ROB_FKC_0003", _AUTHOR)
    # end def test_4m_trigger_to_8m_key_remapping

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Robustness')
    @services('SimultaneousKeystrokes')
    def test_priority_order_fkc_toggle_keys(self):
        """
        [FKC Priority Order]
        Remap FKC toggle hotkey to a standard key (exclude modifier keys). Check there is no effect for the remapping.

        Remapping:
        60% KBD: Fn + a -> Key1
        FS TKL KDB: Fn + F1 -> Key1
        Both (60% and FS TKL KDB)
            Left Ctrl + Caps Lock -> Key2
            Left Alt + Caps Lock -> Key3
            Right Ctrl + Enter -> Key4
            Fn + Enter -> Key5
            Right Ctrl + Caps Lock -> Key6
            Left Alt + Enter -> Key7
            Left Ctrl + Enter -> Key8
        (Random select Key1 ~ Key8)
        """
        # Configure key remapping
        toggle_key_pairs = []
        for index in range(8):
            cidx_pair = getattr(self.f.PRODUCT.FEATURES.COMMON.FULL_KEY_CUSTOMIZATION, f'F_ToggleKey{index}Cidx')
            toggle_key_pairs.append(
                [ControlListTestUtils.cidx_to_key_id(test_case=self, cid_index=to_int(cidx_pair[0])),
                 ControlListTestUtils.cidx_to_key_id(test_case=self, cid_index=to_int(cidx_pair[1]))])
        # end for
        preset_remapped_keys = []
        for toggle_hot_key in toggle_key_pairs:
            if toggle_hot_key[0] == KEY_ID.FN_KEY:
                preset_remapped_keys.append(RemappedKey(
                    layer=FkcMainTable.Layer.FN, action_type=RemappedKey.ActionType.MOUSE,
                    trigger_key=toggle_hot_key[1], action_key=RemappedKey.RandomKey.MOUSE_BUTTON))
            else:
                preset_remapped_keys.append(RemappedKey(
                    action_type=RemappedKey.ActionType.MOUSE, trigger_modifier_keys=[toggle_hot_key[0]],
                    trigger_key=toggle_hot_key[1], action_key=RemappedKey.RandomKey.MOUSE_BUTTON))
            # end if
        # end for
        remapped_keys = self.create_remapping_in_nvs(preset_remapped_keys=preset_remapped_keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Disable all of FKC toggle hotkeys")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            test_case=self, set_toggle_keys_enabled=True, set_fkc_enabled=False, toggle_keys_enabled=0x00)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Build the test sequence and validate results")
        # --------------------------------------------------------------------------------------------------------------
        self.build_key_test_sequence_and_validate_result(remapped_keys=remapped_keys, fn_key=KEY_ID.FN_KEY, block=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable all of FKC toggle hotkeys")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            test_case=self, set_toggle_keys_enabled=True, set_fkc_enabled=False, toggle_keys_enabled=0xFF)

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        fkc_enabled = True
        for remapped_key in remapped_keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Perform the FKC toggle hotkey {remapped_key} properly.")
            # ----------------------------------------------------------------------------------------------------------
            FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.build_key_sequence(test_case=self,
                                                                                remapped_key=remapped_key,
                                                                                fn_key=KEY_ID.FN_KEY)

            fkc_enabled = not fkc_enabled
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check the FKC enabled status has been changed to {fkc_enabled}")
            # ----------------------------------------------------------------------------------------------------------
            enable_disable_event = FullKeyCustomizationTestUtils.HIDppHelper.enable_disable_event(test_case=self)
            checker = FullKeyCustomizationTestUtils.EnableDisableEventChecker
            check_map = checker.get_default_check_map(test_case=self)
            failure_enable_state_check_map = \
                FullKeyCustomizationTestUtils.FkcFailureEnabledStateChecker.get_default_check_map(test_case=self)
            failure_enable_state_check_map.update({
                "enabled": (FullKeyCustomizationTestUtils.FkcFailureEnabledStateChecker.check_enabled, fkc_enabled)
            })
            check_map.update({
                'fkc_failure_enabled_state': (checker.check_fkc_failure_enabled_state, failure_enable_state_check_map)
            })
            _, feature_1b05, _, _ = FullKeyCustomizationTestUtils.HIDppHelper.get_parameters(test_case=self)
            checker.check_fields(test_case=self, message=enable_disable_event,
                                 expected_cls=feature_1b05.enable_disable_event_cls, check_map=check_map)
        # end for

        self.testCaseChecked("ROB_FKC_0004", _AUTHOR)
    # end def test_priority_order_fkc_toggle_keys

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Robustness')
    @services('SimultaneousKeystrokes')
    @services('AtLeastOneKey', (KEY_ID.BACKLIGHT_UP, KEY_ID.BACKLIGHT_DOWN, KEY_ID.CYCLE_THROUGH_ANIMATION_EFFECTS,
                                KEY_ID.CYCLE_THROUGH_COLOR_EFFECT_SUB_SETTINGS, KEY_ID.DIMMING_KEY,))
    def test_priority_order_immersive_lighting_keys(self):
        """
        [FKC Priority Order]
        Remap immersive lighting hotkey to a standard key (exclude modifier keys). Check there is no effect for the
        remapping.

        Remapping:
        60% KBD (example):
        1. Fn + z -> Key1
        2. Fn + x -> Key2
        3. Fn + c -> Key3
        4. Fn + v -> Key4
        (Random select Key1 ~ Key4)
        """
        immersive_lighting_keys = [KEY_ID.BACKLIGHT_UP, KEY_ID.BACKLIGHT_DOWN, KEY_ID.CYCLE_THROUGH_ANIMATION_EFFECTS,
                                   KEY_ID.CYCLE_THROUGH_COLOR_EFFECT_SUB_SETTINGS, KEY_ID.DIMMING_KEY]

        # Search immersive lighting keys from key layout
        immersive_lighting_in_base_layer = [key for key in self.button_stimuli_emulator.get_key_id_list()
                                            if key in immersive_lighting_keys]
        fn_keys = self.button_stimuli_emulator.get_fn_keys()
        immersive_lighting_in_fn_layer = [key for key in fn_keys if key in immersive_lighting_keys]

        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        key_1 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.STANDARD_KEY, fn_trigger_remapping=True)
        key_2 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.STANDARD_KEY, fn_trigger_remapping=True,
            excluded_keys=[key_1])
        key_3 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.STANDARD_KEY, fn_trigger_remapping=True,
            excluded_keys=[key_1, key_2])
        key_4 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.STANDARD_KEY, fn_trigger_remapping=True,
            excluded_keys=[key_1, key_2, key_3])
        key_5 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.STANDARD_KEY, fn_trigger_remapping=True,
            excluded_keys=[key_1, key_2, key_3, key_4])
        action_keys = [key_1, key_2, key_3, key_4, key_5]

        preset_remapped_keys = []
        for index, key in enumerate(immersive_lighting_in_base_layer):
            preset_remapped_keys.append(RemappedKey(
                layer=FkcMainTable.Layer.BASE, action_type=RemappedKey.ActionType.KEYBOARD,
                trigger_key=key, action_key=action_keys[index]))
        # end for
        for index, key in enumerate(immersive_lighting_in_fn_layer):
            preset_remapped_keys.append(RemappedKey(
                layer=FkcMainTable.Layer.FN, action_type=RemappedKey.ActionType.KEYBOARD,
                trigger_key=fn_keys[key], action_key=action_keys[index]))
        # end for
        remapped_keys = self.create_remapping_in_nvs(preset_remapped_keys=preset_remapped_keys)

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        for remapped_key in remapped_keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Perform the FKC toggle hotkey {remapped_key} properly.")
            # ----------------------------------------------------------------------------------------------------------
            FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.build_key_sequence(test_case=self,
                                                                                remapped_key=remapped_key,
                                                                                fn_key=KEY_ID.FN_KEY)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check received no keyboard HID report from device ")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # end for

        self.testCaseChecked("ROB_FKC_0005", _AUTHOR)
    # end def test_priority_order_immersive_lighting_keys

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Robustness')
    @services('SimultaneousKeystrokes')
    def test_priority_order_factory_reset(self):
        """
        [FKC Priority Order]
        Remap keys in the Factory reset sequence to standard keys (exclude modifier keys).
        Check device can be reset after done the Factory reset sequence.

        Factory reset sequence: ESC + O + ESC + O + ESC + B
        Remapping:
        ESC -> Key1
        O -> Key2
        B -> Key3
        (Random select Key1 ~ Key3)
        """
        # Configure key remapping
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=KEY_ID.KEYBOARD_ESCAPE,
                        action_key=RemappedKey.RandomKey.NON_MODIFIER_KEY),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=KEY_ID.KEYBOARD_O,
                        action_key=RemappedKey.RandomKey.NON_MODIFIER_KEY),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=KEY_ID.KEYBOARD_B,
                        action_key=RemappedKey.RandomKey.NON_MODIFIER_KEY),
        ]
        self.create_remapping_in_ram(preset_remapped_keys=preset_remapped_keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform the Factory reset sequence properly. ESC + O + ESC + O + ESC + B")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_ESCAPE)
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_O)
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_ESCAPE)
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_O)
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_ESCAPE)
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_B)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check lost connection to the device")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, verify_connection_reset=False,
                   verify_wireless_device_status_broadcast_event=False)
        try:
            CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(
                test_case=self,
                ble_service_changed_required=False,
                wireless_broadcast_event_required=False)
        except (AssertionError, QueueEmpty):
            # Expected lost the connection
            pass
        except Exception:
            raise
        # end try

        self.testCaseChecked("ROB_FKC_0006", _AUTHOR)
    # end def test_priority_order_factory_reset

    @features('Keyboard')
    @features('FullKeyCustomization')
    @features('Feature8071')
    @level('Robustness')
    @services('SimultaneousKeystrokes')
    def test_priority_order_demo_mode(self):
        """
        [FKC Priority Order]
        Remap keys in the Demo mode key sequence to standard keys (exclude modifier keys).
        Check device can enter Demo mode after done the key sequence.

        Demo mode key sequence:
        1. FS / TKL KBD: Press and hold (F1 + F3 + F5) + Power Cycle
        2. 60% KBD: Press and hold (1 + 3 + 5) + Power Cycle

        FS/ TKL KBD Remapping:
        F1 -> Key1
        F3 -> Key2
        F5 -> Key3

        60% KBD Remapping:
        1 -> Key1
        3 -> Key2
        5 -> Key3
        (Random select Key1 ~ Key3)
        """
        # Configure key remapping
        fn_keys = KeyMatrixTestUtils.get_fn_key_list(test_case=self)
        key_sequence = [KEY_ID.KEYBOARD_1, KEY_ID.KEYBOARD_3, KEY_ID.KEYBOARD_5] \
            if KEY_ID.KEYBOARD_F1 in list(fn_keys.keys()) \
            else [KEY_ID.KEYBOARD_F1, KEY_ID.KEYBOARD_F3, KEY_ID.KEYBOARD_F5]
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=key_sequence[0],
                        action_key=RemappedKey.RandomKey.NON_MODIFIER_KEY),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=key_sequence[1],
                        action_key=RemappedKey.RandomKey.NON_MODIFIER_KEY),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=key_sequence[2],
                        action_key=RemappedKey.RandomKey.NON_MODIFIER_KEY),
        ]
        self.create_remapping_in_ram(preset_remapped_keys=preset_remapped_keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform the Demo mode key sequence properly. "
                                 "Press and hold (1 + 3 + 5) + Power Cycle")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        self.button_stimuli_emulator.multiple_keys_press(key_ids=key_sequence, delay=0.05)
        self.reset(hardware_reset=True)
        self.button_stimuli_emulator.release_all()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Check the device enter Demo mode by 0x8071.manageNvConfig")
        # --------------------------------------------------------------------------------------------------------------
        manage_nv_config = RGBEffectsTestUtils.HIDppHelper.manage_nv_config(
            test_case=self, get_or_set=0, nv_capabilities=RGBEffects.NvCapability.DEMO)
        self.assertEqual(expected=RGBEffects.CapabilityState.ENABLED,
                         obtained=to_int(manage_nv_config.capability_state))

        self.testCaseChecked("ROB_FKC_0007", _AUTHOR)
    # end def test_priority_order_demo_mode

    @features('Keyboard')
    @features('FullKeyCustomization')
    @level('Robustness')
    @services('SimultaneousKeystrokes')
    def test_priority_order_gshift_fn_layer(self):
        """
        [FKC Priority Order]
        Remap GShift + Trigger2 -> Key1 and Fn + Trigger2 -> Key2 (exclude modifier keys). Check the remapping works
        well in the different FKC layers.

        Remapping:
        Trigger1 -> GShift
        GShift + Trigger2 -> Key1
        Fn + Trigger2 -> Key2 (Exclude FKC toggle hotkeys and immersive lighting hotkeys)
        (Random select Trigger1, Trigger2 and  Key1 ~ Key2)
        """
        # Configure key remapping
        random_generation_helper = FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper
        trigger_1 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY)
        trigger_2 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY, fn_trigger_remapping=True,
            excluded_keys=[trigger_1])
        key_1 = random_generation_helper.get_random_action_key(
            test_case=self, key_type=RemappedKey.RandomKey.STANDARD_KEY)
        key_2 = random_generation_helper.get_random_trigger_key(
            test_case=self, key_type=RemappedKey.RandomKey.ALL_REMAPPABLE_KEY, excluded_keys=[key_1])
        preset_remapped_keys = [
            RemappedKey(layer=FkcMainTable.Layer.BASE,
                        action_type=RemappedKey.ActionType.VIRTUAL_MODIFIER,
                        trigger_key=trigger_1,
                        action_key=KEY_ID.G_SHIFT),
            RemappedKey(layer=FkcMainTable.Layer.GSHIFT,
                        action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_2,
                        action_key=key_1),
            RemappedKey(layer=FkcMainTable.Layer.FN,
                        action_type=RemappedKey.ActionType.KEYBOARD,
                        trigger_key=trigger_2,
                        action_key=key_2),
        ]
        self.create_remapping_in_nvs(preset_remapped_keys=preset_remapped_keys)

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform the GShift + Trigger2 keys properly")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(
            key_ids=[trigger_1, trigger_2], delay=0.05)
        self.button_stimuli_emulator.multiple_keys_release(
            key_ids=[trigger_2, trigger_1], delay=0.05)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Check received the HID report for the Key1 {key_1!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_1, state=MAKE))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_1, state=BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform the Fn + Trigger2 keys properly")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(
            key_ids=[KEY_ID.FN_KEY, trigger_2], delay=0.05)
        self.button_stimuli_emulator.multiple_keys_release(
            key_ids=[trigger_2, KEY_ID.FN_KEY], delay=0.05)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Check received the HID report for the Key2 {key_2!r}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_2, state=MAKE))
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self, key=RemappedKey(action_key=key_2, state=BREAK))

        self.testCaseChecked("ROB_FKC_0008", _AUTHOR)
    # end def test_priority_order_gshift_fn_layer
# end class FKCRobustnessTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
