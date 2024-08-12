#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_80a4.robustness
:brief: HID++ 2.0 ``AxisResponseCurve`` robustness test suite
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/06/04
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.axisresponsecurve import AxisResponseCurve
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.axisresponsecurveutils import AxisResponseCurveTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.hidpp20.gaming.feature_80a4.axisresponsecurve import AxisResponseCurveTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vasudev Mukkamala"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AxisResponseCurveRobustnessTestCase(AxisResponseCurveTestCase):
    """
    Validate ``AxisResponseCurve`` robustness test cases
    """

    @features("Feature80A4")
    @level("Robustness")
    def test_get_info_software_id(self):
        """
        Validate ``GetInfo`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(AxisResponseCurve.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetInfo request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_80a4.get_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_80a4_index)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_80a4.get_info_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AxisResponseCurveTestUtils.GetInfoResponseChecker
            checker.check_fields(self, response, self.feature_80a4.get_info_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_80A4_0001", _AUTHOR)
    # end def test_get_info_software_id

    @features("Feature80A4")
    @level("Robustness")
    def test_get_axis_info_software_id(self):
        """
        Validate ``GetAxisInfo`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.AxisIndex.0xPP.0xPP

        SwID boundary values [0..F]
        """
        axis_index = HexList(self.axis_value[0])
        hid_usage_page = HexList(self.config.F_HidUsagePage)
        hid_usage = HexList(self.config.F_HidUsage[int(Numeral(axis_index))])
        axis_resolution = HexList(self.config.F_AxisResolution)
        active_point_count = HexList("0000")
        max_point_count = HexList(self.config.F_MaxPointCount)
        properties = HexList(self.config.F_Properties)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(AxisResponseCurve.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetAxisInfo request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_80a4.get_axis_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_80a4_index,
                axis_index=axis_index)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_80a4.get_axis_info_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetAxisInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AxisResponseCurveTestUtils.GetAxisInfoResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "axis_index": (checker.check_axis_index, axis_index),
                "hid_usage_page": (checker.check_hid_usage_page, hid_usage_page),
                "hid_usage": (checker.check_hid_usage, hid_usage),
                "axis_resolution": (checker.check_axis_resolution, axis_resolution),
                "active_point_count": (checker.check_active_point_count, active_point_count),
                "max_point_count": (checker.check_max_point_count, max_point_count),
                "properties": (checker.check_properties, properties),
            })
            checker.check_fields(self, response, self.feature_80a4.get_axis_info_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_80A4_0002", _AUTHOR)
    # end def test_get_axis_info_software_id

    @features("Feature80A4")
    @level("Robustness")
    def test_get_axis_points_software_id(self):
        """
        Validate ``GetAxisPoints`` software id field is ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.AxisIndex.PointIndex.PointCount.0xPP.0xPP.0xPP.0xPP.

        0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        self.post_requisite_reload_nvs = True
        axis_index = HexList(self.axis_value[0])
        point_index = HexList(self.config.F_PointIndex)
        point_count = HexList(self.config.F_PointCount[3])
        axis_points = HexList('0000 0013 0059 0123 FFFF FFFA')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(AxisResponseCurve.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StartUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.start_update(self, axis_index=axis_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetAxisPoints request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.set_axis_points(self, point_count=point_count,
                                                                   axis_points=axis_points)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StopUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.stop_update(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetAxisPoints request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_80a4.get_axis_points_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_80a4_index,
                axis_index=axis_index,
                point_index=point_index,
                point_count=point_count)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_80a4.get_axis_points_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetAxisPointsResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AxisResponseCurveTestUtils.GetAxisPointsResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "axis_index": (checker.check_axis_index, axis_index),
                "point_index": (checker.check_point_index, point_index),
                "point_count": (checker.check_point_count, point_count),
                "axis_points": (checker.check_axis_points, axis_points),
            })
            checker.check_fields(self, response, self.feature_80a4.get_axis_points_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_80A4_0003", _AUTHOR)
    # end def test_get_axis_points_software_id

    @features("Feature80A4")
    @level("Robustness")
    def test_start_update_software_id(self):
        """
        Validate ``StartUpdate`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.AxisIndex.0xPP.0xPP

        SwID boundary values [0..F]
        """
        self.post_requisite_reload_nvs = True
        axis_index = HexList(self.axis_value[0])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(AxisResponseCurve.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send StartUpdate request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_80a4.start_update_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_80a4_index,
                axis_index=axis_index)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_80a4.start_update_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StopUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.stop_update(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check StartUpdateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(self, response, self.feature_80a4.start_update_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_80A4_0004", _AUTHOR)
    # end def test_start_update_software_id

    @features("Feature80A4")
    @level("Robustness")
    def test_set_axis_points_software_id(self):
        """
        Validate ``SetAxisPoints`` software id field is ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.PointCount.AxisPoints.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        self.post_requisite_reload_nvs = True
        point_count = HexList('03')
        axis_points = HexList('0000 0013 0059 0123 FFFF FFFA')
        axis_index = HexList(self.axis_value[0])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(AxisResponseCurve.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StartUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.start_update(self, axis_index=axis_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetAxisPoints request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_80a4.set_axis_points_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_80a4_index,
                point_count=point_count,
                axis_points=axis_points)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_80a4.set_axis_points_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StopUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_80a4.stop_update_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_80a4_index)
            ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_80a4.stop_update_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetAxisPointsResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(self, response, self.feature_80a4.set_axis_points_response_cls,
                                                        {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_80A4_0005", _AUTHOR)
    # end def test_set_axis_points_software_id

    @features("Feature80A4")
    @level("Robustness")
    def test_stop_update_software_id(self):
        """
        Validate ``StopUpdate`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        self.post_requisite_reload_nvs = True
        status = HexList("00")
        point_count = HexList('03')
        axis_points = HexList('0000 0013 0059 0123 FFFF FFFA')
        active_point_count = HexList(self.config.F_ActivePointCount)
        axis_index = HexList(self.axis_value[0])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(AxisResponseCurve.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StartUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.start_update(self, axis_index=axis_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetAxisPoints request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.set_axis_points(self, point_count=point_count,
                                                                   axis_points=axis_points)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send StopUpdate request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_80a4.stop_update_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_80a4_index)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_80a4.stop_update_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check StopUpdateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AxisResponseCurveTestUtils.StopUpdateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "axis_index": (checker.check_axis_index, axis_index),
                "status": (checker.check_status, status),
                "active_point_count": (checker.check_active_point_count, active_point_count),
            })
            checker.check_fields(self, response, self.feature_80a4.stop_update_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_80A4_0006", _AUTHOR)
    # end def test_stop_update_software_id

    @features("Feature80A4")
    @level("Robustness")
    def test_reset_axis_software_id(self):
        """
        Validate ``ResetAxis`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.AxisIndex.0xPP.0xPP

        SwID boundary values [0..F]
        """
        self.post_requisite_reload_nvs = True
        axis_index = HexList(self.axis_value[0])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(AxisResponseCurve.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ResetAxis request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_80a4.reset_axis_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_80a4_index,
                axis_index=axis_index)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_80a4.reset_axis_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ResetAxisResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(self, response, self.feature_80a4.reset_axis_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_80A4_0007", _AUTHOR)
    # end def test_reset_axis_software_id

    @features("Feature80A4")
    @level("Robustness")
    def test_get_calculated_value_software_id(self):
        """
        Validate ``GetCalculatedValue`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.AxisIndex.InputValue

        SwID boundary values [0..F]
        """
        axis_index = HexList(self.axis_value[0])
        input_value = HexList("0000")
        calculated_value = HexList("0000")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(AxisResponseCurve.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCalculatedValue request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_80a4.get_calculated_value_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_80a4_index,
                axis_index=axis_index,
                input_value=input_value)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_80a4.get_calculated_value_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCalculatedValueResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AxisResponseCurveTestUtils.GetCalculatedValueResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "axis_index": (checker.check_axis_index, axis_index),
                "input_value": (checker.check_input_value, input_value),
                "calculated_value": (checker.check_calculated_value, calculated_value),
            })
            checker.check_fields(self, response, self.feature_80a4.get_calculated_value_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_80A4_0008", _AUTHOR)
    # end def test_get_calculated_value_software_id

    @features("Feature80A4")
    @level("Robustness")
    def test_get_info_padding(self):
        """
        Validate ``GetInfo`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_80a4.get_info_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetInfo request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_80a4.get_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_80a4_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_80a4.get_info_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AxisResponseCurveTestUtils.GetInfoResponseChecker
            checker.check_fields(self, response, self.feature_80a4.get_info_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_80A4_0009", _AUTHOR)
    # end def test_get_info_padding

    @features("Feature80A4")
    @level("Robustness")
    def test_get_axis_info_padding(self):
        """
        Validate ``GetAxisInfo`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.AxisIndex.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        axis_index = HexList(self.axis_value[0])
        hid_usage_page = HexList(self.config.F_HidUsagePage)
        hid_usage = HexList(self.config.F_HidUsage[int(Numeral(axis_index))])
        axis_resolution = HexList(self.config.F_AxisResolution)
        active_point_count = HexList("0000")
        max_point_count = HexList(self.config.F_MaxPointCount)
        properties = HexList(self.config.F_Properties)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_80a4.get_axis_info_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetAxisInfo request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_80a4_index,
                axis_index=axis_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_80a4.get_axis_info_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetAxisInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AxisResponseCurveTestUtils.GetAxisInfoResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "axis_index": (checker.check_axis_index, axis_index),
                "hid_usage_page": (checker.check_hid_usage_page, hid_usage_page),
                "hid_usage": (checker.check_hid_usage, hid_usage),
                "axis_resolution": (checker.check_axis_resolution, axis_resolution),
                "active_point_count": (checker.check_active_point_count, active_point_count),
                "max_point_count": (checker.check_max_point_count, max_point_count),
                "properties": (checker.check_properties, properties),
            })
            checker.check_fields(self, response, self.feature_80a4.get_axis_info_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_80A4_0010", _AUTHOR)
    # end def test_get_axis_info_padding

    @features("Feature80A4")
    @level("Robustness")
    def test_get_axis_points_padding(self):
        """
        Validate ``GetAxisPoints`` padding bytes are ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.AxisIndex.PointIndex.PointCount.0xPP.0xPP.0xPP.0xPP.

        0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        self.post_requisite_reload_nvs = True
        axis_index = HexList(self.axis_value[0])
        point_index = HexList(self.config.F_PointIndex)
        point_count = HexList(self.config.F_PointCount[3])
        axis_points = HexList('0000 0013 0059 0123 FFFF FFFA')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_80a4.get_axis_points_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StartUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.start_update(self, axis_index=axis_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetAxisPoints request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.set_axis_points(self, point_count=point_count,
                                                                   axis_points=axis_points)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StopUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.stop_update(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetAxisPoints request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_80a4_index,
                axis_index=axis_index,
                point_index=point_index,
                point_count=point_count)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_80a4.get_axis_points_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetAxisPointsResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AxisResponseCurveTestUtils.GetAxisPointsResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "axis_index": (checker.check_axis_index, axis_index),
                "point_index": (checker.check_point_index, point_index),
                "point_count": (checker.check_point_count, point_count),
                "axis_points": (checker.check_axis_points, axis_points),
            })
            checker.check_fields(self, response, self.feature_80a4.get_axis_points_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_80A4_0011", _AUTHOR)
    # end def test_get_axis_points_padding

    @features("Feature80A4")
    @level("Robustness")
    def test_start_update_padding(self):
        """
        Validate ``StartUpdate`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.AxisIndex.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        self.post_requisite_reload_nvs = True
        axis_index = HexList(self.axis_value[0])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_80a4.start_update_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send StartUpdate request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_80a4_index,
                axis_index=axis_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_80a4.start_update_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StopUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.stop_update(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check StartUpdateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(self, response, self.feature_80a4.start_update_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_80A4_0012", _AUTHOR)
    # end def test_start_update_padding

    @features("Feature80A4")
    @level("Robustness")
    def test_set_axis_points_padding(self):
        """
        Validate ``SetAxisPoints`` padding bytes are ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.PointCount.AxisPoints.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        self.post_requisite_reload_nvs = True
        point_index = HexList(self.config.F_PointIndex)
        axis_points = HexList('0000 0013 0059 0123 FFFF FFFA')
        point_count = HexList(self.config.F_PointCount[3])
        for axis_index in [HexList(i) for i in range(self.config.F_AxisCount)]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send ResetAxis request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.reset_axis(self, axis_index=axis_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, _LOOP_START_PADDING + f" for axis index:{axis_index}")
            # ----------------------------------------------------------------------------------------------------------
            request_cls = self.feature_80a4.set_axis_points_cls
            for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING,
                                                              request_cls.LEN.PADDING // 8))):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send StartUpdate request")
                # ------------------------------------------------------------------------------------------------------
                AxisResponseCurveTestUtils.HIDppHelper.start_update(self, axis_index=axis_index)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send SetAxisPoints request with padding: {padding}")
                # ------------------------------------------------------------------------------------------------------
                report = request_cls(
                    device_index=ChannelUtils.get_device_index(test_case=self),
                    feature_index=self.feature_80a4_index,
                    point_count=point_count,
                    axis_points=axis_points)
                report.padding = padding
                ChannelUtils.send(
                    test_case=self,
                    report=report,
                    response_queue_name=HIDDispatcher.QueueName.GAMING,
                    response_class_type=self.feature_80a4.set_axis_points_response_cls)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send StopUpdate request")
                # ------------------------------------------------------------------------------------------------------
                AxisResponseCurveTestUtils.HIDppHelper.stop_update(self)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send GetAxisInfo request")
                # ------------------------------------------------------------------------------------------------------
                get_axis_points_response = AxisResponseCurveTestUtils.HIDppHelper.get_axis_points(
                    self, axis_index=axis_index,
                    point_index=point_index,
                    point_count=point_count)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Validate GetAxisInfoResponse.axis_point value")
                # ------------------------------------------------------------------------------------------------------
                for i in range(0, 2):
                    self.assertEqual(expected=axis_points[(i * 4) + 2:(i * 4) + 4],
                                     obtained=get_axis_points_response.axis_points[(i * 4) + 2:(i * 4) + 4],
                                     msg="value obtained from GetAxisPoints is not as Expected")
                # end for
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, _LOOP_END + f" for axis index:{axis_index}")
            # ----------------------------------------------------------------------------------------------------------
        # end for

        self.testCaseChecked("ROB_80A4_0013", _AUTHOR)
    # end def test_set_axis_points_padding

    @features("Feature80A4")
    @level("Robustness")
    def test_stop_update_padding(self):
        """
        Validate ``StopUpdate`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        self.post_requisite_reload_nvs = True
        status = HexList("00")
        point_count = HexList('03')
        axis_points = HexList('0000 0013 0059 0123 FFFF FFFA')
        active_point_count = HexList(self.config.F_ActivePointCount)
        axis_index = HexList(self.axis_value[0])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_80a4.stop_update_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StartUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.start_update(self, axis_index=axis_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetAxisPoints request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.set_axis_points(self, point_count=point_count,
                                                                   axis_points=axis_points)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send StopUpdate request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_80a4_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_80a4.stop_update_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check StopUpdateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AxisResponseCurveTestUtils.StopUpdateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "axis_index": (checker.check_axis_index, axis_index),
                "status": (checker.check_status, status),
                "active_point_count": (checker.check_active_point_count, active_point_count),
            })
            checker.check_fields(self, response, self.feature_80a4.stop_update_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_80A4_0014", _AUTHOR)
    # end def test_stop_update_padding

    @features("Feature80A4")
    @level("Robustness")
    def test_reset_axis_padding(self):
        """
        Validate ``ResetAxis`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.AxisIndex.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        self.post_requisite_reload_nvs = True
        axis_index = HexList(self.axis_value[0])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_80a4.reset_axis_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ResetAxis request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_80a4.reset_axis_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_80a4_index,
                axis_index=axis_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_80a4.reset_axis_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ResetAxisResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(self, response, self.feature_80a4.reset_axis_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_80A4_0015", _AUTHOR)
    # end def test_reset_axis_padding
# end class AxisResponseCurveRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
