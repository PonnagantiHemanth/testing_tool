#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.gaming.feature_8040.robustness
:brief: HID++ 2.0 ``BrightnessControl`` robustness test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2023/11/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.gaming.brightnesscontrol import BrightnessControl
from pyhid.hidpp.features.gaming.brightnesscontrol import CapabilitiesV1
from pyhid.hidpp.features.gaming.rgbeffects import RGBEffects
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.brightnesscontrolutils import BrightnessControlTestUtils
from pytestbox.device.base.rgbeffectsutils import RGBEffectsTestUtils
from pytestbox.device.hidpp20.gaming.feature_8040.brightnesscontrol import BrightnessControlTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BrightnessControlRobustnessTestCase(BrightnessControlTestCase):
    """
    Validate ``BrightnessControl`` robustness test cases
    """

    @features("Feature8040")
    @level("Robustness")
    def test_get_info_software_id(self):
        """
        Validate ``GetInfo`` software id field is ignored by the firmware

        [0] getInfo() -> maxBrightness, capabilities

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(BrightnessControl.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetInfoV0 request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = BrightnessControlTestUtils.HIDppHelper.get_info(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetInfoResponseV0 fields")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.GetInfoResponseChecker.check_fields(
                self, response, self.feature_8040.get_info_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8040_0001#1", _AUTHOR)
    # end def test_get_info_software_id

    @features("Feature8040")
    @level("Robustness")
    def test_get_brightness_software_id(self):
        """
        Validate ``GetBrightness`` software id field is ignored by the firmware

        [1] getBrightness() -> brightness

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(BrightnessControl.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetBrightness request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = BrightnessControlTestUtils.HIDppHelper.get_brightness(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetBrightnessResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.GetBrightnessResponseChecker.check_fields(
                self, response, self.feature_8040.get_brightness_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8040_0001#2", _AUTHOR)
    # end def test_get_brightness_software_id

    @features("Feature8040")
    @level("Robustness")
    def test_set_brightness_software_id(self):
        """
        Validate ``SetBrightness`` software id field is ignored by the firmware

        [2] setBrightness(brightness) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.Brightness.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(BrightnessControl.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetBrightness request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = BrightnessControlTestUtils.HIDppHelper.set_brightness(
                test_case=self,
                brightness=0,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetBrightnessResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.MessageChecker.check_fields(
                self, response, self.feature_8040.set_brightness_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8040_0001#3", _AUTHOR)
    # end def test_set_brightness_software_id

    @features("Feature8040v1")
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.ILLUMINATION)
    @level("Robustness")
    def test_get_illumination_software_id(self):
        """
        Validate ``GetIllumination`` software id field is ignored by the firmware

        [3] getIllumination() -> state

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(BrightnessControl.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetIllumination request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = BrightnessControlTestUtils.HIDppHelper.get_illumination(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetIlluminationResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.GetIlluminationResponseChecker.check_fields(
                self, response, self.feature_8040.get_illumination_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8040_0001#4", _AUTHOR)
    # end def test_get_illumination_software_id

    @features("Feature8040v1")
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.ILLUMINATION)
    @level("Robustness")
    def test_set_illumination_software_id(self):
        """
        Validate ``SetIllumination`` software id field is ignored by the firmware

        [4] setIllumination(state) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.State.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(BrightnessControl.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetIllumination request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = BrightnessControlTestUtils.HIDppHelper.set_illumination(
                test_case=self,
                state=0,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetIlluminationResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.MessageChecker.check_fields(
                self, response, self.feature_8040.set_illumination_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8040_0001#5", _AUTHOR)
    # end def test_set_illumination_software_id

    @features("Feature8040")
    @level("Robustness")
    def test_get_info_padding(self):
        """
        Validate ``GetInfo`` padding bytes are ignored by the firmware

        [0] getInfo() -> maxBrightness, capabilities

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8040.get_info_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetInfo request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = BrightnessControlTestUtils.HIDppHelper.get_info(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetInfoResponseV0 fields")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.GetInfoResponseChecker.check_fields(
                self, response, self.feature_8040.get_info_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8040_0002#1", _AUTHOR)
    # end def test_get_info_padding

    @features("Feature8040")
    @level("Robustness")
    def test_get_brightness_padding(self):
        """
        Validate ``GetBrightness`` padding bytes are ignored by the firmware

        [1] getBrightness() -> brightness

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8040.get_brightness_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetBrightness request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = BrightnessControlTestUtils.HIDppHelper.get_brightness(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetBrightnessResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.GetBrightnessResponseChecker.check_fields(
                self, response, self.feature_8040.get_brightness_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8040_0002#2", _AUTHOR)
    # end def test_get_brightness_padding

    @features("Feature8040")
    @level("Robustness")
    def test_set_brightness_padding(self):
        """
        Validate ``SetBrightness`` padding bytes are ignored by the firmware

        [2] setBrightness(brightness) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.Brightness.0xPP

        Padding (PP) boundary values [00..FF]
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8040.set_brightness_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetBrightness request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = BrightnessControlTestUtils.HIDppHelper.set_brightness(
                test_case=self,
                brightness=0,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetBrightnessResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.MessageChecker.check_fields(
                self, response, self.feature_8040.set_brightness_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8040_0002#3", _AUTHOR)
    # end def test_set_brightness_padding

    @features("Feature8040v1")
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.ILLUMINATION)
    @level("Robustness")
    def test_get_illumination_padding(self):
        """
        Validate ``GetIllumination`` padding bytes are ignored by the firmware

        [3] getIllumination() -> state

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8040.get_illumination_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetIllumination request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = BrightnessControlTestUtils.HIDppHelper.get_illumination(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetIlluminationResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.GetIlluminationResponseChecker.check_fields(
                self, response, self.feature_8040.get_illumination_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8040_0002#4", _AUTHOR)
    # end def test_get_illumination_padding

    @features("Feature8040v1")
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.ILLUMINATION)
    @level("Robustness")
    def test_set_illumination_padding(self):
        """
        Validate ``SetIllumination`` padding bytes are ignored by the firmware

        [4] setIllumination(state) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.State.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8040.set_illumination_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetIllumination request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = BrightnessControlTestUtils.HIDppHelper.set_illumination(
                test_case=self,
                state=0,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetIlluminationResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.MessageChecker.check_fields(
                self, response, self.feature_8040.set_illumination_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8040_0002#5", _AUTHOR)
    # end def test_set_illumination_padding

    @features("Feature8040v1")
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.ILLUMINATION)
    @level("Robustness")
    def test_reserved_bit_of_state(self):
        """
        Validate Reserved bits of 'state' shall be ignored by the firmware when sending setIllumination request
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop: reserved in sample values(0x02, 0xFE, 0x02)")
        # --------------------------------------------------------------------------------------------------------------
        for reserved in range(0x02, 0xFE, 0x02):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send setIllumination request with state={reserved}")
            # ----------------------------------------------------------------------------------------------------------
            response = BrightnessControlTestUtils.HIDppHelper.set_illumination(
                test_case=self, state=0, reserved=reserved)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check setIllumination response is not affected by reserved")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.MessageChecker.check_fields(
                self, response, self.feature_8040.set_illumination_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8040_0003", _AUTHOR)
    # end def test_reserved_bit_of_state

    @features("Feature8040")
    @features("Feature8071")
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.HW_ON_OFF)
    @level("Robustness")
    def test_no_disabled_effect_implemented(self):
        """
        If the hw_on_off or illumination capability is set, validate Disabled effect is not implemented in 0x8071 on
        the device
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send 0x8071.getInfo to get the rgbClusterCount")
        # --------------------------------------------------------------------------------------------------------------
        device_info = RGBEffectsTestUtils.HIDppHelper.get_info_about_device(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop: cluster_index in range(0x8071.getInfo.rgbClusterCount)")
        # --------------------------------------------------------------------------------------------------------------
        for cluster_index in range(to_int(device_info.rgb_cluster_count)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send 0x8071.getInfo to get the effectsNumber of {cluster_index}")
            # ----------------------------------------------------------------------------------------------------------
            cluster_info = RGBEffectsTestUtils.HIDppHelper.get_info_about_rgb_cluster(test_case=self,
                                                                                      rgb_cluster_index=cluster_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop: effect_id in range(0x8071.getInfo.effectsNumber)")
            # ----------------------------------------------------------------------------------------------------------
            for effect_index in range(to_int(cluster_info.effects_number)):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send 0x8071.getInfo request")
                # ------------------------------------------------------------------------------------------------------
                effect_info = RGBEffectsTestUtils.HIDppHelper.get_info_about_effect_general_info(
                    test_case=self, rgb_cluster_index=cluster_index, rgb_cluster_effect_index=effect_index)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check the effect_id is not {RGBEffects.RGBEffectID.DISABLED}")
                # ------------------------------------------------------------------------------------------------------
                self.assertNotEqual(obtained=to_int(effect_info.effect_id),
                                    unexpected=RGBEffects.RGBEffectID.DISABLED,
                                    msg="The Disable effect shall not be implemented if the hw_on_off or illumination "
                                        "capability is set on the device")

            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8040_0004", _AUTHOR)
    # end def test_no_disabled_effect_implemented
# end class BrightnessControlRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
