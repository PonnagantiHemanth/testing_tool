#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1982.robustness
:brief: HID++ 2.0 ``Backlight`` robustness test suite
:author: Anil Gadad <agadad@logitech.com>
:date: 2021/09/29
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.backlight import Backlight
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.backlightutils import BacklightTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.hidpp20.common.feature_1982.backlight import BacklightTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Anil Gadad"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BacklightRobustnessTestCase(BacklightTestCase):
    """
    Validate ``Backlight`` robustness test cases
    """

    @features("Feature1982")
    @level("Robustness")
    def test_get_backlight_config_software_id(self):
        """
        Validate ``GetBacklightConfig`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(Backlight.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetBacklightConfig request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1982.get_backlight_config_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1982_index)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1982.get_backlight_config_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetBacklightConfigResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            BacklightTestUtils.GetBacklightConfigResponseChecker.check_fields(
                self, response, self.feature_1982.get_backlight_config_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1982_0001", _AUTHOR)
    # end def test_get_backlight_config_software_id

    @features("Feature1982")
    @level("Robustness")
    def test_set_backlight_config_software_id(self):
        """
        Validate ``SetBacklightConfig`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.Configuration.Options.BacklightEffect

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        self.post_requisite_reload_nvs = True
        configuration = Backlight.Configuration.DISABLE
        options = BacklightTestUtils.get_default_options(self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(Backlight.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetBacklightConfig request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = BacklightTestUtils.HIDppHelper.set_backlight_config(self, configuration, options,
                                                                           software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetBacklightConfigResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(self, response,
                                                        self.feature_1982.set_backlight_config_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1982_0002", _AUTHOR)
    # end def test_set_backlight_config_software_id

    @features("Feature1982")
    @level("Robustness")
    def test_get_backlight_info_software_id(self):
        """
        Validate ``GetBacklightInfo`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(Backlight.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetBacklightInfo request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1982.get_backlight_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1982_index)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1982.get_backlight_info_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetBacklightInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            BacklightTestUtils.GetBacklightInfoResponseChecker.check_fields(
                self, response, self.feature_1982.get_backlight_info_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1982_0003", _AUTHOR)
    # end def test_get_backlight_info_software_id

    @features("Feature1982v2+")
    @level("Robustness")
    def test_set_backlight_effect_software_id(self):
        """
        Validate ``SetBacklightEffect`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.BacklightEffect.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        self.post_requisite_reload_nvs = True
        backlight_effect = Backlight.BacklightEffect.CURRENT_EFFECT
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(Backlight.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetBacklightEffect request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1982.set_backlight_effect_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1982_index,
                backlight_effect=backlight_effect)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1982.set_backlight_effect_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetBacklightEffectResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(self, response,
                                                        self.feature_1982.set_backlight_effect_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1982_0004", _AUTHOR)
    # end def test_set_backlight_effect_software_id

    @features("Feature1982")
    @level("Robustness")
    def test_get_backlight_config_padding(self):
        """
        Validate ``GetBacklightConfig`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1982.get_backlight_config_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetBacklightConfig request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1982_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1982.get_backlight_config_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetBacklightConfigResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            BacklightTestUtils.GetBacklightConfigResponseChecker.check_fields(
                self, response, self.feature_1982.get_backlight_config_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1982_0005", _AUTHOR)
    # end def test_get_backlight_config_padding

    @features("Feature1982")
    @level("Robustness")
    def test_get_backlight_info_padding(self):
        """
        Validate ``GetBacklightInfo`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1982.get_backlight_info_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetBacklightInfo request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1982_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1982.get_backlight_info_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetBacklightInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            BacklightTestUtils.GetBacklightInfoResponseChecker.check_fields(
                self, response, self.feature_1982.get_backlight_info_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1982_0006", _AUTHOR)
    # end def test_get_backlight_info_padding

    @features("Feature1982v2+")
    @level("Robustness")
    def test_set_backlight_effect_padding(self):
        """
        Validate ``SetBacklightEffect`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.BacklightEffect.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        self.post_requisite_reload_nvs = True
        backlight_effect = Backlight.BacklightEffect.CURRENT_EFFECT
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1982.set_backlight_effect_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetBacklightEffect request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1982_index,
                backlight_effect=backlight_effect)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1982.set_backlight_effect_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetBacklightEffectResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(self, response,
                                                        self.feature_1982.set_backlight_effect_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1982_0007", _AUTHOR)
    # end def test_set_backlight_effect_padding
# end class BacklightRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
