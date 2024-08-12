#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.base.changehostutils
:brief: Helpers for ``ChangeHost`` feature
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2021/12/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.changehost import ChangeHost
from pyhid.hidpp.features.common.changehost import ChangeHostFactory
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ChangeHostTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``ChangeHost`` feature
    """

    class GetHostInfoResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``GetHostInfo`` response
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetHostInfoResponse`` API
            By default, ``GetHostInfoResponseChecker`` is configured to check that the current host is 0.
            The tester shall overload the value if needed.

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "nb_host": (
                    cls.check_nb_host, test_case.f.PRODUCT.DEVICE.F_NbHosts),
                "curr_host": (
                    cls.check_curr_host, 0),
                "rsv": (
                    cls.check_rsv, 0),
                "flags": (
                    cls.check_flags, test_case.f.PRODUCT.FEATURES.COMMON.CHANGE_HOST.F_Flags)
            }
        # end def get_default_check_map

        @staticmethod
        def check_nb_host(test_case, response, expected):
            """
            Check nb_host field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetHostInfoResponse to check
            :type response: ``GetHostInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.nb_host)),
                msg=f"The nb_host parameter differs "
                    f"(expected:{expected}, obtained:{response.nb_host})")
        # end def check_nb_host

        @staticmethod
        def check_curr_host(test_case, response, expected):
            """
            Check curr_host field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetHostInfoResponse to check
            :type response: ``GetHostInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.curr_host)),
                msg=f"The curr_host parameter differs "
                    f"(expected:{expected}, obtained:{response.curr_host})")
        # end def check_curr_host

        @staticmethod
        def check_rsv(test_case, response, expected):
            """
            Check rsv field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetHostInfoResponse to check
            :type response: ``GetHostInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.rsv)),
                msg=f"The rsv parameter differs "
                    f"(expected:{expected}, obtained:{response.rsv})")

        # end def check_rsv

        @staticmethod
        def check_flags(test_case, response, expected):
            """
            Check flags field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetHostInfoResponse to check
            :type response: ``GetHostInfoResponse``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.flags),
                msg=f"The flags parameter differs "
                    f"(expected:{expected}, obtained:{response.flags})")
        # end def check_flags
    # end class GetHostInfoResponseChecker

    class GetCookiesResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``GetCookies`` response
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetCookiesResponse`` API

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "cookies": (
                    cls.check_cookies, None)
            }
        # end def get_default_check_map

        @staticmethod
        def check_cookies(test_case, response, expected):
            """
            Check cookies field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetCookiesResponse to check
            :type response: ``GetCookiesResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            cookies_list = get_cookie_list(response, test_case.f.PRODUCT.DEVICE.F_NbHosts)
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(cookies_list),
                msg=f"The cookies parameter differs "
                    f"(expected:{expected}, obtained:{cookies_list})")
        # end def check_cookies
    # end class GetCookiesResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=ChangeHost.FEATURE_ID, factory=ChangeHostFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_host_info(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetHostInfo``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetHostInfoResponse
            :rtype: ``GetHostInfoResponse``
            """
            feature_1814_index, feature_1814, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1814.get_host_info_cls(
                device_index, feature_1814_index)
            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.common_message_queue,
                response_class_type=test_case.feature_1814.get_host_info_response_cls)
            return response
        # end def get_host_info

        @classmethod
        def set_current_host(cls, test_case, host_index, device_index=None, port_index=None):
            """
            Process ``SetCurrentHost``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param host_index: index of host
            :type host_index: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetCurrentHostResponse
            :rtype: ``SetCurrentHostResponse``
            """
            feature_1814_index, feature_1814, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1814.set_current_host_cls(
                device_index, feature_1814_index,
                host_index=HexList(host_index))
            ChannelUtils.send_only(test_case=test_case, report=report)
            response = ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.COMMON,
                class_type=test_case.feature_1814.set_current_host_response_cls,
                check_first_message=False,
                allow_no_message=True)

            return response
        # end def set_current_host

        @classmethod
        def get_cookies(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetCookies``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetCookiesResponse
            :rtype: ``GetCookiesResponse``
            """
            feature_1814_index, feature_1814, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1814.get_cookies_cls(
                device_index, feature_1814_index)
            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.common_message_queue,
                response_class_type=test_case.feature_1814.get_cookies_response_cls)
            return response
        # end def get_cookies

        @classmethod
        def set_cookie(cls, test_case, host_index, cookie, device_index=None, port_index=None):
            """
            Process ``SetCookie``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param host_index: index of host
            :type host_index: ``int`` or ``HexList``
            :param cookie: cookie value for host
            :type cookie: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetCookieResponse
            :rtype: ``SetCookieResponse``
            """
            feature_1814_index, feature_1814, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1814.set_cookie_cls(
                device_index, feature_1814_index,
                host_index=HexList(host_index),
                cookie=HexList(cookie))
            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.common_message_queue,
                response_class_type=test_case.feature_1814.set_cookie_response_cls)
            return response
        # end def set_cookie
    # end class HIDppHelper
# end class ChangeHostTestUtils


def get_cookie_list(response, nb_host):
    """
    Extract cookie field from device response

    :param response: Response to Get cookie request
    :type response: ``GetCookiesResponse``
    :param nb_host: The number of hosts / Rf channels supported by the device
    :type nb_host: ``int``

    :return: the list of data byte for each host
    :rtype: ``list``
    """
    x = ('0' * (32 - len(str(response.cookies))) + str(response.cookies))[:nb_host * 2]
    cookie_list = [x[i:i + 2] for i in range(0, nb_host * 2, 2)]
    return cookie_list
# end def get_cookie_list

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
