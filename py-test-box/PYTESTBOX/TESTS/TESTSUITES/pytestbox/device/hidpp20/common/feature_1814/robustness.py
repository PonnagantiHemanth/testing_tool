#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.common.feature_1814.robustness
:brief: HID++ 2.0 ``ChangeHost`` robustness test suite
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2021/12/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.changehost import ChangeHost
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
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
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ChangeHostRobustnessTestCase(ChangeHostTestCase):
    """
    Validate ``ChangeHost`` robustness test cases
    """

    @features("Feature1814")
    @level("Robustness")
    def test_get_host_info_software_id(self):
        """
        Validate ``GetHostInfo`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ChangeHost.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetHostInfo request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1814.get_host_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1814_index)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1814.get_host_info_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetHostInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ChangeHostTestUtils.GetHostInfoResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "deviceIndex": (checker.check_device_index, report.deviceIndex),
                "featureIndex": (checker.check_feature_index, report.featureIndex),
            })
            checker.check_fields(self, response, self.feature_1814.get_host_info_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1814_0001", _AUTHOR)
    # end def test_get_host_info_software_id

    @features("Feature1814")
    @level("Robustness")
    def test_set_current_host_software_id(self):
        """
        Validate ``SetCurrentHost`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.hostIndex.0xPP.0xPP

        SwID boundary values [0..F]
        """
        host_index = HexList(0x0)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ChangeHost.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetCurrentHost request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1814.set_current_host_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1814_index,
                host_index=host_index)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1814.set_current_host_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetCurrentHostResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = DeviceTestUtils.MessageChecker
            check_map = {
                "deviceIndex": (checker.check_device_index, report.deviceIndex),
                "featureIndex": (checker.check_feature_index, report.featureIndex),
            }
            checker.check_fields(self, response, self.feature_1814.set_current_host_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1814_0002", _AUTHOR)
    # end def test_set_current_host_software_id

    @features("Feature1814")
    @level("Robustness")
    def test_get_cookies_software_id(self):
        """
        Validate ``GetCookies`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ChangeHost.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCookies request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1814.get_cookies_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1814_index)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1814.get_cookies_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCookiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            cookies_list = get_cookie_list(response, self.f.PRODUCT.DEVICE.F_NbHosts)
            for i in range(self.f.PRODUCT.DEVICE.F_NbHosts):
                self.assertEqual(expected=True,
                                 obtained=int(cookies_list[i], 16) in range(0x100),
                                 msg='The cookies[' + str(i) + '] parameter differs from the one expected')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1814_0003", _AUTHOR)
    # end def test_get_cookies_software_id

    @features("Feature1814")
    @level("Robustness")
    def test_set_cookie_software_id(self):
        """
        Validate ``SetCookie`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.hostIndex.cookie.0xPP

        SwID boundary values [0..F]
        """
        host_index = HexList(0x0)
        cookie = HexList(0x0)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ChangeHost.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetCookie request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1814.set_cookie_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1814_index,
                host_index=host_index,
                cookie=cookie)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1814.set_cookie_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetCookieResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = DeviceTestUtils.MessageChecker
            check_map = {
                "deviceIndex": (checker.check_device_index, report.deviceIndex),
                "featureIndex": (checker.check_feature_index, report.featureIndex),
            }
            checker.check_fields(self, response, self.feature_1814.set_cookie_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1814_0004", _AUTHOR)
    # end def test_set_cookie_software_id

    @features("Feature1814")
    @level("Robustness")
    def test_get_host_info_padding(self):
        """
        Validate ``GetHostInfo`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1814.get_host_info_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetHostInfo request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1814_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1814.get_host_info_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetHostInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ChangeHostTestUtils.GetHostInfoResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "deviceIndex": (checker.check_device_index, report.deviceIndex),
                "featureIndex": (checker.check_feature_index, report.featureIndex),
            })
            checker.check_fields(self, response, self.feature_1814.get_host_info_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1814_0005", _AUTHOR)
    # end def test_get_host_info_padding

    @features("Feature1814")
    @level("Robustness")
    def test_set_current_host_padding(self):
        """
        Validate ``SetCurrentHost`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.hostIndex.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        host_index = HexList(0x0)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1814.set_current_host_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetCurrentHost request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1814_index,
                host_index=host_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1814.set_current_host_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetCurrentHostResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = DeviceTestUtils.MessageChecker
            check_map = {
                "deviceIndex": (checker.check_device_index, report.deviceIndex),
                "featureIndex": (checker.check_feature_index, report.featureIndex),
            }
            checker.check_fields(self, response, self.feature_1814.set_current_host_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1814_0006", _AUTHOR)
    # end def test_set_current_host_padding

    @features("Feature1814")
    @level("Robustness")
    def test_get_cookies_padding(self):
        """
        Validate ``GetCookies`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1814.get_cookies_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCookies request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1814_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1814.get_cookies_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCookiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            cookies_list = get_cookie_list(response, self.f.PRODUCT.DEVICE.F_NbHosts)
            for i in range(self.f.PRODUCT.DEVICE.F_NbHosts):
                self.assertEqual(expected=True,
                                 obtained=int(cookies_list[i], 16) in range(0x100),
                                 msg='The cookies[' + str(i) + '] parameter differs from the one expected')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1814_0007", _AUTHOR)
    # end def test_get_cookies_padding

    @features("Feature1814")
    @level("Robustness")
    def test_set_cookie_padding(self):
        """
        Validate ``SetCookie`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.hostIndex.cookie.0xPP

        Padding (PP) boundary values [00..FF]
        """
        host_index = HexList(0x0)
        cookie = HexList(0x0)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1814.set_cookie_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetCookie request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1814_index,
                host_index=host_index,
                cookie=cookie)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1814.set_cookie_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetCookieResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = DeviceTestUtils.MessageChecker
            check_map = {
                "deviceIndex": (checker.check_device_index, report.deviceIndex),
                "featureIndex": (checker.check_feature_index, report.featureIndex),
            }
            checker.check_fields(self, response, self.feature_1814.set_cookie_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1814_0008", _AUTHOR)
    # end def test_set_cookie_padding
# end class ChangeHostRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
