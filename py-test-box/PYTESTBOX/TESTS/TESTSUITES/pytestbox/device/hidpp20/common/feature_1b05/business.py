#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1b05.business
:brief: HID++ 2.0 ``FullKeyCustomization`` business test suite
:author: Masan Xu <mxu11@logitech.com>
:date: 2023/05/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep
from unittest import skip

from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.fullkeycustomization import FullKeyCustomization
from pylibrary.mcu.fkcprofileformat import RemappedKey
from pylibrary.mcu.profileformat import PresetMacroEntry
from pylibrary.mcu.profileformat import RepeatWhilePressedCommand
from pylibrary.mcu.profileformat import StandardKeyCommand
from pylibrary.mcu.profileformat import WaitForXmsCommand
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.controllistutils import ControlListTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.fullkeycustomizationutils import FullKeyCustomizationTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.base.rgbeffectsutils import RGBEffectsTestUtils
from pytestbox.device.hidpp20.common.feature_1b05.fullkeycustomization import FullKeyCustomizationTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Masan Xu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class FullKeyCustomizationBusinessTestCase(FullKeyCustomizationTestCase):
    """
    Validate ``FullKeyCustomization`` business test cases
    """

    @features('Keyboard')
    @features("Feature1B05")
    @features('Feature1830powerMode', 3)
    @level("Business")
    def test_fkc_resume_key_processing(self):
        """
        If poweron_fkc_enable is TRUE, then when the user wakes up the device by pressing a key, then FKC must first
        be enabled before processing that keypress, and no following keypresses shall be lost
        PS: Acceptable processing delay in this case is TBD
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create a FKC profile and remapping in NVS and enable FKC")
        # --------------------------------------------------------------------------------------------------------------
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(count=1)))
        remapped_key = remapped_keys[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable power on FKC by getSetPowerOnParams request with set_poweron_fkc_enable=1 "
                                 "and poweron_fkc_enable=1")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.HIDppHelper.get_set_power_on_params(
            self,
            set_power_on_fkc_enable=FullKeyCustomization.PowerOnFKCRequest.SET,
            power_on_fkc_enable=FullKeyCustomization.PowerOnFKCStatus.ENABLE
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Empty HID queue")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set DUT into deep sleep mode by 0x1830.SetPowerMode request with PowerModeNumber=3")
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Emulate a keystroke on the trigger key: {remapped_key.trigger_key!s} with "
                                 f"duration {self.FKC_WAKE_UP_DELAY} sec")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=remapped_key.trigger_key, duration=self.FKC_WAKE_UP_DELAY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check there are HID reports of {remapped_key.action_key!s}")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(test_case=self, remapped_key=remapped_key)

        self.testCaseChecked("BUS_1B05_0001", _AUTHOR)
    # end def test_fkc_resume_key_processing

    @features('Keyboard')
    @features("Feature1B05")
    @level("Business")
    @services('KeyMatrix')
    @skip("In development")
    # TODO: Add a flag to determine KBD is 60, TKL or FS and specify a LED pattern before changing FKC status
    def test_fkc_led(self):
        """
        Validate user can observe the effect by visual confirmation only when enable FKC
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create a FKC profile and remapping in RAM buffer")
        # --------------------------------------------------------------------------------------------------------------
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        self.create_remapping_in_ram(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(count=1)))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Set FKC status key to solid green by 0x8071")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Set FKC status key to solid green by 0x8071

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Emulate keystrokes on OOB_FKC_toggle_hotkey to enable FKC")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.set_fkc_state_by_toggle_key(test_case=self,
                                                                  enable=FullKeyCustomization.FKCStatus.ENABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the LED of FKC status key steadies while for 5 sec")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Check FKC status LED

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the LED of FKC status key resumes to solid green")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Check FKC status LED

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Emulate keystrokes on OOB_FKC_toggle_hotkey to disable FKC")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.set_fkc_state_by_toggle_key(test_case=self,
                                                                  enable=FullKeyCustomization.FKCStatus.DISABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the LED of FKC status is solid green")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Check FKC status LED

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, 'Step LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        self.testCaseChecked("BUS_1B05_0002", _AUTHOR)
    # end def test_fkc_led

    @features('Keyboard')
    @features("Feature1B05")
    @level("Business")
    @services('KeyMatrix')
    def test_en_dis_event_when_toggle_fkc_hotkeys(self):
        """
        When the user enables or disables FKC by pressing a FKC toggle hotkey, the device that report this as an
        event to the host SW
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create a FKC profile and remapping in RAM buffer")
        # --------------------------------------------------------------------------------------------------------------
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        self.create_remapping_in_ram(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(count=1)), enable_fkc=FullKeyCustomization.FKCStatus.DISABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Emulate keystrokes OOB_FKC_toggle_hotkey to enable FKC")
        # --------------------------------------------------------------------------------------------------------------
        toggle_key_setting = getattr(self.f.PRODUCT.FEATURES.COMMON.FULL_KEY_CUSTOMIZATION, f'F_ToggleKey0Cidx')
        toggle_key_1 = ControlListTestUtils.cidx_to_key_id(test_case=self,
                                                           cid_index=to_int(toggle_key_setting[0]))
        toggle_key_2 = ControlListTestUtils.cidx_to_key_id(test_case=self,
                                                           cid_index=to_int(toggle_key_setting[1]))
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[toggle_key_1, toggle_key_2], delay=0.05)
        self.button_stimuli_emulator.multiple_keys_release(key_ids=[toggle_key_2, toggle_key_1], delay=0.05)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check enableDisableEvent with enabled=1 and failure=0")
        # --------------------------------------------------------------------------------------------------------------
        enable_disable_event = FullKeyCustomizationTestUtils.HIDppHelper.enable_disable_event(test_case=self)
        fkc_failure_enabled_checker = FullKeyCustomizationTestUtils.FkcFailureEnabledStateChecker
        fkc_failure_enabled_map = fkc_failure_enabled_checker.get_default_check_map(self)
        fkc_failure_enabled_map['enabled'] = (fkc_failure_enabled_checker.check_enabled,
                                              FullKeyCustomization.FKCStatus.ENABLE)
        fkc_failure_enabled_map['failure'] = (fkc_failure_enabled_checker.check_failure,
                                              FullKeyCustomization.EnableDisableStatus.SUCCESS)
        checker = FullKeyCustomizationTestUtils.EnableDisableEventChecker
        check_map = checker.get_default_check_map(self)
        check_map['fkc_failure_enabled_state'] = (checker.check_fkc_failure_enabled_state, fkc_failure_enabled_map)
        checker.check_fields(self, enable_disable_event, self.feature_1b05.enable_disable_event_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Emulate keystrokes OOB_FKC_toggle_hotkey to disable FKC")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[toggle_key_1, toggle_key_2], delay=0.05)
        self.button_stimuli_emulator.multiple_keys_release(key_ids=[toggle_key_2, toggle_key_1], delay=0.05)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check enableDisableEvent with enabled=0 and failure=0")
        # --------------------------------------------------------------------------------------------------------------
        enable_disable_event = FullKeyCustomizationTestUtils.HIDppHelper.enable_disable_event(test_case=self)
        fkc_failure_enabled_checker = FullKeyCustomizationTestUtils.FkcFailureEnabledStateChecker
        fkc_failure_enabled_map = fkc_failure_enabled_checker.get_default_check_map(self)
        fkc_failure_enabled_map['enabled'] = (fkc_failure_enabled_checker.check_enabled,
                                              FullKeyCustomization.FKCStatus.DISABLE)
        fkc_failure_enabled_map['failure'] = (fkc_failure_enabled_checker.check_failure,
                                              FullKeyCustomization.EnableDisableStatus.SUCCESS)
        checker = FullKeyCustomizationTestUtils.EnableDisableEventChecker
        check_map = checker.get_default_check_map(self)
        check_map['fkc_failure_enabled_state'] = (checker.check_fkc_failure_enabled_state, fkc_failure_enabled_map)
        checker.check_fields(self, enable_disable_event, self.feature_1b05.enable_disable_event_cls, check_map)

        self.testCaseChecked("BUS_1B05_0003", _AUTHOR)
    # end def test_en_dis_event_when_toggle_fkc_hotkeys

    @features('Keyboard')
    @features("Feature1B05")
    @level('Business', 'SmokeTests')
    def test_fkc_status_after_power_cycle(self):
        """
        Validate DUT FKC status(Enable/Disable) after power-cycle
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create a FKC profile and remapping in NVS")
        # --------------------------------------------------------------------------------------------------------------
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(count=1)), enable_fkc=FullKeyCustomization.FKCStatus.DISABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable power on FKC by getSetPowerOnParams request with set_poweron_fkc_enable=1 "
                                 "and poweron_fkc_enable=1")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.HIDppHelper.get_set_power_on_params(
            self,
            set_power_on_fkc_enable=FullKeyCustomization.PowerOnFKCRequest.SET,
            power_on_fkc_enable=FullKeyCustomization.PowerOnFKCStatus.ENABLE
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power cycle DUT")
        # --------------------------------------------------------------------------------------------------------------
        if self.is_hardware_reset_possible():
            self.reset(hardware_reset=True, verify_connection_reset=False,
                       verify_wireless_device_status_broadcast_event=False)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get FKC status by getSetEnabled request with set_fkc_enabled=0")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.GET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET,
        )

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
        LogHelper.log_step(self, "Disable power on FKC by getSetPowerOnParams request with set_poweron_fkc_enable=1 "
                                 "and poweron_fkc_enable=0")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.HIDppHelper.get_set_power_on_params(
            self,
            set_power_on_fkc_enable=FullKeyCustomization.PowerOnFKCRequest.SET,
            power_on_fkc_enable=FullKeyCustomization.PowerOnFKCStatus.DISABLE
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power cycle DUT")
        # --------------------------------------------------------------------------------------------------------------
        if self.is_hardware_reset_possible():
            DeviceBaseTestUtils.ResetHelper.hardware_reset(test_case=self)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get FKC status by getSetEnabled request with set_fkc_enabled=0")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.GET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET,
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check FKC is disabled from getSetEnabled response with fkc_enabled=0")
        # --------------------------------------------------------------------------------------------------------------
        fkc_state_check_map['fkc_enabled'] = (fkc_state_checker.check_fkc_enabled,
                                              FullKeyCustomization.FKCStatus.DISABLE)

        check_map['fkc_state'] = (checker.check_fkc_state, fkc_state_check_map)
        checker.check_fields(self, response, self.feature_1b05.get_set_enabled_response_cls, check_map)

        self.testCaseChecked("BUS_1B05_0004", _AUTHOR)
    # end def test_fkc_status_after_power_cycle

    @features('Keyboard')
    @features("Feature1B05")
    @features('Feature1830powerMode', 3)
    @level("Business")
    def test_fkc_status_after_deep_sleep(self):
        """
        Validate DUT FKC status(Enable/Disable) after resuming from deep-sleep
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create a FKC profile and remapping in NVS")
        # --------------------------------------------------------------------------------------------------------------
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(count=1)), enable_fkc=FullKeyCustomization.FKCStatus.DISABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable power-on FKC by getSetPowerOnParams request with set_poweron_fkc_enable=1"
                                 "and poweron_fkc_enable=1")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.HIDppHelper.get_set_power_on_params(
            self,
            set_power_on_fkc_enable=FullKeyCustomization.PowerOnFKCRequest.SET,
            power_on_fkc_enable=FullKeyCustomization.PowerOnFKCStatus.ENABLE
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set DUT into deep sleep mode by 0x1830.SetPowerMode request with PowerModeNumber=3")
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke "return_enter" to wake up DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get FKC status by getSetEnabled request with set_fkc_enabled=0")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.GET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET)

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
        LogHelper.log_step(self, "Disable power on FKC by getSetPowerOnParams request with set_poweron_fkc_enable=1"
                                 "and poweron_fkc_enable=0")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.HIDppHelper.get_set_power_on_params(
            self,
            set_power_on_fkc_enable=FullKeyCustomization.PowerOnFKCRequest.SET,
            power_on_fkc_enable=FullKeyCustomization.PowerOnFKCStatus.DISABLE
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set DUT into deep sleep mode by 0x1830.SetPowerMode request with PowerModeNumber=3")
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke "return_enter" to wake up DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get FKC status by getSetEnabled request with set_fkc_enabled=0")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.GET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET,
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check FKC is disabled from getSetEnabled response with fkc_enabled=0")
        # --------------------------------------------------------------------------------------------------------------
        fkc_state_check_map['fkc_enabled'] = (fkc_state_checker.check_fkc_enabled,
                                              FullKeyCustomization.FKCStatus.DISABLE)

        check_map['fkc_state'] = (checker.check_fkc_state, fkc_state_check_map)
        checker.check_fields(self, response, self.feature_1b05.get_set_enabled_response_cls, check_map)

        self.testCaseChecked("BUS_1B05_0005", _AUTHOR)
    # end def test_fkc_status_after_deep_sleep

    @features('Keyboard')
    @features("Feature1B05")
    @level("Business")
    def test_toggle_keys_status_after_power_cycle(self):
        """
        As a user, I expect that my choice of FKC toggle hotkeys will remain the same after a power-cycle
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable all toggle hotkeys by getSetEnabled request with set_toggle_keys_enabled=1"
                                 "and toggle_keys_enabled=0xFF")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.SET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET,
            toggle_keys_enabled=0xFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check all toggle hotkeys are enabled from getSetEnabled response with "
                                  "toggle_keys_enabled=0xFF")
        # --------------------------------------------------------------------------------------------------------------
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

        checker = FullKeyCustomizationTestUtils.GetSetEnabledResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map['toggle_keys_state'] = (checker.check_toggle_keys_state, toggle_keys_state_check_map)
        checker.check_fields(self, response, self.feature_1b05.get_set_enabled_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power cycle DUT")
        # --------------------------------------------------------------------------------------------------------------
        if self.is_hardware_reset_possible():
            self.reset(hardware_reset=True, verify_connection_reset=False,
                       verify_wireless_device_status_broadcast_event=False)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get all toggle hotkeys status by getSetEnabled request with "
                                 "set_toggle_keys_enabled=0")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.PowerOnFKCRequest.GET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check all toggle hotkeys are enabled from getSetEnabled response with "
                                  "toggle_keys_enabled=0xFF")
        # --------------------------------------------------------------------------------------------------------------
        check_map['toggle_keys_state'] = (checker.check_toggle_keys_state, toggle_keys_state_check_map)
        checker.check_fields(self, response, self.feature_1b05.get_set_enabled_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Disable all toggle hotkeys by getSetEnabled request with set_toggle_keys_enabled=1 "
                                 "and toggle_keys_enabled=0")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.PowerOnFKCRequest.SET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET,
            toggle_keys_enabled=0x0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check all toggle hotkeys are disabled from getSetEnabled response with "
                                  "toggle_keys_enabled=0")
        # --------------------------------------------------------------------------------------------------------------
        toggle_keys_state_check_map['toggle_key_7_enabled'] = (toggle_keys_checker.check_toggle_key_7_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.DISABLE)
        toggle_keys_state_check_map['toggle_key_6_enabled'] = (toggle_keys_checker.check_toggle_key_6_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.DISABLE)
        toggle_keys_state_check_map['toggle_key_5_enabled'] = (toggle_keys_checker.check_toggle_key_5_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.DISABLE)
        toggle_keys_state_check_map['toggle_key_4_enabled'] = (toggle_keys_checker.check_toggle_key_4_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.DISABLE)
        toggle_keys_state_check_map['toggle_key_3_enabled'] = (toggle_keys_checker.check_toggle_key_3_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.DISABLE)
        toggle_keys_state_check_map['toggle_key_2_enabled'] = (toggle_keys_checker.check_toggle_key_2_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.DISABLE)
        toggle_keys_state_check_map['toggle_key_1_enabled'] = (toggle_keys_checker.check_toggle_key_1_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.DISABLE)
        toggle_keys_state_check_map['toggle_key_0_enabled'] = (toggle_keys_checker.check_toggle_key_0_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.DISABLE)

        check_map['toggle_keys_state'] = (checker.check_toggle_keys_state, toggle_keys_state_check_map)
        checker.check_fields(self, response, self.feature_1b05.get_set_enabled_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power cycle DUT")
        # --------------------------------------------------------------------------------------------------------------
        if self.is_hardware_reset_possible():
            self.reset(hardware_reset=True, verify_connection_reset=False,
                       verify_wireless_device_status_broadcast_event=False)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get all toggle hotkeys status by getSetEnabled request with "
                                 "set_toggle_keys_enabled=0")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.GET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check all toggle hotkeys are disabled from getSetEnabled response with"
                                  "toggle_keys_enabled=0xFF")
        # --------------------------------------------------------------------------------------------------------------
        checker.check_fields(self, response, self.feature_1b05.get_set_enabled_response_cls, check_map)

        self.testCaseChecked("BUS_1B05_0006", _AUTHOR)
    # end def test_toggle_keys_status_after_power_cycle

    @features('Keyboard')
    @features("Feature1B05")
    @features('Feature1830powerMode', 3)
    @level("Business")
    def test_toggle_keys_status_after_deep_sleep(self):
        """
        As a user, I expect that my choice of FKC toggle hotkeys will remain the same after deep-sleep
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable all toggle hotkeys by getSetEnabled request with set_toggle_keys_enabled=1"
                                 "and toggle_keys_enabled=0xFF")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.SET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET,
            toggle_keys_enabled=0xFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check all toggle hotkeys are enabled from getSetEnabled response with "
                                  "toggle_keys_enabled=0xFF")
        # --------------------------------------------------------------------------------------------------------------
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

        checker = FullKeyCustomizationTestUtils.GetSetEnabledResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map['toggle_keys_state'] = (checker.check_toggle_keys_state, toggle_keys_state_check_map)
        checker.check_fields(self, response, self.feature_1b05.get_set_enabled_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set DUT into deep sleep mode by 0x1830.SetPowerMode request with PowerModeNumber=3")
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on "return_enter" to wake up DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get all toggle hotkeys status by getSetEnabled request with "
                                 "set_toggle_keys_enabled=0")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.PowerOnFKCRequest.GET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check all toggle hotkeys are enabled from getSetEnabled response with "
                                  "toggle_keys_enabled=0xFF")
        # --------------------------------------------------------------------------------------------------------------
        check_map['toggle_keys_state'] = (checker.check_toggle_keys_state, toggle_keys_state_check_map)
        checker.check_fields(self, response, self.feature_1b05.get_set_enabled_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Disable all toggle hotkeys by getSetEnabled request with set_toggle_keys_enabled=1 "
                                 "and toggle_keys_enabled=0")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.PowerOnFKCRequest.SET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET,
            toggle_keys_enabled=0x0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check all toggle hotkeys are disabled from getSetEnabled response with "
                                  "toggle_keys_enabled=0")
        # --------------------------------------------------------------------------------------------------------------
        toggle_keys_state_check_map['toggle_key_7_enabled'] = (toggle_keys_checker.check_toggle_key_7_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.DISABLE)
        toggle_keys_state_check_map['toggle_key_6_enabled'] = (toggle_keys_checker.check_toggle_key_6_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.DISABLE)
        toggle_keys_state_check_map['toggle_key_5_enabled'] = (toggle_keys_checker.check_toggle_key_5_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.DISABLE)
        toggle_keys_state_check_map['toggle_key_4_enabled'] = (toggle_keys_checker.check_toggle_key_4_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.DISABLE)
        toggle_keys_state_check_map['toggle_key_3_enabled'] = (toggle_keys_checker.check_toggle_key_3_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.DISABLE)
        toggle_keys_state_check_map['toggle_key_2_enabled'] = (toggle_keys_checker.check_toggle_key_2_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.DISABLE)
        toggle_keys_state_check_map['toggle_key_1_enabled'] = (toggle_keys_checker.check_toggle_key_1_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.DISABLE)
        toggle_keys_state_check_map['toggle_key_0_enabled'] = (toggle_keys_checker.check_toggle_key_0_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.DISABLE)

        check_map['toggle_keys_state'] = (checker.check_toggle_keys_state, toggle_keys_state_check_map)
        checker.check_fields(self, response, self.feature_1b05.get_set_enabled_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set DUT into deep sleep mode by 0x1830.SetPowerMode request with PowerModeNumber=3")
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on "return_enter" to wake up DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get all toggle hotkeys status by getSetEnabled request with "
                                 "set_toggle_keys_enabled=0")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.GET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check all toggle hotkeys are disabled from getSetEnabled response with"
                                  "toggle_keys_enabled=0xFF")
        # --------------------------------------------------------------------------------------------------------------
        checker.check_fields(self, response, self.feature_1b05.get_set_enabled_response_cls, check_map)

        self.testCaseChecked("BUS_1B05_0007", _AUTHOR)
    # end def test_toggle_keys_status_after_deep_sleep

    @features('Keyboard')
    @features("Feature1B05")
    @level("Business")
    @services('KeyMatrix')
    def test_forced_release_macros_when_fkc_changing(self):
        """
        Test enabling, disabling or changing the FKC configuration will trigger a forced release of all macros
        """
        preset_macro_entries = [PresetMacroEntry(
            commands=[StandardKeyCommand(key_id=RemappedKey.RandomKey.NON_MODIFIER_KEY),
                      WaitForXmsCommand(ms=500),
                      StandardKeyCommand(key_id=RemappedKey.RandomKey.NON_MODIFIER_KEY),
                      WaitForXmsCommand(ms=500),
                      StandardKeyCommand(key_id=RemappedKey.RandomKey.NON_MODIFIER_KEY),
                      WaitForXmsCommand(ms=500),
                      StandardKeyCommand(key_id=RemappedKey.RandomKey.NON_MODIFIER_KEY),
                      WaitForXmsCommand(ms=500),
                      StandardKeyCommand(key_id=RemappedKey.RandomKey.NON_MODIFIER_KEY),
                      WaitForXmsCommand(ms=500),
                      StandardKeyCommand(key_id=RemappedKey.RandomKey.NON_MODIFIER_KEY),
                      WaitForXmsCommand(ms=500),
                      RepeatWhilePressedCommand()])]

        preset_remapped_keys = [
            RemappedKey(action_type=RemappedKey.ActionType.MACRO,
                        trigger_key=RemappedKey.RandomKey.NON_MODIFIER_KEY,
                        macro_entry_index=0)
        ]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create a FKC profile and remapping in NVS buffer and enable FKC\n"
                                         "Trigger1 -> Macro(repeat: key1, delay=500ms, key2, delay=500ms, key3, "
                                         "delay=500ms, key4, delay=500ms, key5, delay=500ms, key6, delay=500ms)")
        # --------------------------------------------------------------------------------------------------------------
        remapped_keys = self.create_remapping_in_nvs(preset_macro_entries=preset_macro_entries,
                                                     preset_remapped_keys=preset_remapped_keys)
        remapped_key = remapped_keys[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Clean all queues")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Emulate a keypress on the trigger key: {remapped_key.trigger_key!s} to start the "
                                 "macro")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=remapped_key.trigger_key)

        macro_exec_twice_timeout = ((len(remapped_key.macro_commands) * 500 / 1000) + 1)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Sleep for {macro_exec_twice_timeout} secs to wait the macro execution twice")
        # --------------------------------------------------------------------------------------------------------------
        sleep(macro_exec_twice_timeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check DUT sends HID report of the macro: {remapped_key.macro_commands!s} "
                                  f"repeatedly at least twice")
        # --------------------------------------------------------------------------------------------------------------
        for i in range(2):
            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Check {'1st' if i == 0 else '2nd'} macro report")
            # --------------------------------------------------------------------------------------------------------------
            FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(test_case=self, remapped_key=remapped_key)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Disable FKC by getSetEnabled request with set_fkc_enabled=1 and fkc_enabled=0")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.GET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.SET,
            fkc_enabled=FullKeyCustomization.FKCStatus.DISABLE,
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check FKC is disabled from getSetEnabled response with fkc_enabled=0")
        # --------------------------------------------------------------------------------------------------------------
        fkc_state_checker = FullKeyCustomizationTestUtils.FkcStateChecker
        fkc_state_check_map = fkc_state_checker.get_default_check_map(self)
        fkc_state_check_map['fkc_enabled'] = (fkc_state_checker.check_fkc_enabled,
                                              FullKeyCustomization.FKCStatus.DISABLE)

        checker = FullKeyCustomizationTestUtils.GetSetEnabledResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map['fkc_state'] = (checker.check_fkc_state, fkc_state_check_map)
        checker.check_fields(self, response, self.feature_1b05.get_set_enabled_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Empty HID queue")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Wait for {BaseCommunicationChannel.GENERIC_GET_TIMEOUT} secs")
        # --------------------------------------------------------------------------------------------------------------
        sleep(BaseCommunicationChannel.GENERIC_GET_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Check HID queue is still empty after release the {remapped_key.trigger_key!s} key")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=remapped_key.trigger_key)
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)

        self.testCaseChecked("BUS_1B05_0008", _AUTHOR)
    # end def test_forced_release_macros_when_fkc_changing

    @features('Keyboard')
    @features("Feature1B05")
    @level("Business")
    @services('KeyMatrix')
    def test_fkc_enable_disable_without_profiles(self):
        """
        Validate FKC could be enabled/disabled when there are no any FKC profiles present in the DUT NVS
        """
        self.perform_fkc_toggle_hotkeys(fkc_status=FullKeyCustomization.FKCStatus.ENABLE)
        self.perform_fkc_toggle_hotkeys(fkc_status=FullKeyCustomization.FKCStatus.DISABLE)
        self.testCaseChecked("BUS_1B05_0009", _AUTHOR)
    # end def test_fkc_enable_disable_without_profiles
    @features("Feature1B05V1+")
    @level("Business")
    def test_initial_sw_configuration_cookie(self):
        """
        SW will enable FKC by default on first initialization
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create a FKC profile and remapping in RAM buffer")
        # --------------------------------------------------------------------------------------------------------------
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        self.create_remapping_in_nvs(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(full_keys=True)), enable_fkc=FullKeyCustomization.FKCStatus.DISABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get SWConfigurationCookie by getSetSWConfigurationCookie request with "
                                 "set_sw_configuration_cookie=0")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_sw_configuration_cookie(
            test_case=self,
            set_sw_configuration_cookie=FullKeyCustomization.SWConfigurationCookieRequest.GET,
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check sw_configuration_cookie from getSetSWConfigurationCookie response with "
                                  "sw_configuration_cookie=0")
        # --------------------------------------------------------------------------------------------------------------
        sw_cfg_cookie_checker = FullKeyCustomizationTestUtils.GetSetSWConfigurationCookieResponseChecker
        sw_cfg_cookie_check_map = sw_cfg_cookie_checker.get_default_check_map(self)
        sw_cfg_cookie_checker.check_fields(self, response,
                                           self.feature_1b05.get_set_sw_configuration_cookie_response_cls,
                                           sw_cfg_cookie_check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable power-on FKC by getSetPowerOnParams request with set_poweron_fkc_enable=1 "
                                 "and poweron_fkc_enable=1")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_power_on_params(
            test_case=self,
            set_power_on_fkc_enable=FullKeyCustomization.PowerOnFKCRequest.SET,
            power_on_fkc_enable=FullKeyCustomization.PowerOnFKCStatus.ENABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check power-on FKC status is enabled from getSetPowerOnParams response with "
                                  "poweron_fkc_enable=1")
        # --------------------------------------------------------------------------------------------------------------
        power_on_fkc_state_checker = FullKeyCustomizationTestUtils.PowerOnFkcStateChecker
        power_on_fkc_state_map = power_on_fkc_state_checker.get_default_check_map(self)
        power_on_fkc_state_map['power_on_fkc_enable'] = (power_on_fkc_state_checker.check_power_on_fkc_enable,
                                                         FullKeyCustomization.PowerOnFKCStatus.ENABLE)

        power_on_params_checker = FullKeyCustomizationTestUtils.GetSetPowerOnParamsResponseChecker
        power_on_params_check_map = power_on_params_checker.get_default_check_map(self)
        power_on_params_check_map['power_on_fkc_state'] = (power_on_params_checker.check_power_on_fkc_state,
                                                           power_on_fkc_state_map)
        power_on_params_checker.check_fields(self, response, self.feature_1b05.get_set_power_on_params_response_cls,
                                             power_on_params_check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set SWConfigurationCookie by getSetSWConfigurationCookie request with "
                                 "set_sw_configuration_cookie=1 and sw_configuration_cookie=0x1")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_sw_configuration_cookie(
            test_case=self,
            set_sw_configuration_cookie=FullKeyCustomization.SWConfigurationCookieRequest.SET,
            sw_configuration_cookie=0x1,
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check sw_configuration_cookie from getSetSWConfigurationCookie response with "
                                  "sw_configuration_cookie=0x1")
        # --------------------------------------------------------------------------------------------------------------
        sw_cfg_cookie_check_map['sw_configuration_cookie'] = (sw_cfg_cookie_checker.check_sw_configuration_cookie, 0x1)
        sw_cfg_cookie_checker.check_fields(self, response,
                                           self.feature_1b05.get_set_sw_configuration_cookie_response_cls,
                                           sw_cfg_cookie_check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power cycle DUT")
        # --------------------------------------------------------------------------------------------------------------
        if self.is_hardware_reset_possible():
            self.reset(hardware_reset=True, verify_connection_reset=False,
                       verify_wireless_device_status_broadcast_event=False)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get SWConfigurationCookie by getSetSWConfigurationCookie request with "
                                 "set_sw_configuration_cookie=0")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_sw_configuration_cookie(
            test_case=self,
            set_sw_configuration_cookie=FullKeyCustomization.SWConfigurationCookieRequest.GET,
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check sw_configuration_cookie from getSetSWConfigurationCookie response with "
                                  "sw_configuration_cookie=0x1")
        # --------------------------------------------------------------------------------------------------------------
        sw_cfg_cookie_checker.check_fields(self, response,
                                           self.feature_1b05.get_set_sw_configuration_cookie_response_cls,
                                           sw_cfg_cookie_check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get FKC status by getSetEnabled request with set_fkc_enabled=0")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.GET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET,
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check FKC status is enabled from getSetEnabled response with fkc_enabled=1")
        # --------------------------------------------------------------------------------------------------------------
        fkc_state_checker = FullKeyCustomizationTestUtils.FkcStateChecker
        fkc_state_check_map = fkc_state_checker.get_default_check_map(self)
        fkc_state_check_map['fkc_enabled'] = (fkc_state_checker.check_fkc_enabled,
                                              FullKeyCustomization.FKCStatus.ENABLE)

        get_set_enabled_checker = FullKeyCustomizationTestUtils.GetSetEnabledResponseChecker
        get_set_enabled_check_map = get_set_enabled_checker.get_default_check_map(self)
        get_set_enabled_check_map['fkc_state'] = (get_set_enabled_checker.check_fkc_state, fkc_state_check_map)
        get_set_enabled_checker.check_fields(self, response, self.feature_1b05.get_set_enabled_response_cls,
                                             get_set_enabled_check_map)

        self.testCaseChecked("BUS_1B05_0010", _AUTHOR)
    # end def test_initial_sw_configuration_cookie
# end class FullKeyCustomizationBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
