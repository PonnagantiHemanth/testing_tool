#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.gaming.feature_8040.functionality
:brief: HID++ 2.0 ``BrightnessControl`` functionality test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2023/11/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep
from unittest import skip

from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.brightnesscontrol import CapabilitiesV1
from pyhid.hidpp.features.gaming.brightnesscontrol import IlluminationState
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pyraspi.services.kosmos.config.rgbconfiguration import GET_RGB_CONFIGURATION_BY_ID
from pyraspi.services.kosmos.module.devicetree import DeviceFamilyName
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.brightnesscontrolutils import BrightnessControlTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.hidpp20.gaming.feature_8040.brightnesscontrol import BrightnessControlTestCase
from pytestbox.device.base.rgbeffectsutils import RGBEffectsTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"
STARTUP_DURATION_MARGIN = 1


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BrightnessControlFunctionalityTestCase(BrightnessControlTestCase):
    """
    Validate ``BrightnessControl`` functionality test cases
    """

    @features("Feature8040")
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.HW_BRIGHTNESS)
    @level("Functionality")
    @services('AtLeastOneKey', (KEY_ID.BACKLIGHT_UP, KEY_ID.BACKLIGHT_DOWN,
                                KEY_ID.BRIGHTNESS_UP, KEY_ID.BRIGHTNESS_DOWN, KEY_ID.DIMMING_KEY))
    def test_brightness_event_sent_after_changing_by_physical_keys(self):
        """
        If the events capability is set, check the brightnessChangeEvent is sent after the user pressed a physical
        brightness button
        """
        self.post_requisite_reload_nvs = True
        brightness_controls = BrightnessControlTestUtils.get_standard_physical_brightness_controls(test_case=self)
        fn_brightness_controls = BrightnessControlTestUtils.get_functional_physical_brightness_controls(test_case=self)
        controls = brightness_controls if len(brightness_controls) > 0 else fn_brightness_controls
        brightness_control = KEY_ID.DIMMING_KEY if KEY_ID.DIMMING_KEY in controls else (
            KEY_ID.BRIGHTNESS_DOWN if self.config.F_DefaultBrightness
            != self.config.F_MinBrightness else KEY_ID.BRIGHTNESS_UP)
        is_function_key = len(brightness_controls) == 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press the brightness button: "
                                 f"{'FN' + str(brightness_control) if is_function_key else str(brightness_control)}")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)
        BrightnessControlTestUtils.control_brightness_manually(
            test_case=self, key_id=brightness_control, is_function_key=is_function_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the brightness is changed from brightnessChangeEvent")
        # --------------------------------------------------------------------------------------------------------------
        event = BrightnessControlTestUtils.HIDppHelper.brightness_change_event(test_case=self, allow_no_message=True)
        self.assertNotNone(obtained=event,
                           msg='There is no brightnessChangeEvent received after changing the brightness via key: '
                               f'{"FN" + str(brightness_control) if is_function_key else str(brightness_control)}')
        if brightness_control == KEY_ID.BRIGHTNESS_UP:
            if self.config.F_DefaultBrightness == self.config.F_MaxBrightness:
                self.assertEqual(obtained=to_int(event.brightness), expected=self.config.F_DefaultBrightness,
                                 msg='The brightness has reached the maximum, it shall not be changed.')
            else:
                self.assertGreater(to_int(event.brightness), self.config.F_DefaultBrightness,
                                   msg=f'The brightness is not increasing after pressing key: {brightness_control}')
            # end if
        elif brightness_control in [KEY_ID.BRIGHTNESS_DOWN, KEY_ID.DIMMING_KEY]:
            if self.config.F_DefaultBrightness == self.config.F_MinBrightness:
                self.assertEqual(obtained=to_int(event.brightness), expected=self.config.F_MaxBrightness,
                                 msg='The brightness does not match the min brightness after pressing cycle thru '
                                     f'brightness key({brightness_control}) at the min brightness')
            else:
                self.assertLess(to_int(event.brightness), self.config.F_DefaultBrightness,
                                msg=f'The brightness is not decreasing after pressing key: {brightness_control}')
            # end if
        # end if

        self.testCaseChecked("FUN_8040_0001", _AUTHOR)
    # end def test_brightness_event_sent_after_changing_by_physical_keys

    @features("Feature8040")
    @level("Functionality")
    @bugtracker('UnexpectedBrightnessChangeEvent')
    def test_brightness_event_not_sent_after_changing_by_software(self):
        """
        Check the brightnessChangeEvent is not sent after the user changed the brightness via software
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setBrightness request to change the brightness")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)
        BrightnessControlTestUtils.HIDppHelper.set_brightness(
            test_case=self,
            brightness=self.config.F_MinBrightness
            if self.config.F_DefaultBrightness == self.config.F_MaxBrightness else self.config.F_MaxBrightness)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check there is no brightnessChangeEvent received")
        # --------------------------------------------------------------------------------------------------------------
        event = BrightnessControlTestUtils.HIDppHelper.brightness_change_event(test_case=self, allow_no_message=True)
        self.assertNone(
            obtained=event,
            msg="There is no brightnessChangeEvent shall be received after changing the brightness via software")

        self.testCaseChecked("FUN_8040_0002", _AUTHOR)
    # end def test_brightness_event_not_sent_after_changing_by_software

    @features("Feature8040v1")
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.ILLUMINATION)
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.HW_ON_OFF)
    @level("Functionality")
    @skip("Under development")
    def test_illumination_event_sent_after_changing_by_physical_keys(self):
        """
        If the events and illumination capabilities are set, check the illuminationChangeEvent is sent after the user
        pressed a physical button to change the illumination state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press the illumination button")
        # --------------------------------------------------------------------------------------------------------------
        # TODO - lack of the definition of illumination button

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the illumination state is as expected from illuminationChangeEvent")
        # --------------------------------------------------------------------------------------------------------------
        event = BrightnessControlTestUtils.HIDppHelper.illumination_change_event(test_case=self)
        checker = BrightnessControlTestUtils.IlluminationStateChecker
        check_map = checker.get_check_map(state=not self.config.F_DefaultIlluminationState)
        checker.check_fields(test_case=self, message=event,
                             expected_cls=self.feature_8040.illumination_change_event_cls,
                             check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press the illumination button")
        # --------------------------------------------------------------------------------------------------------------
        # TODO - lack of the definition of illumination button

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the illumination state is as expected from illuminationChangeEvent")
        # --------------------------------------------------------------------------------------------------------------
        event = BrightnessControlTestUtils.HIDppHelper.illumination_change_event(test_case=self)
        checker = BrightnessControlTestUtils.IlluminationStateChecker
        check_map = checker.get_check_map(state=self.config.F_DefaultIlluminationState)
        checker.check_fields(test_case=self, message=event,
                             expected_cls=self.feature_8040.illumination_change_event_cls,
                             check_map=check_map)

        self.testCaseChecked("FUN_8040_0003", _AUTHOR)
    # end def test_illumination_event_sent_after_changing_by_physical_keys

    @features("Feature8040v1")
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.ILLUMINATION)
    @level("Functionality")
    def test_illumination_event_sent_after_changing_by_software(self):
        """
        If the events and illumination capabilities are set, check the illuminationChangeEvent is not sent after the
        user changed the illumination state via software
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setIllumination request to change the illumination state")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.set_illumination(test_case=self,
                                                                state=not self.config.F_DefaultIlluminationState)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check there is no illuminationChangeEvent received")
        # --------------------------------------------------------------------------------------------------------------
        event = BrightnessControlTestUtils.HIDppHelper.illumination_change_event(test_case=self, allow_no_message=True)
        self.assertNone(
            obtained=event,
            msg="There is no illuminationChangeEvent shall be received after changing the state via software")

        self.testCaseChecked("FUN_8040_0004", _AUTHOR)
    # end def test_illumination_event_sent_after_changing_by_software

    @features("Feature8040")
    @level("Functionality")
    def test_get_brightness_via_software(self):
        """
        Check the brightness can be retrieved via SW after setting by SW
        """
        self.post_requisite_reload_nvs = True
        new_brightness = self.config.F_MinBrightness \
            if self.config.F_DefaultBrightness == self.config.F_MaxBrightness else self.config.F_MaxBrightness
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setBrightness request to change the brightness")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.set_brightness(
            test_case=self,
            brightness=new_brightness)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getBrightness request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_brightness(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the brightness is as expected from the response of getBrightness")
        # --------------------------------------------------------------------------------------------------------------
        checker = BrightnessControlTestUtils.GetBrightnessResponseChecker
        checker.check_fields(
            test_case=self, message=response, expected_cls=self.feature_8040.get_brightness_response_cls,
            check_map=checker.get_check_map(brightness=new_brightness))

        self.testCaseChecked("FUN_8040_0005", _AUTHOR)
    # end def test_get_brightness_via_software

    @features("Feature8040")
    @features("HasRGBConfiguration")
    @level("Functionality")
    @bugtracker('RgbClusterEffectIndexNotUpdated')
    def test_set_brightness_in_supported_levels(self):
        """
        Check the brightness can be set to any level from minBrightness to maxBrightness
        """
        self.post_requisite_reload_nvs = True
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
        LogHelper.log_info(self, f"Test Loop: brightness in {self.config.F_PreDefineBrightnessLevels}")
        # --------------------------------------------------------------------------------------------------------------
        for brightness in self.config.F_PreDefineBrightnessLevels:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Send setBrightness request with brightness = {brightness} and check result.")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.set_brightness_and_check_result_from_rgb_monitoring(
                test_case=self, brightness=int(brightness), calibration_data=self.calibration_data)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send getBrightness request")
            # ----------------------------------------------------------------------------------------------------------
            response = BrightnessControlTestUtils.HIDppHelper.get_brightness(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the brightness is as expected from the response of getBrightness")
            # ----------------------------------------------------------------------------------------------------------
            checker = BrightnessControlTestUtils.GetBrightnessResponseChecker
            checker.check_fields(
                test_case=self, message=response, expected_cls=self.feature_8040.get_brightness_response_cls,
                check_map=checker.get_check_map(brightness=int(brightness)))

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send setBrightness request with brightness={self.config.F_MinBrightness}")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.set_brightness(test_case=self,
                                                              brightness=self.config.F_MinBrightness)
        # Waiting for I2C command packet sent of this brightness change
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: brightness in {list(self.config.F_PreDefineBrightnessLevels)[::-1]}")
        # --------------------------------------------------------------------------------------------------------------
        for brightness in list(self.config.F_PreDefineBrightnessLevels)[::-1]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Send setBrightness request with brightness = {brightness} and check result.")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.set_brightness_and_check_result_from_rgb_monitoring(
                test_case=self, brightness=int(brightness), calibration_data=self.calibration_data)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send getBrightness request")
            # ----------------------------------------------------------------------------------------------------------
            response = BrightnessControlTestUtils.HIDppHelper.get_brightness(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the brightness is as expected from the response of getBrightness")
            # ----------------------------------------------------------------------------------------------------------
            checker = BrightnessControlTestUtils.GetBrightnessResponseChecker
            checker.check_fields(
                test_case=self, message=response, expected_cls=self.feature_8040.get_brightness_response_cls,
                check_map=checker.get_check_map(brightness=int(brightness)))

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_8040_0006", _AUTHOR)
    # end def test_set_brightness_in_supported_levels

    @features("Feature8040")
    @features("Feature8071")
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.HW_BRIGHTNESS)
    @features("HasRGBConfiguration")
    @level("Functionality")
    @services('AtLeastOneKey', (KEY_ID.BACKLIGHT_UP, KEY_ID.BACKLIGHT_DOWN,
                                KEY_ID.BRIGHTNESS_UP, KEY_ID.BRIGHTNESS_DOWN, KEY_ID.DIMMING_KEY))
    def test_set_brightness_via_physical_keys(self):
        """
        If the hw_brightness capability is set, check the brightness can be changed manually
        """
        self.post_requisite_reload_nvs = True
        brightness_controls = BrightnessControlTestUtils.get_standard_physical_brightness_controls(test_case=self)
        fn_brightness_controls = BrightnessControlTestUtils.get_functional_physical_brightness_controls(test_case=self)
        brightness_control = brightness_controls[0] if len(brightness_controls) > 0 else fn_brightness_controls[0]
        brightness = self.config.F_MinBrightness if brightness_control in [KEY_ID.BRIGHTNESS_UP, KEY_ID.BACKLIGHT_UP] \
            else self.config.F_MaxBrightness
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait the necessary duration to be sure startup animation is finished')
        # --------------------------------------------------------------------------------------------------------------
        fw_id = self.f.PRODUCT.F_ProductReference
        sleep(GET_RGB_CONFIGURATION_BY_ID[fw_id].STARTUP_DURATION + STARTUP_DURATION_MARGIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self,
                            f"Set the brightness to {brightness} and check the brightness is "
                            "as expected from the result of LED Spy/Monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.set_fix_effect_and_check_result_from_rgb_monitoring(
            test_case=self, brightness=brightness)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform an user action to change the brightness")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.control_brightness_manually(
            test_case=self,
            key_id=brightness_control,
            is_function_key=len(brightness_controls) == 0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the brightness is changed as expected")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.brightness_change_event(test_case=self,
                                                                                  check_first_message=False)
        if brightness == self.config.F_MinBrightness:
            self.assertGreater(a=to_int(response.brightness),
                               b=self.config.F_DefaultBrightness,
                               msg=f'The brightness level is not increased after pressing {brightness_control!s}')
        else:
            self.assertLess(a=to_int(response.brightness),
                            b=self.config.F_DefaultBrightness,
                            msg=f'The brightness level is not decreased after pressing {brightness_control!s}')
        # end if

        if self.kosmos.discover_emulator(emulation_type=DeviceFamilyName.GENERIC_LED_SPY):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the brightness is as expected from the result of LED Spy/Monitoring")
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.check_fixed_effect(
                test_case=self, red_value=0xFF, green_value=0xFF, blue_value=0xFF,
                brightness=to_int(response.brightness),
                calibration_data=self.calibration_data,
                check_last_packet_only=True,
                cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)
        # end if

        self.testCaseChecked("FUN_8040_0007", _AUTHOR)
    # end def test_set_brightness_via_physical_keys

    @features("Feature8040v1")
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.ILLUMINATION)
    @level("Functionality")
    def test_turning_on_off_lighting_effect_manually(self):
        """
        If the hw_on_off capability is set, check the lighting can be turned on/off manually
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setIllumination request to set the state OFF")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.set_illumination(test_case=self, state=IlluminationState.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform an user action to turn ON the lighting")
        # --------------------------------------------------------------------------------------------------------------
        # TODO - lack of the definition of illumination button

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getIllumination request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_illumination(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the lighting state is ON from the response of getIllumination")
        # --------------------------------------------------------------------------------------------------------------
        checker = BrightnessControlTestUtils.GetIlluminationResponseChecker
        check_map = checker.get_check_map(illumination_state=IlluminationState.OFF)
        checker.check_fields(test_case=self, message=response,
                             expected_cls=self.feature_8040.get_illumination_response_cls, check_map=check_map)

        if self.kosmos.discover_emulator(emulation_type=DeviceFamilyName.GENERIC_LED_SPY):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the lighting state is ON from the result of LED Spy/Monitoring")
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.check_fixed_effect(
                test_case=self, red_value=0xFF, green_value=0xFF, blue_value=0xFF,
                brightness=self.config.F_DefaultBrightness,
                calibration_data=self.calibration_data,
                check_last_packet_only=True,
                cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform an user action to turn ON the lighting")
        # --------------------------------------------------------------------------------------------------------------
        # TODO - lack of the definition of illumination button

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getIllumination request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_illumination(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the lighting state is OFF from the response of getIllumination")
        # --------------------------------------------------------------------------------------------------------------
        checker = BrightnessControlTestUtils.GetIlluminationResponseChecker
        check_map = checker.get_check_map(illumination_state=IlluminationState.ON)
        checker.check_fields(test_case=self, message=response,
                             expected_cls=self.feature_8040.get_illumination_response_cls, check_map=check_map)

        if self.kosmos.discover_emulator(emulation_type=DeviceFamilyName.GENERIC_LED_SPY):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the lighting state is OFF from the result of LED Spy/Monitoring")
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.check_fixed_effect(
                test_case=self, red_value=0xFF, green_value=0xFF, blue_value=0xFF,
                brightness=self.config.F_MinBrightness,
                calibration_data=self.calibration_data,
                check_last_packet_only=True,
                cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)
        # end if

        self.testCaseChecked("FUN_8040_0008", _AUTHOR)
    # end def test_turning_on_off_lighting_effect_manually

    @features("Feature8040v1")
    @level("Functionality")
    def test_transient_capability_on_devices(self):
        """
        If this is an illumination lighting device, check the transient capability is set, otherwise it shall not be set
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getInfo request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_info(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the transient is set from the response of getInfo")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=1 if self.f.PRODUCT.F_IsLightingDevice else 0,
                         obtained=response.capabilities.transient,
                         msg="The capability transient shall " +
                             ("be set" if self.f.PRODUCT.F_IsLightingDevice else "not be set") +
                             "on a mouse or keyboard.")

        self.testCaseChecked("FUN_8040_0009", _AUTHOR)
    # end def test_transient_capability_on_devices

    @features("Feature8040v1")
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.ILLUMINATION)
    @level("Functionality")
    def test_set_illumination_via_software(self):
        """
        If the illumination capability is set, check that the illumination status can be set and get via SW
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setIllumination to change the illumination state")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.set_illumination(test_case=self,
                                                                state=not self.config.F_DefaultIlluminationState)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getIllumination request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_illumination(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the illumination state from the response of getIllumination")
        # --------------------------------------------------------------------------------------------------------------
        checker = BrightnessControlTestUtils.GetIlluminationResponseChecker
        check_map = checker.get_check_map(illumination_state=not self.config.F_DefaultIlluminationState)
        checker.check_fields(test_case=self, message=response,
                             expected_cls=self.feature_8040.get_illumination_response_cls, check_map=check_map)

        self.testCaseChecked("FUN_8040_0010", _AUTHOR)
    # end def test_set_illumination_via_software

    @features("Feature8040v1")
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.ILLUMINATION)
    @level("Functionality")
    def test_brightness_not_changed_after_changing_illumination_state(self):
        """
        If the illumination capability is set, validate the internal brightness value is not changed when the
        illumination state is turning OFF and ON
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setBrightness request to change the brightness to the maximum value")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.set_brightness(test_case=self, brightness=self.config.F_MaxBrightness)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setIllumination request to set the illumination state OFF")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.set_illumination(test_case=self, state=IlluminationState.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getBrightness request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_brightness(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the brightness is not changed from the response of getBrightness")
        # --------------------------------------------------------------------------------------------------------------
        checker = BrightnessControlTestUtils.GetBrightnessResponseChecker
        check_map = checker.get_check_map(brightness=self.config.F_MaxBrightness)
        checker.check_fields(test_case=self, message=response,
                             expected_cls=self.feature_8040.get_brightness_response_cls, check_map=check_map)

        if self.kosmos.discover_emulator(emulation_type=DeviceFamilyName.GENERIC_LED_SPY):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the illumination is OFF from the result of LED Spy/Monitoring")
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.check_fixed_effect(
                test_case=self, red_value=0xFF, green_value=0xFF, blue_value=0xFF,
                brightness=self.config.F_MinBrightness,
                calibration_data=self.calibration_data,
                check_last_packet_only=True,
                cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setBrightness request to change the brightness to zero")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.set_brightness(test_case=self, brightness=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setIllumination request to set the illumination state ON")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.set_illumination(test_case=self, state=IlluminationState.ON)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getBrightness request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_brightness(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the brightness is not changed from the response of getBrightness")
        # --------------------------------------------------------------------------------------------------------------
        checker = BrightnessControlTestUtils.GetBrightnessResponseChecker
        check_map = checker.get_check_map(brightness=0)
        checker.check_fields(test_case=self, message=response,
                             expected_cls=self.feature_8040.get_brightness_response_cls, check_map=check_map)

        if self.kosmos.discover_emulator(emulation_type=DeviceFamilyName.GENERIC_LED_SPY):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the illumination is OFF from the result of LED Spy/Monitoring")
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.check_fixed_effect(
                test_case=self, red_value=0xFF, green_value=0xFF, blue_value=0xFF,
                brightness=self.config.F_MinBrightness,
                calibration_data=self.calibration_data,
                check_last_packet_only=True,
                cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)
        # end if

        self.testCaseChecked("FUN_8040_0011", _AUTHOR)
    # end def test_brightness_not_changed_after_changing_illumination_state

    @features("Feature8040v1")
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.ILLUMINATION)
    @level("Functionality")
    def test_illumination_not_changed_after_changing_brightness(self):
        """
        If the illumination capability is set, validate the illumination state is not changed when changing the
        brightness value
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setIllumination request to set the illumination state OFF")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.set_illumination(test_case=self, state=IlluminationState.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setBrightness request to change the brightness to a non-zero value")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.set_brightness(test_case=self, brightness=self.config.F_MaxBrightness)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getIllumination request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_illumination(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the illumination state is not ON")
        # --------------------------------------------------------------------------------------------------------------
        checker = BrightnessControlTestUtils.GetIlluminationResponseChecker
        check_map = checker.get_check_map(illumination_state=IlluminationState.OFF)
        checker.check_fields(test_case=self, message=response,
                             expected_cls=self.feature_8040.get_illumination_response_cls, check_map=check_map)

        if self.kosmos.discover_emulator(emulation_type=DeviceFamilyName.GENERIC_LED_SPY):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the illumination is OFF from the result of LED Spy/Monitoring")
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.check_fixed_effect(
                test_case=self, red_value=0xFF, green_value=0xFF, blue_value=0xFF,
                brightness=self.config.F_MinBrightness,
                calibration_data=self.calibration_data,
                check_last_packet_only=True,
                cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setIllumination request to set the illumination state ON")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.set_illumination(test_case=self, state=IlluminationState.ON)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setBrightness request to change the brightness to zero")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.set_brightness(test_case=self, brightness=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getIllumination request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_illumination(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the illumination state is not OFF")
        # --------------------------------------------------------------------------------------------------------------
        checker = BrightnessControlTestUtils.GetIlluminationResponseChecker
        check_map = checker.get_check_map(illumination_state=IlluminationState.ON)
        checker.check_fields(test_case=self, message=response,
                             expected_cls=self.feature_8040.get_illumination_response_cls, check_map=check_map)

        if self.kosmos.discover_emulator(emulation_type=DeviceFamilyName.GENERIC_LED_SPY):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the illumination is OFF from the result of LED Spy/Monitoring")
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.check_fixed_effect(
                test_case=self, red_value=0xFF, green_value=0xFF, blue_value=0xFF,
                brightness=self.config.F_MinBrightness,
                calibration_data=self.calibration_data,
                check_last_packet_only=True,
                cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)
        # end if

        self.testCaseChecked("FUN_8040_0012", _AUTHOR)
    # end def test_illumination_not_changed_after_changing_brightness

    @features("Feature8040v1")
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.ILLUMINATION)
    @level("Functionality")
    def test_illumination_state_persistence_after_power_cycle(self):
        """
        If the illumination capability is set, check that the illumination state is persistence/reset across power cycle

        NB: If transient is set, the settings shall be reset, otherwise persistence.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setBrightness request to change the brightness to a non-zero value")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.set_brightness(test_case=self, brightness=self.config.F_MaxBrightness)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setIllumination request to set the illumination state OFF")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.set_illumination(test_case=self, state=IlluminationState.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power OFF -> ON the DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getIllumination request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_illumination(test_case=self)

        expected_illumination_state = self.config.F_DefaultIlluminationState if \
            HexList(self.config.F_Capabilities).testBit(CapabilitiesV1.POS.TRANSIENT) else IlluminationState.OFF
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Check the illumination is {expected_illumination_state} from the response of getIllumination")
        # --------------------------------------------------------------------------------------------------------------
        checker = BrightnessControlTestUtils.GetIlluminationResponseChecker
        check_map = checker.get_check_map(illumination_state=expected_illumination_state)
        checker.check_fields(test_case=self, message=response,
                             expected_cls=self.feature_8040.get_illumination_response_cls, check_map=check_map)

        if self.kosmos.discover_emulator(emulation_type=DeviceFamilyName.GENERIC_LED_SPY):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the illumination is OFF from the result of LED Spy/Monitoring")
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.check_fixed_effect(
                test_case=self, red_value=0xFF, green_value=0xFF, blue_value=0xFF,
                brightness=self.config.F_MinBrightness,
                calibration_data=self.calibration_data,
                check_last_packet_only=True,
                cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setIllumination request to set the illumination state ON")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.set_illumination(test_case=self, state=IlluminationState.ON)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power OFF -> ON the DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getIllumination request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_illumination(test_case=self)

        expected_illumination_state = self.config.F_DefaultIlluminationState if \
            HexList(self.config.F_Capabilities).testBit(CapabilitiesV1.POS.TRANSIENT) else IlluminationState.ON
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Check the illumination is {expected_illumination_state} from the response of getIllumination")
        # --------------------------------------------------------------------------------------------------------------
        checker = BrightnessControlTestUtils.GetIlluminationResponseChecker
        check_map = checker.get_check_map(illumination_state=expected_illumination_state)
        checker.check_fields(test_case=self, message=response,
                             expected_cls=self.feature_8040.get_illumination_response_cls, check_map=check_map)

        if self.kosmos.discover_emulator(emulation_type=DeviceFamilyName.GENERIC_LED_SPY):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the illumination is ON from the result of LED Spy/Monitoring")
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.check_fixed_effect(
                test_case=self, red_value=0xFF, green_value=0xFF, blue_value=0xFF,
                brightness=self.config.F_DefaultBrightness,
                calibration_data=self.calibration_data,
                check_last_packet_only=True,
                cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)
        # end if

        self.testCaseChecked("FUN_8040_0013", _AUTHOR)
    # end def test_illumination_state_persistence_after_power_cycle

    @features("Feature8040v1")
    @features("Feature1830")
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.ILLUMINATION)
    @level("Functionality")
    def test_illumination_state_persistence_after_deep_sleep(self):
        """
        If the illumination capability is set, check that the illumination state is persistence/reset when resuming from
        deep sleep

        NB: If transient is set, the settings shall be reset, otherwise persistence.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setBrightness request to change the brightness to a non-zero value")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.set_brightness(test_case=self, brightness=self.config.F_MaxBrightness)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setIllumination request to set the illumination state OFF")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.set_illumination(test_case=self, state=IlluminationState.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send 0x1830.SetPowerMode with PowerModeNum=3(deep-sleep)")
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform an user action to wake-up the DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getIllumination request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_illumination(test_case=self)

        expected_illumination_state = self.config.F_DefaultIlluminationState if \
            HexList(self.config.F_Capabilities).testBit(CapabilitiesV1.POS.TRANSIENT) else IlluminationState.OFF
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Check the illumination is {expected_illumination_state} from the response of getIllumination")
        # --------------------------------------------------------------------------------------------------------------
        checker = BrightnessControlTestUtils.GetIlluminationResponseChecker
        check_map = checker.get_check_map(illumination_state=expected_illumination_state)
        checker.check_fields(test_case=self, message=response,
                             expected_cls=self.feature_8040.get_illumination_response_cls, check_map=check_map)

        if self.kosmos.discover_emulator(emulation_type=DeviceFamilyName.GENERIC_LED_SPY):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the illumination is OFF from the result of LED Spy/Monitoring")
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.check_fixed_effect(
                test_case=self, red_value=0xFF, green_value=0xFF, blue_value=0xFF,
                brightness=self.config.F_MinBrightness,
                calibration_data=self.calibration_data,
                check_last_packet_only=True,
                cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setIllumination request to set the illumination state ON")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.set_illumination(test_case=self, state=IlluminationState.ON)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send 0x1830.SetPowerMode with PowerModeNum=3(deep-sleep)")
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform an user action to wake-up the DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getIllumination request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_illumination(test_case=self)

        expected_illumination_state = self.config.F_DefaultIlluminationState if \
            HexList(self.config.F_Capabilities).testBit(CapabilitiesV1.POS.TRANSIENT) else IlluminationState.ON
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Check the illumination is {expected_illumination_state} from the response of getIllumination")
        # --------------------------------------------------------------------------------------------------------------
        checker = BrightnessControlTestUtils.GetIlluminationResponseChecker
        check_map = checker.get_check_map(illumination_state=expected_illumination_state)
        checker.check_fields(test_case=self, message=response,
                             expected_cls=self.feature_8040.get_illumination_response_cls, check_map=check_map)

        if self.kosmos.discover_emulator(emulation_type=DeviceFamilyName.GENERIC_LED_SPY):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the illumination is ON from the result of LED Spy/Monitoring")
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.check_fixed_effect(
                test_case=self, red_value=0xFF, green_value=0xFF, blue_value=0xFF,
                brightness=self.config.F_MaxBrightness,
                calibration_data=self.calibration_data,
                check_last_packet_only=True,
                cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)
        # end if

        self.testCaseChecked("FUN_8040_0014", _AUTHOR)
    # end def test_illumination_state_persistence_after_deep_sleep

    @features("Feature8040")
    @features("Feature1805")
    @level("Functionality")
    def test_brightness_and_illumination_reset_after_setting_oob(self):
        """
        Check the brightness and illumination state is reset after setting OOB
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setBrightness request to change the brightness to a non-default value")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.set_brightness(
            test_case=self,
            brightness=self.config.F_MinBrightness
            if self.config.F_DefaultBrightness == self.config.F_MaxBrightness else self.config.F_MaxBrightness)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setIllumination request to set the illumination state to non-default value")
        # --------------------------------------------------------------------------------------------------------------
        if HexList(self.config.F_Capabilities).testBit(CapabilitiesV1.POS.ILLUMINATION):
            BrightnessControlTestUtils.HIDppHelper.set_illumination(test_case=self,
                                                                    state=not self.config.F_DefaultIlluminationState)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable hidden features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set device OOB by 0x1805")
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.HIDppHelper.set_oob_state(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform a device hardware reset")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getBrightness request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_brightness(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the brightness is reset to default value from the response of getBrightness")
        # --------------------------------------------------------------------------------------------------------------
        checker = BrightnessControlTestUtils.GetBrightnessResponseChecker
        check_map = checker.get_check_map(brightness=self.config.F_DefaultBrightness)
        checker.check_fields(test_case=self, message=response,
                             expected_cls=self.feature_8040.get_brightness_response_cls, check_map=check_map)

        if HexList(self.config.F_Capabilities).testBit(CapabilitiesV1.POS.ILLUMINATION):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send getIllumination request")
            # ----------------------------------------------------------------------------------------------------------
            response = BrightnessControlTestUtils.GetIlluminationResponseChecker

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the illumination is reset to default value from the response of"
                                      "getIllumination")
            # ----------------------------------------------------------------------------------------------------------
            checker = BrightnessControlTestUtils.GetIlluminationResponseChecker
            check_map = checker.get_check_map(illumination_state=self.config.F_DefaultIlluminationState)
            checker.check_fields(test_case=self, message=response,
                                 expected_cls=self.feature_8040.get_illumination_response_cls, check_map=check_map)
        # end if

        self.testCaseChecked("FUN_8040_0015", _AUTHOR)
    # end def test_brightness_and_illumination_reset_after_setting_oob
# end class BrightnessControlFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
