#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_80a4.functionality
:brief: HID++ 2.0 ``AxisResponseCurve`` functionality test suite
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
from pytestbox.device.hidpp20.gaming.feature_80a4.axisresponsecurve import AxisResponseCurveTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vasudev Mukkamala"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AxisResponseCurveFunctionalityTestCase(AxisResponseCurveTestCase):
    """
    Validate ``AxisResponseCurve`` functionality test cases
    """

    @features("Feature80A4")
    @level("Functionality")
    def test_set_axis_points_64_verify(self):
        """
        Validate set axis points can set 64 axis points
        """
        self.post_requisite_reload_nvs = True
        status_no_error = HexList("00")
        active_point_count = HexList("40")
        hid_usage_page = HexList(self.config.F_HidUsagePage)
        axis_resolution = HexList(self.config.F_AxisResolution)
        max_point_count = active_point_count
        properties = HexList(self.config.F_Properties)

        for axis_index in [HexList(i) for i in range(self.config.F_AxisCount)]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StartUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.start_update(self, axis_index=axis_index)
            for index in range(0, len(self.axis_64_points_ordered)):

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Setting all 64 points with SetAxisPoints {index}")
                # ------------------------------------------------------------------------------------------------------
                if index == 21:
                    AxisResponseCurveTestUtils.HIDppHelper.set_axis_points(
                        self, point_count=HexList(int(len(self.axis_64_points_ordered[index]) / 4)),
                        axis_points=self.axis_64_points_ordered[index] + HexList("0000 0000 0000 0000"))
                else:
                    AxisResponseCurveTestUtils.HIDppHelper.set_axis_points(
                        self, point_count=HexList(int(len(self.axis_64_points_ordered[index]) / 4)),
                        axis_points=self.axis_64_points_ordered[index])
                # end if
            # end for

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StopUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            stop_update_response = AxisResponseCurveTestUtils.HIDppHelper.stop_update(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check StopUpdateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AxisResponseCurveTestUtils.StopUpdateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "axis_index": (checker.check_axis_index, axis_index),
                "status": (checker.check_status, status_no_error),
                "active_point_count": (checker.check_active_point_count, active_point_count),
            })
            checker.check_fields(self, stop_update_response, self.feature_80a4.stop_update_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetAxisInfo request")
            # ----------------------------------------------------------------------------------------------------------
            get_axis_info_response = AxisResponseCurveTestUtils.HIDppHelper.get_axis_info(self, axis_index=axis_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetAxisInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AxisResponseCurveTestUtils.GetAxisInfoResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "axis_index": (checker.check_axis_index, axis_index),
                "hid_usage_page": (checker.check_hid_usage_page, hid_usage_page),
                "hid_usage": (checker.check_hid_usage, HexList(self.config.F_HidUsage[int(Numeral(axis_index))])),
                "axis_resolution": (checker.check_axis_resolution, axis_resolution),
                "active_point_count": (checker.check_active_point_count, active_point_count),
                "max_point_count": (checker.check_max_point_count, max_point_count),
                "properties": (checker.check_properties, properties),
            })
            checker.check_fields(self, get_axis_info_response, self.feature_80a4.get_axis_info_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                self,
                "Validating points returned by GetAxisPoints matches with the points that were set with SetAxisPoints")
            # ----------------------------------------------------------------------------------------------------------
            for index in range(0, len(self.axis_64_points_ordered)):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send GetAxisPoints request")
                # ------------------------------------------------------------------------------------------------------
                get_axis_points_response = AxisResponseCurveTestUtils.HIDppHelper.get_axis_points(
                    self, axis_index=axis_index,
                    point_index=HexList(HexList("00") + HexList(index * 3)),
                    point_count=HexList(int(len(self.axis_64_points_ordered[index]) / 4)))
                expected = self.axis_64_points_ordered[index] if index != 21 \
                    else self.axis_64_points_ordered[index] + HexList("0000 0000 0000 0000")

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check GetAxisPointsResponse fields")
                # ------------------------------------------------------------------------------------------------------
                checker = AxisResponseCurveTestUtils.GetAxisPointsResponseChecker
                check_map = checker.get_default_check_map(self)
                check_map.update({
                    "axis_index": (checker.check_axis_index, axis_index),
                    "point_index": (checker.check_point_index, HexList(HexList("00") + HexList(index * 3))),
                    "point_count": (checker.check_point_count,
                                    HexList(int(len(self.axis_64_points_ordered[index]) / 4))),
                    "axis_points": (checker.check_axis_points, expected),
                })
                checker.check_fields(self, get_axis_points_response, self.feature_80a4.get_axis_points_response_cls,
                                     check_map)
            # end for

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                self, "Validating values returned by GetCalculatedValue matches with the values that were set")
            # ----------------------------------------------------------------------------------------------------------
            for rows in range(0, len(self.axis_64_points_ordered)):
                for cols in range(0, len(self.axis_64_points_ordered[rows]), 4):
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, "Send GetCalculatedValue request")
                    # --------------------------------------------------------------------------------------------------
                    response = AxisResponseCurveTestUtils.HIDppHelper.get_calculated_value(
                        self, axis_index=axis_index,
                        input_value=self.axis_64_points_ordered[rows][cols:cols + 2])

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, "Check GetCalculatedValueResponse fields")
                    # --------------------------------------------------------------------------------------------------
                    checker = AxisResponseCurveTestUtils.GetCalculatedValueResponseChecker
                    check_map = checker.get_default_check_map(self)
                    check_map.update({
                        "axis_index": (checker.check_axis_index, axis_index),
                        "input_value": (checker.check_input_value, self.axis_64_points_ordered[rows][cols:cols + 2]),
                        "calculated_value": (checker.check_calculated_value,
                                             self.axis_64_points_ordered[rows][cols + 2:cols + 4]),
                    })
                    checker.check_fields(self, response, self.feature_80a4.get_calculated_value_response_cls, check_map)
                # end for
            # end for
        # end for
        self.testCaseChecked("FUN_80A4_0001", _AUTHOR)
    # end def test_set_axis_points_64_verify

    @features("Feature80A4")
    @level("Functionality")
    def test_set_axis_points_64_reverse_status_verify(self):
        """
        Validate set axis points will not set any points if x co-ordinates of points to be set are in descending order
        """
        self.post_requisite_reload_nvs = True
        # Status index => 0:NoError, 1:NotEnoughData, 2:MinimumMissing, 3:MaximumMissing
        status = [HexList(i) for i in ["00", "01", "02", "03"]]
        active_point_count = HexList("0000")
        for axis_index in [HexList(i) for i in range(self.config.F_AxisCount)]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StartUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.start_update(self, axis_index=axis_index)
            for index in list(reversed(range(0, len(self.axis_64_points_ordered)))):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Setting all 64 points with SetAxisPoints")
                # ------------------------------------------------------------------------------------------------------
                if index == 21:
                    AxisResponseCurveTestUtils.HIDppHelper.set_axis_points(
                        self, point_count=HexList(int(len(self.axis_64_points_ordered[index]) / 4)),
                        axis_points=self.axis_64_points_ordered[index] + HexList("0000 0000 0000 0000"))
                else:
                    AxisResponseCurveTestUtils.HIDppHelper.set_axis_points(
                        self, point_count=HexList(int(len(self.axis_64_points_ordered[index]) / 4)),
                        axis_points=self.axis_64_points_ordered[index])
            # end for

            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StopUpdate request")
            # ------------------------------------------------------------------------------------------------------
            stop_update_response = AxisResponseCurveTestUtils.HIDppHelper.stop_update(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check StopUpdateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AxisResponseCurveTestUtils.StopUpdateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "axis_index": (checker.check_axis_index, axis_index),
                "status": (checker.check_status, status[2]),
                "active_point_count": (checker.check_active_point_count, active_point_count),
            })
            checker.check_fields(self, stop_update_response, self.feature_80a4.stop_update_response_cls, check_map)
        # end for
        self.testCaseChecked("FUN_80A4_0002", _AUTHOR)
    # end def test_set_axis_points_64_reverse_status_verify

    @features("Feature80A4")
    @level("Functionality")
    def test_stop_update_status_verify(self):
        """
        Validate StopUpdate status returned is as expected
        """
        self.post_requisite_reload_nvs = True
        # Status index => 0:NoError, 1:NotEnoughData, 2:MinimumMissing, 3:MaximumMissing
        status = [HexList(i) for i in ["00", "01", "02", "03"]]
        axis_points_value_3_without_minimum = HexList('0007 0014 0003 0004 FFFF FFFF')
        axis_points_value_3_without_maximum = HexList('0000 0010 0006 0010 1003 2006')
        point_count = [HexList(i) for i in self.config.F_PointCount]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, "Verify that if 3 axis point is set using SetAxisPoints returns no error status was sent")
        # --------------------------------------------------------------------------------------------------------------
        for axis_index in [HexList(i) for i in range(self.config.F_AxisCount)]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StartUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.start_update(self, axis_index=axis_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetAxisPoints request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.set_axis_points(self, point_count=point_count[3],
                                                                   axis_points=self.axis_points_value_3)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StopUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            stop_update_response = AxisResponseCurveTestUtils.HIDppHelper.stop_update(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check StopUpdateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AxisResponseCurveTestUtils.StopUpdateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "axis_index": (checker.check_axis_index, axis_index),
                "status": (checker.check_status, status[0]),
                "active_point_count": (checker.check_active_point_count, point_count[3]),
            })
            checker.check_fields(self, stop_update_response, self.feature_80a4.stop_update_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                self,
                "Verify that if 0 axis points are set using SetAxisPoints it returns status not enough data was sent")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StartUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.start_update(self, axis_index=axis_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StopUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            stop_update_response = AxisResponseCurveTestUtils.HIDppHelper.stop_update(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check StopUpdateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AxisResponseCurveTestUtils.StopUpdateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "axis_index": (checker.check_axis_index, axis_index),
                "status": (checker.check_status, status[1]),
                "active_point_count": (checker.check_active_point_count, point_count[0]),
            })
            checker.check_fields(self, stop_update_response, self.feature_80a4.stop_update_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                self,
                "Verify that if 1 axis point is set using SetAxisPoints returns status not enough data was sent")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StartUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.start_update(self, axis_index=axis_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetAxisPoints request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.set_axis_points(self, point_count=point_count[1],
                                                                   axis_points=self.axis_points_value_1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StopUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            stop_update_response = AxisResponseCurveTestUtils.HIDppHelper.stop_update(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check StopUpdateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AxisResponseCurveTestUtils.StopUpdateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "axis_index": (checker.check_axis_index, axis_index),
                "status": (checker.check_status, status[1]),
                "active_point_count": (checker.check_active_point_count, point_count[0]),
            })
            checker.check_fields(self, stop_update_response, self.feature_80a4.stop_update_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                self,
                "Verify that if 3 axis points are set without minimum value using SetAxisPoints returns status"
                " not enough data was sent")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StartUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.start_update(self, axis_index=axis_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetAxisPoints request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.set_axis_points(self, point_count=point_count[3],
                                                                   axis_points=axis_points_value_3_without_minimum)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StopUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            stop_update_response = AxisResponseCurveTestUtils.HIDppHelper.stop_update(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check StopUpdateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AxisResponseCurveTestUtils.StopUpdateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "axis_index": (checker.check_axis_index, axis_index),
                "status": (checker.check_status, status[2]),
                "active_point_count": (checker.check_active_point_count, point_count[0]),
            })
            checker.check_fields(self, stop_update_response, self.feature_80a4.stop_update_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                self,
                "Verify that if 3 axis points are set without maximum value using SetAxisPoints returns status"
                " not enough data was sent")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StartUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.start_update(self, axis_index=axis_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetAxisPoints request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.set_axis_points(self, point_count=point_count[3],
                                                                   axis_points=axis_points_value_3_without_maximum)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StopUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            stop_update_response = AxisResponseCurveTestUtils.HIDppHelper.stop_update(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check StopUpdateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AxisResponseCurveTestUtils.StopUpdateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "axis_index": (checker.check_axis_index, axis_index),
                "status": (checker.check_status, status[3]),
                "active_point_count": (checker.check_active_point_count, point_count[0]),
            })
            checker.check_fields(self, stop_update_response, self.feature_80a4.stop_update_response_cls, check_map)
        # end for
        self.testCaseChecked("FUN_80A4_0003", _AUTHOR)
    # end def test_stop_update_status_verify

    @features("Feature80A4")
    @level("Functionality")
    def test_get_info_verify(self):
        """
        Validate GetInfo Response is as expected
        """
        axis_count = HexList(self.config.F_AxisCount)
        max_get_point_count = HexList(self.config.F_MaxGetPointCount)
        max_set_point_count = HexList(self.config.F_MaxSetPointCount)

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
            "axis_count": (checker.check_axis_count, axis_count),
            "max_get_point_count": (checker.check_max_get_point_count, max_get_point_count),
            "max_set_point_count": (checker.check_max_set_point_count, max_set_point_count)
        })
        checker.check_fields(self, response, self.feature_80a4.get_info_response_cls, check_map)
        self.testCaseChecked("FUN_80A4_0004", _AUTHOR)
    # end def test_get_info_verify

    @features("Feature80A4")
    @level("Functionality")
    def test_get_axis_info_verify(self):
        """
        Validate GetAxisInfo Response is as expected
        """
        self.post_requisite_reload_nvs = True
        hid_usage_page = HexList(self.config.F_HidUsagePage)
        point_count = [HexList(i) for i in self.config.F_PointCount]
        active_point_count = HexList(self.config.F_ActivePointCount)
        max_point_count = HexList(self.config.F_MaxPointCount)
        properties = HexList(self.config.F_Properties)
        axis_resolution = HexList(self.config.F_AxisResolution)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Set 3 axis point is set using SetAxisPoints")
        # --------------------------------------------------------------------------------------------------------------
        for axis_index in [HexList(i) for i in range(self.config.F_AxisCount)]:
            hid_usage = HexList(self.config.F_HidUsage[int(Numeral(axis_index))])
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StartUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.start_update(self, axis_index=axis_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetAxisPoints request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.set_axis_points(self, point_count=point_count[3],
                                                                   axis_points=self.axis_points_value_3)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StopUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.stop_update(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetAxisInfo request")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_80a4.get_axis_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_80a4_index,
                axis_index=axis_index)
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
                "properties": (checker.check_properties, properties)
            })
            checker.check_fields(self, response, self.feature_80a4.get_axis_info_response_cls, check_map)
        # end for
        self.testCaseChecked("FUN_80A4_0005", _AUTHOR)
    # end def test_get_axis_info_verify

    @features("Feature80A4")
    @level("Functionality")
    def test_get_axis_points_verify(self):
        """
        Verify when a value grater than 3 is passes as point count GetAxisPoints considers point count as 3
        """
        self.post_requisite_reload_nvs = True
        status_no_error = HexList("00")
        point_index = HexList(self.config.F_PointIndex)
        point_count = [HexList(i) for i in self.config.F_PointCount]
        active_point_count = HexList("40")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Setting all 64 points with SetAxisPoints")
        # --------------------------------------------------------------------------------------------------------------
        for axis_index in [HexList(i) for i in range(self.config.F_AxisCount)]:

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StartUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.start_update(self, axis_index=axis_index)
            for index in range(0, len(self.axis_64_points_ordered)):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send SetAxisPoints request")
                # ------------------------------------------------------------------------------------------------------
                if index == 21:
                    AxisResponseCurveTestUtils.HIDppHelper.set_axis_points(
                        self, point_count=HexList(int(len(self.axis_64_points_ordered[index]) / 4)),
                        axis_points=self.axis_64_points_ordered[index] + HexList("0000 0000 0000 0000"))
                else:
                    AxisResponseCurveTestUtils.HIDppHelper.set_axis_points(
                        self, point_count=HexList(int(len(self.axis_64_points_ordered[index]) / 4)),
                        axis_points=self.axis_64_points_ordered[index])
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StopUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            stop_update_response = AxisResponseCurveTestUtils.HIDppHelper.stop_update(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check StopUpdateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AxisResponseCurveTestUtils.StopUpdateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "axis_index": (checker.check_axis_index, axis_index),
                "status": (checker.check_status, status_no_error),
                "active_point_count": (checker.check_active_point_count, active_point_count),
            })
            checker.check_fields(self, stop_update_response, self.feature_80a4.stop_update_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                self, "Validating points returned by GetAxisPoints matches with the points that were set with"
                      " SetAxisPoints")
            # ----------------------------------------------------------------------------------------------------------
            point_count_invalid_value = HexList(int(Numeral(point_count[-1])) + 1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetAxisPoints request")
            # ----------------------------------------------------------------------------------------------------------
            response = AxisResponseCurveTestUtils.HIDppHelper.get_axis_points(self,
                                                                              axis_index=axis_index,
                                                                              point_index=point_index,
                                                                              point_count=point_count_invalid_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetAxisPointsResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AxisResponseCurveTestUtils.GetAxisPointsResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "axis_index": (checker.check_axis_index, axis_index),
                "point_index": (checker.check_point_index, point_index),
                "point_count": (checker.check_point_count, point_count[3]),
                "axis_points": (checker.check_axis_points, self.axis_64_points_ordered[0]),
            })
            checker.check_fields(self, response, self.feature_80a4.get_axis_points_response_cls, check_map)
        # end for
        self.testCaseChecked("FUN_80A4_0006", _AUTHOR)
    # end def test_get_axis_points_verify

    @features("Feature80A4")
    @level("Functionality")
    def test_set_axis_points_all_size_writes_verify(self):
        """
        Validate set axis points writes of different sizes works as expected
        """
        self.post_requisite_reload_nvs = True
        status_no_error = HexList("00")
        axis_points_multi_size = [HexList('0000 0002 0001 0003 0002 0004'),
                                  HexList('0003 0007 0004 0009'),
                                  HexList('FFFF FFFF')]
        active_point_count = HexList("06")
        hid_usage_page = HexList(self.config.F_HidUsagePage)
        axis_resolution = HexList(self.config.F_AxisResolution)
        max_point_count = HexList("40")
        properties = HexList(self.config.F_Properties)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Setting points with SetAxisPoints")
        # --------------------------------------------------------------------------------------------------------------
        for axis_index in [HexList(i) for i in range(self.config.F_AxisCount)]:

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StartUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.start_update(self, axis_index=axis_index)
            for index in range(0, len(axis_points_multi_size)):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send SetAxisPoints request")
                # ------------------------------------------------------------------------------------------------------
                if index == 0:
                    AxisResponseCurveTestUtils.HIDppHelper.set_axis_points(
                        self, point_count=HexList(int(len(axis_points_multi_size[index]) / 4)),
                        axis_points=axis_points_multi_size[index])
                elif index == 1:
                    AxisResponseCurveTestUtils.HIDppHelper.set_axis_points(
                        self, point_count=HexList(int(len(axis_points_multi_size[index]) / 4)),
                        axis_points=axis_points_multi_size[index] + HexList("0000 0000"))
                else:
                    AxisResponseCurveTestUtils.HIDppHelper.set_axis_points(
                        self, point_count=HexList(int(len(axis_points_multi_size[index]) / 4)),
                        axis_points=axis_points_multi_size[index] + HexList("0000 0000 0000 0000"))
            # end for

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StopUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            stop_update_response = AxisResponseCurveTestUtils.HIDppHelper.stop_update(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check StopUpdateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AxisResponseCurveTestUtils.StopUpdateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "axis_index": (checker.check_axis_index, axis_index),
                "status": (checker.check_status, status_no_error),
                "active_point_count": (checker.check_active_point_count, active_point_count),
            })
            checker.check_fields(self, stop_update_response, self.feature_80a4.stop_update_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetAxisInfo request")
            # ----------------------------------------------------------------------------------------------------------
            get_axis_info_response = AxisResponseCurveTestUtils.HIDppHelper.get_axis_info(self, axis_index=axis_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetAxisInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AxisResponseCurveTestUtils.GetAxisInfoResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "axis_index": (checker.check_axis_index, axis_index),
                "hid_usage_page": (checker.check_hid_usage_page, hid_usage_page),
                "hid_usage": (checker.check_hid_usage, HexList(self.config.F_HidUsage[int(Numeral(axis_index))])),
                "axis_resolution": (checker.check_axis_resolution, axis_resolution),
                "active_point_count": (checker.check_active_point_count, active_point_count),
                "max_point_count": (checker.check_max_point_count, max_point_count),
                "properties": (checker.check_properties, properties),
            })
            checker.check_fields(self, get_axis_info_response, self.feature_80a4.get_axis_info_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                self,
                "Validating points returned by GetAxisPoints matches with the points that were set with SetAxisPoints")
            # ----------------------------------------------------------------------------------------------------------
            point_index = 0
            for index in range(0, len(axis_points_multi_size)):
                points_read_count = int(len(axis_points_multi_size[index]) / 4)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send GetAxisPoints request")
                # ------------------------------------------------------------------------------------------------------
                response = AxisResponseCurveTestUtils.HIDppHelper.get_axis_points(
                    self, axis_index=axis_index,
                    point_index=HexList(hex(point_index)[2:].zfill(4)),
                    point_count=HexList(points_read_count))
                point_index += points_read_count
                # Adding Padding to expected value based on the no of points read
                if points_read_count == 3:
                    expected_value = axis_points_multi_size[index]
                elif points_read_count == 2:
                    expected_value = axis_points_multi_size[index] + HexList("0000 0000")
                else:
                    expected_value = axis_points_multi_size[index] + HexList("0000 0000 0000 0000")
                # end if

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check GetAxisPointsResponse fields")
                # ------------------------------------------------------------------------------------------------------
                checker = AxisResponseCurveTestUtils.GetAxisPointsResponseChecker
                check_map = checker.get_default_check_map(self)
                check_map.update({
                    "axis_index": (checker.check_axis_index, axis_index),
                    "point_index": (checker.check_point_index,
                                    HexList(hex(point_index-points_read_count)[2:].zfill(4))),
                    "point_count": (checker.check_point_count, HexList(points_read_count)),
                    "axis_points": (checker.check_axis_points, expected_value),
                })
                checker.check_fields(self, response, self.feature_80a4.get_axis_points_response_cls, check_map)
            # end for
        # end for
        self.testCaseChecked("FUN_80A4_0007", _AUTHOR)
    # end def test_set_axis_points_all_size_writes_verify
# end class AxisResponseCurveFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
