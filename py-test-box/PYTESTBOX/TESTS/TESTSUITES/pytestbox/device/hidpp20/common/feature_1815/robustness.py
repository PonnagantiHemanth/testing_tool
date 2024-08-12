#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1815.robustness
:brief: HID++ 2.0 Hosts Info functionality test suite
:author: Christophe Roquebert
:date: 2021/03/16
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.hidpp20.common.feature_1815.hostsinfo import HostsInfoTestCase
from pytestbox.device.base.hostsinfoutils import HostsInfoTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class HostsInfoRobustnessTestCase(HostsInfoTestCase):
    """
    Validates Hosts Info Robustness TestCases
    """

    @features('Feature1815')
    @level('Robustness')
    def test_get_host_friendly_name_page_index_greater_than_name_len(self):
        """
        Validates getHostFriendlyName when the given byte index is greater than the name length
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getHostInfo request to retrieve the name_len value')
        # ----------------------------------------------------------------------------
        get_host_info_resp = HostsInfoTestUtils.HIDppHelper.get_host_info(self, host_index=0)

        host_friendly_name_check_map = HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.get_default_check_map(self)
        for index_greater_than_name_len in range(int(Numeral(get_host_info_resp.name_len)), int(Numeral(
                get_host_info_resp.name_max_len))):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getHostFriendlyName request with the given byte index greater than the '
                                     'name length')
            # ----------------------------------------------------------------------------
            get_host_friendly_name_resp = HostsInfoTestUtils.HIDppHelper.get_host_friendly_name(
                self, host_index=0, byte_index=index_greater_than_name_len)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check getHostFriendlyName response fields')
            # ----------------------------------------------------------------------------
            # Fix host index expected value in check map
            host_friendly_name_check_map["byte_index"] = (
                HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.check_byte_index, index_greater_than_name_len)
            host_friendly_name_check_map["name_chunk"] = (
                HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.check_name_chunk,
                (HostsInfoTestUtils.NAME.BLE_FRIENDLY_NAME, index_greater_than_name_len))
            HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.check_fields(
                self, get_host_friendly_name_resp, self.feature_1815.get_host_friendly_name_response_cls,
                check_map=host_friendly_name_check_map)
        # end for

        self.testCaseChecked("ROT_1815_0010")
    # end def test_get_host_friendly_name_page_index_greater_than_name_len

    @features('Feature1815')
    @level('Robustness')
    def test_get_host_friendly_name_page_index_greater_than_name_max_len(self):
        """
        Validates getHostFriendlyName when the given byte index is greater than the name maximum length
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getHostInfo request to retrieve the name_max_len value')
        # ----------------------------------------------------------------------------
        get_host_info_resp = HostsInfoTestUtils.HIDppHelper.get_host_info(self, host_index=0)

        host_friendly_name_check_map = HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.get_default_check_map(self)
        for index_greater_than_name_max_len in compute_sup_values(int(Numeral(get_host_info_resp.name_max_len))):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getHostFriendlyName request with the given byte index greater than the '
                                     'name maximum length')
            # ----------------------------------------------------------------------------
            get_host_friendly_name_resp = HostsInfoTestUtils.HIDppHelper.get_host_friendly_name(
                self, host_index=0, byte_index=index_greater_than_name_max_len)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check getHostFriendlyName response fields')
            # ----------------------------------------------------------------------------
            # Fix host index expected value in check map
            host_friendly_name_check_map["byte_index"] = (
                HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.check_byte_index, index_greater_than_name_max_len)
            host_friendly_name_check_map["name_chunk"] = (
                HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.check_name_chunk,
                (HostsInfoTestUtils.NAME.BLE_FRIENDLY_NAME, index_greater_than_name_max_len))
            HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.check_fields(
                self, get_host_friendly_name_resp, self.feature_1815.get_host_friendly_name_response_cls,
                check_map=host_friendly_name_check_map)
        # end for

        self.testCaseChecked("ROT_1815_0011")
    # end def test_get_host_friendly_name_page_index_greater_than_name_max_len

    @features('Feature1815')
    @level('Robustness')
    def test_get_feature_info_padding_ignored(self):
        """
        GetFeatureInfo padding bytes shall be ignored by the firmware
        """
        for padding in compute_sup_values(HexList(Numeral(self.feature_1815.get_feature_info_cls.DEFAULT.PADDING,
                                                        self.feature_1815.get_feature_info_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getFeatureInfo request with padding different from zero')
            # ----------------------------------------------------------------------------
            get_feature_info_req = self.feature_1815.get_feature_info_cls(self.deviceIndex, self.feature_1815_index)
            get_feature_info_req.padding = padding

            get_feature_info_resp = self.send_report_wait_response(
                report=get_feature_info_req,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=self.feature_1815.get_feature_info_response_cls)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check getFeatureInfo response fields')
            # ----------------------------------------------------------------------------
            HostsInfoTestUtils.GetFeatureInfoResponseChecker.check_fields(
                self, get_feature_info_resp, self.feature_1815.get_feature_info_response_cls)
        # end for
        self.testCaseChecked("ROT_1815_0012")
    # end def test_get_feature_info_padding_ignored

    @features('Feature1815')
    @level('Robustness')
    def test_get_host_info_padding_ignored(self):
        """
        GetHostInfo padding bytes shall be ignored by the firmware
        """
        for padding in compute_sup_values(HexList(Numeral(self.feature_1815.get_host_info_cls.DEFAULT.PADDING,
                                                        self.feature_1815.get_host_info_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getHostInfo request with padding different from zero')
            # ----------------------------------------------------------------------------
            get_host_info_req = self.feature_1815.get_host_info_cls(self.deviceIndex, self.feature_1815_index,
                                                                    host_index=0)
            get_host_info_req.padding = padding

            get_host_info_resp = self.send_report_wait_response(
                report=get_host_info_req,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=self.feature_1815.get_host_info_response_cls)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check getHostInfo response fields')
            # ----------------------------------------------------------------------------
            HostsInfoTestUtils.GetHostInfoResponseChecker.check_fields(
                self, get_host_info_resp, self.feature_1815.get_host_info_response_cls)
        # end for
        self.testCaseChecked("ROT_1815_0013")
    # end def test_get_host_info_padding_ignored

    @features('Feature1815')
    @level('Robustness')
    def test_get_host_descriptor_padding_ignored(self):
        """
        GetHostDescriptor padding bytes shall be ignored by the firmware
        """
        for padding in compute_sup_values(HexList(Numeral(self.feature_1815.get_host_descriptor_cls.DEFAULT.PADDING,
                                                        self.feature_1815.get_host_descriptor_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getHostDescriptor request with padding different from zero')
            # ----------------------------------------------------------------------------
            get_host_descriptor_req = self.feature_1815.get_host_descriptor_cls(
                self.deviceIndex, self.feature_1815_index, host_index=0, page_index=0)
            get_host_descriptor_req.padding = padding

            get_host_descriptor_resp = self.send_report_wait_response(
                report=get_host_descriptor_req,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=self.feature_1815.get_host_descriptor_response_cls)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check getHostDescriptor response fields')
            # ----------------------------------------------------------------------------
            HostsInfoTestUtils.GetHostDescriptorResponseChecker.check_fields(
                self, get_host_descriptor_resp, self.feature_1815.get_host_descriptor_response_cls)
        # end for
        self.testCaseChecked("ROT_1815_0014")
    # end def test_get_host_descriptor_padding_ignored

    @features('Feature1815')
    @level('Robustness')
    def test_get_host_friendly_name_padding_ignored(self):
        """
        GetHostFriendlyName padding bytes shall be ignored by the firmware
        """
        for padding in compute_sup_values(HexList(Numeral(self.feature_1815.get_host_friendly_name_cls.DEFAULT.PADDING,
                                                       self.feature_1815.get_host_friendly_name_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetHostFriendlyName request with padding different from zero')
            # ----------------------------------------------------------------------------
            get_host_friendly_name_req = self.feature_1815.get_host_friendly_name_cls(
                self.deviceIndex, self.feature_1815_index, host_index=0, page_index=0)
            get_host_friendly_name_req.padding = padding

            get_host_friendly_name_resp = self.send_report_wait_response(
                report=get_host_friendly_name_req,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=self.feature_1815.get_host_friendly_name_response_cls)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check GetHostFriendlyName response fields')
            # ----------------------------------------------------------------------------
            HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.check_fields(
                self, get_host_friendly_name_resp, self.feature_1815.get_host_friendly_name_response_cls)
        # end for
        self.testCaseChecked("ROT_1815_0015")
    # end def test_get_host_friendly_name_padding_ignored

    @features('Feature1815')
    @level('Robustness')
    def test_get_host_os_version_padding_ignored(self):
        """
        GetHostOsVersion padding bytes shall be ignored by the firmware
        """
        for padding in compute_sup_values(HexList(Numeral(self.feature_1815.get_host_os_version_cls.DEFAULT.PADDING,
                                                        self.feature_1815.get_host_os_version_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetHostOsVersion request with padding different from zero')
            # ----------------------------------------------------------------------------
            get_host_os_version_req = self.feature_1815.get_host_os_version_cls(
                self.deviceIndex, self.feature_1815_index, host_index=0)
            get_host_os_version_req.padding = padding

            get_host_os_version_resp = self.send_report_wait_response(
                report=get_host_os_version_req,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=self.feature_1815.get_host_os_version_response_cls)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check GetHostOsVersion response fields')
            # ----------------------------------------------------------------------------
            HostsInfoTestUtils.GetHostOsVersionResponseChecker.check_fields(
                self, get_host_os_version_resp, self.feature_1815.get_host_os_version_response_cls)
        # end for
        self.testCaseChecked("ROT_1815_0016")
    # end def test_get_host_os_version_padding_ignored

    @features('Feature1815')
    @level('Robustness')
    def test_set_host_os_version_padding_ignored(self):
        """
        SetHostOsVersion padding bytes shall be ignored by the firmware
        """
        for padding in compute_sup_values(HexList(Numeral(self.feature_1815.set_host_os_version_cls.DEFAULT.PADDING,
                                                        self.feature_1815.set_host_os_version_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send SetHostOsVersion request with padding different from zero')
            # ----------------------------------------------------------------------------
            set_host_os_version_req = self.feature_1815.set_host_os_version_cls(
                self.deviceIndex, self.feature_1815_index, host_index=0, os_type=0, os_version=0,
                os_revision=HexList('0000'), os_build=HexList('0000'))
            set_host_os_version_req.padding = padding

            set_host_os_version_resp = self.send_report_wait_response(
                report=set_host_os_version_req,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=self.feature_1815.set_host_os_version_response_cls)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check SetHostOsVersion response fields')
            # ----------------------------------------------------------------------------
            HostsInfoTestUtils.SetHostOsVersionResponseChecker.check_fields(
                self, set_host_os_version_resp, self.feature_1815.set_host_os_version_response_cls)
        # end for
        self.testCaseChecked("ROT_1815_0017")
    # end def test_set_host_os_version_padding_ignored
# end class HostsInfoRobustnessTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
