#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.keyboard.feature_4531.interface
:brief: HID++ 2.0 ``MultiPlatform`` interface test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2022/10/13
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
from pytestbox.device.base.multiplatformutils import MultiPlatformTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4531.multiplatform import MultiPlatformTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MultiPlatformInterfaceTestCase(MultiPlatformTestCase):
    """
    Validate ``MultiPlatform`` interface test cases
    """

    @features("Feature4531")
    @level("Interface")
    def test_get_feature_infos(self):
        """
        Validate ``GetFeatureInfos`` interface
        """
        current_host = HexList(0x0)
        current_host_platform = HexList(0x0)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetFeatureInfos request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_4531.get_feature_infos_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_4531_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
            response_class_type=self.feature_4531.get_feature_infos_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetFeatureInfosResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MultiPlatformTestUtils.GetFeatureInfosResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, report.device_index),
            "feature_index": (checker.check_feature_index, report.feature_index),
            "current_host": (checker.check_current_host, current_host),
            "current_host_platform": (checker.check_current_host_platform, current_host_platform),
        })
        checker.check_fields(self, response, self.feature_4531.get_feature_infos_response_cls, check_map)

        self.testCaseChecked("INT_4531_0001", _AUTHOR)
    # end def test_get_feature_infos

    @features("Feature4531")
    @level("Interface")
    def test_get_platform_descriptor(self):
        """
        Validate ``GetPlatformDescriptor`` interface
        """
        platform_index = 0
        platform_descriptor_index = platform_index
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetPlatformDescriptor request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_4531.get_platform_descriptor_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_4531_index,
            platform_descriptor_index=platform_descriptor_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
            response_class_type=self.feature_4531.get_platform_descriptor_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetPlatformDescriptorResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MultiPlatformTestUtils.GetPlatformDescriptorResponseChecker
        check_map = checker.get_default_check_map(self)
        os_mask_check_map = MultiPlatformTestUtils.OSMaskChecker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, report.device_index),
            "feature_index": (checker.check_feature_index, report.feature_index),
            "platform_index": (checker.check_platform_index, platform_index),
            "platform_descriptor_index": (checker.check_platform_descriptor_index, platform_descriptor_index),
            "os_mask": (checker.check_os_mask, os_mask_check_map)
        })
        checker.check_fields(self, response, self.feature_4531.get_platform_descriptor_response_cls, check_map)

        self.testCaseChecked("INT_4531_0002", _AUTHOR)
    # end def test_get_platform_descriptor

    @features("Feature4531")
    @level("Interface")
    def test_get_host_platform(self):
        """
        Validate ``GetHostPlatform`` interface
        """
        host_index = 0
        status = int(self.config.F_Status[host_index])
        platform_index = int(self.config.F_PlatformIndex[host_index])
        platform_source = int(self.config.F_PlatformSource[host_index])
        auto_platform = int(self.config.F_AutoPlatform[host_index])
        auto_descriptor = int(self.config.F_AutoDescriptor[host_index])
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetHostPlatform request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_4531.get_host_platform_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_4531_index,
            host_index=host_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
            response_class_type=self.feature_4531.get_host_platform_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetHostPlatformResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MultiPlatformTestUtils.GetHostPlatformResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, report.device_index),
            "feature_index": (checker.check_feature_index, report.feature_index),
            "host_index": (checker.check_host_index, host_index),
            "status": (checker.check_status, status),
            "platform_index": (checker.check_platform_index, platform_index),
            "platform_source": (checker.check_platform_source, platform_source),
            "auto_platform": (checker.check_auto_platform, auto_platform),
            "auto_descriptor": (checker.check_auto_descriptor, auto_descriptor),
        })
        checker.check_fields(self, response, self.feature_4531.get_host_platform_response_cls, check_map)

        self.testCaseChecked("INT_4531_0003", _AUTHOR)
    # end def test_get_host_platform

    @features("Feature4531")
    @features("SetHostPlatform")
    @level("Interface")
    def test_set_host_platform(self):
        """
        Validate ``SetHostPlatform`` interface
        """
        host_index = HexList(0x0)
        platform_index = HexList(0x0)
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetHostPlatform request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_4531.set_host_platform_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_4531_index,
            host_index=host_index,
            platform_index=platform_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
            response_class_type=self.feature_4531.set_host_platform_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetHostPlatformResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MultiPlatformTestUtils.SetHostPlatformResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, report.device_index),
            "feature_index": (checker.check_feature_index, report.feature_index),
            "host_index": (checker.check_host_index, host_index),
            "platform_index": (checker.check_platform_index, platform_index),
        })
        checker.check_fields(self, response, self.feature_4531.set_host_platform_response_cls, check_map)

        self.testCaseChecked("INT_4531_0004", _AUTHOR)
    # end def test_set_host_platform
# end class MultiPlatformInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
