#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_80a4.errorhandling
:brief: HID++ 2.0 ``AxisResponseCurve`` errorhandling test suite
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/06/04
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.axisresponsecurveutils import AxisResponseCurveTestUtils
from pytestbox.device.hidpp20.gaming.feature_80a4.axisresponsecurve import AxisResponseCurveTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vasudev Mukkamala"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AxisResponseCurveErrorHandlingTestCase(AxisResponseCurveTestCase):
    """
    Validate ``AxisResponseCurve`` errorhandling test cases
    """

    @features("Feature80A4")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_80a4.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetInfo request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_80a4.get_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_80a4_index)
            report.functionIndex = function_index

            AxisResponseCurveTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_FUNCTION_ID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_80A4_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature80A4")
    @level("ErrorHandling")
    def test_get_axis_info_error_verify(self):
        """
        Validate get axis info throws invalid argument error for invalid axis index
        """
        invalid_axis_index = HexList(self.config.F_AxisCount)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Validating get axis info throws invalid argument error for invalid axis index")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetInfo request")
        # --------------------------------------------------------------------------------------------------------------
        get_axis_info = self.feature_80a4.get_axis_info_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_80a4_index,
            axis_index=invalid_axis_index)
        AxisResponseCurveTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=get_axis_info,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])
        self.testCaseChecked("ERR_80A4_0002", _AUTHOR)
    # end def test_get_axis_info_error_verify

    @features("Feature80A4")
    @level("ErrorHandling")
    def test_get_axis_points_error_verify(self):
        """
        Validate get axis points throws invalid argument error for invalid axis index
        """
        invalid_axis_index = HexList(self.config.F_AxisCount)
        point_index = HexList(self.config.F_PointIndex)
        point_index_max_value = HexList(self.config.F_MaxPointCount)
        point_index_invalid_value = HexList("0041")
        point_count = [HexList(i) for i in self.config.F_PointCount]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Validating get axis points throws invalid argument error for invalid axis index")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetAxisPoints request")
        # --------------------------------------------------------------------------------------------------------------
        get_axis_points = self.feature_80a4.get_axis_points_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_80a4_index,
            axis_index=invalid_axis_index,
            point_index=point_index,
            point_count=point_count[2])
        AxisResponseCurveTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=get_axis_points,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        for axis_index in [HexList(i) for i in range(self.config.F_AxisCount)]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Validating get axis points throws invalid argument error for invalid point index")
            # ----------------------------------------------------------------------------------------------------------
            get_axis_points = self.feature_80a4.get_axis_points_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_80a4_index,
                axis_index=HexList(axis_index),
                point_index=point_index_invalid_value,
                point_count=point_count[2])
            AxisResponseCurveTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=get_axis_points,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self,
                "Validating get axis points throws invalid argument error for trying to access points beyond the range")
            # ----------------------------------------------------------------------------------------------------------
            get_axis_points = self.feature_80a4.get_axis_points_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_80a4_index,
                axis_index=HexList(axis_index),
                point_index=point_index_max_value,
                point_count=point_count[3])
            AxisResponseCurveTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=get_axis_points,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        self.testCaseChecked("ERR_80A4_0003", _AUTHOR)
    # end def test_get_axis_points_error_verify

    @features("Feature80A4")
    @level("ErrorHandling")
    def test_start_update_error_verify(self):
        """
        Validate start update throws invalid argument error for invalid axis index
        """
        self.post_requisite_reload_nvs = True
        invalid_axis_index = HexList(self.config.F_AxisCount)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Validating start update throws invalid argument error for invalid axis index")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send StartUpdate request")
        # --------------------------------------------------------------------------------------------------------------
        start_update = self.feature_80a4.start_update_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_80a4_index,
            axis_index=invalid_axis_index)
        AxisResponseCurveTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=start_update,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self,
                           "Validating start update throws busy if start update is called while axis is being updated")
        # --------------------------------------------------------------------------------------------------------------
        for axis_index in [HexList(i) for i in range(self.config.F_AxisCount)]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StartUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            start_update = self.feature_80a4.start_update_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_80a4_index,
                axis_index=HexList(axis_index))
            AxisResponseCurveTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=start_update,
                error_codes=[ErrorCodes.BUSY])
        # end for
        self.testCaseChecked("ERR_80A4_0004", _AUTHOR)
    # end def test_start_update_error_verify

    @features("Feature80A4")
    @level("ErrorHandling")
    def test_set_axis_points_error_verify(self):
        """
        Validate set axis points error throws HIDPP_NOT_ALLOWED when called without calling start update
        """
        self.post_requisite_reload_nvs = True
        axis_index = HexList(self.axis_value[0])
        point_count = [HexList(i) for i in self.config.F_PointCount]
        point_count_invalid_value = HexList(int(Numeral(point_count[-1])) + 1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, "Validating calling set axis points before issuing start update throws not allowed error")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetAxisPoints request")
        # --------------------------------------------------------------------------------------------------------------
        set_axis_points = self.feature_80a4.set_axis_points_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_80a4_index,
            point_count=point_count[3],
            axis_points=self.axis_points_value_3)
        AxisResponseCurveTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=set_axis_points,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, "Validating set axis points throws invalid argument error for invalid point count")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send StartUpdate request")
        # --------------------------------------------------------------------------------------------------------------
        AxisResponseCurveTestUtils.HIDppHelper.start_update(self, axis_index=axis_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetAxisPoints request")
        # --------------------------------------------------------------------------------------------------------------
        set_axis_points = self.feature_80a4.set_axis_points_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_80a4_index,
            point_count=point_count_invalid_value,
            axis_points=self.axis_points_value_3)
        AxisResponseCurveTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=set_axis_points,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        # Disabling updates to prevent interference to other test cases
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send StopUpdate request")
        # --------------------------------------------------------------------------------------------------------------
        AxisResponseCurveTestUtils.HIDppHelper.stop_update(self)
        self.testCaseChecked("ERR_80A4_0005", _AUTHOR)
    # end def test_set_axis_points_error_verify

    @features("Feature80A4")
    @level("ErrorHandling")
    def test_set_axis_points_65_error_verify(self):
        """
        Validate setting 65 axis points and every error occurs
        """
        self.post_requisite_reload_nvs = True
        axis_points_value_64_65 = HexList('0000 0000 8FFF FF00 FFFF FFFF')
        status_no_error = HexList(self.config.F_Status)
        point_count = [HexList(i) for i in self.config.F_PointCount]
        active_point_count = HexList('40')
        for axis_index in [HexList(i) for i in range(self.config.F_AxisCount)]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send StartUpdate request")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.start_update(self, axis_index=axis_index)
            # Set 63 axis points
            for index in range(0, len(self.axis_64_points_ordered) - 1):
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
            LogHelper.log_step(self, "Setting 64th and 65th axis point")
            # ----------------------------------------------------------------------------------------------------------
            set_axis_points = self.feature_80a4.set_axis_points_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_80a4_index,
                point_count=point_count[2],
                axis_points=axis_points_value_64_65)
            AxisResponseCurveTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=set_axis_points,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Setting only 64th axis point")
            # ----------------------------------------------------------------------------------------------------------
            AxisResponseCurveTestUtils.HIDppHelper.\
                set_axis_points(self, point_count=point_count[1],
                                axis_points=self.axis_64_points_ordered[-1] + HexList("0000 0000 0000 0000"))

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
        # end for
        self.testCaseChecked("ERR_80A4_0006", _AUTHOR)
    # end def test_set_axis_points_65_error_verify

    @features("Feature80A4")
    @level("ErrorHandling")
    def test_stop_update_error_verify(self):
        """
        Validate stop update error throws HIDPP_NOT_ALLOWED when called without calling start update
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, "Validating calling stop update before issuing start update throws not allowed error")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send StopUpdate request")
        # --------------------------------------------------------------------------------------------------------------
        stop_update = self.feature_80a4.stop_update_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_80a4_index)
        AxisResponseCurveTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=stop_update,
            error_codes=[ErrorCodes.NOT_ALLOWED])
        self.testCaseChecked("ERR_80A4_0007", _AUTHOR)
    # end def test_stop_update_error_verify

    @features("Feature80A4")
    @level("ErrorHandling")
    def test_reset_axis_error_verify(self):
        """
        Validate Reset Axis throws invalid argument error for invalid axis index
        """
        self.post_requisite_reload_nvs = True
        invalid_axis_index = HexList(self.config.F_AxisCount)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, "Validating reset axis throws invalid argument error for invalid axis index")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ResetAxis request")
        # --------------------------------------------------------------------------------------------------------------
        reset_axis = self.feature_80a4.reset_axis_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_80a4_index,
            axis_index=invalid_axis_index)
        AxisResponseCurveTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=reset_axis,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])
        self.testCaseChecked("ERR_80A4_0008", _AUTHOR)
    # end def test_reset_axis_error_verify

    @features("Feature80A4")
    @level("ErrorHandling")
    def test_get_calculated_value_error_verify(self):
        """
        Validate GetCalculatedValue throws invalid argument error for invalid axis index
        """
        invalid_axis_index = HexList(self.config.F_AxisCount)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, "Validating get calculated value throws invalid argument error for invalid axis index")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetCalculatedValue request")
        # --------------------------------------------------------------------------------------------------------------
        get_calculated_value = self.feature_80a4.get_calculated_value_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_80a4_index,
            axis_index=invalid_axis_index,
            input_value=self.input_value)
        AxisResponseCurveTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=get_calculated_value,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])
        self.testCaseChecked("ERR_80A4_0009", _AUTHOR)
    # end def test_get_calculated_value_error_verify
# end class AxisResponseCurveErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
