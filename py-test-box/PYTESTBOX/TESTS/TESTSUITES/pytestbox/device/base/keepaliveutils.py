#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.base.KeepAliveutils
:brief: Helpers for ``KeepAlive`` feature
:author: Harish Kumar D <hd@logitech.com>
:date: 2024/01/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
# noinspection PyUnresolvedReferences
from pychannel.channelinterfaceclasses import BaseCommunicationChannel

from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.keepalive import GetTimeoutRangeResponse
from pyhid.hidpp.features.common.keepalive import KeepAlive
from pyhid.hidpp.features.common.keepalive import KeepAliveFactory
from pyhid.hidpp.features.common.keepalive import KeepAliveResponse
from pyhid.hidpp.features.common.keepalive import KeepAliveTimeoutEventV1
from pyhid.hidpp.features.common.keepalive import TerminateResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class KeepAliveTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``KeepAlive`` feature
    """

    class GetTimeoutRangeResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetTimeoutRangeResponse``
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
            config = test_case.f.PRODUCT.FEATURES.COMMON.KEEP_ALIVE
            return {
                "timeout_minimum": (cls.check_timeout_minimum, config.F_TimeoutMin),
                "timeout_maximum": (cls.check_timeout_maximum, config.F_TimeoutMax)
            }
        # end def get_default_check_map

        @staticmethod
        def check_timeout_minimum(test_case, response, expected):
            """
            Check timeout_minimum field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetTimeoutRangeResponse to check
            :type response: ``GetTimeoutRangeResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert timeout_minimum that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The timeout_minimum shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(Numeral(expected)),
                obtained=HexList(response.timeout_minimum),
                msg="The timeout_minimum parameter differs from the one expected")
        # end def check_timeout_minimum

        @staticmethod
        def check_timeout_maximum(test_case, response, expected):
            """
            Check timeout_maximum field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetTimeoutRangeResponse to check
            :type response: ``GetTimeoutRangeResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert timeout_maximum that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The timeout_minimum shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(Numeral(expected)),
                obtained=HexList(response.timeout_maximum),
                msg="The timeout_maximum parameter differs from the one expected")
        # end def check_timeout_maximum
    # end class GetTimeoutRangeResponseChecker

    class KeepAliveResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``KeepAliveResponse``
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
                "final_timeout": (cls.check_final_timeout, None)
            }
        # end def get_default_check_map

        @staticmethod
        def check_final_timeout(test_case, response, expected):
            """
            Check final_timeout field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: KeepAliveResponse to check
            :type response: ``KeepAliveResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert final_timeout that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The timeout_minimum shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.final_timeout),
                msg="The final_timeout parameter differs from the one expected")
        # end def check_final_timeout
    # end class KeepAliveResponseChecker

    class KeepAliveTimeoutEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``KeepAliveTimeoutEvent``
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
            config = test_case.f.PRODUCT.FEATURES.COMMON.KEEP_ALIVE
            version = test_case.config_manager.get_feature_version(config)
            if version in [cls.Version.ONE]:
                return {}
            # end if
            raise NotImplementedError(f"Version {version} is not implemented")
        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, event, expected):
            """
            Check reserved field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: KeepAliveTimeoutEvent to check
            :type event: ``KeepAliveTimeoutEventV1``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The timeout_minimum shall be defined in the DUT settings")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(event.reserved),
                msg="The reserved parameter differs from the one expected")
        # end def check_reserved
    # end class KeepAliveTimeoutEventChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case,
                           feature_id=KeepAlive.FEATURE_ID,
                           factory=KeepAliveFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_timeout_range(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetTimeoutRange``

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

            :return: GetTimeoutRangeResponse
            :rtype: ``GetTimeoutRangeResponse``
            """
            feature_0008_index, feature_0008, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_0008.get_timeout_range_cls(
                device_index=device_index,
                feature_index=feature_0008_index)

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
                response_class_type=feature_0008.get_timeout_range_response_cls)
        # end def get_timeout_range

        @classmethod
        def get_timeout_range_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``GetTimeoutRange``

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
            feature_0008_index, feature_0008, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_0008.get_timeout_range_cls(
                device_index=device_index,
                feature_index=feature_0008_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_timeout_range_and_check_error

        @classmethod
        def keep_alive(cls, test_case, requested_timeout, device_index=None, port_index=None, software_id=None,
                       padding=None):
            """
            Process ``KeepAlive``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param requested_timeout: Requested Timeout
            :type requested_timeout: ``HexList | int``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: KeepAliveResponse
            :rtype: ``KeepAliveResponse``
            """
            feature_0008_index, feature_0008, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_0008.keep_alive_cls(
                device_index=device_index,
                feature_index=feature_0008_index,
                requested_timeout=requested_timeout)

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
                response_class_type=feature_0008.keep_alive_response_cls)
        # end def keep_alive

        @classmethod
        def keep_alive_and_check_error(
                cls, test_case, error_codes, requested_timeout, function_index=None,
                device_index=None, port_index=None):
            """
            Process ``KeepAlive``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param requested_timeout: Requested Timeout
            :type requested_timeout: ``HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_0008_index, feature_0008, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_0008.keep_alive_cls(
                device_index=device_index,
                feature_index=feature_0008_index,
                requested_timeout=requested_timeout)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def keep_alive_and_check_error

        @classmethod
        def terminate(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``Terminate``

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

            :return: TerminateResponse
            :rtype: ``TerminateResponse``
            """
            feature_0008_index, feature_0008, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_0008.terminate_cls(
                device_index=device_index,
                feature_index=feature_0008_index)

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
                response_class_type=feature_0008.terminate_response_cls)
        # end def terminate

        @classmethod
        def terminate_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``Terminate``

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
            feature_0008_index, feature_0008, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_0008.terminate_cls(
                device_index=device_index,
                feature_index=feature_0008_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def terminate_and_check_error

        @classmethod
        def keep_alive_timeout_event(
                cls, test_case, timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``KeepAliveTimeoutEvent``: get notification from event queue

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

            :return: KeepAliveTimeoutEvent
            :rtype: ``KeepAliveTimeoutEvent``
            """
            _, feature_0008, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_0008.keep_alive_timeout_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def keep_alive_timeout_event
    # end class HIDppHelper
# end class KeepAliveTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
