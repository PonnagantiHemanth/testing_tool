#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.base.gaminggkeysutils
:brief: Helpers for ``GamingGKeys`` feature
:author: Gautham S B <gsb@logitech.com>
:date: 2023/11/17
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.gaminggkeys import EnableSoftwareControlResponse
from pyhid.hidpp.features.gaming.gaminggkeys import GamingGKeys
from pyhid.hidpp.features.gaming.gaminggkeys import GamingGKeysFactory
from pyhid.hidpp.features.gaming.gaminggkeys import GetCountResponse
from pyhid.hidpp.features.gaming.gaminggkeys import GetPhysicalLayoutResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class GamingGKeysTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``GamingGKeys`` feature
    """

    class GetCountResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetCountResponse``
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
            config = test_case.f.PRODUCT.FEATURES.GAMING.GAMING_G_KEYS
            return {
                "nbbuttons": (cls.check_nbbuttons, None)
            }
        # end def get_default_check_map

        @staticmethod
        def check_nbbuttons(test_case, response, expected):
            """
            Check nbbuttons field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetCountResponse to check
            :type response: ``GetCountResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert nbbuttons that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The nbbuttons shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.nbbuttons),
                msg="The nbbuttons parameter differs from the one expected")
        # end def check_nbbuttons
    # end class GetCountResponseChecker

    class GetPhysicalLayoutResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetPhysicalLayoutResponse``
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
            config = test_case.f.PRODUCT.FEATURES.GAMING.GAMING_G_KEYS
            return {
                "gkeylayout": (cls.check_g_key_layout, None)
            }
        # end def get_default_check_map

        @staticmethod
        def check_g_key_layout(test_case, response, expected):
            """
            Check gkeylayout field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetPhysicalLayoutResponse to check
            :type response: ``GetPhysicalLayoutResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert gkeylayout that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The gkeylayout shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.gkeylayout),
                msg="The gkeylayout parameter differs from the one expected")
        # end def check_gkeylayout
    # end class GetPhysicalLayoutResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case,
                           feature_id=GamingGKeys.FEATURE_ID,
                           factory=GamingGKeysFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_count(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetCount``

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

            :return: GetCountResponse (if not error)
            :rtype: ``GetCountResponse``
            """
            feature_8010_index, feature_8010, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8010.get_count_cls(
                device_index=device_index,
                feature_index=feature_8010_index)

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
                response_class_type=feature_8010.get_count_response_cls)
        # end def getcount

        @classmethod
        def get_count_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``GetCount``

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
            feature_8010_index, feature_8010, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8010.get_count_cls(
                device_index=device_index,
                feature_index=feature_8010_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def getcount_and_check_error

        @classmethod
        def get_physical_layout(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetPhysicalLayout``

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

            :return: GetPhysicalLayoutResponse (if not error)
            :rtype: ``GetPhysicalLayoutResponse``
            """
            feature_8010_index, feature_8010, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8010.get_physical_layout_cls(
                device_index=device_index,
                feature_index=feature_8010_index)

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
                response_class_type=feature_8010.get_physical_layout_response_cls)
        # end def getphysicallayout

        @classmethod
        def get_physical_layout_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``GetPhysicalLayout``

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
            feature_8010_index, feature_8010, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8010.get_physical_layout_cls(
                device_index=device_index,
                feature_index=feature_8010_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def getphysicallayout_and_check_error

        @classmethod
        def enable_software_control(cls, test_case, enable, device_index=None, port_index=None, software_id=None,
                                    padding=None):
            """
            Process ``EnableSoftwareControl``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param enable: enable
            :type enable: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: EnableSoftwareControlResponse (if not error)
            :rtype: ``EnableSoftwareControlResponse``
            """
            feature_8010_index, feature_8010, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8010.enable_software_control_cls(
                device_index=device_index,
                feature_index=feature_8010_index,
                enable=HexList(enable))

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
                response_class_type=feature_8010.enable_software_control_response_cls)
        # end def enablesoftwarecontrol

        @classmethod
        def enable_software_control_and_check_error(
                cls, test_case, error_codes, enable, function_index=None, device_index=None,
                port_index=None):
            """
            Process ``EnableSoftwareControl``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param enable: enable
            :type enable: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_8010_index, feature_8010, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8010.enable_software_control_cls(
                device_index=device_index,
                feature_index=feature_8010_index,
                enable=HexList(enable))

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def enablesoftwarecontrol_and_check_error
    # end class HIDppHelper
# end class GamingGKeysTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
