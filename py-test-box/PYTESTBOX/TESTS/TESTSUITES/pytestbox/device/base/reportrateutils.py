#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.base.reportrateutils
:brief: Helpers for ``ReportRate`` feature
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2022/04/22
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.reportrate import GetReportRateListResponse
from pyhid.hidpp.features.gaming.reportrate import GetReportRateResponse
from pyhid.hidpp.features.gaming.reportrate import ReportRate
from pyhid.hidpp.features.gaming.reportrate import ReportRateFactory
from pyhid.hidpp.features.gaming.reportrate import SetReportRateResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ReportRateTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``ReportRate`` feature
    """

    class GetReportRateListResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``GetReportRateList`` response
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetReportRateListResponse`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "report_rate_list": (
                    cls.check_report_rate_list,
                    Numeral(test_case.f.PRODUCT.FEATURES.GAMING.REPORT_RATE.F_ReportRateList))
            }
        # end def get_default_check_map

        @staticmethod
        def check_report_rate_list(test_case, response, expected):
            """
            Check report_rate_list field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetReportRateListResponse to check
            :type response: ``GetReportRateListResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="ReportRateList shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.report_rate_list),
                msg="The report_rate_list parameter differs "
                    f"(expected:{expected}, obtained:{response.report_rate_list})")
        # end def check_report_rate_list
    # end class GetReportRateListResponseChecker

    class GetReportRateResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``GetReportRate`` response
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetReportRateResponse`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "report_rate": (
                    cls.check_report_rate,
                    int(test_case.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.OOB_PROFILES.F_ReportRate[0]))
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
                msg="The report_rate parameter differs "
                    f"(expected:{expected}, obtained:{response.report_rate})")
        # end def check_report_rate
    # end class GetReportRateResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=ReportRate.FEATURE_ID, factory=ReportRateFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_report_rate_list(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetReportRateList``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetReportRateListResponse
            :rtype: ``GetReportRateListResponse``
            """
            feature_8060_index, feature_8060, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8060.get_report_rate_list_cls(
                device_index=device_index,
                feature_index=feature_8060_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8060.get_report_rate_list_response_cls)
            return response
        # end def get_report_rate_list

        @classmethod
        def get_report_rate(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetReportRate``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetReportRateResponse
            :rtype: ``GetReportRateResponse``
            """
            feature_8060_index, feature_8060, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8060.get_report_rate_cls(
                device_index=device_index,
                feature_index=feature_8060_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8060.get_report_rate_response_cls)
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
            feature_8060_index, feature_8060, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8060.set_report_rate_cls(
                device_index=device_index,
                feature_index=feature_8060_index,
                report_rate=HexList(report_rate))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8060.set_report_rate_response_cls)
            return response
        # end def set_report_rate
    # end class HIDppHelper

    @classmethod
    def get_default_report_rate_list(cls, test_case):
        """
        Get default report rate list

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: Supported default report rate list
        :rtype: ``list[int]``
        """
        report_rate_list = test_case.f.PRODUCT.FEATURES.GAMING.REPORT_RATE.F_ReportRateList
        supported_report_rate_list = []
        report_rate_start = 1
        report_rate_end = 9
        for report_rate in range(report_rate_start, report_rate_end):
            if report_rate_list & 0x01:
                supported_report_rate_list.append(report_rate)
            # end if
            report_rate_list >>= 1
        # end for
        return supported_report_rate_list
    # end def get_default_report_rate_list
# end class ReportRateTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
