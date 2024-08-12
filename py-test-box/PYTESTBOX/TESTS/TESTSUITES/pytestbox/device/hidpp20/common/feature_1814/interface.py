#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.common.feature_1814.interface
:brief: HID++ 2.0 ``ChangeHost`` interface test suite
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2021/12/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pylibrary.tools.hexlist import HexList
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.changehostutils import ChangeHostTestUtils
from pytestbox.device.base.changehostutils import get_cookie_list
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.hidpp20.common.feature_1814.changehost import ChangeHostTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Kevin Dayet"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ChangeHostInterfaceTestCase(ChangeHostTestCase):
    """
    Validate ``ChangeHost`` interface test cases
    """

    @features("Feature1814")
    @level("Interface")
    def test_get_host_info_interface(self):
        """
        Validate ``GetHostInfo`` interface
        """
        nb_host = self.f.PRODUCT.DEVICE.F_NbHosts
        curr_host = HexList(0x0)
        rsv = HexList(0x0)
        flags = self.f.PRODUCT.FEATURES.COMMON.CHANGE_HOST.F_Flags
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetHostInfo request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1814.get_host_info_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1814_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1814.get_host_info_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetHostInfoResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ChangeHostTestUtils.GetHostInfoResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
            "nb_host": (checker.check_nb_host, nb_host),
            "curr_host": (checker.check_curr_host, curr_host),
            "rsv": (checker.check_rsv, rsv),
            "flags": (checker.check_flags, flags),
        })
        checker.check_fields(self, response, self.feature_1814.get_host_info_response_cls, check_map)

        self.testCaseChecked("INT_1814_0001", _AUTHOR)
    # end def test_get_host_info_interface

    # TODO : Not the same than original code ?
    @features("Feature1814")
    @level("Interface")
    def test_set_current_host_interface(self):
        """
        Validate ``SetCurrentHost`` interface
        """
        host_index = HexList(0x0)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetCurrentHost request with host_index=0")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1814.set_current_host_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1814_index,
            host_index=host_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1814.set_current_host_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetCurrentHostResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
        }
        checker.check_fields(self, response, self.feature_1814.set_current_host_response_cls, check_map)

        self.testCaseChecked("INT_1814_0002", _AUTHOR)
    # end def test_set_current_host_interface

    @features("Feature1814")
    @level("Interface")
    def test_get_cookies_interface(self):
        """
        Validate ``GetCookies`` interface

        Change Host
         cookie[0], cookie[1], ..., cookie[nbHost-1] [2]GetCookies
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetCookies request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1814.get_cookies_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1814_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1814.get_cookies_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetCookies.cookie[0..nbHost-1] value")
        # --------------------------------------------------------------------------------------------------------------
        cookies_list = get_cookie_list(response, self.f.PRODUCT.DEVICE.F_NbHosts)
        for i in range(self.f.PRODUCT.DEVICE.F_NbHosts):
            self.assertEqual(expected=True,
                             obtained=int(cookies_list[i], 16) in range(0x100),
                             msg='The cookies[' + str(i) + '] parameter differs from the one expected')
        # end for

        self.testCaseChecked("INT_1814_0003", _AUTHOR)
    # end def test_get_cookies_interface

    @features("Feature1814")
    @level("Interface")
    def test_set_cookie_interface(self):
        """
        Validate ``SetCookie`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetCookie request with hostIndex=0 cookie=0")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1814.set_cookie_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1814_index,
            host_index=0,
            cookie=0)
        ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1814.set_cookie_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetCookies request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1814.get_cookies_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1814_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1814.get_cookies_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate GetCookies.cookie[0] value")
        # --------------------------------------------------------------------------------------------------------------
        cookies_list = get_cookie_list(response, self.f.PRODUCT.DEVICE.F_NbHosts)
        self.assertEqual(expected=0,
                         obtained=int(cookies_list[0], 16),
                         msg='The cookies[0] parameter differs from the one expected')

        self.testCaseChecked("INT_1814_0004", _AUTHOR)
    # end def test_set_cookie_interface
# end class ChangeHostInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
