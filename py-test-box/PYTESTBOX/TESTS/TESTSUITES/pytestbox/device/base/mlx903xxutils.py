#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.base.mlx903xxutils
:brief: Helpers for ``MLX903xx`` feature
:author: Gautham S B <gsb@logitech.com>
:date: 2023/04/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
# noinspection PyUnresolvedReferences
from pychannel.channelinterfaceclasses import BaseCommunicationChannel

from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.peripheral.mlx903xx import MLX903xx
from pyhid.hidpp.features.peripheral.mlx903xx import MLX903xxFactory
from pyhid.hidpp.features.peripheral.mlx903xx import MonitorReportEvent
from pyhid.hidpp.features.peripheral.mlx903xx import MonitorTestResponse
from pyhid.hidpp.features.peripheral.mlx903xx import ReadCalibrationResponse
from pyhid.hidpp.features.peripheral.mlx903xx import ReadEPMIQS624RegisterResponse
from pyhid.hidpp.features.peripheral.mlx903xx import ReadSensorRegisterResponse
from pyhid.hidpp.features.peripheral.mlx903xx import ReadTouchStatusResponse
from pyhid.hidpp.features.peripheral.mlx903xx import ResetSensorResponse
from pyhid.hidpp.features.peripheral.mlx903xx import RollerTestEvent
from pyhid.hidpp.features.peripheral.mlx903xx import SetRollerTestResponse
from pyhid.hidpp.features.peripheral.mlx903xx import ShutdownSensorResponse
from pyhid.hidpp.features.peripheral.mlx903xx import StartCalibrationResponse
from pyhid.hidpp.features.peripheral.mlx903xx import StopCalibrationResponse
from pyhid.hidpp.features.peripheral.mlx903xx import WriteCalibrationResponse
from pyhid.hidpp.features.peripheral.mlx903xx import WriteSensorRegisterResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MLX903xxTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``MLX903xx`` feature
    """

    class ReadSensorRegisterResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``ReadSensorRegisterResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "register_address": (cls.check_register_address, None),
                "register_value": (cls.check_register_value_in_range, 0xFFFF)
            }
        # end def get_default_check_map

        @staticmethod
        def check_register_address(test_case, response, expected):
            """
            Check register_address field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadSensorRegisterResponse to check
            :type response: ``ReadSensorRegisterResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert register_address that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The register_address shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.register_address),
                msg="The register_address parameter differs from the one expected")
        # end def check_register_address

        @staticmethod
        def check_register_value(test_case, response, expected):
            """
            Check register_value field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadSensorRegisterResponse to check
            :type response: ``ReadSensorRegisterResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert register_value that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The register_value shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.register_value),
                msg="The register_value parameter differs from the one expected")
        # end def check_register_value

        @staticmethod
        def check_register_value_in_range(test_case, response, expected):
            """
            Check register_value field is in range

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadSensorRegisterResponse to check
            :type response: ``ReadSensorRegisterResponse``
            :param expected: Expected value
            :type expected: ``HexList``
            """
            test_case.assertNotNone(
                expected,
                msg="The register_value shall be passed as an argument")
            test_case.assertTrue(
                0 <= to_int(response.register_value) <= to_int(expected),
                msg=f"The register_value {response.register_value} is not in expected range (0, {expected})")
        # def check_register_value_in_range
    # end class ReadSensorRegisterResponseChecker

    class CalibrationResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``ReadCalibrationResponse | StopCalibrationResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "nb_turns": (cls.check_nb_turns_in_range, 0xFF),
                "min_x": (cls.check_min_x_in_range, HexList("FFFF")),
                "max_x": (cls.check_max_x_in_range, HexList("FFFF")),
                "min_y": (cls.check_min_y_in_range, HexList("FFFF")),
                "max_y": (cls.check_max_y_in_range, HexList("FFFF"))
            }
        # end def get_default_check_map

        @staticmethod
        def check_nb_turns(test_case, response, expected):
            """
            Check nb_turns field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadCalibrationResponse or StopCalibrationResponse to check
            :type response: ``ReadCalibrationResponse | StopCalibrationResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert nb_turns that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The nb_turns shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.nb_turns),
                msg="The nb_turns parameter differs from the one expected")
        # end def check_nb_turns

        @staticmethod
        def check_min_x(test_case, response, expected):
            """
            Check min_x field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadCalibrationResponse or StopCalibrationResponse to check
            :type response: ``ReadCalibrationResponse | StopCalibrationResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert min_x that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The min_x shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.min_x),
                msg="The min_x parameter differs from the one expected")
        # end def check_min_x

        @staticmethod
        def check_max_x(test_case, response, expected):
            """
            Check max_x field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadCalibrationResponse or StopCalibrationResponse to check
            :type response: ``ReadCalibrationResponse | StopCalibrationResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert max_x that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The max_x shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.max_x),
                msg="The max_x parameter differs from the one expected")
        # end def check_max_x

        @staticmethod
        def check_min_y(test_case, response, expected):
            """
            Check min_y field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadCalibrationResponse or StopCalibrationResponse to check
            :type response: ``ReadCalibrationResponse | StopCalibrationResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert min_y that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The min_y shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.min_y),
                msg="The min_y parameter differs from the one expected")
        # end def check_min_y

        @staticmethod
        def check_max_y(test_case, response, expected):
            """
            Check max_y field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadCalibrationResponse or StopCalibrationResponse to check
            :type response: ``ReadCalibrationResponse | StopCalibrationResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert max_y that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The max_y shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.max_y),
                msg="The max_y parameter differs from the one expected")
        # end def check_max_y

        @staticmethod
        def check_nb_turns_in_range(test_case, response, expected):
            """
            Check nb_turns field is in range

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadCalibrationResponse or StopCalibrationResponse to check
            :type response: ``ReadCalibrationResponse | StopCalibrationResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert nb_turns that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The nb_turns shall be passed as an argument")
            test_case.assertTrue(0 <= to_int(response.nb_turns) <= to_int(expected),
                                 msg=f"The nb_turns value {response.nb_turns} is not in expected range (0, {expected})")
        # def check_nb_turns_in_range

        @staticmethod
        def check_min_x_in_range(test_case, response, expected):
            """
            Check min_x field is in range

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadCalibrationResponse or StopCalibrationResponse to check
            :type response: ``ReadCalibrationResponse | StopCalibrationResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert min_x that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The min_x shall be passed as an argument")
            test_case.assertTrue(0 <= to_int(response.min_x) <= to_int(expected),
                                 msg=f"The min_x value {response.min_x} is not in expected range (0, {expected})")
        # def check_min_x_in_range

        @staticmethod
        def check_max_x_in_range(test_case, response, expected):
            """
            Check max_x field is in range

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadCalibrationResponse or StopCalibrationResponse to check
            :type response: ``ReadCalibrationResponse | StopCalibrationResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert max_x that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The max_x shall be passed as an argument")
            test_case.assertTrue(0 <= to_int(response.max_x) <= to_int(expected),
                                 msg=f"The max_x value {response.max_X} is not in expected range (0, {expected})")
        # def check_max_x_in_range

        @staticmethod
        def check_min_y_in_range(test_case, response, expected):
            """
            Check min_y field is in range

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadCalibrationResponse or StopCalibrationResponse to check
            :type response: ``ReadCalibrationResponse | StopCalibrationResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert min_y that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The min_y shall be passed as an argument")
            test_case.assertTrue(0 <= to_int(response.min_y) <= to_int(expected),
                                 msg=f"The min_y value {response.min_y} is not in expected range (0, {expected})")
        # def check_min_y_in_range

        @staticmethod
        def check_max_y_in_range(test_case, response, expected):
            """
            Check max_y field is in range

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadCalibrationResponse or StopCalibrationResponse to check
            :type response: ``ReadCalibrationResponse | StopCalibrationResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert max_y that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The max_y shall be passed as an argument")
            test_case.assertTrue(0 <= to_int(response.max_y) <= to_int(expected),
                                 msg=f"The max_y value {response.max_y} is not in expected range (0, {expected})")
        # def check_max_y_in_range
    # end class CalibrationResponseChecker

    class StopCalibrationResponseChecker(CalibrationResponseChecker):
        """
        Define Helper to check ``StopCalibrationResponse``
        """
    # end class StopCalibrationResponseChecker

    class ReadCalibrationResponseChecker(CalibrationResponseChecker):
        """
        Define Helper to check ``ReadCalibrationResponse``
        """
    # end class ReadCalibrationResponseChecker

    class ReadTouchStatusResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``ReadTouchStatusResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "status": (cls.check_status, MLX903xx.Touch.UNTOUCHED_STATE),
            }
        # end def get_default_check_map

        @staticmethod
        def check_status(test_case, response, expected):
            """
            Check status field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadTouchStatusResponse to check
            :type response: ``ReadTouchStatusResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert status that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The status shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.status),
                msg="The status parameter differs from the one expected")
        # end def check_status
    # end class ReadTouchStatusResponseChecker

    class ReadEPMIQS624RegisterResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``ReadEPMIQS624RegisterResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "register_address": (cls.check_register_address, None),
                "register_value": (cls.check_register_value_in_range, 0xFFFF)
            }
        # end def get_default_check_map

        @staticmethod
        def check_register_address(test_case, response, expected):
            """
            Check register_address field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadEPMIQS624RegisterResponse to check
            :type response: ``ReadEPMIQS624RegisterResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert register_address that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The register_address shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.register_address),
                msg="The register_address parameter differs from the one expected")
        # end def check_register_address

        @staticmethod
        def check_register_value(test_case, response, expected):
            """
            Check register_value field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadEPMIQS624RegisterResponse to check
            :type response: ``ReadEPMIQS624RegisterResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert register_value that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The register_value shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.register_value),
                msg="The register_value parameter differs from the one expected")
        # end def check_register_value

        @staticmethod
        def check_register_value_in_range(test_case, response, expected):
            """
            Check register_value field in response is in expected range

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadEPMIQS624RegisterResponse to check
            :type response: ``ReadEPMIQS624RegisterResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert register_value that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The register_value shall be passed as an argument")
            test_case.assertTrue(expr=0 <= to_int(response.register_value) <= to_int(expected),
                                 msg=f"The register_value {response.register_value} "
                                     f"is not in expected range (0, {expected})")
        # end def check_register_value_in_range
    # end class ReadEPMIQS624RegisterResponseChecker

    class MonitorReportEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``MonitorReportEvent``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "field_x": (cls.check_field_x, None),
                "field_y": (cls.check_field_y, None),
                "field_z": (cls.check_field_z, None),
                "temperature": (cls.check_temperature, None),
                "angle": (cls.check_angle, None),
                "slot": (cls.check_slot, None),
                "ratchet": (cls.check_ratchet, None),
                "angle_offset": (cls.check_angle_offset, None),
                "angle_ratchet_number": (cls.check_angle_ratchet_number, None),
                "counter": (cls.check_counter, None)
            }
        # end def get_default_check_map

        @staticmethod
        def check_field_x(test_case, event, expected):
            """
            Check field_x field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: MonitorReportEvent to check
            :type event: ``MonitorReportEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert field_x that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The field_x shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.field_x),
                msg="The field_x parameter differs from the one expected")
        # end def check_field_x

        @staticmethod
        def check_field_y(test_case, event, expected):
            """
            Check field_y field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: MonitorReportEvent to check
            :type event: ``MonitorReportEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert field_y that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The field_y shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.field_y),
                msg="The field_y parameter differs from the one expected")
        # end def check_field_y

        @staticmethod
        def check_field_z(test_case, event, expected):
            """
            Check field_z field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: MonitorReportEvent to check
            :type event: ``MonitorReportEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert field_z that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The field_z shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.field_z),
                msg="The field_z parameter differs from the one expected")
        # end def check_field_z

        @staticmethod
        def check_temperature(test_case, event, expected):
            """
            Check temperature field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: MonitorReportEvent to check
            :type event: ``MonitorReportEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert temperature that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The temperature shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.temperature),
                msg="The temperature parameter differs from the one expected")
        # end def check_temperature

        @staticmethod
        def check_angle(test_case, event, expected):
            """
            Check angle field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: MonitorReportEvent to check
            :type event: ``MonitorReportEvent``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert angle that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The angle shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.angle),
                msg="The angle parameter differs from the one expected")
        # end def check_angle

        @staticmethod
        def check_slot(test_case, event, expected):
            """
            Check slot field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: MonitorReportEvent to check
            :type event: ``MonitorReportEvent``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert slot that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The slot shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.slot),
                msg="The slot parameter differs from the one expected")
        # end def check_slot

        @staticmethod
        def check_ratchet(test_case, event, expected):
            """
            Check ratchet field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: MonitorReportEvent to check
            :type event: ``MonitorReportEvent``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert ratchet that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The ratchet shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.ratchet),
                msg="The ratchet parameter differs from the one expected")
        # end def check_ratchet

        @staticmethod
        def check_angle_offset(test_case, event, expected):
            """
            Check angle_offset field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: MonitorReportEvent to check
            :type event: ``MonitorReportEvent``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert angle_offset that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The angle_offset shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.angle_offset),
                msg="The angle_offset parameter differs from the one expected")
        # end def check_angle_offset

        @staticmethod
        def check_angle_ratchet_number(test_case, event, expected):
            """
            Check angle_ratchet_number field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: MonitorReportEvent to check
            :type event: ``MonitorReportEvent``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert angle_ratchet_number that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The angle_ratchet_number shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.angle_ratchet_number),
                msg="The angle_ratchet_number parameter differs from the one expected")
        # end def check_angle_ratchet_number

        @staticmethod
        def check_counter(test_case, event, expected):
            """
            Check counter field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: MonitorReportEvent to check
            :type event: ``MonitorReportEvent``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert counter that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The counter shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.counter),
                msg="The counter parameter differs from the one expected")
        # end def check_counter
    # end class MonitorReportEventChecker

    class RollerTestEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``RollerTestEvent``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "accumulator": (cls.check_accumulator, None),
                "timestamp_value": (cls.check_timestamp_value, None)
            }
        # end def get_default_check_map

        @staticmethod
        def check_accumulator(test_case, event, expected):
            """
            Check accumulator field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: RollerTestEvent to check
            :type event: ``RollerTestEvent``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert accumulator that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The accumulator shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.accumulator),
                msg="The accumulator parameter differs from the one expected")
        # end def check_accumulator

        @staticmethod
        def check_timestamp_value(test_case, event, expected):
            """
            Check timestamp_value field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: RollerTestEvent to check
            :type event: ``RollerTestEvent``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert timestamp_value that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The timestamp_value shall be passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.timestamp_value),
                msg="The timestamp_value parameter differs from the one expected")
        # end def check_timestamp_value
    # end class RollerTestEventChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case,
                           feature_id=MLX903xx.FEATURE_ID,
                           factory=MLX903xxFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def read_sensor_register(cls, test_case, register_address, device_index=None, port_index=None,
                                 software_id=None, padding=None):
            """
            Process ``ReadSensorRegister``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param register_address: The register address
            :type register_address: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: ReadSensorRegisterResponse (if not error)
            :rtype: ``ReadSensorRegisterResponse``
            """
            feature_9205_index, feature_9205, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9205.read_sensor_register_cls(
                device_index=device_index,
                feature_index=feature_9205_index,
                register_address=HexList(register_address))

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_9205.read_sensor_register_response_cls)
        # end def read_sensor_register

        @classmethod
        def read_sensor_register_and_check_error(
                cls, test_case, error_codes, register_address, function_index=None,
                device_index=None, port_index=None):
            """
            Process ``ReadSensorRegister``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param register_address: The register address
            :type register_address: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_9205_index, feature_9205, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9205.read_sensor_register_cls(
                device_index=device_index,
                feature_index=feature_9205_index,
                register_address=HexList(register_address))

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def read_sensor_register_and_check_error

        @classmethod
        def write_sensor_register(cls, test_case, register_address, register_value, device_index=None,
                                  port_index=None, software_id=None):
            """
            Process ``WriteSensorRegister``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param register_address: The register address
            :type register_address: ``int | HexList``
            :param register_value: The register value
            :type register_value: ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``

            :return: WriteSensorRegisterResponse (if not error)
            :rtype: ``WriteSensorRegisterResponse``
            """
            feature_9205_index, feature_9205, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9205.write_sensor_register_cls(
                device_index=device_index,
                feature_index=feature_9205_index,
                register_address=HexList(register_address),
                register_value=register_value)

            if software_id is not None:
                report.software_id = software_id
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_9205.write_sensor_register_response_cls)
        # end def write_sensor_register

        @classmethod
        def write_sensor_register_and_check_error(
                cls, test_case, error_codes, register_address, register_value, function_index=None,
                device_index=None, port_index=None):
            """
            Process ``WriteSensorRegister``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param register_address: The register address
            :type register_address: ``int | HexList``
            :param register_value: The register value
            :type register_value: ``HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_9205_index, feature_9205, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9205.write_sensor_register_cls(
                device_index=device_index,
                feature_index=feature_9205_index,
                register_address=HexList(register_address),
                register_value=register_value)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def write_sensor_register_and_check_error

        @classmethod
        def reset_sensor(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``ResetSensor``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: ResetSensorResponse (if not error)
            :rtype: ``ResetSensorResponse``
            """
            feature_9205_index, feature_9205, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9205.reset_sensor_cls(
                device_index=device_index,
                feature_index=feature_9205_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_9205.reset_sensor_response_cls)
        # end def reset_sensor

        @classmethod
        def reset_sensor_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``ResetSensor``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_9205_index, feature_9205, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9205.reset_sensor_cls(
                device_index=device_index,
                feature_index=feature_9205_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def reset_sensor_and_check_error

        @classmethod
        def shutdown_sensor(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``ShutdownSensor``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: ShutdownSensorResponse (if not error)
            :rtype: ``ShutdownSensorResponse``
            """
            feature_9205_index, feature_9205, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9205.shutdown_sensor_cls(
                device_index=device_index,
                feature_index=feature_9205_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_9205.shutdown_sensor_response_cls)
        # end def shutdown_sensor

        @classmethod
        def shutdown_sensor_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``ShutdownSensor``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_9205_index, feature_9205, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9205.shutdown_sensor_cls(
                device_index=device_index,
                feature_index=feature_9205_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def shutdown_sensor_and_check_error

        @classmethod
        def monitor_test(cls, test_case, count, threshold, device_index=None, port_index=None, software_id=None):
            """
            Process ``MonitorTest``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param count: The total number of events requested
            :type count: ``int | HexList``
            :param threshold: The minimum, absolute, variation on X or Y field values so that a new report be generated
            :type threshold: ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``

            :return: MonitorTestResponse (if not error)
            :rtype: ``MonitorTestResponse``
            """
            feature_9205_index, feature_9205, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9205.monitor_test_cls(
                device_index=device_index,
                feature_index=feature_9205_index,
                count=HexList(count),
                threshold=threshold)

            if software_id is not None:
                report.software_id = software_id
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_9205.monitor_test_response_cls)
        # end def monitor_test

        @classmethod
        def monitor_test_and_check_error(
                cls, test_case, error_codes, count, threshold, function_index=None,
                device_index=None, port_index=None):
            """
            Process ``MonitorTest``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param count: The total number of events requested
            :type count: ``int | HexList``
            :param threshold: The minimum, absolute, variation on X or Y field values so that a new report be generated
            :type threshold: ``HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_9205_index, feature_9205, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9205.monitor_test_cls(
                device_index=device_index,
                feature_index=feature_9205_index,
                count=HexList(count),
                threshold=threshold)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def monitor_test_and_check_error

        @classmethod
        def start_calibration(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``StartCalibration``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: StartCalibrationResponse (if not error)
            :rtype: ``StartCalibrationResponse``
            """
            feature_9205_index, feature_9205, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9205.start_calibration_cls(
                device_index=device_index,
                feature_index=feature_9205_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_9205.start_calibration_response_cls)
        # end def start_calibration

        @classmethod
        def start_calibration_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``StartCalibration``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_9205_index, feature_9205, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9205.start_calibration_cls(
                device_index=device_index,
                feature_index=feature_9205_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def start_calibration_and_check_error

        @classmethod
        def stop_calibration(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``StopCalibration``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: StopCalibrationResponse (if not error)
            :rtype: ``StopCalibrationResponse``
            """
            feature_9205_index, feature_9205, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9205.stop_calibration_cls(
                device_index=device_index,
                feature_index=feature_9205_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_9205.stop_calibration_response_cls)
        # end def stop_calibration

        @classmethod
        def stop_calibration_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``StopCalibration``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_9205_index, feature_9205, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9205.stop_calibration_cls(
                device_index=device_index,
                feature_index=feature_9205_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def stop_calibration_and_check_error

        @classmethod
        def read_calibration(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``ReadCalibration``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: ReadCalibrationResponse (if not error)
            :rtype: ``ReadCalibrationResponse``
            """
            feature_9205_index, feature_9205, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9205.read_calibration_cls(
                device_index=device_index,
                feature_index=feature_9205_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_9205.read_calibration_response_cls)
        # end def read_calibration

        @classmethod
        def read_calibration_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``ReadCalibration``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_9205_index, feature_9205, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9205.read_calibration_cls(
                device_index=device_index,
                feature_index=feature_9205_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def read_calibration_and_check_error

        @classmethod
        def write_calibration(cls, test_case, nb_turns, min_x, max_x, min_y, max_y, device_index=None,
                              port_index=None, software_id=None, padding=None):
            """
            Process ``WriteCalibration``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param nb_turns: The number of complete turns affected
            :type nb_turns: ``int | HexList``
            :param min_x: X field minimum value
            :type min_x: ``HexList``
            :param max_x: X field maximum value
            :type max_x: ``HexList``
            :param min_y: Y field minimum value
            :type min_y: ``HexList``
            :param max_y: Y field maximum value
            :type max_y: ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: WriteCalibrationResponse (if not error)
            :rtype: ``WriteCalibrationResponse``
            """
            feature_9205_index, feature_9205, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9205.write_calibration_cls(
                device_index=device_index,
                feature_index=feature_9205_index,
                nb_turns=HexList(nb_turns),
                min_x=min_x,
                max_x=max_x,
                min_y=min_y,
                max_y=max_y)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_9205.write_calibration_response_cls)
        # end def write_calibration

        @classmethod
        def write_calibration_and_check_error(
                cls, test_case, error_codes, nb_turns, min_x, max_x, min_y, max_y,
                function_index=None, device_index=None, port_index=None):
            """
            Process ``WriteCalibration``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param nb_turns: The number of complete turns affected
            :type nb_turns: ``int | HexList``
            :param min_x: X field minimum value
            :type min_x: ``HexList``
            :param max_x: X field maximum value
            :type max_x: ``HexList``
            :param min_y: Y field minimum value
            :type min_y: ``HexList``
            :param max_y: Y field maximum value
            :type max_y: ``HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_9205_index, feature_9205, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9205.write_calibration_cls(
                device_index=device_index,
                feature_index=feature_9205_index,
                nb_turns=HexList(nb_turns),
                min_x=min_x,
                max_x=max_x,
                min_y=min_y,
                max_y=max_y)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def write_calibration_and_check_error

        @classmethod
        def read_touch_status(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``ReadTouchStatus``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: ReadTouchStatusResponse (if not error)
            :rtype: ``ReadTouchStatusResponse``
            """
            feature_9205_index, feature_9205, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9205.read_touch_status_cls(
                device_index=device_index,
                feature_index=feature_9205_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_9205.read_touch_status_response_cls)
        # end def read_touch_status

        @classmethod
        def read_touch_status_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``ReadTouchStatus``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_9205_index, feature_9205, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9205.read_touch_status_cls(
                device_index=device_index,
                feature_index=feature_9205_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def read_touch_status_and_check_error

        @classmethod
        def set_roller_test(cls, test_case, multiplier, test_mode, device_index=None, port_index=None,
                            software_id=None, padding=None):
            """
            Process ``SetRollerTest``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param multiplier: The period multiplier
            :type multiplier: ``int | HexList``
            :param test_mode: The test mode HID/HIDPP
            :type test_mode: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: SetRollerTestResponse (if not error)
            :rtype: ``SetRollerTestResponse``
            """
            feature_9205_index, feature_9205, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9205.set_roller_test_cls(
                device_index=device_index,
                feature_index=feature_9205_index,
                multiplier=HexList(multiplier),
                test_mode=HexList(test_mode))

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_9205.set_roller_test_response_cls)
        # end def set_roller_test

        @classmethod
        def set_roller_test_and_check_error(
                cls, test_case, error_codes, multiplier, test_mode, function_index=None,
                device_index=None, port_index=None):
            """
            Process ``SetRollerTest``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param multiplier: The period multiplier
            :type multiplier: ``int | HexList``
            :param test_mode: The test mode HID/HIDPP
            :type test_mode: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_9205_index, feature_9205, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9205.set_roller_test_cls(
                device_index=device_index,
                feature_index=feature_9205_index,
                multiplier=HexList(multiplier),
                test_mode=HexList(test_mode))

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def set_roller_test_and_check_error

        @classmethod
        def read_epm_iqs624_register(cls, test_case, register_address, device_index=None, port_index=None,
                                     software_id=None, padding=None):
            """
            Process ``ReadEPMIQS624Register``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param register_address: The register address
            :type register_address: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: ReadEPMIQS624RegisterResponse (if not error)
            :rtype: ``ReadEPMIQS624RegisterResponse``
            """
            feature_9205_index, feature_9205, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9205.read_epm_iqs624_register_cls(
                device_index=device_index,
                feature_index=feature_9205_index,
                register_address=HexList(register_address))

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_9205.read_epm_iqs624_register_response_cls)
        # end def read_epm_iqs624_register

        @classmethod
        def read_epm_iqs624_register_and_check_error(
                cls, test_case, error_codes, register_address, function_index=None, device_index=None, port_index=None):
            """
            Process ``ReadEPMIQS624Register``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param register_address: The register address
            :type register_address: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_9205_index, feature_9205, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9205.read_epm_iqs624_register_cls(
                device_index=device_index,
                feature_index=feature_9205_index,
                register_address=HexList(register_address))

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def read_epm_iqs624_register_and_check_error

        @classmethod
        def monitor_report_event(
                cls, test_case, timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``MonitorReportEvent``: get notification from event queue

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param timeout: Time to wait for message before raising exception in seconds (0 disable it) - OPTIONAL
            :type timeout: ``float``
            :param check_first_message: Flag to check on the first received message - OPTIONAL
            :type check_first_message: ``bool``
            :param allow_no_message: Flag to raise exception when the requested message in not received - OPTIONAL
            :type allow_no_message: ``bool``
            :param skip_error_message: Flag to skip error catching mechanism - OPTIONAL
            :type skip_error_message: ``bool``

            :return: MonitorReportEvent
            :rtype: ``MonitorReportEvent``
            """
            _, feature_9205, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_9205.monitor_report_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def monitor_report_event

        @classmethod
        def roller_test_event(
                cls, test_case, timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``RollerTestEvent``: get notification from event queue

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param timeout: Time to wait for message before raising exception in seconds (0 disable it) - OPTIONAL
            :type timeout: ``float``
            :param check_first_message: Flag to check on the first received message - OPTIONAL
            :type check_first_message: ``bool``
            :param allow_no_message: Flag to raise exception when the requested message in not received - OPTIONAL
            :type allow_no_message: ``bool``
            :param skip_error_message: Flag to skip error catching mechanism - OPTIONAL
            :type skip_error_message: ``bool``

            :return: RollerTestEvent
            :rtype: ``RollerTestEvent``
            """
            _, feature_9205, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_9205.roller_test_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def roller_test_event
    # end class HIDppHelper
# end class MLX903xxTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
