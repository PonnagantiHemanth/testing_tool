#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.base.temperaturemeasurementutils
:brief: Helpers for ``TemperatureMeasurement`` feature
:author: Sanjib Hazra <shazra@logitech.com>
:date: 2021/06/07
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hidpp.features.common.temperaturemeasurement import TemperatureMeasurement
from pyhid.hidpp.features.common.temperaturemeasurement import TemperatureMeasurementFactory
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TemperatureMeasurementTestUtils(DeviceBaseTestUtils):
    """
    This class provides helpers for common checks on ``TemperatureMeasurement`` feature
    """
    class GetInfoResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check ``GetInfo`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetInfoResponse`` API

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "sensor_count": (cls.check_sensor_count,
                                 test_case.f.PRODUCT.FEATURES.COMMON.TEMPERATURE_MEASUREMENT.F_SensorCount)
            }
        # end def get_default_check_map

        @staticmethod
        def check_sensor_count(test_case, response, expected):
            """
            Check sensor_count field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetInfoResponse to check
            :type response: ``GetInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.sensor_count)),
                msg=f"The sensor_count parameter differs "
                    f"(expected:{expected}, obtained:{response.sensor_count})")
        # end def check_sensor_count
    # end class GetInfoResponseChecker

    class GetTemperatureResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check ``GetTemperature`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetTemperatureResponse`` API

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "sensor_id": (cls.check_sensor_id, None),
                "temperature": (cls.check_temperature, None)
            }
        # end def get_default_check_map

        @staticmethod
        def check_sensor_id(test_case, response, expected):
            """
            Check sensor_id field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetTemperatureResponse to check
            :type response: ``GetTemperatureResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.sensor_id)),
                msg=f"The sensor_id parameter differs "
                    f"(expected:{expected}, obtained:{response.sensor_id})")
        # end def check_sensor_id

        @staticmethod
        def check_temperature(test_case, response, expected):
            """
            Check temperature field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetTemperatureResponse to check
            :type response: ``GetTemperatureResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            if expected is None:
                # temperature response is converted from two's complement to signed integer with range from -128 to 127
                temp = int(Numeral(response.temperature))
                if temp > 127:
                    binary_number = int("{0:08b}".format(int(temp)))
                    str_convert = str(binary_number)
                    inverse_s = temp ^ (2 ** (len(str_convert) + 1) - 1)
                    result = bin(inverse_s)[3:]
                    two_complement = bin(int(result, 2) + int("1", 2))
                    output = int(two_complement, 2)
                    output = output * (-1)
                    temp = output
                # end if
                test_case.assertTrue(expr=(-128 <= temp <= 127),
                                     msg=f"The temperature:{temp} is not in range(-128, 127)")
            else:
                test_case.assertEqual(expected=int(Numeral(expected)), obtained=int(Numeral(response.temperature)),
                                      msg=f"The temperature parameter differs "
                                          f"(expected:{expected}, obtained:{response.temperature})")
            # end if
        # end def check_temperature
    # end class GetTemperatureResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``
        @classmethod
        def get_parameters(cls, test_case, feature_id=TemperatureMeasurement.FEATURE_ID,
                           factory=TemperatureMeasurementFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_info(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetInfo``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetInfoResponse
            :rtype: ``GetInfoResponse``
            """
            feature_1f30_index, feature_1f30, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1f30.get_info_cls(
                device_index, feature_1f30_index)
            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.common_message_queue,
                response_class_type=test_case.feature_1f30.get_info_response_cls)
            return response
        # end def get_info

        @classmethod
        def get_temperature(cls, test_case, sensor_id, device_index=None, port_index=None):
            """
            Process ``GetTemperature``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param sensor_id: Sensor Index
            :type sensor_id: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetTemperatureResponse
            :rtype: ``GetTemperatureResponse``
            """
            feature_1f30_index, feature_1f30, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1f30.get_temperature_cls(
                device_index, feature_1f30_index,
                sensor_id=HexList(sensor_id))
            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.common_message_queue,
                response_class_type=test_case.feature_1f30.get_temperature_response_cls)
            return response
        # end def get_temperature
    # end class HIDppHelper
# end class TemperatureMeasurementTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
