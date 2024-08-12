#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.base.macrorecordkeyutils
:brief: Helpers for ``MacroRecordkey`` feature
:author: Zane Lu <zlu@logitech.com>
:date: 2023/11/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
# noinspection PyUnresolvedReferences
from pychannel.channelinterfaceclasses import BaseCommunicationChannel

from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.macrorecordkey import ButtonReportEvent
from pyhid.hidpp.features.gaming.macrorecordkey import MacroRecordkey
from pyhid.hidpp.features.gaming.macrorecordkey import MacroRecordkeyFactory
from pyhid.hidpp.features.gaming.macrorecordkey import SetLEDResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MacroRecordkeyTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``MacroRecordkey`` feature
    """

    class ButtonReportEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``ButtonReportEvent``
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
            config = test_case.f.PRODUCT.FEATURES.GAMING.MACRORECORD_KEY
            return {
                "mr_button_status": (cls.check_mr_button_status, None)
            }
        # end def get_default_check_map

        @staticmethod
        def check_mr_button_status(test_case, event, expected):
            """
            Check mr_button_status field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: ButtonReportEvent to check
            :type event: ``ButtonReportEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert mr_button_status that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The mr_button_status shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.mr_button_status),
                msg="The mr_button_status parameter differs from the one expected")
        # end def check_mr_button_status
    # end class ButtonReportEventChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case,
                           feature_id=MacroRecordkey.FEATURE_ID,
                           factory=MacroRecordkeyFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def set_led(cls, test_case, enabled, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``SetLED``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param enabled: enabled
            :type enabled: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: SetLEDResponse (if not error)
            :rtype: ``SetLEDResponse``
            """
            feature_8030_index, feature_8030, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8030.set_led_cls(
                device_index=device_index,
                feature_index=feature_8030_index,
                enabled=HexList(enabled))

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8030.set_led_response_cls)
        # end def set_led

        @classmethod
        def set_led_and_check_error(
                cls, test_case, error_codes, enabled, function_index=None, device_index=None,
                port_index=None):
            """
            Process ``SetLED``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param enabled: enabled
            :type enabled: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_8030_index, feature_8030, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8030.set_led_cls(
                device_index=device_index,
                feature_index=feature_8030_index,
                enabled=HexList(enabled))

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def set_led_and_check_error

        @classmethod
        def button_report_event(
                cls, test_case, timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``ButtonReportEvent``: get notification from event queue

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

            :return: ButtonReportEvent
            :rtype: ``ButtonReportEvent``
            """
            _, feature_8030, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_8030.button_report_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def button_report_event
    # end class HIDppHelper
# end class MacroRecordkeyTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
