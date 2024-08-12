#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.mouse.feature_2150.robustness
:brief: HID++ 2.0 ``Thumbwheel`` robustness test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/12/14
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import skip

from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.mouse.thumbwheel import Thumbwheel
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.thumbwheelutils import ThumbwheelTestUtils
from pytestbox.device.hidpp20.mouse.feature_2150.thumbwheel import ThumbwheelTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ThumbwheelRobustnessTestCase(ThumbwheelTestCase):
    """
    Validate ``Thumbwheel`` robustness test cases
    """

    @features("Feature2150")
    @level("Robustness")
    def test_get_thumbwheel_info_software_id(self):
        """
        Validate ``GetThumbwheelInfo`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(Thumbwheel.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetThumbwheelInfo request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_2150.get_thumbwheel_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2150_index)
            report.software_id = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2150.get_thumbwheel_info_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetThumbwheelInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ThumbwheelTestUtils.GetThumbwheelInfoResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_2150.get_thumbwheel_info_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2150_0001#1", _AUTHOR)
    # end def test_get_thumbwheel_info_software_id

    @features("Feature2150")
    @level("Robustness")
    def test_get_thumbwheel_status_software_id(self):
        """
        Validate ``GetThumbwheelStatus`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(Thumbwheel.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetThumbwheelStatus request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_2150.get_thumbwheel_status_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2150_index)
            report.software_id = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2150.get_thumbwheel_status_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetThumbwheelStatusResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ThumbwheelTestUtils.GetThumbwheelStatusResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_2150.get_thumbwheel_status_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2150_0001#2", _AUTHOR)
    # end def test_get_thumbwheel_status_software_id

    @features("Feature2150")
    @level("Robustness")
    def test_set_thumbwheel_reporting_software_id(self):
        """
        Validate ``SetThumbwheelReporting`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.ReportingMode.InvertMaskBitMap.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        reporting_mode = Thumbwheel.REPORTING_MODE.HID
        invert_direction = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(Thumbwheel.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetThumbwheelReporting request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_2150.set_thumbwheel_reporting_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2150_index,
                reporting_mode=reporting_mode,
                invert_direction=invert_direction)
            report.software_id = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2150.set_thumbwheel_reporting_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetThumbwheelReportingResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(
                self, response, self.feature_2150.set_thumbwheel_reporting_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2150_0001#3", _AUTHOR)
    # end def test_set_thumbwheel_reporting_software_id

    @features("Feature2150")
    @level("Robustness")
    def test_get_thumbwheel_info_padding(self):
        """
        Validate ``GetThumbwheelInfo`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_2150.get_thumbwheel_info_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetThumbwheelInfo request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2150_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2150.get_thumbwheel_info_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetThumbwheelInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ThumbwheelTestUtils.GetThumbwheelInfoResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_2150.get_thumbwheel_info_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2150_0002#1", _AUTHOR)
    # end def test_get_thumbwheel_info_padding

    @features("Feature2150")
    @level("Robustness")
    def test_get_thumbwheel_status_padding(self):
        """
        Validate ``GetThumbwheelStatus`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_2150.get_thumbwheel_status_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetThumbwheelStatus request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2150_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2150.get_thumbwheel_status_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetThumbwheelStatusResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ThumbwheelTestUtils.GetThumbwheelStatusResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_2150.get_thumbwheel_status_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2150_0002#2", _AUTHOR)
    # end def test_get_thumbwheel_status_padding

    @features("Feature2150")
    @level("Robustness")
    def test_set_thumbwheel_reporting_padding(self):
        """
        Validate ``SetThumbwheelReporting`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.ReportingMode.InvertMaskBitMap.0xPP

        Padding (PP) boundary values [00..FF]
        """
        reporting_mode = Thumbwheel.REPORTING_MODE.HID
        invert_direction = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_2150.set_thumbwheel_reporting_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetThumbwheelReporting request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2150_index,
                reporting_mode=reporting_mode,
                invert_direction=invert_direction)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2150.set_thumbwheel_reporting_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetThumbwheelReportingResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(
                self, response, self.feature_2150.set_thumbwheel_reporting_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2150_0002#3", _AUTHOR)
    # end def test_set_thumbwheel_reporting_padding

    @features("Feature2150")
    @level("Robustness")
    @skip("Under development")
    def test_device_behaviour_rotation_angle_above_360(self):
        """
        Validate DUT behaviour when rotation angle is above 360 degree
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "TBA")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "TBA")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2150_0003", _AUTHOR)
    # end def test_device_behaviour_rotation_angle_above_360
# end class ThumbwheelRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
