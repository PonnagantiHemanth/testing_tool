#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.common.feature_1814.changehost
:brief: Validate HID++ 2.0 ``ChangeHost`` feature
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2021/12/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.core import TYPE_SUCCESS
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.changehostutils import ChangeHostTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pyusb.libusbdriver import ChannelIdentifier


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ChangeHostTestCase(DeviceBaseTestCase):
    """
    Validate ``ChangeHost`` TestCases in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x1814 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1814_index, self.feature_1814, _, _ = ChangeHostTestUtils.HIDppHelper.get_parameters(self)
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites
        """
        # noinspection PyBroadException
        try:
            if self.status != TYPE_SUCCESS:
                # Switch communication channel to receiver on port 0
                status = DeviceManagerUtils.set_channel(
                    test_case=self, new_channel_id=ChannelIdentifier(
                        port_index=self.host_number_to_port_index(0), device_index=1))
                self.assertTrue(status, msg='The device do not connect on host 0')
            # end if
        except Exception:
            self.log_traceback_as_warning(supplementary_message="Exception in tearDown:")
        finally:
            super().tearDown()
        # end try
    # end def tearDown
# end class ChangeHostTestCase


class ChangeHostMultiReceiverTestCase(DeviceBaseTestCase):
    """
    Validate ``ChangeHost`` with Multi Receivers TestCases in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()

        self.post_requisite_channel_enable = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)

        if self.f.SHARED.PAIRING.F_BLEDevicePairing:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, "Cleanup receiver pairing data when the first receiver is a dongle")
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.unpair_all(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, "Cleanup all pairing slots except the first one using the debugger link")
            # ----------------------------------------------------------------------------------------------------------
            CommonBaseTestUtils.NvsHelper.clean_pairing_data(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, f"Pair to all {self.f.PRODUCT.DEVICE.F_NbHosts} hosts supported by "
                                             f"the device")
            # ----------------------------------------------------------------------------------------------------------
            # Initialize the authentication method parameter
            DevicePairingTestUtils.set_authentication_method(self, self.config_manager)
            # Get available ble pro receiver port indexes excluding the first receiver index which the DUT will already
            # be paired to
            self.ble_pro_receiver_port_indexes = ReceiverTestUtils.get_receiver_port_indexes(
                self, ReceiverTestUtils.USB_PID_MEZZY_BLE_PRO, skip=[ChannelUtils.get_port_index(test_case=self)])
            # Get available host indexes excluding the first host which will already be in paired state
            available_hosts_index = list(range(self.f.PRODUCT.DEVICE.F_NbHosts))[1:]
            self.assertTrue(expr=len(self.ble_pro_receiver_port_indexes) == len(available_hosts_index),
                            msg="Not the right amount of MEZZY BLE Pro receivers to test")
            dispatcher_to_dump = self.current_channel.hid_dispatcher
            for host_index, port_index in zip(available_hosts_index, self.ble_pro_receiver_port_indexes):
                DevicePairingTestUtils.pair_device_slot_to_other_receiver(
                    test_case=self,
                    device_slot=host_index,
                    other_receiver_port_index=port_index,
                    hid_dispatcher_to_dump=dispatcher_to_dump)
                # Note that if we do not close the channel here, we got 3 receiver * 4 interfaces opened at the
                # same time and we do not receive the HID event when emulating a user action
                # FIXME : To be removed when the HID device layer is available
                self.current_channel.close()
            # end for

            # Reconnect with the first receiver
            ReceiverTestUtils.switch_to_receiver(
                self, receiver_port_index=ChannelUtils.get_port_index(test_case=self, channel=self.backup_dut_channel))

            # Change host on Device
            DevicePairingTestUtils.change_host_by_link_state(
                self, link_state=DeviceConnection.LinkStatus.LINK_ESTABLISHED)

            DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x1814 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1814_index, self.feature_1814, _, _ = ChangeHostTestUtils.HIDppHelper.get_parameters(self)
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites
        """
        # noinspection PyBroadException
        try:
            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, "Reload initial NVS")
            # ------------------------------------------------------------------------------------------------------
            DeviceTestUtils.NvsHelper.restore_nvs(self)

            if self.post_requisite_channel_enable:
                self.device.enable_usb_port(self.host_number_to_port_index(2))
            # end if

            if self.status != TYPE_SUCCESS:
                # Switch communication channel to receiver on port 0
                status = DeviceManagerUtils.set_channel(
                    test_case=self, new_channel_id=ChannelIdentifier(port_index=self.host_number_to_port_index(0)))
                self.assertTrue(status, msg='The device do not connect on host 0')
            # end if
        except Exception:
            self.log_traceback_as_warning(supplementary_message="Exception in tearDown:")
        finally:
            super().tearDown()
        # end try
    # end def tearDown
# end class ChangeHostTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
