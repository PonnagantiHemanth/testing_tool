#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.keyboard.feature_4531.robustness
:brief: HID++ 2.0 ``MultiPlatform`` robustness test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2022/10/13
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.keyboard.multiplatform import MultiPlatform
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.multiplatformutils import MultiPlatformTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4531.multiplatform import MultiPlatformTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MultiPlatformRobustnessTestCase(MultiPlatformTestCase):
    """
    Validate ``MultiPlatform`` robustness test cases
    """

    @features("Feature4531")
    @level("Robustness")
    def test_get_feature_infos_software_id(self):
        """
        Validate ``GetFeatureInfos`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        current_host = HexList(0x0)
        current_host_platform = HexList(0x0)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(MultiPlatform.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetFeatureInfos request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_4531.get_feature_infos_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_4531_index)
            report.software_id = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=self.feature_4531.get_feature_infos_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetFeatureInfosResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = MultiPlatformTestUtils.GetFeatureInfosResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "current_host": (checker.check_current_host, current_host),
                "current_host_platform": (checker.check_current_host_platform, current_host_platform),
            })
            checker.check_fields(self, response, self.feature_4531.get_feature_infos_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4531_0001#1", _AUTHOR)
    # end def test_get_feature_infos_software_id

    @features("Feature4531")
    @level("Robustness")
    def test_get_platform_descriptor_software_id(self):
        """
        Validate ``GetPlatformDescriptor`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.PlatformDescriptorIndex.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        platform_index = 0
        platform_descriptor_index = platform_index
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(MultiPlatform.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetPlatformDescriptor request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_4531.get_platform_descriptor_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_4531_index,
                platform_descriptor_index=platform_descriptor_index)
            report.software_id = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=self.feature_4531.get_platform_descriptor_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetPlatformDescriptorResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = MultiPlatformTestUtils.GetPlatformDescriptorResponseChecker
            check_map = checker.get_default_check_map(self)
            os_mask_check_map = MultiPlatformTestUtils.OSMaskChecker.get_default_check_map(test_case=self)
            check_map.update({
                "platform_index": (checker.check_platform_index, platform_index),
                "platform_descriptor_index": (checker.check_platform_descriptor_index, platform_descriptor_index),
                "os_mask": (checker.check_os_mask, os_mask_check_map)
            })
            checker.check_fields(self, response, self.feature_4531.get_platform_descriptor_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4531_0001#2", _AUTHOR)
    # end def test_get_platform_descriptor_software_id

    @features("Feature4531")
    @level("Robustness")
    def test_get_host_platform_software_id(self):
        """
        Validate ``GetHostPlatform`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.HostIndex.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        host_index = 0
        status = int(self.config.F_Status[host_index])
        platform_index = int(self.config.F_PlatformIndex[host_index])
        platform_source = int(self.config.F_PlatformSource[host_index])
        auto_platform = int(self.config.F_AutoPlatform[host_index])
        auto_descriptor = int(self.config.F_AutoDescriptor[host_index])
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(MultiPlatform.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetHostPlatform request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_4531.get_host_platform_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_4531_index,
                host_index=host_index)
            report.software_id = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=self.feature_4531.get_host_platform_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetHostPlatformResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = MultiPlatformTestUtils.GetHostPlatformResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "host_index": (checker.check_host_index, host_index),
                "status": (checker.check_status, status),
                "platform_index": (checker.check_platform_index, platform_index),
                "platform_source": (checker.check_platform_source, platform_source),
                "auto_platform": (checker.check_auto_platform, auto_platform),
                "auto_descriptor": (checker.check_auto_descriptor, auto_descriptor),
            })
            checker.check_fields(self, response, self.feature_4531.get_host_platform_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4531_0001#3", _AUTHOR)
    # end def test_get_host_platform_software_id

    @features("Feature4531")
    @features("SetHostPlatform")
    @level("Robustness")
    def test_set_host_platform_software_id(self):
        """
        Validate ``SetHostPlatform`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.HostIndex.PlatformIndex.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        host_index = HexList(0x0)
        platform_index = HexList(0x0)
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(MultiPlatform.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetHostPlatform request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_4531.set_host_platform_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_4531_index,
                host_index=host_index,
                platform_index=platform_index)
            report.software_id = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=self.feature_4531.set_host_platform_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetHostPlatformResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = MultiPlatformTestUtils.SetHostPlatformResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "host_index": (checker.check_host_index, host_index),
                "platform_index": (checker.check_platform_index, platform_index),
            })
            checker.check_fields(self, response, self.feature_4531.set_host_platform_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4531_0001#4", _AUTHOR)
    # end def test_set_host_platform_software_id

    @features("Feature4531")
    @level("Robustness")
    def test_get_feature_infos_padding(self):
        """
        Validate ``GetFeatureInfos`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        current_host = HexList(0x0)
        current_host_platform = HexList(0x0)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_4531.get_feature_infos_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetFeatureInfos request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_4531_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=self.feature_4531.get_feature_infos_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetFeatureInfosResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = MultiPlatformTestUtils.GetFeatureInfosResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "current_host": (checker.check_current_host, current_host),
                "current_host_platform": (checker.check_current_host_platform, current_host_platform),
            })
            checker.check_fields(self, response, self.feature_4531.get_feature_infos_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4531_0002#1", _AUTHOR)
    # end def test_get_feature_infos_padding

    @features("Feature4531")
    @level("Robustness")
    def test_get_platform_descriptor_padding(self):
        """
        Validate ``GetPlatformDescriptor`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.PlatformDescriptorIndex.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        platform_index = 0
        platform_descriptor_index = platform_index
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_4531.get_platform_descriptor_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetPlatformDescriptor request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_4531_index,
                platform_descriptor_index=platform_descriptor_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=self.feature_4531.get_platform_descriptor_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetPlatformDescriptorResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = MultiPlatformTestUtils.GetPlatformDescriptorResponseChecker
            check_map = checker.get_default_check_map(self)
            os_mask_check_map = MultiPlatformTestUtils.OSMaskChecker.get_default_check_map(self)
            check_map.update({
                "platform_index": (checker.check_platform_index, platform_index),
                "platform_descriptor_index": (checker.check_platform_descriptor_index, platform_descriptor_index),
                "os_mask": (checker.check_os_mask, os_mask_check_map)
            })
            checker.check_fields(self, response, self.feature_4531.get_platform_descriptor_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4531_0002#2", _AUTHOR)
    # end def test_get_platform_descriptor_padding

    @features("Feature4531")
    @level("Robustness")
    def test_get_host_platform_padding(self):
        """
        Validate ``GetHostPlatform`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.HostIndex.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        host_index = 0
        status = int(self.config.F_Status[host_index])
        platform_index = int(self.config.F_PlatformIndex[host_index])
        platform_source = int(self.config.F_PlatformSource[host_index])
        auto_platform = int(self.config.F_AutoPlatform[host_index])
        auto_descriptor = int(self.config.F_AutoDescriptor[host_index])
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_4531.get_host_platform_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetHostPlatform request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_4531_index,
                host_index=host_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=self.feature_4531.get_host_platform_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetHostPlatformResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = MultiPlatformTestUtils.GetHostPlatformResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "host_index": (checker.check_host_index, host_index),
                "status": (checker.check_status, status),
                "platform_index": (checker.check_platform_index, platform_index),
                "platform_source": (checker.check_platform_source, platform_source),
                "auto_platform": (checker.check_auto_platform, auto_platform),
                "auto_descriptor": (checker.check_auto_descriptor, auto_descriptor),
            })
            checker.check_fields(self, response, self.feature_4531.get_host_platform_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4531_0002#3", _AUTHOR)
    # end def test_get_host_platform_padding

    @features("Feature4531")
    @features("SetHostPlatform")
    @level("Robustness")
    def test_set_host_platform_padding(self):
        """
        Validate ``SetHostPlatform`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.HostIndex.PlatformIndex.0xPP

        Padding (PP) boundary values [00..FF]
        """
        host_index = HexList(0x0)
        platform_index = HexList(0x0)
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_4531.set_host_platform_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetHostPlatform request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_4531_index,
                host_index=host_index,
                platform_index=platform_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=self.feature_4531.set_host_platform_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetHostPlatformResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = MultiPlatformTestUtils.SetHostPlatformResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "host_index": (checker.check_host_index, host_index),
                "platform_index": (checker.check_platform_index, platform_index),
            })
            checker.check_fields(self, response, self.feature_4531.set_host_platform_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4531_0002#4", _AUTHOR)
    # end def test_set_host_platform_padding
# end class MultiPlatformRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
