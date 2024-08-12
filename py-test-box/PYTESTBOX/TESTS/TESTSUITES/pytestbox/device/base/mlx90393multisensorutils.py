#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.base.mlx90393multisensorutils
:brief: Helpers for MLX Multi Sensor feature
:author: Ganesh Thiraviam <gthiraviam@logitech.com>
:date: 2021/03/10
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.hidpp.features.peripheral.mlx90393multisensor import MLX90393MultiSensor
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.basetestutils import CommonBaseTestUtils

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
LogHelper = CommonBaseTestUtils.LogHelper


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class MLX90393MultiSensorTestUtils(CommonBaseTestUtils):
    """
    This class provides helpers for common checks on MLX90393MultiSensor feature
    """
    @staticmethod
    def check_sensor_id(test_case, response, expected):
        """
        Check sensor_id field in response

        :param test_case: Current test case
        :type test_case: ``BaseTestCase``
        :param response: Response to check
        :type response: ``WriteSensorRegisterResponse`` or ``ReadSensorRegisterResponse``
            or ``ResetSensorResponse`` or ``ShutdownSensorResponse`` or ``ReadCalibrationResponse``
            or ``MonitorTestResponse`` or  ``StartCalibrationResponse``
        :param expected: Expected value
        :type expected: ``int`` or ``HexList``
        """
        # --------------------------------------------------
        LogHelper.log_check(test_case, "Validate sensor_id")
        # --------------------------------------------------
        test_case.assertEqual(
            expected=expected,
            obtained=response.sensor_id,
            msg=f"The obtained sensor_id ({response.sensor_id}) differs from the expected({expected})")
    # end def check_sensor_id

    @staticmethod
    def check_reg_addr(test_case, response, expected):
        """
        Check reg_addr field in response

        :param test_case: Current test case
        :type test_case: ``BaseTestCase``
        :param response: Response to check
        :type response: ``WriteSensorRegisterResponse`` or ``ReadSensorRegisterResponse``
        :param expected: Expected value
        :type expected: ``int`` or ``HexList``
        """
        # -------------------------------------------------
        LogHelper.log_check(test_case, "Validate reg_addr")
        # -------------------------------------------------
        test_case.assertEqual(
            expected=HexList(expected),
            obtained=response.reg_addr,
            msg=f"The obtained register address ({response.reg_addr}) differs from the expected({expected})")
    # end def check_reg_addr

    @staticmethod
    def check_reg_value(test_case, response, expected):
        """
        Check reg_value field in response

        :param test_case: Current test case
        :type test_case: ``BaseTestCase``
        :param response: Response to check
        :type response: ``WriteSensorRegisterResponse`` or ``ReadSensorRegisterResponse``
        :param expected: Expected value
        :type expected: ``str`` or ``HexList``
        """
        # --------------------------------------------------
        LogHelper.log_check(test_case, "Validate reg_value")
        # --------------------------------------------------
        test_case.assertEqual(
            expected=HexList(expected),
            obtained=response.reg_value,
            msg=f"The obtained reg value({response.reg_value}) differs from the expected({expected})")
    # end def check_reg_value

    @staticmethod
    def check_calibration_data(test_case, response, expected):
        """
        Check calibration_data field in response

        :param test_case: Current test case
        :type test_case: ``BaseTestCase``
        :param response: Response to check
        :type response: ``ReadCalibrationResponse`` or ``WriteCalibrationResponse`` or ``StopCalibrationResponse``
        :param expected: Expected value
        :type expected: ``int`` or ``HexList``
        """
        # ---------------------------------------------------------
        LogHelper.log_check(test_case, "Validate calibration_data")
        # ---------------------------------------------------------
        test_case.assertNotEqual(
            expected=HexList(expected),
            obtained=response.calibration_data,
            msg=f"The obtained calibration data({response.calibration_data}) is not valid")
    # end def check_calibration_data

    @staticmethod
    def check_count(test_case, response, expected):
        """
        Check count field in response

        :param test_case: Current test case
        :type test_case: ``BaseTestCase``
        :param response: Response to check
        :type response: ``MonitorTestResponse``
        :param expected: Expected value
        :type expected: ``int`` or ``HexList``
        """
        # ----------------------------------------------
        LogHelper.log_check(test_case, "Validate count")
        # ----------------------------------------------
        test_case.assertEqual(
            expected=HexList(expected),
            obtained=response.count,
            msg=f"The obtained({response.count}) differs from the expected({expected})")
    # end def check_count

    @staticmethod
    def check_threshold(test_case, response, expected):
        """
        Check threshold field in response

        :param test_case: Current test case
        :type test_case: ``BaseTestCase``
        :param response: Response to check
        :type response: ``MonitorTestResponse``
        :param expected: Expected value
        :type expected: ``int`` or ``HexList``
        """
        # --------------------------------------------------
        LogHelper.log_check(test_case, "Validate threshold")
        # --------------------------------------------------
        test_case.assertEqual(
            expected=HexList(expected),
            obtained=response.threshold,
            msg=f"The obtained({response.threshold}) differs from the expected({expected})")
    # end def check_threshold

    @staticmethod
    def check_command(test_case, response, expected):
        """
        Check command field in response

        :param test_case: Current test case
        :type test_case: ``BaseTestCase``
        :param response: Response to check
        :type response: ``ManageDynCallParamResponse``
        :param expected: Expected value
        :type expected: ``int`` or ``HexList``
        """
        # ------------------------------------------------
        LogHelper.log_check(test_case, "Validate command")
        # ------------------------------------------------
        test_case.assertEqual(
            expected=expected,
            obtained=response.command,
            msg=f"The obtained({response.command}) differs from the expected({expected})")
    # end def check_command

    @staticmethod
    def check_parameters(test_case, response, expected):
        """
        Check parameters field in response

        :param test_case: Current test case
        :type test_case: ``BaseTestCase``
        :param response: Response to check
        :type response: ``ManageDynCallParamResponse``
        :param expected: Expected value
        :type expected: ``int`` or ``HexList``
        """
        # ---------------------------------------------------
        LogHelper.log_check(test_case, "Validate parameters")
        # ---------------------------------------------------
        test_case.assertEqual(
                expected=HexList(expected),
                obtained=response.parameters,
                msg=f"The obtained({response.parameters}) differs from the expected({expected})")
    # end def check_parameters

    class ReadSensorRegisterHelper(object):
        """
        ReadSensorRegister helper
        """
        class HIDppHelper(CommonBaseTestUtils.HIDppHelper):
            """
            ReadSensorRegister HIDppHelper
            """
            @classmethod
            def read(cls, test_case, sensor_id, reg_addr):
                """
                Validate read

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param sensor_id: Sensor ID
                :type sensor_id: ``int`` or ``HexList``
                :param reg_addr: Register Address
                :type reg_addr: ``int`` or ``HexList``
                :return: ReadSensorRegisterResponse
                :rtype: ``ReadSensorRegisterResponse``
                """
                # --------------------------------------------------------------
                LogHelper.log_step(test_case, "Send ReadSensorRegister request")
                # --------------------------------------------------------------
                report = test_case.feature_9209.read_sensor_register_cls(
                        test_case.deviceIndex,
                        test_case.feature_9209_index,
                        HexList(sensor_id),
                        HexList(reg_addr))
                response = test_case.send_report_wait_response(
                        report=report,
                        response_queue=test_case.hidDispatcher.peripheral_message_queue,
                        response_class_type=test_case.feature_9209.read_sensor_register_response_cls)
                return response
            # end def read

            @classmethod
            def wrong_index(cls, test_case, sensor_id, reg_addr):
                """
                Validate wrong index

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param sensor_id: Sensor ID
                :type sensor_id: ``int`` or ``HexList``
                :param reg_addr: Register Address
                :type reg_addr: ``int`` or ``HexList``
                """
                wrong_index = MLX90393MultiSensor.MAX_FUNCTION_INDEX + 1
                # --------------------------------------------------------------------------------------------------
                LogHelper.log_step(test_case, f"Send ReadSensorRegister request with function index: {wrong_index}")
                # --------------------------------------------------------------------------------------------------
                report = test_case.feature_9209.read_sensor_register_cls(
                        test_case.deviceIndex,
                        test_case.feature_9209_index,
                        HexList(sensor_id),
                        HexList(reg_addr))
                report.functionIndex = wrong_index
                error_response = test_case.send_report_wait_response(
                        report=report,
                        response_queue=test_case.hidDispatcher.error_message_queue,
                        response_class_type=ErrorCodes)
                # --------------------------------------------------------------------------------------
                LogHelper.log_check(test_case, f"Validate error code: {ErrorCodes.INVALID_FUNCTION_ID}")
                # --------------------------------------------------------------------------------------
                test_case.assertEqual(obtained=int(Numeral(error_response.errorCode)),
                                      expected=ErrorCodes.INVALID_FUNCTION_ID,
                                      msg="The error_code parameter differs from the one expected")
            # end def wrong_index

            @classmethod
            def padding(cls, test_case, sensor_id, reg_addr, reg_value):
                """
                Validate padding

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param sensor_id: Sensor ID
                :type sensor_id: ``int`` or ``HexList``
                :param reg_addr: Register Address
                :type reg_addr: ``int`` or ``HexList``
                :param reg_value: Register Value
                :type reg_value: ``str`` or ``HexList``
                """
                request_cls = test_case.feature_9209.read_sensor_register_cls
                for padding in compute_sup_values(HexList(Numeral(
                        request_cls.DEFAULT.PADDING,
                        request_cls.LEN.PADDING // 8))):
                    # --------------------------------------------------------------------------------------
                    LogHelper.log_step(test_case, f"Send ReadSensorRegister request with padding:{padding}")
                    # --------------------------------------------------------------------------------------
                    report = request_cls(
                            test_case.deviceIndex,
                            test_case.feature_9209_index,
                            HexList(sensor_id),
                            HexList(reg_addr))
                    report.padding = padding
                    response = test_case.send_report_wait_response(
                            report=report,
                            response_queue=test_case.hidDispatcher.peripheral_message_queue,
                            response_class_type=test_case.feature_9209.read_sensor_register_response_cls)
                    MLX90393MultiSensorTestUtils.check_sensor_id(test_case, response, HexList(sensor_id))
                    MLX90393MultiSensorTestUtils.check_reg_addr(test_case, response, reg_addr)
                    MLX90393MultiSensorTestUtils.check_reg_value(test_case, response, reg_value)
                # end for
            # end def padding
        # end class HIDppHelper
    # end class ReadSensorRegisterHelper

    class WriteSensorRegisterHelper(object):
        """
        WriteSensorRegister helper
        """
        class HIDppHelper(CommonBaseTestUtils.HIDppHelper):
            """
            WriteSensorRegister HIDppHelper
            """
            @classmethod
            def write(cls, test_case, sensor_id, reg_addr, reg_value):
                """
                Validate write

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param sensor_id: Sensor ID
                :type sensor_id: ``int`` or ``HexList``
                :param reg_addr: Register Address
                :type reg_addr: ``int`` or ``HexList``
                :param reg_value: Register Value
                :type reg_value: ``str`` or ``HexList``
                :return: WriteSensorRegisterResponse
                :rtype: ``WriteSensorRegisterResponse``
                """
                # ---------------------------------------------------------------
                LogHelper.log_step(test_case, "Send WriteSensorRegister request")
                # ---------------------------------------------------------------
                report = test_case.feature_9209.write_sensor_register_cls(
                        test_case.deviceIndex,
                        test_case.feature_9209_index,
                        HexList(sensor_id),
                        HexList(reg_addr),
                        HexList(reg_value))
                response = test_case.send_report_wait_response(
                        report=report,
                        response_queue=test_case.hidDispatcher.peripheral_message_queue,
                        response_class_type=test_case.feature_9209.write_sensor_register_response_cls)
                return response
            # end def write

            @classmethod
            def padding(cls, test_case, sensor_id, reg_addr, reg_value):
                """
                Validate padding

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param sensor_id: Sensor ID
                :type sensor_id: ``int`` or ``HexList``
                :param reg_addr: Register Address
                :type reg_addr: ``int`` or ``HexList``
                :param reg_value: Register Value
                :type reg_value: ``str`` or ``HexList``
                """
                request_cls = test_case.feature_9209.write_sensor_register_cls
                for padding in compute_sup_values(HexList(Numeral(
                        request_cls.DEFAULT.PADDING,
                        request_cls.LEN.PADDING // 8))):
                    # ---------------------------------------------------------------------------------------
                    LogHelper.log_step(test_case, f"Send WriteSensorRegister request with padding:{padding}")
                    # ---------------------------------------------------------------------------------------
                    report = request_cls(
                            test_case.deviceIndex,
                            test_case.feature_9209_index,
                            HexList(sensor_id),
                            HexList(reg_addr),
                            HexList(reg_value))
                    report.padding = padding
                    response = test_case.send_report_wait_response(
                            report=report,
                            response_queue=test_case.hidDispatcher.peripheral_message_queue,
                            response_class_type=test_case.feature_9209.write_sensor_register_response_cls)
                    MLX90393MultiSensorTestUtils.check_sensor_id(test_case, response, HexList(sensor_id))
                    MLX90393MultiSensorTestUtils.check_reg_addr(test_case, response, reg_addr)
                    MLX90393MultiSensorTestUtils.check_reg_value(test_case, response, reg_value)
                # end for
            # end def padding
        # end class HIDppHelper
    # end class WriteSensorRegisterHelper

    class ResetSensorHelper(object):
        """
        ResetSensor helper
        """
        class HIDppHelper(CommonBaseTestUtils.HIDppHelper):
            """
            ResetSensor HIDppHelper
            """
            @classmethod
            def write(cls, test_case, sensor_id):
                """
                Validate write

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param sensor_id: Sensor ID
                :type sensor_id: ``int`` or ``HexList``
                :return: ResetSensorResponse
                :rtype: ``ResetSensorResponse``
                """
                # -------------------------------------------------------
                LogHelper.log_step(test_case, "Send ResetSensor request")
                # -------------------------------------------------------
                report = test_case.feature_9209.reset_sensor_cls(
                        test_case.deviceIndex,
                        test_case.feature_9209_index,
                        HexList(sensor_id))
                response = test_case.send_report_wait_response(
                        report=report,
                        response_queue=test_case.hidDispatcher.peripheral_message_queue,
                        response_class_type=test_case.feature_9209.reset_sensor_response_cls)
                return response
            # end def write

            @classmethod
            def padding(cls, test_case, sensor_id):
                """
                Validate padding

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param sensor_id: Sensor ID
                :type sensor_id: ``int`` or ``HexList``
                """
                request_cls = test_case.feature_9209.reset_sensor_cls
                for padding in compute_sup_values(HexList(Numeral(
                        request_cls.DEFAULT.PADDING,
                        request_cls.LEN.PADDING // 8))):
                    # -------------------------------------------------------------------------------
                    LogHelper.log_step(test_case, f"Send ResetSensor request with padding:{padding}")
                    # -------------------------------------------------------------------------------
                    report = request_cls(
                            test_case.deviceIndex,
                            test_case.feature_9209_index,
                            HexList(sensor_id))
                    report.padding = padding
                    response = test_case.send_report_wait_response(
                            report=report,
                            response_queue=test_case.hidDispatcher.peripheral_message_queue,
                            response_class_type=test_case.feature_9209.reset_sensor_response_cls)
                    MLX90393MultiSensorTestUtils.check_sensor_id(test_case, response, HexList(sensor_id))
                # end for
            # end def padding
        # end class HIDppHelper
    # end class ResetSensorHelper

    class ShutdownSensorHelper(object):
        """
        ShutdownSensor helper
        """
        class HIDppHelper(CommonBaseTestUtils.HIDppHelper):
            """
            ShutdownSensor HIDppHelper
            """
            @classmethod
            def write(cls, test_case, sensor_id):
                """
                Validate write

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param sensor_id: Sensor ID
                :type sensor_id: ``int`` or ``HexList``
                :return: ShutdownSensorResponse
                :rtype: ``ShutdownSensorResponse``
                """
                # ----------------------------------------------------------
                LogHelper.log_step(test_case, "Send ShutdownSensor request")
                # ----------------------------------------------------------
                report = test_case.feature_9209.shutdown_sensor_cls(
                        test_case.deviceIndex,
                        test_case.feature_9209_index,
                        HexList(sensor_id))
                response = test_case.send_report_wait_response(
                        report=report,
                        response_queue=test_case.hidDispatcher.peripheral_message_queue,
                        response_class_type=test_case.feature_9209.shutdown_sensor_response_cls)
                return response
            # end def write

            @classmethod
            def padding(cls, test_case, sensor_id):
                """
                Validate padding

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param sensor_id: Sensor ID
                :type sensor_id: ``int`` or ``HexList``
                """
                request_cls = test_case.feature_9209.shutdown_sensor_cls
                for padding in compute_sup_values(HexList(Numeral(
                        request_cls.DEFAULT.PADDING,
                        request_cls.LEN.PADDING // 8))):
                    # ----------------------------------------------------------------------------------
                    LogHelper.log_step(test_case, f"Send ShutdownSensor request with padding:{padding}")
                    # ----------------------------------------------------------------------------------
                    report = request_cls(
                            test_case.deviceIndex,
                            test_case.feature_9209_index,
                            HexList(sensor_id))
                    report.padding = padding
                    response = test_case.send_report_wait_response(
                            report=report,
                            response_queue=test_case.hidDispatcher.peripheral_message_queue,
                            response_class_type=test_case.feature_9209.shutdown_sensor_response_cls)
                    MLX90393MultiSensorTestUtils.check_sensor_id(test_case, response, HexList(sensor_id))
                # end for
            # end def padding
        # end class HIDppHelper
    # end class ShutdownSensorHelper

    class MonitorTestHelper(object):
        """
        MonitorTest helper
        """
        class HIDppHelper(CommonBaseTestUtils.HIDppHelper):
            """
            MonitorTest HIDppHelper
            """
            @classmethod
            def read(cls, test_case, sensor_id, count, threshold):
                """
                Validate read

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param sensor_id: Sensor Index
                :type sensor_id: ``int`` or ``HexList``
                :param count: Monitor Mode Sample (counter)
                :type count: ``int`` or ``HexList``
                :param threshold: Monitor Mode Threshold
                :type threshold: ``int`` or ``HexList``
                :return: MonitorTestResponse
                :rtype: ``MonitorTestResponse``
                """
                # -------------------------------------------------------
                LogHelper.log_step(test_case, "Send MonitorTest request")
                # -------------------------------------------------------
                report = test_case.feature_9209.monitor_test_cls(
                        test_case.deviceIndex,
                        test_case.feature_9209_index,
                        HexList(sensor_id),
                        HexList(count),
                        HexList(threshold))
                response = test_case.send_report_wait_response(
                        report=report,
                        response_queue=test_case.hidDispatcher.peripheral_message_queue,
                        response_class_type=test_case.feature_9209.monitor_test_response_cls)
                return response
            # end def read

            @classmethod
            def padding(cls, test_case, sensor_id, count, threshold):
                """
                Validate padding

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param sensor_id: Sensor Index
                :type sensor_id: ``int`` or ``HexList``
                :param count: Monitor Mode Sample (counter)
                :type count: ``str`` or ``HexList``
                :param threshold: Monitor Mode Threshold
                :type threshold: ``str`` or ``HexList``
                """
                request_cls = test_case.feature_9209.monitor_test_cls
                for padding in compute_sup_values(HexList(Numeral(
                        request_cls.DEFAULT.PADDING,
                        request_cls.LEN.PADDING // 8))):
                    # -------------------------------------------------------------------------------
                    LogHelper.log_step(test_case, f"Send MonitorTest request with padding:{padding}")
                    # -------------------------------------------------------------------------------
                    report = request_cls(
                            test_case.deviceIndex,
                            test_case.feature_9209_index,
                            HexList(sensor_id),
                            HexList(count),
                            HexList(threshold))
                    report.padding = padding
                    response = test_case.send_report_wait_response(
                            report=report,
                            response_queue=test_case.hidDispatcher.peripheral_message_queue,
                            response_class_type=test_case.feature_9209.monitor_test_response_cls)
                    MLX90393MultiSensorTestUtils.check_sensor_id(test_case, response, HexList(sensor_id))
                    MLX90393MultiSensorTestUtils.check_count(test_case, response, count)
                    MLX90393MultiSensorTestUtils.check_threshold(test_case, response, threshold)
                # end for
            # end def padding
        # end class HIDppHelper
    # end class MonitorTestHelper

    class StartCalibrationHelper(object):
        """
        StartCalibration helper
        """
        class HIDppHelper(CommonBaseTestUtils.HIDppHelper):
            """
            StartCalibration HIDppHelper
            """
            @classmethod
            def write(cls, test_case, sensor_id):
                """
                Validate write

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param sensor_id: Sensor ID
                :type sensor_id: ``int`` or ``HexList``
                :return: StartCalibrationResponse
                :rtype: ``StartCalibrationResponse``
                """
                # ------------------------------------------------------------
                LogHelper.log_step(test_case, "Send StartCalibration request")
                # ------------------------------------------------------------
                report = test_case.feature_9209.start_calibration_cls(
                        test_case.deviceIndex,
                        test_case.feature_9209_index,
                        HexList(sensor_id))
                response = test_case.send_report_wait_response(
                        report=report,
                        response_queue=test_case.hidDispatcher.peripheral_message_queue,
                        response_class_type=test_case.feature_9209.start_calibration_response_cls)
                return response
            # end def write

            @classmethod
            def padding(cls, test_case, sensor_id):
                """
                Validate padding

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param sensor_id: Sensor ID
                :type sensor_id: ``int`` or ``HexList``
                """
                request_cls = test_case.feature_9209.start_calibration_cls
                for padding in compute_sup_values(HexList(Numeral(
                        request_cls.DEFAULT.PADDING,
                        request_cls.LEN.PADDING // 8))):
                    # ------------------------------------------------------------------------------------
                    LogHelper.log_step(test_case, f"Send StartCalibration request with padding:{padding}")
                    # ------------------------------------------------------------------------------------
                    report = request_cls(
                            test_case.deviceIndex,
                            test_case.feature_9209_index,
                            HexList(sensor_id))
                    report.padding = padding
                    response = test_case.send_report_wait_response(
                            report=report,
                            response_queue=test_case.hidDispatcher.peripheral_message_queue,
                            response_class_type=test_case.feature_9209.start_calibration_response_cls)
                    MLX90393MultiSensorTestUtils.check_sensor_id(test_case, response, HexList(sensor_id))
                # end for
            # end def padding
        # end class HIDppHelper
    # end class StartCalibrationHelper

    class StopCalibrationHelper(object):
        """
        StopCalibration helper
        """
        class HIDppHelper(CommonBaseTestUtils.HIDppHelper):
            """
            StopCalibration HIDppHelper
            """
            @classmethod
            def write(cls, test_case, sensor_id):
                """
                Validate write

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param sensor_id: Sensor ID
                :type sensor_id: ``int`` or ``HexList``
                :return: StopCalibrationResponse
                :rtype: ``StopCalibrationResponse``
                """
                # -----------------------------------------------------------
                LogHelper.log_step(test_case, "Send StopCalibration request")
                # -----------------------------------------------------------
                report = test_case.feature_9209.stop_calibration_cls(
                        test_case.deviceIndex,
                        test_case.feature_9209_index,
                        HexList(sensor_id))
                response = test_case.send_report_wait_response(
                        report=report,
                        response_queue=test_case.hidDispatcher.peripheral_message_queue,
                        response_class_type=test_case.feature_9209.stop_calibration_response_cls)
                return response
            # end def write

            @classmethod
            def padding(cls, test_case, sensor_id):
                """
                Validate padding
                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param sensor_id: Sensor ID
                :type sensor_id: ``int`` or ``HexList``
                """
                request_cls = test_case.feature_9209.stop_calibration_cls
                product = test_case.f.PRODUCT.FEATURES.PERIPHERAL.MLX_90393_MULTI_SENSOR
                for padding in compute_sup_values(HexList(Numeral(
                        request_cls.DEFAULT.PADDING,
                        request_cls.LEN.PADDING // 8))):
                    # -----------------------------------------------------------------------------------
                    LogHelper.log_step(test_case, f"Send StopCalibration request with padding:{padding}")
                    # -----------------------------------------------------------------------------------
                    report = request_cls(
                            test_case.deviceIndex,
                            test_case.feature_9209_index,
                            HexList(sensor_id))
                    report.padding = padding
                    response = test_case.send_report_wait_response(
                            report=report,
                            response_queue=test_case.hidDispatcher.peripheral_message_queue,
                            response_class_type=test_case.feature_9209.stop_calibration_response_cls)
                    MLX90393MultiSensorTestUtils.check_sensor_id(test_case, response, HexList(sensor_id))
                    calibration_data = product.F_CalibrationData[sensor_id]
                    MLX90393MultiSensorTestUtils.check_calibration_data(test_case, response, calibration_data)
                # end for
            # end def padding
        # end class HIDppHelper
    # end class StopCalibrationHelper

    class ReadCalibrationHelper(object):
        """
        ReadCalibration helper
        """
        class HIDppHelper(CommonBaseTestUtils.HIDppHelper):
            """
            ReadCalibration HIDppHelper
            """
            @classmethod
            def read(cls, test_case, sensor_id):
                """
                Validate read

                :param test_case: Current test case
                :param sensor_id: Sensor Index
                :type sensor_id: ``int`` or ``HexList``
                :type test_case: ``BaseTestCase``
                :return: ReadCalibrationResponse
                :rtype: ``ReadCalibrationResponse``
                """
                # -----------------------------------------------------------
                LogHelper.log_step(test_case, "Send ReadCalibration request")
                # -----------------------------------------------------------
                report = test_case.feature_9209.read_calibration_cls(
                        test_case.deviceIndex, test_case.feature_9209_index, HexList(sensor_id))
                response = test_case.send_report_wait_response(
                        report=report,
                        response_queue=test_case.hidDispatcher.peripheral_message_queue,
                        response_class_type=test_case.feature_9209.read_calibration_response_cls)
                return response
            # end def read

            @classmethod
            def padding(cls, test_case, sensor_id):
                """
                Validate padding

                :param test_case: Current test case
                :param sensor_id: Sensor Index
                :type sensor_id: ``int`` or ``HexList``
                :type test_case: ``BaseTestCase``
                """
                request_cls = test_case.feature_9209.read_calibration_cls
                product = test_case.f.PRODUCT.FEATURES.PERIPHERAL.MLX_90393_MULTI_SENSOR
                for padding in compute_sup_values(HexList(Numeral(
                        request_cls.DEFAULT.PADDING,
                        request_cls.LEN.PADDING // 8))):
                    # -----------------------------------------------------------------------------------
                    LogHelper.log_step(test_case, f"Send ReadCalibration request with padding:{padding}")
                    # -----------------------------------------------------------------------------------
                    report = request_cls(
                            test_case.deviceIndex, test_case.feature_9209_index, HexList(sensor_id))
                    report.padding = padding
                    response = test_case.send_report_wait_response(
                            report=report,
                            response_queue=test_case.hidDispatcher.peripheral_message_queue,
                            response_class_type=test_case.feature_9209.read_calibration_response_cls)
                    MLX90393MultiSensorTestUtils.check_sensor_id(test_case, response, HexList(sensor_id))
                    calibration_data = product.F_CalibrationData[sensor_id]
                    MLX90393MultiSensorTestUtils.check_calibration_data(test_case, response, calibration_data)
                # end for
            # end def padding
        # end class HIDppHelper
    # end class ReadCalibrationHelper

    class WriteCalibrationHelper(object):
        """
        WriteCalibration helper
        """
        class HIDppHelper(CommonBaseTestUtils.HIDppHelper):
            """
            WriteCalibration HIDppHelper
            """
            @classmethod
            def write(cls, test_case, sensor_id, calibration_data):
                """
                Validate write

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param sensor_id: Sensor Index
                :type sensor_id: ``int`` or ``HexList``
                :param calibration_data: Calibration Data
                :type calibration_data: ``int`` or ``HexList``
                :return: WriteCalibrationResponse
                :rtype: ``WriteCalibrationResponse``
                """
                # ------------------------------------------------------------
                LogHelper.log_step(test_case, "Send WriteCalibration request")
                # ------------------------------------------------------------
                report = test_case.feature_9209.write_calibration_cls(
                        test_case.deviceIndex, test_case.feature_9209_index,
                        HexList(sensor_id), HexList(calibration_data))
                response = test_case.send_report_wait_response(
                        report=report,
                        response_queue=test_case.hidDispatcher.peripheral_message_queue,
                        response_class_type=test_case.feature_9209.write_calibration_response_cls)
                return response
            # end def write

            @classmethod
            def padding(cls, test_case, sensor_id, calibration_data):
                """
                Validate padding

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param sensor_id: Sensor Index
                :type sensor_id: ``int`` or ``HexList``
                :param calibration_data: Calibration Data
                :type calibration_data: ``int`` or ``HexList``
                """
                request_cls = test_case.feature_9209.write_calibration_cls
                product = test_case.f.PRODUCT.FEATURES.PERIPHERAL.MLX_90393_MULTI_SENSOR
                for padding in compute_sup_values(HexList(Numeral(
                        request_cls.DEFAULT.PADDING,
                        request_cls.LEN.PADDING // 8))):
                    # ------------------------------------------------------------------------------------
                    LogHelper.log_step(test_case, f"Send WriteCalibration request with padding:{padding}")
                    # ------------------------------------------------------------------------------------
                    report = request_cls(
                            test_case.deviceIndex,
                            test_case.feature_9209_index,
                            HexList(sensor_id),
                            HexList(calibration_data))
                    report.padding = padding
                    response = test_case.send_report_wait_response(
                            report=report,
                            response_queue=test_case.hidDispatcher.peripheral_message_queue,
                            response_class_type=test_case.feature_9209.write_calibration_response_cls)
                    MLX90393MultiSensorTestUtils.check_sensor_id(test_case, response, HexList(sensor_id))
                    calibration_data = product.F_CalibrationData[sensor_id]
                    MLX90393MultiSensorTestUtils.check_calibration_data(test_case, response, calibration_data)
                # end for
            # end def padding
        # end class HIDppHelper
    # end class WriteCalibrationHelper

    class CalibrateHelper(object):
        """
        Calibrate helper
        """
        class HIDppHelper(CommonBaseTestUtils.HIDppHelper):
            """
            Calibrate HIDppHelper
            """
            @classmethod
            def write(cls, test_case, sensor_id, ref_point_id, ref_point_out_val):
                """
                Validate write

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param sensor_id: Sensor Index
                :type sensor_id: ``int`` or ``HexList``
                :param ref_point_id: Reference Point Index
                :type ref_point_id: ``int`` or ``HexList``
                :param ref_point_out_val: Reference Point Out Value
                :type ref_point_out_val: ``int`` or ``HexList``
                :return: CalibrateResponse
                :rtype: ``CalibrateResponse``
                """
                # -----------------------------------------------------
                LogHelper.log_step(test_case, "Send Calibrate request")
                # -----------------------------------------------------
                report = test_case.feature_9209.calibrate_cls(
                        test_case.deviceIndex, test_case.feature_9209_index,
                        HexList(sensor_id), HexList(ref_point_id), HexList(ref_point_out_val))
                response = test_case.send_report_wait_response(
                        report=report,
                        response_queue=test_case.hidDispatcher.peripheral_message_queue,
                        response_class_type=test_case.feature_9209.calibrate_response_cls)
                return response
            # end def write
        # end class HIDppHelper
    # end class CalibrateHelper

    class ManageDynCallParamHelper(object):
        """
        ManageDynCallParam helper
        """
        class HIDppHelper(CommonBaseTestUtils.HIDppHelper):
            """
            ManageDynCallParam HIDppHelper
            """
            @classmethod
            def write(cls, test_case, command, sensor_id, parameters):
                """
                Validate write

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param command: Command
                :type command: ``int`` or ``HexList``
                :param sensor_id: Sensor Index
                :type sensor_id: ``int`` or ``HexList``
                :param parameters: Dynamic Call Parameters
                :type parameters: ``int`` or ``HexList``
                :return: ManageDynCallParamResponse
                :rtype: ``ManageDynCallParamResponse``
                """
                # --------------------------------------------------------
                LogHelper.log_step(test_case, "Send ManageDynCal request")
                # --------------------------------------------------------
                report = test_case.feature_9209.manage_dyn_call_param_cls(
                        test_case.deviceIndex,
                        test_case.feature_9209_index,
                        command,
                        sensor_id,
                        HexList(parameters))
                response = test_case.send_report_wait_response(
                        report=report,
                        response_queue=test_case.hidDispatcher.peripheral_message_queue,
                        response_class_type=test_case.feature_9209.manage_dyn_call_param_response_cls)
                return response
            # end def write

            @classmethod
            def padding(cls, test_case, command, sensor_id, parameters):
                """
                Validate padding

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param command: Command
                :type command: ``int`` or ``HexList``
                :param sensor_id: Sensor Index
                :type sensor_id: ``int`` or ``HexList``
                :param parameters: Dynamic Call Parameters
                :type parameters: ``int`` or ``HexList``
                """
                request_cls = test_case.feature_9209.manage_dyn_call_param_cls
                for padding in compute_sup_values(HexList(Numeral(
                        request_cls.DEFAULT.PADDING,
                        request_cls.LEN.PADDING // 8))):
                    # --------------------------------------------------------------------------------
                    LogHelper.log_step(test_case, f"Send ManageDynCal request with padding:{padding}")
                    # --------------------------------------------------------------------------------
                    report = request_cls(
                            test_case.deviceIndex,
                            test_case.feature_9209_index,
                            command,
                            sensor_id,
                            HexList(parameters))
                    report.padding = padding
                    response = test_case.send_report_wait_response(
                            report=report,
                            response_queue=test_case.hidDispatcher.peripheral_message_queue,
                            response_class_type=test_case.feature_9209.manage_dyn_call_param_response_cls)
                    MLX90393MultiSensorTestUtils.check_sensor_id(test_case, response, sensor_id)
                    MLX90393MultiSensorTestUtils.check_parameters(test_case, response, parameters)
                # end for
            # end def padding
        # end class HIDppHelper
    # end class ManageDynCallParamHelper

    class MonitorReportEventHelper(object):
        """
        MonitorReportEvent helper
        """
        class HIDppHelper(CommonBaseTestUtils.HIDppHelper):
            """
            MonitorReportEvent HIDppHelper
            """
            @classmethod
            def monitor_report(cls, test_case):
                """
                Process MonitorReportEvent

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :return: MonitorReportEventResponse
                :rtype: ``MonitorReportEventResponse``
                """
                # ---------------------------------------------------------------
                LogHelper.log_step(test_case, "Send MonitorReportEvent request")
                # ---------------------------------------------------------------
                monitor_report_event = test_case.getMessage(queue=test_case.hidDispatcher.event_message_queue,
                                                            class_type=test_case.feature_9209.
                                                            monitor_report_event_cls)
                return monitor_report_event
            # end def monitor_report
        # end class HIDppHelper
# end class MLX90393MultiSensorTestUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
