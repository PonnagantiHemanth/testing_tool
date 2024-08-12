#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_80a4.interface
:brief: HID++ 2.0 ``AxisResponseCurve`` interface test suite
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/06/04
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.axisresponsecurveutils import AxisResponseCurveTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.hidpp20.gaming.feature_80a4.axisresponsecurve import AxisResponseCurveTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vasudev Mukkamala"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AxisResponseCurveInterfaceTestCase(AxisResponseCurveTestCase):
    """
    Validate ``AxisResponseCurve`` interface test cases
    """

    @features("Feature80A4")
    @level("Interface")
    def test_get_info_interface(self):
        """
        Validate ``GetInfo`` normal processing
        """
        axis_count = HexList(self.config.F_AxisCount)
        max_get_point_count = HexList(self.config.F_MaxGetPointCount)
        max_set_point_count = HexList(self.config.F_MaxSetPointCount)
        capabilities = HexList(self.config.F_Capabilities)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetInfo request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_80a4.get_info_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_80a4_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_80a4.get_info_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetInfoResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = AxisResponseCurveTestUtils.GetInfoResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
            "axis_count": (checker.check_axis_count, axis_count),
            "max_get_point_count": (checker.check_max_get_point_count, max_get_point_count),
            "max_set_point_count": (checker.check_max_set_point_count, max_set_point_count),
        })
        if self.feature_80a4.VERSION > 0:
            check_map.update({"capabilities": (checker.check_capabilities, capabilities)})
        # end if
        checker.check_fields(self, response, self.feature_80a4.get_info_response_cls, check_map)

        self.testCaseChecked("INT_80A4_0001", _AUTHOR)
    # end def test_get_info_interface

    @features("Feature80A4")
    @level("Interface")
    def test_get_axis_info_interface(self):
        """
        Validate ``GetAxisInfo`` normal processing
        """
        self.post_requisite_reload_nvs = True

        axis_index = HexList(self.axis_value[0])
        hid_usage_page = HexList(self.config.F_HidUsagePage)
        hid_usage = HexList(self.config.F_HidUsage[int(Numeral(axis_index))])
        axis_resolution = HexList(self.config.F_AxisResolution)
        active_point_count = HexList("0000")
        max_point_count = HexList(self.config.F_MaxPointCount)
        properties = HexList(self.config.F_Properties)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetAxisInfo request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_80a4.get_axis_info_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_80a4_index,
            axis_index=axis_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_80a4.get_axis_info_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetAxisInfoResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = AxisResponseCurveTestUtils.GetAxisInfoResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
            "axis_index": (checker.check_axis_index, axis_index),
            "hid_usage_page": (checker.check_hid_usage_page, hid_usage_page),
            "hid_usage": (checker.check_hid_usage, hid_usage),
            "axis_resolution": (checker.check_axis_resolution, axis_resolution),
            "active_point_count": (checker.check_active_point_count, active_point_count),
            "max_point_count": (checker.check_max_point_count, max_point_count),
            "properties": (checker.check_properties, properties),
        })
        checker.check_fields(self, response, self.feature_80a4.get_axis_info_response_cls, check_map)

        self.testCaseChecked("INT_80A4_0002", _AUTHOR)
    # end def test_get_axis_info_interface

    @features("Feature80A4")
    @level("Interface")
    def test_get_axis_points_interface(self):
        """
        Validate ``GetAxisPoints`` normal processing
        """
        axis_index = HexList(self.axis_value[0])
        point_index = HexList(self.config.F_PointIndex)
        point_count = HexList(self.config.F_PointCount[0])
        axis_points = HexList(0x0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetAxisPoints request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_80a4.get_axis_points_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_80a4_index,
            axis_index=axis_index,
            point_index=point_index,
            point_count=point_count)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_80a4.get_axis_points_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetAxisPointsResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = AxisResponseCurveTestUtils.GetAxisPointsResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
            "axis_index": (checker.check_axis_index, axis_index),
            "point_index": (checker.check_point_index, point_index),
            "point_count": (checker.check_point_count, point_count),
            "axis_points": (checker.check_axis_points, axis_points),
        })
        checker.check_fields(self, response, self.feature_80a4.get_axis_points_response_cls, check_map)

        self.testCaseChecked("INT_80A4_0003", _AUTHOR)
    # end def test_get_axis_points_interface

    @features("Feature80A4")
    @level("Interface")
    def test_start_update_interface(self):
        """
        Validate ``StartUpdate`` normal processing
        """
        self.post_requisite_reload_nvs = True
        axis_index = HexList(self.axis_value[0])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send StartUpdate request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_80a4.start_update_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_80a4_index,
            axis_index=axis_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_80a4.start_update_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check StartUpdateResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
        }
        checker.check_fields(self, response, self.feature_80a4.start_update_response_cls, check_map)

        self.testCaseChecked("INT_80A4_0004", _AUTHOR)
    # end def test_start_update_interface

    @features("Feature80A4")
    @level("Interface")
    def test_set_axis_points_interface(self):
        """
        Validate ``SetAxisPoints`` normal processing
        """
        self.post_requisite_reload_nvs = True
        point_count = HexList('03')
        axis_points = HexList('0000 0013 0059 0123 FFFF FFFA')
        axis_index = HexList(self.axis_value[0])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send StartUpdate request")
        # --------------------------------------------------------------------------------------------------------------
        AxisResponseCurveTestUtils.HIDppHelper.start_update(self, axis_index=axis_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetAxisPoints request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_80a4.set_axis_points_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_80a4_index,
            point_count=point_count,
            axis_points=axis_points)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_80a4.set_axis_points_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetAxisPointsResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
        }
        checker.check_fields(self, response, self.feature_80a4.set_axis_points_response_cls, check_map)

        self.testCaseChecked("INT_80A4_0005", _AUTHOR)
    # end def test_set_axis_points_interface

    @features("Feature80A4")
    @level("Interface")
    def test_stop_update_interface(self):
        """
        Validate ``StopUpdate`` normal processing
        """
        self.post_requisite_reload_nvs = True
        status = HexList("00")
        point_count = HexList('03')
        axis_points = HexList('0000 0013 0059 0123 FFFF FFFA')
        active_point_count = HexList(self.config.F_ActivePointCount)
        axis_index = HexList(self.axis_value[0])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send StartUpdate request")
        # --------------------------------------------------------------------------------------------------------------
        AxisResponseCurveTestUtils.HIDppHelper.start_update(self, axis_index=axis_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetAxisPoints request")
        # --------------------------------------------------------------------------------------------------------------
        AxisResponseCurveTestUtils.HIDppHelper.set_axis_points(self, point_count=point_count,
                                                               axis_points=axis_points)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send StopUpdate request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_80a4.stop_update_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_80a4_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_80a4.stop_update_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check StopUpdateResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = AxisResponseCurveTestUtils.StopUpdateResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
            "axis_index": (checker.check_axis_index, axis_index),
            "status": (checker.check_status, status),
            "active_point_count": (checker.check_active_point_count, active_point_count),
        })
        checker.check_fields(self, response, self.feature_80a4.stop_update_response_cls, check_map)

        self.testCaseChecked("INT_80A4_0006", _AUTHOR)
    # end def test_stop_update_interface

    @features("Feature80A4")
    @level("Interface")
    def test_reset_axis_interface(self):
        """
        Validate ``ResetAxis`` normal processing
        """
        self.post_requisite_reload_nvs = True
        axis_index = 0

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ResetAxis request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_80a4.reset_axis_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_80a4_index,
            axis_index=axis_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_80a4.reset_axis_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ResetAxisResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
        }
        checker.check_fields(self, response, self.feature_80a4.reset_axis_response_cls, check_map)

        self.testCaseChecked("INT_80A4_0007", _AUTHOR)
    # end def test_reset_axis_interface

    @features("Feature80A4")
    @level("Interface")
    def test_get_calculated_value_interface(self):
        """
        Validate ``GetCalculatedValue`` normal processing
        """
        axis_index = HexList(self.axis_value[0])
        input_value = HexList("0000")
        calculated_value = HexList("0000")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetCalculatedValue request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_80a4.get_calculated_value_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_80a4_index,
            axis_index=axis_index,
            input_value=input_value)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_80a4.get_calculated_value_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetCalculatedValueResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = AxisResponseCurveTestUtils.GetCalculatedValueResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
            "axis_index": (checker.check_axis_index, axis_index),
            "input_value": (checker.check_input_value, input_value),
            "calculated_value": (checker.check_calculated_value, calculated_value),
        })
        checker.check_fields(self, response, self.feature_80a4.get_calculated_value_response_cls, check_map)

        self.testCaseChecked("INT_80A4_0008", _AUTHOR)
    # end def test_get_calculated_value_interface

    @features("Feature80A4v1+")
    @level("Interface")
    def test_save_to_nvs_interface(self):
        """
        Validate ``SaveToNvs`` normal processing
        """
        axis_index = HexList(self.axis_value[0])
        status_no_error = 0

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send save_to_nvs request")
        # ----------------------------------------------------------------------------------------------------------
        AxisResponseCurveTestUtils.HIDppHelper.save_to_nvs(
            self, axis_index=axis_index, device_index=ChannelUtils.get_device_index(test_case=self))
        save_to_nvs_event = AxisResponseCurveTestUtils.HIDppHelper.save_complete_event(self)
        checker = AxisResponseCurveTestUtils.SaveCompleteEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "axis_index": (checker.check_axis_index, axis_index),
            "status": (checker.check_status, status_no_error),
        })
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check save_to_nvs_event fields")
        # ----------------------------------------------------------------------------------------------------------
        checker.check_fields(self, save_to_nvs_event, self.feature_80a4.save_complete_event_cls, check_map)

        self.testCaseChecked("INT_80A4_0009", _AUTHOR)
    # end def test_save_to_nvs_interface

    @features("Feature80A4v1+")
    @level("Interface")
    def test_reload_from_nvs_interface(self):
        """
        Validate ``ReloadFromNvs`` normal processing
        """
        axis_index = HexList(self.axis_value[0])
        status_no_error = 0

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SaveToNvs request")
        # --------------------------------------------------------------------------------------------------------------
        AxisResponseCurveTestUtils.HIDppHelper.reload_from_nvs(
            self, axis_index=axis_index, device_index=ChannelUtils.get_device_index(test_case=self))
        reload_from_nvs_event = AxisResponseCurveTestUtils.HIDppHelper.reload_complete_event(self)
        checker = AxisResponseCurveTestUtils.ReloadCompleteEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "axis_index": (checker.check_axis_index, axis_index),
            "status": (checker.check_status, status_no_error),
        })

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check save_to_nvs_event fields")
        # ----------------------------------------------------------------------------------------------------------
        checker.check_fields(self, reload_from_nvs_event, self.feature_80a4.reload_complete_event_cls, check_map)

        self.testCaseChecked("INT_80A4_0010", _AUTHOR)
    # end def test_reload_from_nvs_interface
# end class AxisResponseCurveInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
