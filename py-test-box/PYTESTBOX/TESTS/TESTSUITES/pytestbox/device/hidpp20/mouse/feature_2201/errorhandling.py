#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.mouse.feature_2201.errorhandling
:brief: HID++ 2.0 Adjustable DPI error handling test suite
:author: Fred Chen <fchen7@logitech.com>
:date: 2021/06/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.adjustabledpiutils import AdjustableDpiTestUtils
from pytestbox.device.hidpp20.mouse.feature_2201.adjustabledpi import AdjustableDpiTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AdjustableDpiErrorHandlingTestCase(AdjustableDpiTestCase):
    """
    Validates Adjustable DPI Error Handling TestCases
    """
    @features('Feature2201')
    @level('ErrorHandling')
    def test_wrong_sensor_idx(self):
        """
        Send command by invalid sensorIdx shall raise error
        """
        for sensor_idx in compute_wrong_range(list(range(self.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI.F_SensorCount)),
                                              max_value=0xFF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send GetSensorDpiList with invalid sensor index value: {sensor_idx}')
            # ----------------------------------------------------------------------------------------------------------
            get_sensor_dpi_list_req = self.feature_2201.get_sensor_dpi_list_cls(device_index=self.deviceIndex,
                                                                                feature_index=self.feature_2201_index,
                                                                                sensor_idx=int(sensor_idx))
            error_resp = self.send_report_wait_response(
                report=get_sensor_dpi_list_req,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Error Codes InvalidArgument (2) returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=ErrorCodes.INVALID_ARGUMENT,
                             obtained=error_resp.errorCode,
                             msg=f'The received error code {error_resp.errorCode} '
                                 f'do not match the expected one {ErrorCodes.INVALID_ARGUMENT}!')
        # end for

        self.testCaseChecked("ERR_2201_0001")
    # end def test_wrong_sensor_idx

    @features('Feature2201')
    @level('ErrorHandling')
    def test_invalid_dpi(self):
        """
        Send SetSensorDpi with invalid DPI value
        """
        for s in range(self.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI.F_SensorCount):
            for invalid_dpi in AdjustableDpiTestUtils.generate_invalid_dpi_list(self.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Send SetSensorDpi with invalid DPI value: {invalid_dpi}')
                # ------------------------------------------------------------------------------------------------------
                if self.feature_2201.VERSION < 2:
                    set_sensor_dpi_req = self.feature_2201.set_sensor_dpi_cls(device_index=self.deviceIndex,
                                                                              feature_index=self.feature_2201_index,
                                                                              sensor_idx=s,
                                                                              dpi=invalid_dpi)
                else:
                    set_sensor_dpi_req = self.feature_2201.set_sensor_dpi_cls(device_index=self.deviceIndex,
                                                                              feature_index=self.feature_2201_index,
                                                                              sensor_idx=s,
                                                                              dpi=invalid_dpi,
                                                                              dpi_level=0)
                # end if
                error_resp = self.send_report_wait_response(
                    report=set_sensor_dpi_req,
                    response_queue=self.hidDispatcher.error_message_queue,
                    response_class_type=ErrorCodes)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check Error Codes InvalidArgument (2) returned by the device')
                # ------------------------------------------------------------------------------------------------------
                self.assertEqual(expected=ErrorCodes.INVALID_ARGUMENT,
                                 obtained=error_resp.errorCode,
                                 msg=f'The received error code {error_resp.errorCode} '
                                     f'do not match the expected one {ErrorCodes.INVALID_ARGUMENT}!')
            # end for
        # end for

        self.testCaseChecked("ERR_2201_0002")
    # end def test_invalid_dpi

    @features('Feature2201v2+')
    @features('SupportDPILevels')
    @level('ErrorHandling')
    def test_invalid_dpi_level(self):
        """
        Send SetSensorDpi with invalid dpiLevel
        """
        for s in range(self.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI.F_SensorCount):
            for invalid_dpi_level in \
                    compute_wrong_range(list(range(self.max_supported_dpi_levels + 1)), max_value=0xFF):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Send SetSensorDpi with invalid dpiLevel: {invalid_dpi_level}')
                # ------------------------------------------------------------------------------------------------------
                set_sensor_dpi_req = self.feature_2201.set_sensor_dpi_cls(
                    device_index=self.deviceIndex, feature_index=self.feature_2201_index, sensor_idx=s,
                    dpi=self.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI.F_DpiDefault, dpi_level=invalid_dpi_level)

                error_resp = self.send_report_wait_response(
                    report=set_sensor_dpi_req,
                    response_queue=self.hidDispatcher.error_message_queue,
                    response_class_type=ErrorCodes)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check Error Codes InvalidArgument (2) returned by the device')
                # ------------------------------------------------------------------------------------------------------
                self.assertEqual(expected=ErrorCodes.INVALID_ARGUMENT,
                                 obtained=error_resp.errorCode,
                                 msg=f'The received error code {error_resp.errorCode} '
                                     f'do not match the expected one {ErrorCodes.INVALID_ARGUMENT}!')
            # end for
        # end for

        self.testCaseChecked("ERR_2201_0003")
    # end def test_invalid_dpi_level

    @features('Feature2201')
    @level('ErrorHandling')
    def test_wrong_function_index(self):
        """
        Send command by invalid function index shall raise an error
        """
        for function_index in compute_wrong_range(
                list(range(self.feature_2201.get_max_function_index() + 1)), max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send GetSensorCount with invalid function index value: {function_index}')
            # ----------------------------------------------------------------------------------------------------------
            get_sensor_count_req = self.feature_2201.get_sensor_count_cls(device_index=self.deviceIndex,
                                                                          feature_index=self.feature_2201_index)

            get_sensor_count_req.functionIndex = int(function_index)
            error_resp = self.send_report_wait_response(
                report=get_sensor_count_req,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Error Codes InvalidFunctionId (7) returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=get_sensor_count_req.featureIndex,
                             obtained=error_resp.featureIndex,
                             msg='The request and response feature indexes differ !')
            self.assertEqual(expected=ErrorCodes.INVALID_FUNCTION_ID,
                             obtained=error_resp.errorCode,
                             msg=f'The received error code {error_resp.errorCode} '
                                 f'do not match the expected one {ErrorCodes.INVALID_FUNCTION_ID}!')
        # end for

        self.testCaseChecked("ERR_2201_0004")
    # end def test_wrong_function_index
# end class AdjustableDpiErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
