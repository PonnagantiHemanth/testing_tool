#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1815.interface
:brief: HID++ 2.0 Hosts Info interface test suite
:author: Christophe Roquebert
:date: 2021/03/08
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.hidpp20.common.feature_1815.hostsinfo import HostsInfoTestCase
from pytestbox.device.base.hostsinfoutils import HostsInfoTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class HostsInfoInterfaceTestCase(HostsInfoTestCase):
    """
    Validates Hosts Info interface TestCases
    """
    @features('Feature1815')
    @level('Interface')
    def test_get_feature_info_api(self):
        """
        Validates getFeatureInfo API
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getFeatureInfo request')
        # ----------------------------------------------------------------------------
        get_feature_info_resp = HostsInfoTestUtils.HIDppHelper.get_feature_info(self)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check getFeatureInfo response fields')
        # ----------------------------------------------------------------------------
        HostsInfoTestUtils.GetFeatureInfoResponseChecker.check_fields(
            self, get_feature_info_resp, self.feature_1815.get_feature_info_response_cls)

        self.testCaseChecked("FNT_1815_0001")
    # end def test_get_feature_info_api

    @features('Feature1815')
    @features('BLEDevicePairing')
    @level('Interface')
    def test_get_host_info_api(self):
        """
        Validates getHostInfo API
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getHostInfo request')
        # ----------------------------------------------------------------------------
        get_host_info_resp = HostsInfoTestUtils.HIDppHelper.get_host_info(self, host_index=0)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check getHostInfo response fields')
        # ----------------------------------------------------------------------------
        HostsInfoTestUtils.GetHostInfoResponseChecker.check_fields(
            self, get_host_info_resp, self.feature_1815.get_host_info_response_cls)

        self.testCaseChecked("FNT_1815_0002")
    # end def test_get_host_info_api

    @features('Feature1815')
    @features('BLEDevicePairing')
    @level('Interface')
    def test_get_host_descriptor_api(self):
        """
        Validates getHostDescriptor API
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getHostDescriptor request')
        # ----------------------------------------------------------------------------
        get_host_descriptor_req = self.feature_1815.get_host_descriptor_cls(self.deviceIndex, self.feature_1815_index)
        get_host_descriptor_resp = self.send_report_wait_response(
            report=get_host_descriptor_req,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=self.feature_1815.get_host_descriptor_response_cls)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check getHostDescriptor response fields')
        # ----------------------------------------------------------------------------
        HostsInfoTestUtils.GetHostDescriptorResponseChecker.check_fields(
            self, get_host_descriptor_resp, self.feature_1815.get_host_descriptor_response_cls)

        self.testCaseChecked("FNT_1815_0003")
    # end def test_get_host_descriptor_api

    @features('Feature1815')
    @level('Interface')
    def test_get_host_friendly_name_api(self):
        """
        Validates getHostFriendlyName API
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getHostFriendlyName request')
        # ----------------------------------------------------------------------------
        get_host_friendly_name_resp = HostsInfoTestUtils.HIDppHelper.get_host_friendly_name(
            self, host_index=0, byte_index=0)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check getHostFriendlyName response fields')
        # ----------------------------------------------------------------------------
        HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.check_fields(
            self, get_host_friendly_name_resp, self.feature_1815.get_host_friendly_name_response_cls)

        self.testCaseChecked("FNT_1815_0004")
    # end def test_get_host_friendly_name_api

    @features('Feature1815')
    @level('Interface')
    def test_set_host_friendly_name_api(self):
        """
        Validates setHostFriendlyName API
        """
        new_name = 'Logi dongle'
        self.post_requisite_reload_nvs = True
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setHostFriendlyName request')
        # ----------------------------------------------------------------------------
        set_host_friendly_name_resp = HostsInfoTestUtils.HIDppHelper.set_host_friendly_name_chunk(
            self, host_index=0, byte_index=0, name_chunk=new_name)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check setHostFriendlyName response fields')
        # ----------------------------------------------------------------------------
        host_friendly_name_check_map = HostsInfoTestUtils.SetHostFriendlyNameResponseChecker.get_default_check_map(self)
        # Fix name length expected value in check map
        host_friendly_name_check_map["name_len"] = (
            HostsInfoTestUtils.SetHostFriendlyNameResponseChecker.check_name_len, len(new_name))
        HostsInfoTestUtils.SetHostFriendlyNameResponseChecker.check_fields(
            self, set_host_friendly_name_resp, self.feature_1815.set_host_friendly_name_response_cls,
            check_map=host_friendly_name_check_map)

        self.testCaseChecked("FNT_1815_0005")
    # end def test_set_host_friendly_name_api

    @features('Feature1815')
    @level('Interface')
    def test_get_host_os_version_api(self):
        """
        Validates GetHostOsVersion API
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetHostOsVersion request')
        # ----------------------------------------------------------------------------
        get_host_os_version_resp = HostsInfoTestUtils.HIDppHelper.get_host_os_version(self, host_index=0)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check GetHostOsVersion response fields')
        # ----------------------------------------------------------------------------
        HostsInfoTestUtils.GetHostOsVersionResponseChecker.check_fields(
            self, get_host_os_version_resp, self.feature_1815.get_host_os_version_response_cls)

        self.testCaseChecked("FNT_1815_0006")
    # end def test_get_host_os_version_api

    @features('Feature1815')
    @level('Interface')
    def test_set_host_os_version_api(self):
        """
        Validates SetHostOsVersion API
        """
        self.post_requisite_reload_nvs = True

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send SetHostOsVersion request')
        # ----------------------------------------------------------------------------
        set_host_os_version_resp = HostsInfoTestUtils.HIDppHelper.set_host_os_version(
            self, host_index=0, os_type=0, os_version=0, os_revision=0, os_build=0)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check SetHostOsVersion response fields')
        # ----------------------------------------------------------------------------
        HostsInfoTestUtils.SetHostOsVersionResponseChecker.check_fields(
            self, set_host_os_version_resp, self.feature_1815.set_host_os_version_response_cls)

        self.testCaseChecked("FNT_1815_0007")
    # end def test_set_host_os_version_api

# end class HostsInfoInterfaceTestCase
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
