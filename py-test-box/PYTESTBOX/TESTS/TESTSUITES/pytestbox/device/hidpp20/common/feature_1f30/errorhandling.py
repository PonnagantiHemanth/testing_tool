#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1f30.errorhandling
:brief: HID++ 2.0 ``TemperatureMeasurement`` error handling test suite
:author: Sanjib Hazra <shazra@logitech.com>
:date: 2021/06/07
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.hidpp20.common.feature_1f30.temperaturemeasurement import TemperatureMeasurementTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Sanjib Hazra"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TemperatureMeasurementErrorHandlingTestCase(TemperatureMeasurementTestCase):
    """
    Validates ``TemperatureMeasurement`` errorhandling test cases
    """
    @features("Feature1F30")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validates function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(
                value=list(range(self.feature_1f30.get_max_function_index() + 1)),
                max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetInfo request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1f30.get_info_cls(self.deviceIndex, self.feature_1f30_index)
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
        self.testCaseChecked("ERR_1F30_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature1F30")
    @level("ErrorHandling")
    def test_get_temperature_wrong_sensor_id(self):
        """
        Validates ``GetTemperature`` with invalid sensor id
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over Sensor index invalid range (typical wrong values)')
        # --------------------------------------------------------------------------------------------------------------
        for invalid_sensor_id in compute_sup_values(HexList(self.product.F_SensorCount)):
            report = self.feature_1f30.get_temperature_cls(
                    self.deviceIndex,
                    self.feature_1f30_index, HexList(invalid_sensor_id))
            error_response = self.send_report_wait_response(
                    report=report,
                    response_queue=self.hidDispatcher.error_message_queue,
                    response_class_type=ErrorCodes)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Validate error code: {ErrorCodes.INVALID_FUNCTION_ID}")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(obtained=int(Numeral(error_response.errorCode)),
                             expected=ErrorCodes.INVALID_FUNCTION_ID,
                             msg="The error_code parameter differs from the one expected")
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_1F30_0002", _AUTHOR)
    # end def test_get_temperature_wrong_sensor_id
# end class TemperatureMeasurementErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
