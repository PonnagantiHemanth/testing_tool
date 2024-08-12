#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.base.configurabledeviceregistersutils
:brief: Helpers for ``ConfigurableDeviceRegisters`` feature
:author: Udayathilagan <uelamaran@logitech.com>
:date: 2024/05/08
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.configurabledeviceregisters import ConfigurableDeviceRegisters, SetRegisterValue
from pyhid.hidpp.features.common.configurabledeviceregisters import ConfigurableDeviceRegistersFactory
from pyhid.hidpp.features.common.configurabledeviceregisters import GetCapabilitiesResponse
from pyhid.hidpp.features.common.configurabledeviceregisters import GetRegisterInfoResponse
from pyhid.hidpp.features.common.configurabledeviceregisters import GetRegisterValueResponse
from pyhid.hidpp.features.common.configurabledeviceregisters import SetRegisterValueResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pychannel.throughreceiverchannel import ThroughEQuadReceiverChannel


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ConfigurableDeviceRegistersTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``ConfigurableDeviceRegisters`` feature
    """

    class GetCapabilitiesResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetCapabilitiesResponse``
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
            config = test_case.f.PRODUCT.FEATURES.COMMON.CONFIGURABLE_DEVICE_REGISTERS
            return {
                "reserved": (cls.check_reserved, 0),
                "capabilities": (cls.check_capabilities, config.F_Capabilities)
            }
        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponse``
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
        def check_capabilities(test_case, response, expected):
            """
            Check capabilities field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert capabilities that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The capabilities shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.capabilities),
                msg="The capabilities parameter differs from the one expected")
        # end def check_capabilities
    # end class GetCapabilitiesResponseChecker

    class GetRegisterInfoResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetRegisterInfoResponse``
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
                "configurable": (cls.check_configurable, 0),
                "supported": (cls.check_supported, 0),
                "register_size": (cls.check_register_size, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetRegisterInfoResponse to check
            :type response: ``GetRegisterInfoResponse``
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
        def check_configurable(test_case, response, expected):
            """
            Check configurable field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetRegisterInfoResponse to check
            :type response: ``GetRegisterInfoResponse``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert configurable that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The configurable shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.configurable),
                msg="The configurable parameter differs from the one expected")
        # end def check_configurable

        @staticmethod
        def check_supported(test_case, response, expected):
            """
            Check supported field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetRegisterInfoResponse to check
            :type response: ``GetRegisterInfoResponse``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert supported that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The supported shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.supported),
                msg="The supported parameter differs from the one expected")
        # end def check_supported

        @staticmethod
        def check_register_size(test_case, response, expected):
            """
            Check register_size field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetRegisterInfoResponse to check
            :type response: ``GetRegisterInfoResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert register_size that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The register_size shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.register_size),
                msg="The register_size parameter differs from the one expected")
        # end def check_register_size
    # end class GetRegisterInfoResponseChecker

    class GetRegisterValueResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetRegisterValueResponse``
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
                "register_value": (cls.check_register_value, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_register_value(test_case, response, expected):
            """
            Check register_value field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetRegisterValueResponse to check
            :type response: ``GetRegisterValueResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert register value that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The register_value shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.register_value),
                msg="The register_value parameter differs from the one expected")
        # end def check_register_value
    # end class GetRegisterValueResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case,
                           feature_id=ConfigurableDeviceRegisters.FEATURE_ID,
                           factory=ConfigurableDeviceRegistersFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_capabilities(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetCapabilities``

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

            :return: GetCapabilitiesResponse (if not error)
            :rtype: ``GetCapabilitiesResponse``
            """
            feature_180b_index, feature_180b, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_180b.get_capabilities_cls(
                device_index=device_index,
                feature_index=feature_180b_index)

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
                response_class_type=feature_180b.get_capabilities_response_cls)
        # end def get_capabilities

        @classmethod
        def get_capabilities_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``GetCapabilities``

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
            feature_180b_index, feature_180b, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_180b.get_capabilities_cls(
                device_index=device_index,
                feature_index=feature_180b_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_capabilities_and_check_error

        @classmethod
        def get_register_info(cls, test_case, register_id, device_index=None, port_index=None, software_id=None,
                              padding=None):
            """
            Process ``GetRegisterInfo``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param register_id: Register Id
            :type register_id: ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: GetRegisterInfoResponse (if not error)
            :rtype: ``GetRegisterInfoResponse``
            """
            feature_180b_index, feature_180b, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_180b.get_register_info_cls(
                device_index=device_index,
                feature_index=feature_180b_index,
                register_id=register_id)

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
                response_class_type=feature_180b.get_register_info_response_cls)
        # end def get_register_info

        @classmethod
        def get_register_info_and_check_error(
                cls, test_case, error_codes, register_id, function_index=None, device_index=None,
                port_index=None):
            """
            Process ``GetRegisterInfo``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param register_id: Register Id
            :type register_id: ``HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_180b_index, feature_180b, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_180b.get_register_info_cls(
                device_index=device_index,
                feature_index=feature_180b_index,
                register_id=register_id)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_register_info_and_check_error

        @classmethod
        def get_register_value(cls, test_case, register_id, device_index=None, port_index=None, software_id=None,
                               padding=None, register_size=None):
            """
            Process ``GetRegisterValue``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param register_id: Register Id
            :type register_id: ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``
            :param register_size: Register size - OPTIONAL
            :type register_size: ``int | None``

            :return: GetRegisterValueResponse (if not error)
            :rtype: ``GetRegisterValueResponse``
            """
            feature_180b_index, feature_180b, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_180b.get_register_value_cls(
                device_index=device_index,
                feature_index=feature_180b_index,
                register_id=register_id)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_180b.get_register_value_response_cls)
            return GetRegisterValueResponse.from_hex_list(HexList(response),
                                                          register_id=Numeral(register_id),
                                                          register_size=register_size)
        # end def get_register_value

        @classmethod
        def get_register_value_and_check_error(
                cls, test_case, error_codes, register_id, function_index=None, device_index=None,
                port_index=None):
            """
            Process ``GetRegisterValue``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param register_id: Register Id
            :type register_id: ``HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_180b_index, feature_180b, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_180b.get_register_value_cls(
                device_index=device_index,
                feature_index=feature_180b_index,
                register_id=register_id)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_register_value_and_check_error

        @classmethod
        def set_register_value(cls, test_case, register_id, register_value, register_size=None, device_index=None,
                               port_index=None, software_id=None):
            """
            Process ``SetRegisterValue``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param register_id: Register Id
            :type register_id: ``int``
            :param register_value: Register Value
            :type register_value: ``HexList``
            :param register_size: Register Size - OPTIONAL
            :type register_size: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            """
            feature_180b_index, feature_180b, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_180b.set_register_value_cls(
                device_index=device_index,
                feature_index=feature_180b_index,
                register_id=register_id,
                register_value=register_value,
                register_size=register_size)

            if software_id is not None:
                report.software_id = software_id
            # end if

            report = SetRegisterValue.register_value_based_on_size(report,
                                                                   register_id=register_id,
                                                                   register_value=register_value,
                                                                   register_size=None)
            ChannelUtils.send_only(
                test_case=test_case,
                report=report)
            if not isinstance(test_case.current_channel, ThroughEQuadReceiverChannel):
                CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(test_case=test_case)
            # end if
        # end def set_register_value

        @classmethod
        def set_register_value_and_check_error(
                cls, test_case, error_codes, register_id, register_value, function_index=None,
                device_index=None, port_index=None):
            """
            Process ``SetRegisterValue``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param register_id: Register Id
            :type register_id: ``HexList``
            :param register_value: Register Value
            :type register_value: ``HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_180b_index, feature_180b, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_180b.set_register_value_cls(
                device_index=device_index,
                feature_index=feature_180b_index,
                register_id=register_id,
                register_value=register_value)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def set_register_value_and_check_error
    # end class HIDppHelper
# end class ConfigurableDeviceRegistersTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
