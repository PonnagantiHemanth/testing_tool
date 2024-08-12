#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.base.extendedadjustabledpiutils
:brief: Helpers for ``ExtendedAdjustableDpi`` feature
:author: Fred Chen <fchen7@logitech.com>
:date: 2022/06/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.mouse.extendedadjustabledpi import DpiCalibrationCompletedEvent
from pyhid.hidpp.features.mouse.extendedadjustabledpi import ExtendedAdjustableDpi
from pyhid.hidpp.features.mouse.extendedadjustabledpi import ExtendedAdjustableDpiFactory
from pyhid.hidpp.features.mouse.extendedadjustabledpi import GetDpiCalibrationInfoResponse
from pyhid.hidpp.features.mouse.extendedadjustabledpi import GetSensorCapabilitiesResponse
from pyhid.hidpp.features.mouse.extendedadjustabledpi import GetSensorCountResponse
from pyhid.hidpp.features.mouse.extendedadjustabledpi import GetSensorDpiListResponse
from pyhid.hidpp.features.mouse.extendedadjustabledpi import GetSensorDpiParametersResponse
from pyhid.hidpp.features.mouse.extendedadjustabledpi import GetSensorDpiRangesResponse
from pyhid.hidpp.features.mouse.extendedadjustabledpi import GetSensorLodListResponse
from pyhid.hidpp.features.mouse.extendedadjustabledpi import SensorDpiParametersEvent
from pyhid.hidpp.features.mouse.extendedadjustabledpi import SetDpiCalibrationResponse
from pyhid.hidpp.features.mouse.extendedadjustabledpi import SetSensorDpiParametersResponse
from pyhid.hidpp.features.mouse.extendedadjustabledpi import ShowSensorDpiStatusResponse
from pyhid.hidpp.features.mouse.extendedadjustabledpi import StartDpiCalibrationResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ExtendedAdjustableDpiTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``ExtendedAdjustableDpi`` feature
    """

    class GetSensorCountResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetSensorCountResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "num_sensor": (
                    cls.check_num_sensor,
                    test_case.f.PRODUCT.FEATURES.MOUSE.EXTENDED_ADJUSTABLE_DPI.F_NumSensor),
                "reserved": (cls.check_reserved, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_num_sensor(test_case, response, expected):
            """
            Check num_sensor field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorCountResponse to check
            :type response: ``GetSensorCountResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.num_sensor),
                msg="The num_sensor parameter differs "
                    f"(expected:{expected}, obtained:{response.num_sensor})")
        # end def check_num_sensor

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorCountResponse to check
            :type response: ``GetSensorCountResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved})")
        # end def check_reserved
    # end class GetSensorCountResponseChecker

    class GetSensorCapabilitiesResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetSensorCapabilitiesResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.MOUSE.EXTENDED_ADJUSTABLE_DPI
            return {
                "sensor_idx": (cls.check_sensor_idx, 0),
                "num_dpi_levels": (cls.check_num_dpi_levels, config.F_NumDpiLevels),
                "reserved_4bits": (cls.check_reserved_4bits, 0),
                "profile_supported": (cls.check_profile_supported, config.F_ProfileSupported),
                "calibration_supported": (cls.check_calibration_supported, config.F_CalibrationSupported),
                "lod_supported": (cls.check_lod_supported, config.F_LodSupported),
                "dpi_y_supported": (cls.check_dpi_y_supported, config.F_DpiYSupported),
                "reserved": (cls.check_reserved, 0),
            }
        # end def get_default_check_map

        @staticmethod
        def check_sensor_idx(test_case, response, expected):
            """
            Check sensor_idx field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorCapabilitiesResponse to check
            :type response: ``GetSensorCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.sensor_idx),
                msg="The sensor_idx parameter differs "
                    f"(expected:{expected}, obtained:{response.sensor_idx})")
        # end def check_sensor_idx

        @staticmethod
        def check_num_dpi_levels(test_case, response, expected):
            """
            Check num_dpi_levels field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorCapabilitiesResponse to check
            :type response: ``GetSensorCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.num_dpi_levels),
                msg="The num_dpi_levels parameter differs "
                    f"(expected:{expected}, obtained:{response.num_dpi_levels})")
        # end def check_num_dpi_levels

        @staticmethod
        def check_reserved_4bits(test_case, response, expected):
            """
            Check reserved_4bits field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorCapabilitiesResponse to check
            :type response: ``GetSensorCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved_4bits),
                msg="The reserved_4bits parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved_4bits})")
        # end def check_reserved_4bits

        @staticmethod
        def check_profile_supported(test_case, response, expected):
            """
            Check profile_supported field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorCapabilitiesResponse to check
            :type response: ``GetSensorCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.profile_supported),
                msg="The profile_supported parameter differs "
                    f"(expected:{expected}, obtained:{response.profile_supported})")
        # end def check_profile_supported

        @staticmethod
        def check_calibration_supported(test_case, response, expected):
            """
            Check calibration_supported field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorCapabilitiesResponse to check
            :type response: ``GetSensorCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.calibration_supported),
                msg="The calibration_supported parameter differs "
                    f"(expected:{expected}, obtained:{response.calibration_supported})")
        # end def check_calibration_supported

        @staticmethod
        def check_lod_supported(test_case, response, expected):
            """
            Check lod_supported field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorCapabilitiesResponse to check
            :type response: ``GetSensorCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.lod_supported),
                msg="The lod_supported parameter differs "
                    f"(expected:{expected}, obtained:{response.lod_supported})")
        # end def check_lod_supported

        @staticmethod
        def check_dpi_y_supported(test_case, response, expected):
            """
            Check dpi_y_supported field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorCapabilitiesResponse to check
            :type response: ``GetSensorCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.dpi_y_supported),
                msg="The dpi_y_supported parameter differs "
                    f"(expected:{expected}, obtained:{response.dpi_y_supported})")
        # end def check_dpi_y_supported

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorCapabilitiesResponse to check
            :type response: ``GetSensorCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved})")
        # end def check_reserved
    # end class GetSensorCapabilitiesResponseChecker

    class GetSensorDpiRangesResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetSensorDpiRangesResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return cls.get_default_check_map_by_req_idx(
                test_case=test_case, sensor_idx=0, direction=ExtendedAdjustableDpi.Direction.X, dpi_range_req_idx=0)
        # end def get_default_check_map

        @classmethod
        def get_default_check_map_by_req_idx(cls, test_case, sensor_idx, direction, dpi_range_req_idx):
            """
            Get the default check methods and expected values by requirement index

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param sensor_idx: The index of the sensor
            :type sensor_idx: ``int`` or ``HexList``
            :param direction: The direction of the DPI. 0:X, 1:Y
            :type direction: ``int`` or ``HexList``
            :param dpi_range_req_idx: The index of DPI range request. This index starts from 0 and needs to be
                                      incremented by "1" till end of list received.
            :type dpi_range_req_idx: ``int``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.MOUSE.EXTENDED_ADJUSTABLE_DPI
            dpi_ranges = config.F_DpiRangesX if direction == ExtendedAdjustableDpi.Direction.X else config.F_DpiRangesY
            dpi_ranges_length = len(config.F_DpiRangesX)

            # Compute start index in DpiRanges
            start_idx = 0
            for base in range(1, dpi_range_req_idx + 1):
                start_idx += 6
                if base % 2 == 0:
                    start_idx += 1
                # end if
            # end for

            # Convert DPI Range settings to the payload of GetSensorDpiRanges
            dpi_ranges_payload = []
            if start_idx > dpi_ranges_length:
                dpi_ranges_payload = [0] * 7
            else:
                max_data_count = 7
                if dpi_ranges_length < (start_idx + max_data_count):
                    max_data_count = dpi_ranges_length - start_idx
                # end if

                if dpi_range_req_idx % 2 == 0:
                    for idx in range(max_data_count):
                        if idx < 6:
                            dpi_range = int(dpi_ranges[start_idx + idx], 16)
                        else:
                            dpi_range = (int(dpi_ranges[start_idx + idx], 16) & 0xFF00) >> 8
                        # end if
                        dpi_ranges_payload.append(dpi_range)
                    # end for
                else:
                    for idx in range(max_data_count):
                        if idx < 6:
                            dpi_range = (int(dpi_ranges[start_idx + idx], 16) & 0xFF) << 8
                            dpi_range += (int(dpi_ranges[start_idx + idx + 1], 16) & 0xFF00) >> 8
                        else:
                            dpi_range = (int(dpi_ranges[start_idx + idx], 16) & 0xFF)
                        # end if
                        dpi_ranges_payload.append(dpi_range)
                    # end for
                # end if

                if max_data_count < 7:
                    for _ in range(7 - max_data_count):
                        dpi_ranges_payload.append(0)
                    # end for
                # end if
            # end if

            return {
                "sensor_idx": (cls.check_sensor_idx, sensor_idx),
                "direction": (cls.check_direction, direction),
                "dpi_range_req_idx": (cls.check_dpi_range_req_idx, dpi_range_req_idx),
                "dpi_ranges_1": (cls.check_dpi_ranges_1, dpi_ranges_payload[0]),
                "dpi_ranges_2": (cls.check_dpi_ranges_2, dpi_ranges_payload[1]),
                "dpi_ranges_3": (cls.check_dpi_ranges_3, dpi_ranges_payload[2]),
                "dpi_ranges_4": (cls.check_dpi_ranges_4, dpi_ranges_payload[3]),
                "dpi_ranges_5": (cls.check_dpi_ranges_5, dpi_ranges_payload[4]),
                "dpi_ranges_6": (cls.check_dpi_ranges_6, dpi_ranges_payload[5]),
                "dpi_ranges_7_msb": (cls.check_dpi_ranges_7_msb, dpi_ranges_payload[6]),
            }
        # end def get_default_check_map_by_req_idx

        @staticmethod
        def check_sensor_idx(test_case, response, expected):
            """
            Check sensor_idx field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorDpiRangesResponse to check
            :type response: ``GetSensorDpiRangesResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.sensor_idx),
                msg="The sensor_idx parameter differs "
                    f"(expected:{expected}, obtained:{response.sensor_idx})")
        # end def check_sensor_idx

        @staticmethod
        def check_direction(test_case, response, expected):
            """
            Check direction field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorDpiRangesResponse to check
            :type response: ``GetSensorDpiRangesResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.direction),
                msg="The direction parameter differs "
                    f"(expected:{expected}, obtained:{response.direction})")
        # end def check_direction

        @staticmethod
        def check_dpi_range_req_idx(test_case, response, expected):
            """
            Check dpi_range_req_idx field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorDpiRangesResponse to check
            :type response: ``GetSensorDpiRangesResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.dpi_range_req_idx),
                msg="The dpi_range_req_idx parameter differs "
                    f"(expected:{expected}, obtained:{response.dpi_range_req_idx})")
        # end def check_dpi_range_req_idx

        @staticmethod
        def check_dpi_ranges_1(test_case, response, expected):
            """
            Check dpi_ranges_1 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorDpiRangesResponse to check
            :type response: ``GetSensorDpiRangesResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.dpi_ranges_1),
                msg="The dpi_ranges_1 parameter differs "
                    f"(expected:{expected}, obtained:{response.dpi_ranges_1})")
        # end def check_dpi_ranges_1

        @staticmethod
        def check_dpi_ranges_2(test_case, response, expected):
            """
            Check dpi_ranges_2 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorDpiRangesResponse to check
            :type response: ``GetSensorDpiRangesResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.dpi_ranges_2),
                msg="The dpi_ranges_2 parameter differs "
                    f"(expected:{expected}, obtained:{response.dpi_ranges_2})")
        # end def check_dpi_ranges_2

        @staticmethod
        def check_dpi_ranges_3(test_case, response, expected):
            """
            Check dpi_ranges_3 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorDpiRangesResponse to check
            :type response: ``GetSensorDpiRangesResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.dpi_ranges_3),
                msg="The dpi_ranges_3 parameter differs "
                    f"(expected:{expected}, obtained:{response.dpi_ranges_3})")
        # end def check_dpi_ranges_3

        @staticmethod
        def check_dpi_ranges_4(test_case, response, expected):
            """
            Check dpi_ranges_4 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorDpiRangesResponse to check
            :type response: ``GetSensorDpiRangesResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.dpi_ranges_4),
                msg="The dpi_ranges_4 parameter differs "
                    f"(expected:{expected}, obtained:{response.dpi_ranges_4})")
        # end def check_dpi_ranges_4

        @staticmethod
        def check_dpi_ranges_5(test_case, response, expected):
            """
            Check dpi_ranges_5 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorDpiRangesResponse to check
            :type response: ``GetSensorDpiRangesResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.dpi_ranges_5),
                msg="The dpi_ranges_5 parameter differs "
                    f"(expected:{expected}, obtained:{response.dpi_ranges_5})")
        # end def check_dpi_ranges_5

        @staticmethod
        def check_dpi_ranges_6(test_case, response, expected):
            """
            Check dpi_ranges_6 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorDpiRangesResponse to check
            :type response: ``GetSensorDpiRangesResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.dpi_ranges_6),
                msg="The dpi_ranges_6 parameter differs "
                    f"(expected:{expected}, obtained:{response.dpi_ranges_6})")
        # end def check_dpi_ranges_6

        @staticmethod
        def check_dpi_ranges_7_msb(test_case, response, expected):
            """
            Check dpi_ranges_7_msb field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorDpiRangesResponse to check
            :type response: ``GetSensorDpiRangesResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.dpi_ranges_7_msb),
                msg="The dpi_ranges_7_msb parameter differs "
                    f"(expected:{expected}, obtained:{response.dpi_ranges_7_msb})")
        # end def check_dpi_ranges_7_msb
    # end class GetSensorDpiRangesResponseChecker

    class GetSensorDpiListResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetSensorDpiListResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.MOUSE.EXTENDED_ADJUSTABLE_DPI
            return {
                "sensor_idx": (cls.check_sensor_idx, 0),
                "direction": (cls.check_direction, ExtendedAdjustableDpi.Direction.X),
                "dpi_list_1": (cls.check_dpi_list_1, int(config.F_DpiListX[0])),
                "dpi_list_2": (cls.check_dpi_list_2, int(config.F_DpiListX[1])),
                "dpi_list_3": (cls.check_dpi_list_3, int(config.F_DpiListX[2])),
                "dpi_list_4": (cls.check_dpi_list_4, int(config.F_DpiListX[3])),
                "dpi_list_5": (cls.check_dpi_list_5, int(config.F_DpiListX[4])),
                "dpi_list_6": (cls.check_dpi_list_6, int(config.F_DpiListX[5])),
                "reserved": (cls.check_reserved, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_sensor_idx(test_case, response, expected):
            """
            Check sensor_idx field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorDpiListResponse to check
            :type response: ``GetSensorDpiListResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.sensor_idx),
                msg="The sensor_idx parameter differs "
                    f"(expected:{expected}, obtained:{response.sensor_idx})")
        # end def check_sensor_idx

        @staticmethod
        def check_direction(test_case, response, expected):
            """
            Check direction field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorDpiListResponse to check
            :type response: ``GetSensorDpiListResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.direction),
                msg="The direction parameter differs "
                    f"(expected:{expected}, obtained:{response.direction})")
        # end def check_direction

        @staticmethod
        def check_dpi_list_1(test_case, response, expected):
            """
            Check dpi_list_1 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorDpiListResponse to check
            :type response: ``GetSensorDpiListResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.dpi_list_1),
                msg="The dpi_list_1 parameter differs "
                    f"(expected:{expected}, obtained:{response.dpi_list_1})")
        # end def check_dpi_list_1

        @staticmethod
        def check_dpi_list_2(test_case, response, expected):
            """
            Check dpi_list_2 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorDpiListResponse to check
            :type response: ``GetSensorDpiListResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.dpi_list_2),
                msg="The dpi_list_2 parameter differs "
                    f"(expected:{expected}, obtained:{response.dpi_list_2})")
        # end def check_dpi_list_2

        @staticmethod
        def check_dpi_list_3(test_case, response, expected):
            """
            Check dpi_list_3 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorDpiListResponse to check
            :type response: ``GetSensorDpiListResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.dpi_list_3),
                msg="The dpi_list_3 parameter differs "
                    f"(expected:{expected}, obtained:{response.dpi_list_3})")
        # end def check_dpi_list_3

        @staticmethod
        def check_dpi_list_4(test_case, response, expected):
            """
            Check dpi_list_4 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorDpiListResponse to check
            :type response: ``GetSensorDpiListResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.dpi_list_4),
                msg="The dpi_list_4 parameter differs "
                    f"(expected:{expected}, obtained:{response.dpi_list_4})")
        # end def check_dpi_list_4

        @staticmethod
        def check_dpi_list_5(test_case, response, expected):
            """
            Check dpi_list_5 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorDpiListResponse to check
            :type response: ``GetSensorDpiListResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.dpi_list_5),
                msg="The dpi_list_5 parameter differs "
                    f"(expected:{expected}, obtained:{response.dpi_list_5})")
        # end def check_dpi_list_5

        @staticmethod
        def check_dpi_list_6(test_case, response, expected):
            """
            Check dpi_list_6 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorDpiListResponse to check
            :type response: ``GetSensorDpiListResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.dpi_list_6),
                msg="The dpi_list_6 parameter differs "
                    f"(expected:{expected}, obtained:{response.dpi_list_6})")
        # end def check_dpi_list_6

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorDpiListResponse to check
            :type response: ``GetSensorDpiListResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved})")
        # end def check_reserved
    # end class GetSensorDpiListResponseChecker

    class GetSensorLodListResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetSensorLodListResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.MOUSE.EXTENDED_ADJUSTABLE_DPI
            return {
                "sensor_idx": (cls.check_sensor_idx, 0),
                "lod_1": (cls.check_lod_1, int(config.F_DpiLodList[0], 16)),
                "lod_2": (cls.check_lod_2, int(config.F_DpiLodList[1], 16)),
                "lod_3": (cls.check_lod_3, int(config.F_DpiLodList[2], 16)),
                "lod_4": (cls.check_lod_4, int(config.F_DpiLodList[3], 16)),
                "lod_5": (cls.check_lod_5, int(config.F_DpiLodList[4], 16)),
                "reserved": (cls.check_reserved, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_sensor_idx(test_case, response, expected):
            """
            Check sensor_idx field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorLodListResponse to check
            :type response: ``GetSensorLodListResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.sensor_idx),
                msg="The sensor_idx parameter differs "
                    f"(expected:{expected}, obtained:{response.sensor_idx})")
        # end def check_sensor_idx

        @staticmethod
        def check_lod_1(test_case, response, expected):
            """
            Check lod_1 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorLodListResponse to check
            :type response: ``GetSensorLodListResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.lod_1),
                msg="The lod_1 parameter differs "
                    f"(expected:{expected}, obtained:{response.lod_1})")
        # end def check_lod_1

        @staticmethod
        def check_lod_2(test_case, response, expected):
            """
            Check lod_2 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorLodListResponse to check
            :type response: ``GetSensorLodListResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.lod_2),
                msg="The lod_2 parameter differs "
                    f"(expected:{expected}, obtained:{response.lod_2})")
        # end def check_lod_2

        @staticmethod
        def check_lod_3(test_case, response, expected):
            """
            Check lod_3 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorLodListResponse to check
            :type response: ``GetSensorLodListResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.lod_3),
                msg="The lod_3 parameter differs "
                    f"(expected:{expected}, obtained:{response.lod_3})")
        # end def check_lod_3

        @staticmethod
        def check_lod_4(test_case, response, expected):
            """
            Check lod_4 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorLodListResponse to check
            :type response: ``GetSensorLodListResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.lod_4),
                msg="The lod_4 parameter differs "
                    f"(expected:{expected}, obtained:{response.lod_4})")
        # end def check_lod_4

        @staticmethod
        def check_lod_5(test_case, response, expected):
            """
            Check lod_5 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorLodListResponse to check
            :type response: ``GetSensorLodListResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.lod_5),
                msg="The lod_5 parameter differs "
                    f"(expected:{expected}, obtained:{response.lod_5})")
        # end def check_lod_5

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorLodListResponse to check
            :type response: ``GetSensorLodListResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved})")
        # end def check_reserved
    # end class GetSensorLodListResponseChecker

    class GetSensorDpiParametersResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetSensorDpiParametersResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.MOUSE.EXTENDED_ADJUSTABLE_DPI
            return {
                "sensor_idx": (cls.check_sensor_idx, 0),
                "dpi_x": (cls.check_dpi_x, config.F_DefaultDpiX),
                "default_dpi_x": (cls.check_default_dpi_x, config.F_DefaultDpiX),
                "dpi_y": (cls.check_dpi_y, config.F_DefaultDpiY),
                "default_dpi_y": (cls.check_default_dpi_y, config.F_DefaultDpiY),
                "lod": (cls.check_lod, config.F_DefaultLod),
                "reserved": (cls.check_reserved, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_sensor_idx(test_case, response, expected):
            """
            Check sensor_idx field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorDpiParametersResponse to check
            :type response: ``GetSensorDpiParametersResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.sensor_idx),
                msg="The sensor_idx parameter differs "
                    f"(expected:{expected}, obtained:{response.sensor_idx})")
        # end def check_sensor_idx

        @staticmethod
        def check_dpi_x(test_case, response, expected):
            """
            Check dpi_x field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorDpiParametersResponse to check
            :type response: ``GetSensorDpiParametersResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.dpi_x),
                msg="The dpi_x parameter differs "
                    f"(expected:{expected}, obtained:{response.dpi_x})")
        # end def check_dpi_x

        @staticmethod
        def check_default_dpi_x(test_case, response, expected):
            """
            Check default_dpi_x field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorDpiParametersResponse to check
            :type response: ``GetSensorDpiParametersResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.default_dpi_x),
                msg="The default_dpi_x parameter differs "
                    f"(expected:{expected}, obtained:{response.default_dpi_x})")
        # end def check_default_dpi_x

        @staticmethod
        def check_dpi_y(test_case, response, expected):
            """
            Check dpi_y field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorDpiParametersResponse to check
            :type response: ``GetSensorDpiParametersResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.dpi_y),
                msg="The dpi_y parameter differs "
                    f"(expected:{expected}, obtained:{response.dpi_y})")
        # end def check_dpi_y

        @staticmethod
        def check_default_dpi_y(test_case, response, expected):
            """
            Check default_dpi_y field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorDpiParametersResponse to check
            :type response: ``GetSensorDpiParametersResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.default_dpi_y),
                msg="The default_dpi_y parameter differs "
                    f"(expected:{expected}, obtained:{response.default_dpi_y})")
        # end def check_default_dpi_y

        @staticmethod
        def check_lod(test_case, response, expected):
            """
            Check lod field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorDpiParametersResponse to check
            :type response: ``GetSensorDpiParametersResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.lod),
                msg="The lod parameter differs "
                    f"(expected:{expected}, obtained:{response.lod})")
        # end def check_lod

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSensorDpiParametersResponse to check
            :type response: ``GetSensorDpiParametersResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved})")
        # end def check_reserved
    # end class GetSensorDpiParametersResponseChecker

    class SetSensorDpiParametersResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``SetSensorDpiParametersResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.MOUSE.EXTENDED_ADJUSTABLE_DPI
            return {
                "sensor_idx": (cls.check_sensor_idx, 0),
                "dpi_x": (cls.check_dpi_x, config.F_DefaultDpiX),
                "dpi_y": (cls.check_dpi_y, config.F_DefaultDpiY),
                "lod": (cls.check_lod, config.F_DefaultLod),
                "reserved": (cls.check_reserved, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_sensor_idx(test_case, response, expected):
            """
            Check sensor_idx field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SetSensorDpiParametersResponse to check
            :type response: ``SetSensorDpiParametersResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.sensor_idx),
                msg="The sensor_idx parameter differs "
                    f"(expected:{expected}, obtained:{response.sensor_idx})")
        # end def check_sensor_idx

        @staticmethod
        def check_dpi_x(test_case, response, expected):
            """
            Check dpi_x field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SetSensorDpiParametersResponse to check
            :type response: ``SetSensorDpiParametersResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.dpi_x),
                msg="The dpi_x parameter differs "
                    f"(expected:{expected}, obtained:{response.dpi_x})")
        # end def check_dpi_x

        @staticmethod
        def check_dpi_y(test_case, response, expected):
            """
            Check dpi_y field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SetSensorDpiParametersResponse to check
            :type response: ``SetSensorDpiParametersResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.dpi_y),
                msg="The dpi_y parameter differs "
                    f"(expected:{expected}, obtained:{response.dpi_y})")
        # end def check_dpi_y

        @staticmethod
        def check_lod(test_case, response, expected):
            """
            Check lod field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SetSensorDpiParametersResponse to check
            :type response: ``SetSensorDpiParametersResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.lod),
                msg="The lod parameter differs "
                    f"(expected:{expected}, obtained:{response.lod})")
        # end def check_lod

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SetSensorDpiParametersResponse to check
            :type response: ``SetSensorDpiParametersResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved})")
        # end def check_reserved
    # end class SetSensorDpiParametersResponseChecker

    class ShowSensorDpiStatusResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``ShowSensorDpiStatusResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            get_feature = test_case.config_manager.get_feature
            return {
                "sensor_idx": (cls.check_sensor_idx, 0),
                "dpi_level": (cls.check_dpi_level,
                              get_feature(ConfigurationManager.ID.OOB_PROFILES_DEFAULT_DPI_INDEX)[0] + 1),
                "led_hold_type": (cls.check_led_hold_type, ExtendedAdjustableDpi.LedHoldType.TIMER_BASED),
                "button_num": (cls.check_button_num, 0),
                "reserved": (cls.check_reserved, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_sensor_idx(test_case, response, expected):
            """
            Check sensor_idx field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ShowSensorDpiStatusResponse to check
            :type response: ``ShowSensorDpiStatusResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.sensor_idx),
                msg="The sensor_idx parameter differs "
                    f"(expected:{expected}, obtained:{response.sensor_idx})")
        # end def check_sensor_idx

        @staticmethod
        def check_dpi_level(test_case, response, expected):
            """
            Check dpi_level field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ShowSensorDpiStatusResponse to check
            :type response: ``ShowSensorDpiStatusResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.dpi_level),
                msg="The dpi_level parameter differs "
                    f"(expected:{expected}, obtained:{response.dpi_level})")
        # end def check_dpi_level

        @staticmethod
        def check_led_hold_type(test_case, response, expected):
            """
            Check led_hold_type field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ShowSensorDpiStatusResponse to check
            :type response: ``ShowSensorDpiStatusResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.led_hold_type),
                msg="The led_hold_type parameter differs "
                    f"(expected:{expected}, obtained:{response.led_hold_type})")
        # end def check_led_hold_type

        @staticmethod
        def check_button_num(test_case, response, expected):
            """
            Check button_num field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ShowSensorDpiStatusResponse to check
            :type response: ``ShowSensorDpiStatusResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.button_num),
                msg="The button_num parameter differs "
                    f"(expected:{expected}, obtained:{response.button_num})")
        # end def check_button_num

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ShowSensorDpiStatusResponse to check
            :type response: ``ShowSensorDpiStatusResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved})")
        # end def check_reserved
    # end class ShowSensorDpiStatusResponseChecker

    class GetDpiCalibrationInfoResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetDpiCalibrationInfoResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.MOUSE.EXTENDED_ADJUSTABLE_DPI
            return {
                "sensor_idx": (cls.check_sensor_idx, 0),
                "mouse_width": (cls.check_mouse_width, config.F_MouseWidth),
                "mouse_length": (cls.check_mouse_length, config.F_MouseLength),
                "calib_dpi_x": (cls.check_calib_dpi_x, config.F_CalibDpiX),
                "calib_dpi_y": (cls.check_calib_dpi_y, config.F_CalibDpiY),
                "reserved": (cls.check_reserved, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_sensor_idx(test_case, response, expected):
            """
            Check sensor_idx field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetDpiCalibrationInfoResponse to check
            :type response: ``GetDpiCalibrationInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.sensor_idx),
                msg="The sensor_idx parameter differs "
                    f"(expected:{expected}, obtained:{response.sensor_idx})")
        # end def check_sensor_idx

        @staticmethod
        def check_mouse_width(test_case, response, expected):
            """
            Check mouse_width field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetDpiCalibrationInfoResponse to check
            :type response: ``GetDpiCalibrationInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.mouse_width),
                msg="The mouse_width parameter differs "
                    f"(expected:{expected}, obtained:{response.mouse_width})")
        # end def check_mouse_width

        @staticmethod
        def check_mouse_length(test_case, response, expected):
            """
            Check mouse_length field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetDpiCalibrationInfoResponse to check
            :type response: ``GetDpiCalibrationInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.mouse_length),
                msg="The mouse_length parameter differs "
                    f"(expected:{expected}, obtained:{response.mouse_length})")
        # end def check_mouse_length

        @staticmethod
        def check_calib_dpi_x(test_case, response, expected):
            """
            Check calib_dpi_x field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetDpiCalibrationInfoResponse to check
            :type response: ``GetDpiCalibrationInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.calib_dpi_x),
                msg="The calib_dpi_x parameter differs "
                    f"(expected:{expected}, obtained:{response.calib_dpi_x})")
        # end def check_calib_dpi_x

        @staticmethod
        def check_calib_dpi_y(test_case, response, expected):
            """
            Check calib_dpi_y field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetDpiCalibrationInfoResponse to check
            :type response: ``GetDpiCalibrationInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.calib_dpi_y),
                msg="The calib_dpi_y parameter differs "
                    f"(expected:{expected}, obtained:{response.calib_dpi_y})")
        # end def check_calib_dpi_y

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetDpiCalibrationInfoResponse to check
            :type response: ``GetDpiCalibrationInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved})")
        # end def check_reserved
    # end class GetDpiCalibrationInfoResponseChecker

    class StartDpiCalibrationResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``StartDpiCalibrationResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "sensor_idx": (cls.check_sensor_idx, 0),
                "direction": (cls.check_direction, ExtendedAdjustableDpi.Direction.X),
                "expected_count": (cls.check_expected_count, None),
                "calib_type": (cls.check_calib_type, ExtendedAdjustableDpi.CalibType.HW),
                "calib_start_timeout": (cls.check_calib_start_timeout, 0),
                "calib_hw_process_timeout": (cls.check_calib_hw_process_timeout, 0),
                "calib_sw_process_timeout": (cls.check_calib_sw_process_timeout, 0),
                "reserved": (cls.check_reserved, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_sensor_idx(test_case, response, expected):
            """
            Check sensor_idx field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: StartDpiCalibrationResponse to check
            :type response: ``StartDpiCalibrationResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.sensor_idx),
                msg="The sensor_idx parameter differs "
                    f"(expected:{expected}, obtained:{response.sensor_idx})")
        # end def check_sensor_idx

        @staticmethod
        def check_direction(test_case, response, expected):
            """
            Check direction field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: StartDpiCalibrationResponse to check
            :type response: ``StartDpiCalibrationResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.direction),
                msg="The direction parameter differs "
                    f"(expected:{expected}, obtained:{response.direction})")
        # end def check_direction

        @staticmethod
        def check_expected_count(test_case, response, expected):
            """
            Check expected_count field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: StartDpiCalibrationResponse to check
            :type response: ``StartDpiCalibrationResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.expected_count),
                msg="The expected_count parameter differs "
                    f"(expected:{expected}, obtained:{response.expected_count})")
        # end def check_expected_count

        @staticmethod
        def check_calib_type(test_case, response, expected):
            """
            Check calib_type field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: StartDpiCalibrationResponse to check
            :type response: ``StartDpiCalibrationResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.calib_type),
                msg="The calib_type parameter differs "
                    f"(expected:{expected}, obtained:{response.calib_type})")
        # end def check_calib_type

        @staticmethod
        def check_calib_start_timeout(test_case, response, expected):
            """
            Check calib_start_timeout field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: StartDpiCalibrationResponse to check
            :type response: ``StartDpiCalibrationResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.calib_start_timeout),
                msg="The calib_start_timeout parameter differs "
                    f"(expected:{expected}, obtained:{response.calib_start_timeout})")
        # end def check_calib_start_timeout

        @staticmethod
        def check_calib_hw_process_timeout(test_case, response, expected):
            """
            Check calib_hw_process_timeout field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: StartDpiCalibrationResponse to check
            :type response: ``StartDpiCalibrationResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.calib_hw_process_timeout),
                msg="The calib_hw_process_timeout parameter differs "
                    f"(expected:{expected}, obtained:{response.calib_hw_process_timeout})")
        # end def check_calib_hw_process_timeout

        @staticmethod
        def check_calib_sw_process_timeout(test_case, response, expected):
            """
            Check calib_sw_process_timeout field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: StartDpiCalibrationResponse to check
            :type response: ``StartDpiCalibrationResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.calib_sw_process_timeout),
                msg="The calib_sw_process_timeout parameter differs "
                    f"(expected:{expected}, obtained:{response.calib_sw_process_timeout})")
        # end def check_calib_sw_process_timeout

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: StartDpiCalibrationResponse to check
            :type response: ``StartDpiCalibrationResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved})")
        # end def check_reserved
    # end class StartDpiCalibrationResponseChecker

    class SetDpiCalibrationResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``SetDpiCalibrationResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "sensor_idx": (cls.check_sensor_idx, 0),
                "direction": (cls.check_direction, ExtendedAdjustableDpi.Direction.X),
                "calib_cor": (cls.check_calib_cor, 0),
                "reserved": (cls.check_reserved, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_sensor_idx(test_case, response, expected):
            """
            Check sensor_idx field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SetDpiCalibrationResponse to check
            :type response: ``SetDpiCalibrationResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.sensor_idx),
                msg="The sensor_idx parameter differs "
                    f"(expected:{expected}, obtained:{response.sensor_idx})")
        # end def check_sensor_idx

        @staticmethod
        def check_direction(test_case, response, expected):
            """
            Check direction field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SetDpiCalibrationResponse to check
            :type response: ``SetDpiCalibrationResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.direction),
                msg="The direction parameter differs "
                    f"(expected:{expected}, obtained:{response.direction})")
        # end def check_direction

        @staticmethod
        def check_calib_cor(test_case, response, expected):
            """
            Check calib_cor field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SetDpiCalibrationResponse to check
            :type response: ``SetDpiCalibrationResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.calib_cor),
                msg="The calib_cor parameter differs "
                    f"(expected:{expected}, obtained:{response.calib_cor})")
        # end def check_calib_cor

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SetDpiCalibrationResponse to check
            :type response: ``SetDpiCalibrationResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved})")
        # end def check_reserved
    # end class SetDpiCalibrationResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=ExtendedAdjustableDpi.FEATURE_ID,
                           factory=ExtendedAdjustableDpiFactory, device_index=None, port_index=None,
                           update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_sensor_count(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetSensorCount``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int`` or ``None``

            :return: GetSensorCountResponse
            :rtype: ``GetSensorCountResponse``
            """
            feature_2202_index, feature_2202, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2202.get_sensor_count_cls(
                device_index=device_index,
                feature_index=feature_2202_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=feature_2202.get_sensor_count_response_cls)
            return response
        # end def get_sensor_count

        @classmethod
        def get_sensor_capabilities(cls, test_case, sensor_idx, device_index=None, port_index=None):
            """
            Process ``GetSensorCapabilities``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param sensor_idx: The index of the sensor
            :type sensor_idx: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int`` or ``None``

            :return: GetSensorCapabilitiesResponse
            :rtype: ``GetSensorCapabilitiesResponse``
            """
            feature_2202_index, feature_2202, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2202.get_sensor_capabilities_cls(
                device_index=device_index,
                feature_index=feature_2202_index,
                sensor_idx=sensor_idx)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=feature_2202.get_sensor_capabilities_response_cls)
            return response
        # end def get_sensor_capabilities

        @classmethod
        def get_sensor_dpi_ranges(
                cls, test_case, sensor_idx, direction, dpi_range_req_idx, device_index=None, port_index=None):
            """
            Process ``GetSensorDpiRanges``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param sensor_idx: The index of the sensor
            :type sensor_idx: ``int`` or ``HexList``
            :param direction: The direction of the DPI. 0:X, 1:Y
            :type direction: ``int`` or ``HexList``
            :param dpi_range_req_idx: The index of DPI range request. This index starts from 0 and needs to be
                                      incremented by "1" till end of list received.
            :type dpi_range_req_idx: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int`` or ``None``

            :return: GetSensorDpiRangesResponse
            :rtype: ``GetSensorDpiRangesResponse``
            """
            feature_2202_index, feature_2202, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2202.get_sensor_dpi_ranges_cls(
                device_index=device_index,
                feature_index=feature_2202_index,
                sensor_idx=sensor_idx,
                direction=direction,
                dpi_range_req_idx=dpi_range_req_idx)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=feature_2202.get_sensor_dpi_ranges_response_cls)
            return response
        # end def get_sensor_dpi_ranges

        @classmethod
        def get_sensor_dpi_list(cls, test_case, sensor_idx, direction, device_index=None, port_index=None):
            """
            Process ``GetSensorDpiList``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param sensor_idx: The index of the sensor
            :type sensor_idx: ``int`` or ``HexList``
            :param direction: The direction of the DPI. 0:X, 1:Y
            :type direction: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int`` or ``None``

            :return: GetSensorDpiListResponse
            :rtype: ``GetSensorDpiListResponse``
            """
            feature_2202_index, feature_2202, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2202.get_sensor_dpi_list_cls(
                device_index=device_index,
                feature_index=feature_2202_index,
                sensor_idx=sensor_idx,
                direction=direction)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=feature_2202.get_sensor_dpi_list_response_cls)
            return response
        # end def get_sensor_dpi_list

        @classmethod
        def get_sensor_lod_list(cls, test_case, sensor_idx, device_index=None, port_index=None):
            """
            Process ``GetSensorLodList``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param sensor_idx: The index of the sensor
            :type sensor_idx: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int`` or ``None``

            :return: GetSensorLodListResponse
            :rtype: ``GetSensorLodListResponse``
            """
            feature_2202_index, feature_2202, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2202.get_sensor_lod_list_cls(
                device_index=device_index,
                feature_index=feature_2202_index,
                sensor_idx=sensor_idx)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=feature_2202.get_sensor_lod_list_response_cls)
            return response
        # end def get_sensor_lod_list

        @classmethod
        def get_sensor_dpi_parameters(cls, test_case, sensor_idx, device_index=None, port_index=None):
            """
            Process ``GetSensorDpiParameters``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param sensor_idx: The index of the sensor
            :type sensor_idx: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int`` or ``None``

            :return: GetSensorDpiParametersResponse
            :rtype: ``GetSensorDpiParametersResponse``
            """
            feature_2202_index, feature_2202, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2202.get_sensor_dpi_parameters_cls(
                device_index=device_index,
                feature_index=feature_2202_index,
                sensor_idx=sensor_idx)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=feature_2202.get_sensor_dpi_parameters_response_cls)
            return response
        # end def get_sensor_dpi_parameters

        @classmethod
        def set_sensor_dpi_parameters(cls, test_case, sensor_idx, dpi_x, dpi_y, lod, device_index=None,
                                      port_index=None):
            """
            Process ``SetSensorDpiParameters``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param sensor_idx: The index of the sensor
            :type sensor_idx: ``int`` or ``HexList``
            :param dpi_x: The new DPI X direction numeric value (1 - 57343) for the current slot
            :type dpi_x: ``int`` or ``HexList``
            :param dpi_y: The new DPI Y direction numeric value (1 - 57343) for the current slot
            :type dpi_y: ``int`` or ``HexList``
            :param lod: The new LOD for the current slot
            :type lod: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int`` or ``None``

            :return: SetSensorDpiParametersResponse
            :rtype: ``SetSensorDpiParametersResponse``
            """
            feature_2202_index, feature_2202, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2202.set_sensor_dpi_parameters_cls(
                device_index=device_index,
                feature_index=feature_2202_index,
                sensor_idx=sensor_idx,
                dpi_x=dpi_x,
                dpi_y=dpi_y,
                lod=lod)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=feature_2202.set_sensor_dpi_parameters_response_cls)
            return response
        # end def set_sensor_dpi_parameters

        @classmethod
        def show_sensor_dpi_status(cls, test_case, sensor_idx, dpi_level, led_hold_type, button_num,
                                   device_index=None, port_index=None):
            """
            Process ``ShowSensorDpiStatus``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param sensor_idx: The index of the sensor
            :type sensor_idx: ``int`` or ``HexList``
            :param dpi_level: The dpi level to be shown [1..N]. The N is determined by NumDpiLevels
                              from getSensorCapabilities
            :type dpi_level: ``int`` or ``HexList``
            :param led_hold_type: This parameter indicates the LED hold type.
            :type led_hold_type: ``int`` or ``HexList``
            :param button_num: The HID button number which initiates the DPI level change
            :type button_num: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int`` or ``None``

            :return: ShowSensorDpiStatusResponse
            :rtype: ``ShowSensorDpiStatusResponse``
            """
            feature_2202_index, feature_2202, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2202.show_sensor_dpi_status_cls(
                device_index=device_index,
                feature_index=feature_2202_index,
                sensor_idx=sensor_idx,
                dpi_level=dpi_level,
                led_hold_type=led_hold_type,
                button_num=button_num)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=feature_2202.show_sensor_dpi_status_response_cls)
            return response
        # end def show_sensor_dpi_status

        @classmethod
        def get_dpi_calibration_info(cls, test_case, sensor_idx, device_index=None, port_index=None):
            """
            Process ``GetDpiCalibrationInfo``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param sensor_idx: The index of the sensor
            :type sensor_idx: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int`` or ``None``

            :return: GetDpiCalibrationInfoResponse
            :rtype: ``GetDpiCalibrationInfoResponse``
            """
            feature_2202_index, feature_2202, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2202.get_dpi_calibration_info_cls(
                device_index=device_index,
                feature_index=feature_2202_index,
                sensor_idx=HexList(sensor_idx))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=feature_2202.get_dpi_calibration_info_response_cls)
            return response
        # end def get_dpi_calibration_info

        @classmethod
        def start_dpi_calibration(cls, test_case, sensor_idx, direction, expected_count, calib_type,
                                  calib_start_timeout, calib_hw_process_timeout, calib_sw_process_timeout,
                                  device_index=None, port_index=None):
            """
            Process ``StartDpiCalibration``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param sensor_idx: The index of the sensor
            :type sensor_idx: ``int`` or ``HexList``
            :param direction: The direction of the DPI. 0:X, 1:Y
            :type direction: ``int`` or ``HexList``
            :param expected_count: The expected pixel counts for mouse movement
            :type expected_count: ``int`` or ``HexList``
            :param calib_type: 0: HW, 1: SW
            :type calib_type: ``int`` or ``HexList``
            :param calib_start_timeout: Timeout (unit: second) used for HW calibration process.
                                        This timeout is limited to 60 sec.
            :type calib_start_timeout: ``int`` or ``HexList``
            :param calib_hw_process_timeout: Timeout (unit: second) used for HW calibration process.
                                             This timeout is limited to 60 sec.
            :type calib_hw_process_timeout: ``int`` or ``HexList``
            :param calib_sw_process_timeout: Timeout (unit: second) used for SW calibration process.
                                             This timeout is limited to 60 sec.
            :type calib_sw_process_timeout: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int`` or ``None``

            :return: StartDpiCalibrationResponse
            :rtype: ``StartDpiCalibrationResponse``
            """
            feature_2202_index, feature_2202, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2202.start_dpi_calibration_cls(
                device_index=device_index,
                feature_index=feature_2202_index,
                sensor_idx=sensor_idx,
                direction=direction,
                expected_count=expected_count,
                calib_type=calib_type,
                calib_start_timeout=calib_start_timeout,
                calib_hw_process_timeout=calib_hw_process_timeout,
                calib_sw_process_timeout=calib_sw_process_timeout)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=feature_2202.start_dpi_calibration_response_cls)
            return response
        # end def start_dpi_calibration

        @classmethod
        def set_dpi_calibration(cls, test_case, sensor_idx, direction, calib_cor, device_index=None, port_index=None):
            """
            Process ``SetDpiCalibration``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param sensor_idx: The index of the sensor
            :type sensor_idx: ``int`` or ``HexList``
            :param direction: The direction of the DPI. 0:X, 1:Y
            :type direction: ``int`` or ``HexList``
            :param calib_cor: The correction value, given by a previous dpiCalibrationCompletedEvent or computed by SW.
            :type calib_cor: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int`` or ``None``

            :return: SetDpiCalibrationResponse
            :rtype: ``SetDpiCalibrationResponse``
            """
            feature_2202_index, feature_2202, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2202.set_dpi_calibration_cls(
                device_index=device_index,
                feature_index=feature_2202_index,
                sensor_idx=HexList(sensor_idx),
                direction=HexList(direction),
                calib_cor=HexList(calib_cor))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=feature_2202.set_dpi_calibration_response_cls)
            return response
        # end def set_dpi_calibration

        @classmethod
        def sensor_dpi_parameters_event(cls, test_case, timeout=2,
                                        check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``SensorDpiParametersEvent``: get notification from event queue

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param timeout: Time to wait for message before raising exception in seconds (0 disable it) - OPTIONAL
            :type timeout: ``float``
            :param check_first_message: Flag to check on the first received message - OPTIONAL
            :type check_first_message: ``bool``
            :param allow_no_message: Flag to raise exception when the requested message in not received - OPTIONAL
            :type allow_no_message: ``bool``
            :param skip_error_message: Flag to skip error catching mechanism - OPTIONAL
            :type skip_error_message: ``bool``

            :return: SensorDpiParametersEvent
            :rtype: ``SensorDpiParametersEvent``
            """
            _, feature_2202, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_2202.sensor_dpi_parameters_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def sensor_dpi_parameters_event

        @classmethod
        def dpi_calibration_completed_event(cls, test_case, timeout=2,
                                            check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``DpiCalibrationCompletedEvent``: get notification from event queue

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param timeout: Time to wait for message before raising exception in seconds (0 disable it) - OPTIONAL
            :type timeout: ``float``
            :param check_first_message: Flag to check on the first received message - OPTIONAL
            :type check_first_message: ``bool``
            :param allow_no_message: Flag to raise exception when the requested message in not received - OPTIONAL
            :type allow_no_message: ``bool``
            :param skip_error_message: Flag to skip error catching mechanism - OPTIONAL
            :type skip_error_message: ``bool``

            :return: DpiCalibrationCompletedEvent
            :rtype: ``DpiCalibrationCompletedEvent``
            """
            _, feature_2202, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_2202.dpi_calibration_completed_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def dpi_calibration_completed_event
    # end class HIDppHelper

    @classmethod
    def get_none_default_dpi_parameters(cls, test_case):
        """
        Get non-default DPI parameters (except LOD)

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: The none-default DPI parameters
        :rtype: tuple[``int``, ``int``, ``int``]
        """
        config = test_case.f.PRODUCT.FEATURES.MOUSE.EXTENDED_ADJUSTABLE_DPI
        dpi_x = int(config.F_DefaultDpiX) + 200
        dpi_y = int(config.F_DefaultDpiY) + 100 if config.F_DpiYSupported else 0
        lod = int(config.F_DefaultLod) if config.F_LodSupported else 0
        return dpi_x, dpi_y, lod
    # end def get_none_default_dpi_parameters

    @classmethod
    def compute_expected_dpi(cls, test_case, dpi_x, dpi_y=0):
        """
        Compute the expected DPI

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param dpi_x: The DPI X value
        :type dpi_x: ``int``
        :param dpi_y: The DPI Y value - OPTIONAL
        :type dpi_y: ``int``

        :return: The expected DPI value be applied in device
        :rtype: tuple[``int``, ``int``]

        :raise ``ValueError``: Whe the DPI step is 0
        """
        dpi_ranges_x = [int(dpi, 16) for dpi in test_case.f.PRODUCT.FEATURES.MOUSE.EXTENDED_ADJUSTABLE_DPI.F_DpiRangesX]
        dpi_ranges_y = [] if dpi_y == 0 else \
            [int(dpi, 16) for dpi in test_case.f.PRODUCT.FEATURES.MOUSE.EXTENDED_ADJUSTABLE_DPI.F_DpiRangesY]
        dpi_ranges = dpi_ranges_x
        new_dpi = dpi_x
        if dpi_x < dpi_y:
            dpi_ranges = dpi_ranges_y
            new_dpi = dpi_y
        # end if
        dpi_ranges_len = len(dpi_ranges)
        step = 0
        for boundary_dpi_idx in range(0, dpi_ranges_len, 2):
            dpi = dpi_ranges[boundary_dpi_idx]
            if new_dpi > dpi:
                continue
            # end if

            if boundary_dpi_idx > 0:
                step = dpi_ranges[boundary_dpi_idx - 1] - 0xE000
                break
            # end if
        # end for

        assert step > 0

        inc_x = (dpi_x + step / 2) // step
        inc_y = (dpi_y + step / 2) // step
        new_dpi_x = int(inc_x * step)
        new_dpi_y = int(inc_y * step)
        return new_dpi_x, new_dpi_y
    # end def compute_expected_dpi

    # noinspection PyShadowingBuiltins
    @classmethod
    def compute_expected_count(cls, test_case, direction, distance=None, min=False, max=False):
        """
        Compute expected count

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param direction: The direction of the DPI. 0:X, 1:Y
        :type direction: ``ExtendedAdjustableDpi.Direction``
        :param distance: The cursor moving distance (mm) in the X/Y direction - OPTIONAL
        :type distance: ``int`` or ``None``
        :param min: Get the min expected count - OPTIONAL
        :type min: ``bool``
        :param max: Get the max expected count - OPTIONAL
        :type max: ``bool``

        :return: The expected count
        :rtype: ``int``

        :raise: ``AssertionError``, if distance is not in the range MouseLength ~ 500mm
        """
        config = test_case.f.PRODUCT.FEATURES.MOUSE.EXTENDED_ADJUSTABLE_DPI
        calib_dpi = config.F_CalibDpiX if direction == ExtendedAdjustableDpi.Direction.X else config.F_CalibDpiY
        if min:
            distance = config.F_MouseLength
        elif max:
            distance = 500
        # end if
        assert distance <= 500, f'The distance({distance} mm) shall <= 500mm'
        assert distance >= config.F_MouseLength, \
            f'The distance({distance} mm) shall >= Mouse Length {config.F_MouseLength} mm'
        return int(distance / 25.4 * calib_dpi)
    # end def compute_expected_count
# end class ExtendedAdjustableDpiTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
