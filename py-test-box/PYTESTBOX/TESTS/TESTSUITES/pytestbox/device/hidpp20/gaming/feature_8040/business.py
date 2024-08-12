#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.gaming.feature_8040.business
:brief: HID++ 2.0 ``BrightnessControl`` business test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2023/11/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import time
from time import sleep
from random import choice

from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.unifiedbattery import UnifiedBattery
from pyhid.hidpp.features.gaming.brightnesscontrol import CapabilitiesV1
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagement
from pyhid.hidpp.features.gaming.rgbeffects import RGBEffects
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.fkcprofileformat import TagField_1_Byte
from pylibrary.mcu.fkcprofileformat import TagField_11_Bytes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pyraspi.services.kosmos.config.rgbconfiguration import GET_RGB_CONFIGURATION_BY_ID
from pyraspi.services.kosmos.module.devicetree import DeviceFamilyName
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.base.protocolmanagerutils import ProtocolManagerUtils
from pytestbox.device.base.brightnesscontrolutils import BrightnessControlTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.base.profilemanagementutils import ProfileManagementTestUtils
from pytestbox.device.base.rgbeffectsutils import RGBEffectsTestUtils
from pytestbox.device.base.unifiedbatteryutils import UnifiedBatteryTestUtils
from pytestbox.device.hidpp20.gaming.feature_8040.brightnesscontrol import BrightnessControlTestCase
from pytestbox.device.hidpp20.gaming.feature_8101.profilemanagement import ProfileManagementTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"
STARTUP_DURATION_MARGIN = 1
DIMMING_OFF_TIMEOUT_MARGIN = 2


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BrightnessControlBusinessTestCase(BrightnessControlTestCase):
    """
    Validate ``BrightnessControl`` business test cases
    """

    @features("Feature8040")
    @features("Feature8071")
    @features("Feature8101")
    @level("Business")
    @services("RGBMonitoring")
    def test_passive_animation_dimmed_down_before_deep_sleep(self):
        """
        Verify brightness of 'Passive' animation to be dimmed down linearly to 0 for the last 30 seconds before going
        to deep sleep
        """
        self.post_requisite_reload_nvs = True
        _, feature_8071, _, _ = RGBEffectsTestUtils.HIDppHelper.get_parameters(self)
        effect_dict = feature_8071.get_effect_dictionary()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an onboard profile and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Change the active RGB color effect of the cluster"
                                 f"{RGBEffectsTestUtils.RGBClusterId.PRIMARY!s} to "
                                 f"{RGBEffects.RGBEffectID.FIXED!s}.")
        # --------------------------------------------------------------------------------------------------------------
        profile.tag_fields[ProfileManagement.Tag.ACTIVE_CLUSTER_0_EFFECT].setValue(
            fid=TagField_11_Bytes.FID.DATA,
            value=effect_dict[RGBEffects.RGBEffectID.FIXED](red=0xFF, green=0xFF, blue=0xFF).params)
        profile.tag_fields[ProfileManagement.Tag.ACTIVE_CLUSTER_1_EFFECT].setValue(
            fid=TagField_11_Bytes.FID.DATA,
            value=effect_dict[RGBEffects.RGBEffectID.FIXED](red=0xFF, green=0xFF, blue=0xFF).params)
        profile.tag_fields[ProfileManagement.Tag.PASSIVE_CLUSTER_0_EFFECT].setValue(
            fid=TagField_11_Bytes.FID.DATA,
            value=effect_dict[RGBEffects.RGBEffectID.FIXED](red=0xFF, green=0xFF, blue=0xFF).params)
        profile.tag_fields[ProfileManagement.Tag.PASSIVE_CLUSTER_1_EFFECT].setValue(
            fid=TagField_11_Bytes.FID.DATA,
            value=effect_dict[RGBEffects.RGBEffectID.FIXED](red=0xFF, green=0xFF, blue=0xFF).params)
        profile.tag_fields[ProfileManagement.Tag.LIGHTING_FLAG].setValue(
            fid=TagField_1_Byte.FID.DATA,
            value=0)
        profile.crc_32 = directory.update_file(file_id_lsb=profile.file_id_lsb,
                                               table_in_hexlist=HexList(profile))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write 0x8101 profile to RAM\n{profile}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                         store_in_nvs=True,
                                         first_sector_id_lsb=profile.first_sector_id_lsb,
                                         crc_32=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Update the directory and save in the NVS\n{directory}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory),
                                         store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={ProfileManagement.Partition.FileId.RAM}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                            file_id=profile.file_id_lsb,
                                            count=len(HexList(profile)),
                                            crc_32=profile.crc_32)
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform an user action and start ticking the elapsed time before deep sleep")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        init_time = time()
        elapsed_time = 0
        dimming_duration = 30
        start_dimming_time = 0
        start_dimming = False
        dimming_brightness = self.config.F_MaxBrightness
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop: elapsed_time in range("
                                 f"{self.f.PRODUCT.DEVICE.F_MaxWaitDeepSleep + self.f.PRODUCT.DEVICE.F_MaxWaitSleep})")
        # --------------------------------------------------------------------------------------------------------------
        while elapsed_time < (self.f.PRODUCT.DEVICE.F_MaxWaitDeepSleep + self.f.PRODUCT.DEVICE.F_MaxWaitSleep):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check the brightness is not decreasing/is decreasing when the {elapsed_time}"
                                      "less or equals/higher than "
                                      f"{self.f.PRODUCT.DEVICE.F_MaxWaitDeepSleep - dimming_duration}")
            # ----------------------------------------------------------------------------------------------------------
            if elapsed_time > (self.f.PRODUCT.DEVICE.F_MaxWaitDeepSleep - dimming_duration):
                RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)
                sleep(1)
                RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)
                elapsed_time = time() - init_time
                try:
                    dimming_brightness = \
                        ((dimming_duration - (elapsed_time - start_dimming_time)) / dimming_duration) * \
                        self.config.F_MaxBrightness if start_dimming else self.config.F_MaxBrightness
                    RGBEffectsTestUtils.RgbSpyHelper.check_fixed_effect(
                        test_case=self, red_value=0xFF, green_value=0xFF, blue_value=0xFF,
                        brightness=int(dimming_brightness),
                        check_last_packet_only=True,
                        calibration_data=self.calibration_data,
                        cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)
                    if not start_dimming:
                        start_dimming_time = elapsed_time - 1  # The duration time of first dimming shall be counted
                        start_dimming = True
                    # end if
                except AssertionError:
                    if start_dimming:
                        if int(dimming_brightness) <= 0:
                            break
                        else:
                            self.assertAlmostEqual(first=dimming_brightness,
                                                   second=self.config.F_MinBrightness,
                                                   delta=1)
                        # end if
                    # end if
                # end try
            # end if
            elapsed_time = time() - init_time
        # end while
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_8040_0001", _AUTHOR)
    # end def test_passive_animation_dimmed_down_before_deep_sleep

    @features("Feature8040")
    @features("HasRGBConfiguration")
    @level("Business")
    @bugtracker('BrightnessNotPersistence')
    def test_brightness_persistence_after_power_cycle(self):
        """
        When in onboard mode, check the immersive lighting brightness to persist/reset across power cycles

        NB: If transient is set, the settings shall be reset, otherwise persistence.
        """
        self.post_requisite_reload_nvs = True
        pre_define_brightness_levels = list(self.config.F_PreDefineBrightnessLevels)
        pre_define_brightness_levels.remove(str(self.config.F_DefaultBrightness))
        new_brightness = int(choice(pre_define_brightness_levels))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setBrightness request to change the brightness a non-default value")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.set_brightness(test_case=self, brightness=new_brightness)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power OFF -> ON the DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getBrightness request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_brightness(test_case=self)

        transient = HexList(self.config.F_Capabilities).testBit(CapabilitiesV1.POS.TRANSIENT)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self,
                            f"Check the brightness is {'reset' if transient else 'persistence'} "
                            "from the response of getBrightness")
        # --------------------------------------------------------------------------------------------------------------
        checker = BrightnessControlTestUtils.GetBrightnessResponseChecker
        check_map = checker.get_check_map(brightness=self.config.F_DefaultBrightness if transient else new_brightness)
        checker.check_fields(test_case=self, message=response,
                             expected_cls=self.feature_8040.get_brightness_response_cls, check_map=check_map)

        if self.kosmos.discover_emulator(emulation_type=DeviceFamilyName.GENERIC_LED_SPY) and \
                (RGBEffects.RGBEffectID.FIXED in RGBEffectsTestUtils.get_supported_effect_ids_by_cluster(
                    test_case=self, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the brightness is persistence from the result of LED Spy/Monitoring")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.set_fix_effect_and_check_result_from_rgb_monitoring(
                test_case=self, brightness=self.config.F_DefaultBrightness if transient else new_brightness)
        # end if

        self.testCaseChecked("BUS_8040_0002", _AUTHOR)
    # end def test_brightness_persistence_after_power_cycle

    @features("Feature8040")
    @features("Feature1830")
    @features("HasRGBConfiguration")
    @level("Business")
    def test_brightness_persistence_after_deep_sleep(self):
        """
        When in onboard mode, check the immersive lighting brightness to persist/reset when resuming from deep sleep

        NB: If transient is set, the settings shall be reset, otherwise persistence.
        """
        self.post_requisite_reload_nvs = True
        pre_define_brightness_levels = list(self.config.F_PreDefineBrightnessLevels)
        pre_define_brightness_levels.remove(str(self.config.F_DefaultBrightness))
        new_brightness = int(choice(pre_define_brightness_levels))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setBrightness request to change the brightness a non-default value")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.set_brightness(test_case=self, brightness=new_brightness)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send 0x1830.SetPowerMode with PowerModeNum=3(deep-sleep)")
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform an user action to wake-up the DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getBrightness request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_brightness(test_case=self)

        transient = HexList(self.config.F_Capabilities).testBit(CapabilitiesV1.POS.TRANSIENT)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self,
                            f"Check the brightness is {'reset' if transient else 'persistence'} "
                            "from the response of getBrightness")
        # --------------------------------------------------------------------------------------------------------------
        checker = BrightnessControlTestUtils.GetBrightnessResponseChecker
        check_map = checker.get_check_map(brightness=self.config.F_DefaultBrightness if transient else new_brightness)
        checker.check_fields(test_case=self, message=response,
                             expected_cls=self.feature_8040.get_brightness_response_cls, check_map=check_map)

        if self.kosmos.discover_emulator(emulation_type=DeviceFamilyName.GENERIC_LED_SPY) and \
                (RGBEffects.RGBEffectID.FIXED in RGBEffectsTestUtils.get_supported_effect_ids_by_cluster(
                    test_case=self, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the brightness is persistence from the result of LED Spy/Monitoring")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.set_fix_effect_and_check_result_from_rgb_monitoring(
                test_case=self, brightness=self.config.F_DefaultBrightness if transient else new_brightness)
        # end if

        self.testCaseChecked("BUS_8040_0003", _AUTHOR)
    # end def test_brightness_persistence_after_deep_sleep

    @features("Feature8040")
    @features("Feature8071")
    @features("Keyboard")
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.HW_BRIGHTNESS)
    @level("Business")
    @services('AtLeastOneKey', (KEY_ID.BACKLIGHT_UP, KEY_ID.BACKLIGHT_DOWN,
                                KEY_ID.BRIGHTNESS_UP, KEY_ID.BRIGHTNESS_DOWN, KEY_ID.DIMMING_KEY))
    def test_adjust_brightness_via_physical_button_in_all_power_mode(self):
        """
        When in onboard mode, check that the keyboard supports physical button(s) for controlling the brightness

        This test case shall also be tested under the following power modes:
        - Run Mode (Power Mode) #1
        - Walk Mode (Power Mode) #1
        - Sleep Mode (Power Mode) #1
        - Deep Sleep Mode (Power Mode) #1
        """
        self.post_requisite_reload_nvs = True
        power_modes = ['run_mode', 'walk_mode', 'sleep_mode', 'deep_sleep_mode']
        brightness_controls = BrightnessControlTestUtils.get_standard_physical_brightness_controls(test_case=self)
        fn_brightness_controls = \
            BrightnessControlTestUtils.get_functional_physical_brightness_controls(test_case=self)
        controls = fn_brightness_controls if len(fn_brightness_controls) > 0 else brightness_controls
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait the necessary duration to be sure startup animation is finished')
        # --------------------------------------------------------------------------------------------------------------
        fw_id = self.f.PRODUCT.F_ProductReference
        sleep(GET_RGB_CONFIGURATION_BY_ID[fw_id].STARTUP_DURATION + STARTUP_DURATION_MARGIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self,
                            f"Set the brightness to {self.config.F_MaxBrightness} and check the brightness is "
                            "as expected from the result of LED Spy/Monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.set_fix_effect_and_check_result_from_rgb_monitoring(
            test_case=self, brightness=self.config.F_MaxBrightness, calibration_data=self.calibration_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over {power_modes}")
        # --------------------------------------------------------------------------------------------------------------
        for power_mode in power_modes:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send setBrightness request with brightness={self.config.F_MaxBrightness}")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.HIDppHelper.set_brightness(test_case=self,
                                                                  brightness=self.config.F_MaxBrightness)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Test Loop: brightness in range({self.config.F_Steps - 1})")
            # ----------------------------------------------------------------------------------------------------------
            for _ in range(self.config.F_Steps - 1):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Get the current brightness from the DUT")
                # ------------------------------------------------------------------------------------------------------
                current_brightness = \
                    to_int(BrightnessControlTestUtils.HIDppHelper.get_brightness(test_case=self).brightness)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"Make the device into power mode: {power_mode}")
                # ------------------------------------------------------------------------------------------------------
                self._test_enter_specified_power_mode(power_mode=power_mode)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "Press shortcut to decrease the brightness then check the result")
                # ------------------------------------------------------------------------------------------------------
                self._test_adjust_brightness_via_physical_button(increase_brightness=False,
                                                                 current_brightness=current_brightness,
                                                                 calibration_data=self.calibration_data,
                                                                 check_fix_effect=power_mode != 'deep_sleep_mode')
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        if len({KEY_ID.BACKLIGHT_UP, KEY_ID.BRIGHTNESS_UP}.intersection(set(controls))) > 0:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self,
                                f"Set the brightness to {self.config.F_MaxBrightness} and check the brightness is "
                                "as expected from the result of LED Spy/Monitoring")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.set_fix_effect_and_check_result_from_rgb_monitoring(
                test_case=self, brightness=self.config.F_MaxBrightness, calibration_data=self.calibration_data)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Test Loop: Loop over {power_modes}")
            # ----------------------------------------------------------------------------------------------------------
            for power_mode in power_modes:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send setBrightness request with brightness={self.config.F_MinBrightness}")
                # ------------------------------------------------------------------------------------------------------
                BrightnessControlTestUtils.HIDppHelper.set_brightness(test_case=self,
                                                                      brightness=self.config.F_MinBrightness)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"Test Loop: brightness in range({self.config.F_Steps - 1})")
                # ------------------------------------------------------------------------------------------------------
                for _ in range(self.config.F_Steps - 1):
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_info(self, f"Make the device into power mode: {power_mode}")
                    # --------------------------------------------------------------------------------------------------
                    self._test_enter_specified_power_mode(power_mode=power_mode)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_info(self, "Press shortcut to increase the brightness then check the result")
                    # --------------------------------------------------------------------------------------------------
                    self._test_adjust_brightness_via_physical_button(increase_brightness=True,
                                                                     calibration_data=self.calibration_data,
                                                                     check_fix_effect=power_mode != 'deep_sleep_mode')
                # end for
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "End Test Loop")
                # ------------------------------------------------------------------------------------------------------
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end if

        self.testCaseChecked("BUS_8040_0004#1", _AUTHOR)
    # end def test_adjust_brightness_via_physical_button_in_all_power_mode

    @features("Feature8040")
    @features("Feature8071")
    @features("Keyboard")
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.HW_BRIGHTNESS)
    @level("Business")
    @services("PowerSupply")
    @services('AtLeastOneKey', (KEY_ID.BACKLIGHT_UP, KEY_ID.BACKLIGHT_DOWN,
                                KEY_ID.BRIGHTNESS_UP, KEY_ID.BRIGHTNESS_DOWN, KEY_ID.DIMMING_KEY))
    def test_adjust_brightness_via_physical_button_in_all_battery_level(self):
        """
        When in onboard mode, check that the keyboard supports physical button(s) for controlling the brightness

        e.g. FN+X -> Decrease brightness
        e.g. FN+Z -> Increase brightness

        This test case shall also be tested under the following battery levels:
        - Full (Battery Level) #2
        - Good (Battery Level) #2
        - Low (Battery Level) #2
        - Critical (Battery Level) #2
        """
        self.post_requisite_reload_nvs = True
        battery_levels = UnifiedBattery.BATTERY_LEVELS_V0ToV5
        brightness_controls = BrightnessControlTestUtils.get_standard_physical_brightness_controls(test_case=self)
        fn_brightness_controls = \
            BrightnessControlTestUtils.get_functional_physical_brightness_controls(test_case=self)
        controls = fn_brightness_controls if len(fn_brightness_controls) > 0 else brightness_controls
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over {battery_levels}")
        # --------------------------------------------------------------------------------------------------------------
        for index, battery_level in enumerate(battery_levels):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Make the device into battery level: {battery_level}")
            # ----------------------------------------------------------------------------------------------------------
            state_of_charge = int(self.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_SupportedLevels[index])
            battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, state_of_charge)
            self.reset(hardware_reset=True, starting_voltage=battery_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait the necessary duration to be sure startup animation is finished')
            # ----------------------------------------------------------------------------------------------------------
            fw_id = self.f.PRODUCT.F_ProductReference
            sleep(GET_RGB_CONFIGURATION_BY_ID[fw_id].STARTUP_DURATION + STARTUP_DURATION_MARGIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send setBrightness request with brightness={self.config.F_MaxBrightness}")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.HIDppHelper.set_brightness(test_case=self,
                                                                  brightness=self.config.F_MaxBrightness)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self,
                                f"Set the brightness to {self.config.F_MaxBrightness} and check the brightness is "
                                "as expected from the result of LED Spy/Monitoring")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.set_fix_effect_and_check_result_from_rgb_monitoring(
                test_case=self, brightness=self.config.F_MaxBrightness, calibration_data=self.calibration_data)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Test Loop: brightness in range({self.config.F_Steps - 1})")
            # ----------------------------------------------------------------------------------------------------------
            for _ in range(self.config.F_Steps - 1):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "Press shortcut to decrease the brightness then check the result")
                # ------------------------------------------------------------------------------------------------------
                self._test_adjust_brightness_via_physical_button(increase_brightness=False,
                                                                 calibration_data=self.calibration_data)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        if len({KEY_ID.BACKLIGHT_UP, KEY_ID.BRIGHTNESS_UP}.intersection(set(controls))) > 0:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Test Loop: Loop over {battery_levels}")
            # ----------------------------------------------------------------------------------------------------------
            for index, battery_level in enumerate(battery_levels):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Make the device into battery level: {battery_level}")
                # ------------------------------------------------------------------------------------------------------
                state_of_charge = int(self.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_SupportedLevels[index])
                battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, state_of_charge)
                self.reset(hardware_reset=True, starting_voltage=battery_value)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Wait the necessary duration to be sure startup animation is finished')
                # ------------------------------------------------------------------------------------------------------
                fw_id = self.f.PRODUCT.F_ProductReference
                sleep(GET_RGB_CONFIGURATION_BY_ID[fw_id].STARTUP_DURATION + STARTUP_DURATION_MARGIN)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send setBrightness request with brightness={self.config.F_MaxBrightness}")
                # ------------------------------------------------------------------------------------------------------
                BrightnessControlTestUtils.HIDppHelper.set_brightness(test_case=self,
                                                                      brightness=self.config.F_MaxBrightness)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self,
                                    f"Set the brightness to {self.config.F_MaxBrightness} and check the brightness is "
                                    "as expected from the result of LED Spy/Monitoring")
                # ------------------------------------------------------------------------------------------------------
                BrightnessControlTestUtils.set_fix_effect_and_check_result_from_rgb_monitoring(
                    test_case=self, brightness=self.config.F_MaxBrightness, calibration_data=self.calibration_data)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"Test Loop: brightness in range({self.config.F_Steps - 1})")
                # ------------------------------------------------------------------------------------------------------
                for _ in range(self.config.F_Steps - 1):
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_info(self, "Press shortcut to increase the brightness then check the result")
                    # --------------------------------------------------------------------------------------------------
                    self._test_adjust_brightness_via_physical_button(increase_brightness=True,
                                                                     calibration_data=self.calibration_data)
                # end for
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "End Test Loop")
                # ------------------------------------------------------------------------------------------------------
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end if

        self.testCaseChecked("BUS_8040_0004#2", _AUTHOR)
    # end def test_adjust_brightness_via_physical_button_in_all_battery_level

    @features("Feature8040")
    @features("Feature8071")
    @features("Keyboard")
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.HW_BRIGHTNESS)
    @level("Business")
    @services('AtLeastOneKey', (KEY_ID.BACKLIGHT_UP, KEY_ID.BACKLIGHT_DOWN,
                                KEY_ID.BRIGHTNESS_UP, KEY_ID.BRIGHTNESS_DOWN, KEY_ID.DIMMING_KEY))
    def test_adjust_brightness_via_physical_button_in_all_charging_status(self):
        """
        When in onboard mode, check that the keyboard supports physical button(s) for controlling the brightness

        e.g. FN+X -> Decrease brightness
        e.g. FN+Z -> Increase brightness

        This test case shall also be tested under the following charging modes:
        - Wired charging (Charging Mode) #3
        - Wireless charging (Charging Mode) #3
        - Wireless Powered (NRWP devices) #3
        """
        self.post_requisite_reload_nvs = True
        charging_statuses = ['wired_charging', 'wireless_charging', 'wireless_powered']
        brightness_controls = BrightnessControlTestUtils.get_standard_physical_brightness_controls(test_case=self)
        fn_brightness_controls = \
            BrightnessControlTestUtils.get_functional_physical_brightness_controls(test_case=self)
        controls = fn_brightness_controls if len(fn_brightness_controls) > 0 else brightness_controls
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over {charging_statuses}")
        # --------------------------------------------------------------------------------------------------------------
        for charging_status in charging_statuses:
            if self._test_enter_specified_charging_power_status(charging_status=charging_status):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Entered {charging_status}")
                # ------------------------------------------------------------------------------------------------------
            else:
                continue
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send setBrightness request with brightness={self.config.F_MaxBrightness}")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.HIDppHelper.set_brightness(test_case=self,
                                                                  brightness=self.config.F_MaxBrightness)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self,
                                f"Set the brightness to {self.config.F_MaxBrightness} and check the brightness is "
                                "as expected from the result of LED Spy/Monitoring")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.set_fix_effect_and_check_result_from_rgb_monitoring(
                test_case=self, brightness=self.config.F_MaxBrightness, calibration_data=self.calibration_data)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Test Loop: brightness in range({self.config.F_Steps - 1})")
            # ----------------------------------------------------------------------------------------------------------
            for _ in range(self.config.F_Steps - 1):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "Press shortcut to decrease the brightness then check the result")
                # ------------------------------------------------------------------------------------------------------
                self._test_adjust_brightness_via_physical_button(increase_brightness=False,
                                                                 calibration_data=self.calibration_data)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Disable {charging_status}")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.ChargingHelper.exit_charging_mode(test_case=self, source=self.external_power_source)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        if len({KEY_ID.BACKLIGHT_UP, KEY_ID.BRIGHTNESS_UP}.intersection(set(controls))) > 0:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Test Loop: Loop over {charging_statuses}")
            # ----------------------------------------------------------------------------------------------------------
            for charging_status in charging_statuses:
                if self._test_enter_specified_charging_power_status(charging_status=charging_status):
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f"Entered {charging_status}")
                    # --------------------------------------------------------------------------------------------------
                else:
                    continue
                # end if

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send setBrightness request with brightness={self.config.F_MinBrightness}")
                # ------------------------------------------------------------------------------------------------------
                BrightnessControlTestUtils.HIDppHelper.set_brightness(test_case=self,
                                                                      brightness=self.config.F_MinBrightness)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self,
                                    f"Set the brightness to {self.config.F_MaxBrightness} and check the brightness is "
                                    "as expected from the result of LED Spy/Monitoring")
                # ------------------------------------------------------------------------------------------------------
                BrightnessControlTestUtils.set_fix_effect_and_check_result_from_rgb_monitoring(
                    test_case=self, brightness=self.config.F_MaxBrightness, calibration_data=self.calibration_data)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"Test Loop: brightness in range({self.config.F_Steps - 1})")
                # ------------------------------------------------------------------------------------------------------
                for index in range(self.config.F_Steps - 1):
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_info(self, "Press shortcut to increase the brightness then check the result")
                    # --------------------------------------------------------------------------------------------------
                    self._test_adjust_brightness_via_physical_button(increase_brightness=True,
                                                                     calibration_data=self.calibration_data)
                # end for
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "End Test Loop")
                # ------------------------------------------------------------------------------------------------------
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Disable {charging_status}")
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.ChargingHelper.exit_charging_mode(test_case=self, source=self.external_power_source)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end if

        self.testCaseChecked("BUS_8040_0004#3", _AUTHOR)
    # end def test_adjust_brightness_via_physical_button_in_all_charging_status

    @features("Feature8040")
    @features("Feature8071")
    @features("Keyboard")
    @features("60PercentKeyboard")
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.HW_BRIGHTNESS)
    @level("Business")
    @services('AtLeastOneKey', (KEY_ID.BACKLIGHT_UP, KEY_ID.BACKLIGHT_DOWN,
                                KEY_ID.BRIGHTNESS_UP, KEY_ID.BRIGHTNESS_DOWN, KEY_ID.DIMMING_KEY))
    def test_five_brightness_levels_are_defined_on_60_percent_keyboards_in_all_power_mode(self):
        """
        In OOB state, check that there are FIVE different brightness levels can be selected

        This test case shall also be tested under the following power modes:
        - Run Mode (Power Mode) #1
        - Walk Mode (Power Mode) #1
        - Sleep Mode (Power Mode) #1
        - Deep Sleep Mode (Power Mode) #1
        """
        self.post_requisite_reload_nvs = True
        power_modes = ['run_mode', 'walk_mode', 'sleep_mode', 'deep_sleep_mode']
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getInfo request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_info(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the steps capability is 5 from the response of getInfo")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(to_int(response.steps), 5, msg="The supported brightness steps on a 60% keyboard is 5.")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self,
                            f"Set the brightness to {self.config.F_MaxBrightness} and check the brightness is "
                            "as expected from the result of LED Spy/Monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.set_fix_effect_and_check_result_from_rgb_monitoring(
            test_case=self, brightness=self.config.F_MaxBrightness, calibration_data=self.calibration_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over {power_modes}")
        # --------------------------------------------------------------------------------------------------------------
        for power_mode in power_modes:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send setBrightness request with brightness={self.config.F_MaxBrightness}")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.HIDppHelper.set_brightness(test_case=self,
                                                                  brightness=self.config.F_MaxBrightness)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop: brightness in range(5 - 1)")
            # ----------------------------------------------------------------------------------------------------------
            # There are only 4 intervals between 5 brightness levels
            for _ in range(5 - 1):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"Make the device into power mode: {power_mode}")
                # ------------------------------------------------------------------------------------------------------
                self._test_enter_specified_power_mode(power_mode=power_mode)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "Press the brightness adjustment button to change the brightness")
                # ------------------------------------------------------------------------------------------------------
                self._test_adjust_brightness_via_physical_button(
                    increase_brightness=False,
                    calibration_data=self.calibration_data,
                    check_fix_effect=power_mode != 'deep_sleep_mode')
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send getBrightness request")
            # ----------------------------------------------------------------------------------------------------------
            response = BrightnessControlTestUtils.HIDppHelper.get_brightness(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the brightness matches the MaxBrightness supported on the device")
            # ----------------------------------------------------------------------------------------------------------
            checker = BrightnessControlTestUtils.GetBrightnessResponseChecker
            check_map = checker.get_check_map(brightness=self.config.F_MaxBrightness)
            checker.check_fields(test_case=self, message=response,
                                 expected_cls=self.feature_8040.get_brightness_response_cls, check_map=check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_8040_0005#1", _AUTHOR)
    # end def test_five_brightness_levels_are_defined_on_60_percent_keyboards_in_all_power_mode

    @features("Feature8040")
    @features("Feature8071")
    @features("Keyboard")
    @features("60PercentKeyboard")
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.HW_BRIGHTNESS)
    @level("Business")
    @services("PowerSupply")
    @services('AtLeastOneKey', (KEY_ID.BACKLIGHT_UP, KEY_ID.BACKLIGHT_DOWN,
                                KEY_ID.BRIGHTNESS_UP, KEY_ID.BRIGHTNESS_DOWN, KEY_ID.DIMMING_KEY))
    def test_five_brightness_levels_are_defined_on_60_percent_keyboards_in_all_battery_levels(self):
        """
        In OOB state, check that there are FIVE different brightness levels can be selected

        This test case shall also be tested under the following battery levels:
        - Full (Battery Level) #2
        - Good (Battery Level) #2
        - Low (Battery Level) #2
        - Critical (Battery Level) #2
        """
        brightness_controls = BrightnessControlTestUtils.get_standard_physical_brightness_controls(test_case=self)
        brightness_control = KEY_ID.DIMMING_KEY if KEY_ID.DIMMING_KEY in brightness_controls else KEY_ID.BACKLIGHT_UP
        self.post_requisite_reload_nvs = True
        battery_levels = UnifiedBattery.BATTERY_LEVELS_V0ToV5
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getInfo request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_info(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the steps capability is 5 from the response of getInfo")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(to_int(response.steps), 5, msg="The supported brightness steps on a 60% keyboard is 5.")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over {battery_levels}")
        # --------------------------------------------------------------------------------------------------------------
        for index, battery_level in enumerate(battery_levels):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Make the device into battery level: {battery_level}")
            # ----------------------------------------------------------------------------------------------------------
            state_of_charge = int(self.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_SupportedLevels[index])
            battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, state_of_charge)
            self.reset(hardware_reset=True, starting_voltage=battery_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait the necessary duration to be sure startup animation is finished')
            # ----------------------------------------------------------------------------------------------------------
            fw_id = self.f.PRODUCT.F_ProductReference
            sleep(GET_RGB_CONFIGURATION_BY_ID[fw_id].STARTUP_DURATION + STARTUP_DURATION_MARGIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send setBrightness request with brightness={self.config.F_MaxBrightness}")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.HIDppHelper.set_brightness(test_case=self,
                                                                  brightness=self.config.F_MaxBrightness)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self,
                                f"Set the brightness to {self.config.F_MaxBrightness} and check the brightness is "
                                "as expected from the result of LED Spy/Monitoring")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.set_fix_effect_and_check_result_from_rgb_monitoring(
                test_case=self, brightness=self.config.F_MaxBrightness, calibration_data=self.calibration_data)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop: brightness in range(5 - 1)")
            # ----------------------------------------------------------------------------------------------------------
            # There are only 4 intervals between 5 brightness levels
            for _ in range(5 - 1):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "Press the brightness adjustment button to change the brightness")
                # ------------------------------------------------------------------------------------------------------
                self._test_adjust_brightness_via_physical_button(increase_brightness=False,
                                                                 brightness_control=brightness_control,
                                                                 calibration_data=self.calibration_data)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send getBrightness request")
            # ----------------------------------------------------------------------------------------------------------
            response = BrightnessControlTestUtils.HIDppHelper.get_brightness(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the brightness matches the MaxBrightness supported on the device")
            # ----------------------------------------------------------------------------------------------------------
            checker = BrightnessControlTestUtils.GetBrightnessResponseChecker
            check_map = checker.get_check_map(brightness=self.config.F_MaxBrightness)
            checker.check_fields(test_case=self, message=response,
                                 expected_cls=self.feature_8040.get_brightness_response_cls, check_map=check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_8040_0005#2", _AUTHOR)
    # end def test_five_brightness_levels_are_defined_on_60_percent_keyboards_in_all_battery_levels

    @features("Feature8040")
    @features("Feature8071")
    @features("Keyboard")
    @features("60PercentKeyboard")
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.HW_BRIGHTNESS)
    @level("Business")
    @services('AtLeastOneKey', (KEY_ID.BACKLIGHT_UP, KEY_ID.BACKLIGHT_DOWN,
                                KEY_ID.BRIGHTNESS_UP, KEY_ID.BRIGHTNESS_DOWN, KEY_ID.DIMMING_KEY))
    def test_five_brightness_levels_are_defined_on_60_percent_keyboards_in_all_charging_status(self):
        """
        In OOB state, check that there are FIVE different brightness levels can be selected

        This test case shall also be tested under the following charging statuses:
        - Wired charging (Charging Mode) #3
        - Wireless charging (Charging Mode) #3
        - Wireless Powered (NRWP devices) #3
        """
        self.post_requisite_reload_nvs = True
        charging_statuses = ['wired_charging', 'wireless_charging', 'wireless_powered']
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getInfo request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_info(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the steps capability is 5 from the response of getInfo")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(to_int(response.steps), 5, msg="The supported brightness steps on a 60% keyboard is 5.")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over {charging_statuses}")
        # --------------------------------------------------------------------------------------------------------------
        for charging_status in charging_statuses:
            if self._test_enter_specified_charging_power_status(charging_status=charging_status):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Entered {charging_status}")
                # ------------------------------------------------------------------------------------------------------
            else:
                continue
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send setBrightness request with brightness={self.config.F_MaxBrightness}")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.HIDppHelper.set_brightness(test_case=self,
                                                                  brightness=self.config.F_MaxBrightness)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self,
                                f"Set the brightness to {self.config.F_MaxBrightness} and check the brightness is "
                                "as expected from the result of LED Spy/Monitoring")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.set_fix_effect_and_check_result_from_rgb_monitoring(
                test_case=self, brightness=self.config.F_MaxBrightness, calibration_data=self.calibration_data)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop: brightness in range(5 - 1)")
            # ----------------------------------------------------------------------------------------------------------
            # There are only 4 intervals between 5 brightness levels
            for _ in range(5 - 1):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "Press the brightness adjustment button to change the brightness")
                # ------------------------------------------------------------------------------------------------------
                self._test_adjust_brightness_via_physical_button(increase_brightness=False,
                                                                 calibration_data=self.calibration_data)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send getBrightness request")
            # ----------------------------------------------------------------------------------------------------------
            response = BrightnessControlTestUtils.HIDppHelper.get_brightness(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the brightness matches the MaxBrightness supported on the device")
            # ----------------------------------------------------------------------------------------------------------
            checker = BrightnessControlTestUtils.GetBrightnessResponseChecker
            check_map = checker.get_check_map(brightness=self.config.F_MaxBrightness)
            checker.check_fields(test_case=self, message=response,
                                 expected_cls=self.feature_8040.get_brightness_response_cls, check_map=check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Disable {charging_status}")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.ChargingHelper.exit_charging_mode(test_case=self, source=self.external_power_source)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_8040_0005#3", _AUTHOR)
    # end def test_five_brightness_levels_are_defined_on_60_percent_keyboards_in_all_charging_status

    @features("Feature8040")
    @features("Feature8071")
    @features("Keyboard")
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.HW_BRIGHTNESS)
    @level("Business")
    def test_all_brightness_levels_of_out_of_box_in_all_power_modes(self):
        """
        In OOB state, check that the device has different brightness levels can be selected

        This test case shall also be tested under the following power mode, battery level and charging mode:
        - Run Mode (Power Mode) #1
        - Walk Mode (Power Mode) #1
        - Sleep Mode (Power Mode) #1
        """
        self.post_requisite_reload_nvs = True
        power_modes = ['run_mode', 'walk_mode', 'sleep_mode']
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getInfo request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_info(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the steps capability is more than 1 from the response of getInfo")
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreater(to_int(response.steps), 1,
                           msg="The steps of the brightness should be more than 1.")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait the necessary duration to be sure startup animation is finished')
        # --------------------------------------------------------------------------------------------------------------
        fw_id = self.f.PRODUCT.F_ProductReference
        sleep(GET_RGB_CONFIGURATION_BY_ID[fw_id].STARTUP_DURATION + STARTUP_DURATION_MARGIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self,
                            f"Set the brightness to {self.config.F_MaxBrightness} and check the brightness is "
                            "as expected from the result of LED Spy/Monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.set_fix_effect_and_check_result_from_rgb_monitoring(
            test_case=self, brightness=self.config.F_MaxBrightness, calibration_data=self.calibration_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over {power_modes}")
        # --------------------------------------------------------------------------------------------------------------
        for power_mode in power_modes:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop: brightness in "
                                     f"{range(self.config.F_MinBrightness + 1, self.config.F_MaxBrightness + 1)}")
            # ----------------------------------------------------------------------------------------------------------
            for brightness in range(self.config.F_MinBrightness + 1, self.config.F_MaxBrightness + 1):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"Make the device into power mode: {power_mode}")
                # ------------------------------------------------------------------------------------------------------
                self._test_enter_specified_power_mode(power_mode=power_mode)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send setBrightness request")
                # ------------------------------------------------------------------------------------------------------
                BrightnessControlTestUtils.HIDppHelper.set_brightness(
                    test_case=self,
                    brightness=self.config.F_MaxBrightness if
                    brightness < ((self.config.F_MaxBrightness - self.config.F_MinBrightness) / 2)
                    else self.config.F_MinBrightness)
                sleep(0.2)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"Adjust the brightness to {brightness} via software")
                # ------------------------------------------------------------------------------------------------------
                self._test_adjust_brightness_via_software(target_brightness=brightness,
                                                          calibration_data=self.calibration_data)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_8040_0006#1", _AUTHOR)
    # end def test_all_brightness_levels_of_out_of_box_in_all_power_modes

    @features("Feature8040")
    @features("Feature8071")
    @features("Keyboard")
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.HW_BRIGHTNESS)
    @level("Business")
    @services("PowerSupply")
    def test_all_brightness_levels_of_out_of_box_in_all_battery_levels(self):
        """
        In OOB state, check that the device has different brightness levels can be selected

        This test case shall also be tested under the following power mode, battery level and charging mode:
        - Full (Battery Level) #2
        - Good (Battery Level) #2
        - Low (Battery Level) #2
        - Critical (Battery Level) #2
        """
        self.post_requisite_reload_nvs = True
        battery_levels = UnifiedBattery.BATTERY_LEVELS_V0ToV5
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over {battery_levels}")
        # --------------------------------------------------------------------------------------------------------------
        for index, battery_level in enumerate(battery_levels):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Make the device into battery level: {battery_level}")
            # ----------------------------------------------------------------------------------------------------------
            state_of_charge = int(self.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_SupportedLevels[index])
            battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, state_of_charge)
            self.reset(hardware_reset=True, starting_voltage=battery_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait the necessary duration to be sure startup animation is finished')
            # ----------------------------------------------------------------------------------------------------------
            fw_id = self.f.PRODUCT.F_ProductReference
            sleep(GET_RGB_CONFIGURATION_BY_ID[fw_id].STARTUP_DURATION + STARTUP_DURATION_MARGIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self,
                                f"Set the brightness to {self.config.F_MaxBrightness} and check the brightness is "
                                "as expected from the result of LED Spy/Monitoring")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.set_fix_effect_and_check_result_from_rgb_monitoring(
                test_case=self, brightness=self.config.F_MaxBrightness)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop: brightness in "
                                     f"{range(self.config.F_MinBrightness + 1, self.config.F_MaxBrightness + 1)}")
            # ----------------------------------------------------------------------------------------------------------
            for brightness in range(self.config.F_MinBrightness + 1, self.config.F_MaxBrightness + 1):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send setBrightness request")
                # ------------------------------------------------------------------------------------------------------
                BrightnessControlTestUtils.HIDppHelper.set_brightness(
                    test_case=self,
                    brightness=self.config.F_MaxBrightness if
                    brightness < ((self.config.F_MaxBrightness - self.config.F_MinBrightness)/2)
                    else self.config.F_MinBrightness)
                sleep(0.2)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"Adjust the brightness to {brightness} via software")
                # ------------------------------------------------------------------------------------------------------
                self._test_adjust_brightness_via_software(target_brightness=brightness,
                                                          calibration_data=self.calibration_data)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_8040_0006#2", _AUTHOR)
    # end def test_all_brightness_levels_of_out_of_box_in_all_battery_levels

    @features("Feature8040")
    @features("Feature8071")
    @features("Keyboard")
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.HW_BRIGHTNESS)
    @level("Business")
    @services('AtLeastOneKey', (KEY_ID.BACKLIGHT_UP, KEY_ID.BACKLIGHT_DOWN,
                                KEY_ID.BRIGHTNESS_UP, KEY_ID.BRIGHTNESS_DOWN, KEY_ID.DIMMING_KEY))
    def test_all_brightness_levels_of_out_of_box_in_all_charging_status(self):
        """
        In OOB state, check that the device has different brightness levels can be selected

        This test case shall also be tested under the following charging modes
        - Wired charging (Charging Mode) #3
        - Wireless charging (Charging Mode) #3
        - Wireless Powered (NRWP devices) #3
        """
        self.post_requisite_reload_nvs = True
        charging_statuses = ['wired_charging', 'wireless_charging', 'wireless_powered']
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getInfo request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_info(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over {charging_statuses}")
        # --------------------------------------------------------------------------------------------------------------
        for charging_status in charging_statuses:
            if self._test_enter_specified_charging_power_status(charging_status=charging_status):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Entered {charging_status}")
                # ------------------------------------------------------------------------------------------------------
            else:
                continue
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send setBrightness request with brightness={self.config.F_MaxBrightness}")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.HIDppHelper.set_brightness(test_case=self,
                                                                  brightness=self.config.F_MaxBrightness)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self,
                                f"Set the brightness to {self.config.F_MaxBrightness} and check the brightness is "
                                "as expected from the result of LED Spy/Monitoring")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.set_fix_effect_and_check_result_from_rgb_monitoring(
                test_case=self, brightness=self.config.F_MaxBrightness)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Test Loop: brightness in range({response.steps})")
            # ----------------------------------------------------------------------------------------------------------
            for index in range(to_int(response.steps) - 1):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "Press the brightness adjustment button to change the brightness")
                # ------------------------------------------------------------------------------------------------------
                self._test_adjust_brightness_via_physical_button(
                    increase_brightness=self.config.F_DefaultBrightness == self.config.F_MinBrightness,
                    calibration_data=self.calibration_data)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Disable {charging_status}")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.ChargingHelper.exit_charging_mode(test_case=self, source=self.external_power_source)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_8040_0006#3", _AUTHOR)
    # end def test_all_brightness_levels_of_out_of_box_in_all_charging_status

    @features("Feature8040")
    @features("ContextualKeys")
    @level("Business")
    @services("RGBMonitoring")
    def test_screen_dimming_off_after_timeout(self):
        """
        Validate the screen of the device is dimming or turing OFF after X seconds timeout of inactivity in
        autonomously mode
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform an user action and start ticking the elapsed time before "
                                 f"{self.config.F_DimmingOffTimeout} seconds")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        init_time = time()
        elapsed_time = 0
        dimming_duration = 30
        start_dimming_time = 0
        start_dimming = False
        dimming_brightness = self.config.F_MaxBrightness
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: elapsed_time in range({self.config.F_DimmingOffTimeout})")
        # --------------------------------------------------------------------------------------------------------------
        # Add 2 seconds tolerance for DimmingOffTimeout
        while elapsed_time < self.config.F_DimmingOffTimeout + DIMMING_OFF_TIMEOUT_MARGIN:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the brightness is not decreasing/is decreasing when the elapsed_time"
                                      f"less or equals/higher than {self.config.F_DimmingOffTimeout}")
            # ----------------------------------------------------------------------------------------------------------
            if elapsed_time > (self.config.F_DimmingOffTimeout - dimming_duration):
                RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)
                sleep(1)
                RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)
                elapsed_time = time() - init_time
                try:
                    dimming_brightness = \
                        ((dimming_duration - (elapsed_time - start_dimming_time)) / dimming_duration) * \
                        self.config.F_MaxBrightness if start_dimming else self.config.F_MaxBrightness
                    RGBEffectsTestUtils.RgbSpyHelper.check_fixed_effect(
                        test_case=self, red_value=0xFF, green_value=0xFF, blue_value=0xFF,
                        brightness=int(dimming_brightness),
                        check_last_packet_only=True,
                        calibration_data=self.calibration_data,
                        cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)
                    if not start_dimming:
                        start_dimming_time = elapsed_time - 1  # The duration time of first dimming shall be counted
                        start_dimming = True
                    # end if
                except AssertionError:
                    if start_dimming:
                        if int(dimming_brightness) <= 0:
                            break
                        else:
                            self.assertAlmostEqual(first=dimming_brightness,
                                                   second=self.config.F_MinBrightness,
                                                   delta=1)
                        # end if
                    # end if
                # end try
            # end if
            elapsed_time = time() - init_time
        # end while
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_8040_0007", _AUTHOR)
    # end def test_screen_dimming_off_after_timeout

    @features("Feature8040")
    @features("Feature1805")
    @features("Unifying")
    @features("ContextualKeys")
    @level("Business")
    @services("PowerSupply")
    def test_starting_brightness_in_all_power_modes_unifying(self):
        """
        When the device is connecting with a receiver, validate the brightness of the device is starting with 100%
        brightness after first connection.

        This test case shall also be tested under the following battery levels:
        - Full (Battery Level) #1
        - Good (Battery Level) #1
        - Low (Battery Level) #1
        - Critical (Battery Level) #1
        """
        self.post_requisite_reload_nvs = True
        battery_levels = UnifiedBattery.BATTERY_LEVELS_V0ToV5
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over {battery_levels}")
        # --------------------------------------------------------------------------------------------------------------
        for index, battery_level in enumerate(battery_levels):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set device OOB by 0x1805")
            # ----------------------------------------------------------------------------------------------------------
            DeviceBaseTestUtils.HIDppHelper.set_oob_state(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Make the device into battery level: {battery_level}")
            # ----------------------------------------------------------------------------------------------------------
            state_of_charge = int(self.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_SupportedLevels[index])
            battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, state_of_charge)
            self.reset(hardware_reset=True, starting_voltage=battery_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send getBrightness request")
            # ----------------------------------------------------------------------------------------------------------
            response = BrightnessControlTestUtils.HIDppHelper.get_brightness(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the brightness is 100% from the response of getBrightness")
            # ----------------------------------------------------------------------------------------------------------
            checker = BrightnessControlTestUtils.GetBrightnessResponseChecker
            check_map = checker.get_check_map(brightness=self.config.F_MaxBrightness)
            checker.check_fields(test_case=self, message=response,
                                 expected_cls=self.feature_8040.get_brightness_response_cls, check_map=check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the brightness is 100% from the result of LED Spy/Monitoring")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.set_fix_effect_and_check_result_from_rgb_monitoring(
                test_case=self, brightness=self.config.F_MaxBrightness)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_8040_0008#1", _AUTHOR)
    # end def test_starting_brightness_in_all_power_modes_unifying

    @features("Feature8040")
    @features("Feature1805")
    @features("Unifying")
    @features("ContextualKeys")
    @level("Business")
    def test_starting_brightness_in_all_power_modes_unifying(self):
        """
        When the device is connecting with a receiver, validate the brightness of the device is starting with 100%
        brightness after first connection.

        This test case shall also be tested under the following charging mode:
        - Wireless charging (Charging Mode) #2
        - Wireless Powered (NRWP devices) #2
        """
        self.post_requisite_reload_nvs = True
        # Only test wireless charging/powered
        # Because gaming devices always switches to USB protocol when charging via USB cable
        charging_statuses = ['wireless_charging', 'wireless_powered']
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over {charging_statuses}")
        # --------------------------------------------------------------------------------------------------------------
        for index, charging_status in enumerate(charging_statuses):
            if self._test_enter_specified_charging_power_status(charging_status=charging_status):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Entered {charging_status}")
                # ------------------------------------------------------------------------------------------------------
            else:
                continue
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set device OOB by 0x1805")
            # ----------------------------------------------------------------------------------------------------------
            DeviceBaseTestUtils.HIDppHelper.set_oob_state(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Power OFF -> ON the DUT")
            # ----------------------------------------------------------------------------------------------------------
            self.reset(hardware_reset=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send getBrightness request")
            # ----------------------------------------------------------------------------------------------------------
            response = BrightnessControlTestUtils.HIDppHelper.get_brightness(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the brightness is 100% from the response of getBrightness")
            # ----------------------------------------------------------------------------------------------------------
            checker = BrightnessControlTestUtils.GetBrightnessResponseChecker
            check_map = checker.get_check_map(brightness=self.config.F_MaxBrightness)
            checker.check_fields(test_case=self, message=response,
                                 expected_cls=self.feature_8040.get_brightness_response_cls, check_map=check_map)

            if self.kosmos.discover_emulator(emulation_type=DeviceFamilyName.GENERIC_LED_SPY) and \
                    (RGBEffects.RGBEffectID.FIXED in RGBEffectsTestUtils.get_supported_effect_ids_by_cluster(
                        test_case=self, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check the brightness is 100% from the result of LED Spy/Monitoring")
                # ------------------------------------------------------------------------------------------------------
                BrightnessControlTestUtils.set_fix_effect_and_check_result_from_rgb_monitoring(
                    test_case=self, brightness=self.config.F_MaxBrightness)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Disable {charging_status}")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.ChargingHelper.exit_charging_mode(test_case=self, source=self.external_power_source)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_8040_0008#2", _AUTHOR)
    # end def test_starting_brightness_in_all_power_modes_unifying

    @features("Feature8040")
    @features("Feature1805")
    @features("Bluetooth")
    @features("ContextualKeys")
    @level("Business")
    @services("PowerSupply")
    @services("BleContext")
    def test_starting_brightness_in_all_power_modes_ble(self):
        """
        When the device is in BLE mode, validate the brightness of the device is starting with 100% brightness after
        first connection.

        This test case shall also be tested under the following battery levels:
        - Full (Battery Level) #1
        - Good (Battery Level) #1
        - Low (Battery Level) #1
        - Critical (Battery Level) #1
        """
        if KEY_ID.LS2_BLE_CONNECTION_TOGGLE in self.button_stimuli_emulator._keyboard_layout.KEYS.keys():
            connection_buttons = [KEY_ID.LS2_BLE_CONNECTION_TOGGLE] * 2
        elif KEY_ID.LS2_CONNECTION in self.button_stimuli_emulator._keyboard_layout.KEYS.keys() \
                and KEY_ID.BLE_CONNECTION in self.button_stimuli_emulator._keyboard_layout.KEYS.keys():
            connection_buttons = [KEY_ID.LS2_CONNECTION, KEY_ID.BLE_CONNECTION]
        else:
            raise KeyError('No available connection button is defined in the key matrix.')
        # end if
        self.post_requisite_reload_nvs = True
        battery_levels = UnifiedBattery.BATTERY_LEVELS_V0ToV5
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over {battery_levels}")
        # --------------------------------------------------------------------------------------------------------------
        for index, battery_level in enumerate(battery_levels):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Make the device into battery level: {battery_level}")
            # ----------------------------------------------------------------------------------------------------------
            state_of_charge = int(self.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_SupportedLevels[index])
            battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, state_of_charge)
            self.reset(hardware_reset=True, starting_voltage=battery_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Switch to BLE Mode")
            # ----------------------------------------------------------------------------------------------------------
            self.post_requisite_exit_ble_channel = True
            ProtocolManagerUtils.select_channel_by_protocol(self, LogitechProtocol.BLE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send getBrightness request")
            # ----------------------------------------------------------------------------------------------------------
            response = BrightnessControlTestUtils.HIDppHelper.get_brightness(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the brightness is 100% from the response of getBrightness")
            # ----------------------------------------------------------------------------------------------------------
            checker = BrightnessControlTestUtils.GetBrightnessResponseChecker
            check_map = checker.get_check_map(brightness=self.config.F_MaxBrightness)
            checker.check_fields(test_case=self, message=response,
                                 expected_cls=self.feature_8040.get_brightness_response_cls, check_map=check_map)

            if self.kosmos.discover_emulator(emulation_type=DeviceFamilyName.GENERIC_LED_SPY) and \
                    (RGBEffects.RGBEffectID.FIXED in RGBEffectsTestUtils.get_supported_effect_ids_by_cluster(
                        test_case=self, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check the brightness is 100% from the result of LED Spy/Monitoring")
                # ------------------------------------------------------------------------------------------------------
                BrightnessControlTestUtils.set_fix_effect_and_check_result_from_rgb_monitoring(
                    test_case=self, brightness=self.config.F_MaxBrightness)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Exit BLE channel")
            # ----------------------------------------------------------------------------------------------------------
            ProtocolManagerUtils.exit_ble_channel(self)
            self.post_requisite_exit_ble_channel = False

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {connection_buttons[0]} to switch to Unifying")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=connection_buttons[0])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_8040_0009#1", _AUTHOR)
    # end def test_starting_brightness_in_all_power_modes_ble

    @features("Feature8040")
    @features("Bluetooth")
    @features("ContextualKeys")
    @level("Business")
    @services("BleContext")
    @services('PowerSupply')
    def test_starting_brightness_in_all_charging_status_ble(self):
        """
        When the device is in BLE mode, validate the brightness of the device is starting with 100% brightness after
        first connection.

        This test case shall also be tested under the following charging modes:
        - Wireless charging (Charging Mode) #1
        - Wireless Powered (NRWP devices) #1
        """
        if KEY_ID.LS2_BLE_CONNECTION_TOGGLE in self.button_stimuli_emulator._keyboard_layout.KEYS.keys():
            connection_buttons = [KEY_ID.LS2_BLE_CONNECTION_TOGGLE] * 2
        elif KEY_ID.LS2_CONNECTION in self.button_stimuli_emulator._keyboard_layout.KEYS.keys() \
                and KEY_ID.BLE_CONNECTION in self.button_stimuli_emulator._keyboard_layout.KEYS.keys():
            connection_buttons = [KEY_ID.LS2_CONNECTION, KEY_ID.BLE_CONNECTION]
        else:
            raise KeyError('No available connection button is defined in the key matrix.')
        # end if
        self.post_requisite_reload_nvs = True
        # Only test wireless charging/powered
        # Because gaming devices always switches to USB protocol when charging via USB cable
        charging_statuses = ['wireless_charging', 'wireless_powered']
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over {charging_statuses}")
        # --------------------------------------------------------------------------------------------------------------
        for charging_status in charging_statuses:
            if self._test_enter_specified_charging_power_status(charging_status=charging_status):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Entered {charging_status}")
                # ------------------------------------------------------------------------------------------------------
            else:
                continue
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Switch to BLE Mode")
            # ----------------------------------------------------------------------------------------------------------
            self.post_requisite_exit_ble_channel = True
            ProtocolManagerUtils.select_channel_by_protocol(self, LogitechProtocol.BLE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send getBrightness request")
            # ----------------------------------------------------------------------------------------------------------
            response = BrightnessControlTestUtils.HIDppHelper.get_brightness(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the brightness is 100% from the response of getBrightness")
            # ----------------------------------------------------------------------------------------------------------
            checker = BrightnessControlTestUtils.GetBrightnessResponseChecker
            check_map = checker.get_check_map(brightness=self.config.F_MaxBrightness)
            checker.check_fields(test_case=self, message=response,
                                 expected_cls=self.feature_8040.get_brightness_response_cls, check_map=check_map)

            if self.kosmos.discover_emulator(emulation_type=DeviceFamilyName.GENERIC_LED_SPY) and \
                    (RGBEffects.RGBEffectID.FIXED in RGBEffectsTestUtils.get_supported_effect_ids_by_cluster(
                        test_case=self, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check the brightness is 100% from the result of LED Spy/Monitoring")
                # ------------------------------------------------------------------------------------------------------
                BrightnessControlTestUtils.set_fix_effect_and_check_result_from_rgb_monitoring(
                    test_case=self, brightness=self.config.F_MaxBrightness)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Exit BLE channel")
            # ----------------------------------------------------------------------------------------------------------
            ProtocolManagerUtils.exit_ble_channel(self)
            self.post_requisite_exit_ble_channel = False

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {connection_buttons[0]} to switch to Unifying")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=connection_buttons[0])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Disable {charging_status}")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.ChargingHelper.exit_charging_mode(test_case=self, source=self.external_power_source)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_8040_0009#2", _AUTHOR)
    # end def test_starting_brightness_in_all_charging_status_ble

    def _test_enter_specified_power_mode(self, power_mode):
        """
        Enter the specified power mode

        :param power_mode: Device power mode
        :type power_mode: ``str``
        """
        if power_mode == 'run_mode':
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Perform an user action to make the device in run mode")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.user_action()
        elif power_mode == 'walk_mode':
            time_to_enter_walk_mode = 5
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, "Perform an user action and wait "
                      f"{time_to_enter_walk_mode + 1} seconds to make the device in walk mode")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.user_action()
            sleep(time_to_enter_walk_mode + 1)
        elif power_mode == 'sleep_mode':
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, "Perform an user action and wait for a few seconds"
                      f"({self.f.PRODUCT.DEVICE.F_MaxWaitSleep}) to make the device in sleep mode")
            # ----------------------------------------------------------------------------------------------------------
            if self.f.PRODUCT.FEATURES.GAMING.RGB_EFFECTS.F_Enabled:
                RGBEffectsTestUtils.HIDppHelper.manage_rgb_power_mode(
                    self, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
                    rgb_power_mode=RGBEffectsTestUtils.PowerMode.POWER_SAVE_MODE)
            else:
                self.button_stimuli_emulator.user_action()
                sleep(self.f.PRODUCT.DEVICE.F_MaxWaitSleep)
            # end if
        elif power_mode == 'deep_sleep_mode':
            if self.f.PRODUCT.FEATURES.COMMON.POWER_MODES.F_Enabled:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send 0x1830.SetPowerMode with PowerModeNum=3(deep-sleep)")
                # ------------------------------------------------------------------------------------------------------
                PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Wait for {self.f.PRODUCT.DEVICE.F_MaxWaitDeepSleep} seconds to enter deep-sleep mode")
                # ------------------------------------------------------------------------------------------------------
                sleep(self.f.PRODUCT.DEVICE.F_MaxWaitDeepSleep)
            # end if
        # end if
    # end def _test_enter_specified_power_mode

    def _test_enter_specified_charging_power_status(self, charging_status):
        """
        Enter the specified charging/powered status

        :param charging_status: Device charging/powered status
        :type charging_status: ``str``
        """
        enter_specific_changing_mode = False
        if charging_status == 'wired_charging' and UnifiedBatteryTestUtils.is_the_capability_supported(
                test_case=self, capability=UnifiedBattery.Flags.RECHARGEABLE):
            DeviceTestUtils.ChargingHelper.enter_charging_mode(
                test_case=self, source=UnifiedBattery.ExternalPowerStatus.WIRED)
            self.external_power_source = UnifiedBattery.ExternalPowerStatus.WIRED
            enter_specific_changing_mode = True
        elif charging_status == 'wireless_charging' and self.f.PRODUCT.DEVICE.BATTERY.F_WirelessCharging and \
                UnifiedBatteryTestUtils.is_the_capability_supported(test_case=self,
                                                                    capability=UnifiedBattery.Flags.RECHARGEABLE):
            DeviceTestUtils.ChargingHelper.enter_charging_mode(
                test_case=self, source=UnifiedBattery.ExternalPowerStatus.WIRELESS)
            self.external_power_source = UnifiedBattery.ExternalPowerStatus.WIRELESS
            enter_specific_changing_mode = True
        elif charging_status == 'wireless_powered' and UnifiedBatteryTestUtils.is_the_capability_supported(
                test_case=self, capability=UnifiedBattery.Flags.REMOVABLE_BATTERY):
            DeviceTestUtils.ChargingHelper.enter_charging_mode(
                test_case=self, source=UnifiedBattery.ExternalPowerStatus.WIRELESS)
            self.external_power_source = UnifiedBattery.ExternalPowerStatus.WIRELESS
            self.post_requisite_discharge_super_cap = True
            enter_specific_changing_mode = True
        # end if

        return enter_specific_changing_mode
    # end def _test_enter_specified_charging_power_status

    def _test_adjust_brightness_via_physical_button(self, increase_brightness, calibration_data,
                                                    brightness_control=None, current_brightness=None,
                                                    check_fix_effect=True):
        """
        When in onboard mode, check that the keyboard supports shortcuts/physical key for controlling the brightness of
        immersive lighting effects

        :param increase_brightness: Flag indicating the brightness shall be increased or decreased
        :type increase_brightness: ``bool``
        :param calibration_data: Reb, Blue and Green calibration data for zone0, zone1 and zone2
        :type calibration_data: ``list[list[int, int, int]]``
        :param brightness_control: The physical control of brightness - OPTIONAL
        :type brightness_control: ``KEY_ID | None``
        :param current_brightness: The current brightness before pressing a button to adjust the brightness - OPTIONAL
        :type current_brightness: ``int | None``
        :param check_fix_effect: Flag indicating that the brightness shall be validated via
                                 checking RGB fix effect - OPTIONAL
        :type check_fix_effect: ``bool``
        """
        if brightness_control is None:
            brightness_controls = BrightnessControlTestUtils.get_standard_physical_brightness_controls(test_case=self)
            fn_brightness_controls = \
                BrightnessControlTestUtils.get_functional_physical_brightness_controls(test_case=self)
            controls = fn_brightness_controls if len(fn_brightness_controls) > 0 else brightness_controls
            brightness_control = KEY_ID.DIMMING_KEY if KEY_ID.DIMMING_KEY in controls else (
                list(set(controls).intersection({KEY_ID.BRIGHTNESS_UP, KEY_ID.BACKLIGHT_UP}))[0] if increase_brightness
                else list(set(controls).intersection({KEY_ID.BACKLIGHT_DOWN, KEY_ID.BRIGHTNESS_DOWN})))[0]
            is_function_key = len(fn_brightness_controls) > 0
        else:
            is_function_key = True if brightness_control in \
                BrightnessControlTestUtils.get_functional_physical_brightness_controls(test_case=self) else False
        # end if

        if current_brightness is None:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Get the current brightness from the DUT")
            # ----------------------------------------------------------------------------------------------------------
            current_brightness = \
                to_int(BrightnessControlTestUtils.HIDppHelper.get_brightness(test_case=self).brightness)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {brightness_control!s} to "
                                 f"{'increase' if increase_brightness else 'decrease' } the brightness")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)
        BrightnessControlTestUtils.control_brightness_manually(
            test_case=self, key_id=brightness_control, is_function_key=is_function_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring after 0.5 second')
        # --------------------------------------------------------------------------------------------------------------
        sleep(0.5)
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the brightness is {'increase' if increase_brightness else 'decrease' } "
                                  "from the brightnessChangeEvent")
        # --------------------------------------------------------------------------------------------------------------
        event = BrightnessControlTestUtils.HIDppHelper.brightness_change_event(test_case=self,
                                                                               check_first_message=False,
                                                                               allow_no_message=True)
        self.assertNotNone(
            obtained=event,
            msg="There is no brightnessChangeEvent received after changing brightness via physical control(s)")
        if increase_brightness:
            self.assertGreater(
                to_int(event.brightness),
                current_brightness,
                msg="The brightness is not increasing after pressing: "
                    f"{'FN_KEY' + f'{brightness_control!s}' if is_function_key else f'{brightness_control!s}'}")
        else:
            self.assertLess(
                to_int(event.brightness),
                current_brightness,
                msg="The brightness is not decreasing after pressing: "
                    f"{'FN_KEY' + f'{brightness_control!s}' if is_function_key else f'{brightness_control!s}'}")
        # end if

        if check_fix_effect and self.kosmos.discover_emulator(emulation_type=DeviceFamilyName.GENERIC_LED_SPY):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check the brightness is {'increase' if increase_brightness else 'decrease' } "
                                      "from the result of LED Spy/Monitoring")
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.check_fixed_effect(
                test_case=self, red_value=0xFF, green_value=0xFF, blue_value=0xFF,
                brightness=to_int(event.brightness),
                calibration_data=calibration_data,
                check_last_packet_only=True,
                cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)
        # end if
    # end def _test_adjust_brightness_via_physical_button

    def _test_adjust_brightness_via_software(self, target_brightness, calibration_data):
        """
        Check that the brightness can be changed via software

        :param target_brightness: Target brightness to be changed
        :type target_brightness: ``int``
        :param calibration_data: Reb, Blue and Green calibration data for zone0, zone1 and zone2
        :type calibration_data: ``list[list[int, int, int]]``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send setBrightness request with brightness={target_brightness}")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.set_brightness(test_case=self, brightness=target_brightness)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring after 0.5 second')
        # --------------------------------------------------------------------------------------------------------------
        sleep(0.5)
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the brightness is {target_brightness} from the response of getBrightness")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_brightness(test_case=self)
        checker = BrightnessControlTestUtils.GetBrightnessResponseChecker
        check_map = checker.get_check_map(brightness=target_brightness)
        checker.check_fields(test_case=self, message=response,
                             expected_cls=self.feature_8040.get_brightness_response_cls, check_map=check_map)

        if self.kosmos.discover_emulator(emulation_type=DeviceFamilyName.GENERIC_LED_SPY):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the brightness is as expected from the result of LED Spy/Monitoring")
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.check_fixed_effect(
                test_case=self, red_value=0xFF, green_value=0xFF, blue_value=0xFF,
                brightness=target_brightness,
                calibration_data=calibration_data,
                cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)
        # end if
    # end def _test_adjust_brightness_via_software
# end class BrightnessControlBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
