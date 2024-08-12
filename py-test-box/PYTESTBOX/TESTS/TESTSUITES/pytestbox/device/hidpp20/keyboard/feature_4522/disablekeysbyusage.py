#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.keyboard.feature_4522.disablekeysbyusage
:brief: Base for HID++ 2.0 DisableKeysByUsage test suites
:author: YY Liu <yliu5@logitech.com>
:date: 2021/09/13
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hidpp.features.keyboard.disablekeysbyusage import DisableKeysByUsage
from pyhid.hidpp.features.keyboard.disablekeysbyusage import DisableKeysByUsageFactory
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.disablekeysbyusageutils import DisableKeysByUsageTestUtils
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DisableKeysByUsageBaseTestCase(DeviceBaseTestCase):
    """
    Base test case class for x4522 - Disable Keys By Usage test cases implementation
    """
    def setUp(self):
        """
        Handles test prerequisites.
        """
        self.post_requisite_reload_nvs = False
        self.post_requisite_reconnect_first_receiver = False

        super().setUp()

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Set default values before each test')
        # ----------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.game_mode_status = DisableKeysByUsage.GameMode.DISABLE

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x4522)')
        # ----------------------------------------------------------------------------
        self.feature_4522_index, self.feature_4522, _, _ = DisableKeysByUsageTestUtils.HIDppHelper.get_parameters(
            self, feature_id=DisableKeysByUsage.FEATURE_ID, factory=DisableKeysByUsageFactory)

    # end def setUp

    def tearDown(self):
        """
        Handles test post-requisites.
        """
        # noinspection PyBroadException
        try:
            if self.post_requisite_reload_nvs:
                # ---------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Reload initial NVS')
                # ---------------------------------------------------------------------------
                CommonBaseTestUtils.NvsHelper.restore_nvs(self)
            # end if
            if self.post_requisite_reconnect_first_receiver:
                # Reconnect with the first receiver
                ReceiverTestUtils.switch_to_receiver(
                    test_case=self,
                    receiver_port_index=ChannelUtils.get_port_index(test_case=self, channel=self.backup_dut_channel))
                # Change host on Device
                DevicePairingTestUtils.change_host_by_link_state(
                    self, link_state=DeviceConnection.LinkStatus.LINK_ESTABLISHED)
            # end if
        except Exception:
            self.log_traceback_as_warning(supplementary_message="Exception in tearDown:")
        # end try

        super().tearDown()
    # end def tearDown
# end class DisableKeysByUsageBaseTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
