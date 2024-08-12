#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_80a4.business
:brief: HID++ 2.0 ``AxisResponseCurve`` business test suite
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/06/04
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.devicereset import ForceDeviceReset
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
class AxisResponseCurveBusinessTestCase(AxisResponseCurveTestCase):
    """
    Validate ``AxisResponseCurve`` business test cases
    """

    @features("Feature80A4")
    @level("Business")
    def test_axis_response_curve_flow_verify(self):
        """
        Validate axis response curve flow
        """
        self.post_requisite_reload_nvs = True
        status_no_error = HexList("00")
        point_count = HexList(self.config.F_PointCount[3])
        point_index = HexList(self.config.F_PointIndex)
        axis_points = self.axis_points_value_3
        for axis_index in [HexList(i) for i in range(self.config.F_AxisCount)]:
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
            stop_update_response = AxisResponseCurveTestUtils.HIDppHelper.stop_update(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check StopUpdateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AxisResponseCurveTestUtils.StopUpdateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "axis_index": (checker.check_axis_index, axis_index),
                "status": (checker.check_status, status_no_error),
                "active_point_count": (checker.check_active_point_count, point_count),
            })
            checker.check_fields(self, stop_update_response, self.feature_80a4.stop_update_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetAxisPoints request")
            # ----------------------------------------------------------------------------------------------------------
            get_axis_points_response = AxisResponseCurveTestUtils.HIDppHelper.get_axis_points(
                    self, axis_index=axis_index,
                    point_index=point_index,
                    point_count=point_count)

            for index in range(0, 2):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check value from GetAxisPoints")
                # ------------------------------------------------------------------------------------------------------
                self.assertEqual(expected=axis_points[(index * 4) + 2:(index * 4) + 4],
                                 obtained=get_axis_points_response.axis_points[(index * 4) + 2:(index * 4) + 4],
                                 msg="value obtained from GetAxisPoints is not as Expected")

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send GetCalculatedValue request")
                # ------------------------------------------------------------------------------------------------------
                get_calculated_value_response = AxisResponseCurveTestUtils.HIDppHelper.get_calculated_value(
                        self, axis_index=axis_index, input_value=axis_points[(index * 4):(index * 4) + 2])

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check value from GetCalculatedValue")
                # ------------------------------------------------------------------------------------------------------
                self.assertEqual(expected=axis_points[(index * 4) + 2:(index * 4) + 4],
                                 obtained=get_calculated_value_response.calculated_value,
                                 msg=f'value obtained from GetCalculatedValue on axis {axis_index} is not as Expected')
            # end for
        # end for
        self.testCaseChecked("BUS_80A4_0001", _AUTHOR)
    # end def test_axis_response_curve_flow_verify

    @features("Feature80A4")
    @level("Business")
    def test_set_axis_response_curve_reset_axis(self):
        """
        Validate set axis response value set doesn't persist across a reset
        """
        self.post_requisite_reload_nvs = True
        axis_points_value = HexList('0000 0013 0059 0123 FFFF FFFA')
        status_no_error = HexList("00")
        point_count = [HexList(i) for i in self.config.F_PointCount]
        hid_usage_page = HexList(self.config.F_HidUsagePage)
        active_point_count = [HexList(i) for i in self.config.F_PointCount]
        max_point_count = HexList("40")
        properties = HexList(self.config.F_Properties)
        axis_resolution = HexList(self.config.F_AxisResolution)
        for axis_index in [HexList(i) for i in range(self.config.F_AxisCount)]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StartUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.start_update(self, axis_index=axis_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetAxisPoints request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.set_axis_points(self, point_count=point_count[3],
                                                                   axis_points=axis_points_value)

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
                "active_point_count": (checker.check_active_point_count, point_count[3]),
            })
            checker.check_fields(self, stop_update_response, self.feature_80a4.stop_update_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetAxisInfo request")
            # ----------------------------------------------------------------------------------------------------------
            response = AxisResponseCurveTestUtils.HIDppHelper.get_axis_info(self, axis_index=axis_index)

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
                "active_point_count": (checker.check_active_point_count, active_point_count[3]),
                "max_point_count": (checker.check_max_point_count, max_point_count),
                "properties": (checker.check_properties, properties),
            })
            checker.check_fields(self, response, self.feature_80a4.get_axis_info_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send ResetAxis request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.reset_axis(self, axis_index=axis_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetAxisInfo request")
            # ----------------------------------------------------------------------------------------------------------
            response = AxisResponseCurveTestUtils.HIDppHelper.get_axis_info(self, axis_index=axis_index)

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
                "active_point_count": (checker.check_active_point_count, active_point_count[0]),
                "max_point_count": (checker.check_max_point_count, max_point_count),
                "properties": (checker.check_properties, properties),
            })
            checker.check_fields(self, response, self.feature_80a4.get_axis_info_response_cls, check_map)
        # end for
        self.testCaseChecked("BUS_80A4_0002", _AUTHOR)
    # end def test_set_axis_response_curve_reset_axis

    @features("Feature80A4")
    @level("Business")
    def test_force_device_reset(self):
        """
        Validate set axis response value set doesn't persist across a reset
        """
        self.post_requisite_reload_nvs = True
        axis_points_value = HexList('0000 0013 0059 0123 FFFF FFFA')
        status_no_error = HexList("00")
        point_count = [HexList(i) for i in self.config.F_PointCount]
        hid_usage_page = HexList(self.config.F_HidUsagePage)
        active_point_count = [HexList(i) for i in self.config.F_PointCount]
        max_point_count = HexList("40")
        properties = HexList(self.config.F_Properties)
        axis_resolution = HexList(self.config.F_AxisResolution)
        for axis_index in [HexList(i) for i in range(self.config.F_AxisCount)]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StartUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.start_update(self, axis_index=axis_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetAxisPoints request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.set_axis_points(self, point_count=point_count[3],
                                                                   axis_points=axis_points_value)

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
                "active_point_count": (checker.check_active_point_count, point_count[3]),
            })
            checker.check_fields(self, stop_update_response, self.feature_80a4.stop_update_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetAxisInfo request")
            # ----------------------------------------------------------------------------------------------------------
            response = AxisResponseCurveTestUtils.HIDppHelper.get_axis_info(self, axis_index=axis_index)

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
                "active_point_count": (checker.check_active_point_count, active_point_count[3]),
                "max_point_count": (checker.check_max_point_count, max_point_count),
                "properties": (checker.check_properties, properties),
            })
            checker.check_fields(self, response, self.feature_80a4.get_axis_info_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send ForceDeviceReset")
            # ----------------------------------------------------------------------------------------------------------
            feature_1802_index = ChannelUtils.update_feature_mapping(self, feature_id=ForceDeviceReset.FEATURE_ID)
            force_device_reset = ForceDeviceReset(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                                  featureId=feature_1802_index)
            ChannelUtils.send_only(self, report=force_device_reset)
            # Wait DUT to complete reset procedure
            sleep(5)
            # Reset device connection
            self.reset(hardware_reset=False, recover_time_needed=True)
            sleep(2)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Enable Hidden Features again")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetAxisInfo request")
            # ----------------------------------------------------------------------------------------------------------
            response = AxisResponseCurveTestUtils.HIDppHelper.get_axis_info(self, axis_index=axis_index)

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
                "active_point_count": (checker.check_active_point_count, active_point_count[0]),
                "max_point_count": (checker.check_max_point_count, max_point_count),
                "properties": (checker.check_properties, properties),
            })
            checker.check_fields(self, response, self.feature_80a4.get_axis_info_response_cls, check_map)

        # end for
        self.testCaseChecked("BUS_80A4_0003", _AUTHOR)
    # end def test_force_device_reset

    @features("Feature80A4")
    @level("Business")
    def test_get_axis_response_curve_read_more_than_written(self):
        """
        Validate failure if read points are greater than values set by SetAxisResponse
        """
        self.post_requisite_reload_nvs = True
        axis_points_value = HexList('0000 0000 0000 0019 FFFF FFFD')
        status_no_error = HexList("00")
        point_index = HexList(self.config.F_PointIndex)
        point_count = [HexList(i) for i in self.config.F_PointCount]
        for axis_index in [HexList(i) for i in range(self.config.F_AxisCount)]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StartUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.start_update(self, axis_index=axis_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetAxisPoints request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.set_axis_points(self, point_count=point_count[3],
                                                                   axis_points=axis_points_value)

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
                "active_point_count": (checker.check_active_point_count, point_count[3]),
            })
            checker.check_fields(self, stop_update_response, self.feature_80a4.stop_update_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetAxisPoints request")
            # ----------------------------------------------------------------------------------------------------------
            get_axis_points_response = AxisResponseCurveTestUtils.HIDppHelper.get_axis_points(
                    self, axis_index=axis_index,
                    point_index=point_index,
                    point_count=point_count[2])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetAxisPointsResponse")
            # ----------------------------------------------------------------------------------------------------------
            for index in range(0, 2):
                self.assertEqual(expected=axis_points_value[(index * 4) + 2:(index * 4) + 4],
                                 obtained=get_axis_points_response.axis_points[(index * 4) + 2:(index * 4) + 4],
                                 msg="value obtained from GetAxisPoints is not as expected")
            # end for
        # end for
        self.testCaseChecked("BUS_80A4_0004", _AUTHOR)
    # end def test_get_axis_response_curve_read_more_than_written
# end class AxisResponseCurveBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
