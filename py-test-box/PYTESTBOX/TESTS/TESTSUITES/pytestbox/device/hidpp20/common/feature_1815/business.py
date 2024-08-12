#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1815.business
:brief: HID++ 2.0 Hosts Info business test suite
:author: Christophe Roquebert
:date: 2021/03/10
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.bleproprepairing import BleProPrepairing
from pyhid.hidpp.features.common.bleproprepairing import BleProPrepairingFactory
from pyhid.hidpp.features.common.hostsinfo import HostsInfo
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.hidpp20.common.feature_1815.hostsinfo import HostsInfoTestCase
from pytestbox.device.base.hostsinfoutils import HostsInfoTestUtils
from pytestbox.shared.base.bleprosafeprepairedreceiverutils import BleProSafePrePairedReceiverTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pyusb.libusbdriver import ChannelIdentifier


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class HostsInfoBusinessTestCase(HostsInfoTestCase):
    """
    Validates Hosts Info Business TestCases
    """
    @features('Feature1815')
    @level('Business', 'SmokeTests')
    def test_get_all_host_descriptors(self):
        """
        Validates that we can retrieve all the Host descriptors when the first slot is paired and the next two ones
        are unpaired
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

        for host_id in range(int(Numeral(get_feature_info_resp.num_hosts))):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getHostInfo request')
            # ----------------------------------------------------------------------------
            get_host_info_resp = HostsInfoTestUtils.HIDppHelper.get_host_info(self, host_index=host_id)

            # Fix host index expected value in check map
            host_info_check_map = HostsInfoTestUtils.GetHostInfoResponseChecker.get_default_check_map(self)
            host_info_check_map["host_index"] = \
                (HostsInfoTestUtils.GetHostInfoResponseChecker.check_host_index, host_id)

            for page_id in range(int(Numeral(get_host_info_resp.num_pages))):
                # ----------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check getHostInfo response fields')
                # ----------------------------------------------------------------------------
                HostsInfoTestUtils.GetHostInfoResponseChecker.check_fields(
                    self, get_host_info_resp, self.feature_1815.get_host_info_response_cls, host_info_check_map)

                # ----------------------------------------------------------------------------
                LogHelper.log_step(self, 'Send getHostDescriptor request')
                # ----------------------------------------------------------------------------
                get_host_descriptor_resp = HostsInfoTestUtils.HIDppHelper.get_host_descriptor(
                    self, host_index=host_id, page_index=page_id)

                # Fix host and page index expected values in check map
                host_desc_check_map = HostsInfoTestUtils.GetHostDescriptorResponseChecker.get_default_check_map(self)
                host_desc_check_map["host_index"] = (
                    HostsInfoTestUtils.GetHostDescriptorResponseChecker.check_host_index, host_id)
                host_desc_check_map["page_index"] = (
                    HostsInfoTestUtils.GetHostDescriptorResponseChecker.check_page_index, page_id)

                # ----------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check getHostDescriptor response fields')
                # ----------------------------------------------------------------------------
                HostsInfoTestUtils.GetHostDescriptorResponseChecker.check_fields(
                    self, get_host_descriptor_resp, self.feature_1815.get_host_descriptor_response_cls,
                    check_map=host_desc_check_map)

        self.testCaseChecked("FNT_1815_0010")
    # end def test_get_all_host_descriptors

    @features('Feature1815')
    @features('Feature1816')
    @level('Business')
    @services('AtLeastOneKey', (KEY_ID.HOST_1, KEY_ID.CONNECT_BUTTON))
    def test_get_host_descriptor_on_prepaired(self):
        """
        Validates that we can retrieve the Host descriptors linked to a pairing with a pre-paired receiver
        """
        # Define test values
        self.pre_paired_receiver_port_index = ChannelUtils.get_port_index(test_case=self)
        self.rcv_prepairing_slot = 0x02
        self.ltk_key = HexList('000102030405060708090A0B0C0D0E0F')
        self.irk_local_key = HexList('101112131415161718191A1B1C1D1E1F')
        self.irk_remote_key = HexList('202122232425262728292A2B2C2D2E2F')

        self.post_requisite_reload_nvs = True
        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Cleanup all pairing slots except the first one')
        # ---------------------------------------------------------------------------
        DevicePairingTestUtils.NvsManager.clean_pairing_data(self)

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Get feature 1816 index')
        # ---------------------------------------------------------------------------
        if self.current_channel != self.backup_dut_channel:
            DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel)
        # end if
        DeviceBaseTestUtils.HIDppHelper.get_parameters(
            self, feature_id=BleProPrepairing.FEATURE_ID, factory=BleProPrepairingFactory)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pre Pair Receiver with Device')
        # ---------------------------------------------------------------------------
        # noinspection PyUnresolvedReferences
        self.receiver_address, self.device_address = BleProSafePrePairedReceiverTestUtils.pre_pairing_sequence(
            self,
            self.feature_1816,
            self.feature_1816_index,
            self.rcv_prepairing_slot,
            self.ltk_key,
            self.irk_local_key,
            self.irk_remote_key)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Change host on Device')
        # ---------------------------------------------------------------------------
        DevicePairingTestUtils.change_host_by_link_state(
            self, link_state=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED, clean_device_connection_event=False)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for device to be connected')
        # ---------------------------------------------------------------------------
        DeviceManagerUtils.set_channel(test_case=self,
                                       new_channel_id=ChannelIdentifier(
                                           port_index=ChannelUtils.get_port_index(test_case=self),
                                           device_index=self.rcv_prepairing_slot),
                                       open_channel=False)
        ChannelUtils.wait_for_channel_device_to_be_connected(test_case=self)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # ---------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getFeatureInfo request')
        # ----------------------------------------------------------------------------
        self.feature_1815_index = DeviceBaseTestUtils.HIDppHelper.get_feature_index(
            self, HostsInfo.FEATURE_ID, device_index=self.rcv_prepairing_slot)
        get_feature_info_resp = HostsInfoTestUtils.HIDppHelper.get_feature_info(
            self, device_index=self.rcv_prepairing_slot)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check getFeatureInfo response fields')
        # ----------------------------------------------------------------------------
        HostsInfoTestUtils.GetFeatureInfoResponseChecker.check_fields(
            self, get_feature_info_resp, self.feature_1815.get_feature_info_response_cls)

        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test loop over number of hosts')
        # ---------------------------------------------------------------------------
        for host_id in range(int(Numeral(get_feature_info_resp.num_hosts))):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getHostInfo request')
            # ----------------------------------------------------------------------------
            get_host_info_resp = HostsInfoTestUtils.HIDppHelper.get_host_info(
                self, host_index=host_id, device_index=self.rcv_prepairing_slot)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check getHostInfo response fields')
            # ----------------------------------------------------------------------------
            # Fix host index expected value in check map
            host_info_check_map = HostsInfoTestUtils.GetHostInfoResponseChecker.get_default_check_map(self)
            host_info_check_map["host_index"] = (HostsInfoTestUtils.GetHostInfoResponseChecker.check_host_index,
                                                 host_id)

            # ---------------------------------------------------------------------------
            LogHelper.log_info(self, 'Test loop over number of pages')
            # ---------------------------------------------------------------------------
            for page_id in range(int(Numeral(get_host_info_resp.num_pages))):
                # ----------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check getHostInfo response fields')
                # ----------------------------------------------------------------------------
                HostsInfoTestUtils.GetHostInfoResponseChecker.check_fields(
                    self, get_host_info_resp, self.feature_1815.get_host_info_response_cls, host_info_check_map)

                # ----------------------------------------------------------------------------
                LogHelper.log_step(self, 'Send getHostDescriptor request')
                # ----------------------------------------------------------------------------
                get_host_descriptor_resp = HostsInfoTestUtils.HIDppHelper.get_host_descriptor(
                    self, host_index=host_id, page_index=page_id, device_index=self.rcv_prepairing_slot)

                # Update host and page index expected values in check map
                host_desc_check_map = HostsInfoTestUtils.GetHostDescriptorResponseChecker.get_default_check_map(self)
                host_desc_check_map["host_index"] = (
                    HostsInfoTestUtils.GetHostDescriptorResponseChecker.check_host_index, host_id)
                host_desc_check_map["page_index"] = (
                    HostsInfoTestUtils.GetHostDescriptorResponseChecker.check_page_index, page_id)

                # ----------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check getHostDescriptor response fields')
                # ----------------------------------------------------------------------------
                HostsInfoTestUtils.GetHostDescriptorResponseChecker.check_fields(
                    self, get_host_descriptor_resp, self.feature_1815.get_host_descriptor_response_cls,
                    check_map=host_desc_check_map)
            # end for
            # ---------------------------------------------------------------------------
            LogHelper.log_info(self, 'End test loop')
            # ---------------------------------------------------------------------------
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'End test loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("FNT_1815_0011")
    # end def test_get_host_descriptor_on_prepaired

# end class HostsInfoBusinessTestCase
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
