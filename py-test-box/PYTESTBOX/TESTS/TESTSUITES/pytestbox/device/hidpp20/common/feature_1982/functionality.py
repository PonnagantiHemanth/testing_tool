#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1982.functionality
:brief: HID++ 2.0 ``Backlight`` functionality test suite
:author: Anil Gadad <agadad@logitech.com>
:date: 2021/09/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep
from time import perf_counter
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.backlight import Backlight
from pyhid.hidpp.features.common.configurableproperties import ConfigurableProperties
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.features.keyboard.keyboardinternationallayouts import KeyboardInternationalLayouts
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.emulatorinterfaces import HOST
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.emulator.ledid import LED_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pyraspi.services.keyboardemulator import KeyboardMixin
from pyraspi.services.kosmos.config.backlightconfiguration import GET_BACKLIGHT_CONFIGURATION_BY_ID
from pyraspi.services.kosmos.i2c.i2cbacklightparser import BacklightEffectType
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.backlightutils import BacklightTestUtils as Utils
from pytestbox.device.base.connectionschemeutils import BleProConnectionSchemeTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.layoututils import LayoutTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.base.unifiedbatteryutils import UnifiedBatteryTestUtils
from pytestbox.device.hidpp20.common.feature_1982.backlight import BacklightTestCase
from pytestbox.shared.base.bleprosafeprepairedreceiverutils import BleProSafePrePairedReceiverTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pyusb.libusbdriver import ChannelIdentifier

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Anil Gadad"
_CHECK_CURRENT_LEVEL_0_BACKLIGHT_STATUS_4 = "Check the currentLevel = 0 and backlightStatus = 4"
_CHECK_CURRENT_LEVEL_7_BACKLIGHT_STATUS_4 = "Check the currentLevel = 7 and backlightStatus = 4"
_CLEAR_BACKLIGHT_INFO_EVENT = "Clearing any existing Event messages of BacklightInfoEvent type"
_DEVICE_RESET = "Power reset device"
_DISABLE_WOW_EFFECT = "Disable WOW effect to read correct currentLevel value"
_GET_BACKLIGHT_CONFIG_REQUEST = "Send GetBacklightConfig request"
_GET_BACKLIGHT_INFO_REQUEST = "Send GetBacklightInfo request"
_PRESS_BACKLIGHT_DOWN_BUTTON = "Press backlight - button"
_SET_BACKLIGHT_CONFIG_REQUEST = "Send SetBacklightConfig request"
_UPPER_MARGIN_LUMINANCE_VALUE = 1.25  # margin of 30 % because als is not calibrated
_REACTION_FADE_OUT_DURATION_MARGIN = 0.1  # in second


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BacklightFunctionalityTestCase(BacklightTestCase):
    """
    Validate ``Backlight`` functionality test cases
    """

    @features("Feature1982")
    @features("Feature1982RequiredOptions", Backlight.SupportedOptionsMask.WOW_S)
    @level("Functionality")
    def test_possible_wow_settings(self):
        """
        Validate the possible wow settings
        """
        self.post_requisite_reload_nvs = True
        default_options = Utils.get_default_options(self)
        supported_options = Numeral(self.config.F_SupportedOptions)

        for wow_state in Backlight.Wow:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _SET_BACKLIGHT_CONFIG_REQUEST)
            # ----------------------------------------------------------------------------------------------------------
            options = default_options | Backlight.Options.WOW \
                if wow_state == Backlight.Wow.ENABLE else default_options & ~Backlight.Options.WOW

            Utils.HIDppHelper.set_backlight_config(self, configuration=Backlight.Configuration.ENABLE, options=options)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _GET_BACKLIGHT_CONFIG_REQUEST)
            # ----------------------------------------------------------------------------------------------------------
            get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check wow setting in supported_options field in GetBacklightConfig response")
            # ----------------------------------------------------------------------------------------------------------
            supported_options = supported_options | Backlight.SupportedOptionsMask.WOW \
                if wow_state == Backlight.Wow.ENABLE else supported_options & ~Backlight.SupportedOptionsMask.WOW

            Utils.GetBacklightConfigResponseChecker.check_supported_options(self, get_backlight_config_resp,
                                                                            supported_options)
        # end for

        self.testCaseChecked("FUN_1982_0001", _AUTHOR)
    # end def test_possible_wow_settings

    @features("Feature1982")
    @features("Feature1982RequiredOptions", Backlight.SupportedOptionsMask.CROWN_S)
    @level("Functionality")
    def test_possible_crown_settings(self):
        """
        Validate the possible crown settings
        """
        self.post_requisite_reload_nvs = True
        default_options = Utils.get_default_options(self)
        supported_options = Numeral(self.config.F_SupportedOptions)

        for crown_state in Backlight.Crown:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _SET_BACKLIGHT_CONFIG_REQUEST)
            # ----------------------------------------------------------------------------------------------------------
            options = default_options | Backlight.Options.CROWN \
                if crown_state == Backlight.Crown.ENABLE else default_options & ~Backlight.Options.CROWN

            Utils.HIDppHelper.set_backlight_config(self, configuration=Backlight.Configuration.ENABLE, options=options)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _GET_BACKLIGHT_CONFIG_REQUEST)
            # ----------------------------------------------------------------------------------------------------------
            get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check crown setting in supported_options field in GetBacklightConfig response")
            # ----------------------------------------------------------------------------------------------------------
            supported_options = supported_options | Backlight.SupportedOptionsMask.CROWN\
                if crown_state == Backlight.Crown.ENABLE else supported_options & ~Backlight.SupportedOptionsMask.CROWN

            Utils.GetBacklightConfigResponseChecker.check_supported_options(self, get_backlight_config_resp,
                                                                            supported_options)
        # end for

        self.testCaseChecked("FUN_1982_0002", _AUTHOR)
    # end def test_possible_crown_settings

    @features("Feature1982")
    @features("Feature1982RequiredOptions", Backlight.SupportedOptionsMask.PWR_SAVE_S)
    @level("Functionality")
    def test_possible_pwr_save_settings(self):
        """
        Validate the possible pwrSave settings
        """
        self.post_requisite_reload_nvs = True
        default_options = Utils.get_default_options(self)
        supported_options = Numeral(self.config.F_SupportedOptions)

        for power_save_state in Backlight.PwrSave:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _SET_BACKLIGHT_CONFIG_REQUEST)
            # ----------------------------------------------------------------------------------------------------------
            options = default_options | Backlight.Options.PWR_SAVE \
                if power_save_state == Backlight.PwrSave.ENABLE else default_options & ~Backlight.Options.PWR_SAVE

            Utils.HIDppHelper.set_backlight_config(self, configuration=Backlight.Configuration.ENABLE, options=options)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _GET_BACKLIGHT_CONFIG_REQUEST)
            # ----------------------------------------------------------------------------------------------------------
            get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check pwrSave setting in supported_options field in GetBacklightConfig response")
            # ----------------------------------------------------------------------------------------------------------
            supported_options = supported_options | Backlight.SupportedOptionsMask.PWR_SAVE \
                if power_save_state == Backlight.PwrSave.ENABLE \
                else supported_options & ~Backlight.SupportedOptionsMask.PWR_SAVE

            Utils.GetBacklightConfigResponseChecker.check_supported_options(self, get_backlight_config_resp,
                                                                            supported_options)
        # end for

        self.testCaseChecked("FUN_1982_0003", _AUTHOR)
    # end def test_possible_pwr_save_settings

    @features("Feature1982")
    @features("Feature1982RequiredOptions", Backlight.SupportedOptionsMask.PWR_SAVE_S)
    @level("Functionality")
    @services('PowerSupply')
    def test_disable_whole_backlight_system_at_critical_level(self):
        """
        Automatic Mode: Action-19
        [Since v1] Validate enabled pwrSave causes to disable the whole backlight system while battery at
        critical level.
        """
        self.post_requisite_reload_nvs = True
        default_options = Utils.get_default_options(self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_BACKLIGHT_CONFIG_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(
            self, configuration=Backlight.Configuration.ENABLE, options=default_options | Backlight.Options.PWR_SAVE)

        critical_voltage = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(
            self, UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, "critical"))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Set voltage to critical level {critical_voltage}")
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(critical_voltage)

        # Add delay to wait for previous commands to process and prevent them from generating events after clearing
        # queue
        sleep(10)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check backlightStatus field in GetBacklightInfo response")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(
            self, get_backlight_info_resp, Backlight.BacklightStatus.DISABLED_BY_CRITICAL_BATTERY)

        self.testCaseChecked("FUN_1982_0004", _AUTHOR)
    # end def test_disable_whole_backlight_system_at_critical_level

    @features("Feature1982v2+")
    @level("Functionality")
    @services("HardwareReset")
    def test_backlight_effect_setting_kept_after_power_reset_device(self):
        """
        [Automatic mode] Backlight Settings, Action-15
        [Since v2] Validate the backlight effect setting will be kept by setBacklightConfig after power reset device.
        """
        self.post_requisite_reload_nvs = True
        inverted_default_capability = Utils.get_inverted_default_capability(self)
        non_default_effect = Utils.get_non_default_backlight_effect(self)
        self.assertNotEqual(unexpected=None, obtained=non_default_effect,
                            msg='Cannot find the non-default backlight effect!')
        backlight_level = Backlight.CurrentLevel.CURRENT_LEVEL_7
        hands_out_duration = self.config.F_OobDurationHandsOut + 1
        hands_in_duration = self.config.F_OobDurationHandsIn + 1
        powered_duration = self.config.F_OobDurationPowered + 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Backlight.setBacklightConfig with bcklEn = 1, bcklMode = Automatic mode and "
                                 "other parameters with non-default setting")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=inverted_default_capability,
                                               backlight_effect=non_default_effect,
                                               current_backlight_level=backlight_level,
                                               curr_duration_hands_out=hands_out_duration,
                                               curr_duration_hands_in=hands_in_duration,
                                               curr_duration_powered=powered_duration)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power reset DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wait power LED timeout")
        # --------------------------------------------------------------------------------------------------------------
        sleep(Utils.POWER_LED_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_CONFIG_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check wow, crown, pwrSave and durations equals to non-default setting")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightConfigResponseChecker.check_supported_options(
            self, get_backlight_config_resp,
            (Numeral(self.config.F_SupportedOptions) & 0x00FF) | (inverted_default_capability << 8))
        Utils.GetBacklightConfigResponseChecker.check_curr_duration_hands_out(self, get_backlight_config_resp,
                                                                              hands_out_duration)
        Utils.GetBacklightConfigResponseChecker.check_curr_duration_hands_in(self, get_backlight_config_resp,
                                                                             hands_in_duration)
        Utils.GetBacklightConfigResponseChecker.check_curr_duration_powered(self, get_backlight_config_resp,
                                                                            powered_duration)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the currentBacklightLevel = default level")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightConfigResponseChecker.check_current_backlight_level_by_range(
            self, get_backlight_config_resp,
            [Backlight.CurrentLevel.CURRENT_LEVEL_2, Backlight.CurrentLevel.CURRENT_LEVEL_4])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check backlightStatus = Automatic mode (2), backlightEffect = {non_default_effect}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.ALS_AUTOMATIC_MODE)
        Utils.GetBacklightInfoResponseChecker.check_backlight_effect(self, get_backlight_info_resp, non_default_effect)

        self.testCaseChecked("FUN_1982_0005#1", _AUTHOR)
    # end def test_backlight_effect_setting_kept_after_power_reset_device

    @features("Feature1982v2+")
    @features("Feature1830")
    @level("Functionality")
    def test_backlight_effect_setting_kept_after_woke_up_device(self):
        """
        [Automatic mode] Backlight Settings, Action-3
        [Since v2] Validate the backlight effect setting will be kept by setBacklightConfig after woke up
        from deep sleep mode.
        """
        self.post_requisite_reload_nvs = True
        inverted_default_capability = Utils.get_inverted_default_capability(self)
        non_default_effect = Utils.get_non_default_backlight_effect(self)
        self.assertNotEqual(unexpected=None, obtained=non_default_effect,
                            msg='Cannot find the non-default backlight effect!')
        backlight_level = Backlight.CurrentLevel.CURRENT_LEVEL_7
        hands_out_duration = self.config.F_OobDurationHandsOut + 1
        hands_in_duration = self.config.F_OobDurationHandsIn + 1
        powered_duration = self.config.F_OobDurationPowered + 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Backlight.setBacklightConfig with bcklEn = 1, bcklMode = Automatic mode and "
                                 "other parameters with non-default setting")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=inverted_default_capability,
                                               backlight_effect=non_default_effect,
                                               current_backlight_level=backlight_level,
                                               curr_duration_hands_out=hands_out_duration,
                                               curr_duration_hands_in=hands_in_duration,
                                               curr_duration_powered=powered_duration)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "0x1830.setPowerMode = Deep sleep mode")
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "User action")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wait power LED timeout")
        # --------------------------------------------------------------------------------------------------------------
        sleep(Utils.POWER_LED_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_CONFIG_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check wow, crown, pwrSave and durations equals to non-default setting")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightConfigResponseChecker.check_supported_options(
            self, get_backlight_config_resp,
            (Numeral(self.config.F_SupportedOptions) & 0x00FF) | (inverted_default_capability << 8))
        Utils.GetBacklightConfigResponseChecker.check_curr_duration_hands_out(self, get_backlight_config_resp,
                                                                              hands_out_duration)
        Utils.GetBacklightConfigResponseChecker.check_curr_duration_hands_in(self, get_backlight_config_resp,
                                                                             hands_in_duration)
        Utils.GetBacklightConfigResponseChecker.check_curr_duration_powered(self, get_backlight_config_resp,
                                                                            powered_duration)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the currentBacklightLevel = default level")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightConfigResponseChecker.check_current_backlight_level_by_range(
            self, get_backlight_config_resp,
            [Backlight.CurrentLevel.CURRENT_LEVEL_2, Backlight.CurrentLevel.CURRENT_LEVEL_4])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check backlightStatus = Automatic mode (2), backlightEffect = {non_default_effect}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.ALS_AUTOMATIC_MODE)
        Utils.GetBacklightInfoResponseChecker.check_backlight_effect(self, get_backlight_info_resp, non_default_effect)

        self.testCaseChecked("FUN_1982_0005#2", _AUTHOR)
    # end def test_backlight_effect_setting_kept_after_woke_up_device

    @features("Feature1982v2+")
    @features("MultipleChannels", 2)
    @features('MultipleEasySwitchButtons')
    @level("Functionality")
    def test_backlight_effect_setting_kept_after_changed_host(self):
        """
        [Automatic mode] Backlight Settings, Action-16
        [Since v2] Validate the backlight effect setting will be kept by setBacklightConfig after changing hosts.
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True
        inverted_default_capability = Utils.get_inverted_default_capability(self)
        non_default_effect = Utils.get_non_default_backlight_effect(self)
        self.assertNotEqual(unexpected=None, obtained=non_default_effect,
                            msg='Cannot find the non-default backlight effect!')
        backlight_level = Backlight.CurrentLevel.CURRENT_LEVEL_7
        hands_out_duration = self.config.F_OobDurationHandsOut + 1
        hands_in_duration = self.config.F_OobDurationHandsIn + 1
        powered_duration = self.config.F_OobDurationPowered + 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair host 2 to receiver slot 2")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.pair_all_available_hosts(self, number_of_host=2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Change to host 1 by press host 1 button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH1)
        DeviceManagerUtils.switch_channel(
            test_case=self,
            new_channel_id=ChannelIdentifier(port_index=1, device_index=HOST.CH1), allow_no_message=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Backlight.setBacklightConfig with bcklEn = 1, bcklMode = Automatic mode and "
                                 "other parameters with non-default setting")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=inverted_default_capability,
                                               backlight_effect=non_default_effect,
                                               current_backlight_level=backlight_level,
                                               curr_duration_hands_out=hands_out_duration,
                                               curr_duration_hands_in=hands_in_duration,
                                               curr_duration_powered=powered_duration)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Change to host 2 by press host 2 button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Change to host 1 by press host 1 button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_CONFIG_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check wow, crown, pwrSave and durations equals to non-default setting")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightConfigResponseChecker.check_supported_options(
            self, get_backlight_config_resp,
            (Numeral(self.config.F_SupportedOptions) & 0x00FF) | (inverted_default_capability << 8))
        Utils.GetBacklightConfigResponseChecker.check_curr_duration_hands_out(self, get_backlight_config_resp,
                                                                              hands_out_duration)
        Utils.GetBacklightConfigResponseChecker.check_curr_duration_hands_in(self, get_backlight_config_resp,
                                                                             hands_in_duration)
        Utils.GetBacklightConfigResponseChecker.check_curr_duration_powered(self, get_backlight_config_resp,
                                                                            powered_duration)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the currentBacklightLevel = default level")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightConfigResponseChecker.check_current_backlight_level_by_range(
            self, get_backlight_config_resp,
            [Backlight.CurrentLevel.CURRENT_LEVEL_2, Backlight.CurrentLevel.CURRENT_LEVEL_4])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check backlightStatus = Automatic mode (2), backlightEffect = {non_default_effect}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.ALS_AUTOMATIC_MODE)
        Utils.GetBacklightInfoResponseChecker.check_backlight_effect(self, get_backlight_info_resp, non_default_effect)

        self.testCaseChecked("FUN_1982_0005#3", _AUTHOR)
    # end def test_backlight_effect_setting_kept_after_changed_host

    @features("Feature1982v2+")
    @features("MultipleChannels", 2)
    @features('MultipleEasySwitchButtons')
    @level("Functionality")
    @services('EmulatedKeys', (KEY_ID.BACKLIGHT_UP,))
    def test_backlight_effect_setting_kept_after_changed_host_in_temporary_manual_mode(self):
        """
        [Temporary manual mode] Backlight Settings, Action-16
        [Since v2] Validate the backlight effect setting will be kept by setBacklightConfig after changing hosts.
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True
        inverted_default_capability = Utils.get_inverted_default_capability(self)
        non_default_effect = Utils.get_non_default_backlight_effect(self)
        self.assertNotEqual(unexpected=None, obtained=non_default_effect,
                            msg='Cannot find the non-default backlight effect!')
        backlight_level = Backlight.CurrentLevel.CURRENT_LEVEL_7
        hands_out_duration = self.config.F_OobDurationHandsOut + 1
        hands_in_duration = self.config.F_OobDurationHandsIn + 1
        powered_duration = self.config.F_OobDurationPowered + 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair host 2 to receiver slot 2")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.pair_all_available_hosts(self, number_of_host=2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Change to host 1 by press host 1 button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH1)
        DeviceManagerUtils.switch_channel(
            test_case=self,
            new_channel_id=ChannelIdentifier(port_index=1, device_index=HOST.CH1), allow_no_message=True)
        self.cleanup_battery_event_from_queue()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Backlight.setBacklightConfig with bcklEn = 1, bcklMode = Automatic mode and "
                                 "other parameters with non-default setting")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=inverted_default_capability,
                                               backlight_effect=non_default_effect,
                                               current_backlight_level=backlight_level,
                                               curr_duration_hands_out=hands_out_duration,
                                               curr_duration_hands_in=hands_in_duration,
                                               curr_duration_powered=powered_duration)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Short press Brightness down button")
        # --------------------------------------------------------------------------------------------------------------
        # Wait device sends backlight info notification
        sleep(2)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.EVENT,
                                    class_type=self.feature_1982.backlight_info_event_cls)
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_DOWN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait BacklightInfoEvent then check the backlightStatus = Temporary manual mode (4)")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.EVENT,
                                    class_type=WirelessDeviceStatusBroadcastEvent)
        backlight_info_event = Utils.HIDppHelper.backlight_info_event(self)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, backlight_info_event,
                                                                     Backlight.BacklightStatus.MANUAL_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Change to host 2 by press host 2 button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Change to host 1 by press host 1 button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_CONFIG_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check wow, crown, pwrSave and durations equals to non-default setting")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightConfigResponseChecker.check_supported_options(
            self, get_backlight_config_resp,
            (Numeral(self.config.F_SupportedOptions) & 0x00FF) | (inverted_default_capability << 8))
        Utils.GetBacklightConfigResponseChecker.check_curr_duration_hands_out(self, get_backlight_config_resp,
                                                                              hands_out_duration)
        Utils.GetBacklightConfigResponseChecker.check_curr_duration_hands_in(self, get_backlight_config_resp,
                                                                             hands_in_duration)
        Utils.GetBacklightConfigResponseChecker.check_curr_duration_powered(self, get_backlight_config_resp,
                                                                            powered_duration)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the currentBacklightLevel = default level")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightConfigResponseChecker.check_current_backlight_level_by_range(
            self, get_backlight_config_resp,
            [Backlight.CurrentLevel.CURRENT_LEVEL_2, Backlight.CurrentLevel.CURRENT_LEVEL_4])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check backlightStatus = Automatic mode (2), backlightEffect = {non_default_effect}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.ALS_AUTOMATIC_MODE)
        Utils.GetBacklightInfoResponseChecker.check_backlight_effect(self, get_backlight_info_resp, non_default_effect)

        self.testCaseChecked("FUN_1982_0005#4", _AUTHOR)
    # end def test_backlight_effect_setting_kept_after_changed_host_in_temporary_manual_mode

    @features("Feature1982v3+")
    @features("Feature1830")
    @level("Functionality")
    def test_backlight_effect_setting_kept_after_woke_up_device_in_permanent_manual_mode(self):
        """
        [Permanent manual mode] Backlight Settings, Action-3
        [Since v3] The device should keep the backlight effect and durations selection resistant to the waking up
        from deep sleep.
        """
        self.post_requisite_reload_nvs = True
        inverted_default_capability = Utils.get_inverted_default_capability(
            self, backlight_mode=Backlight.Options.PERMANENT_MANUAL_MODE)
        non_default_effect = Utils.get_non_default_backlight_effect(self)
        self.assertNotEqual(unexpected=None, obtained=non_default_effect,
                            msg='Cannot find the non-default backlight effect!')
        backlight_level = Backlight.CurrentLevel.CURRENT_LEVEL_7
        hands_out_duration = self.config.F_OobDurationHandsOut + 1
        hands_in_duration = self.config.F_OobDurationHandsIn + 1
        powered_duration = self.config.F_OobDurationPowered + 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Backlight.setBacklightConfig with bcklEn = 1, bcklMode = Permanent manual mode "
                                 "and other parameters with non-default setting")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=inverted_default_capability,
                                               backlight_effect=non_default_effect,
                                               current_backlight_level=backlight_level,
                                               curr_duration_hands_out=hands_out_duration,
                                               curr_duration_hands_in=hands_in_duration,
                                               curr_duration_powered=powered_duration)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "0x1830.setPowerMode = Deep sleep mode")
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "User action")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wait power LED timeout")
        # --------------------------------------------------------------------------------------------------------------
        sleep(Utils.POWER_LED_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_CONFIG_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check wow, crown, pwrSave and durations equals to non-default setting")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightConfigResponseChecker.check_supported_options(
            self, get_backlight_config_resp,
            (Numeral(self.config.F_SupportedOptions) & 0x00FF) | (inverted_default_capability << 8))
        Utils.GetBacklightConfigResponseChecker.check_curr_duration_hands_out(self, get_backlight_config_resp,
                                                                              hands_out_duration)
        Utils.GetBacklightConfigResponseChecker.check_curr_duration_hands_in(self, get_backlight_config_resp,
                                                                             hands_in_duration)
        Utils.GetBacklightConfigResponseChecker.check_curr_duration_powered(self, get_backlight_config_resp,
                                                                            powered_duration)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the currentBacklightLevel = {backlight_level}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightConfigResponseChecker.check_current_backlight_level(self, get_backlight_config_resp,
                                                                              backlight_level)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check backlightStatus = Automatic mode (2), backlightEffect = {non_default_effect}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.PERMANENT_MANUAL_MODE)
        Utils.GetBacklightInfoResponseChecker.check_backlight_effect(self, get_backlight_info_resp, non_default_effect)

        self.testCaseChecked("FUN_1982_0005#5", _AUTHOR)
    # end def test_backlight_effect_setting_kept_after_woke_up_device_in_permanent_manual_mode

    @features("Feature1982v2+")
    @level("Functionality")
    @services('HardwareReset')
    def test_backlight_effect_setting_not_kept_after_power_reset_device(self):
        """
        Validate that backlightEffect setting will not be kept by ``setBacklightEffect`` after power reset device
        """
        self.post_requisite_reload_nvs = True
        non_default_effect = Utils.get_non_default_backlight_effect(self)
        self.assertNotEqual(unexpected=None, obtained=non_default_effect,
                            msg='Cannot find the non-default backlight effect!')
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setBacklightEffect request")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_effect(self, backlight_effect=non_default_effect)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power reset DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)
        sleep(Utils.POWER_LED_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_CONFIG_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check wow, crown, pwrSave in the supported_options field in"
                                  "GetBacklightConfig response")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightConfigResponseChecker.check_supported_options(self, get_backlight_config_resp,
                                                                        self.config.F_SupportedOptions)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check backlightStatus and backlightEffect fields in GetBacklightInfo response")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.ALS_AUTOMATIC_MODE)
        Utils.GetBacklightInfoResponseChecker.check_backlight_effect(self, get_backlight_info_resp,
                                                                     self.config.F_BacklightEffect)

        self.testCaseChecked("FUN_1982_0006", _AUTHOR)
    # end def test_backlight_effect_setting_not_kept_after_power_reset_device

    @features("Feature1982")
    @level("Functionality")
    @services('EmulatedKeys', (KEY_ID.BACKLIGHT_UP, KEY_ID.BACKLIGHT_DOWN,))
    def test_receive_backlight_info_event_if_press_backlight_button(self):
        """
        Validate that ``backlightInfoEvent`` is received after pressing backlight +/- button
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get current backlight level by getBacklightInfo")
        # --------------------------------------------------------------------------------------------------------------
        current_level = Numeral(Utils.HIDppHelper.get_backlight_info(self).current_level)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press backlight up button")
        # --------------------------------------------------------------------------------------------------------------
        # Wait 1 seconds for BacklightInfoEvent
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_UP, delay=1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Wait for backlightInfoEvent with currentLevel = {current_level + 1}, "
                                  f"backlightStatus = {Backlight.BacklightStatus.MANUAL_MODE}")
        # --------------------------------------------------------------------------------------------------------------
        event_response = Utils.HIDppHelper.backlight_info_event(self)
        Utils.BacklightInfoEventResponseChecker.check_current_level(self, event_response, current_level + 1)
        Utils.BacklightInfoEventResponseChecker.check_backlight_status(self, event_response,
                                                                       Backlight.BacklightStatus.MANUAL_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press backlight down button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_DOWN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Wait for backlightInfoEvent with currentLevel = {current_level}, "
                                  f"backlightStatus = {Backlight.BacklightStatus.MANUAL_MODE}")
        # --------------------------------------------------------------------------------------------------------------
        event_response = Utils.HIDppHelper.backlight_info_event(self)
        Utils.BacklightInfoEventResponseChecker.check_current_level(self, event_response, current_level)
        Utils.BacklightInfoEventResponseChecker.check_backlight_status(self, event_response,
                                                                       Backlight.BacklightStatus.MANUAL_MODE)

        self.testCaseChecked("FUN_1982_0007#1", _AUTHOR)
    # end def test_receive_backlight_info_event_if_press_backlight_button

    @features("Feature1982v3+")
    @level("Functionality")
    @services('EmulatedKeys', (KEY_ID.BACKLIGHT_UP, KEY_ID.BACKLIGHT_DOWN,))
    def test_receive_backlight_info_event_in_permanent_manual_mode(self):
        """
        [Since v3] Shall receive backlightInfoEvent if change currentLevel in the Permanent Manual Mode.
        """
        self.post_requisite_reload_nvs = True
        enable_permanent_manual_mode = Utils.get_default_options(self) | Backlight.Options.PERMANENT_MANUAL_MODE
        current_level = Backlight.CurrentLevel.CURRENT_LEVEL_2
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set baclMode = Permanent manual mode by setBacklightConfig")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=enable_permanent_manual_mode,
                                               current_backlight_level=current_level)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check bcklMode = Permanent manual mode (3) by getBacklightConfig")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)
        Utils.GetBacklightConfigResponseChecker.check_supported_options(
            self, get_backlight_config_resp,
            (Numeral(self.config.F_SupportedOptions) & 0x00FF) | (enable_permanent_manual_mode << 8))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press backlight up button")
        # --------------------------------------------------------------------------------------------------------------
        # Wait device sends backlight info notification
        sleep(2)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.EVENT,
                                    class_type=self.feature_1982.backlight_info_event_cls)
        # Wait 1 seconds for BacklightInfoEvent
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_UP, delay=1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Wait for backlightInfoEvent with currentLevel = {current_level + 1}, "
                                  f"backlightStatus = {Backlight.BacklightStatus.PERMANENT_MANUAL_MODE}")
        # --------------------------------------------------------------------------------------------------------------
        event_response = Utils.HIDppHelper.backlight_info_event(self)
        Utils.BacklightInfoEventResponseChecker.check_current_level(self, event_response, current_level + 1)
        Utils.BacklightInfoEventResponseChecker.check_backlight_status(self, event_response,
                                                                       Backlight.BacklightStatus.PERMANENT_MANUAL_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press backlight down button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_DOWN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Wait for backlightInfoEvent with currentLevel = {current_level}, "
                                  f"backlightStatus = {Backlight.BacklightStatus.PERMANENT_MANUAL_MODE}")
        # --------------------------------------------------------------------------------------------------------------
        event_response = Utils.HIDppHelper.backlight_info_event(self)
        Utils.BacklightInfoEventResponseChecker.check_current_level(self, event_response, current_level)
        Utils.BacklightInfoEventResponseChecker.check_backlight_status(self, event_response,
                                                                       Backlight.BacklightStatus.PERMANENT_MANUAL_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Change the currentBacklightLevel = {default + 2} by setBacklightConfig")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=enable_permanent_manual_mode,
                                               current_backlight_level=current_level + 2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check currentLevel = {current_level + 2}, "
                                  f"backlightStatus = Permanent manual mode(5) by getBacklightInfo")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)
        Utils.BacklightInfoEventResponseChecker.check_current_level(self, get_backlight_info_resp, current_level + 2)
        Utils.BacklightInfoEventResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                       Backlight.BacklightStatus.PERMANENT_MANUAL_MODE)

        self.testCaseChecked("FUN_1982_0007#2", _AUTHOR)
    # end def test_receive_backlight_info_event_in_permanent_manual_mode

    @features("Feature1982")
    @features("Feature1982RequiredOptions", Backlight.SupportedOptionsMask.PWR_SAVE_S)
    @level("Functionality")
    @services('PowerSupply')
    @services('Rechargeable')
    @bugtracker("Backlight_EventGenerationForEnterOrExitCriticalBattery")
    def test_receive_backlight_info_event_if_enter_or_exit_disabled_by_critical_battery_state(self):
        """
        Validate that ``backlightInfoEvent`` is received if enter or exit disabled by critical battery state
        """
        self.post_requisite_reload_nvs = True
        default_options = Utils.get_default_options(self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_BACKLIGHT_CONFIG_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(
            self,
            configuration=Backlight.Configuration.ENABLE,
            options=default_options | Backlight.Options.PWR_SAVE)

        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.EVENT,
                                    class_type=self.feature_1982.backlight_info_event_cls)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set voltage to enter battery critical level (battery discharging mode)")
        # --------------------------------------------------------------------------------------------------------------
        critical_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'critical')
        battery_critical = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, critical_state_of_charge)
        self.power_supply_emulator.set_voltage(battery_critical)

        # Add delay, to let the device enter into critical battery state
        sleep(6)

        backlight_status = Backlight.BacklightStatus.DISABLED_BY_CRITICAL_BATTERY
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Wait for backlightInfoEvent with backlightStatus = {backlight_status}")
        # --------------------------------------------------------------------------------------------------------------
        backlight_info_event_resp = Utils.HIDppHelper.backlight_info_event(self)
        self.assertEqual(expected=HexList(backlight_status), obtained=backlight_info_event_resp.backlight_status,
                         msg=f"The backlight_status parameter differs (expected:{HexList(backlight_status)},"
                             f"obtained:{backlight_info_event_resp.backlight_status})")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set voltage to leave battery critical level (battery charging mode)")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_disable_recharge = True
        self.power_supply_emulator.recharge(True)
        self.device.turn_on_usb_charging_cable()

        low_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'low')
        battery_low = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, low_state_of_charge, discharge=False)
        self.power_supply_emulator.set_voltage(battery_low)

        backlight_status_als_on = Backlight.BacklightStatus.ALS_AUTOMATIC_MODE
        backlight_status_als_off = Backlight.BacklightStatus.ALS_MODE_SATURATED
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Wait for backlightInfoEvent with backlightStatus = "
                                  f"{backlight_status_als_on} or {backlight_status_als_off}")
        # --------------------------------------------------------------------------------------------------------------
        backlight_info_event_resp = Utils.HIDppHelper.backlight_info_event(self)
        self.assertIn(member=backlight_info_event_resp.backlight_status,
                      container=[HexList(backlight_status_als_on), HexList(backlight_status_als_off)],
                      msg=f"The backlight_status parameter differs ("
                          f"expected: {HexList(backlight_status_als_on)} or {HexList(backlight_status_als_off)}, "
                          f"obtained:{backlight_info_event_resp.backlight_status})")

        self.testCaseChecked("FUN_1982_0008", _AUTHOR)
    # end def test_receive_backlight_info_event_if_enter_or_exit_disabled_by_critical_battery_state

    @features("Feature1982")
    @features("NoMembraneKeyboard")
    @level("Functionality")
    def test_receive_backlight_info_event_when_there_is_a_change_of_backlight_effect(self):
        """
        Mechanical keyboard
        [Since v2] Shall receive backlightInfoEvent when there is a change of backlight effect.

        Note: Change the backlight effect on the keyboard (Fn+Vol Down)
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Change backlightEffect by pressing FN + Volume Down key")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=KEY_ID.FN_KEY)
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_VOLUME_DOWN, delay=1)
        self.button_stimuli_emulator.key_release(key_id=KEY_ID.FN_KEY)

        default_effect = Numeral(self.config.F_BacklightEffect)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Wait for backlightInfoEvent with backlightEffect != {default_effect}")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.backlight_info_event(self)
        self.assertNotEqual(unexpected=default_effect, obtained=get_backlight_info_resp.backlight_effect,
                            msg=f"The backlight_effect parameter shall not be {default_effect}, "
                                f"(obtained:{get_backlight_info_resp.backlight_effect})")

        self.testCaseChecked("FUN_1982_0009", _AUTHOR)
    # end def test_receive_backlight_info_event_when_there_is_a_change_of_backlight_effect

    @features("Feature1982v2+")
    @level("Functionality")
    @services('EmulatedKeys', (KEY_ID.BACKLIGHT_UP, KEY_ID.BACKLIGHT_DOWN,))
    def test_backlight_plus_minus_button_can_increase_decrease_backlight_intensity(self):
        """
        Validate that backlight +/- button can increase/decrease backlight intensity
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Store the currentLevel from GetBacklightInfo response")
        # --------------------------------------------------------------------------------------------------------------
        current_level = int(Numeral(get_backlight_info_resp.current_level))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press backlight + button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_UP)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        backlight_status = Backlight.BacklightStatus.MANUAL_MODE
        current_level += 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the currentLevel = {current_level}, backlightStatus = {backlight_status}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightInfoResponseChecker.check_current_level(self, get_backlight_info_resp, current_level)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp, backlight_status)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _PRESS_BACKLIGHT_DOWN_BUTTON)
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_DOWN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        current_level -= 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the currentLevel = {current_level}, backlightStatus = {backlight_status}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightInfoResponseChecker.check_current_level(self, get_backlight_info_resp, current_level)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp, backlight_status)

        self.testCaseChecked("FUN_1982_0010", _AUTHOR)
    # end def test_backlight_plus_minus_button_can_increase_decrease_backlight_intensity

    @features("Feature1982v2+")
    @level("Functionality")
    @services('EmulatedKeys', (KEY_ID.BACKLIGHT_UP,))
    def test_set_currentLevel_to_7_by_backlight_button_and_validate_backlightStatus(self):
        """
        Validate that backlightStatus settings shall not be changed after changed backlight effect when currentLevel is
        set to 7 by backlight +/- button
        """
        self.post_requisite_reload_nvs = True
        duration = Utils.compute_duration_to_max_or_min_level(self, to_max_level=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press backlight + button with duration {duration}s to the max level")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_UP, duration=duration)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_CURRENT_LEVEL_7_BACKLIGHT_STATUS_4)
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightInfoResponseChecker.check_current_level(self, get_backlight_info_resp,
                                                                  Backlight.CurrentLevel.CURRENT_LEVEL_7)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.MANUAL_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_BACKLIGHT_CONFIG_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_effect(test_case=self,
                                               backlight_effect=Utils.get_non_default_backlight_effect(self))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_CURRENT_LEVEL_7_BACKLIGHT_STATUS_4)
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightInfoResponseChecker.check_current_level(self, get_backlight_info_resp,
                                                                  Backlight.CurrentLevel.CURRENT_LEVEL_7)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.MANUAL_MODE)

        self.testCaseChecked("FUN_1982_0011", _AUTHOR)
    # end def test_set_currentLevel_to_7_by_backlight_button_and_validate_backlightStatus

    @features("Feature1982")
    @level("Functionality")
    @services('EmulatedKeys', (KEY_ID.BACKLIGHT_UP,))
    def test_current_level_returned_to_als_settings_after_reconnection(self):
        """
        Temporary manual mode -> Automatic mode
        Validate that currentLevel returned to ALS settings after reconnection when currentLevel is set to 7 by
        backlight +/- button
        """
        self.post_requisite_reload_nvs = True
        duration = Utils.compute_duration_to_max_or_min_level(self, to_max_level=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press backlight + button with duration {duration}s to the max level")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_UP, duration=duration)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_CURRENT_LEVEL_7_BACKLIGHT_STATUS_4)
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightInfoResponseChecker.check_current_level(self, get_backlight_info_resp,
                                                                  Backlight.CurrentLevel.CURRENT_LEVEL_7)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.MANUAL_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Disconnect device then reconnect to it after 6 seconds (to make sure device "
                                 "reconnected from deep sleep mode)")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.close_channel(self)
        self.device.disable_usb_port(port_index=ChannelUtils.get_port_index(self))
        # Wait device to enter deep sleep mode
        sleep(6)
        self.device.enable_usb_port(port_index=ChannelUtils.get_port_index(self))
        DeviceManagerUtils.set_channel(self, new_channel=self.current_channel)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wake up device")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Wait power led turned off")
        # --------------------------------------------------------------------------------------------------------------
        sleep(Utils.POWER_LED_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the currentLevel != {Backlight.CurrentLevel.CURRENT_LEVEL_7} and "
                                  f"backlightStatus = {Backlight.BacklightStatus.ALS_AUTOMATIC_MODE}")
        # --------------------------------------------------------------------------------------------------------------
        self.assertNotEqual(unexpected=HexList(Backlight.CurrentLevel.CURRENT_LEVEL_7),
                            obtained=get_backlight_info_resp.current_level,
                            msg=f"The current_level parameter shall not be 7, "
                                f"obtained:{get_backlight_info_resp.current_level})")
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.ALS_AUTOMATIC_MODE)

        self.testCaseChecked("FUN_1982_0012", _AUTHOR)
    # end def test_current_level_returned_to_als_settings_after_reconnection

    @features("Feature1982")
    @level("Functionality")
    @services('EmulatedKeys', (KEY_ID.BACKLIGHT_UP,))
    def test_current_level_returned_to_als_settings_after_power_reset(self):
        """
        Validate that currentLevel returned to ALS settings after power reset when currentLevel is set to 7 by
        backlight +/- button
        """
        self.post_requisite_reload_nvs = True
        duration = Utils.compute_duration_to_max_or_min_level(self, to_max_level=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press backlight + button with duration {duration}s to the max level")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_UP, duration=duration)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_CURRENT_LEVEL_7_BACKLIGHT_STATUS_4)
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightInfoResponseChecker.check_current_level(self, get_backlight_info_resp,
                                                                  Backlight.CurrentLevel.CURRENT_LEVEL_7)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.MANUAL_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power reset the device")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)
        sleep(Utils.POWER_LED_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the currentLevel != 7 and backlightStatus = 2")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.ALS_AUTOMATIC_MODE)
        self.assertNotEqual(unexpected=HexList(Backlight.CurrentLevel.CURRENT_LEVEL_7),
                            obtained=get_backlight_info_resp.current_level,
                            msg=f"The current_level shouldn't be 7")

        self.testCaseChecked("FUN_1982_0013", _AUTHOR)
    # end def test_current_level_returned_to_als_settings_after_power_reset

    @features("Feature1982")
    @level("Functionality")
    @services('AmbientLightSensor')
    def test_backlight_shall_be_turned_off_when_als_is_let_in_saturated_state(self):
        """
        Auto_OFF_NotPowered (Use case 3)
        Validate that backlight shall be turned off when ALS is let in saturated state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Let ALS in saturated state by ALS emulator")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_restore_default_luminance_value = True
        luminance_threshold_backlight_off = self.ambient_light_sensor_emulator.get_luminance_threshold_backlight_off()
        self.ambient_light_sensor_emulator.\
            set_ambient_light_intensity(luminance_threshold_backlight_off * _UPPER_MARGIN_LUMINANCE_VALUE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset DUT to update ALS value")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)
        # Let some time for the device to compute ALS value after its internal reset
        sleep(5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the currentLevel = 0 and backlightStatus = 3")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightInfoResponseChecker.check_current_level(self, get_backlight_info_resp,
                                                                  Backlight.CurrentLevel.CURRENT_LEVEL_0)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.ALS_MODE_SATURATED)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set ALS to default value by ALS emulator")
        # --------------------------------------------------------------------------------------------------------------
        self.ambient_light_sensor_emulator.set_ambient_light_intensity()
        self.post_requisite_restore_default_luminance_value = False

        self.testCaseChecked("FUN_1982_0014", _AUTHOR)
    # end def test_backlight_shall_be_turned_off_when_als_is_let_in_saturated_state

    @features("Feature1982v2+")
    @level("Functionality")
    def test_nvs_content_of_backlight_feature_by_set_backlight_config(self):
        """
        Validate NVS content of backlight feature after setting bcklEn=1, wow=0, crown=0, pwrSave=0,
        backlightEffect=none_default_effect by setBacklightConfig
        """
        self.post_requisite_reload_nvs = True
        disabled_wow_crown_pwrsave = Utils.get_default_options(self) & 0xF8
        none_default_effect = Utils.get_non_default_backlight_effect(self)
        curr_duration_hands_out = 4
        curr_duration_hands_in = 5
        curr_duration_powered = 6

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_BACKLIGHT_CONFIG_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=disabled_wow_crown_pwrsave,
                                               backlight_effect=none_default_effect,
                                               curr_duration_hands_out=curr_duration_hands_out,
                                               curr_duration_hands_in=curr_duration_hands_in,
                                               curr_duration_powered=curr_duration_powered)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read NVS_LEDBKLT_ID chunks in NVS")
        # --------------------------------------------------------------------------------------------------------------
        backlight_chunk = Utils.get_backlight_chunk(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check all of settings changed as input settings")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightConfigResponseChecker.check_configuration(self, backlight_chunk,
                                                                    Backlight.Configuration.ENABLE)
        Utils.GetBacklightInfoResponseChecker.check_backlight_effect(self, backlight_chunk, none_default_effect)
        self.assertEqual(expected=HexList(disabled_wow_crown_pwrsave), obtained=backlight_chunk.options,
                         msg="The options parameter differs from the expected one")
        if self.feature_1982.VERSION > 2:
            checker = Utils.GetBacklightConfigResponseChecker
            checker.check_curr_duration_hands_out(self, backlight_chunk, curr_duration_hands_out)
            checker.check_curr_duration_hands_in(self, backlight_chunk, curr_duration_hands_in)
            checker.check_curr_duration_powered(self, backlight_chunk, curr_duration_powered)
        # end if

        self.testCaseChecked("FUN_1982_0015", _AUTHOR)
    # end def test_nvs_content_of_backlight_feature_by_set_backlight_config

    @features("Feature1982v2+")
    @level("Functionality")
    def test_setting_backlight_effect_by_set_backlight_config_will_not_change_current_effect(self):
        """
        Validate that setting backlightEffect to 0xFF by setBacklightConfig will not change current effect
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_BACKLIGHT_CONFIG_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=Utils.get_default_options(self),
                                               backlight_effect=Backlight.BacklightEffect.CURRENT_EFFECT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the backlightEffect = default_backlight_effect")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightInfoResponseChecker.check_backlight_effect(self, get_backlight_info_resp,
                                                                     self.config.F_BacklightEffect)

        self.testCaseChecked("FUN_1982_0016", _AUTHOR)
    # end def test_setting_backlight_effect_by_set_backlight_config_will_not_change_current_effect

    @features("Feature1982v2+")
    @level("Functionality")
    def test_setting_backlight_effect_by_set_backlight_effect_will_not_change_current_effect(self):
        """
        Validate that setting backlightEffect to 0xFF by ``setBacklightEffect`` will not change current effect
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setBacklightEffect request")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_effect(self, backlight_effect=Backlight.BacklightEffect.CURRENT_EFFECT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the backlightEffect = default_backlight_effect")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightInfoResponseChecker.check_backlight_effect(self, get_backlight_info_resp,
                                                                     self.config.F_BacklightEffect)

        self.testCaseChecked("FUN_1982_0017", _AUTHOR)
    # end def test_setting_backlight_effect_by_set_backlight_effect_will_not_change_current_effect

    @features("Feature1982")
    @level("Functionality")
    @services('EmulatedKeys', (KEY_ID.BACKLIGHT_UP, KEY_ID.BACKLIGHT_DOWN,))
    def test_brightness_levels_can_be_set_by_backlight_buttons(self):
        """
        Validate that all 8 brightness levels can be set by backlight +/- buttons
        """
        self.post_requisite_reload_nvs = True
        press_count = Utils.compute_press_count_to_max_or_min_level(self, to_max_level=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press backlight + button {press_count} times to the max level")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_UP, repeat=press_count, delay=0.1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_CURRENT_LEVEL_7_BACKLIGHT_STATUS_4)
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightInfoResponseChecker.check_current_level(self, get_backlight_info_resp,
                                                                  Backlight.CurrentLevel.CURRENT_LEVEL_7)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.MANUAL_MODE)

        press_count = Utils.compute_press_count_to_max_or_min_level(self, to_max_level=False)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press backlight - button {press_count} times to the lowest level")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_DOWN, repeat=press_count, delay=0.1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_CURRENT_LEVEL_0_BACKLIGHT_STATUS_4)
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightInfoResponseChecker.check_current_level(self, get_backlight_info_resp,
                                                                  Backlight.CurrentLevel.CURRENT_LEVEL_0)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.MANUAL_MODE)

        self.testCaseChecked("FUN_1982_0018", _AUTHOR)
    # end def test_brightness_levels_can_be_set_by_backlight_buttons

    @features("Feature1805")
    @features("Feature1982")
    @level("Functionality")
    @services('EmulatedKeys', (KEY_ID.BACKLIGHT_UP,))
    def test_brightness_feature_configured_in_automatic_mode_after_oob(self):
        """
        OOB
        Validate that when user takes his device from the box (OOB), user expects to have the backlight feature
        configured in automatic mode by default
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press backlight + button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_UP)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check backlightStatus = {Backlight.BacklightStatus.MANUAL_MODE}")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.MANUAL_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pre-pair device to the first receiver")
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.pre_pair_device_to_receiver(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setOobState request")
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.HIDppHelper.set_oob_state(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _DEVICE_RESET)
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Wait power led turned off")
        # --------------------------------------------------------------------------------------------------------------
        sleep(Utils.POWER_LED_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the currentLevel in [2, 4], "
                                  f"backlightStatus = {Backlight.BacklightStatus.ALS_AUTOMATIC_MODE}, "
                                  f"backlightEffect = {self.config.F_BacklightEffect}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightInfoResponseChecker.check_current_level_by_range(
            self, get_backlight_info_resp, [Backlight.CurrentLevel.CURRENT_LEVEL_2,
                                            Backlight.CurrentLevel.CURRENT_LEVEL_4])
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.ALS_AUTOMATIC_MODE)
        if self.feature_1982.VERSION > 1:
            Utils.GetBacklightInfoResponseChecker.check_backlight_effect(self, get_backlight_info_resp,
                                                                         self.config.F_BacklightEffect)
        # end if

        self.testCaseChecked("FUN_1982_0019", _AUTHOR)
    # end def test_brightness_feature_configured_in_automatic_mode_after_oob

    @features("Feature1982")
    @level("Functionality")
    def test_brightness_feature_remain_same_until_reactivate(self):
        """
        Disabled by SW
        Validate that when user has deactivated the backlight feature, user expects that will remain as this until
        he reactivates the backlight
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_BACKLIGHT_CONFIG_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.DISABLE,
                                               options=Utils.get_default_options(self))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate backlight config by GetBacklightConfig response")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)
        Utils.GetBacklightConfigResponseChecker.check_configuration(self, get_backlight_config_resp,
                                                                    Backlight.Configuration.DISABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _DEVICE_RESET)
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Validate bcklEn = {Backlight.Configuration.DISABLE} by GetBacklightConfig response")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)
        Utils.GetBacklightConfigResponseChecker.check_configuration(self, get_backlight_config_resp,
                                                                    Backlight.Configuration.DISABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_BACKLIGHT_CONFIG_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=Utils.get_default_options(self))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate bcklEn = 1 by GetBacklightConfig response")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)
        Utils.GetBacklightConfigResponseChecker.check_configuration(self, get_backlight_config_resp,
                                                                    Backlight.Configuration.ENABLE)

        self.testCaseChecked("FUN_1982_0020", _AUTHOR)
    # end def test_brightness_feature_remain_same_until_reactivate

    @features("Feature1982v2+")
    @features('Feature1830powerMode', 3)
    @level("Functionality")
    @services('EmulatedKeys', (KEY_ID.BACKLIGHT_UP,))
    def test_backlight_configuration_is_reset_to_default_configuration(self):
        """
        Validate that when the device has not been used for 2 hours and the user has not deactivated the backlight,
        the backlight configuration is reset to the default configuration except the backlight effect
        """
        self.post_requisite_reload_nvs = True
        non_default_effect = Utils.get_non_default_backlight_effect(self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_BACKLIGHT_CONFIG_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=Utils.get_default_options(self),
                                               backlight_effect=non_default_effect)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check getBacklightInfo response fields")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)
        Utils.GetBacklightInfoResponseChecker.check_backlight_effect(self, get_backlight_info_resp, non_default_effect)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.ALS_AUTOMATIC_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press backlight + button twice")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_UP, repeat=2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check backlightStatus = {Backlight.BacklightStatus.MANUAL_MODE}")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(
            self, get_backlight_info_resp, Backlight.BacklightStatus.MANUAL_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wait device enter deep sleep mode")
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wake up device")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Wait power led turned off")
        # --------------------------------------------------------------------------------------------------------------
        sleep(Utils.POWER_LED_TIMEOUT)

        backlight_status = Backlight.BacklightStatus.ALS_AUTOMATIC_MODE
        configuration = Backlight.Configuration.ENABLE
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Validate bcklEn = {configuration}, backlightEffect = {non_default_effect}, "
                                  f"backlightStatus = {backlight_status}")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)
        Utils.GetBacklightConfigResponseChecker.check_configuration(self, get_backlight_config_resp, configuration)
        Utils.GetBacklightInfoResponseChecker.check_backlight_effect(self, get_backlight_info_resp, non_default_effect)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp, backlight_status)

        self.testCaseChecked("FUN_1982_0021", _AUTHOR)
    # end def test_backlight_configuration_is_reset_to_default_configuration

    @features("Feature1982")
    @level("Functionality")
    @services('EmulatedKeys', (KEY_ID.BACKLIGHT_UP,))
    def test_reactivate_backlight_feature_through_software(self):
        """
        TempManual_OFF_NotPowered: Action-5
        Validate that when the user reactivate the backlight feature through the Software, the backlight setting
        restarts in automatic mode
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Backlight.setBacklightConfig with bcklEn = 0 and "
                                 "bcklMode=Automatic mode(1), others set by default values")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(
            self, configuration=Backlight.Configuration.DISABLE, options=Utils.get_default_options(self))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press backlight + button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_UP)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check backlightStatus = {Backlight.BacklightStatus.DISABLED_BY_SW}")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.DISABLED_BY_SW)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, "Validate bcklEn = 0 and bcklMode=Automatic mode(1) by Backlight.getBacklightConfig")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)
        Utils.GetBacklightConfigResponseChecker.check_configuration(
            test_case=self, response=get_backlight_config_resp, expected=Backlight.Configuration.DISABLE)
        Utils.GetBacklightConfigResponseChecker.check_supported_options(
            test_case=self, response=get_backlight_config_resp, expected=self.config.F_SupportedOptions)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Backlight.setBacklightConfig with bcklEn = 1 and "
                                 "bcklMode=Automatic mode(1), others set by default values")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(
            self, configuration=Backlight.Configuration.ENABLE, options=Utils.get_default_options(self))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate bcklEn = 1 and bcklMode=Automatic mode(1) by Backlight.getBacklightConfig")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)
        Utils.GetBacklightConfigResponseChecker.check_configuration(
            test_case=self, response=get_backlight_config_resp, expected=Backlight.Configuration.ENABLE)
        Utils.GetBacklightConfigResponseChecker.check_supported_options(
            test_case=self, response=get_backlight_config_resp, expected=self.config.F_SupportedOptions)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(
            test_case=self, response=get_backlight_info_resp, expected=Backlight.BacklightStatus.ALS_AUTOMATIC_MODE)

        self.testCaseChecked("FUN_1982_0022#1", _AUTHOR)
    # end def test_reactivate_backlight_feature_through_software

    @features("Feature1982")
    @level("Functionality")
    @services('EmulatedKeys', (KEY_ID.BACKLIGHT_UP,))
    def test_reactivate_backlight_feature_through_software_in_charging_state(self):
        """
        TempManual_OFF_Powered: Action-5
        Validate when the user reactivate the backlight feature through the Software, the backlight setting stay
        in the Temporary manual mode while USB charging cable replugged.
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_unplug_usb_charging_cable = True
        configuration = Backlight.Configuration.DISABLE
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Replug USB charging cable")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.ChargingHelper.enter_charging_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press backlight + button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_UP)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check backlightStatus = {Backlight.BacklightStatus.MANUAL_MODE}")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.MANUAL_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_BACKLIGHT_CONFIG_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=configuration,
                                               options=Utils.get_default_options(self))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Validate bcklEn = {configuration} and all other settings return default values")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)
        Utils.GetBacklightConfigResponseChecker.check_configuration(
            test_case=self, response=get_backlight_config_resp, expected=configuration)
        Utils.GetBacklightConfigResponseChecker.check_supported_options(
            test_case=self, response=get_backlight_config_resp, expected=self.config.F_SupportedOptions)

        configuration = Backlight.Configuration.ENABLE
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_BACKLIGHT_CONFIG_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=configuration,
                                               options=Utils.get_default_options(self))

        backlight_status = Backlight.BacklightStatus.ALS_AUTOMATIC_MODE
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Validate bcklEn = {configuration}, backlightStatus = {backlight_status}")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)
        Utils.GetBacklightConfigResponseChecker.check_configuration(
            test_case=self, response=get_backlight_config_resp, expected=configuration)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(
            test_case=self, response=get_backlight_info_resp, expected=backlight_status)

        self.testCaseChecked("FUN_1982_0022#2", _AUTHOR)
    # end def test_reactivate_backlight_feature_through_software_in_charging_state

    @features("Feature1982v3+")
    @level("Functionality")
    @services('EmulatedKeys', (KEY_ID.BACKLIGHT_UP,))
    def test_reactivate_backlight_feature_through_software_in_permanent_manual_mode(self):
        """
        PermManual_OFF_NotPowered: Action-5
        Validate when the user reactivate the backlight feature through the Software in the the Permanent manual mode,
        the backlight setting stay in the Permanent manual mode.
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Backlight.setBacklightConfig with bcklEn = 0 and "
                                 "bcklMode=Permanent manual mode(3), others set by default values")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(
            self, configuration=Backlight.Configuration.DISABLE,
            options=(Utils.get_default_options(self) & 0x07) | Backlight.Options.PERMANENT_MANUAL_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check backlightStatus = {Backlight.BacklightStatus.DISABLED_BY_SW}")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.DISABLED_BY_SW)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, "Validate bcklEn = 0, backlightStatus = Permanent manual mode(3) by Backlight.getBacklightConfig")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)
        Utils.GetBacklightConfigResponseChecker.check_configuration(
            test_case=self, response=get_backlight_config_resp, expected=Backlight.Configuration.DISABLE)
        Utils.GetBacklightConfigResponseChecker.check_supported_options(
            test_case=self, response=get_backlight_config_resp,
            expected=Numeral(self.config.F_SupportedOptions) & 0x07FF | (Backlight.Options.PERMANENT_MANUAL_MODE << 8))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Backlight.setBacklightConfig with bcklEn = 1 and "
                                 "bcklMode=Permanent manual mode(3), others set by default values")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(
            self, configuration=Backlight.Configuration.ENABLE,
            options=(Utils.get_default_options(self) & 0x07) | Backlight.Options.PERMANENT_MANUAL_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate bcklEn = 1, backlightStatus = Permanent manual mode(3) "
                                  "by Backlight.getBacklightConfig")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)
        Utils.GetBacklightConfigResponseChecker.check_configuration(
            test_case=self, response=get_backlight_config_resp, expected=Backlight.Configuration.ENABLE)
        Utils.GetBacklightConfigResponseChecker.check_supported_options(
            test_case=self, response=get_backlight_config_resp,
            expected=Numeral(self.config.F_SupportedOptions) & 0x07FF | (Backlight.Options.PERMANENT_MANUAL_MODE << 8))
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(
            test_case=self, response=get_backlight_info_resp, expected=Backlight.BacklightStatus.PERMANENT_MANUAL_MODE)

        self.testCaseChecked("FUN_1982_0022#3", _AUTHOR)
    # end def test_reactivate_backlight_feature_through_software_in_permanent_manual_mode

    @features("Feature1805")
    @features("Feature1816")
    @features("Feature1982v0tov2")
    @level("Functionality")
    def test_oob_static_backlight_effect_applied_to_all_layers(self):
        """
        OOB
        [Up to v2 ] Validate OOB, the backlight effect (Static) should be applied to all layers
        """
        self.post_requisite_reload_nvs = True
        non_default_effect = Utils.get_non_default_backlight_effect(self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Change backlight effect to non-default setting {non_default_effect}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=Utils.get_default_options(self),
                                               backlight_effect=non_default_effect)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check backlight effect = {non_default_effect}")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)
        Utils.GetBacklightInfoResponseChecker.check_backlight_effect(self, get_backlight_info_resp, non_default_effect)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pre-pair device to the first receiver")
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.pre_pair_device_to_receiver(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setOobState request")
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.HIDppHelper.set_oob_state(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _DEVICE_RESET)
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Wait power led turned off")
        # --------------------------------------------------------------------------------------------------------------
        sleep(Utils.POWER_LED_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the currentLevel in [2, 4], "
                                  f"backlightStatus = {Backlight.BacklightStatus.ALS_AUTOMATIC_MODE}, "
                                  f"backlightEffect = {self.config.F_BacklightEffect}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightInfoResponseChecker.check_current_level_by_range(
            self, get_backlight_info_resp, [Backlight.CurrentLevel.CURRENT_LEVEL_2,
                                            Backlight.CurrentLevel.CURRENT_LEVEL_4])
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.ALS_AUTOMATIC_MODE)
        Utils.GetBacklightInfoResponseChecker.check_backlight_effect(self, get_backlight_info_resp,
                                                                     Backlight.BacklightEffect.STATIC_EFFECT)

        self.testCaseChecked("FUN_1982_0023", _AUTHOR)
    # end def test_oob_static_backlight_effect_applied_to_all_layers

    @features("Feature1982")
    @level("Functionality")
    @services('EmulatedKeys', (KEY_ID.BACKLIGHT_UP,))
    def test_backlight_is_increased_to_max_level_by_key_press_and_hold(self):
        """
        Validate that the backlight is increased to max level by key press and hold
        """
        self.post_requisite_reload_nvs = True
        duration = Utils.compute_duration_to_max_or_min_level(self, to_max_level=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press and hold backlight + button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(KEY_ID.BACKLIGHT_UP)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Wait {duration} seconds to the max backlight level")
        # --------------------------------------------------------------------------------------------------------------
        sleep(duration)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the currentLevel = {Backlight.CurrentLevel.CURRENT_LEVEL_7} and "
                                  f"backlightStatus = {Backlight.BacklightStatus.MANUAL_MODE}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightInfoResponseChecker.check_current_level(
            self, get_backlight_info_resp, Backlight.CurrentLevel.CURRENT_LEVEL_7)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(
            self, get_backlight_info_resp, Backlight.BacklightStatus.MANUAL_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Release backlight + button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(KEY_ID.BACKLIGHT_UP)

        self.testCaseChecked("FUN_1982_0024", _AUTHOR)
    # end def test_backlight_is_increased_to_max_level_by_key_press_and_hold

    @features("Feature1982")
    @level("Functionality")
    @services('EmulatedKeys', (KEY_ID.BACKLIGHT_UP, KEY_ID.BACKLIGHT_DOWN,))
    def test_behavior_when_brightness_level_is_maximum_or_minimum_and_up_or_down_key_pressed(self):
        """
        Validate the current level keeps unchanged when the level is max then the user pressed the brightness up key
        and also when the level is minimum then the user pressed the brightness down key
        """
        self.post_requisite_reload_nvs = True
        press_count = Utils.compute_press_count_to_max_or_min_level(self, to_max_level=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press backlight + button {press_count} times to the max level")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_UP, repeat=press_count, delay=0.1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_CURRENT_LEVEL_7_BACKLIGHT_STATUS_4)
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightInfoResponseChecker.check_current_level(
            self, get_backlight_info_resp, Backlight.CurrentLevel.CURRENT_LEVEL_7)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(
            self, get_backlight_info_resp, Backlight.BacklightStatus.MANUAL_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press backlight + button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_UP)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_CURRENT_LEVEL_7_BACKLIGHT_STATUS_4)
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightInfoResponseChecker.check_current_level(
            self, get_backlight_info_resp, Backlight.CurrentLevel.CURRENT_LEVEL_7)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(
            self, get_backlight_info_resp, Backlight.BacklightStatus.MANUAL_MODE)

        press_count = Utils.compute_press_count_to_max_or_min_level(self, to_max_level=False)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press backlight - button {press_count} times to the lowest level")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_DOWN, repeat=press_count, delay=0.1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_CURRENT_LEVEL_0_BACKLIGHT_STATUS_4)
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightInfoResponseChecker.check_current_level(
            self, get_backlight_info_resp, Backlight.CurrentLevel.CURRENT_LEVEL_0)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(
            self, get_backlight_info_resp, Backlight.BacklightStatus.MANUAL_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _PRESS_BACKLIGHT_DOWN_BUTTON)
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_DOWN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _GET_BACKLIGHT_INFO_REQUEST)
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_CURRENT_LEVEL_0_BACKLIGHT_STATUS_4)
        # --------------------------------------------------------------------------------------------------------------
        Utils.GetBacklightInfoResponseChecker.check_current_level(
            self, get_backlight_info_resp, Backlight.CurrentLevel.CURRENT_LEVEL_0)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(
            self, get_backlight_info_resp, Backlight.BacklightStatus.MANUAL_MODE)

        self.testCaseChecked("FUN_1982_0025", _AUTHOR)
    # end def test_behavior_when_brightness_level_is_maximum_or_minimum_and_up_or_down_key_pressed

    @features("Feature1982v2+")
    @features("Feature1830")
    @level("Functionality")
    @services('EmulatedKeys', (KEY_ID.BACKLIGHT_DOWN,))
    def test_backlight_mode_stay_unchanged_if_disabled_backlight_manually_after_woke_up_device(self):
        """
        TempManual_OFF_NotPowered: Action-3
        BcklMode unchaged - Manually disabled (BLL set to Level 0)
        [Since v2] Validate when the device has not been used for 2 hours and the user has deactivated
        (backlight level=0) the backlight by backlight key, the backlight configuration be kept and stay
        in Temporary Manual Mode after woke up from deep sleep mode.
        """
        self.post_requisite_reload_nvs = True
        inverted_default_capability = Utils.get_inverted_default_capability(self)
        backlight_effect = Utils.get_non_default_backlight_effect(self)
        duration_hands_out = 1
        duration_hands_in = 2
        duration_powered = 3
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Backlight.setBacklightConfig with bcklEn = 1, bcklMode = Automatic mode "
                                 "and other parameters with non-default setting")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=inverted_default_capability,
                                               backlight_effect=backlight_effect,
                                               curr_duration_hands_out=duration_hands_out,
                                               curr_duration_hands_in=duration_hands_in,
                                               curr_duration_powered=duration_powered)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set currentBacklightLevel = 0 by press Backlight - button")
        # --------------------------------------------------------------------------------------------------------------
        press_count = Utils.compute_press_count_to_max_or_min_level(self, to_max_level=False)
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_DOWN, repeat=press_count)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, "Check current_level=0 and backlightStatus = Temporary manual mode (4) by getBacklightInfo")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)
        Utils.GetBacklightInfoResponseChecker.check_current_level(self, get_backlight_info_resp,
                                                                  Backlight.CurrentLevel.CURRENT_LEVEL_0)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.MANUAL_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "0x1830.setPowerMode = Deep sleep mode")
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "User action")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wait power LED timeout")
        # --------------------------------------------------------------------------------------------------------------
        sleep(Utils.POWER_LED_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, "Check wow, crown, pwrSave and durations equals to non-default setting. "
                  "Check the currentBacklightLevel = 0")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)
        checker = Utils.GetBacklightConfigResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(HOST.CH1)),
            "supported_options": (checker.check_supported_options,
                                  (Numeral(self.config.F_SupportedOptions) & 0x00FF) |
                                  (inverted_default_capability << 8)),
            "current_backlight_level": (checker.check_current_backlight_level, Backlight.CurrentLevel.CURRENT_LEVEL_0),
            "curr_duration_hands_out": (checker.check_curr_duration_hands_out, duration_hands_out),
            "curr_duration_hands_in": (checker.check_curr_duration_hands_in, duration_hands_in),
            "curr_duration_powered": (checker.check_curr_duration_powered, duration_powered),
        })
        checker.check_fields(
            self, get_backlight_config_resp, self.feature_1982.get_backlight_config_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, "Check backlightStatus = Temporary manual mode (4), backlightEffect = {none default effect}")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)
        checker = Utils.GetBacklightInfoResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "backlight_status": (checker.check_backlight_status, Backlight.BacklightStatus.MANUAL_MODE),
            "current_level": (checker.check_current_level, Backlight.CurrentLevel.CURRENT_LEVEL_0),
            "backlight_effect": (checker.check_backlight_effect, backlight_effect),
        })
        checker.check_fields(
            self, get_backlight_info_resp, self.feature_1982.get_backlight_info_response_cls, check_map)

        self.testCaseChecked("FUN_1982_0026#1", _AUTHOR)
    # end def test_backlight_mode_stay_unchanged_if_disabled_backlight_manually_after_woke_up_device

    @features("Feature1982v2+")
    @level("Functionality")
    @services('EmulatedKeys', (KEY_ID.BACKLIGHT_DOWN,))
    def test_backlight_mode_stay_unchanged_if_disabled_backlight_manually_after_changed_host(self):
        """
        TempManual_OFF_Powered: Action-16
        BcklMode unchaged - Manually disabled (BLL set to Level 0)
        [Since v2] Validate when the user has deactivated (backlight level=0) the backlight by backlight key,
        the backlight configuration be kept and stay in Temporary Manual Mode after changed host.
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_unplug_usb_charging_cable = True
        self.post_requisite_clean_pairing_data = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Plug USB charging cable")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.ChargingHelper.enter_charging_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair host 2 to receiver slot 2")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.pair_all_available_hosts(self, number_of_host=2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Change to host 1 by press host 1 button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(HOST.CH1)
        DeviceManagerUtils.switch_channel(
            test_case=self,
            new_channel_id=ChannelIdentifier(port_index=1, device_index=HOST.CH1), allow_no_message=True)

        inverted_default_capability = Utils.get_inverted_default_capability(self)
        backlight_effect = Utils.get_non_default_backlight_effect(self)
        duration_hands_out = 1
        duration_hands_in = 2
        duration_powered = 3
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Backlight.setBacklightConfig with bcklEn = 1, bcklMode = Automatic mode "
                                 "and other parameters with non-default setting")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=inverted_default_capability,
                                               backlight_effect=backlight_effect,
                                               curr_duration_hands_out=duration_hands_out,
                                               curr_duration_hands_in=duration_hands_in,
                                               curr_duration_powered=duration_powered)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set currentBacklightLevel = 0 by press Backlight - button")
        # --------------------------------------------------------------------------------------------------------------
        press_count = Utils.compute_press_count_to_max_or_min_level(self, to_max_level=False)
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_DOWN, repeat=press_count)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, "Check current_level=0 and backlightStatus = Temporary manual mode (4) by getBacklightInfo")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)
        Utils.GetBacklightInfoResponseChecker.check_current_level(self, get_backlight_info_resp,
                                                                  Backlight.CurrentLevel.CURRENT_LEVEL_0)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.MANUAL_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Change to host 2 by press host 2 button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(HOST.CH2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Change tp host 1 by press host 1 button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(HOST.CH1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, "Check wow, crown, pwrSave and durations equals to non-default setting. "
                  "Check the currentBacklightLevel = 0")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)
        checker = Utils.GetBacklightConfigResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(HOST.CH1)),
            "supported_options": (checker.check_supported_options,
                                  (Numeral(self.config.F_SupportedOptions) & 0x00FF) |
                                  (inverted_default_capability << 8)),
            "current_backlight_level": (checker.check_current_backlight_level, Backlight.CurrentLevel.CURRENT_LEVEL_0),
            "curr_duration_hands_out": (checker.check_curr_duration_hands_out, duration_hands_out),
            "curr_duration_hands_in": (checker.check_curr_duration_hands_in, duration_hands_in),
            "curr_duration_powered": (checker.check_curr_duration_powered, duration_powered),
        })
        checker.check_fields(
            self, get_backlight_config_resp, self.feature_1982.get_backlight_config_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, "Check backlightStatus = Temporary manual mode (4), backlightEffect = {none default effect}")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)
        checker = Utils.GetBacklightInfoResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "backlight_status": (checker.check_backlight_status, Backlight.BacklightStatus.MANUAL_MODE),
            "current_level": (checker.check_current_level, Backlight.CurrentLevel.CURRENT_LEVEL_0),
            "backlight_effect": (checker.check_backlight_effect, backlight_effect),
        })
        checker.check_fields(
            self, get_backlight_info_resp, self.feature_1982.get_backlight_info_response_cls, check_map)

        self.testCaseChecked("FUN_1982_0026#2", _AUTHOR)
    # end def test_backlight_mode_stay_unchanged_if_disabled_backlight_manually_after_changed_host

    @features("Feature1982v2+")
    @level("Functionality")
    @services('EmulatedKeys', (KEY_ID.BACKLIGHT_DOWN,))
    def test_backlight_mode_changed_from_manual_mode_to_als_mode_after_power_cycle(self):
        """
        TempManual_ON_NotPowered: Action-15
        BcklMode unchaged - Manually disabled (BLL set to Level 0)
        [Since v2] Validate when the user has deactivated (backlight level=0) the backlight by backlight key,
        the backlight configuration be kept but backlight mode changed to ALS mode and current level = default level
        after power off->on device.
        """
        self.post_requisite_reload_nvs = True
        inverted_default_capability = Utils.get_inverted_default_capability(self)
        backlight_effect = Utils.get_non_default_backlight_effect(self)
        duration_hands_out = 1
        duration_hands_in = 2
        duration_powered = 3
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Backlight.setBacklightConfig with bcklEn = 1, bcklMode = Automatic mode "
                                 "and other parameters with non-default setting")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=inverted_default_capability,
                                               backlight_effect=backlight_effect,
                                               curr_duration_hands_out=duration_hands_out,
                                               curr_duration_hands_in=duration_hands_in,
                                               curr_duration_powered=duration_powered)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set currentBacklightLevel = 0 by press Backlight - button")
        # --------------------------------------------------------------------------------------------------------------
        press_count = Utils.compute_press_count_to_max_or_min_level(self, to_max_level=False)
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_DOWN, repeat=press_count)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, "Check current_level=0 and backlightStatus = Temporary manual mode (4) by getBacklightInfo")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)
        Utils.GetBacklightInfoResponseChecker.check_current_level(self, get_backlight_info_resp,
                                                                  Backlight.CurrentLevel.CURRENT_LEVEL_0)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.MANUAL_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power reset DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wait power LED timeout")
        # --------------------------------------------------------------------------------------------------------------
        sleep(Utils.POWER_LED_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, "Check wow, crown, pwrSave and durations equals to non-default setting. "
                  "Check the currentBacklightLevel = default level")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_config_resp = Utils.HIDppHelper.get_backlight_config(self)
        checker = Utils.GetBacklightConfigResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(HOST.CH1)),
            "supported_options": (checker.check_supported_options,
                                  (Numeral(self.config.F_SupportedOptions) & 0x00FF) |
                                  (inverted_default_capability << 8)),
            "curr_duration_hands_out": (checker.check_curr_duration_hands_out, duration_hands_out),
            "curr_duration_hands_in": (checker.check_curr_duration_hands_in, duration_hands_in),
            "curr_duration_powered": (checker.check_curr_duration_powered, duration_powered),
        })
        checker.check_fields(
            self, get_backlight_config_resp, self.feature_1982.get_backlight_config_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, "Check backlightStatus = ALS mode (2), backlightEffect = {none default effect}")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)
        checker = Utils.GetBacklightInfoResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "backlight_effect": (checker.check_backlight_effect, backlight_effect),
        })
        checker.check_fields(
            self, get_backlight_info_resp, self.feature_1982.get_backlight_info_response_cls, check_map)

        self.testCaseChecked("FUN_1982_0026#3", _AUTHOR)
    # end def test_backlight_mode_changed_from_manual_mode_to_als_mode_after_power_cycle

    @features("Feature1982v3+")
    @features("Feature1803v1")
    @features("Feature1982RequiredOptions", Backlight.SupportedOptionsMask.PWR_SAVE_S)
    @level("Functionality")
    @services("PowerSupply")
    def test_als_off_proximity_off_after_in_critical_battery_level(self):
        """
        Auto_ON_NotPowered: Action-19
        Sensor Power OFF - Disabled by Critical Battery
        Validate ALS and Proximity sensors en_state = OFF while battery level is less than 10%
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable pwrSave = 1 by setBacklightConfig")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=Utils.get_default_options(self) | Backlight.Options.PWR_SAVE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set voltage to enter battery critical level (battery discharging mode)")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.EVENT,
                                    class_type=self.feature_1982.backlight_info_event_cls)
        critical_voltage = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(
            self, UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, "critical"))
        self.power_supply_emulator.set_voltage(critical_voltage)
        # Add delay, to let the device enter into critical battery state
        sleep(6)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait for backlightInfoEvent with backlightStatus = Disabled by critical battery (1)")
        # --------------------------------------------------------------------------------------------------------------
        backlight_info_event = Utils.HIDppHelper.backlight_info_event(self, check_first_message=False)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(
            self, backlight_info_event, Backlight.BacklightStatus.DISABLED_BY_CRITICAL_BATTERY)

        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ALS sensor turned OFF and proximity sensors turned OFF by 0x1803.readGroupOut")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: read GPIO state and check result

        self.testCaseChecked("FUN_1982_0027#1", _AUTHOR)
    # end def test_als_off_proximity_off_after_in_critical_battery_level

    @features("Feature1982v2+")
    @level("Functionality")
    @services('EmulatedKeys', (KEY_ID.BACKLIGHT_DOWN,))
    @services('LedIndicator')
    @services('RequiredLeds', (LED_ID.PROXIMITY_SENSOR_ENABLED, LED_ID.ALS_SENSOR_ENABLED,))
    def test_als_off_proximity_off_after_disabled_backlight_manually(self):
        """
        TempManual_OFF_NotPowered; Action-13
        Sensor Power OFF - Manually disabled (BLL set to Level 0)
        Validate ALS and Proximity sensors en_state = OFF after set BLL to level 0 by backlight button
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press Backlight - button multiple times until backlight level = 0")
        # --------------------------------------------------------------------------------------------------------------
        press_count = Utils.compute_press_count_to_max_or_min_level(self, to_max_level=False)
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_DOWN, repeat=press_count)
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start monitoring PROXIMITY_SENSOR_ENABLED and ALS_SENSOR_ENABLED signals')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self,
                                                                      led_identifiers=[LED_ID.PROXIMITY_SENSOR_ENABLED,
                                                                                       LED_ID.ALS_SENSOR_ENABLED])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, "Check current_level = 0 and backlightStatus = Temporary manual mode (4) by getBcklightInfo")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)
        Utils.GetBacklightInfoResponseChecker.check_current_level(self, get_backlight_info_resp,
                                                                  Backlight.CurrentLevel.CURRENT_LEVEL_0)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.MANUAL_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait measurement duration')
        # --------------------------------------------------------------------------------------------------------------
        backlight_off_measurement_duration_sec = 4
        sleep(backlight_off_measurement_duration_sec)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop  monitoring PROXIMITY_SENSOR_ENABLED and ALS_SENSOR_ENABLED signals')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self,
                                                                     led_identifiers=[LED_ID.PROXIMITY_SENSOR_ENABLED,
                                                                                      LED_ID.ALS_SENSOR_ENABLED])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ALS sensor turned OFF and proximity sensors turned OFF")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
            self, LED_ID.PROXIMITY_SENSOR_ENABLED, minimum_duration=backlight_off_measurement_duration_sec*1000,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
            self, LED_ID.ALS_SENSOR_ENABLED, minimum_duration=backlight_off_measurement_duration_sec*1000,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST, reset=True)

        self.testCaseChecked("FUN_1982_0027#2", _AUTHOR)
    # end def test_als_off_proximity_off_after_disabled_backlight_manually

    @features("Feature1982v2+")
    @features("Rechargeable")
    @level("Functionality")
    @services("HardwareReset")
    @services('LedIndicator')
    @services('RequiredLeds', (LED_ID.PROXIMITY_SENSOR_ENABLED, LED_ID.ALS_SENSOR_ENABLED,))
    def test_als_off_proximity_off_after_plug_usb_cable(self):
        """
        Auto_On_Not_Powered: Action-4
        Sensor Power OFF - USB Charging
        Validate ALS and Proximity sensors en_state = OFF after connected USB charging cable.
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_unplug_usb_charging_cable = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Hardware reset and wait for stable environment')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)
        sleep(8)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start monitoring PROXIMITY_SENSOR_ENABLED signal')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self,
                                                                      led_identifiers=[LED_ID.PROXIMITY_SENSOR_ENABLED,
                                                                                       LED_ID.ALS_SENSOR_ENABLED])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait measurement duration')
        # --------------------------------------------------------------------------------------------------------------
        duration_before_plugging_usb = 2
        sleep(duration_before_plugging_usb)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Plug USB charging cable")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.ChargingHelper.enter_charging_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wait 5 seconds to make sure device updated power stat")
        # --------------------------------------------------------------------------------------------------------------
        usb_plugged_measurement_duration_sec = 5
        sleep(usb_plugged_measurement_duration_sec)
        LogHelper.log_step(self, 'Stop  monitoring PROXIMITY_SENSOR_ENABLED signal')
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self,
                                                                     led_identifiers=[LED_ID.PROXIMITY_SENSOR_ENABLED,
                                                                                      LED_ID.ALS_SENSOR_ENABLED])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ALS sensor turned OFF and proximity sensors turned OFF")
        # --------------------------------------------------------------------------------------------------------------
        # Proximity sensor is ON before plugging in usb
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, LED_ID.PROXIMITY_SENSOR_ENABLED, minimum_duration=duration_before_plugging_usb*1000,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        # Proximity sensor is OFF when usb is plugged
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, LED_ID.PROXIMITY_SENSOR_ENABLED,
                                                                    minimum_duration=usb_plugged_measurement_duration_sec*1000)
        # ALS sensor is OFF during all the test
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
            self, LED_ID.ALS_SENSOR_ENABLED, minimum_duration=(duration_before_plugging_usb+usb_plugged_measurement_duration_sec)*1000,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST, reset=True)

        self.testCaseChecked("FUN_1982_0027#3", _AUTHOR)
    # end def test_als_off_proximity_off_after_plug_usb_cable

    @features("Feature1982v2+")
    @level("Functionality")
    @services('RequiredLeds', (LED_ID.PROXIMITY_SENSOR_ENABLED, LED_ID.ALS_SENSOR_ENABLED,))
    def test_als_on_proximity_on_after_enable_backlight_by_sw(self):
        """
        Auto_On_Not_Powered: Action-5
        Sensor Power ON - Enbled by SW
        Validate ALS and Proximity sensors en_state = ON after enabled backlight by SW
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Backlight.setBacklightConfig with bcklEn = 0")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(
            self, Backlight.Configuration.DISABLE, Utils.get_default_options(self))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start monitoring PROXIMITY_SENSOR_ENABLED and ALS_SENSOR_ENABLED signals')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self,
                                                                      led_identifiers=[LED_ID.PROXIMITY_SENSOR_ENABLED,
                                                                                       LED_ID.ALS_SENSOR_ENABLED])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait backlight Off measurement duration')
        # --------------------------------------------------------------------------------------------------------------
        backlight_disable_measurement_duration_sec = 3
        sleep(backlight_disable_measurement_duration_sec)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Backlight.setBacklightConfig with bcklEn = 1")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(
            self, Backlight.Configuration.ENABLE, Utils.get_default_options(self))  # ~3.6 sec

        sleep(4)    # Time to let backlight enable

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait backlight On measurement duration')
        # --------------------------------------------------------------------------------------------------------------
        backlight_enable_measurement_duration_sec = 70
        end_time = perf_counter() + backlight_enable_measurement_duration_sec

        # Send user action to keep device in power active mode
        while perf_counter() < end_time:
            self.button_stimuli_emulator.user_action()
            sleep(5)
        # end while

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop  monitoring PROXIMITY_SENSOR_ENABLED signal')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self,
                                                                     led_identifiers=[LED_ID.PROXIMITY_SENSOR_ENABLED,
                                                                                      LED_ID.ALS_SENSOR_ENABLED])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check proximity sensor is turned OFF on startup then turned ON")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
            self, LED_ID.PROXIMITY_SENSOR_ENABLED, minimum_duration=backlight_disable_measurement_duration_sec * 1000,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, LED_ID.PROXIMITY_SENSOR_ENABLED, minimum_duration=backlight_enable_measurement_duration_sec * 1000)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ALS sensor is turned OFF on startup then turned ON")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
            self, LED_ID.ALS_SENSOR_ENABLED, minimum_duration=backlight_disable_measurement_duration_sec*1000,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST, reset=True)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, LED_ID.ALS_SENSOR_ENABLED, minimum_duration=300)  # Pulse duration

        self.testCaseChecked("FUN_1982_0028", _AUTHOR)
    # end def test_als_on_proximity_on_after_enable_backlight_by_sw

    @features("Feature1982v2+")
    @level("Functionality")
    @services('EmulatedKeys', (KEY_ID.BACKLIGHT_UP,))
    @services('LedIndicator')
    @services('RequiredLeds', (LED_ID.PROXIMITY_SENSOR_ENABLED, LED_ID.ALS_SENSOR_ENABLED,))
    def test_als_off_proximity_on_in_temporary_manual_mode(self):
        """
        ALS-OFF Proximity-ON - Enter Temporary manual mode
        Validate ALS en_state = OFF and Proximity en_state = ON after pressed backlight keys from Automatic mode
        """
        self.post_requisite_reload_nvs = True

        sleep(4)  # Wait for stable environment

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press backlight + button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_UP)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait backlightInfoEvent then check backlightStatus = Temporary manual mode (4)")
        # --------------------------------------------------------------------------------------------------------------
        backlight_info_event = Utils.HIDppHelper.backlight_info_event(self)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, backlight_info_event,
                                                                     Backlight.BacklightStatus.MANUAL_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start monitoring PROXIMITY_SENSOR_ENABLED and ALS_SENSOR_ENABLED signals')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self,
                                                                      led_identifiers=[LED_ID.PROXIMITY_SENSOR_ENABLED,
                                                                                       LED_ID.ALS_SENSOR_ENABLED])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait measurement duration')
        # --------------------------------------------------------------------------------------------------------------
        temporary_mode_measurement_duration_sec = 8
        sleep(temporary_mode_measurement_duration_sec)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop  monitoring PROXIMITY_SENSOR_ENABLED and ALS_SENSOR_ENABLED signals')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self,
                                                                     led_identifiers=[LED_ID.PROXIMITY_SENSOR_ENABLED,
                                                                                      LED_ID.ALS_SENSOR_ENABLED])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ALS sensor turned OFF and proximity sensors turned ON")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, LED_ID.PROXIMITY_SENSOR_ENABLED, minimum_duration=temporary_mode_measurement_duration_sec*1000,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
            self, LED_ID.ALS_SENSOR_ENABLED, minimum_duration=temporary_mode_measurement_duration_sec*1000,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST, reset=True)

        self.testCaseChecked("FUN_1982_0029#1", _AUTHOR)
    # end def test_als_off_proximity_on_in_temporary_manual_mode

    @features("Feature1982v3+")
    @features("Feature1803v1")
    @level("Functionality")
    def test_als_off_proximity_on_in_permanent_manual_mode(self):
        """
        ALS-OFF Proximity-ON - Enter Permanent manual mode
        Validate ALS en_state = OFF and Proximity en_state = ON after set backlMode to
        Permanent manual mode by SW from Automatic mode
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set bcklMode = Permanent manual mode (3)")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(
            self, Backlight.Configuration.ENABLE,
            Utils.switch_backlight_mode(self, Backlight.Options.PERMANENT_MANUAL_MODE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check backlightStatus = Permanent manual mode (5) by getBacklightInfo")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.PERMANENT_MANUAL_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ALS sensor turned OFF and proximity sensors turned ON by 0x1803.readGroupOut")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
        # TODO: read GPIO state and check result

        self.testCaseChecked("FUN_1982_0029#2", _AUTHOR)
    # end def test_als_off_proximity_on_in_permanent_manual_mode

    @features("Feature1982v3+")
    @level("Functionality")
    @services('EmulatedKeys', (KEY_ID.BACKLIGHT_UP,))
    def test_backlight_mode_stay_in_permanent_manual_mode_after_pressed_backlight_button(self):
        """
        Permanent manual mode (Stay)
        Validate the bcklMode remains unchanged after pressed backlight button in Permanent manual mode
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set bcklMode = Permanent manual mode (3)")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(
            self, Backlight.Configuration.ENABLE,
            Utils.switch_backlight_mode(self, Backlight.Options.PERMANENT_MANUAL_MODE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check backlightStatus = Permanent manual mode (5) by getBacklightInfo")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_info_resp = Utils.HIDppHelper.get_backlight_info(self)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(self, get_backlight_info_resp,
                                                                     Backlight.BacklightStatus.PERMANENT_MANUAL_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press backlight + button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_UP)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait backlightInfoEvent then check backlightStatus = Permanent manual mode (5)")
        # --------------------------------------------------------------------------------------------------------------
        backlight_info_event = Utils.HIDppHelper.backlight_info_event(self)
        Utils.GetBacklightInfoResponseChecker.check_backlight_status(
            self, backlight_info_event, Backlight.BacklightStatus.PERMANENT_MANUAL_MODE)

        self.testCaseChecked("FUN_1982_0030", _AUTHOR)
    # end def test_backlight_mode_stay_in_permanent_manual_mode_after_pressed_backlight_button

    @features("Feature1982v2+")
    @features('Keyboard')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @features("Feature1982RequiredEffect", Backlight.SupportedBacklightEffectMask.REACTION)
    @level("Functionality")
    @services('LedSpyOverI2cMonitoring')
    def test_reaction_backlight_effect_on_japanese_layout_by_backlight_monitoring(self):
        """
        Validate the Reaction Backlight Effect behaviour when japanese layout is configured by backlight monitoring
        """
        self.post_requisite_reload_nvs = True

        fw_id = self.f.PRODUCT.F_ProductReference
        physical_layout = KeyboardMixin.LAYOUT.JIS_109_KEY
        key_ids = list(GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].KEY_ID_TO_LED_ID.keys())
        key_ids_to_not_used = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].BACKLIGHT_EFFECT_FORBIDDEN_KEYS
        key_ids = [ele for ele in key_ids if ele not in key_ids_to_not_used]

        make_duration = ButtonStimuliInterface.DEFAULT_DURATION
        # Need to be greater than REACTION_RAMP_DOWN_KEY_RELEASE_DURATION to take into account the duration of fade out
        # after key release
        break_duration = \
            GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].REACTION_RAMP_DOWN_KEY_RELEASE_DURATION + \
            _REACTION_FADE_OUT_DURATION_MARGIN

        # Create key make and break sequence sorted by delay
        sequence = []
        timestamp = 0
        for key_id in key_ids:
            timestamp += break_duration
            key_id_sequence = [key_id, []]
            key_id_sequence[1].append((MAKE, timestamp))

            timestamp += make_duration
            key_id_sequence[1].append((BREAK, timestamp))

            sequence.append(key_id_sequence)
        # end for
        sequence_sorted_by_delay, max_timestamp = self._sort_sequence_by_delay(sequence)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to JPN")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_keyboard_layout = True
        LayoutTestUtils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.JAPANESE)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setBacklightConfig request with reaction effect')
        # ----------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=Backlight.Options.NONE,
                                               backlight_effect=Backlight.BacklightEffect.REACTION_EFFECT)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start I2C monitoring and play sequence')
        # ----------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        Utils.BacklightSpyHelper.start_monitoring(self)
        self.button_stimuli_emulator.perform_action_list_with_multiple_delays(sequence_sorted_by_delay)
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(timeout=max_timestamp + 10, block=False)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop I2C monitoring when sequence is finished')
        # ----------------------------------------------------------------------------------------------------------
        # Wait reaction sequence is finished with 1 second margin
        sleep(max_timestamp + 1)
        Utils.BacklightSpyHelper.stop_monitoring(self)

        # ------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check reaction effect on single key press')
        # ------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_reaction_effect(self, keys_sequence=sequence, layout_type=physical_layout)

        self.testCaseChecked("FUN_1982_0031", _AUTHOR)
    # end def test_reaction_backlight_effect_on_japanese_layout_by_backlight_monitoring

    @features("Feature1982v2+")
    @features('Keyboard')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @features("Feature1982RequiredEffect", Backlight.SupportedBacklightEffectMask.REACTION)
    @level("Functionality")
    @services('LedSpyOverI2cMonitoring')
    def test_reaction_backlight_effect_on_uk_layout_by_backlight_monitoring(self):
        """
        Validate the Reaction Backlight Effect behaviour when uk layout is configured by backlight monitoring
        """
        self.post_requisite_reload_nvs = True

        fw_id = self.f.PRODUCT.F_ProductReference
        physical_layout = KeyboardMixin.LAYOUT.ISO_105_KEY
        key_ids = list(GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].KEY_ID_TO_LED_ID.keys())
        key_ids_to_not_used = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].BACKLIGHT_EFFECT_FORBIDDEN_KEYS
        key_ids = [ele for ele in key_ids if ele not in key_ids_to_not_used]

        make_duration = ButtonStimuliInterface.DEFAULT_DURATION
        # Need to be greater than REACTION_RAMP_DOWN_KEY_RELEASE_DURATION to take into account the duration of fade out
        # after key release
        break_duration = \
            GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].REACTION_RAMP_DOWN_KEY_RELEASE_DURATION + \
            _REACTION_FADE_OUT_DURATION_MARGIN

        # Create key make and break sequence sorted by delay
        sequence = []
        timestamp = 0
        for key_id in key_ids:
            timestamp += break_duration
            key_id_sequence = [key_id, []]
            key_id_sequence[1].append((MAKE, timestamp))

            timestamp += make_duration
            key_id_sequence[1].append((BREAK, timestamp))

            sequence.append(key_id_sequence)
        # end for
        sequence_sorted_by_delay, max_timestamp = self._sort_sequence_by_delay(sequence)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to UK")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_keyboard_layout = True
        LayoutTestUtils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.UK)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setBacklightConfig request with reaction effect')
        # ----------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=Backlight.Options.NONE,
                                               backlight_effect=Backlight.BacklightEffect.REACTION_EFFECT)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start I2C monitoring and play sequence')
        # ----------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        Utils.BacklightSpyHelper.start_monitoring(self)
        self.button_stimuli_emulator.perform_action_list_with_multiple_delays(sequence_sorted_by_delay)
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(timeout=max_timestamp + 10, block=False)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop I2C monitoring when sequence is finished')
        # ----------------------------------------------------------------------------------------------------------
        # Wait reaction sequence is finished with 1 second margin
        sleep(max_timestamp + 1)
        Utils.BacklightSpyHelper.stop_monitoring(self)

        # ------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check reaction effect on single key press')
        # ------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_reaction_effect(self, keys_sequence=sequence, layout_type=physical_layout)

        self.testCaseChecked("FUN_1982_0032", _AUTHOR)
    # end def test_reaction_backlight_effect_on_uk_layout_by_backlight_monitoring

    @features("Feature1982v2+")
    @features('Keyboard')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @features("Feature1982RequiredEffect", Backlight.SupportedBacklightEffectMask.WAVES)
    @level("Functionality")
    @services('BacklightMonitoring')
    def test_waves_backlight_effect_on_japanese_layout_by_backlight_monitoring(self):
        """
        Validate the Waves Backlight Effect behaviour when japanese layout is configured by backlight monitoring.
        """
        self.post_requisite_reload_nvs = True
        fw_id = self.f.PRODUCT.F_ProductReference
        physical_layout = KeyboardMixin.LAYOUT.JIS_109_KEY
        led_id_to_check = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].LED_ID_AVAILABLE
        backlight_duration_fade_in = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].FADE_IN_DURATION
        backlight_duration_fade_out = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].FADE_OUT_DURATION
        backlight_duration_with_margin = (backlight_duration_fade_in + Utils.INCREMENT_DURATION_HANDS_IN_OUT_OR_POWERED
                                          + backlight_duration_fade_out) * Utils.BACKLIGHT_DURATION_10_PERCENT_MARGIN

        period = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].WAVES_EFFECT_PERIOD
        three_period_duration_with_margin = 3 * period * Utils.BACKLIGHT_DURATION_10_PERCENT_MARGIN

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to JPN")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_keyboard_layout = True
        LayoutTestUtils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.JAPANESE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setBacklightConfig request with waves effect')
        # --------------------------------------------------------------------------------------------------------------
        default_options = Utils.get_default_options(self)
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=Backlight.Options.NONE,
                                               backlight_effect=Backlight.BacklightEffect.WAVES_EFFECT)
        # Wait until the effect is finished
        sleep(backlight_duration_with_margin)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get current backlight level by getBacklightInfo")
        # --------------------------------------------------------------------------------------------------------------
        current_level = to_int(Utils.HIDppHelper.get_backlight_info(self).current_level)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start I2C monitoring')
        # --------------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.start_monitoring(self)
        # Wait 1 second to be able to verify that no effect is played before interacting with the device
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set proximity presence, press key and remove proximity presence")
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        self.proximity_sensor_emulator.set_proximity_presence()
        self.button_stimuli_emulator.user_action()
        self.kosmos.pes.delay(delay_s=(3 * period - backlight_duration_with_margin))
        self.proximity_sensor_emulator.set_proximity_presence(enable=False)
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(block=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Wait {three_period_duration_with_margin}s to monitor 3 period of waves effect")
        # --------------------------------------------------------------------------------------------------------------
        sleep(three_period_duration_with_margin)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop I2C monitoring')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.stop_monitoring(self)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check recording starts with None effect')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(self, effect_type=BacklightEffectType.NONE_EFFECT,
                                                              led_id_to_check=led_id_to_check,
                                                              layout_type=physical_layout)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check the Waves requirements by backlight monitoring on level {current_level}')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(self,
                                                              effect_type=BacklightEffectType.WAVES_EFFECT,
                                                              led_id_to_check=led_id_to_check,
                                                              level=current_level,
                                                              layout_type=physical_layout)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check recording ends with None effect')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(self, effect_type=BacklightEffectType.NONE_EFFECT,
                                                              led_id_to_check=led_id_to_check,
                                                              layout_type=physical_layout)

        self.testCaseChecked("FUN_1982_0033", _AUTHOR)
    # end def test_waves_backlight_effect_on_japanese_layout_by_backlight_monitoring

    @features("Feature1982v2+")
    @features('Keyboard')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @features("Feature1982RequiredEffect", Backlight.SupportedBacklightEffectMask.WAVES)
    @level("Functionality")
    @services('BacklightMonitoring')
    def test_waves_backlight_effect_on_uk_layout_by_backlight_monitoring(self):
        """
        Validate the Waves Backlight Effect behaviour when UK layout is configured by backlight monitoring.
        """
        self.post_requisite_reload_nvs = True
        fw_id = self.f.PRODUCT.F_ProductReference
        physical_layout = KeyboardMixin.LAYOUT.ISO_105_KEY
        led_id_to_check = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].LED_ID_AVAILABLE
        backlight_duration_fade_in = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].FADE_IN_DURATION
        backlight_duration_fade_out = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].FADE_OUT_DURATION
        backlight_duration_with_margin = (backlight_duration_fade_in + Utils.INCREMENT_DURATION_HANDS_IN_OUT_OR_POWERED
                                          + backlight_duration_fade_out) * Utils.BACKLIGHT_DURATION_10_PERCENT_MARGIN

        period = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].WAVES_EFFECT_PERIOD
        three_period_duration_with_margin = 3 * period * Utils.BACKLIGHT_DURATION_10_PERCENT_MARGIN

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to UK")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_keyboard_layout = True
        LayoutTestUtils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.UK)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setBacklightConfig request with waves effect')
        # --------------------------------------------------------------------------------------------------------------
        default_options = Utils.get_default_options(self)
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=Backlight.Options.NONE,
                                               backlight_effect=Backlight.BacklightEffect.WAVES_EFFECT)
        # Wait until the effect is finished
        sleep(backlight_duration_with_margin)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get current backlight level by getBacklightInfo")
        # --------------------------------------------------------------------------------------------------------------
        current_level = to_int(Utils.HIDppHelper.get_backlight_info(self).current_level)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start I2C monitoring')
        # --------------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.start_monitoring(self)
        # Wait 1 second to be able to verify that no effect is played before interacting with the device
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set proximity presence, press key and remove proximity presence")
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        self.proximity_sensor_emulator.set_proximity_presence()
        self.button_stimuli_emulator.user_action()
        self.kosmos.pes.delay(delay_s=(3 * period - backlight_duration_with_margin))
        self.proximity_sensor_emulator.set_proximity_presence(enable=False)
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(block=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Wait {three_period_duration_with_margin}s to monitor 3 period of waves effect")
        # --------------------------------------------------------------------------------------------------------------
        sleep(three_period_duration_with_margin)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop I2C monitoring')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.stop_monitoring(self)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check recording starts with None effect')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(self, effect_type=BacklightEffectType.NONE_EFFECT,
                                                              led_id_to_check=led_id_to_check,
                                                              layout_type=physical_layout)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check the Waves requirements by backlight monitoring on level {current_level}')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(self,
                                                              effect_type=BacklightEffectType.WAVES_EFFECT,
                                                              led_id_to_check=led_id_to_check,
                                                              level=current_level,
                                                              layout_type=physical_layout)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check recording ends with None effect')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(self, effect_type=BacklightEffectType.NONE_EFFECT,
                                                              led_id_to_check=led_id_to_check)

        self.testCaseChecked("FUN_1982_0034", _AUTHOR)
    # end def test_waves_backlight_effect_on_uk_layout_by_backlight_monitoring

    @features("Feature1982v2+")
    @features('Keyboard')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @features("Feature1982RequiredEffect", Backlight.SupportedBacklightEffectMask.CONTRAST)
    @level("Functionality")
    @services('BacklightMonitoring')
    def test_contrast_backlight_effect_on_japanese_layout_by_backlight_monitoring(self):
        """
        Validate the Contrast Backlight Effect behaviour when japanese layout is configured by backlight monitoring.
        """
        self.post_requisite_reload_nvs = True
        fw_id = self.f.PRODUCT.F_ProductReference
        physical_layout = KeyboardMixin.LAYOUT.JIS_109_KEY
        led_id_to_check = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].LED_ID_AVAILABLE
        backlight_duration_fade_in = \
            GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].CONTRAST_FADE_IN_GROUP_KEYS1_DURATION + \
            GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].CONTRAST_DELTA_GROUP_KEYS1_VS_2_DURATION + \
            GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].CONTRAST_FADE_IN_GROUP_KEYS2_DURATION
        backlight_duration_fade_out = \
            GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].CONTRAST_FADE_OUT_DURATION
        backlight_duration_with_margin = (backlight_duration_fade_in + Utils.INCREMENT_DURATION_HANDS_IN_OUT_OR_POWERED
                                          + backlight_duration_fade_out) * Utils.BACKLIGHT_DURATION_10_PERCENT_MARGIN

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to JPN")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_keyboard_layout = True
        LayoutTestUtils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.JAPANESE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setBacklightConfig request with contrast effect')
        # --------------------------------------------------------------------------------------------------------------
        default_options = Utils.get_default_options(self)
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=Backlight.Options.NONE,
                                               backlight_effect=Backlight.BacklightEffect.CONTRAST_EFFECT)
        # Wait until the effect is finished
        sleep(backlight_duration_with_margin)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get current backlight level by getBacklightInfo")
        # --------------------------------------------------------------------------------------------------------------
        current_level = to_int(Utils.HIDppHelper.get_backlight_info(self).current_level)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start I2C monitoring')
        # --------------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.start_monitoring(self)
        # Wait 1 second to be able to verify that no effect is played before interacting with the device
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set proximity presence, press key and remove proximity presence")
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        self.proximity_sensor_emulator.set_proximity_presence()
        self.button_stimuli_emulator.user_action()
        self.proximity_sensor_emulator.set_proximity_presence(enable=False)
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(block=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Wait {backlight_duration_with_margin}s to be sure the effect is finished")
        # --------------------------------------------------------------------------------------------------------------
        sleep(backlight_duration_with_margin)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop I2C monitoring')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.stop_monitoring(self)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check recording starts with None effect')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(self, effect_type=BacklightEffectType.NONE_EFFECT,
                                                              led_id_to_check=led_id_to_check,
                                                              layout_type=physical_layout)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check the Contrast requirements by backlight monitoring on level {current_level}')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.\
            check_backlight_requirements(self,
                                         effect_type=BacklightEffectType.CONTRAST_EFFECT,
                                         led_id_to_check=led_id_to_check,
                                         fade_in_phase_duration=backlight_duration_fade_in,
                                         level=current_level,
                                         fade_out_phase_duration=backlight_duration_fade_out,
                                         layout_type=physical_layout)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check recording ends with None effect')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(self, effect_type=BacklightEffectType.NONE_EFFECT,
                                                              led_id_to_check=led_id_to_check,
                                                              layout_type=physical_layout)

        self.testCaseChecked("FUN_1982_0033", _AUTHOR)
    # end def test_contrast_backlight_effect_on_japanese_layout_by_backlight_monitoring

    @features("Feature1982v2+")
    @features('Keyboard')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @features("Feature1982RequiredEffect", Backlight.SupportedBacklightEffectMask.CONTRAST)
    @level("Functionality")
    @services('BacklightMonitoring')
    def test_contrast_backlight_effect_on_uk_layout_by_backlight_monitoring(self):
        """
        Validate the Contrast Backlight Effect behaviour when UK layout is configured by backlight monitoring.
        """
        self.post_requisite_reload_nvs = True
        fw_id = self.f.PRODUCT.F_ProductReference
        physical_layout = KeyboardMixin.LAYOUT.ISO_105_KEY
        led_id_to_check = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].LED_ID_AVAILABLE
        backlight_duration_fade_in = \
            GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].CONTRAST_FADE_IN_GROUP_KEYS1_DURATION + \
            GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].CONTRAST_DELTA_GROUP_KEYS1_VS_2_DURATION + \
            GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].CONTRAST_FADE_IN_GROUP_KEYS2_DURATION
        backlight_duration_fade_out = \
            GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].CONTRAST_FADE_OUT_DURATION
        backlight_duration_with_margin = (backlight_duration_fade_in + Utils.INCREMENT_DURATION_HANDS_IN_OUT_OR_POWERED
                                          + backlight_duration_fade_out) * Utils.BACKLIGHT_DURATION_10_PERCENT_MARGIN

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to UK")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_keyboard_layout = True
        LayoutTestUtils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.UK)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setBacklightConfig request with waves effect')
        # --------------------------------------------------------------------------------------------------------------
        default_options = Utils.get_default_options(self)
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=Backlight.Options.NONE,
                                               backlight_effect=Backlight.BacklightEffect.CONTRAST_EFFECT)
        # Wait until the effect is finished
        sleep(backlight_duration_with_margin)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get current backlight level by getBacklightInfo")
        # --------------------------------------------------------------------------------------------------------------
        current_level = to_int(Utils.HIDppHelper.get_backlight_info(self).current_level)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start I2C monitoring')
        # --------------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.start_monitoring(self)
        # Wait 1 second to be able to verify that no effect is played before interacting with the device
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set proximity presence, press key and remove proximity presence")
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        self.proximity_sensor_emulator.set_proximity_presence()
        self.button_stimuli_emulator.user_action()
        self.proximity_sensor_emulator.set_proximity_presence(enable=False)
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(block=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Wait {backlight_duration_with_margin}s to be sure the effect is finished")
        # --------------------------------------------------------------------------------------------------------------
        sleep(backlight_duration_with_margin)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop I2C monitoring')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.stop_monitoring(self)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check recording starts with None effect')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(self, effect_type=BacklightEffectType.NONE_EFFECT,
                                                              led_id_to_check=led_id_to_check,
                                                              layout_type=physical_layout)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check the Contrast requirements by backlight monitoring on level {current_level}')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.\
            check_backlight_requirements(self,
                                         effect_type=BacklightEffectType.CONTRAST_EFFECT,
                                         led_id_to_check=led_id_to_check,
                                         fade_in_phase_duration=backlight_duration_fade_in,
                                         level=current_level,
                                         fade_out_phase_duration=backlight_duration_fade_out,
                                         layout_type=physical_layout)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check recording ends with None effect')
        # ----------------------------------------------------------------------------------------------------------
        Utils.BacklightSpyHelper.check_backlight_requirements(self, effect_type=BacklightEffectType.NONE_EFFECT,
                                                              led_id_to_check=led_id_to_check,
                                                              layout_type=physical_layout)

        self.testCaseChecked("FUN_1982_0034", _AUTHOR)
    # end def test_contrast_backlight_effect_on_uk_layout_by_backlight_monitoring

    @features("Feature1982v2+")
    @features('Keyboard')
    @features("Feature1982RequiredEffect", Backlight.SupportedBacklightEffectMask.STATIC)
    @level("Functionality")
    @services('BacklightMonitoring')
    @services('RequiredKeys', (KEY_ID.BACKLIGHT_UP, KEY_ID.BACKLIGHT_DOWN,))
    @bugtracker("Backlight_DurationEffectLevelZeroToOneByMonitoring")
    def test_static_backlight_effect_on_all_level_min_to_max_by_backlight_monitoring(self):
        """
        Validate the Static Backlight Effect behaviour (value and fade in/out) on all the brightness level from
        max to min and min to max by backlight monitoring
        """
        self.post_requisite_reload_nvs = True
        number_of_level = int(self.config.F_NumberOfLevel)
        fw_id = self.f.PRODUCT.F_ProductReference
        physical_layout = KeyboardMixin.LAYOUT.DEFAULT
        led_id_to_check = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].LED_ID_AVAILABLE
        backlight_duration_fade_in = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].FADE_IN_DURATION
        backlight_duration_fade_out = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].FADE_OUT_DURATION
        backlight_duration_with_margin = (backlight_duration_fade_in + Utils.INCREMENT_DURATION_HANDS_IN_OUT_OR_POWERED
                                          + backlight_duration_fade_out) * Utils.BACKLIGHT_DURATION_20_PERCENT_MARGIN

        press_count = Utils.compute_press_count_to_max_or_min_level(self, to_max_level=False)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press backlight - button {press_count} times to the min level")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_DOWN, repeat=press_count)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setBacklightConfig request with static effect')
        # --------------------------------------------------------------------------------------------------------------
        enable_permanent_manual_mode = Utils.get_default_options(self) | Backlight.Options.PERMANENT_MANUAL_MODE
        Utils.HIDppHelper.set_backlight_config(self,
                                               configuration=Backlight.Configuration.ENABLE,
                                               options=enable_permanent_manual_mode,
                                               backlight_effect=Backlight.BacklightEffect.STATIC_EFFECT,
                                               current_backlight_level=0)
        # Wait until the effect is finished
        sleep(backlight_duration_with_margin)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop to check the backlight effect from min to max level by led driver ic spy")
        # --------------------------------------------------------------------------------------------------------------
        for press in range(number_of_level - 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start I2C monitoring')
            # ----------------------------------------------------------------------------------------------------------
            Utils.BacklightSpyHelper.start_monitoring(self)
            # Wait 1 second to be able to verify that no effect is played before interacting with the device
            sleep(1)

            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Press backlight + button ")
            # --------------------------------------------------------------------------------------------------------------
            self.kosmos.sequencer.offline_mode = True
            self.proximity_sensor_emulator.set_proximity_presence()
            self.button_stimuli_emulator.keystroke(KEY_ID.BACKLIGHT_UP)
            self.proximity_sensor_emulator.set_proximity_presence(enable=False)
            self.kosmos.sequencer.offline_mode = False
            self.kosmos.sequencer.play_sequence(block=False)

            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Wait {backlight_duration_with_margin}s to be sure the effect is finished")
            # --------------------------------------------------------------------------------------------------------------
            sleep(backlight_duration_with_margin)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop I2C monitoring')
            # ----------------------------------------------------------------------------------------------------------
            Utils.BacklightSpyHelper.stop_monitoring(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check recording starts with None effect')
            # ----------------------------------------------------------------------------------------------------------
            Utils.BacklightSpyHelper.check_backlight_requirements(self, effect_type=BacklightEffectType.NONE_EFFECT,
                                                                  led_id_to_check=led_id_to_check)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the Static requirements by the LED Driver IC Spy')
            # ----------------------------------------------------------------------------------------------------------
            level_pwm_value = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].LEVEL_PWM_VALUE[press + 1]
            max_pwm_value = GET_BACKLIGHT_CONFIGURATION_BY_ID[fw_id][physical_layout].MAX_PWM_VALUE
            duration_fade_in_by_level = backlight_duration_fade_in * level_pwm_value / max_pwm_value
            duration_fade_out_by_level = backlight_duration_fade_out * level_pwm_value / max_pwm_value

            Utils.BacklightSpyHelper.check_backlight_requirements(self,
                                                                  effect_type=BacklightEffectType.STATIC_EFFECT,
                                                                  led_id_to_check=led_id_to_check,
                                                                  fade_in_phase_duration=duration_fade_in_by_level,
                                                                  level=press + 1,
                                                                  fade_out_phase_duration=duration_fade_out_by_level)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check recording ends with None effect')
            # ----------------------------------------------------------------------------------------------------------
            Utils.BacklightSpyHelper.check_backlight_requirements(self, effect_type=BacklightEffectType.NONE_EFFECT,
                                                                  led_id_to_check=led_id_to_check)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_1982_0035", _AUTHOR)
    # end def test_static_backlight_effect_on_all_level_min_to_max_by_backlight_monitoring
# end class BacklightFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
