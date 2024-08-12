#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.hid.mouse.feature_2111.smartshifttunable
:brief: Base for HID++ 2.0 SmartShiftTunable test suites
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2021/08/10
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hidpp.features.mouse.smartshifttunable import SmartShiftTunable
from pyhid.hidpp.features.mouse.smartshifttunable import SmartShiftTunableFactory
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.smartshiftunableutils import SmartShiftTunableTestUtils
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class SmartShiftTunableBaseTestCase(DeviceBaseTestCase):
    """
    Base test case class for x2111 - SmartShift 3G/EPM wheel with tunable torque test cases implementation
    """
    def setUp(self):
        """
        Handles test prerequisites.
        """
        self.post_requisite_reload_nvs = False
        self.post_requisite_reconnect_first_receiver = False

        super().setUp()

        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x2111)')
        # ----------------------------------------------------------------------------
        self.feature_2111_index, self.feature_2111, _, _ = SmartShiftTunableTestUtils.HIDppHelper.get_parameters(
            self, feature_id=SmartShiftTunable.FEATURE_ID, factory=SmartShiftTunableFactory)
    # end def setUp

    def tearDown(self):
        """
        Handles test post-requisites.
        """
        # noinspection PyBroadException
        try:
            if self.post_requisite_reload_nvs:
                # ---------------------------------------------------------------------------
                CommonBaseTestUtils.LogHelper.log_post_requisite(self, 'Reload initial NVS')
                # ---------------------------------------------------------------------------
                CommonBaseTestUtils.NvsHelper.restore_nvs(self)
            # end if
            if self.post_requisite_reconnect_first_receiver:
                # Reconnect with the first receiver
                ReceiverTestUtils.switch_to_receiver(self, ChannelUtils.get_port_index(test_case=self))
                # Change host on Device
                DevicePairingTestUtils.change_host_by_link_state(
                    self, link_state=DeviceConnection.LinkStatus.LINK_ESTABLISHED)
            # end if
        except Exception:
            self.log_traceback_as_warning(supplementary_message="Exception in tearDown:")
        # end try
        super().tearDown()
    # end def tearDown
# end class SmartShiftTunableBaseTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
