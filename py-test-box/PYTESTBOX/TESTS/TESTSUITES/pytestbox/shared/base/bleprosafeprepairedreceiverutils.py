#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.shared.base.bleprosafeprepairedreceiverutils
:brief:  Helpers for BLE Pro Safe Pre Paired Receiver feature
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/07/24
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
import time

from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.features.common.bleproprepairing import BleProPrepairing
from pyhid.hidpp.features.common.bleproprepairing import BleProPrepairingFactory
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetBLEProDevicePairingInfoRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetBLEProDevicePairingInfoResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import NonVolatilePairingInformation
from pyhid.hidpp.hidpp1.registers.performdevicediscovery import PerformDeviceDiscovery
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.device.base.bleproprepairingutils import BleProPrePairingTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.shared.base.bleproreceiverprepairingutils import BleProReceiverPrepairingTestUtils
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.enumerationutils import EnumerationTestUtils
from pytestbox.base.loghelper import LogHelper
from pyusb.libusbdriver import ChannelIdentifier


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class BleProSafePrePairedReceiverTestUtils(CommonBaseTestUtils):
    """
    This class provides helpers for common checks on BLE Pro Safe Pre Paired Receiver feature
    """
    DISCOVERABLE_TIME = 5.0
    PRE_PAIRED_RCV_SEARCH_TIME = 1.0

    @classmethod
    def pre_pairing_sequence(cls, test_case, feature_1816, feature_index_1816, rcv_pre_pairing_slot,
                             ltk_key=None, irk_local_key=None, irk_remote_key=None, csrk_local_key=None,
                             csrk_remote_key=None, log_first_step=0):
        """
        Perform full standard pre pairing sequence for both receiver and device

        :param test_case: The current test case
        :type test_case: ``DeviceBaseTestCase``
        :param feature_1816: Device BLE Pro pre-pairing feature main class
        :type feature_1816: ``BleProPrepairingInterface``
        :param feature_index_1816: 0x1816 HID++ feature index in device mapping table
        :type feature_index_1816: ``int``
        :param rcv_pre_pairing_slot: Receiver slot used for pre pairing
        :type rcv_pre_pairing_slot: ``int``
        :param ltk_key: LTK Key
        :type ltk_key: ``HexList``
        :param irk_local_key: IRK Local Key
        :type irk_local_key: ``HexList``
        :param irk_remote_key: IRK Remote Key
        :type irk_remote_key: ``HexList``
        :param csrk_local_key: CSRK Local Key
        :type csrk_local_key: ``HexList``
        :param csrk_remote_key: CSRK Remote Key
        :type csrk_remote_key: ``HexList``
        :param log_first_step: Log step number, if <= 0 no log printed
        :type log_first_step: ``int``

        :return: Receiver and device address
        :rtype: ``list``
        """
        if log_first_step > 0:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(test_case, 'Enable Test Mode on Receiver')
            # ---------------------------------------------------------------------------
        # end if
        ReceiverTestUtils.HIDppHelper.activate_features(test_case, manufacturing=True)

        if log_first_step > 0:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(test_case, 'Enable Manufacturing Features on Device')
            # ---------------------------------------------------------------------------
        # end if
        DeviceTestUtils.HIDppHelper.activate_features(
            test_case, manufacturing=True, device_index=test_case.original_device_index)

        if log_first_step > 0:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(test_case, 'Run Pre Pairing sequence on Receiver')
            # ---------------------------------------------------------------------------
        # end if
        (receiver_address, device_address, ltk_key, irk_local_key, irk_remote_key, csrk_local_key,
         csrk_remote_key) = BleProReceiverPrepairingTestUtils.receiver_prepairing_sequence(
            test_case, rcv_pre_pairing_slot, ltk_key, irk_local_key, irk_remote_key, csrk_local_key, csrk_remote_key,
            pre_pairing_main_class=feature_1816, pre_pairing_index=feature_index_1816, force_random_data=True)

        if log_first_step > 0:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(test_case, 'Run Pre Pairing sequence on Device')
            # ---------------------------------------------------------------------------
        # end if
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=test_case, pre_pairing_main_class=feature_1816, pre_pairing_index=feature_index_1816,
            long_term_key=ltk_key,
            remote_identity_resolving_key=irk_local_key, local_identity_resolving_key=irk_remote_key,
            remote_connection_signature_resolving_key=csrk_local_key,
            local_connection_signature_resolving_key=csrk_remote_key,
            receiver_address=receiver_address, start=False)

        if log_first_step > 0:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(test_case, 'Reset receiver')
            # ---------------------------------------------------------------------------
        # end if
        ReceiverTestUtils.reset_receiver(test_case)

        ChannelUtils.get_only(
            test_case=test_case, queue_name=HIDDispatcher.QueueName.EVENT, class_type=WirelessDeviceStatusBroadcastEvent,
            check_first_message=False, allow_no_message=True)

        return receiver_address, device_address
    # end def pre_pairing_sequence

    @staticmethod
    def check_prepairing_ble_pro_device_info(test_case, pairing_slot):
        """
        Read BLE Pro device pairing information and check it is pre pairing information

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param pairing_slot: Pre pairing slot
        :type pairing_slot: ``int``
        """
        device_pairing_info_req = GetBLEProDevicePairingInfoRequest(
            NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_PAIRING_INFO_MIN + pairing_slot - 1)

        device_pairing_info_resp = test_case.send_report_wait_response(
            report=device_pairing_info_req,
            response_queue=test_case.hidDispatcher.receiver_response_queue,
            response_class_type=GetBLEProDevicePairingInfoResponse)

        check_map = EnumerationTestUtils.BLEProDevicePairingInfoResponseChecker.get_default_check_map(test_case)
        check_map["pairing_slot"] = (
            EnumerationTestUtils.BLEProDevicePairingInfoResponseChecker.check_pairing_slot,
            NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_PAIRING_INFO_MIN + 1)
        check_map["link_status"] = (
            EnumerationTestUtils.BLEProDevicePairingInfoResponseChecker.check_link_status,
            DeviceConnection.LinkStatus.LINK_ESTABLISHED)
        check_map["prepairing_auth_method"] = (
            EnumerationTestUtils.BLEProDevicePairingInfoResponseChecker.check_prepairing_auth_method, 1)
        check_map["emu_2_buttons_auth_method"] = (
            EnumerationTestUtils.BLEProDevicePairingInfoResponseChecker.check_emu_2_buttons_auth_method, 0)
        check_map["passkey_auth_method"] = (
            EnumerationTestUtils.BLEProDevicePairingInfoResponseChecker.check_passkey_auth_method, 0)

        EnumerationTestUtils.BLEProDevicePairingInfoResponseChecker.check_fields(
            test_case, device_pairing_info_resp, GetBLEProDevicePairingInfoResponse, check_map)
    # end def check_prepairing_ble_pro_device_info

    @classmethod
    def check_device_discoverable(cls, test_case, spy_receiver_port_index):
        """
        Check that a device can be discovered by a receiver, i.e. Device Discovery notifications are received

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param spy_receiver_port_index: Port index of the receiver to use
        :type spy_receiver_port_index: ``int``
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(test_case, 'Start Discovery on spy receiver')
        # ---------------------------------------------------------------------------
        cls.SpyReceiver.start_discovery(test_case, spy_receiver_port_index)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(test_case, 'Check Device Discovery notifications are received while DUT is discoverable')
        # ---------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            test_case, PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE)
        test_case.assertNotNone(
            device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

        cls.SpyReceiver.cancel_discovery(test_case, spy_receiver_port_index)
    # end def check_device_discoverable

    @staticmethod
    def pre_pair_device_to_receiver(test_case):
        """
        Run a safe pre-pairing sequence between the device and the receiver using paring slot 2

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        """
        # Define test values
        test_case.pre_paired_receiver_port_index = ChannelUtils.get_port_index(test_case=test_case)
        test_case.rcv_prepairing_slot = 0x02
        test_case.ltk_key = RandHexList(16)
        test_case.irk_local_key = RandHexList(16)
        test_case.irk_remote_key = RandHexList(16)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(test_case, "Cleanup all pairing slots except the first one")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.NvsManager.clean_pairing_data(test_case)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(test_case, "Get feature 1816 index")
        # --------------------------------------------------------------------------------------------------------------
        if test_case.current_channel != test_case.backup_dut_channel:
            DeviceManagerUtils.set_channel(test_case=test_case, new_channel=test_case.backup_dut_channel)
        # end if
        DeviceBaseTestUtils.HIDppHelper.get_parameters(
            test_case, feature_id=BleProPrepairing.FEATURE_ID, factory=BleProPrepairingFactory)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case, "Pre Pair Receiver with Device")
        # --------------------------------------------------------------------------------------------------------------
        # noinspection PyUnresolvedReferences
        test_case.receiver_address, test_case.device_address = \
            BleProSafePrePairedReceiverTestUtils.pre_pairing_sequence(
                test_case,
                test_case.feature_1816,
                test_case.feature_1816_index,
                test_case.rcv_prepairing_slot,
                test_case.ltk_key,
                test_case.irk_local_key,
                test_case.irk_remote_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case, "Change host on Device")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.change_host_by_link_state(
            test_case, link_state=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED, clean_device_connection_event=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case, "Wait for device to be connected")
        # --------------------------------------------------------------------------------------------------------------
        DeviceManagerUtils.set_channel(test_case=test_case,
                                       new_channel_id=ChannelIdentifier(
                                           port_index=ChannelUtils.get_port_index(test_case=test_case),
                                           device_index=test_case.rcv_prepairing_slot),
                                       open_channel=False)
        ChannelUtils.wait_for_channel_device_to_be_connected(test_case=test_case)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case, "Verify an HID report can be received")
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(test_case)
    # end def pre_pair_device_to_receiver

    class SpyReceiver:
        """
        Class to provide interface to spy receiver
        """
        @staticmethod
        def start_discovery(test_case, spy_receiver_port_index,
                            timeout=PerformDeviceDiscovery.DiscoveryTimeout.USE_DEFAULT):
            """
            Start discovery

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param spy_receiver_port_index: Spy receiver port index
            :type spy_receiver_port_index: ``int``
            :param timeout: Discovery timeout
            :type timeout: ``int``
            """
            ReceiverTestUtils.switch_to_receiver(test_case, spy_receiver_port_index)
            test_case.enable_hidpp_reporting()
            DiscoveryTestUtils.start_discovery(test_case, timeout)
        # end def start_discovery

        @staticmethod
        def cancel_discovery(test_case, spy_receiver_port_index):
            """
            Cancel discovery

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param spy_receiver_port_index: Spy receiver port index
            :type spy_receiver_port_index: ``int``
            """
            ReceiverTestUtils.switch_to_receiver(test_case, spy_receiver_port_index)
            DiscoveryTestUtils.cancel_discovery(test_case)
        # end def cancel_discovery

        @staticmethod
        def pair_device(test_case, spy_receiver_port_index, bluetooth_address):
            """
            Pair device

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param spy_receiver_port_index: Spy receiver port index
            :type spy_receiver_port_index: ``int``
            :param bluetooth_address: Device bluetooth address
            :type bluetooth_address: ``HexList``

            :return: the pairing slot allocated by the receiver
            :rtype: ``int``
            """
            ReceiverTestUtils.switch_to_receiver(test_case, spy_receiver_port_index)
            return DevicePairingTestUtils.pair_device(test_case, bluetooth_address)
        # end def pair_device

        @ staticmethod
        def unpair_all(test_case, spy_receiver_port_index):
            """
            Unpair all slots

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param spy_receiver_port_index: Spy receiver port index
            :type spy_receiver_port_index: ``int``
            """
            if spy_receiver_port_index is not None:
                ReceiverTestUtils.switch_to_receiver(test_case, spy_receiver_port_index)
                DevicePairingTestUtils.unpair_all(test_case, first_slot=1)
            # end if
        # end def unpair_all

        @staticmethod
        def failed_pairing_sequence(test_case, spy_receiver_port_index, bluetooth_address):
            """
            Perform a pairing sequence with a failure

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param spy_receiver_port_index: Spy receiver port index
            :type spy_receiver_port_index: ``int``
            :param bluetooth_address: Device bluetooth address
            :type bluetooth_address: ``HexList``
            """
            ReceiverTestUtils.switch_to_receiver(test_case, spy_receiver_port_index)
            # Send 'Perform device connection' request with Connect Devices = 1 (i.e Pairing)
            DevicePairingTestUtils.start_pairing_sequence(test_case, bluetooth_address)

            # Wait for a start pairing status notification
            DevicePairingTestUtils.PairingChecker.check_start_pairing_status(test_case)

            # Wait for a display passkey notification
            passkey_digits = DevicePairingTestUtils.PairingChecker.get_passkey_digits(test_case)

            # Wait for a 'Digit Start' passkey notification
            DevicePairingTestUtils.PairingChecker.get_display_passkey_start(test_case)

            # Pass key corruption
            passkey_digits >>= 1

            # Loop over passkey inputs list provided by the receiver
            DevicePairingTestUtils.generate_keystrokes(test_case, passkey_digits)

            # User enters the last passkey input
            DevicePairingTestUtils.generate_end_of_sequence(test_case)

            # Wait for a failed pairing status notification
            DevicePairingTestUtils.PairingChecker.check_failed_pairing_status(test_case)
        # end def failed_pairing_sequence

        @staticmethod
        def timeout_pairing_sequence(test_case, spy_receiver_port_index, bluetooth_address):
            """
            Perform a pairing sequence with a timeout

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param spy_receiver_port_index: Spy receiver port index
            :type spy_receiver_port_index: ``int``
            :param bluetooth_address: Device bluetooth address
            :type bluetooth_address: ``HexList``
            """
            ReceiverTestUtils.switch_to_receiver(test_case, spy_receiver_port_index)
            # Send 'Perform device connection' request with Connect Devices = 1 (i.e Pairing)
            DevicePairingTestUtils.start_pairing_sequence(test_case, bluetooth_address)

            # Wait for a start pairing status notification
            DevicePairingTestUtils.PairingChecker.check_start_pairing_status(test_case)

            # Wait for a display passkey notification
            DevicePairingTestUtils.PairingChecker.get_passkey_digits(test_case)

            # Wait for a 'Digit Start' passkey notification
            DevicePairingTestUtils.PairingChecker.get_display_passkey_start(test_case)

            time.sleep(DevicePairingTestUtils.PAIRING_TIMEOUT)

            # Wait for a timeout pairing status notification
            DevicePairingTestUtils.PairingChecker.check_timeout_pairing_status(test_case)
        # end def timeout_pairing_sequence
    # end class SpyReceiver
# end class BleProSafePrePairedRcvTestUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
