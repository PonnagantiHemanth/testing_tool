#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.peripheral.feature_9215.errorhandling
:brief: HID++ 2.0 ``Ads1231`` error handling test suite
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/06/06
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
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.ads1231utils import Ads1231TestUtils as Utils
from pytestbox.device.hidpp20.peripheral.feature_9215.ads1231 import Ads1231TestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vasudev Mukkamala"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class Ads1231ErrorHandlingTestCase(Ads1231TestCase):
    """
    Validate ``Ads1231`` errorhandling test cases
    """

    @features("Feature9215")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(
                value=list(range(self.feature_9215.get_max_function_index() + 1)),
                max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ResetSensor request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_9215.reset_sensor_cls(self.deviceIndex, self.feature_9215_index)
            report.functionIndex = function_index

            error_response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Validate ErrorCode ({ErrorCodes.INVALID_FUNCTION_ID})")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(obtained=int(Numeral(error_response.errorCode)),
                             expected=ErrorCodes.INVALID_FUNCTION_ID,
                             msg="The error_code parameter differs from the one expected")
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_9215_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature9215")
    @level("ErrorHandling")
    def test_calibrate_error_verify(self):
        """
        Validate passing invalid arguments to Calibrate returns an error
        """
        error_codes = [ErrorCodes.INVALID_ARGUMENT]
        ref_point_index_invalid_value = HexList("04")
        ref_point_output_invalid_value = HexList("65")
        ref_point_index_value = [HexList("00"), HexList("01"), HexList("02")]
        ref_point_out_value = [HexList("00"), HexList("30"), HexList("40")]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Passing Invalid Reference Point Index to Calibrate")
        # --------------------------------------------------------------------------------------------------------------
        calibrate = self.feature_9215.calibrate_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_9215_index,
                ref_point_index=ref_point_index_invalid_value,
                ref_point_out_value=ref_point_out_value[1])
        DeviceBaseTestUtils.HIDppHelper.send_report_wait_error(self, report=calibrate,
                                                               error_codes=error_codes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Passing Invalid reference point output value to Calibrate")
        # --------------------------------------------------------------------------------------------------------------
        calibrate = self.feature_9215.calibrate_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_9215_index,
                ref_point_index=ref_point_index_value[1],
                ref_point_out_value=ref_point_output_invalid_value)
        DeviceBaseTestUtils.HIDppHelper.send_report_wait_error(self, report=calibrate,
                                                               error_codes=error_codes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "verifying for ref point 2 if its ref output percentage value is "
                                 "less that of ref point 1 an error is raised")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.calibrate(self, ref_point_index=ref_point_index_value[1],
                                    ref_point_out_value=ref_point_out_value[2])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Setting reference output percentage value of ref point 2 to a "
                                 "value which is less than ref point 1")
        # --------------------------------------------------------------------------------------------------------------
        calibrate = self.feature_9215.calibrate_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_9215_index,
                ref_point_index=ref_point_index_value[2],
                ref_point_out_value=ref_point_out_value[1])
        DeviceBaseTestUtils.HIDppHelper.send_report_wait_error(self, report=calibrate,
                                                               error_codes=error_codes)

        self.testCaseChecked("ERR_9215_0002", _AUTHOR)
    # end def test_calibrate_error_verify

    @features("Feature9215")
    @level("ErrorHandling")
    def test_read_calibration_error_verify(self):
        """
        Validate passing invalid argument value to ReadCalibration returns an error
        """
        error_codes = [ErrorCodes.INVALID_ARGUMENT]
        ref_point_index_invalid_value = HexList("04")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Passing Invalid Reference Point Index to ReadCalibration")
        # --------------------------------------------------------------------------------------------------------------
        read_calibration = self.feature_9215.read_calibration_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_9215_index,
                ref_point_index=ref_point_index_invalid_value)
        DeviceBaseTestUtils.HIDppHelper.send_report_wait_error(self, report=read_calibration,
                                                               error_codes=error_codes)
        self.testCaseChecked("ERR_9215_0003", _AUTHOR)
    # end def test_read_calibration_error_verify

    @features("Feature9215")
    @level("ErrorHandling")
    def test_write_calibration_error_verify(self):
        """
        Validate passing invalid argument value to WriteCalibration returns an error
        """
        error_codes = [ErrorCodes.INVALID_ARGUMENT]
        self.post_requisite_reload_nvs = True
        ref_point_index_invalid_value = HexList("04")
        ref_point_output_invalid_value = HexList("65")
        ref_point_index_value = [HexList("00"), HexList("01"), HexList("02")]
        ref_point_out_value = [HexList("00"), HexList("30"), HexList("40")]
        ref_point_cal_value = [HexList("002000"), HexList("F01000"), HexList("FE0000")]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Passing invalid Reference Point Index value to WriteCalibration")
        # --------------------------------------------------------------------------------------------------------------
        write_calibration = self.feature_9215.write_calibration_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_9215_index,
                ref_point_index=ref_point_index_invalid_value,
                ref_point_out_value=ref_point_out_value[1],
                ref_point_cal_value=ref_point_cal_value[2])
        DeviceBaseTestUtils.HIDppHelper.send_report_wait_error(self, report=write_calibration,
                                                               error_codes=error_codes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Passing invalid Reference Point Output value to WriteCalibration")
        # --------------------------------------------------------------------------------------------------------------
        write_calibration = self.feature_9215.write_calibration_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_9215_index,
                ref_point_index=ref_point_index_value[1],
                ref_point_out_value=ref_point_output_invalid_value,
                ref_point_cal_value=ref_point_cal_value[2])
        DeviceBaseTestUtils.HIDppHelper.send_report_wait_error(self, report=write_calibration,
                                                               error_codes=error_codes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "verifying for ref point 2 if its ref output percentage value is "
                                 "less that of ref point 1 an error is raised")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.write_calibration(self, ref_point_index=ref_point_index_value[1],
                                            ref_point_out_value=ref_point_out_value[2],
                                            ref_point_cal_value=ref_point_cal_value[1])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Setting reference output percentage value of ref point 2 to a "
                                 "value which is less than ref point 1")
        # --------------------------------------------------------------------------------------------------------------
        write_calibration = self.feature_9215.write_calibration_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_9215_index,
                ref_point_index=ref_point_index_value[2],
                ref_point_out_value=ref_point_out_value[1],
                ref_point_cal_value=ref_point_cal_value[2])
        DeviceBaseTestUtils.HIDppHelper.send_report_wait_error(self, report=write_calibration,
                                                               error_codes=error_codes)
        self.testCaseChecked("ERR_9215_0004", _AUTHOR)
    # end def test_write_calibration_error_verify

    @features("Feature9215")
    @level("ErrorHandling")
    def test_read_other_nvs_data_error_verify(self):
        """
        Validate passing invalid argument value to ReadOtherNvsData returns an error
        """
        error_codes = [ErrorCodes.INVALID_ARGUMENT]
        data_field_id_invalid = HexList("01")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Passing Invalid Data Field Id to ReadOtherNvsData")
        # --------------------------------------------------------------------------------------------------------------
        read_other_nvs_data = self.feature_9215.read_other_nvs_data_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_9215_index,
                data_field_id=data_field_id_invalid)
        DeviceBaseTestUtils.HIDppHelper.send_report_wait_error(self, report=read_other_nvs_data,
                                                               error_codes=error_codes)
        self.testCaseChecked("ERR_9215_0005", _AUTHOR)
    # end def test_read_other_nvs_data_error_verify

    @features("Feature9215")
    @level("ErrorHandling")
    def test_write_other_nvs_data_error_verify(self):
        """
        Validate passing invalid argument value to WriteOtherNvsData returns an error
        """
        error_codes = [ErrorCodes.INVALID_ARGUMENT]
        self.post_requisite_reload_nvs = True
        data = HexList("400000000000000000000000000000")
        data_field_id_invalid = HexList("01")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Passing Invalid Data Field Id to WriteOtherNvsData")
        # --------------------------------------------------------------------------------------------------------------
        write_other_nvs_data = self.feature_9215.write_other_nvs_data_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_9215_index,
                data_field_id=data_field_id_invalid,
                data=data)
        DeviceBaseTestUtils.HIDppHelper.send_report_wait_error(self, report=write_other_nvs_data,
                                                               error_codes=error_codes)
        self.testCaseChecked("ERR_9215_0006", _AUTHOR)
    # end def test_write_other_nvs_data_error_verify

    @features("Feature9215WithManDynCal")
    @level("ErrorHandling")
    def test_manage_dynamic_calibration_parameters_error_verify(self):
        """
        Validate passing invalid argument value to ManageDynamicCalibrationParameter returns an error
        """
        error_codes = [ErrorCodes.INVALID_ARGUMENT]
        offset_extension_invalid_value = HexList("65")
        command_invalid_value = HexList("01")
        command_set_value = HexList("80")
        offset_extension_value = HexList("07")
        offset_adjustment_count_value = HexList("0014")
        dynamic_threshold_value = HexList("05")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Passing Invalid offset extension to ManageDynamicCalibrationParameters")
        # --------------------------------------------------------------------------------------------------------------
        manage_dynamic_calibration_params = self.feature_9215.manage_dynamic_calibration_parameters_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_9215_index,
                command=command_set_value,
                offset_extension=offset_extension_invalid_value,
                offset_adjustment_count=offset_adjustment_count_value,
                dynamic_threshold=dynamic_threshold_value)
        DeviceBaseTestUtils.HIDppHelper.send_report_wait_error(self, report=manage_dynamic_calibration_params,
                                                               error_codes=error_codes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Passing Invalid Command value to ManageDynamicCalibrationParameters")
        # --------------------------------------------------------------------------------------------------------------
        manage_dynamic_calibration_params = self.feature_9215.manage_dynamic_calibration_parameters_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_9215_index,
                command=command_invalid_value,
                offset_extension=offset_extension_value,
                offset_adjustment_count=offset_adjustment_count_value,
                dynamic_threshold=dynamic_threshold_value)
        DeviceBaseTestUtils.HIDppHelper.send_report_wait_error(self, report=manage_dynamic_calibration_params,
                                                               error_codes=error_codes)
        self.testCaseChecked("ERR_9215_0007", _AUTHOR)
    # end def test_manage_dynamic_calibration_parameters_error_verify
# end class Ads1231ErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
