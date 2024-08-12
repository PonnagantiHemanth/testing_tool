#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_0007.robustness
:brief: HID++ 2.0 DeviceFriendlyName robustness test suite
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2020/10/13
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicefriendlynameutils import DeviceFriendlyNameTestUtils as Utils
from pytestbox.device.hidpp20.common.feature_0007.devicefriendlyname import DeviceFriendlyNameTestCase

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
_AUTHOR = "Suresh Thiyagarajan"


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceFriendlyNameRobustnessTestCase(DeviceFriendlyNameTestCase):
    """
    Validates DeviceFriendlyName robustness test cases
    """
    @features('Feature0007')
    @level('Robustness')
    def test_get_friendly_name_padding(self):
        """
        Validate GetFriendlyName padding bytes are ignored

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex.ByteIndex.0xPP.0xPP
        """
        request_cls = self.feature_0007.get_friendly_name_cls
        for padding in compute_sup_values(HexList(Numeral(
                request_cls.DEFAULT.PADDING,
                request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetFriendlyName with byte_index:0 and padding: {padding}")
            # ----------------------------------------------------------------------------------------
            report = request_cls(ChannelUtils.get_device_index(test_case=self), self.feature_0007_index, 0)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_0007.get_friendly_name_response_cls
            )

            Utils.GetFriendlyNameHelper.MessageChecker.check_fields(
                    self, response, self.feature_0007.get_friendly_name_response_cls)
        # end for
        self.testCaseChecked("ROB_0007_0001", _AUTHOR)
    # end def test_get_friendly_name_padding

    @features('Feature0007')
    @level('Robustness')
    def test_nvs_chunk_content_verification(self):
        """
        Validate SetFriendlyName nvs chunk
        """
        self.post_requisite_reload_nvs = True
        Utils.SetFriendlyNameHelper.HIDppHelper.set_friendly_name(self, byte_index=0, name_chunk=self.test_name_chunk)
        Utils.NvsHelper.validate_nvs_chunk(self)
        self.testCaseChecked("ROB_0007_0003", _AUTHOR)
    # end def test_nvs_chunk_content_verification

    @features('Feature0007')
    @level('Robustness')
    def test_get_default_friendly_name_padding(self):
        """
        Validate GetDefaultFriendlyName padding bytes are ignored

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex.ByteIndex.0xPP.0xPP
        """
        request_cls = self.feature_0007.get_default_friendly_name_cls
        for padding in compute_sup_values(HexList(Numeral(
                request_cls.DEFAULT.PADDING,
                request_cls.LEN.PADDING // 8))):
            # -----------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetDefaultFriendlyName with byte_index:0 and padding: {padding}")
            # -----------------------------------------------------------------------------------------------
            report = request_cls(ChannelUtils.get_device_index(test_case=self), self.feature_0007_index, 0)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_0007.get_default_friendly_name_response_cls)
            Utils.GetDefaultFriendlyNameHelper.MessageChecker.check_fields(
                    self, response, self.feature_0007.get_default_friendly_name_response_cls)
        # end for
        self.testCaseChecked("ROB_0007_0002", _AUTHOR)
    # end def test_get_default_friendly_name_padding
# end class DeviceFriendlyNameRobustnessTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
