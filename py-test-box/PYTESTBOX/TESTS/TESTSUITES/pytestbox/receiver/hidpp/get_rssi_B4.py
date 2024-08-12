#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.receiver.hidpp.get_rssi_B4
:brief: Validates HID++ Get RSSI register
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/02/28
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.registers.getrssi import GetRssiRequest
from pyhid.hidpp.hidpp1.registers.getrssi import GetRssiResponse
from pyhid.hidpp.hidpp1.registers.testmodecontrol import TestModeControl
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import ReceiverBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.receiver.base.receivermanagedeactivatablefeaturesauthutils import \
    ReceiverManageDeactivatableFeaturesAuthTestUtils
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
from pytestbox.shared.base.tdeutils import TDETestUtils


class GetRssiTestCase(ReceiverBaseTestCase):
    """
    Get RSSI register TestCases
    """

    def setUp(self):
        """
        Handles test prerequisites.
        """
        self.ble_context = None
        self.post_requisite_reload_nvs = False

        super().setUp()

        # ------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup device initial NVS")
        # ------------------------------------------------------------------------
        if self.device_memory_manager is not None:
            self.device_memory_manager.read_nvs(backup=True)
        # end if
    # end def setUp

    def tearDown(self):
        """
        Handles test post-requisites.
        """
        # noinspection PyBroadException
        try:
            if self.post_requisite_reload_nvs and self.device_memory_manager is not None:

                # ------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload DUT initial NVS")
                # ------------------------------------------------------
                self.device_memory_manager.load_nvs(backup=True)
                self.post_requisite_reload_nvs = False
            # end if
        except Exception:
            self.log_traceback_as_warning(supplementary_message="Exception in tearDown:")
        # end try
        super().tearDown()
    # end def tearDown

    @features('RcvGetRssi')
    @features('ManageDeactivatableFeaturesAuth')
    @level('Business')
    def test_get_rssi_by_tde(self):
        """
        For manufacturing, open a session, complete authentication and enable features. Features should be enabled.
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Enable Test Mode Control')
        # ---------------------------------------------------------------------------
        TDETestUtils.set_check_test_mode(
            self, test_mode_enable=TestModeControl.TestModeEnable.ENABLE_MANUFACTURING_TEST_MODE)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable all manufacturing features')
        # ----------------------------------------------------------------------------
        ReceiverManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features(test_case=self, manufacturing=True)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send the Get RSSI request to the dongle')
        # ----------------------------------------------------------------------------
        get_info_resp = ChannelUtils.send(
            test_case=self,
            report=GetRssiRequest(index=1),
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=GetRssiResponse)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate Get RSSI firmware response')
        # ---------------------------------------------------------------------------
        unsigned_value = int.from_bytes(to_int(get_info_resp.signal_strength).to_bytes(1, 'little'), 'little',
                                        signed=True)
        self.assertLessEqual(unsigned_value, GetRssiResponse.STRENGTH.NRF52_MAX,
                             msg='The signal strength parameter is greater than the expected value')
        self.assertGreater(unsigned_value, GetRssiResponse.STRENGTH.NRF52_MIN,
                           msg='The signal strength parameter is lower than the expected value')

        self.testCaseChecked("BUS_RCV-B4_0001")
    # end def test_get_rssi_by_tde

    @features('RcvGetRssi')
    @level('Functionality')
    def test_get_rssi(self):
        """
        Validate 0xB4 - Get RSSI

        This register returns the last RSSI read by the dongle.
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send the Get RSSI request to the dongle')
        # ----------------------------------------------------------------------------
        get_info_resp = ChannelUtils.send(
            test_case=self,
            report=GetRssiRequest(index=1),
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=GetRssiResponse)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate Get RSSI firmware response')
        # ---------------------------------------------------------------------------
        unsigned_value = int.from_bytes(to_int(get_info_resp.signal_strength).to_bytes(1, 'little'), 'little',
                                        signed=True)
        self.assertLessEqual(unsigned_value, GetRssiResponse.STRENGTH.NRF52_MAX,
                             msg='The signal strength parameter is greater than the expected value')
        self.assertGreater(unsigned_value, GetRssiResponse.STRENGTH.NRF52_MIN,
                           msg='The signal strength parameter is lower than the expected value')

        self.testCaseChecked("FUN_RCV-B4_0001")
    # end def test_get_rssi

    @features('RcvGetRssi')
    @features('BLEDevicePairing')
    @level('Functionality')
    @services('Debugger')
    def test_get_rssi_all_slots(self):
        """
        Create a inconsistent pairing block by deleting the 0x28 chunk in receiver nvs
         - validate we can unpair the ghost pairing slot
        """
        self.post_requisite_reload_nvs = True

        # Initialize the authentication method parameter
        DevicePairingTestUtils.set_authentication_method(self, self.config_manager)

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Clean-up receiver pairing slot')
        # ---------------------------------------------------------------------------
        DevicePairingTestUtils.unpair_all(self)

        self.pairing_slot_list = []
        current_pairing_slot = None
        for i in range(DevicePairingTestUtils.NvsManager.RECEIVER_PAIRING_SLOT_COUNT-1):
            # Retrieve current device BT address
            self.device_bluetooth_address = DiscoveryTestUtils.discover_device(self)

            if current_pairing_slot is not None:
                # Previous connection is lost when starting the new sequence
                device_connection = ChannelUtils.get_only(test_case=self,
                                                          queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                                          class_type=DeviceConnection)

                device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
                device_info = device_info_class.fromHexList(HexList(device_connection.information))
                assert (to_int(device_info.device_info_link_status) == DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED)
            # end if

            # Pair the discovered device
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Pair the device on the next receiver slot')
            # ----------------------------------------------------------------------------
            current_pairing_slot = DevicePairingTestUtils.pair_device(self, self.device_bluetooth_address)
            self.pairing_slot_list.append(current_pairing_slot)

            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send the Get RSSI request to the dongle')
            # ----------------------------------------------------------------------------
            get_info_resp = ChannelUtils.send(
                test_case=self,
                report=GetRssiRequest(index=current_pairing_slot),
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=GetRssiResponse)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate Get RSSI firmware response')
            # ---------------------------------------------------------------------------
            unsigned_value = int.from_bytes(to_int(get_info_resp.signal_strength).to_bytes(1, 'little'), 'little',
                                            signed=True)
            self.assertLessEqual(unsigned_value, GetRssiResponse.STRENGTH.NRF52_MAX,
                                 msg='The signal strength parameter is greater than the expected value')
            self.assertGreater(unsigned_value, GetRssiResponse.STRENGTH.NRF52_MIN,
                               msg='The signal strength parameter is lower than the expected value')

            if current_pairing_slot == DevicePairingTestUtils.NvsManager.RECEIVER_PAIRING_SLOT_COUNT:
                break
            # end if
        # end for

        # ---------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, 'Clean-up receiver pairing slot')
        # ---------------------------------------------------------------------------
        DevicePairingTestUtils.unpair_all(self)

        self.testCaseChecked("FUN_RCV-B4_0002")
    # end def test_get_rssi_all_slots
# end class GetRssiTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
