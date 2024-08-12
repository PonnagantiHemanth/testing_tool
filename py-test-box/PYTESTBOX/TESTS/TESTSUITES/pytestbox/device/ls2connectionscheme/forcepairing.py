#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ls2connectionscheme.forcepairing
:brief: Validate LS2 connection scheme for Force Pairing test cases
:author: Zane Lu <zlu@logitech.com>
:date: 2022/04/13
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.forcepairingutils import ForcePairingTestUtils
from pytestbox.device.ls2connectionscheme.uhs_connection_scheme import UhsConnectionSchemeBase
from pytestbox.device.ls2connectionscheme.utils import Ls2ConnectionSchemeTestUtils
from pytestbox.device.ls2connectionscheme.portconfiguration import PortConfiguration
from pyusb.libusbdriver import ChannelIdentifier


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ForcePairingBaseTestCase(UhsConnectionSchemeBase):
    """
    LS2 connection scheme - Force Pairing Base Test Case
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()

        self.MAX_WAIT_FOR_LED_OFF = self.f.PRODUCT.FEATURES.COMMON.FORCE_PAIRING.F_MaxWaitForLedOff

        self.DUT_DEVICE_INDEX = 1

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'the device is connected with the pre-paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.connect_to_the_pre_paired_receiver()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x1500 index")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.close_channel(test_case=self)
        new_channel = DeviceManagerUtils.get_channel(
            test_case=self,
            channel_id=ChannelIdentifier(port_index=PortConfiguration.PRE_PAIRED_RECEIVER_PORT,
                                         device_index=self.DUT_DEVICE_INDEX))
        DeviceManagerUtils.set_channel(test_case=self, new_channel=new_channel)

        self.feature_1500_index, self.feature_1500, _, _ = ForcePairingTestUtils.HIDppHelper.get_parameters(self)

        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(self, [True, False, True, False, False])

        self.pre_paired_channel = DeviceManagerUtils.get_channel(
            test_case=self, channel_id=ChannelIdentifier(port_index=PortConfiguration.PRE_PAIRED_RECEIVER_PORT))
        self.assertNotNone(obtained=self.pre_paired_channel, msg="Pre-paired receiver not found")

        self.crush_channel = DeviceManagerUtils.get_channel(
            test_case=self, channel_id=ChannelIdentifier(port_index=PortConfiguration.CRUSH_RECEIVER_PORT))
        self.assertNotNone(obtained=self.crush_channel, msg="Crush receiver not found")

        self.ls2_channel = DeviceManagerUtils.get_channel(
            test_case=self, channel_id=ChannelIdentifier(port_index=PortConfiguration.LS2_RECEIVER_PORT))
        self.assertNotNone(obtained=self.ls2_channel, msg="LS2 receiver not found")
    # end def setUp

# end class ForcePairingBaseTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
