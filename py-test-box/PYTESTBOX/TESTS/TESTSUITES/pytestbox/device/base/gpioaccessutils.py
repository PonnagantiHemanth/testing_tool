#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.base.gpioaccessutils
:brief: Helpers for ``GpioAccess`` feature
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/06/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.gpioaccess import GpioAccess
from pyhid.hidpp.features.common.gpioaccess import GpioAccessFactory
from pyhid.hidpp.features.common.gpioaccess import ReadGroupOutResponseV1
from pyhid.hidpp.features.common.gpioaccess import ReadGroupResponse
from pyhid.hidpp.features.common.gpioaccess import SetGroupInResponse
from pyhid.hidpp.features.common.gpioaccess import WriteGroupOutResponse
from pyhid.hidpp.features.common.gpioaccess import WriteGroupResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class GpioAccessTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``GpioAccess`` feature
    """

    class ReadGroupResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``ReadGroupResponse``
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
            config = test_case.f.PRODUCT.FEATURES.COMMON.GPIO_ACCESS
            return {
                "port_number": (
                    cls.check_port_number,
                    # Port Number always starts with 0
                    0),
                "gpio_mask": (
                    cls.check_gpio_mask,
                    config.F_GpioInputMask[0]),
                "value": (
                    cls.check_value,
                    config.F_GpioInputValue[0])
            }
        # end def get_default_check_map

        @staticmethod
        def check_port_number(test_case, response, expected):
            """
            Check port_number field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadGroupResponse to check
            :type response: ``ReadGroupResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert port_number that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The port_number shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.port_number),
                msg=f"The port_number parameter differs "
                    f"(expected:{expected}, obtained:{response.port_number})")
        # end def check_port_number

        @staticmethod
        def check_gpio_mask(test_case, response, expected):
            """
            Check gpio_mask field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadGroupResponse to check
            :type response: ``ReadGroupResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert gpio_mask that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The gpio_mask shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.gpio_mask),
                msg=f"The gpio_mask parameter differs "
                    f"(expected:{expected}, obtained:{response.gpio_mask})")
        # end def check_gpio_mask

        @staticmethod
        def check_value(test_case, response, expected):
            """
            Check value field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadGroupResponse to check
            :type response: ``ReadGroupResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert value that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The value shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.value),
                msg=f"The value parameter differs "
                    f"(expected:{expected}, obtained:{response.value})")
        # end def check_value
    # end class ReadGroupResponseChecker

    class ReadGroupOutResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``ReadGroupOutResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``

            :raise ``NotImplementedError``: Version that raise an exception
            """
            config = test_case.f.PRODUCT.FEATURES.COMMON.GPIO_ACCESS
            version = test_case.config_manager.get_feature_version(config)
            if version != cls.Version.ZERO:
                return {
                    "port_number": (cls.check_port_number, 0),
                    "gpio_mask": (cls.check_gpio_mask, config.F_GpioOutputMask[0]),
                    "value": (cls.check_value, config.F_GpioOutputMask[0])
                }
            else:
                raise NotImplementedError(f"ReadGroupOut function is not supported in version {version}")
            # end if
        # end def get_default_check_map

        @staticmethod
        def check_port_number(test_case, response, expected):
            """
            Check port_number field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadGroupOutResponse to check
            :type response: ``ReadGroupOutResponseV1``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert port_number that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The port_number shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.port_number),
                msg="The port_number parameter differs from the one expected")
        # end def check_port_number

        @staticmethod
        def check_gpio_mask(test_case, response, expected):
            """
            Check gpio_mask field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadGroupOutResponse to check
            :type response: ``ReadGroupOutResponseV1``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert gpio_mask that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The gpio_mask shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.gpio_mask),
                msg="The gpio_mask parameter differs from the one expected")
        # end def check_gpio_mask

        @staticmethod
        def check_value(test_case, response, expected):
            """
            Check value field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadGroupOutResponse to check
            :type response: ``ReadGroupOutResponseV1``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert value that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The value shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.value),
                msg="The value parameter differs "
                    f"(expected:{expected}, obtained:{response.value})")
        # end def check_value
    # end class ReadGroupOutResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=GpioAccess.FEATURE_ID, factory=GpioAccessFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def set_group_in(cls, test_case, port_number, gpio_mask, device_index=None, port_index=None, software_id=None,
                         padding=None):
            """
            Process ``SetGroupIn``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param port_number: Port Number
            :type port_number: ``int | HexList``
            :param gpio_mask: Gpio Mask
            :type gpio_mask: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: SetGroupInResponse (if not error)
            :rtype: ``SetGroupInResponse``
            """
            feature_1803_index, feature_1803, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1803.set_group_in_cls(
                device_index=device_index,
                feature_index=feature_1803_index,
                port_number=HexList(port_number),
                gpio_mask=HexList(gpio_mask))

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
                response_class_type=feature_1803.set_group_in_response_cls)
        # end def set_group_in

        @classmethod
        def set_group_in_and_check_error(
                cls, test_case, error_codes, port_number, gpio_mask, function_index=None,
                device_index=None, port_index=None):
            """
            Process ``SetGroupIn``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param port_number: Port Number
            :type port_number: ``int | HexList``
            :param gpio_mask: Gpio Mask
            :type gpio_mask: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_1803_index, feature_1803, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1803.set_group_in_cls(
                device_index=device_index,
                feature_index=feature_1803_index,
                port_number=HexList(port_number),
                gpio_mask=HexList(gpio_mask))

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def set_group_in_and_check_error

        @classmethod
        def write_group_out(cls, test_case, port_number, gpio_mask, value, device_index=None, port_index=None,
                            software_id=None, padding=None):
            """
            Process ``WriteGroupOut``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param port_number: Port Number
            :type port_number: ``int | HexList``
            :param gpio_mask: Gpio Mask
            :type gpio_mask: ``int | HexList``
            :param value: Value
            :type value: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: WriteGroupOutResponse (if not error)
            :rtype: ``WriteGroupOutResponse``
            """
            feature_1803_index, feature_1803, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1803.write_group_out_cls(
                device_index=device_index,
                feature_index=feature_1803_index,
                port_number=HexList(port_number),
                gpio_mask=HexList(gpio_mask),
                value=HexList(value))

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
                response_class_type=feature_1803.write_group_out_response_cls)
        # end def write_group_out

        @classmethod
        def write_group_out_and_check_error(
                cls, test_case, error_codes, port_number, gpio_mask, value, function_index=None,
                device_index=None, port_index=None):
            """
            Process ``WriteGroupOut``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param port_number: Port Number
            :type port_number: ``int | HexList``
            :param gpio_mask: Gpio Mask
            :type gpio_mask: ``int | HexList``
            :param value: Value
            :type value: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_1803_index, feature_1803, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1803.write_group_out_cls(
                device_index=device_index,
                feature_index=feature_1803_index,
                port_number=HexList(port_number),
                gpio_mask=HexList(gpio_mask),
                value=HexList(value))

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def write_group_out_and_check_error

        @classmethod
        def read_group(cls, test_case, port_number, gpio_mask, device_index=None, port_index=None, software_id=None,
                       padding=None):
            """
            Process ``ReadGroup``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param port_number: Port Number
            :type port_number: ``int | HexList``
            :param gpio_mask: Gpio Mask
            :type gpio_mask: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: ReadGroupResponse (if not error)
            :rtype: ``ReadGroupResponse``
            """
            feature_1803_index, feature_1803, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1803.read_group_cls(
                device_index=device_index,
                feature_index=feature_1803_index,
                port_number=HexList(port_number),
                gpio_mask=HexList(gpio_mask))

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
                response_class_type=feature_1803.read_group_response_cls)
        # end def read_group

        @classmethod
        def read_group_and_check_error(
                cls, test_case, error_codes, port_number, gpio_mask, function_index=None,
                device_index=None, port_index=None):
            """
            Process ``ReadGroup``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param port_number: Port Number
            :type port_number: ``int | HexList``
            :param gpio_mask: Gpio Mask
            :type gpio_mask: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_1803_index, feature_1803, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1803.read_group_cls(
                device_index=device_index,
                feature_index=feature_1803_index,
                port_number=HexList(port_number),
                gpio_mask=HexList(gpio_mask))

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def read_group_and_check_error

        @classmethod
        def write_group(cls, test_case, port_number, gpio_mask, value, device_index=None, port_index=None,
                        software_id=None, padding=None):
            """
            Process ``WriteGroup``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param port_number: Port Number
            :type port_number: ``int | HexList``
            :param gpio_mask: Gpio Mask
            :type gpio_mask: ``int | HexList``
            :param value: Value
            :type value: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: WriteGroupResponse (if not error)
            :rtype: ``WriteGroupResponse``
            """
            feature_1803_index, feature_1803, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1803.write_group_cls(
                device_index=device_index,
                feature_index=feature_1803_index,
                port_number=HexList(port_number),
                gpio_mask=HexList(gpio_mask),
                value=HexList(value))

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
                response_class_type=feature_1803.write_group_response_cls)
        # end def write_group

        @classmethod
        def write_group_and_check_error(
                cls, test_case, error_codes, port_number, gpio_mask, value, function_index=None,
                device_index=None, port_index=None):
            """
            Process ``WriteGroup``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param port_number: Port Number
            :type port_number: ``int | HexList``
            :param gpio_mask: Gpio Mask
            :type gpio_mask: ``int | HexList``
            :param value: Value
            :type value: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_1803_index, feature_1803, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1803.write_group_cls(
                device_index=device_index,
                feature_index=feature_1803_index,
                port_number=HexList(port_number),
                gpio_mask=HexList(gpio_mask),
                value=HexList(value))

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def write_group_and_check_error

        @classmethod
        def read_group_out(cls, test_case, port_number=None, gpio_mask=None, device_index=None, port_index=None,
                           software_id=None, padding=None):
            """
            Process ``ReadGroupOut``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param port_number: Port Number - OPTIONAL
            :type port_number: ``int | HexList | None``
            :param gpio_mask: Gpio Mask - OPTIONAL
            :type gpio_mask: ``int | HexList | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: ReadGroupOutResponse (if not error)
            :rtype: ``ReadGroupOutResponseV1``
            """
            feature_1803_index, feature_1803, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1803.read_group_out_cls(
                device_index=device_index,
                feature_index=feature_1803_index,
                port_number=HexList(port_number),
                gpio_mask=HexList(gpio_mask))

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
                response_class_type=feature_1803.read_group_out_response_cls)
        # end def read_group_out

        @classmethod
        def read_group_out_and_check_error(
                cls, test_case, error_codes, port_number=None, gpio_mask=None, function_index=None,
                device_index=None, port_index=None):
            """
            Process ``ReadGroupOut``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param port_number: Port Number - OPTIONAL
            :type port_number: ``int | HexList | None``
            :param gpio_mask: Gpio Mask - OPTIONAL
            :type gpio_mask: ``int | HexList | None``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_1803_index, feature_1803, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1803.read_group_out_cls(
                device_index=device_index,
                feature_index=feature_1803_index,
                port_number=HexList(port_number),
                gpio_mask=HexList(gpio_mask))

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def read_group_out_and_check_error
    # end class HIDppHelper
# end class GpioAccessTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
