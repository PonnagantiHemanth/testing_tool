#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.base.ads1231utils
:brief: Helpers for ``Ads1231`` feature
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/02/01
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hidpp.features.peripheral.ads1231 import Ads1231
from pyhid.hidpp.features.peripheral.ads1231 import Ads1231Factory
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class Ads1231TestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``Ads1231`` feature
    """

    class ReadCalibrationResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``ReadCalibration`` response
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``ReadCalibrationResponse`` API

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "ref_point_index": (cls.check_ref_point_index, None),
                "ref_point_out_value": (cls.check_ref_point_out_value, None),
                "ref_point_cal_value": (cls.check_ref_point_cal_value, None)
            }
        # end def get_default_check_map

        @staticmethod
        def check_ref_point_index(test_case, response, expected):
            """
            Check ref_point_index field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: ReadCalibrationResponse to check
            :type response: ``ReadCalibrationResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.ref_point_index)),
                msg=f"The ref_point_index parameter differs "
                    f"(expected:{expected}, obtained:{response.ref_point_index})")
        # end def check_ref_point_index

        @staticmethod
        def check_ref_point_out_value(test_case, response, expected):
            """
            Check ref_point_out_value field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: ReadCalibrationResponse to check
            :type response: ``ReadCalibrationResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.ref_point_out_value)),
                msg=f"The ref_point_out_value parameter differs "
                    f"(expected:{expected}, obtained:{response.ref_point_out_value})")
        # end def check_ref_point_out_value

        @staticmethod
        def check_ref_point_cal_value(test_case, response, expected):
            """
            Check ref_point_cal_value field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: ReadCalibrationResponse to check
            :type response: ``ReadCalibrationResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.ref_point_cal_value)),
                msg=f"The ref_point_cal_value parameter differs "
                    f"(expected:{expected}, obtained:{response.ref_point_cal_value})")
        # end def check_ref_point_cal_value
    # end class ReadCalibrationResponseChecker

    class WriteCalibrationResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``WriteCalibration`` response
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``WriteCalibrationResponse`` API

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "ref_point_index": (cls.check_ref_point_index, None),
                "ref_point_out_value": (cls.check_ref_point_out_value, None),
                "ref_point_cal_value": (cls.check_ref_point_cal_value, None)
            }
        # end def get_default_check_map

        @staticmethod
        def check_ref_point_index(test_case, response, expected):
            """
            Check ref_point_index field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: WriteCalibrationResponse to check
            :type response: ``WriteCalibrationResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.ref_point_index)),
                msg=f"The ref_point_index parameter differs "
                    f"(expected:{expected}, obtained:{response.ref_point_index})")
        # end def check_ref_point_index

        @staticmethod
        def check_ref_point_out_value(test_case, response, expected):
            """
            Check ref_point_out_value field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: WriteCalibrationResponse to check
            :type response: ``WriteCalibrationResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.ref_point_out_value)),
                msg=f"The ref_point_out_value parameter differs "
                    f"(expected:{expected}, obtained:{response.ref_point_out_value})")
        # end def check_ref_point_out_value

        @staticmethod
        def check_ref_point_cal_value(test_case, response, expected):
            """
            Check ref_point_cal_value field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: WriteCalibrationResponse to check
            :type response: ``WriteCalibrationResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.ref_point_cal_value)),
                msg=f"The ref_point_cal_value parameter differs "
                    f"(expected:{expected}, obtained:{response.ref_point_cal_value})")
        # end def check_ref_point_cal_value
    # end class WriteCalibrationResponseChecker

    class ReadOtherNvsDataResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``ReadOtherNvsData`` response
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``ReadOtherNvsDataResponse`` API

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "data_field_id": (cls.check_data_field_id, None),
                "data": (cls.check_data, None)
            }
        # end def get_default_check_map

        @staticmethod
        def check_data_field_id(test_case, response, expected):
            """
            Check data_field_id field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: ReadOtherNvsDataResponse to check
            :type response: ``ReadOtherNvsDataResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.data_field_id)),
                msg=f"The data_field_id parameter differs "
                    f"(expected:{expected}, obtained:{response.data_field_id})")
        # end def check_data_field_id

        @staticmethod
        def check_data(test_case, response, expected):
            """
            Check data field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: ReadOtherNvsDataResponse to check
            :type response: ``ReadOtherNvsDataResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.data)),
                msg=f"The data parameter differs "
                    f"(expected:{expected}, obtained:{response.data})")
        # end def check_data
    # end class ReadOtherNvsDataResponseChecker

    class WriteOtherNvsDataResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``WriteOtherNvsData`` response
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``WriteOtherNvsDataResponse`` API

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "data_field_id": (cls.check_data_field_id, None),
                "data": (cls.check_data, None)
            }
        # end def get_default_check_map

        @staticmethod
        def check_data_field_id(test_case, response, expected):
            """
            Check data_field_id field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: WriteOtherNvsDataResponse to check
            :type response: ``WriteOtherNvsDataResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.data_field_id)),
                msg=f"The data_field_id parameter differs "
                    f"(expected:{expected}, obtained:{response.data_field_id})")
        # end def check_data_field_id

        @staticmethod
        def check_data(test_case, response, expected):
            """
            Check data field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: WriteOtherNvsDataResponse to check
            :type response: ``WriteOtherNvsDataResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.data)),
                msg=f"The data parameter differs "
                    f"(expected:{expected}, obtained:{response.data})")
        # end def check_data
    # end class WriteOtherNvsDataResponseChecker

    class ManageDynamicCalibrationParametersResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``ManageDynamicCalibrationParameters`` response
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``ManageDynamicCalibrationParametersResponse`` API

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "command": (cls.check_command, None),
                "offset_extension": (cls.check_offset_extension, None),
                "offset_adjustment_count": (cls.check_offset_adjustment_count, None),
                "dynamic_threshold": (cls.check_dynamic_threshold, None)
            }
        # end def get_default_check_map

        @staticmethod
        def check_command(test_case, response, expected):
            """
            Check command field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: ManageDynamicCalibrationParametersResponse to check
            :type response: ``ManageDynamicCalibrationParametersResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.command)),
                msg=f"The command parameter differs "
                    f"(expected:{expected}, obtained:{response.command})")
        # end def check_command

        @staticmethod
        def check_offset_extension(test_case, response, expected):
            """
            Check offset_extension field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: ManageDynamicCalibrationParametersResponse to check
            :type response: ``ManageDynamicCalibrationParametersResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.offset_extension)),
                msg=f"The offset_extension parameter differs "
                    f"(expected:{expected}, obtained:{response.offset_extension})")
        # end def check_offset_extension

        @staticmethod
        def check_offset_adjustment_count(test_case, response, expected):
            """
            Check offset_adjustment_count field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: ManageDynamicCalibrationParametersResponse to check
            :type response: ``ManageDynamicCalibrationParametersResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.offset_adjustment_count)),
                msg=f"The offset_adjustment_count parameter differs "
                    f"(expected:{expected}, obtained:{response.offset_adjustment_count})")
        # end def check_offset_adjustment_count

        @staticmethod
        def check_dynamic_threshold(test_case, response, expected):
            """
            Check dynamic_threshold field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: ManageDynamicCalibrationParametersResponse to check
            :type response: ``ManageDynamicCalibrationParametersResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.dynamic_threshold)),
                msg=f"The dynamic_threshold parameter differs "
                    f"(expected:{expected}, obtained:{response.dynamic_threshold})")
        # end def check_dynamic_threshold
    # end class ManageDynamicCalibrationParametersResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=Ads1231.FEATURE_ID, factory=Ads1231Factory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def reset_sensor(cls, test_case, device_index=None, port_index=None):
            """
            Process ``ResetSensor``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: ResetSensorResponse
            :rtype: ``ResetSensorResponse``
            """
            feature_9215_index, feature_9215, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9215.reset_sensor_cls(
                device_index, feature_9215_index)
            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.peripheral_message_queue,
                response_class_type=test_case.feature_9215.reset_sensor_response_cls)
            return response
        # end def reset_sensor

        @classmethod
        def shutdown_sensor(cls, test_case, device_index=None, port_index=None):
            """
            Process ``ShutdownSensor``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: ShutdownSensorResponse
            :rtype: ``ShutdownSensorResponse``
            """
            feature_9215_index, feature_9215, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9215.shutdown_sensor_cls(
                device_index, feature_9215_index)
            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.peripheral_message_queue,
                response_class_type=test_case.feature_9215.shutdown_sensor_response_cls)
            return response
        # end def shutdown_sensor

        @classmethod
        def set_monitor_mode(cls, test_case, count, threshold, device_index=None, port_index=None):
            """
            Process ``SetMonitorMode``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param count: The total number of events requested
            :type count: ``int`` or ``HexList``
            :param threshold: The minimum, absolute, variation on X or Y field values so that a new report be generated
            :type threshold: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetMonitorModeResponse
            :rtype: ``SetMonitorModeResponse``
            """
            feature_9215_index, feature_9215, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9215.set_monitor_mode_cls(
                device_index, feature_9215_index,
                count=HexList(count),
                threshold=HexList(threshold))
            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.peripheral_message_queue,
                response_class_type=test_case.feature_9215.set_monitor_mode_response_cls)
            return response
        # end def set_monitor_mode

        @classmethod
        def calibrate(cls, test_case, ref_point_index, ref_point_out_value, device_index=None, port_index=None):
            """
            Process ``Calibrate``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param ref_point_index: Index of the point in the sensor output curve that we want to measure and store
            :type ref_point_index: ``int`` or ``HexList``
            :param ref_point_out_value: Expected output value at reference point, expressed as the % of the max
            output value
            :type ref_point_out_value: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: CalibrateResponse
            :rtype: ``CalibrateResponse``
            """
            feature_9215_index, feature_9215, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9215.calibrate_cls(
                device_index, feature_9215_index,
                ref_point_index=HexList(ref_point_index),
                ref_point_out_value=HexList(ref_point_out_value))
            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.peripheral_message_queue,
                response_class_type=test_case.feature_9215.calibrate_response_cls)
            return response
        # end def calibrate

        @classmethod
        def read_calibration(cls, test_case, ref_point_index, device_index=None, port_index=None):
            """
            Process ``ReadCalibration``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param ref_point_index: Index of the point in the sensor output curve that we want to measure and store
            :type ref_point_index: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: ReadCalibrationResponse
            :rtype: ``ReadCalibrationResponse``
            """
            feature_9215_index, feature_9215, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9215.read_calibration_cls(
                device_index, feature_9215_index,
                ref_point_index=HexList(ref_point_index))
            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.peripheral_message_queue,
                response_class_type=test_case.feature_9215.read_calibration_response_cls)
            return response
        # end def read_calibration

        @classmethod
        def write_calibration(cls, test_case, ref_point_index, ref_point_out_value, ref_point_cal_value,
                              device_index=None, port_index=None):
            """
            Process ``WriteCalibration``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param ref_point_index: Index of the point in the sensor output curve that we want to measure and store
            :type ref_point_index: ``int`` or ``HexList``
            :param ref_point_out_value: Expected output value at reference point, expressed as the % of the max
            output value
            :type ref_point_out_value: ``int`` or ``HexList``
            :param ref_point_cal_value: Calibration value for the reference point
            :type ref_point_cal_value: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: WriteCalibrationResponse
            :rtype: ``WriteCalibrationResponse``
            """
            feature_9215_index, feature_9215, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9215.write_calibration_cls(
                device_index, feature_9215_index,
                ref_point_index=HexList(ref_point_index),
                ref_point_out_value=HexList(ref_point_out_value),
                ref_point_cal_value=HexList(ref_point_cal_value))
            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.peripheral_message_queue,
                response_class_type=test_case.feature_9215.write_calibration_response_cls)
            return response
        # end def write_calibration

        @classmethod
        def read_other_nvs_data(cls, test_case, data_field_id, device_index=None, port_index=None):
            """
            Process ``ReadOtherNvsData``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param data_field_id: Index of the data field to read Values: 0 to 255
            :type data_field_id: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: ReadOtherNvsDataResponse
            :rtype: ``ReadOtherNvsDataResponse``
            """
            feature_9215_index, feature_9215, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9215.read_other_nvs_data_cls(
                device_index, feature_9215_index,
                data_field_id=HexList(data_field_id))
            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.peripheral_message_queue,
                response_class_type=test_case.feature_9215.read_other_nvs_data_response_cls)
            return response
        # end def read_other_nvs_data

        @classmethod
        def write_other_nvs_data(cls, test_case, data_field_id, data, device_index=None, port_index=None):
            """
            Process ``WriteOtherNvsData``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param data_field_id: Index of the data field to read Values: 0 to 255
            :type data_field_id: ``int`` or ``HexList``
            :param data: Data
            :type data: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: WriteOtherNvsDataResponse
            :rtype: ``WriteOtherNvsDataResponse``
            """
            feature_9215_index, feature_9215, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9215.write_other_nvs_data_cls(
                device_index, feature_9215_index,
                data_field_id=HexList(data_field_id),
                data=HexList(data))
            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.peripheral_message_queue,
                response_class_type=test_case.feature_9215.write_other_nvs_data_response_cls)
            return response
        # end def write_other_nvs_data

        @classmethod
        def manage_dynamic_calibration_parameters(cls, test_case, command, offset_extension, offset_adjustment_count,
                                                  dynamic_threshold, device_index=None, port_index=None):
            """
            Process ``ManageDynamicCalibrationParameters``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param command: Command
            :type command: ``int`` or ``HexList``
            :param offset_extension: Offset Extension
            :type offset_extension: ``int`` or ``HexList``
            :param offset_adjustment_count: Offset Adjustment Count
            :type offset_adjustment_count: ``int`` or ``HexList``
            :param dynamic_threshold: Dynamic Threshold
            :type dynamic_threshold: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: ManageDynamicCalibrationParametersResponse
            :rtype: ``ManageDynamicCalibrationParametersResponse``
            """
            feature_9215_index, feature_9215, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9215.manage_dynamic_calibration_parameters_cls(
                device_index, feature_9215_index,
                command=HexList(command),
                offset_extension=HexList(offset_extension),
                offset_adjustment_count=HexList(offset_adjustment_count),
                dynamic_threshold=HexList(dynamic_threshold))
            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.peripheral_message_queue,
                response_class_type=test_case.feature_9215.manage_dynamic_calibration_parameters_response_cls)
            return response
        # end def manage_dynamic_calibration_parameters

        @classmethod
        def monitor_report_event(cls, test_case):
            """
            Process ``MonitorReportEvent``: get notification from event queue

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: MonitorReportEvent
            :rtype: ``MonitorReportEvent``
            """
            return test_case.getMessage(queue=test_case.hidDispatcher.event_message_queue,
                                        class_type=test_case.feature_9215.monitor_report_event_cls)
        # end def monitor_report_event
    # end class HIDppHelper
# end class Ads1231TestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
