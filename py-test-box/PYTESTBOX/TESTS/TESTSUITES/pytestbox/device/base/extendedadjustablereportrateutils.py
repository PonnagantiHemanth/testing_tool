#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.base.extendedadjustablereportrateutils
:brief: Helpers for ``ExtendedAdjustableReportRate`` feature
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/05/11
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pychannel.channelinterfaceclasses import LogitechProtocol
from pychannel.throughreceiverchannel import ThroughReceiverChannel
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import ExtendedAdjustableReportRate
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import ExtendedAdjustableReportRateFactory
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytransport.usb.usbconstants import LogitechReceiverProductId


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ExtendedAdjustableReportRateTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``ExtendedAdjustableReportRate`` feature
    """

    class ReportRateListChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``ReportRateList``
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
            config = test_case.f.PRODUCT.FEATURES.GAMING.EXTENDED_ADJUSTABLE_REPORT_RATE
            test_case.assertNotNone(
                config.F_SupportedReportRateList,
                msg="Configuration shall be (a) defined in the DUT settings (b) passed as an argument")
            connection_type_index = ExtendedAdjustableReportRateTestUtils.get_current_connection_type_index(test_case)
            report_rate_list = HexList(config.F_SupportedReportRateList[connection_type_index])
            return cls.get_check_map(report_rate_list)
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, report_rate_list):
            """
            Get the check methods and expected values for a report rate list

            :param report_rate_list: Report rate list
            :type report_rate_list: ``HexList``

            :return: Check map
            :rtype: ``dict``
            """
            return {
                "reserved_0": (
                    cls.check_reserved_0, 0),
                "rate_8khz": (
                    cls.check_rate_8khz,
                    report_rate_list.testBit(ExtendedAdjustableReportRate.ReportRateList.POS.RATE_8KHZ)),
                "rate_4khz": (
                    cls.check_rate_4khz,
                    report_rate_list.testBit(ExtendedAdjustableReportRate.ReportRateList.POS.RATE_4KHZ)),
                "rate_2khz": (
                    cls.check_rate_2khz,
                    report_rate_list.testBit(ExtendedAdjustableReportRate.ReportRateList.POS.RATE_2KHZ)),
                "rate_1khz": (
                    cls.check_rate_1khz,
                    report_rate_list.testBit(ExtendedAdjustableReportRate.ReportRateList.POS.RATE_1KHZ)),
                "rate_500hz": (
                    cls.check_rate_500hz,
                    report_rate_list.testBit(ExtendedAdjustableReportRate.ReportRateList.POS.RATE_500HZ)),
                "rate_250hz": (
                    cls.check_rate_250hz,
                    report_rate_list.testBit(ExtendedAdjustableReportRate.ReportRateList.POS.RATE_250HZ)),
                "rate_125hz": (
                    cls.check_rate_125hz,
                    report_rate_list.testBit(ExtendedAdjustableReportRate.ReportRateList.POS.RATE_125HZ)),
            }
        # end def get_check_map

        @staticmethod
        def check_reserved_0(test_case, bitmap, expected):
            """
            Check reserved_0 field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: ReportRateList to check
            :type bitmap: ``ReportRateList``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved_0),
                msg=f"The reserved_0 parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.reserved_0})")
        # end def check_reserved_0

        @staticmethod
        def check_rate_8khz(test_case, bitmap, expected):
            """
            Check rate_8khz field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: ReportRateList to check
            :type bitmap: ``ReportRateList``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="Rate8KHz shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.rate_8khz),
                msg=f"The rate_8khz parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.rate_8khz})")
        # end def check_rate_8khz

        @staticmethod
        def check_rate_4khz(test_case, bitmap, expected):
            """
            Check rate_4khz field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: ReportRateList to check
            :type bitmap: ``ReportRateList``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="Rate4KHz shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.rate_4khz),
                msg=f"The rate_4khz parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.rate_4khz})")
        # end def check_rate_4khz

        @staticmethod
        def check_rate_2khz(test_case, bitmap, expected):
            """
            Check rate_2khz field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: ReportRateList to check
            :type bitmap: ``ReportRateList``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="Rate2KHz shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.rate_2khz),
                msg=f"The rate_2khz parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.rate_2khz})")
        # end def check_rate_2khz

        @staticmethod
        def check_rate_1khz(test_case, bitmap, expected):
            """
            Check rate_1khz field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: ReportRateList to check
            :type bitmap: ``ReportRateList``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="Rate1KHz shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.rate_1khz),
                msg=f"The rate_1khz parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.rate_1khz})")
        # end def check_rate_1khz

        @staticmethod
        def check_rate_500hz(test_case, bitmap, expected):
            """
            Check rate_500hz field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: ReportRateList to check
            :type bitmap: ``ReportRateList``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="Rate500Hz shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.rate_500hz),
                msg=f"The rate_500hz parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.rate_500hz})")
        # end def check_rate_500hz

        @staticmethod
        def check_rate_250hz(test_case, bitmap, expected):
            """
            Check rate_250hz field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: ReportRateList to check
            :type bitmap: ``ReportRateList``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="Rate250Hz shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.rate_250hz),
                msg=f"The rate_250hz parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.rate_250hz})")
        # end def check_rate_250hz

        @staticmethod
        def check_rate_125hz(test_case, bitmap, expected):
            """
            Check rate_125hz field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: ReportRateList to check
            :type bitmap: ``ReportRateList``
            :param expected: Expected value
            :type expected: ``bool``
            """
            test_case.assertNotNone(
                expected, msg="Rate125Hz shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.rate_125hz),
                msg=f"The rate_125hz parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.rate_125hz})")
        # end def check_rate_125hz
    # end class ReportRateListChecker

    class GetDeviceCapabilitiesResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetDeviceCapabilitiesResponse``
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
                "report_rate_list": (
                    cls.check_report_rate_list,
                    ExtendedAdjustableReportRateTestUtils.ReportRateListChecker.get_default_check_map(test_case))
            }
        # end def get_default_check_map

        @staticmethod
        def check_report_rate_list(test_case, message, expected):
            """
            Check ``report_rate_list``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: GetDeviceCapabilitiesResponse to check
            :type message: ``GetDeviceCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            ExtendedAdjustableReportRateTestUtils.ReportRateListChecker.check_fields(
                test_case, message.report_rate_list, ExtendedAdjustableReportRate.ReportRateList, expected)
        # end def check_report_rate_list
    # end class GetDeviceCapabilitiesResponseChecker

    class GetActualReportRateListResponseChecker(GetDeviceCapabilitiesResponseChecker):
        """
        Define Helper to check ``GetActualReportRateListResponse``
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
            config = test_case.f.PRODUCT.FEATURES.GAMING.EXTENDED_ADJUSTABLE_REPORT_RATE
            test_case.assertNotNone(
                config.F_SupportedReportRateList,
                msg="Configuration shall be (a) defined in the DUT settings (b) passed as an argument")

            connection_type_index = ExtendedAdjustableReportRateTestUtils.get_current_connection_type_index(test_case)
            report_rate_list = HexList(config.F_SupportedReportRateList[connection_type_index])
            if isinstance(test_case.current_channel, ThroughReceiverChannel):
                channel_rate_list = HexList(ExtendedAdjustableReportRateTestUtils.get_channel_report_rate_list(
                    test_case.current_channel.receiver_channel))
                report_rate_list &= channel_rate_list
            # end if
            return {
                "report_rate_list": (
                    cls.check_report_rate_list,
                    ExtendedAdjustableReportRateTestUtils.ReportRateListChecker.get_check_map(report_rate_list))
            }
        # end def get_default_check_map
    # end class GetActualReportRateListResponseChecker

    class GetReportRateResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetReportRateResponse``
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
            config = test_case.f.PRODUCT.FEATURES.GAMING.EXTENDED_ADJUSTABLE_REPORT_RATE
            test_case.assertNotNone(
                config.F_SupportedReportRateList,
                msg="Configuration shall be (a) defined in the DUT settings (b) passed as an argument")

            # Compute the highest report rate supported by the device
            highest_report_rate = ExtendedAdjustableReportRateTestUtils.get_highest_report_rate(test_case)

            return {
                "report_rate": (
                    cls.check_report_rate, highest_report_rate)
            }
        # end def get_default_check_map

        @staticmethod
        def check_report_rate(test_case, response, expected):
            """
            Check report_rate field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetReportRateResponse to check
            :type response: ``GetReportRateResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="ReportRate shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.report_rate),
                msg=f"The report_rate parameter differs "
                    f"(expected:{expected}, obtained:{response.report_rate})")
        # end def check_report_rate
    # end class GetReportRateResponseChecker

    class SetReportRateResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``SetReportRateResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            """

            return {}
        # end def get_default_check_map
    # end class SetReportRateResponseChecker

    class ReportRateInfoEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``RerportRateInfoEvent``
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
            connection_type_index = ExtendedAdjustableReportRateTestUtils.get_current_connection_type_index(test_case)

            # Compute the highest report rate supported by the device
            highest_report_rate = ExtendedAdjustableReportRateTestUtils.get_highest_report_rate(test_case)

            return {
                "connection_type": (cls.check_connection_type, connection_type_index),
                "report_rate": (cls.check_report_rate, highest_report_rate)
            }
        # end def get_default_check_map

        @staticmethod
        def check_connection_type(test_case, message, expected):
            """
            Check connection type field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: ReportRateInfoEvent to check
            :type message: ``ReportRateInfoEvent``
            :param expected: Expected value
            "type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(message.connection_type),
                msg=f"The connection_type parameter differs "
                    f"(expected:{expected}, obtained:{message.report_rate})")
        # end def check_connection_type

        @staticmethod
        def check_report_rate(test_case, message, expected):
            """
            Check report_rate field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: GetReportRateResponse to check
            :type message: ``GetReportRateResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="ReportRate shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(message.report_rate),
                msg=f"The report_rate parameter differs "
                    f"(expected:{expected}, obtained:{message.report_rate})")
        # end def check_report_rate
    # end class ReportRateInfoEventChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=ExtendedAdjustableReportRate.FEATURE_ID,
                           factory=ExtendedAdjustableReportRateFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_device_capabilities(cls, test_case, connection_type, device_index=None, port_index=None):
            """
            Process ``GetDeviceCapabilities``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param connection_type: Connection Type 
            :type connection_type: ``int`` or ``HexList`` or ``ExtendedAdjustableReportRate.ConnectionType``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetDeviceCapabilitiesResponse
            :rtype: ``GetDeviceCapabilitiesResponse``
            """
            feature_8061_index, feature_8061, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8061.get_device_capabilities_cls(
                device_index=device_index,
                feature_index=feature_8061_index,
                connection_type=HexList(connection_type))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8061.get_device_capabilities_response_cls)
            return response
        # end def get_device_capabilities

        @classmethod
        def get_actual_report_rate_list(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetActualReportRateList``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetActualReportRateListResponse
            :rtype: ``GetActualReportRateListResponse``
            """
            feature_8061_index, feature_8061, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8061.get_actual_report_rate_list_cls(
                device_index=device_index,
                feature_index=feature_8061_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8061.get_actual_report_rate_list_response_cls)
            return response
        # end def get_actual_report_rate_list

        @classmethod
        def get_report_rate(cls, test_case, connection_type, device_index=None, port_index=None):
            """
            Process ``GetReportRate``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param connection_type: Connection Type 
            :type connection_type: ``int`` or ``HexList`` or ``ExtendedAdjustableReportRate.ConnectionType``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetReportRateResponse
            :rtype: ``GetReportRateResponse``
            """
            feature_8061_index, feature_8061, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8061.get_report_rate_cls(
                device_index=device_index,
                feature_index=feature_8061_index,
                connection_type=HexList(connection_type))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8061.get_report_rate_response_cls)
            return response
        # end def get_report_rate

        @classmethod
        def set_report_rate(cls, test_case, report_rate, device_index=None, port_index=None):
            """
            Process ``SetReportRate``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param report_rate: Report Rate
            :type report_rate: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetReportRateResponse
            :rtype: ``SetReportRateResponse``
            """
            feature_8061_index, feature_8061, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8061.set_report_rate_cls(
                device_index=device_index,
                feature_index=feature_8061_index,
                report_rate=HexList(report_rate))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8061.set_report_rate_response_cls)
            return response
        # end def set_report_rate

        @classmethod
        def report_rate_info_event(cls, test_case, timeout=2, check_first_message=True, allow_no_message=False,
                                   skip_error_message=False):
            """
            Process ``ReportRateInfoEvent``: get notification from event queue

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

            :return: ReportRateInfoEvent
            :rtype: ``ReportRateInfoEvent``
            """
            _, feature_8061, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_8061.report_rate_info_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def report_rate_info_event
    # end class HIDppHelper

    @staticmethod
    def get_supported_rate_list(test_case):
        """
        Get the report rates that are supported by the device under test

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBastTestCase``

        :return: report rate supported by the device under test
        :rtype: ``list[int]``
        """
        config = test_case.f.PRODUCT.FEATURES.GAMING.EXTENDED_ADJUSTABLE_REPORT_RATE
        connection_type_index = ExtendedAdjustableReportRateTestUtils.get_current_connection_type_index(test_case)
        settings = HexList(config.F_SupportedReportRateList[connection_type_index])
        return [i for i in range(len(settings * 8)) if settings.testBit(i)]
    # end def get_supported_rate_list

    @staticmethod
    def get_unsupported_report_rate(test_case):
        """
        Get the report rates that are not supported by the device under test

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: report rate not supported by the device under test
        :rtype: ``list[int]``
        """
        return [report_rate for report_rate in range(256) if report_rate
                not in ExtendedAdjustableReportRateTestUtils.get_supported_rate_list(test_case)]
    # end def get_unsupported_report_rate

    @staticmethod
    def get_highest_report_rate(test_case):
        """
        Get the highest report rate of current connection type that are supported by the device

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: highest report rate or ``None`` if the capability bitmap is empty
        :rtype: ``int`` or ``None``

        :raise ``AssertionError``: If the SupportedReportRateList is None
        """
        config = test_case.f.PRODUCT.FEATURES.GAMING.EXTENDED_ADJUSTABLE_REPORT_RATE
        test_case.assertNotNone(
            config.F_SupportedReportRateList,
            msg="Configuration shall be (a) defined in the DUT settings (b) passed as an argument")

        connection_type_index = ExtendedAdjustableReportRateTestUtils.get_current_connection_type_index(test_case)
        report_rate_list = HexList(config.F_SupportedReportRateList[connection_type_index])
        if isinstance(test_case.current_channel, ThroughReceiverChannel):
            channel_rate_list = HexList(ExtendedAdjustableReportRateTestUtils.get_channel_report_rate_list(
                test_case.current_channel.receiver_channel))
            report_rate_list &= channel_rate_list
        # end if

        highest_report_rate = None
        for rate_index in range(ExtendedAdjustableReportRate.RATE._8_KHz, -1, -1):
            if report_rate_list.testBit(rate_index):
                highest_report_rate = rate_index
                break
            # end if
        # end for

        return highest_report_rate
    # end def get_highest_report_rate

    @staticmethod
    def get_none_default_wireless_report_rate(test_case):
        """
        Get the new wireless report rate of the OOB profile if the default wireless report rate equals the default wired
         report rate

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: report rate
        :rtype: ``int``
        """
        config = test_case.f.PRODUCT.FEATURES.GAMING.EXTENDED_ADJUSTABLE_REPORT_RATE
        oob_config = test_case.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.OOB_PROFILES

        wireless_settings = HexList(
            config.F_SupportedReportRateList[ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS])
        reversed_report_rate_list = [i for i in range(len(wireless_settings * 8) - 1, -1, -1) if
                                     wireless_settings.testBit(i)]

        if oob_config.F_ReportRateWireless[0] == oob_config.F_ReportRateWired[0]:
            for report_rate_wireless in reversed_report_rate_list:
                if report_rate_wireless != oob_config.F_ReportRateWired[0]:
                    return report_rate_wireless
                # end if
            # end for
        else:
            return int(oob_config.F_ReportRateWireless[0])
        # end if
    # end def get_none_default_wireless_report_rate

    @staticmethod
    def get_current_connection_type_index(test_case):
        """
        Get the device's current connection type index

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: The device's current connection type
        :rtype: ``ExtendedAdjustableReportRate.ConnectionType``
        """
        return ExtendedAdjustableReportRate.ConnectionType.WIRED \
            if test_case.config_manager.current_protocol == LogitechProtocol.USB \
            else ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS
    # end def get_current_connection_type_index

    @staticmethod
    def get_channel_report_rate_list(channel):
        """
        Get report list rate for given channel

        :param channel: Channel
        :type channel: `BaseCommunicationChannel`

        :return: Report rate list
        :rtype: `ExtendedAdjustableReportRate.ReportRateList`
        """
        report_rate = ExtendedAdjustableReportRate.ReportRateList(
            rate_8khz=False,
            rate_4khz=False,
            rate_2khz=False,
            rate_1khz=True,
            rate_500hz=True,
            rate_250hz=True,
            rate_125hz=True,
        )
        if channel is not None and channel.get_transport_id() in LogitechReceiverProductId.uhs_pids():
            report_rate.rate_2khz = True
            report_rate.rate_4khz = True
        # end if
        return report_rate
    # end def get_channel_report_rate_list

    @staticmethod
    def force_report_rate(test_case, report_rate):
        """
        Force the reporting rate to the given value using the 0x8061 HID++ feature API

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param report_rate: Report Rate
        :type report_rate: ``int`` or ``HexList``
        """
        host_mode = OnboardProfiles.Mode.HOST_MODE

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(test_case, "Get feature 0x8100 index")
        # --------------------------------------------------------------------------------------------------------------
        _, feature_8100, _, _ = OnboardProfilesTestUtils.HIDppHelper.get_parameters(test_case)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case, f"Send SetOnboardMode request with onboardMode = {host_mode} (host mode)")
        # --------------------------------------------------------------------------------------------------------------
        response = OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(test_case=test_case, onboard_mode=host_mode)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case, "Check no error returned")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.MessageChecker.check_fields(
            test_case=test_case, message=response,
            expected_cls=feature_8100.set_onboard_mode_response_cls, check_map={})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(test_case, "Get feature 0x8061 index")
        # --------------------------------------------------------------------------------------------------------------
        _, feature_8061, _, _ = ExtendedAdjustableReportRateTestUtils.HIDppHelper.get_parameters(test_case)

        # Add a loop to ensure that the DUT has successfully transitioned to the new report rate.
        # We noticed that occasionally, our Bazooka2 sample was resetting and reverting to the default value.
        # Loop counter = 4 is an empirical value based on experience
        loop_counter = 4
        for index in range(loop_counter):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, f"Send SetReportRate request with report rate = {report_rate}")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableReportRateTestUtils.HIDppHelper.set_report_rate(test_case=test_case,
                                                                              report_rate=report_rate)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, "Wait ReportRateInfoEvent response")
            # ----------------------------------------------------------------------------------------------------------
            response = ExtendedAdjustableReportRateTestUtils.HIDppHelper.report_rate_info_event(
                test_case=test_case, check_first_message=False)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(test_case, "Check ReportRateInfoEvent response inputs fields are as expected")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableReportRateTestUtils.ReportRateInfoEventChecker
            check_map = checker.get_default_check_map(test_case=test_case)
            check_map.update({
                "report_rate": (checker.check_report_rate, report_rate)
            })
            checker.check_fields(test_case, response, feature_8061.report_rate_info_event_cls, check_map)

            # The DUT could reset after receiving the previous SetReportRate request
            message = ChannelUtils.get_only(
                test_case=test_case, queue_name=HIDDispatcher.QueueName.EVENT, timeout=3,
                class_type=WirelessDeviceStatusBroadcastEvent, check_first_message=False, allow_no_message=True)
            if message is None:
                break
            elif index == (loop_counter - 1):
                raise Exception(f'Report Rate could not be configured at {report_rate}')
            else:
                # --------------------------------------------------------------------------------------------------
                LogHelper.log_step(test_case, f"Send SetOnboardMode request with onboardMode = host mode")
                # --------------------------------------------------------------------------------------------------
                OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(
                    test_case=test_case, onboard_mode=OnboardProfiles.Mode.HOST_MODE)

                ChannelUtils.clean_messages(test_case=test_case, queue_name=HIDDispatcher.QueueName.EVENT,
                                            class_type=(WirelessDeviceStatusBroadcastEvent,
                                                        feature_8061.report_rate_info_event_cls))
            # end if
        # end for
    # end def force_report_rate

    @classmethod
    def set_report_rate(cls, test_case, connection_type, report_rate):
        """
        Set the report rate of the device under test to the given value if not already the default

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param connection_type: Connection type index
        :type connection_type: ``ExtendedAdjustableReportRate.ConnectionType``
        :param report_rate: Report rate
        :type report_rate: ``int`` or ``HexList``
        """
        default_report_rate = None
        config = test_case.f.PRODUCT.FEATURES.GAMING.EXTENDED_ADJUSTABLE_REPORT_RATE
        supported_report_rate_list = config.F_SupportedReportRateList
        if connection_type == ExtendedAdjustableReportRate.ConnectionType.WIRED:
            default_report_rate = config.F_DefaultReportRateWired
        elif connection_type == ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS:
            default_report_rate = config.F_DefaultReportRateWireless
        # end if
        if default_report_rate == report_rate:
            # Check if report_rate is the default report rate
            return
        elif config.F_Enabled and HexList(supported_report_rate_list[connection_type]).testBit(report_rate):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, f"Change the report rate to {report_rate}")
            # ----------------------------------------------------------------------------------------------------------
            test_case.post_requisite_reload_nvs = True
            cls.force_report_rate(test_case=test_case, report_rate=report_rate)
        else:
            raise ValueError(f"Unable to set reporting rate to {report_rate}, please ensure the setting is correct.")
        # end if
    # end def set_report_rate

# end class ExtendedAdjustableReportRateTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
