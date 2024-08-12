#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.base.manufacturingmodeutils
:brief: Helpers for ``ManufacturingMode`` feature
:author: Masan Xu <mxu11@logitech.com>
:date: 2023/06/14
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.manufacturingmode import GetManufacturingModeResponse
from pyhid.hidpp.features.common.manufacturingmode import ManufacturingMode
from pyhid.hidpp.features.common.manufacturingmode import ManufacturingModeFactory
from pyhid.hidpp.features.common.manufacturingmode import SetManufacturingModeResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ManufacturingModeTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``ManufacturingMode`` feature
    """

    class GetManufacturingModeResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetManufacturingModeResponse``
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
                "reserved": (cls.check_reserved, 0),
                "manufacturing_mode": (cls.check_manufacturing_mode, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetManufacturingModeResponse to check
            :type response: ``GetManufacturingModeResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The reserved shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs from the one expected")
        # end def check_reserved

        @staticmethod
        def check_manufacturing_mode(test_case, response, expected):
            """
            Check manufacturing_mode field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetManufacturingModeResponse to check
            :type response: ``GetManufacturingModeResponse``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert manufacturing_mode that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The manufacturing_mode shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.manufacturing_mode),
                msg="The manufacturing_mode parameter differs from the one expected")
        # end def check_manufacturing_mode
    # end class GetManufacturingModeResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case,
                           feature_id=ManufacturingMode.FEATURE_ID,
                           factory=ManufacturingModeFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def set_manufacturing_mode(cls, test_case, manufacturing_mode, device_index=None, port_index=None,
                                   software_id=None, padding=None):
            """
            Process ``SetManufacturingMode``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param manufacturing_mode: Manufacturing Mode
            :type manufacturing_mode: ``bool | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: SetManufacturingModeResponse (if not error)
            :rtype: ``SetManufacturingModeResponse``
            """
            feature_1801_index, feature_1801, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1801.set_manufacturing_mode_cls(
                device_index=device_index,
                feature_index=feature_1801_index,
                manufacturing_mode=manufacturing_mode)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1801.set_manufacturing_mode_response_cls)
        # end def set_manufacturing_mode

        @classmethod
        def set_manufacturing_mode_and_check_error(
                cls, test_case, error_codes, manufacturing_mode, function_index=None,
                device_index=None, port_index=None, reserved=None):
            """
            Process ``SetManufacturingMode``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param manufacturing_mode: Manufacturing Mode
            :type manufacturing_mode: ``bool | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param reserved: Reserved - OPTIONAL
            :type reserved: ``int | None``
            """
            feature_1801_index, feature_1801, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1801.set_manufacturing_mode_cls(
                device_index=device_index,
                feature_index=feature_1801_index,
                manufacturing_mode=manufacturing_mode)

            if function_index is not None:
                report.function_index = function_index
            # end if

            if reserved is not None:
                report.reserved = reserved
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def set_manufacturing_mode_and_check_error

        @classmethod
        def get_manufacturing_mode(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetManufacturingMode``

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

            :return: GetManufacturingModeResponse (if not error)
            :rtype: ``GetManufacturingModeResponse``
            """
            feature_1801_index, feature_1801, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1801.get_manufacturing_mode_cls(
                device_index=device_index,
                feature_index=feature_1801_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1801.get_manufacturing_mode_response_cls)
        # end def get_manufacturing_mode

        @classmethod
        def get_manufacturing_mode_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``GetManufacturingMode``

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
            feature_1801_index, feature_1801, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1801.get_manufacturing_mode_cls(
                device_index=device_index,
                feature_index=feature_1801_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_manufacturing_mode_and_check_error
    # end class HIDppHelper
# end class ManufacturingModeTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
