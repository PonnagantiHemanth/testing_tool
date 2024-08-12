#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.gaming.feature_8090.robustness
:brief: HID++ 2.0 ``ModeStatus`` robustness test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2022/08/30
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.modestatus import ModeStatus
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.modestatusutils import ModeStatusTestUtils
from pytestbox.device.hidpp20.gaming.feature_8090.modestatus import ModeStatusTestCase

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
class ModeStatusRobustnessTestCase(ModeStatusTestCase):
    """
    Validate ``ModeStatus`` robustness test cases
    """

    @features("Feature8090")
    @level("Robustness")
    def test_get_mode_status_software_id(self):
        """
        Validate ``GetModeStatus`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ModeStatus.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetModeStatus request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8090.get_mode_status_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8090_index)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_8090.get_mode_status_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetModeStatusResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ModeStatusTestUtils.GetModeStatusResponseChecker.check_fields(
                self, response, self.feature_8090.get_mode_status_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8090_0001#1", _AUTHOR)
    # end def test_get_mode_status_software_id

    @features("Feature8090")
    @level("Robustness")
    def test_set_mode_status_software_id(self):
        """
        Validate ``SetModeStatus`` software id field is ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.ModeStatus0.ModeStatus1.ChangedMask0.ChangedMask1.
        0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        self.post_requisite_reload_nvs = True
        changed_mask_0 = 1 if self.config.F_ModeStatus0ChangedBySw else 0
        changed_mask_1 = self.config.F_PowerSaveModeSupported + \
            (self.config.F_NonGamingSurfaceModeSupported << 1)
        mode_status_0 = (0xFF - to_int(self.config.F_ModeStatus0)) & changed_mask_0
        mode_status_1 = (0xFF - to_int(self.config.F_ModeStatus1)) & changed_mask_1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ModeStatus.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetModeStatus request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8090.set_mode_status_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8090_index,
                mode_status_0=mode_status_0,
                mode_status_1=mode_status_1,
                changed_mask_0=changed_mask_0,
                changed_mask_1=changed_mask_1)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_8090.set_mode_status_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetModeStatusResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(
                self, response, self.feature_8090.set_mode_status_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8090_0001#2", _AUTHOR)
    # end def test_set_mode_status_software_id

    @features("Feature8090")
    @level("Robustness")
    def test_get_dev_config_software_id(self):
        """
        Validate ``GetDevConfig`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ModeStatus.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetDevConfig request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8090.get_dev_config_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8090_index)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_8090.get_dev_config_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetDevConfigResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ModeStatusTestUtils.GetDevConfigResponseChecker.check_fields(
                self, response, self.feature_8090.get_dev_config_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8090_0001#3", _AUTHOR)
    # end def test_get_dev_config_software_id

    @features("Feature8090")
    @level("Robustness")
    def test_get_mode_status_padding(self):
        """
        Validate ``GetModeStatus`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8090.get_mode_status_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetModeStatus request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8090_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_8090.get_mode_status_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetModeStatusResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ModeStatusTestUtils.GetModeStatusResponseChecker.check_fields(
                self, response, self.feature_8090.get_mode_status_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8090_0002#1", _AUTHOR)
    # end def test_get_mode_status_padding

    @features("Feature8090")
    @level("Robustness")
    def test_set_mode_status_padding(self):
        """
        Validate ``SetModeStatus`` padding bytes are ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.ModeStatus0.ModeStatus1.ChangedMask0.ChangedMask1.
        0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        self.post_requisite_reload_nvs = True
        changed_mask_0 = 1 if self.config.F_ModeStatus0ChangedBySw else 0
        changed_mask_1 = self.config.F_PowerSaveModeSupported + \
            (self.config.F_NonGamingSurfaceModeSupported << 1)
        mode_status_0 = (0xFF - to_int(self.config.F_ModeStatus0)) & changed_mask_0
        mode_status_1 = (0xFF - to_int(self.config.F_ModeStatus1)) & changed_mask_1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8090.set_mode_status_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetModeStatus request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8090_index,
                mode_status_0=mode_status_0,
                mode_status_1=mode_status_1,
                changed_mask_0=changed_mask_0,
                changed_mask_1=changed_mask_1)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_8090.set_mode_status_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetModeStatusResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(
                self, response, self.feature_8090.set_mode_status_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8090_0002#2", _AUTHOR)
    # end def test_set_mode_status_padding

    @features("Feature8090")
    @level("Robustness")
    def test_get_dev_config_padding(self):
        """
        Validate ``GetDevConfig`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8090.get_dev_config_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetDevConfig request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8090_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_8090.get_dev_config_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetDevConfigResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ModeStatusTestUtils.GetDevConfigResponseChecker.check_fields(
                self, response, self.feature_8090.get_dev_config_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8090_0002#3", _AUTHOR)
    # end def test_get_dev_config_padding

    @features("Feature8090")
    @level("Robustness")
    def test_dev_config_not_changed_after_setting_mode_status_by_sw(self):
        """
        Validate DevCapability is not going to change while the ModeStatus0, 1 is changed by setModeStatus request
        """
        self.post_requisite_reload_nvs = True
        changed_mask_0 = 1 if self.config.F_ModeStatus0ChangedBySw else 0
        changed_mask_1 = self.config.F_PowerSaveModeSupported + \
            (self.config.F_NonGamingSurfaceModeSupported << 1)
        mode_status_0 = (0xFF - to_int(self.config.F_ModeStatus0)) & changed_mask_0
        mode_status_1 = (0xFF - to_int(self.config.F_ModeStatus1)) & changed_mask_1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setModeStatus request with ModeStatus0 = 1 (Performance mode), "
                                 "ModeStatus1 = 0 (Low latency mode)")
        # --------------------------------------------------------------------------------------------------------------
        response = ModeStatusTestUtils.HIDppHelper.set_mode_status(test_case=self,
                                                                   mode_status_0=mode_status_0,
                                                                   mode_status_1=mode_status_1,
                                                                   changed_mask_0=changed_mask_0,
                                                                   changed_mask_1=changed_mask_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait setModeStatus response and check its inputs fields are as expected")
        # --------------------------------------------------------------------------------------------------------------
        ModeStatusTestUtils.MessageChecker.check_fields(
            self, response, self.feature_8090.set_mode_status_response_cls, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getDevConfig request")
        # --------------------------------------------------------------------------------------------------------------
        response = ModeStatusTestUtils.HIDppHelper.get_dev_config(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getDevConfig response and check DevConfig are as expected (Product capability)")
        # --------------------------------------------------------------------------------------------------------------
        ModeStatusTestUtils.GetDevConfigResponseChecker.check_fields(
            self, response, self.feature_8090.get_dev_config_response_cls)

        self.testCaseChecked("ROB_8090_0003", _AUTHOR)
    # end def test_dev_config_not_changed_after_setting_mode_status_by_sw
# end class ModeStatusRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
