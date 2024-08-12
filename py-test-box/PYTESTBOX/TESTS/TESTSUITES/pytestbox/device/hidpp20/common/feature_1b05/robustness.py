#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1b05.robustness
:brief: HID++ 2.0 ``FullKeyCustomization`` robustness test suite
:author: Masan Xu <mxu11@logitech.com>
:date: 2023/05/29
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import sample
from time import sleep
from unittest import skip
from math import ceil

import pylibrary
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.fullkeycustomization import FullKeyCustomization
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.fkcprofileformat import FkcMainTable
from pylibrary.mcu.fkcprofileformat import RemappedKey
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.fullkeycustomizationutils import FullKeyCustomizationTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.hidpp20.common.feature_1b05.fullkeycustomization import FullKeyCustomizationTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Masan Xu"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class FullKeyCustomizationRobustnessTestCase(FullKeyCustomizationTestCase):
    """
    Validate ``FullKeyCustomization`` robustness test cases
    """

    @features('Keyboard')
    @features("Feature1B05")
    @level("Robustness")
    def test_get_capabilities_software_id(self):
        """
        Validate ``GetCapabilities`` software id field is ignored by the firmware

        [0] getCapabilities() -> fkcConfigFileVer, macroDefFileVer, fkcConfigFileMaxsize,
        macroDefFileMaxsize, fkcConfigMaxTriggers

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(FullKeyCustomization.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = FullKeyCustomizationTestUtils.HIDppHelper.get_capabilities(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = FullKeyCustomizationTestUtils.GetCapabilitiesResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_1b05.get_capabilities_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1B05_0001#1", _AUTHOR)
    # end def test_get_capabilities_software_id

    @features('Keyboard')
    @features("Feature1B05")
    @level("Robustness")
    def test_get_set_power_on_params_software_id(self):
        """
        Validate ``GetSetPowerOnParams`` software id field is ignored by the firmware

        [1] getSetPowerOnParams(setPowerOnFkcState, powerOnFkcState) -> powerOnFkcState

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.SetPowerOnFkcState.PowerOnFkcState.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(FullKeyCustomization.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetSetPowerOnParams request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_power_on_params(
                test_case=self,
                set_power_on_fkc_enable=FullKeyCustomization.PowerOnFKCRequest.GET,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetSetPowerOnParamsResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = FullKeyCustomizationTestUtils.GetSetPowerOnParamsResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_1b05.get_set_power_on_params_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1B05_0001#2", _AUTHOR)
    # end def test_get_set_power_on_params_software_id

    @features('Keyboard')
    @features("Feature1B05")
    @level("Robustness")
    def test_get_toggle_key_list_software_id(self):
        """
        Validate ``GetToggleKeyList`` software id field is ignored by the firmware

        [2] getToggleKeyList() -> toggleKey0Cid, toggleKey1Cid, toggleKey2Cid, toggleKey3Cid, toggleKey4Cid,
        toggleKey5Cid, toggleKey6Cid, toggleKey7Cid

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(FullKeyCustomization.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetToggleKeyList request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = FullKeyCustomizationTestUtils.HIDppHelper.get_toggle_key_list(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetToggleKeyListResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = FullKeyCustomizationTestUtils.GetToggleKeyListResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_1b05.get_toggle_key_list_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1B05_0001#3", _AUTHOR)
    # end def test_get_toggle_key_list_software_id

    @features('Keyboard')
    @features("Feature1B05")
    @level("Robustness")
    def test_get_set_enabled_software_id(self):
        """
        Validate ``GetSetEnabled`` software id field is ignored by the firmware

        [3] getSetEnabled(setGetFkcState, fkcState, toggleKeysState) -> fkcState, toggleKeysState

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.SetGetFkcState.FkcState.ToggleKeysState

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(FullKeyCustomization.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetSetEnabled request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
                test_case=self,
                set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.GET,
                set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetSetEnabledResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = FullKeyCustomizationTestUtils.GetSetEnabledResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_1b05.get_set_enabled_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1B05_0001#4", _AUTHOR)
    # end def test_get_set_enabled_software_id

    @features('Keyboard')
    @features("Feature1B05")
    @level("Robustness")
    def test_get_capabilities_padding(self):
        """
        Validate ``GetCapabilities`` padding bytes are ignored by the firmware

        [0] getCapabilities() -> fkcConfigFileVer, macroDefFileVer, fkcConfigFileMaxsize,
        macroDefFileMaxsize, fkcConfigMaxTriggers

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1b05.get_capabilities_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = FullKeyCustomizationTestUtils.HIDppHelper.get_capabilities(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = FullKeyCustomizationTestUtils.GetCapabilitiesResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_1b05.get_capabilities_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1B05_0002#1", _AUTHOR)
    # end def test_get_capabilities_padding

    @features('Keyboard')
    @features("Feature1B05")
    @level("Robustness")
    def test_get_set_power_on_params_padding(self):
        """
        Validate ``GetSetPowerOnParams`` padding bytes are ignored by the firmware

        [1] getSetPowerOnParams(setPowerOnFkcState, powerOnFkcState) -> powerOnFkcState

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.SetPowerOnFkcState.PowerOnFkcState.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1b05.get_set_power_on_params_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetSetPowerOnParams request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_power_on_params(
                test_case=self,
                set_power_on_fkc_enable=FullKeyCustomization.PowerOnFKCRequest.GET,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetSetPowerOnParamsResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = FullKeyCustomizationTestUtils.GetSetPowerOnParamsResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_1b05.get_set_power_on_params_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1B05_0002#2", _AUTHOR)
    # end def test_get_set_power_on_params_padding

    @features('Keyboard')
    @features("Feature1B05")
    @level("Robustness")
    def test_get_toggle_key_list_padding(self):
        """
        Validate ``GetToggleKeyList`` padding bytes are ignored by the firmware

        [2] getToggleKeyList() -> toggleKey0Cid, toggleKey1Cid, toggleKey2Cid, toggleKey3Cid, toggleKey4Cid,
        toggleKey5Cid, toggleKey6Cid, toggleKey7Cid

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1b05.get_toggle_key_list_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetToggleKeyList request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = FullKeyCustomizationTestUtils.HIDppHelper.get_toggle_key_list(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetToggleKeyListResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = FullKeyCustomizationTestUtils.GetToggleKeyListResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_1b05.get_toggle_key_list_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1B05_0002#3", _AUTHOR)
    # end def test_get_toggle_key_list_padding

    @features('Keyboard')
    @features("Feature1B05")
    @level("Robustness")
    @services('KeyMatrix')
    @skip("In development")
    def test_base_layer_trigger_list_event_max_triggers(self):
        """
        If FKC is enabled, baseLayerTriggerAsListEvent is sent by DUT when keystroke 16 trigger keys
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create a FKC profile with enabled NotifySW flag in RAM buffer")
        # --------------------------------------------------------------------------------------------------------------
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(full_keys=True)), notify_sw=True,
            enable_fkc=FullKeyCustomization.FKCStatus.DISABLE)
        remapped_16_keys = sample(remapped_keys, 16)
        LogHelper.log_info(self, f'{remapped_16_keys}')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Perform fkc toggle hotkeys")
        # --------------------------------------------------------------------------------------------------------------
        self.perform_fkc_toggle_hotkeys(fkc_status=FullKeyCustomization.FKCStatus.ENABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Emulate keystrokes on 16 {remapped_key}.trigger_key")
        # --------------------------------------------------------------------------------------------------------------
        trigger_key_ids = []
        for remapped_key in remapped_16_keys:
            trigger_key_ids.append(remapped_key.trigger_key)
        # end for
        LogHelper.log_info(self, f'{trigger_key_ids}')
        self.button_stimuli_emulator.multiple_keys_press(key_ids=trigger_key_ids)
        sleep(ButtonStimuliInterface.DEFAULT_DELAY)
        self.button_stimuli_emulator.multiple_keys_release(key_ids=trigger_key_ids)
        sleep(ButtonStimuliInterface.DEFAULT_DELAY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check baseLayerTriggerAsListEvent with key_trigger[0..16]=(fckIdx of"
                                  "{remapped_key}.trigger_key[0..16]) + 1")
        # --------------------------------------------------------------------------------------------------------------
        base_trigger_list = FullKeyCustomizationTestUtils.HIDppHelper.base_layer_trigger_as_list_event(
            test_case=self)

        checker = FullKeyCustomizationTestUtils.BaseLayerTriggerAsListEventChecker
        check_map = checker.get_default_check_map(self)
        for i in range(len(remapped_16_keys)):
            check_map[f'key_trigger_{i}'] = (getattr(checker, f'key_trigger_{i}'),
                                             FullKeyCustomization.KeyState.PRESSED)
        # end for

        checker.check_fields(self, base_trigger_list, self.feature_1b05.base_layer_trigger_as_bitmap_event_cls,
                             check_map)

        self.testCaseChecked("ROB_1B05_0003", _AUTHOR)
    # end def test_base_layer_trigger_list_event_max_triggers

    @features('Keyboard')
    @features("Feature1B05")
    @level("Robustness")
    @services('KeyMatrix')
    @skip("In development")
    def test_base_layer_trigger_bitmap_event_max_triggers(self):
        """
        If FKC is enabled, baseLayerTriggerAsBitmapEvent is sent by DUT when keystroke trigger keys as much as
        possible(>17)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create a FKC profile with enabled NotifySW flag in RAM buffer")
        # --------------------------------------------------------------------------------------------------------------
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(full_keys=True)), notify_sw=True,
            enable_fkc=FullKeyCustomization.FKCStatus.DISABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Perform fkc toggle hotkeys")
        # --------------------------------------------------------------------------------------------------------------
        self.perform_fkc_toggle_hotkeys(fkc_status=FullKeyCustomization.FKCStatus.ENABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Emulate keystrokes on all trigger_keys simultaneously")
        # --------------------------------------------------------------------------------------------------------------
        trigger_key_ids = []
        for remapped_key in remapped_keys:
            trigger_key_ids.append(remapped_key.trigger_key)
        # end for
        LogHelper.log_info(self, f'{trigger_key_ids}')
        self.button_stimuli_emulator.multiple_keys_press(key_ids=trigger_key_ids)
        sleep(ButtonStimuliInterface.DEFAULT_DELAY)
        self.button_stimuli_emulator.multiple_keys_release(key_ids=trigger_key_ids)
        sleep(ButtonStimuliInterface.DEFAULT_DELAY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check baseLayerTriggerAsListEvent with key_trigger_bitmap of fkcIdx of all "
                                  "trigger_keys = 1")
        # --------------------------------------------------------------------------------------------------------------
        base_trigger_bitmap = FullKeyCustomizationTestUtils.HIDppHelper.base_layer_trigger_as_bitmap_event(
            test_case=self)

        trigger_bitmap_checker = FullKeyCustomizationTestUtils.KeyTriggerBitmapChecker
        trigger_bitmap_check_map = trigger_bitmap_checker.get_default_check_map(self)
        checker = FullKeyCustomizationTestUtils.BaseLayerTriggerAsBitmapEventChecker
        check_map = checker.get_default_check_map(self)
        for i in range(len(remapped_keys)):
            trigger_bitmap_check_map[f'fkc_idx_{remapped_keys[i].fkc_idx}'] = (
                getattr(trigger_bitmap_checker, f'check_fkc_idx_{remapped_keys[i].fkc_idx}'),
                FullKeyCustomization.KeyState.PRESSED)
            check_map['key_trigger_bitmap'] = (checker.check_key_trigger_bitmap, trigger_bitmap_check_map)
        # end for

        checker.check_fields(self, base_trigger_bitmap, self.feature_1b05.base_layer_trigger_as_bitmap_event_cls,
                             check_map)

        self.testCaseChecked("ROB_1B05_0004", _AUTHOR)
    # end def test_base_layer_trigger_bitmap_event_max_triggers

    @features('Keyboard')
    @features("Feature1B05")
    @level("Robustness")
    @services('RequiredKeys', (KEY_ID.FN_KEY,))
    @services('KeyMatrix')
    @skip("In development")
    def test_fn_layer_trigger_list_event_max_triggers(self):
        """
        If FKC is enabled, fnLayerTriggerAsListEvent is sent by DUT when keystroke 16 trigger keys
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create a FKC profile with enabled NotifySW flag in RAM buffer")
        # --------------------------------------------------------------------------------------------------------------
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            layer=FkcMainTable.Layer.FN, button=random_parameters_cls.Button(full_keys=True)), notify_sw=True,
            enable_fkc=FullKeyCustomization.FKCStatus.DISABLE)
        remapped_16_keys = sample(remapped_keys, 16)
        LogHelper.log_info(self, f'{remapped_16_keys}')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Perform fkc toggle hotkeys")
        # --------------------------------------------------------------------------------------------------------------
        self.perform_fkc_toggle_hotkeys(fkc_status=FullKeyCustomization.FKCStatus.ENABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Emulate keystrokes on FN + 16 {remapped_key}.trigger_key")
        # --------------------------------------------------------------------------------------------------------------
        trigger_key_ids = []
        for remapped_key in remapped_16_keys:
            trigger_key_ids.append(remapped_key.trigger_key)
        # end for
        LogHelper.log_info(self, f'{trigger_key_ids}')
        self.button_stimuli_emulator.key_press(key_ids=KEY_ID.FN_KEY)
        sleep(ButtonStimuliInterface.DEFAULT_DELAY)
        self.button_stimuli_emulator.multiple_keys_press(key_ids=trigger_key_ids)
        sleep(ButtonStimuliInterface.DEFAULT_DELAY)
        self.button_stimuli_emulator.multiple_keys_release(key_ids=trigger_key_ids)
        sleep(ButtonStimuliInterface.DEFAULT_DELAY)
        self.button_stimuli_emulator.key_release(key_ids=KEY_ID.FN_KEY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check fnLayerTriggerAsListEvent with key_trigger[0..16]=(fckIdx of"
                                  "{remapped_key}.trigger_key[0..16]) + 1")
        # --------------------------------------------------------------------------------------------------------------
        fn_trigger_list = FullKeyCustomizationTestUtils.HIDppHelper.fn_layer_trigger_as_list_event(
            test_case=self)

        checker = FullKeyCustomizationTestUtils.FNLayerTriggerAsListEventChecker
        check_map = checker.get_default_check_map(self)
        for i in range(len(remapped_16_keys)):
            check_map[f'key_trigger_{i}'] = (getattr(checker, f'key_trigger_{i}'),
                                             FullKeyCustomization.KeyState.PRESSED)
        # end for

        checker.check_fields(self, fn_trigger_list, self.feature_1b05.fn_layer_trigger_as_bitmap_event_cls,
                             check_map)

        self.testCaseChecked("ROB_1B05_0005", _AUTHOR)
    # end def test_fn_layer_trigger_list_event_max_triggers

    @features('Keyboard')
    @features("Feature1B05")
    @level("Robustness")
    @services('RequiredKeys', (KEY_ID.FN_KEY,))
    @services('KeyMatrix')
    @skip("In development")
    def test_fn_layer_trigger_bitmap_event_max_triggers(self):
        """
        If FKC is enabled, fnLayerTriggerAsBitmapEvent is sent by DUT when keystroke trigger keys as much as
        possible(>17)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create a FKC profile with enabled NotifySW flag in RAM buffer")
        # --------------------------------------------------------------------------------------------------------------
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            layer=FkcMainTable.Layer.FN, button=random_parameters_cls.Button(full_keys=True)), notify_sw=True,
            enable_fkc=FullKeyCustomization.FKCStatus.DISABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Perform fkc toggle hotkeys")
        # --------------------------------------------------------------------------------------------------------------
        self.perform_fkc_toggle_hotkeys(fkc_status=FullKeyCustomization.FKCStatus.ENABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Emulate keystrokes on FN + all trigger_keys simultaneously")
        # --------------------------------------------------------------------------------------------------------------
        trigger_key_ids = []
        for remapped_key in remapped_keys:
            trigger_key_ids.append(remapped_key.trigger_key)
        # end for
        LogHelper.log_info(self, f'{trigger_key_ids}')
        self.button_stimuli_emulator.key_press(key_ids=KEY_ID.FN_KEY)
        sleep(ButtonStimuliInterface.DEFAULT_DELAY)
        self.button_stimuli_emulator.multiple_keys_press(key_ids=trigger_key_ids)
        sleep(ButtonStimuliInterface.DEFAULT_DELAY)
        self.button_stimuli_emulator.multiple_keys_release(key_ids=trigger_key_ids)
        sleep(ButtonStimuliInterface.DEFAULT_DELAY)
        self.button_stimuli_emulator.key_release(key_ids=KEY_ID.FN_KEY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check fnLayerTriggerAsListEvent with key_trigger_bitmap of fkcIdx of all "
                                  "trigger_keys = 1")
        # --------------------------------------------------------------------------------------------------------------
        fn_trigger_bitmap = FullKeyCustomizationTestUtils.HIDppHelper.fn_layer_trigger_as_list_event(
            test_case=self)

        trigger_bitmap_checker = FullKeyCustomizationTestUtils.KeyTriggerBitmapChecker
        trigger_bitmap_check_map = trigger_bitmap_checker.get_default_check_map(self)
        checker = FullKeyCustomizationTestUtils.FNLayerTriggerAsBitmapEventChecker
        check_map = checker.get_default_check_map(self)
        for i in range(len(remapped_keys)):
            trigger_bitmap_check_map[f'fkc_idx_{remapped_keys[i].fkc_idx}'] = (
                getattr(trigger_bitmap_checker, f'check_fkc_idx_{remapped_keys[i].fkc_idx}'),
                FullKeyCustomization.KeyState.PRESSED)
            check_map['key_trigger_bitmap'] = (checker.check_key_trigger_bitmap, trigger_bitmap_check_map)
        # end for

        checker.check_fields(self, fn_trigger_bitmap, self.feature_1b05.fn_layer_trigger_as_bitmap_event_cls,
                             check_map)
        self.testCaseChecked("ROB_1B05_0006", _AUTHOR)
    # end def test_fn_layer_trigger_bitmap_event_max_triggers

    @features('Keyboard')
    @features("Feature1B05")
    @level("Robustness")
    @services('RequiredKeys', (KEY_ID.G_SHIFT,))
    @services('KeyMatrix')
    @skip("In development")
    def test_gshift_layer_trigger_list_event_max_triggers(self):
        """
        If FKC is enabled, gshiftLayerTriggerAsListEvent is sent by DUT when keystroke 16 trigger keys
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create a FKC profile with enabled NotifySW flag in RAM buffer")
        # --------------------------------------------------------------------------------------------------------------
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            layer=FkcMainTable.Layer.GSHIFT, button=random_parameters_cls.Button(full_keys=True)), notify_sw=True,
            enable_fkc=FullKeyCustomization.FKCStatus.DISABLE)
        remapped_16_keys = sample(remapped_keys, 16)
        LogHelper.log_info(self, f'{remapped_16_keys}')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Perform fkc toggle hotkeys")
        # --------------------------------------------------------------------------------------------------------------
        self.perform_fkc_toggle_hotkeys(fkc_status=FullKeyCustomization.FKCStatus.ENABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Emulate keystrokes on GSHIFT + 16 {remapped_key}.trigger_key")
        # --------------------------------------------------------------------------------------------------------------
        trigger_key_ids = []
        for remapped_key in remapped_16_keys:
            trigger_key_ids.append(remapped_key.trigger_key)
        # end for
        LogHelper.log_info(self, f'{trigger_key_ids}')
        self.button_stimuli_emulator.key_press(key_ids=KEY_ID.G_SHIFT)
        sleep(ButtonStimuliInterface.DEFAULT_DELAY)
        self.button_stimuli_emulator.multiple_keys_press(key_ids=trigger_key_ids)
        sleep(ButtonStimuliInterface.DEFAULT_DELAY)
        self.button_stimuli_emulator.multiple_keys_release(key_ids=trigger_key_ids)
        sleep(ButtonStimuliInterface.DEFAULT_DELAY)
        self.button_stimuli_emulator.key_release(key_ids=KEY_ID.G_SHIFT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check gshiftLayerTriggerAsListEvent with key_trigger[0..16]=(fckIdx of"
                                  "{remapped_key}.trigger_key[0..16]) + 1")
        # --------------------------------------------------------------------------------------------------------------
        gshift_trigger_list = FullKeyCustomizationTestUtils.HIDppHelper.gshift_layer_trigger_as_list_event(
            test_case=self)

        checker = FullKeyCustomizationTestUtils.GShiftLayerTriggerAsListEventChecker
        check_map = checker.get_default_check_map(self)
        for i in range(len(remapped_16_keys)):
            check_map[f'key_trigger_{i}'] = (getattr(checker, f'key_trigger_{i}'),
                                             FullKeyCustomization.KeyState.PRESSED)
        # end for

        checker.check_fields(self, gshift_trigger_list, self.feature_1b05.gshift_layer_trigger_as_bitmap_event_cls,
                             check_map)
        self.testCaseChecked("ROB_1B05_0007", _AUTHOR)
    # end def test_gshift_layer_trigger_list_event_max_triggers

    @features('Keyboard')
    @features("Feature1B05")
    @level("Robustness")
    @services('RequiredKeys', (KEY_ID.G_SHIFT,))
    @services('KeyMatrix')
    @skip("In development")
    def test_gshift_layer_trigger_bitmap_event_max_triggers(self):
        """
        If FKC is enabled, gshiftLayerTriggerAsListEvent is sent by DUT when keystroke trigger keys as much as
        possible(>17)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create a FKC profile with enabled NotifySW flag in RAM buffer")
        # --------------------------------------------------------------------------------------------------------------
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            layer=FkcMainTable.Layer.GSHIFT, button=random_parameters_cls.Button(full_keys=True)), notify_sw=True,
            enable_fkc=FullKeyCustomization.FKCStatus.DISABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Perform fkc toggle hotkeys")
        # --------------------------------------------------------------------------------------------------------------
        self.perform_fkc_toggle_hotkeys(fkc_status=FullKeyCustomization.FKCStatus.ENABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Emulate keystrokes on GSHIFT + all trigger_keys simultaneously")
        # --------------------------------------------------------------------------------------------------------------
        trigger_key_ids = []
        for remapped_key in remapped_keys:
            trigger_key_ids.append(remapped_key.trigger_key)
        # end for
        LogHelper.log_info(self, f'{trigger_key_ids}')
        self.button_stimuli_emulator.key_press(key_ids=KEY_ID.G_SHIFT)
        sleep(ButtonStimuliInterface.DEFAULT_DELAY)
        self.button_stimuli_emulator.multiple_keys_press(key_ids=trigger_key_ids)
        sleep(ButtonStimuliInterface.DEFAULT_DELAY)
        self.button_stimuli_emulator.multiple_keys_release(key_ids=trigger_key_ids)
        sleep(ButtonStimuliInterface.DEFAULT_DELAY)
        self.button_stimuli_emulator.key_release(key_ids=KEY_ID.G_SHIFT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check gshiftLayerTriggerAsListEvent with key_trigger_bitmap of fkcIdx of all "
                                  "trigger_keys = 1")
        # --------------------------------------------------------------------------------------------------------------
        gshift_trigger_bitmap = FullKeyCustomizationTestUtils.HIDppHelper.gshift_layer_trigger_as_list_event(
            test_case=self)

        trigger_bitmap_checker = FullKeyCustomizationTestUtils.KeyTriggerBitmapChecker
        trigger_bitmap_check_map = trigger_bitmap_checker.get_default_check_map(self)
        checker = FullKeyCustomizationTestUtils.GShiftLayerTriggerAsBitmapEventChecker
        check_map = checker.get_default_check_map(self)
        for i in range(len(remapped_keys)):
            trigger_bitmap_check_map[f'fkc_idx_{remapped_keys[i].fkc_idx}'] = (
                getattr(trigger_bitmap_checker, f'check_fkc_idx_{remapped_keys[i].fkc_idx}'),
                FullKeyCustomization.KeyState.PRESSED)
            check_map['key_trigger_bitmap'] = (checker.check_key_trigger_bitmap, trigger_bitmap_check_map)
        # end for

        checker.check_fields(self, gshift_trigger_bitmap, self.feature_1b05.fn_layer_trigger_as_bitmap_event_cls,
                             check_map)

        self.testCaseChecked("ROB_1B05_0008", _AUTHOR)
    # end def test_gshift_layer_trigger_bitmap_event_max_triggers

    @features('Keyboard')
    @features("Feature1B05")
    @features("Feature1B05MacroMaxSize")
    @level("Robustness")
    def test_execute_exceeded_size_macro_file(self):
        """
        FW should still work properly even if executing a macro whose size is greater than
        0x1b05.getCapabilities.macroDefFileMaxsize
        """
        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.MACRO,
                        trigger_key=RemappedKey.RandomKey.NON_MODIFIER_KEY,
                        macro_entry_index=0)
        ]

        # To create a macro whose size is double 0x1b05.getCapabilities.macroDefFileMaxsize
        macro_command_count = ceil(self.f.PRODUCT.FEATURES.COMMON.FULL_KEY_CUSTOMIZATION.F_MacroDefFileMaxsize /
                                   pylibrary.mcu.profileformat.MacroCommand2.DATA_SIZE)

        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(
            preset_remapped_keys=preset_remapped_keys,  random_parameters=random_parameters_cls(
                macro=random_parameters_cls.Macro(entry_count=1, command_count=macro_command_count)))
        remapped_key = remapped_keys[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Clean HID queue")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Emulate a keystroke on the trigger key: {remapped_key.trigger_key!r} to start the "
                                 "macro")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=remapped_key.trigger_key)
        # Gaming KBD polling rate is 1ms, so the delay time is calculated by the macro command count * 2(MAKE and BREAK)
        sleep((macro_command_count * 2 / 1000) + 1)
        try:
            FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(test_case=self, remapped_key=remapped_key)
        except Exception as e:
            LogHelper.log_info(self, f'Acceptable exception: {e}, because any exceeded side macro files are invalid')
            KeyMatrixTestUtils.reset_last_reports(test_case=self)
        # end try

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform fkc toggle hotkeys to disable FKC")
        # --------------------------------------------------------------------------------------------------------------
        self.perform_fkc_toggle_hotkeys(fkc_status=FullKeyCustomization.FKCStatus.DISABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Emulate a keystroke on the key: {remapped_key.trigger_key!r}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=remapped_key.trigger_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check HID Keyboard report linked to the key {remapped_key.trigger_key!r} to make '
                                  'sure the DUT is still alive')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                      key=KeyMatrixTestUtils.Key(remapped_key.trigger_key, MAKE))
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                      key=KeyMatrixTestUtils.Key(remapped_key.trigger_key, BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset to check if the DUT isn't bricked even if there is an exceeded size macro "
                                 "file in NVS")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        self.testCaseChecked("ROB_1B05_0009", _AUTHOR)
    # end def test_execute_exceeded_size_macro_file
# end class FullKeyCustomizationRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
