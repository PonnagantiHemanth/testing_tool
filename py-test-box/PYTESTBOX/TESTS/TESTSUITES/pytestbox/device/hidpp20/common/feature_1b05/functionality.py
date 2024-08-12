#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1b05.functionality
:brief: HID++ 2.0 ``FullKeyCustomization`` functionality test suite
:author: Masan Xu <mxu11@logitech.com>
:date: 2023/05/17
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import choice
from random import sample
from time import sleep
from unittest import skip

from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.fullkeycustomization import FullKeyCustomization
from pyhid.hidpp.features.common.fullkeycustomization import GetSetSWConfigurationCookieV1
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagement
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.fkcprofileformat import FkcMainTable
from pylibrary.mcu.fkcprofileformat import RemappedKey
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.controllistutils import ControlListTestUtils
from pytestbox.device.base.fullkeycustomizationutils import FullKeyCustomizationTestUtils
from pytestbox.device.base.profilemanagementutils import ProfileManagementTestUtils
from pytestbox.device.hidpp20.common.feature_1b05.fullkeycustomization import FullKeyCustomizationTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Masan Xu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class FullKeyCustomizationFunctionalityTestCase(FullKeyCustomizationTestCase):
    """
    Validate ``FullKeyCustomization`` functionality test cases
    """

    def _validate_remapped_keys(self, remapped_keys, fkc_status):
        """
        Emulate keystrokes on the trigger key of remapped keys and check their HID report depending on current fkc
        status

        :param remapped_keys: All remapped keys
        :type remapped_keys: ``list[RemappedKey]``
        :param fkc_status: Indicate current FKC status, it will change the expected report to trigger or action key
                           report
        :type fkc_status: ``FullKeyCustomization.FKCStatus``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Empty HID queue")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queues(test_case=self)

        self.kosmos.sequencer.offline_mode = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over {remapped_key} in range {remapped_keys}")
        # --------------------------------------------------------------------------------------------------------------
        for remapped_key in remapped_keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Emulate a keystroke on {remapped_key.trigger_key!r}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=remapped_key.trigger_key)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos Board
        self.kosmos.sequencer.play_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over {remapped_key} in range {remapped_keys}")
        # --------------------------------------------------------------------------------------------------------------
        for remapped_key in remapped_keys:
            if fkc_status is FullKeyCustomization.FKCStatus.ENABLE:
                expected_report = remapped_key.action_key
                expected_report_str = "action"
            else:
                expected_report = remapped_key.trigger_key
                expected_report_str = "trigger"
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check DUT sends the {expected_report_str} key report of {remapped_key}")
            # ----------------------------------------------------------------------------------------------------------
            FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
                test_case=self,
                key=RemappedKey(action_key=expected_report, state=MAKE)
            )
            FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
                test_case=self,
                key=RemappedKey(action_key=expected_report, state=BREAK)
            )
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
    # end def _validate_remapped_keys

    @features('Keyboard')
    @features("Feature1B05")
    @level("Functionality")
    def test_get_set_enabled_fkc_status(self):
        """
        Validate getSetEnabled API can enable/disable FKC
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create a FKC profile and remapping in RAM buffer")
        # --------------------------------------------------------------------------------------------------------------
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(full_keys=True)), enable_fkc=FullKeyCustomization.FKCStatus.DISABLE)
        remapped_17_keys = sample(remapped_keys, 17)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Validate remapped_keys: {remapped_17_keys}")
        # --------------------------------------------------------------------------------------------------------------
        self._validate_remapped_keys(remapped_keys=remapped_17_keys, fkc_status=FullKeyCustomization.FKCStatus.DISABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable FKC by getSetEnabled request with set_fkc_enabled=1 and fkc_enabled=1")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.GET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.SET,
            fkc_enabled=FullKeyCustomization.FKCStatus.ENABLE,
        )
        # Wait all key release events
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check FKC is enabled from getSetEnabled response with fkc_enabled=1")
        # --------------------------------------------------------------------------------------------------------------
        fkc_state_checker = FullKeyCustomizationTestUtils.FkcStateChecker
        fkc_state_check_map = fkc_state_checker.get_default_check_map(self)
        fkc_state_check_map['fkc_enabled'] = (fkc_state_checker.check_fkc_enabled,
                                              FullKeyCustomization.FKCStatus.ENABLE)

        checker = FullKeyCustomizationTestUtils.GetSetEnabledResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map['fkc_state'] = (checker.check_fkc_state, fkc_state_check_map)
        checker.check_fields(self, response, self.feature_1b05.get_set_enabled_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Validate remapped_keys: {remapped_17_keys}")
        # --------------------------------------------------------------------------------------------------------------
        self._validate_remapped_keys(remapped_keys=remapped_17_keys, fkc_status=FullKeyCustomization.FKCStatus.ENABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Disable FKC by getSetEnabled request with set_fkc_enabled=1 and fkc_enabled=0")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.GET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.SET,
            fkc_enabled=FullKeyCustomization.FKCStatus.DISABLE,
        )
        # Wait all key release events
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check FKC is disabled from getSetEnabled response with fkc_enabled=0")
        # --------------------------------------------------------------------------------------------------------------
        fkc_state_check_map['fkc_enabled'] = (fkc_state_checker.check_fkc_enabled,
                                              FullKeyCustomization.FKCStatus.DISABLE)
        check_map['fkc_state'] = (checker.check_fkc_state, fkc_state_check_map)
        checker.check_fields(self, response, self.feature_1b05.get_set_enabled_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Validate remapped_keys: {remapped_17_keys}")
        # --------------------------------------------------------------------------------------------------------------
        self._validate_remapped_keys(remapped_keys=remapped_17_keys, fkc_status=FullKeyCustomization.FKCStatus.DISABLE)

        self.testCaseChecked("FUN_1B05_0001", _AUTHOR)
    # end def test_get_set_enabled_fkc_status

    @features('Keyboard')
    @features("Feature1B05")
    @level("Functionality")
    @services('KeyMatrix')
    def test_get_set_enabled_fkc_toggle_hotkeys(self):
        """
        Validate getSetEnabled API can enable/disable FKC toggle keys
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create a FKC profile and remapping in RAM buffer")
        # --------------------------------------------------------------------------------------------------------------
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        self.create_remapping_in_ram(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(count=1)), enable_fkc=FullKeyCustomization.FKCStatus.DISABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over index {i} in range {toggle_hotkeys}")
        # --------------------------------------------------------------------------------------------------------------
        for i in range(FullKeyCustomization.TOGGLE_HOTKEYS_CNT):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Enable toggle_hotkeys[{i}] by getSetEnabled request with "
                                     f"set_toggle_keys_enabled=1 and toggle_keys_enabled[{i}]=1")
            # ----------------------------------------------------------------------------------------------------------
            FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
                test_case=self,
                set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET,
                set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.SET,
                toggle_keys_enabled=(1 << i)
            )

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Emulate keystrokes on toggle_hotkeys[{i}]")
            # ----------------------------------------------------------------------------------------------------------
            toggle_key_setting = getattr(self.f.PRODUCT.FEATURES.COMMON.FULL_KEY_CUSTOMIZATION, f'F_ToggleKey{i}Cidx')
            toggle_key_1 = ControlListTestUtils.cidx_to_key_id(test_case=self,
                                                               cid_index=to_int(toggle_key_setting[0]))
            toggle_key_2 = ControlListTestUtils.cidx_to_key_id(test_case=self,
                                                               cid_index=to_int(toggle_key_setting[1]))
            self.button_stimuli_emulator.multiple_keys_press(key_ids=[toggle_key_1, toggle_key_2],
                                                             delay=ButtonStimuliInterface.DEFAULT_DELAY)
            self.button_stimuli_emulator.multiple_keys_release(key_ids=[toggle_key_2, toggle_key_1],
                                                               delay=ButtonStimuliInterface.DEFAULT_DELAY)

            # FKC is disabled by default, every iteration will toggle FKC status
            expected_fkc_status = FullKeyCustomization.FKCStatus.DISABLE if i % 2 else \
                FullKeyCustomization.FKCStatus.ENABLE
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check enableDisableEvent with enabled={expected_fkc_status} and failure=0")
            # ----------------------------------------------------------------------------------------------------------
            enable_disable_event = FullKeyCustomizationTestUtils.HIDppHelper.enable_disable_event(test_case=self)

            fkc_failure_enabled_checker = FullKeyCustomizationTestUtils.FkcFailureEnabledStateChecker
            fkc_failure_enabled_map = fkc_failure_enabled_checker.get_default_check_map(self)
            fkc_failure_enabled_map['enabled'] = (fkc_failure_enabled_checker.check_enabled, expected_fkc_status)

            checker = FullKeyCustomizationTestUtils.EnableDisableEventChecker
            check_map = checker.get_default_check_map(self)
            check_map['fkc_failure_enabled_state'] = (checker.check_fkc_failure_enabled_state, fkc_failure_enabled_map)
            checker.check_fields(self, enable_disable_event, self.feature_1b05.enable_disable_event_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Disable toggle_hotkeys by getSetEnabled request with"
                                     f"set_toggle_keys_enabled=1 and toggle_keys_enabled=0")
            # ----------------------------------------------------------------------------------------------------------
            FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
                test_case=self,
                set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET,
                set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.SET,
            )

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Emulate keystrokes on toggle_hotkeys[{i}]")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.multiple_keys_press(key_ids=[toggle_key_1, toggle_key_2],
                                                             delay=ButtonStimuliInterface.DEFAULT_DELAY)
            self.button_stimuli_emulator.multiple_keys_release(key_ids=[toggle_key_2, toggle_key_1],
                                                               delay=ButtonStimuliInterface.DEFAULT_DELAY)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check there aren't any enableDisableEvents")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                                           timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                           class_type=self.feature_1b05.enable_disable_event_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1B05_0002", _AUTHOR)
    # end def test_get_set_enabled_fkc_toggle_hotkeys

    @features('Keyboard')
    @features("Feature1B05")
    @level("Functionality")
    def test_get_set_power_on_params_fkc_status(self):
        """
        Validate getSetPowerOnParams API can set or get current poweron_fkc_enable
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable power-on FKC by getSetPowerOnParams request with set_poweron_fkc_enable=1"
                                 "and poweron_fkc_enable=1")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_power_on_params(
            test_case=self,
            set_power_on_fkc_enable=FullKeyCustomization.PowerOnFKCRequest.SET,
            power_on_fkc_enable=FullKeyCustomization.PowerOnFKCStatus.ENABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check power-on FKC status is enabled from getSetPowerOnParams response with"
                                  "poweron_fkc_enable=1")
        # --------------------------------------------------------------------------------------------------------------
        power_on_fkc_state_checker = FullKeyCustomizationTestUtils.PowerOnFkcStateChecker
        power_on_fkc_state_map = power_on_fkc_state_checker.get_default_check_map(self)
        power_on_fkc_state_map['power_on_fkc_enable'] = (power_on_fkc_state_checker.check_power_on_fkc_enable,
                                                         FullKeyCustomization.PowerOnFKCStatus.ENABLE)

        checker = FullKeyCustomizationTestUtils.GetSetPowerOnParamsResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map['power_on_fkc_state'] = (checker.check_power_on_fkc_state, power_on_fkc_state_map)
        checker.check_fields(self, response, self.feature_1b05.get_set_power_on_params_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Disable power-on FKC by getSetPowerOnParams request with set_poweron_fkc_enable=1"
                                 "and poweron_fkc_enable=0")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_power_on_params(
            test_case=self,
            set_power_on_fkc_enable=FullKeyCustomization.PowerOnFKCRequest.SET,
            power_on_fkc_enable=FullKeyCustomization.PowerOnFKCStatus.DISABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check power-on FKC status is disabled from getSetPowerOnParams response with"
                                  "poweron_fkc_enable=0")
        # --------------------------------------------------------------------------------------------------------------
        power_on_fkc_state_map['power_on_fkc_enable'] = (power_on_fkc_state_checker.check_power_on_fkc_enable,
                                                         FullKeyCustomization.PowerOnFKCStatus.DISABLE)
        check_map['power_on_fkc_state'] = (checker.check_power_on_fkc_state, power_on_fkc_state_map)
        checker.check_fields(self, response, self.feature_1b05.get_set_power_on_params_response_cls, check_map)

        self.testCaseChecked("FUN_1B05_0003", _AUTHOR)
    # end def test_get_set_power_on_params_fkc_status

    @features('Keyboard')
    @features("Feature1B05")
    @level("Functionality")
    def test_force_release_pressed_keys_when_fkc_changing(self):
        """
        Force release any pressed keys(send HID breaks) when disable/enable FKC
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create a FKC profile and remapping in NVS")
        # --------------------------------------------------------------------------------------------------------------
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(count=1)), enable_fkc=FullKeyCustomization.FKCStatus.DISABLE)
        remapped_key = remapped_keys[0]
        # Wait all key release events
        sleep(1)
        ChannelUtils.empty_queues(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Emulate a keypress on {remapped_key.trigger_key!s}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=remapped_key.trigger_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check DUT sends HID make report of {remapped_key.trigger_key!s}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self,
            key=RemappedKey(action_key=remapped_key.trigger_key, state=MAKE)
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable FKC by getSetEnabled request with set_fkc_enabled=1 and fkc_enabled=1")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.GET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.SET,
            fkc_enabled=FullKeyCustomization.FKCStatus.ENABLE
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check if there are HID breaks to release all keys")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self,
            key=RemappedKey(action_key=remapped_key.trigger_key, state=BREAK)
        )
        ChannelUtils.empty_queues(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Emulate a keyrelease on {remapped_key.trigger_key!s}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=remapped_key.trigger_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check there aren't any HID break reports")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Emulate a keypress on {remapped_key.trigger_key!s}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=remapped_key.trigger_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check DUT sends HID make report of {remapped_key.action_key!s}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self,
            key=RemappedKey(action_key=remapped_key.action_key, state=MAKE)
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Disable FKC by getSetEnabled request with set_fkc_enabled=1 and fkc_enabled=0")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.GET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.SET,
            fkc_enabled=FullKeyCustomization.FKCStatus.DISABLE
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check if there are HID breaks to release all keys")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report_by_remapped_key(
            test_case=self,
            key=RemappedKey(action_key=remapped_key.action_key, state=BREAK)
        )
        ChannelUtils.empty_queues(test_case=self)

        self.testCaseChecked("FUN_1B05_0004", _AUTHOR)
    # end def test_force_release_pressed_keys_when_fkc_changing

    @features('Keyboard')
    @features("Feature1B05")
    @level("Functionality")
    @services('KeyMatrix')
    def test_base_layer_trigger_list_event(self):
        """
        If FKC is enabled, baseLayerTriggerAsListEvent is sent by DUT when keystroke a trigger key
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create a FKC profile with enabled NotifySW flag in RAM buffer")
        # --------------------------------------------------------------------------------------------------------------
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(full_keys=True)), notify_sw=True,
            enable_fkc=FullKeyCustomization.FKCStatus.DISABLE)
        remapped_key = choice(remapped_keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Perform fkc toggle hotkeys")
        # --------------------------------------------------------------------------------------------------------------
        self.perform_fkc_toggle_hotkeys(fkc_status=FullKeyCustomization.FKCStatus.ENABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Emulate a keystroke on {remapped_key.trigger_key!s}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=remapped_key.trigger_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check baseLayerTriggerAsListEvent with key_trigger[0]="
                                  f"(fckIdx of {remapped_key.trigger_key!s}) + 1")
        # --------------------------------------------------------------------------------------------------------------
        base_trigger_list = FullKeyCustomizationTestUtils.HIDppHelper.base_layer_trigger_as_list_event(test_case=self)
        checker = FullKeyCustomizationTestUtils.BaseLayerTriggerAsListEventChecker
        check_map = checker.get_default_check_map(self)
        check_map['key_trigger_0'] = (checker.check_key_trigger_0, remapped_key.fkc_idx + 1)
        checker.check_fields(self, base_trigger_list, self.feature_1b05.base_layer_trigger_as_list_event_cls, check_map)

        self.testCaseChecked("FUN_1B05_0005", _AUTHOR)
    # end def test_base_layer_trigger_list_event

    @features('Keyboard')
    @features("Feature1B05")
    @level("Functionality")
    @services('KeyMatrix')
    @skip("In development")
    def test_base_layer_trigger_bitmap_event(self):
        """
        If FKC is enabled, baseLayerTriggerAsBitmapEvent is sent by DUT when keystroke 17 trigger keys
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create a FKC profile with enabled NotifySW flag in RAM buffer")
        # --------------------------------------------------------------------------------------------------------------
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(full_keys=True)), notify_sw=True,
            enable_fkc=FullKeyCustomization.FKCStatus.DISABLE)
        remapped_17_keys = sample(remapped_keys, 17)
        LogHelper.log_info(self, f'{remapped_17_keys}')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Perform fkc toggle hotkeys")
        # --------------------------------------------------------------------------------------------------------------
        self.perform_fkc_toggle_hotkeys(fkc_status=FullKeyCustomization.FKCStatus.ENABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Emulate keystrokes on 17 trigger_keys simultaneously")
        # --------------------------------------------------------------------------------------------------------------
        trigger_key_ids = []
        for remapped_key in remapped_17_keys:
            trigger_key_ids.append(remapped_key.trigger_key)
        # end for
        LogHelper.log_info(self, f'{trigger_key_ids}')
        self.button_stimuli_emulator.multiple_keys_press(key_ids=trigger_key_ids)
        sleep(ButtonStimuliInterface.DEFAULT_DELAY)
        self.button_stimuli_emulator.multiple_keys_release(key_ids=trigger_key_ids)
        sleep(ButtonStimuliInterface.DEFAULT_DELAY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check baseLayerTriggerAsListEvent with key_trigger_bitmap of fkcIdx of 17 "
                                  "trigger_keys = 1")
        # --------------------------------------------------------------------------------------------------------------
        base_trigger_bitmap = FullKeyCustomizationTestUtils.HIDppHelper.base_layer_trigger_as_bitmap_event(
            test_case=self)

        trigger_bitmap_checker = FullKeyCustomizationTestUtils.KeyTriggerBitmapChecker
        trigger_bitmap_check_map = trigger_bitmap_checker.get_default_check_map(self)
        checker = FullKeyCustomizationTestUtils.BaseLayerTriggerAsBitmapEventChecker
        check_map = checker.get_default_check_map(self)
        for i in range(len(remapped_17_keys)):
            trigger_bitmap_check_map[f'fkc_idx_{remapped_17_keys[i].fkc_idx}'] = (
                getattr(trigger_bitmap_checker, f'check_fkc_idx_{remapped_17_keys[i].fkc_idx}'),
                FullKeyCustomization.KeyState.PRESSED)
            check_map['key_trigger_bitmap'] = (checker.check_key_trigger_bitmap, trigger_bitmap_check_map)
        # end for

        checker.check_fields(self, base_trigger_bitmap, self.feature_1b05.base_layer_trigger_as_bitmap_event_cls,
                             check_map)

        self.testCaseChecked("FUN_1B05_0006", _AUTHOR)
    # end def test_base_layer_trigger_bitmap_event

    @features('Keyboard')
    @features("Feature1B05")
    @level("Functionality")
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.FN_KEY,))
    def test_fn_layer_trigger_list_event(self):
        """
        If FKC is enabled, fnLayerTriggerAsListEvent is sent by DUT when keystroke a trigger key
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create a FKC profile with enabled NotifySW flag in RAM buffer")
        # --------------------------------------------------------------------------------------------------------------
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            layer=FkcMainTable.Layer.FN, button=random_parameters_cls.Button(full_keys=True)), notify_sw=True,
            enable_fkc=FullKeyCustomization.FKCStatus.DISABLE)
        remapped_key = choice(remapped_keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Perform fkc toggle hotkeys")
        # --------------------------------------------------------------------------------------------------------------
        self.perform_fkc_toggle_hotkeys(fkc_status=FullKeyCustomization.FKCStatus.ENABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Emulate keystrokes on FN + {remapped_key.trigger_key!s}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[KEY_ID.FN_KEY, remapped_key.trigger_key],
                                                         delay=ButtonStimuliInterface.DEFAULT_DELAY)
        self.button_stimuli_emulator.multiple_keys_release(key_ids=[remapped_key.trigger_key, KEY_ID.FN_KEY],
                                                           delay=ButtonStimuliInterface.DEFAULT_DELAY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check fnLayerTriggerAsListEvent with key_trigger[0]="
                                  f"(fckIdx of {remapped_key.trigger_key!s}) + 1")
        # --------------------------------------------------------------------------------------------------------------
        fn_trigger_list = FullKeyCustomizationTestUtils.HIDppHelper.fn_layer_trigger_as_list_event(test_case=self)
        checker = FullKeyCustomizationTestUtils.FNLayerTriggerAsListEventChecker
        check_map = checker.get_default_check_map(self)
        check_map['key_trigger_0'] = (checker.check_key_trigger_0, remapped_key.fkc_idx + 1)
        checker.check_fields(self, fn_trigger_list, self.feature_1b05.fn_layer_trigger_as_list_event_cls, check_map)

        self.testCaseChecked("FUN_1B05_0007", _AUTHOR)
    # end def test_fn_layer_trigger_list_event

    @features('Keyboard')
    @features("Feature1B05")
    @level("Functionality")
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.FN_KEY,))
    @skip("In development")
    def test_fn_layer_trigger_bitmap_event(self):
        """
        If FKC is enabled, fnLayerTriggerAsBitmapEvent is sent by DUT when keystroke 17 trigger keys
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create a FKC profile with enabled NotifySW flag in RAM buffer")
        # --------------------------------------------------------------------------------------------------------------
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            layer=FkcMainTable.Layer.FN, button=random_parameters_cls.Button(full_keys=True)), notify_sw=True,
            enable_fkc=FullKeyCustomization.FKCStatus.DISABLE)
        remapped_17_keys = sample(remapped_keys, 17)
        LogHelper.log_info(self, f'{remapped_17_keys}')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Perform fkc toggle hotkeys")
        # --------------------------------------------------------------------------------------------------------------
        self.perform_fkc_toggle_hotkeys(fkc_status=FullKeyCustomization.FKCStatus.ENABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Emulate keystrokes on FN + 17 trigger_keys simultaneously")
        # --------------------------------------------------------------------------------------------------------------
        trigger_key_ids = []
        for remapped_key in remapped_17_keys:
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
        LogHelper.log_check(self, "Check fnLayerTriggerAsListEvent with key_trigger_bitmap of fkcIdx of 17 "
                                  "trigger_keys = 1")
        # --------------------------------------------------------------------------------------------------------------
        fn_trigger_bitmap = FullKeyCustomizationTestUtils.HIDppHelper.fn_layer_trigger_as_bitmap_event(
            test_case=self)

        trigger_bitmap_checker = FullKeyCustomizationTestUtils.KeyTriggerBitmapChecker
        trigger_bitmap_check_map = trigger_bitmap_checker.get_default_check_map(self)
        checker = FullKeyCustomizationTestUtils.FNLayerTriggerAsBitmapEventChecker
        check_map = checker.get_default_check_map(self)
        for i in range(len(remapped_17_keys)):
            trigger_bitmap_check_map[f'fkc_idx_{remapped_17_keys[i].fkc_idx}'] = (
                getattr(trigger_bitmap_checker, f'check_fkc_idx_{remapped_17_keys[i].fkc_idx}'),
                FullKeyCustomization.KeyState.PRESSED)
            check_map['key_trigger_bitmap'] = (checker.check_key_trigger_bitmap, trigger_bitmap_check_map)
        # end for

        checker.check_fields(self, fn_trigger_bitmap, self.feature_1b05.fn_layer_trigger_as_bitmap_event_cls,
                             check_map)

        self.testCaseChecked("FUN_1B05_0008", _AUTHOR)
    # end def test_fn_layer_trigger_bitmap_event

    @features('Keyboard')
    @features("Feature1B05")
    @level("Functionality")
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.G_SHIFT,))
    def test_gshift_layer_trigger_list_event(self):
        """
        If FKC is enabled, gshiftLayerTriggerAsListEvent is sent by DUT when keystroke a trigger key
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create a FKC profile with enabled NotifySW flag in RAM buffer")
        # --------------------------------------------------------------------------------------------------------------
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            layer=FkcMainTable.Layer.GSHIFT, button=random_parameters_cls.Button(full_keys=True)), notify_sw=True,
            enable_fkc=FullKeyCustomization.FKCStatus.DISABLE)
        remapped_key = choice(remapped_keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Perform fkc toggle hotkeys")
        # --------------------------------------------------------------------------------------------------------------
        self.perform_fkc_toggle_hotkeys(fkc_status=FullKeyCustomization.FKCStatus.ENABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Emulate keystrokes on GSHIFT + {remapped_key.trigger_key!s}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[KEY_ID.G_SHIFT, remapped_key.trigger_key],
                                                         delay=ButtonStimuliInterface.DEFAULT_DELAY)
        self.button_stimuli_emulator.multiple_keys_release(key_ids=[remapped_key.trigger_key, KEY_ID.G_SHIFT],
                                                           delay=ButtonStimuliInterface.DEFAULT_DELAY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check gshiftLayerTriggerAsListEvent with key_trigger[0]="
                                  f"(fckIdx of {remapped_key.trigger_key!s}) + 1")
        # --------------------------------------------------------------------------------------------------------------
        gshift_trigger_list = FullKeyCustomizationTestUtils.HIDppHelper.gshift_layer_trigger_as_list_event(
            test_case=self)
        checker = FullKeyCustomizationTestUtils.GShiftLayerTriggerAsListEventChecker
        check_map = checker.get_default_check_map(self)
        check_map['key_trigger_0'] = (checker.check_key_trigger_0, remapped_key.fkc_idx + 1)
        checker.check_fields(self, gshift_trigger_list, self.feature_1b05.gshift_layer_trigger_as_list_event_cls,
                             check_map)

        self.testCaseChecked("FUN_1B05_0009", _AUTHOR)
    # end def test_gshift_layer_trigger_list_event

    @features('Keyboard')
    @features("Feature1B05")
    @level("Functionality")
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.G_SHIFT,))
    @skip("In development")
    def test_gshift_layer_trigger_bitmap_event(self):
        """
        If FKC is enabled, gshiftLayerTriggerAsBitmapEvent is sent by DUT when keystroke 17 trigger keys
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create a FKC profile with enabled NotifySW flag in RAM buffer")
        # --------------------------------------------------------------------------------------------------------------
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            layer=FkcMainTable.Layer.GSHIFT, button=random_parameters_cls.Button(full_keys=True)), notify_sw=True,
            enable_fkc=FullKeyCustomization.FKCStatus.DISABLE)
        remapped_17_keys = sample(remapped_keys, 17)
        LogHelper.log_info(self, f'{remapped_17_keys}')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Perform fkc toggle hotkeys")
        # --------------------------------------------------------------------------------------------------------------
        self.perform_fkc_toggle_hotkeys(fkc_status=FullKeyCustomization.FKCStatus.ENABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Emulate keystrokes on GSHIFT + 17 trigger_keys simultaneously")
        # --------------------------------------------------------------------------------------------------------------
        trigger_key_ids = []
        for remapped_key in remapped_17_keys:
            trigger_key_ids.append(remapped_key.trigger_key)
        # end for
        LogHelper.log_info(self, f'{trigger_key_ids}')
        self.button_stimuli_emulator.keys_press(key_ids=KEY_ID.G_SHIFT)
        sleep(ButtonStimuliInterface.DEFAULT_DELAY)
        self.button_stimuli_emulator.multiple_keys_press(key_ids=trigger_key_ids)
        sleep(ButtonStimuliInterface.DEFAULT_DELAY)
        self.button_stimuli_emulator.multiple_keys_release(key_ids=trigger_key_ids)
        sleep(ButtonStimuliInterface.DEFAULT_DELAY)
        self.button_stimuli_emulator.key_release(key_ids=KEY_ID.G_SHIFT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check gshiftLayerTriggerAsListEvent with key_trigger_bitmap of fkcIdx of 17 "
                                  "trigger_keys = 1")
        # --------------------------------------------------------------------------------------------------------------
        gshift_trigger_bitmap = FullKeyCustomizationTestUtils.HIDppHelper.gshift_layer_trigger_as_bitmap_event(
            test_case=self)

        trigger_bitmap_checker = FullKeyCustomizationTestUtils.KeyTriggerBitmapChecker
        trigger_bitmap_check_map = trigger_bitmap_checker.get_default_check_map(self)
        checker = FullKeyCustomizationTestUtils.GShiftLayerTriggerAsBitmapEventChecker
        check_map = checker.get_default_check_map(self)
        for i in range(len(remapped_17_keys)):
            trigger_bitmap_check_map[f'fkc_idx_{remapped_17_keys[i].fkc_idx}'] = (
                getattr(trigger_bitmap_checker, f'check_fkc_idx_{remapped_17_keys[i].fkc_idx}'),
                FullKeyCustomization.KeyState.PRESSED)
            check_map['key_trigger_bitmap'] = (checker.check_key_trigger_bitmap, trigger_bitmap_check_map)
        # end for

        checker.check_fields(self, gshift_trigger_bitmap, self.feature_1b05.gshift_layer_trigger_as_bitmap_event_cls,
                             check_map)

        self.testCaseChecked("FUN_1B05_0010", _AUTHOR)
    # end def test_gshift_layer_trigger_bitmap_event

    @features('Keyboard')
    @features("Feature1B05")
    @level("Functionality")
    @services('KeyMatrix')
    def test_fkc_toggle_hotkeys(self):
        """
        Validate FKC toggle keys can enable/disable FKC
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create a FKC profile and remapping in RAM buffer")
        # --------------------------------------------------------------------------------------------------------------
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(count=3)), enable_fkc=FullKeyCustomization.FKCStatus.DISABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Validate all remapped_keys")
        # --------------------------------------------------------------------------------------------------------------
        self._validate_remapped_keys(remapped_keys=remapped_keys, fkc_status=FullKeyCustomization.FKCStatus.DISABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable all toggle hotkeys by getSetEnabled request with "
                                 "set_toggle_keys_enabled=1 and toggle_keys_enabled=0xFF")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.SET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET,
            toggle_keys_enabled=0xFF)

        toggle_keys_checker = FullKeyCustomizationTestUtils.ToggleKeysStateChecker
        toggle_keys_state_check_map = toggle_keys_checker.get_default_check_map(self)
        toggle_keys_state_check_map['toggle_key_7_enabled'] = (toggle_keys_checker.check_toggle_key_7_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.ENABLE)
        toggle_keys_state_check_map['toggle_key_6_enabled'] = (toggle_keys_checker.check_toggle_key_6_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.ENABLE)
        toggle_keys_state_check_map['toggle_key_5_enabled'] = (toggle_keys_checker.check_toggle_key_5_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.ENABLE)
        toggle_keys_state_check_map['toggle_key_4_enabled'] = (toggle_keys_checker.check_toggle_key_4_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.ENABLE)
        toggle_keys_state_check_map['toggle_key_3_enabled'] = (toggle_keys_checker.check_toggle_key_3_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.ENABLE)
        toggle_keys_state_check_map['toggle_key_2_enabled'] = (toggle_keys_checker.check_toggle_key_2_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.ENABLE)
        toggle_keys_state_check_map['toggle_key_1_enabled'] = (toggle_keys_checker.check_toggle_key_1_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.ENABLE)
        toggle_keys_state_check_map['toggle_key_0_enabled'] = (toggle_keys_checker.check_toggle_key_0_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.ENABLE)

        for toggle_key_idx in range(FullKeyCustomization.TOGGLE_HOTKEYS_CNT):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Perform fkc toggle hotkeys")
            # ----------------------------------------------------------------------------------------------------------
            self.perform_fkc_toggle_hotkeys(fkc_status=FullKeyCustomization.FKCStatus.ENABLE,
                                            toggle_key_index=toggle_key_idx)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Get FKC status by getSetEnabled request with set_fkc_enabled=0")
            # ----------------------------------------------------------------------------------------------------------
            response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
                self,
                set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.GET,
                set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check FKC status is enabled from getSetEnabled response with fkc_enabled=1")
            # ----------------------------------------------------------------------------------------------------------
            fkc_state_checker = FullKeyCustomizationTestUtils.FkcStateChecker
            fkc_state_check_map = fkc_state_checker.get_default_check_map(self)
            fkc_state_check_map['fkc_enabled'] = (fkc_state_checker.check_fkc_enabled,
                                                  FullKeyCustomization.FKCStatus.ENABLE)

            checker = FullKeyCustomizationTestUtils.GetSetEnabledResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map['fkc_state'] = (checker.check_fkc_state, fkc_state_check_map)
            check_map['toggle_keys_state'] = (checker.check_toggle_keys_state, toggle_keys_state_check_map)

            checker.check_fields(self, response, self.feature_1b05.get_set_enabled_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Validate all remapped_keys")
            # ----------------------------------------------------------------------------------------------------------
            self._validate_remapped_keys(remapped_keys=remapped_keys, fkc_status=FullKeyCustomization.FKCStatus.ENABLE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Perform fkc toggle hotkeys")
            # ----------------------------------------------------------------------------------------------------------
            self.perform_fkc_toggle_hotkeys(fkc_status=FullKeyCustomization.FKCStatus.DISABLE,
                                            toggle_key_index=toggle_key_idx)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Get FKC status by getSetEnabled request with set_fkc_enabled=0")
            # ----------------------------------------------------------------------------------------------------------
            response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
                self,
                set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.GET,
                set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check FKC status is disabled from getSetEnabled response with "
                                      "fkc_enabled=0")
            # ----------------------------------------------------------------------------------------------------------
            fkc_state_check_map['fkc_enabled'] = (fkc_state_checker.check_fkc_enabled,
                                                  FullKeyCustomization.FKCStatus.DISABLE)
            check_map['fkc_state'] = (checker.check_fkc_state, fkc_state_check_map)
            checker.check_fields(self, response, self.feature_1b05.get_set_enabled_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Validate all remapped_keys")
            # ----------------------------------------------------------------------------------------------------------
            self._validate_remapped_keys(remapped_keys=remapped_keys, fkc_status=FullKeyCustomization.FKCStatus.DISABLE)
        # end for

        self.testCaseChecked("FUN_1B05_0011", _AUTHOR)
    # end def test_fkc_toggle_hotkeys

    @features('Keyboard')
    @features("Feature1B05")
    @level("Functionality")
    @services('KeyMatrix')
    def test_fkc_toggle_hotkeys_overwrite_power_on_fkc(self):
        """
        When the user enables or disables FKC by pressing a FKC toggle hotkey, the device shall update the
        poweron_fkc_enable to match the current enabled status
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create a FKC profile and remapping in RAM buffer")
        # --------------------------------------------------------------------------------------------------------------
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        self.create_remapping_in_ram(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(count=1)), enable_fkc=FullKeyCustomization.FKCStatus.DISABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Perform fkc toggle hotkeys")
        # --------------------------------------------------------------------------------------------------------------
        self.perform_fkc_toggle_hotkeys(fkc_status=FullKeyCustomization.FKCStatus.ENABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get power-on FKC by getSetPowerOnParams request with set_poweron_fkc_enable=0 and"
                                 "poweron_fkc_enable=0")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_power_on_params(
            test_case=self, set_power_on_fkc_enable=FullKeyCustomization.PowerOnFKCRequest.GET)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check power-on FKC status is enable from getSetPowerOnParams response with"
                                  "poweron_fkc_enable=1")
        # --------------------------------------------------------------------------------------------------------------
        power_on_fkc_state_checker = FullKeyCustomizationTestUtils.PowerOnFkcStateChecker
        power_on_fkc_state_map = power_on_fkc_state_checker.get_default_check_map(self)
        power_on_fkc_state_map['power_on_fkc_enable'] = (power_on_fkc_state_checker.check_power_on_fkc_enable,
                                                         FullKeyCustomization.PowerOnFKCStatus.ENABLE)

        checker = FullKeyCustomizationTestUtils.GetSetPowerOnParamsResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map['power_on_fkc_state'] = (checker.check_power_on_fkc_state, power_on_fkc_state_map)
        checker.check_fields(self, response, self.feature_1b05.get_set_power_on_params_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Perform fkc toggle hotkeys")
        # --------------------------------------------------------------------------------------------------------------
        self.perform_fkc_toggle_hotkeys(fkc_status=FullKeyCustomization.FKCStatus.DISABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get power-on FKC by getSetPowerOnParams request with set_poweron_fkc_enable=0 and"
                                 "poweron_fkc_enable=0")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_power_on_params(
            test_case=self, set_power_on_fkc_enable=FullKeyCustomization.PowerOnFKCRequest.GET)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check power-on FKC status is enable from getSetPowerOnParams response with"
                                  "poweron_fkc_enable=0")
        # --------------------------------------------------------------------------------------------------------------
        power_on_fkc_state_map['power_on_fkc_enable'] = (power_on_fkc_state_checker.check_power_on_fkc_enable,
                                                         FullKeyCustomization.PowerOnFKCStatus.DISABLE)
        check_map['power_on_fkc_state'] = (checker.check_power_on_fkc_state, power_on_fkc_state_map)
        checker.check_fields(self, response, self.feature_1b05.get_set_power_on_params_response_cls, check_map)

        self.testCaseChecked("FUN_1B05_0012", _AUTHOR)
    # end def test_fkc_toggle_hotkeys_overwrite_power_on_fkc

    @features('Keyboard')
    @features("Feature1B05")
    @level("Functionality")
    @services('KeyMatrix')
    def test_fkc_status_decouple(self):
        """
        Validate the FKC status is completely decoupled across different profiles
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create two FKC profiles for the remapping in NVS(activate profile1 and "
                                         "enable FKC)")
        # --------------------------------------------------------------------------------------------------------------
        max_profile_count = self.f.PRODUCT.FEATURES.GAMING.PROFILE_MANAGEMENT.F_NumOnboardProfiles
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys, profiles = self.create_remapping_in_nvs(
            random_parameters=random_parameters_cls(profile_count=max_profile_count,
                                                    button=random_parameters_cls.Button(full_keys=True)),
            enable_fkc=FullKeyCustomization.FKCStatus.ENABLE
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check FKC status is ON by getSetEnabled")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.GET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET,
        )
        fkc_state_checker = FullKeyCustomizationTestUtils.FkcStateChecker
        fkc_state_check_map = fkc_state_checker.get_default_check_map(self)
        fkc_state_check_map['fkc_enabled'] = (fkc_state_checker.check_fkc_enabled,
                                              FullKeyCustomization.FKCStatus.ENABLE)
        checker = FullKeyCustomizationTestUtils.GetSetEnabledResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map['fkc_state'] = (checker.check_fkc_state, fkc_state_check_map)
        checker.check_fields(self, response, self.feature_1b05.get_set_enabled_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Activate on-board profile2 in NVS by 0x8101.configure")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(
            test_case=self, feature_id=ProfileManagement.FEATURE_ID,
            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
            file_id=ProfileManagement.Partition.FileId.NVS | profiles[1].file_id_lsb,
            count=len(HexList(profiles[1])),
            crc_32=profiles[1].crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check FKC status is ON by getSetEnabled")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.GET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET,
        )
        checker.check_fields(self, response, self.feature_1b05.get_set_enabled_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Disable FKC by getSetEnabled")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.GET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.SET,
            fkc_enabled=FullKeyCustomization.FKCStatus.DISABLE,
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Activate on-board profile1 in NVS by 0x8101.configure")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(
            test_case=self, feature_id=ProfileManagement.FEATURE_ID,
            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
            file_id=ProfileManagement.Partition.FileId.NVS | profiles[0].file_id_lsb,
            count=len(HexList(profiles[0])),
            crc_32=profiles[0].crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check FKC status is OFF by getSetEnabled")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.GET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET,
        )
        fkc_state_check_map['fkc_enabled'] = (fkc_state_checker.check_fkc_enabled,
                                              FullKeyCustomization.FKCStatus.DISABLE)
        check_map['fkc_state'] = (checker.check_fkc_state, fkc_state_check_map)
        checker.check_fields(self, response, self.feature_1b05.get_set_enabled_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Activate on-board profile2 in NVS by 0x8101.configure")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(
            test_case=self, feature_id=ProfileManagement.FEATURE_ID,
            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
            file_id=ProfileManagement.Partition.FileId.NVS | profiles[1].file_id_lsb,
            count=len(HexList(profiles[1])),
            crc_32=profiles[1].crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check FKC status is OFF by getSetEnabled")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.GET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET,
        )
        checker.check_fields(self, response, self.feature_1b05.get_set_enabled_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable FKC by getSetEnabled")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.GET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.SET,
            fkc_enabled=FullKeyCustomization.FKCStatus.ENABLE,
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Activate on-board profile1 in NVS by 0x8101.configure")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(
            test_case=self, feature_id=ProfileManagement.FEATURE_ID,
            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
            file_id=ProfileManagement.Partition.FileId.NVS | profiles[0].file_id_lsb,
            count=len(HexList(profiles[0])),
            crc_32=profiles[0].crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check FKC status is ON by getSetEnabled")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.GET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET,
        )
        fkc_state_check_map['fkc_enabled'] = (fkc_state_checker.check_fkc_enabled,
                                              FullKeyCustomization.FKCStatus.ENABLE)
        check_map['fkc_state'] = (checker.check_fkc_state, fkc_state_check_map)
        checker.check_fields(self, response, self.feature_1b05.get_set_enabled_response_cls, check_map)
        self.testCaseChecked("FUN_1B05_0013", _AUTHOR)
    # end def test_fkc_status_decouple

    @features("Feature1B05V1+")
    @level("Functionality")
    def test_get_set_sw_configuration_cookie(self):
        """
        Validate getSetSWConfigurationCookie is able to set and get SWConfigurationCookie
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over {sw_cfg_cookie} in valid range of sw_configuration_cookie")
        # --------------------------------------------------------------------------------------------------------------
        for sw_cfg_cookie in [2 ** i for i in range(GetSetSWConfigurationCookieV1.LEN.SW_CONFIGURATION_COOKIE)]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set SWConfigurationCookie by getSetSWConfigurationCookie request with "
                                     f"set_sw_configuration_cookie=1 and sw_configuration_cookie={sw_cfg_cookie}")
            # ----------------------------------------------------------------------------------------------------------
            response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_sw_configuration_cookie(
                test_case=self,
                set_sw_configuration_cookie=FullKeyCustomization.SWConfigurationCookieRequest.SET,
                sw_configuration_cookie=sw_cfg_cookie,
            )

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check sw_configuration_cookie from getSetSWConfigurationCookie response with"
                                      f"sw_configuration_cookie={sw_cfg_cookie}")
            # ----------------------------------------------------------------------------------------------------------
            checker = FullKeyCustomizationTestUtils.GetSetSWConfigurationCookieResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map['sw_configuration_cookie'] = (checker.check_sw_configuration_cookie, sw_cfg_cookie)
            checker.check_fields(self, response, self.feature_1b05.get_set_sw_configuration_cookie_response_cls,
                                 check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Get SWConfigurationCookie by getSetSWConfigurationCookie request with"
                                     "set_sw_configuration_cookie=0")
            # ----------------------------------------------------------------------------------------------------------
            response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_sw_configuration_cookie(
                test_case=self,
                set_sw_configuration_cookie=FullKeyCustomization.SWConfigurationCookieRequest.GET,
            )

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check sw_configuration_cookie from getSetSWConfigurationCookie response with"
                                      f"sw_configuration_cookie={sw_cfg_cookie}")
            # ----------------------------------------------------------------------------------------------------------
            checker.check_fields(self, response, self.feature_1b05.get_set_sw_configuration_cookie_response_cls,
                                 check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1B05_0014", _AUTHOR)
    # end def test_get_set_sw_configuration_cookie
# end class FullKeyCustomizationFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
