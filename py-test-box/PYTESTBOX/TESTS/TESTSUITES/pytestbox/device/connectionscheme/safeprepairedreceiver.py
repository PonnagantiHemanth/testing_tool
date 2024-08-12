#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.connectionscheme.safeprepairedreceiver
:brief: Validate Safe Prepaired Receiver feature
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/08/07
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import time
from contextlib import contextmanager
from unittest import expectedFailure

from pychannel.channelinterfaceclasses import LinkEnablerInfo
from pychannel.throughreceiverchannel import ThroughBleProReceiverChannel
from pychannel.throughreceiverchannel import ThroughReceiverChannel
from pychannel.usbchannel import UsbChannel
from pyharness.core import TestException
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.batterylevelscalibration import BatteryLevelsCalibration
from pyhid.hidpp.features.common.bleproprepairing import BleProPrepairing
from pyhid.hidpp.features.common.bleproprepairing import BleProPrepairingFactory
from pyhid.hidpp.features.common.configurabledeviceproperties import ConfigurableDeviceProperties
from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pyhid.hidpp.features.common.deviceinformation import DeviceInformationFactory
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuth
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuthFactory
from pyhid.hidpp.features.common.oobstate import OobState
from pyhid.hidpp.features.common.passwordauthentication import PasswordAuthentication
from pyhid.hidpp.features.common.tdeaccesstonvm import TdeAccessToNvm
from pyhid.hidpp.features.common.unifiedbattery import UnifiedBattery
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatus
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.features.devicereset import DeviceReset
from pyhid.hidpp.features.devicereset import ForceDeviceReset
from pyhid.hidpp.features.enablehidden import EnableHidden
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.features.hireswheel import HiResWheel
from pyhid.hidpp.features.root import Root
from pyhid.hidpp.features.root import RootFactory
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.notifications.devicediscovery import DeviceDiscovery
from pyhid.hidpp.hidpp1.notifications.discoverystatus import DiscoveryStatus
from pyhid.hidpp.hidpp1.notifications.linkqualityinfo import LinkQualityInfoShort
from pyhid.hidpp.hidpp1.registers.nonvolatilememoryaccess import GetNonVolatileMemoryAccessRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilememoryaccess import GetNonVolatileMemoryAccessResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilememoryaccess import SetNonVolatileMemoryAccessRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilememoryaccess import SetNonVolatileMemoryAccessResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetBLEProDevicePairingInfoRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetBLEProDevicePairingInfoResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import NonVolatilePairingInformation
from pyhid.hidpp.hidpp1.registers.performdevicediscovery import PerformDeviceDiscovery
from pyhid.hidpp.hidpp1.registers.prepairingdata import PrepairingData
from pyhid.hidpp.hidpp1.registers.prepairingmanagement import PrepairingManagement
from pyhid.hidpp.hidpp1.registers.reset import SetResetRequest
from pyhid.hidpp.hidpp1.registers.testmodecontrol import TestModeControl
from pylibrary.emulator.emulatorinterfaces import HOST
from pylibrary.mcu.connectchunks import ConnectIdChunkData
from pylibrary.mcu.nrf52.blenvschunks import BleNvsChunks
from pylibrary.tools.bitstruct import BitStruct
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleproprepairingutils import BleProPrePairingTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicemanagedeactivatablefeaturesauthutils import \
    DeviceManageDeactivatableFeaturesAuthTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.unifiedbatteryutils import UnifiedBatteryTestUtils
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.shared.base.bleproreceiverprepairingutils import BleProReceiverPrepairingTestUtils
from pytestbox.shared.base.bleprosafeprepairedreceiverutils import BleProSafePrePairedReceiverTestUtils
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.enumerationutils import EnumerationTestUtils
from pytestbox.shared.base.tdeutils import TDETestUtils
from pytransport.transportcontext import TransportContextException
from pytransport.usb.usbconstants import LogitechReceiverProductId
from pyusb.libusbdriver import ChannelIdentifier
from pyusb.libusbdriver import LibusbDriver


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ConnectionSchemeTestCaseMixin(DeviceBaseTestCase):
    """
    Connection Scheme TestCase Mixin
    """
    # ------------------------------------------------------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------------------------------------------------------
    class DeviceSlotState:
        """
        Device slot state information
        """
        current_slot = None
        slot_1_state = None
        slot_2_state = None
        slot_3_state = None
    # end class DeviceSlotState

    # ------------------------------------------------------------------------------------------------------------------
    # Public functions
    # ------------------------------------------------------------------------------------------------------------------
    def setUp(self):
        """
        Handles test prerequisites.
        """
        super().setUp()

        self.feature_1816 = None
        self.feature_1816_index = None
        self.rcv_prepairing_slot = None
        self.ltk_key = None
        self.irk_local_key = None
        self.irk_remote_key = None
        self.device_address = None
        self.receiver_address = None
        self.pre_paired_receiver_port_index = ChannelUtils.get_port_index(test_case=self)
        self.spy_receiver_port_index = self._get_spy_receiver_port_index()
        self.gotthard_receiver_port_index = None
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.NvsHelper.backup_nvs(self)
    # end def setUp

    # ------------------------------------------------------------------------------------------------------------------
    # Private functions
    # ------------------------------------------------------------------------------------------------------------------
    def _get_spy_receiver_port_index(self):
        """
        Search an other receiver of same type which can be used as a spy

        :return: Spy receiver port index
        :rtype: ``int``
        """
        spy_receiver_port_index = None
        ble_pro_receivers_pids = LogitechReceiverProductId.ble_pro_pids()
        for ble_pro_receivers_pid in ble_pro_receivers_pids:
            spy_receiver_port_index = ReceiverTestUtils.get_receiver_port_index(
                self, ble_pro_receivers_pid, skip=[self.pre_paired_receiver_port_index])
            if spy_receiver_port_index is not None:
                break
            # end if
        # end for
        return spy_receiver_port_index
    # end def _get_spy_receiver_port_index

    def _get_gotthard_receiver_port_index(self):
        """
        Search first available Gotthard receiver

        :return: Gothard receiver port index
        :rtype: ``int``
        """
        return ReceiverTestUtils.get_receiver_port_index(self, ReceiverTestUtils.USB_PID_GOTTHARD)
    # end def _get_gotthard_receiver_port_index

    def _pre_pair_receiver_with_device(self):
        """
        Pre Pair Receiver with Device

        :return: Receiver and device address
        :rtype: ``list``
        """
        value = BleProSafePrePairedReceiverTestUtils.pre_pairing_sequence(
            self,
            self.feature_1816,
            self.feature_1816_index,
            self.rcv_prepairing_slot,
            self.ltk_key,
            self.irk_local_key,
            self.irk_remote_key, )
        return value
    # end def _pre_pair_receiver_with_device

    def _pair_slot_2_to_second_receiver(self):
        """
        Pre-requisite pair slot_2
        """
        host_index = 1
        DeviceBaseTestUtils.NvsHelper.change_host(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.NONE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(self, self.spy_receiver_port_index)

        # Fetch Device USB Descriptors matching the spy receiver interfaces configuration
        ChannelUtils.get_descriptors(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(
            self, 'Check Device Discovery notifications are received while DUT is discoverable')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
        self.assertNotNone(
            device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair device with second receiver')
        # --------------------------------------------------------------------------------------------------------------
        # noinspection PyUnresolvedReferences
        # bluetooth_address is part of the data in device discovery notification part 0
        device_index = BleProSafePrePairedReceiverTestUtils.SpyReceiver.pair_device(
            self,
            self.spy_receiver_port_index,
            device_discovery[DeviceDiscovery.PART.CONFIGURATION].data.bluetooth_address)

        DevicePairingTestUtils.check_connection_status(
            self, device_index, DeviceConnection.LinkStatus.LINK_ESTABLISHED)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check User action -> Button')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)
    # end def _pair_slot_2_to_second_receiver

    def _pair_to_second_receiver(self, slot=2):
        """
        Pre-requisite pair slot_1

        :param slot: Device pairing slot
        :rtype: ``int``
        """
        host_index = slot - 1
        DeviceBaseTestUtils.NvsHelper.change_host(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.NONE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(self, self.spy_receiver_port_index)

        # Fetch Device USB Descriptors matching the spy receiver interfaces configuration
        ChannelUtils.get_descriptors(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self, PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE)
        self.assertNotNone(
            device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Pair device with second receiver')
        # --------------------------------------------------------------------------------------------------------------
        # noinspection PyUnresolvedReferences
        # bluetooth_address is part of the data in device discovery notification part 0
        device_index = BleProSafePrePairedReceiverTestUtils.SpyReceiver.pair_device(
            self,
            self.spy_receiver_port_index,
            device_discovery[DeviceDiscovery.PART.CONFIGURATION].data.bluetooth_address)

        DevicePairingTestUtils.check_connection_status(
            self, device_index, DeviceConnection.LinkStatus.LINK_ESTABLISHED)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check User action -> Button')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.device_nvs_host_index = host_index
    # end def _pair_to_second_receiver

    def _read_pairing_slot_status(self):
        """
        Read device slots connections status
        -> current used slot
        -> slot_x empty(0), paired(1), pre-paired(2)

        :return: Device slot state information
        :rtype: ``DeviceSlotState``
        """
        self.memory_manager.read_nvs()
        connect_id_chunk_list = self.memory_manager.get_active_chunk_by_name('NVS_CONNECT_ID')
        current_slot = int(Numeral(connect_id_chunk_list.data.host_index))
        slot_1_state = int(Numeral(getattr(connect_id_chunk_list.data, f'pairing_src_0')))
        if hasattr(connect_id_chunk_list.data, 'pairing_src_1'):
            slot_2_state = int(Numeral(getattr(connect_id_chunk_list.data, f'pairing_src_1')))
        else:
            slot_2_state = 0
        # end if
        if hasattr(connect_id_chunk_list.data, 'pairing_src_2'):
            slot_3_state = int(Numeral(getattr(connect_id_chunk_list.data, f'pairing_src_2')))
        else:
            slot_3_state = 0
        # end if
        self.DeviceSlotState.current_slot = current_slot
        self.DeviceSlotState.slot_1_state = slot_1_state
        self.DeviceSlotState.slot_2_state = slot_2_state
        self.DeviceSlotState.slot_3_state = slot_3_state
        return self.DeviceSlotState
    # end def _read_pairing_slot_status

    def _turn_on_pre_paired_rcv(self):
        """
        plug the pre-paired receiver and re-launch hidpp reading

        :return: Device index
        :rtype: ``int``
        """
        device_index = self.rcv_prepairing_slot
        self.channel_enable(self.pre_paired_receiver_port_index, wait_time=2.0, wait_device_notification=False)
        return device_index
    # end def _turn_on_pre_paired_rcv

    def _turn_off_pre_paired_rcv(self):
        """
        clean pre-paired receiver unplug
        """
        ChannelUtils.close_channel(test_case=self)
        LibusbDriver.disable_usb_port(port_index=self.pre_paired_receiver_port_index)
    # end def _turn_off_pre_paired_rcv

    def _check_pre_pairing_ble_bond_id_chunk_in_nvs(self, host_index=0, chunk_index=-1):
        """
        Verify NVS BLE Bond Id chunk presence and contents

        :param host_index: Device pairing slot
        :type host_index: ``int``
        :param chunk_index: chunk position in history (-1 for the last one)
        :rtype: ``int``
        """
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=host_index)

        self.assertEqual(obtained=ble_bond_id_chunks[chunk_index].master_bluetooth_address,
                         expected=self.receiver_address,
                         msg='Master Bluetooth Address in NVS should be the Receiver Address')
        self.assertEqual(obtained=ble_bond_id_chunks[chunk_index].bluetooth_low_energy_address.device_bluetooth_address,
                         expected=self.device_address,
                         msg='Device Bluetooth Address in NVS should be the Device Address')
        self.assertEqual(obtained=ble_bond_id_chunks[chunk_index].local_ble_gap_enc_info.enc_info_long_term_key,
                         expected=BleProPrePairingTestUtils.get_key(self, 'long_term_key'),
                         msg='LTK Key should be the pre pairing one')
        self.assertEqual(obtained=ble_bond_id_chunks[chunk_index].remote_identity_key.identity_resolving_key,
                         expected=BleProPrePairingTestUtils.get_key(self, 'remote_identity_resolving_key'),
                         msg='IRK Remote Key should be the pre pairing one')
        self.assertEqual(obtained=ble_bond_id_chunks[chunk_index].local_identity_key.identity_resolving_key,
                         expected=BleProPrePairingTestUtils.get_key(self, 'local_identity_resolving_key'),
                         msg='IRK Local Key should be the pre pairing one')
        # Check BLE Pro Attributes - latency removal bit on the last occurence
        self.assertEqual(
            obtained=ble_bond_id_chunks[chunk_index].ble_pro_attributes.ble_pro_attr_suppress_first_report_latency_bit,
            expected=1,
            msg='BLE Pro Attr Suppress First Report Latency Bit in NVS shall be set')
        if self.f.SHARED.PAIRING.F_BLEProOsDetection:
            # Check OS detected type on the last occurence
            self.assertEqual(obtained=int(Numeral(ble_bond_id_chunks[chunk_index].os_detected_type)),
                             expected=BleNvsChunks.OsDetectedType.LOGITECH_BLE_PRO,
                             msg='The OS detected type shall match the Logitech BLE Pro constant')
        else:
            self.assertEqual(obtained=int(Numeral(ble_bond_id_chunks[chunk_index].os_detected_type)),
                             expected=BleNvsChunks.OsDetectedType.UNDETERMINED,
                             msg='The OS detected type shall keep its initial value')
        # end if
    # end def _check_pre_pairing_ble_bond_id_chunk_in_nvs

    def _check_ble_pro_device_pairing_information(self):
        device_pairing_info_resp = EnumerationTestUtils.get_device_pairing_information(
            test_case=self, pairing_slot=self.rcv_prepairing_slot)

        check_map = EnumerationTestUtils.BLEProDevicePairingInfoResponseChecker.get_default_check_map(self)
        check_map["pairing_slot"] = (
            EnumerationTestUtils.BLEProDevicePairingInfoResponseChecker.check_pairing_slot,
            NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_PAIRING_INFO_MIN + self.rcv_prepairing_slot - 1)
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
            self, device_pairing_info_resp, GetBLEProDevicePairingInfoResponse, check_map)
    # end def _check_ble_pro_device_pairing_information

    def _check_device_discovery_notifications_are_received_while_dut_is_discoverable(self):
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self, PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE)
        self.assertNotNone(
            device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

        BleProSafePrePairedReceiverTestUtils.SpyReceiver.cancel_discovery(self, self.spy_receiver_port_index)
        return device_discovery
    # end def _check_device_discovery_notifications_are_received_while_dut_is_discoverable

    def _enter_discoverable_mode(self, channel_id=HOST.CH2, click_count=1):
        """
        Enter into pairing mode on the given channel

        :param channel_id: targeted channel index
        :type channel_id: ``int``
        :param click_count: number of click on the Connect button
        :type click_count: ``int``
        """
        if self.config_manager.current_device_type == ConfigurationManager.DEVICE_TYPE.MOUSE:
            time.sleep(1)
            self.button_stimuli_emulator.user_action()
            time.sleep(.05)
            for _ in range(click_count):
                # Enter discoverable mode on the next channel
                self.button_stimuli_emulator.change_host()
                time.sleep(.05)
            # end for
        # end if
        self.button_stimuli_emulator.enter_pairing_mode(host_index=channel_id)
    # end def _enter_discoverable_mode

    def _force_host_to_oob_state_in_nvs(self):
        """
        Switch the current host in NVS chunk and force it to OOB state
        """
        self.memory_manager.read_nvs()
        self.memory_manager.switch_to_host_id(host_id=self.device_nvs_host_index, is_test_setup=False, force_oob=True)
        self.memory_manager.load_nvs()
    # end def _force_host_to_oob_state_in_nvs
# end class ConnectionSchemeTestCaseMixin


class SafePrePairedRcvrTestCase(ConnectionSchemeTestCaseMixin):
    """
    Device Safe Pre Paired Receiver TestCases
    """
    # TDE business case maximum accepted duration (in seconds)
    # Note : As no hard limit is defined so far, it has been set based on first test executions
    TDE_MAX_DURATION = 14.0
    MAX_LOOP_COUNT = 10

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()
        assert self.spy_receiver_port_index is not None
        assert self.pre_paired_receiver_port_index is not None

        # Cleanup all pairing slots except the first one
        DevicePairingTestUtils.NvsManager.clean_pairing_data(self)
        self.device_nvs_host_index = 1 if self.f.PRODUCT.DEVICE.F_NbHosts > 1 else 0
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.unpair_all(self, self.spy_receiver_port_index)
        # Note that if we do not close the channel here, we got 3 receiver * 4 interfaces opened at the
        # same time and we do not receive the HID event when emulating a user action
        # FIXME : To be removed when the HID device layer is available
        ChannelUtils.close_channel(test_case=self)

        # Get the feature under test
        DeviceManagerUtils.set_channel(
            test_case=self,
            new_channel_id=ChannelIdentifier(
                port_index=self.pre_paired_receiver_port_index, device_index=self.original_device_index))
        self.feature_1816_index = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=BleProPrepairing.FEATURE_ID)
        self.feature_1816 = BleProPrepairingFactory.create(
            ChannelUtils.get_feature_version(test_case=self, feature_index=self.feature_1816_index))

        # Define test values
        self.rcv_prepairing_slot = 0x02
        self.ltk_key = HexList('000102030405060708090A0B0C0D0E0F')
        self.irk_local_key = HexList('101112131415161718191A1B1C1D1E1F')
        self.irk_remote_key = HexList('202122232425262728292A2B2C2D2E2F')

        # Initialize the authentication method parameter
        DevicePairingTestUtils.set_authentication_method(self, self.config_manager)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Setup End')
        # --------------------------------------------------------------------------------------------------------------
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Start Tear Down')
        # --------------------------------------------------------------------------------------------------------------
        # noinspection PyBroadException
        try:
            if hasattr(self, "spy_receiver_port_index") and self.spy_receiver_port_index is not None:
                BleProSafePrePairedReceiverTestUtils.SpyReceiver.cancel_discovery(self, self.spy_receiver_port_index)
                BleProSafePrePairedReceiverTestUtils.SpyReceiver.unpair_all(self, self.spy_receiver_port_index)
            # end if

            ChannelUtils.clean_messages(
                test_case=self,
                channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                class_type=(DeviceDiscovery, DiscoveryStatus))

            if hasattr(self, "pre_paired_receiver_port_index") and self.pre_paired_receiver_port_index is not None:
                self.device.enable_usb_port(self.pre_paired_receiver_port_index)
                assert self.channel_switch(device_uid=ChannelIdentifier(
                    port_index=self.pre_paired_receiver_port_index, device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER)), \
                    "Could not connect to receiver"
            # end if

            DevicePairingTestUtils.unpair_all(test_case=self)
        except Exception:
            self.log_traceback_as_warning(
                supplementary_message="Exception in tearDown (pre-paired receiver dedicated part):")
        # end try

        # noinspection PyBroadException
        try:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, "Reload initial NVS")
            # ----------------------------------------------------------------------------------------------------------
            CommonBaseTestUtils.NvsHelper.restore_nvs(self)
            time.sleep(2)
            assert self.channel_switch(device_uid=ChannelIdentifier(
                port_index=self.pre_paired_receiver_port_index, device_index=self.original_device_index)), \
                "Could not connect to device"
            ChannelUtils.get_only(
                test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, class_type=WirelessDeviceStatusBroadcastEvent,
                check_first_message=False, allow_no_message=True)
        except Exception:
            self.log_traceback_as_warning(supplementary_message="Exception in tearDown (spy receiver dedicated part):")
        # end try

        # noinspection PyBroadException
        try:
            if self.gotthard_receiver_port_index is not None:
                # Remove all channels related to the gotthard receiver
                DeviceManagerUtils.remove_channel_from_cache(
                    test_case=self, port_index=self.gotthard_receiver_port_index)
            # end if
        except Exception:
            self.log_traceback_as_warning(supplementary_message="Exception in tearDown:")
        # end try

        super().tearDown()
    # end def tearDown

    def _pre_pairing_channel_1(self, check_connection=False):
        """
        Complete the pairing with the pre-paired receiver on channel 1
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pre Pair Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        self.receiver_address, self.device_address = BleProSafePrePairedReceiverTestUtils.pre_pairing_sequence(
            self,
            self.feature_1816,
            self.feature_1816_index,
            self.rcv_prepairing_slot,
            self.ltk_key,
            self.irk_local_key,
            self.irk_remote_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force CH1 in OOB state on Device')
        # --------------------------------------------------------------------------------------------------------------
        self.device_nvs_host_index = 0
        self._force_host_to_oob_state_in_nvs()

        if check_connection:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the connection')
            # ----------------------------------------------------------------------------------------------------------
            DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

            DevicePairingTestUtils.check_connection_status(
                self, self.rcv_prepairing_slot, DeviceConnection.LinkStatus.LINK_ESTABLISHED,
                log_step=True, log_check=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
            # ----------------------------------------------------------------------------------------------------------
            self.memory_manager.read_nvs()
            DeviceBaseTestUtils.NvsHelper.check_connect_id(
                self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.MFG)
        # end if
    # end def _pre_pairing_channel_1

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @features('MultipleChannels', HOST.CH2)
    @level('Business')
    @services('MultiHost')
    @services('Debugger')
    def test_empty_slot_business(self):
        """
        Check device connects on pre-paired receiver when slot CH2 is empty and pre-paired receiver is in range
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pre Pair Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        self.receiver_address, self.device_address = BleProSafePrePairedReceiverTestUtils.pre_pairing_sequence(
            self,
            self.feature_1816,
            self.feature_1816_index,
            self.rcv_prepairing_slot,
            self.ltk_key,
            self.irk_local_key,
            self.irk_remote_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Switch to CH2 host on Device')
        # --------------------------------------------------------------------------------------------------------------
        prepaired_channel = DeviceManagerUtils.get_channel(test_case=self, channel_id=ChannelIdentifier(
            port_index=self.pre_paired_receiver_port_index, device_index=self.rcv_prepairing_slot))
        tries_counter = 5
        ChannelUtils.empty_queue(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT)
        while tries_counter > 0 and not prepaired_channel.is_device_connected(force_refresh_cache=True):
            DevicePairingTestUtils.change_host_by_link_state(
                self, link_state=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED)
            time.sleep(2)
            tries_counter -= 1
        # end while

        assert tries_counter > 0, "Failed to switch on CH2"

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on Spy Receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(self, self.spy_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check DUT is never discoverable')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self,
            max(BleProSafePrePairedReceiverTestUtils.PRE_PAIRED_RCV_SEARCH_TIME,
                float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)),
            max_tries=1,
            raise_err=False
        )
        self.assertNone(device_discovery, 'No discovery notifications should have been received')

        BleProSafePrePairedReceiverTestUtils.SpyReceiver.cancel_discovery(self, self.spy_receiver_port_index)
        ReceiverTestUtils.switch_to_receiver(self, self.pre_paired_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.MFG)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check BLE Bond Id Chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self._check_pre_pairing_ble_bond_id_chunk_in_nvs(host_index=self.device_nvs_host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a user action')
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        DevicePairingTestUtils.check_connection_status(
            self, self.rcv_prepairing_slot, DeviceConnection.LinkStatus.LINK_ESTABLISHED, log_step=True, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Read BLE Pro device pairing information')
        # --------------------------------------------------------------------------------------------------------------
        device_pairing_info_resp = EnumerationTestUtils.get_device_pairing_information(
            test_case=self, pairing_slot=self.rcv_prepairing_slot)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check BLE Pro device pairing information')
        # --------------------------------------------------------------------------------------------------------------
        check_map = EnumerationTestUtils.BLEProDevicePairingInfoResponseChecker.get_default_check_map(self)
        check_map["pairing_slot"] = (
            EnumerationTestUtils.BLEProDevicePairingInfoResponseChecker.check_pairing_slot,
            NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_PAIRING_INFO_MIN + self.rcv_prepairing_slot - 1)
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
            self, device_pairing_info_resp, GetBLEProDevicePairingInfoResponse, check_map)

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0001#1")
    # end def test_empty_slot_business

    class Timer:
        """
        Timer class to measure timings
        """
        def __init__(self, section_name):
            """
            Constructor

            :param section_name: Name of the section
            :type section_name: ``str``
            """
            self._section_name = section_name
            self._start_time = time.perf_counter()
            self._end_time = None
        # end def __init__

        def __str__(self):
            """
            Converts the current object to a readable string.

            :return: The current object, as a string.
            :rtype: ``str``
            """
            return f'{self._section_name} duration : {self.get()}'
        # end def __str__

        def stop(self):
            """
            Stop the measurement and return end time

            :return: timing with ns resolution
            :rtype: ``float``
            """
            self._end_time = time.perf_counter()
            return self._end_time
        # end def stop

        def get(self):
            """
            Get the time measurement

            :return: timing with ns resolution
            :rtype: ``float``
            """
            if self._end_time is None:
                return time.perf_counter() - self._start_time
            else:
                return self._end_time - self._start_time
            # end if
        # end def get
    # end class Timer

    @contextmanager
    def time_tracking(self, section_name="Section", times_list=None):
        """
        Enable time measurement of a section

        :param section_name: Section name
        :type section_name: ``str``
        :param times_list: Times tracking list if the section is part of a longer sequence (None if not used) - OPTIONAL
        :type times_list: ``list``
        """
        timer = self.Timer(section_name)
        try:
            yield timer
        finally:
            timer.stop()
            if times_list is not None:
                times_list.append(timer.get())
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case=self, msg=str(timer))
            # ----------------------------------------------------------------------------------------------------------
        # end try
    # end def time_tracking

    def _tde_nominal_case(self):
        """
        TDE nominal case
        """
        features_list = [
            DeviceInformation.FEATURE_ID,
            EnableHidden.FEATURE_ID,
            ManageDeactivatableFeaturesAuth.FEATURE_ID,
            PasswordAuthentication.FEATURE_ID,
            TdeAccessToNvm.FEATURE_ID,
            0x1803,  # GPio Access
            ConfigurableDeviceProperties.FEATURE_ID,
            BatteryLevelsCalibration.FEATURE_ID,
            0x2111,  # FreeRatchet
            HiResWheel.FEATURE_ID,
            0x9205,  # MLX903X
            0x9300,  # EPMDrive
            0x18A1,  # LEDTest
            OobState.FEATURE_ID,
            BleProPrepairing.FEATURE_ID,
            DeviceReset.FEATURE_ID
        ]
        gotthard_device_index = 0x01
        timers_results = []

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Connect to Gotthard receiver')
        # --------------------------------------------------------------------------------------------------------------
        ReceiverTestUtils.switch_to_receiver(
            self,
            self.gotthard_receiver_port_index,
            task_enabler=ReceiverTestUtils.GotthardReceiver.GOTTHARD_TASK_ENABLER)
        with self.time_tracking("Gotthard connection", timers_results):
            try:
                ReceiverTestUtils.GotthardReceiver.init_connection(self)
            except TestException as e:
                self.log_warning(f'Gotthard receiver initialization failed with {e}. Reset the receiver via usb hub')
                try:
                    ChannelUtils.close_channel(test_case=self)
                    LibusbDriver.disable_usb_port(port_index=LibusbDriver.GOTTHARD)
                finally:
                    LibusbDriver.enable_usb_port(port_index=LibusbDriver.GOTTHARD)
                # end try
                ReceiverTestUtils.switch_to_receiver(
                    self,
                    self.gotthard_receiver_port_index,
                    task_enabler=ReceiverTestUtils.GotthardReceiver.GOTTHARD_TASK_ENABLER)
                ReceiverTestUtils.GotthardReceiver.init_connection(self)
            # end try
        # end with

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_title_2(self, 'Update feature mapping (Gotthard)')
        # --------------------------------------------------------------------------------------------------------------
        root_feature = RootFactory.create(self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.IMPORTANT.ROOT))
        DeviceBaseTestUtils.HIDppHelper.get_feature_index(
            self, EnableHidden.FEATURE_ID, gotthard_device_index, self.gotthard_receiver_port_index)
        DeviceBaseTestUtils.HIDppHelper.get_feature_index(
            self, WirelessDeviceStatus.FEATURE_ID, gotthard_device_index, self.gotthard_receiver_port_index)
        DeviceBaseTestUtils.HIDppHelper.get_feature_index(
            self, OobState.FEATURE_ID, gotthard_device_index, self.gotthard_receiver_port_index)
        ufy_device_info_idx = DeviceBaseTestUtils.HIDppHelper.get_feature_index(
            self, DeviceInformation.FEATURE_ID, gotthard_device_index, self.gotthard_receiver_port_index)
        ufy_device_reset_feature_id = DeviceBaseTestUtils.HIDppHelper.get_feature_index(
            self, DeviceReset.FEATURE_ID, gotthard_device_index, self.gotthard_receiver_port_index)
        ufy_feature_index_1816 = DeviceBaseTestUtils.HIDppHelper.get_feature_index(
            self, BleProPrepairing.FEATURE_ID, gotthard_device_index, self.gotthard_receiver_port_index)
        ufy_manage_deact_idx = DeviceBaseTestUtils.HIDppHelper.get_feature_index(
            test_case=self, feature_id=ManageDeactivatableFeaturesAuth.FEATURE_ID, device_index=gotthard_device_index,
            port_index=self.gotthard_receiver_port_index, skip_not_found=True)
        DeviceBaseTestUtils.HIDppHelper.get_feature_index(
            self, PasswordAuthentication.FEATURE_ID, gotthard_device_index, self.gotthard_receiver_port_index)

        ufy_feature_1816 = BleProPrepairingFactory.create(
            ChannelUtils.get_feature_version(
                test_case=self, feature_index=ufy_feature_index_1816,
                channel=DeviceManagerUtils.get_channel(test_case=self, channel_id=ChannelIdentifier(
                    port_index=gotthard_device_index,
                    device_index=self.gotthard_receiver_port_index))))
        ufy_device_info = DeviceInformationFactory.create(
            ChannelUtils.get_feature_version(
                test_case=self, feature_index=ufy_device_info_idx,
                channel=DeviceManagerUtils.get_channel(test_case=self, channel_id=ChannelIdentifier(
                    port_index=gotthard_device_index,
                    device_index=self.gotthard_receiver_port_index))))
        ufy_feature_1e02 = ManageDeactivatableFeaturesAuthFactory.create(
            ChannelUtils.get_feature_version(
                test_case=self, feature_index=ufy_manage_deact_idx,
                channel=DeviceManagerUtils.get_channel(test_case=self, channel_id=ChannelIdentifier(
                    port_index=gotthard_device_index,
                    device_index=self.gotthard_receiver_port_index))))

        # Read RSSI not available yet in framework

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get features (Gotthard)')
        # --------------------------------------------------------------------------------------------------------------
        with self.time_tracking("Get features (Gotthard)", timers_results):
            for feature_id in features_list:
                with self.time_tracking(f"Get feature {feature_id}"):
                    ChannelUtils.send(
                        test_case=self,
                        report=root_feature.get_feature_cls(deviceIndex=gotthard_device_index, featureId=feature_id),
                        response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                        response_class_type=root_feature.get_feature_response_cls
                    )
                # end with
            # end for
        # end with

        # ---------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get FW info (Gotthard)')
        # ---------------------------------------------------------------------------------------------------------------
        get_fw_info_report = ufy_device_info.get_fw_info_cls(
            device_index=gotthard_device_index, feature_index=ufy_device_info_idx, entity_index=0)
        with self.time_tracking("Get FW info (Gotthard)", timers_results):
            ChannelUtils.send(
                test_case=self,
                report=get_fw_info_report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=ufy_device_info.get_fw_info_response_cls
            )
        # end with

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable hidden features (Gotthard)')
        # --------------------------------------------------------------------------------------------------------------
        with self.time_tracking("Enable hidden features (Gotthard)", timers_results):
            DeviceBaseTestUtils.HIDppHelper.enable_hidden_features(self,
                                                                   device_index=gotthard_device_index,
                                                                   port_index=self.gotthard_receiver_port_index)
            if ufy_manage_deact_idx != Root.FEATURE_NOT_FOUND:
                DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features(
                    test_case=self,
                    manufacturing=True,
                    device_index=gotthard_device_index,
                    port_index=self.gotthard_receiver_port_index)
            # end if
        # end with

        # Set LED Off : 18A1 not available yet in framework

        # Random key generation not necessary for this test

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start pre pairing on BLE Pro receiver')
        # --------------------------------------------------------------------------------------------------------------
        ReceiverTestUtils.switch_to_receiver(self, self.pre_paired_receiver_port_index)
        with self.time_tracking("Start Prepairing on BLE Pro receiver", timers_results):
            ReceiverTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
            BleProReceiverPrepairingTestUtils.set_prepairing_management(
                self, self.rcv_prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)
        # end with

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start pre pairing on device and get device address (with Gotthard)')
        # --------------------------------------------------------------------------------------------------------------
        ReceiverTestUtils.switch_to_receiver(
            self,
            self.gotthard_receiver_port_index,
            task_enabler=ReceiverTestUtils.GotthardReceiver.GOTTHARD_TASK_ENABLER)
        DeviceManagerUtils.set_channel(
            test_case=self, new_channel_id=ChannelIdentifier(port_index=self.gotthard_receiver_port_index,
                                                             device_index=gotthard_device_index))
        with self.time_tracking("Start Prepairing device (with Gotthard)", timers_results):
            device_address = BleProPrePairingTestUtils.pre_pairing_start_sequence(
                self, ufy_feature_1816, ufy_feature_index_1816)
        # end with

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set keys on BLE Pro receiver')
        # --------------------------------------------------------------------------------------------------------------
        ReceiverTestUtils.switch_to_receiver(self, self.pre_paired_receiver_port_index)
        with self.time_tracking("Prepairing BLE Pro receiver : set keys and device address", timers_results):
            self.ltk_key, self.irk_local_key, self.irk_remote_key = BleProReceiverPrepairingTestUtils.set_keys(
                self, ltk_key=True, irk_local_key=True, irk_remote_key=True, force_random_data=True)[:3]
            BleProReceiverPrepairingTestUtils.set_prepairing_data(
                self, PrepairingData.DataType.REMOTE_ADDRESS, device_address)
        # end with

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get BLE Pro receiver address')
        # --------------------------------------------------------------------------------------------------------------
        with self.time_tracking("Get receiver address", timers_results):
            prepairing_data_resp = BleProReceiverPrepairingTestUtils.get_prepairing_data(
                self, PrepairingData.DataType.LOCAL_ADDRESS)
            receiver_address = prepairing_data_resp.local_address
        # end with

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set keys and receiver address on device (with Gotthard)')
        # --------------------------------------------------------------------------------------------------------------
        ReceiverTestUtils.switch_to_receiver(
            self,
            self.gotthard_receiver_port_index,
            task_enabler=ReceiverTestUtils.GotthardReceiver.GOTTHARD_TASK_ENABLER)
        DeviceManagerUtils.set_channel(
            test_case=self, new_channel_id=ChannelIdentifier(port_index=self.gotthard_receiver_port_index,
                                                             device_index=gotthard_device_index))
        with self.time_tracking("Prepairing device : set keys and receiver address (with Gotthard)", timers_results):
            BleProPrePairingTestUtils.pre_pairing_sequence(
                test_case=self, pre_pairing_main_class=ufy_feature_1816, pre_pairing_index=ufy_feature_index_1816,
                long_term_key=self.ltk_key,
                remote_identity_resolving_key=self.irk_local_key, local_identity_resolving_key=self.irk_remote_key,
                remote_connection_signature_resolving_key=None, local_connection_signature_resolving_key=None,
                receiver_address=receiver_address, start=False)
        # end with

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Store prepairing data on BLE Pro receiver')
        # --------------------------------------------------------------------------------------------------------------
        ReceiverTestUtils.switch_to_receiver(self, self.pre_paired_receiver_port_index)
        with self.time_tracking("Store prepairing data on BLE Pro receiver", timers_results):
            BleProReceiverPrepairingTestUtils.set_prepairing_management(
                self, self.rcv_prepairing_slot, PrepairingManagement.PrepairingManagementControl.STORE)
        # end with

        # Since the receiver finished adding
        if DeviceManagerUtils.get_channel(
                test_case=self,
                channel_id=ChannelIdentifier(
                    port_index=ChannelUtils.get_port_index(test_case=self),
                    device_index=self.rcv_prepairing_slot)) is None:
            if isinstance(self.current_channel, UsbChannel):
                current_receiver_channel = self.current_channel
            elif isinstance(self.current_channel, ThroughReceiverChannel):
                current_receiver_channel = self.current_channel.receiver_channel
            else:
                assert False, \
                    "Cannot use this method on a channel other than UsbReceiverChannel or ThroughReceiverChannel"
            # end if

            new_channel = ThroughBleProReceiverChannel(
                receiver_channel=current_receiver_channel, device_index=self.rcv_prepairing_slot)
            DeviceManagerUtils.add_channel_to_cache(test_case=self, channel=new_channel)

            self.backup_dut_channel.hid_dispatcher.dump_mapping_in_other_dispatcher(
                other_dispatcher=new_channel.hid_dispatcher)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set OOB state (with Gotthard)')
        # --------------------------------------------------------------------------------------------------------------
        ReceiverTestUtils.switch_to_receiver(
            self,
            self.gotthard_receiver_port_index,
            task_enabler=ReceiverTestUtils.GotthardReceiver.GOTTHARD_TASK_ENABLER)
        DeviceManagerUtils.set_channel(
            test_case=self, new_channel_id=ChannelIdentifier(port_index=self.gotthard_receiver_port_index,
                                                             device_index=gotthard_device_index))
        with self.time_tracking("Set OOB state (with Gotthard)", timers_results):
            DeviceBaseTestUtils.HIDppHelper.set_oob_state(test_case=self,
                                                          enable_hidden_features=False,
                                                          device_index=gotthard_device_index,
                                                          port_index=self.gotthard_receiver_port_index)
        # end with

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force BLE Pro receiver Reset')
        # --------------------------------------------------------------------------------------------------------------
        ReceiverTestUtils.switch_to_receiver(
            test_case=self,
            receiver_port_index=self.pre_paired_receiver_port_index,
            task_enabler=BitStruct(Numeral(LinkEnablerInfo.HID_PP_MASK)))
        with self.time_tracking("BLE Pro Receiver reset", timers_results):
            reset_req = SetResetRequest(Hidpp1Data.DeviceIndex.TRANSCEIVER)
            try:
                ChannelUtils.send_only(
                    test_case=self,
                    report=reset_req,
                    timeout=1
                )
            except TransportContextException as e:
                if e.get_cause() not in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                                         TransportContextException.Cause.CONTEXT_ERROR_IO,
                                         TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
                    raise
                # end if
            # end try
            time.sleep(2.5)
        # end with

        ChannelUtils.close_channel(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force device Reset (with Gotthard)')
        # --------------------------------------------------------------------------------------------------------------
        ReceiverTestUtils.switch_to_receiver(
            self,
            receiver_port_index=self.gotthard_receiver_port_index,
            task_enabler=BitStruct(Numeral(LinkEnablerInfo.HID_PP_MASK)))
        DeviceManagerUtils.set_channel(
            test_case=self, new_channel_id=ChannelIdentifier(port_index=self.gotthard_receiver_port_index,
                                                             device_index=gotthard_device_index))
        force_device_reset = ForceDeviceReset(deviceIndex=gotthard_device_index, featureId=ufy_device_reset_feature_id)
        with self.time_tracking("Device reset (with Gotthard)", timers_results):
            try:
                ChannelUtils.send_only(
                    test_case=self,
                    report=force_device_reset,
                    timeout=0.6
                )
            except TransportContextException as e:
                if e.get_cause() not in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                                         TransportContextException.Cause.CONTEXT_ERROR_IO,
                                         TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
                    raise
                # end if
            # end try
        # end with

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send BLE Pro device pairing information (polling until reconnection)')
        # --------------------------------------------------------------------------------------------------------------
        time.sleep(1)
        ReceiverTestUtils.switch_to_receiver(self, receiver_port_index=self.pre_paired_receiver_port_index)
        device_pairing_info_req = GetBLEProDevicePairingInfoRequest(
            NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_PAIRING_INFO_MIN + self.rcv_prepairing_slot - 1)
        message_received = False
        timeout = self.TDE_MAX_DURATION
        with self.time_tracking("BLE Pro device pairing information", timers_results):
            start_time = time.perf_counter()
            while message_received is False:
                try:
                    ChannelUtils.send_only(
                        test_case=self,
                        report=device_pairing_info_req,
                        timeout=1
                    )
                    message_received = ChannelUtils.get_only(test_case=self,
                                                             queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                                                             timeout=0.1)
                except Exception as err:
                    if start_time + timeout < time.perf_counter():
                        raise err
                    else:
                        ChannelUtils.clean_messages(test_case=self,
                                                    queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                                                    class_type=Hidpp1ErrorCodes)
                        continue
                    # end if
                # end try
            # end while
        # end with

        wait_event = True
        while wait_event:
            wireless_device_status_broadcast_event = ChannelUtils.get_only(
                test_case=self,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=WirelessDeviceStatusBroadcastEvent,
                timeout=0.2,
                check_first_message=False,
                allow_no_message=True
            )
            wait_event = False if wireless_device_status_broadcast_event is None else True
        # end while

        BleProSafePrePairedReceiverTestUtils.check_prepairing_ble_pro_device_info(self, self.rcv_prepairing_slot)

        DeviceManagerUtils.set_channel(
            test_case=self,
            new_channel_id=ChannelIdentifier(
                port_index=ChannelUtils.get_port_index(test_case=self), device_index=self.rcv_prepairing_slot),
            open_channel=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get features (BLE Pro)')
        # --------------------------------------------------------------------------------------------------------------
        with self.time_tracking("Get features (BLE Pro)", timers_results):
            for feature_id in features_list:
                with self.time_tracking(f"Get feature {hex(feature_id)}"):
                    ChannelUtils.send(
                        test_case=self,
                        report=root_feature.get_feature_cls(deviceIndex=self.rcv_prepairing_slot, featureId=feature_id),
                        response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                        response_class_type=root_feature.get_feature_response_cls
                    )
                # end with
            # end for
        # end with

        # ---------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get FW info (BLE Pro)')
        # ---------------------------------------------------------------------------------------------------------------
        get_fw_info_report = self.ble_device_info.get_fw_info_cls(
            device_index=self.rcv_prepairing_slot, feature_index=self.ble_device_info_idx, entity_index=0)
        with self.time_tracking("Get FW info (BLE Pro)", timers_results):
            ChannelUtils.send(
                test_case=self,
                report=get_fw_info_report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.ble_device_info.get_fw_info_response_cls
            )
        # end with

        # ---------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable hidden features (BLE Pro)')
        # ---------------------------------------------------------------------------------------------------------------
        with self.time_tracking("Enable hidden features (BLE Pro)", timers_results):
            # Enable hidden features is required here only to call Set OOB State later. OOB State is tagged as
            # engineering but not deactivatable, so no need to activate any deactivatable features
            DeviceBaseTestUtils.HIDppHelper.enable_hidden_features(test_case=self,
                                                                   device_index=self.rcv_prepairing_slot)
        # end with

        # ---------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable manufacturing test mode and write pass flag (BLE Pro)')
        # ---------------------------------------------------------------------------------------------------------------
        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.current_channel.receiver_channel)
        tde_pass_flag_nvmem_addr = 0x000B
        tde_pass_flag_data = 0xAA
        write_pass_flag_req = SetNonVolatileMemoryAccessRequest(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                                                                nvm_address_lsb=tde_pass_flag_nvmem_addr & 0xFF,
                                                                nvm_address_msb=(tde_pass_flag_nvmem_addr >> 8) & 0xFF,
                                                                data=tde_pass_flag_data)
        with self.time_tracking("Enable manufacturing test mode and write pass flag (BLE Pro)", timers_results):
            # Enable Manufacturing test mode
            ReceiverTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

            # Write pass flag
            write_pass_flag_resp = ChannelUtils.send(
                test_case=self,
                report=write_pass_flag_req,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=SetNonVolatileMemoryAccessResponse
            )
        # end with
        TDETestUtils.MessageChecker.check_fields(self, write_pass_flag_resp, SetNonVolatileMemoryAccessResponse, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Read Pass Flag (BLE Pro)')
        # --------------------------------------------------------------------------------------------------------------
        read_pass_flag_req = GetNonVolatileMemoryAccessRequest(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                                                               nvm_address_lsb=tde_pass_flag_nvmem_addr & 0xFF,
                                                               nvm_address_msb=(tde_pass_flag_nvmem_addr >> 8) & 0xFF)
        with self.time_tracking("Read pass flag (BLE Pro)", timers_results):
            read_pass_flag_resp = ChannelUtils.send(
                test_case=self,
                report=read_pass_flag_req,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=GetNonVolatileMemoryAccessResponse
            )
        # end with

        TDETestUtils.GetNonVolatileMemoryAccessResponseChecker.check_fields(
            self,
            read_pass_flag_resp,
            GetNonVolatileMemoryAccessResponse,
            TDETestUtils.GetNonVolatileMemoryAccessResponseChecker.get_check_map(tde_pass_flag_nvmem_addr & 0xFF,
                                                                                 (tde_pass_flag_nvmem_addr >> 8) & 0xFF,
                                                                                 tde_pass_flag_data))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Restore OOB state (BLE Pro)')
        # --------------------------------------------------------------------------------------------------------------
        DeviceManagerUtils.set_channel(
            test_case=self, new_channel_id=ChannelIdentifier(
                port_index=ChannelUtils.get_port_index(test_case=self), device_index=self.rcv_prepairing_slot))
        with self.time_tracking("Restore OOB state (BLE Pro)", timers_results):
            DeviceBaseTestUtils.HIDppHelper.set_oob_state(test_case=self,
                                                          enable_hidden_features=False,
                                                          device_index=self.rcv_prepairing_slot,
                                                          port_index=self.pre_paired_receiver_port_index)
        # end with

        if ufy_manage_deact_idx != Root.FEATURE_NOT_FOUND:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Reconnect to Gotthard receiver')
            # ----------------------------------------------------------------------------------------------------------
            ReceiverTestUtils.switch_to_receiver(
                self,
                self.gotthard_receiver_port_index,
                task_enabler=ReceiverTestUtils.GotthardReceiver.GOTTHARD_TASK_ENABLER)
            with self.time_tracking("Gotthard connection", timers_results):
                try:
                    ReceiverTestUtils.GotthardReceiver.init_connection(self)
                except TestException as e:
                    self.log_warning(f'Gotthard receiver initialization failed with {e}. Reset the receiver via usb hub')
                    try:
                        ChannelUtils.close_channel(test_case=self)
                        LibusbDriver.disable_usb_port(port_index=LibusbDriver.GOTTHARD)
                    finally:
                        LibusbDriver.enable_usb_port(port_index=LibusbDriver.GOTTHARD)
                    # end try
                    ReceiverTestUtils.switch_to_receiver(
                        self,
                        self.gotthard_receiver_port_index,
                        task_enabler=ReceiverTestUtils.GotthardReceiver.GOTTHARD_TASK_ENABLER)
                    ReceiverTestUtils.GotthardReceiver.init_connection(self)
                # end try
            # end with

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Enable hidden features (Gotthard)')
            # ----------------------------------------------------------------------------------------------------------
            with self.time_tracking("Enable hidden features (Gotthard)", timers_results):
                # Enable hidden features is required here only to call Manage Deactivatable features later,
                # which is tagged as engineering but not deactivatable, so no need to activate any deactivatable
                # features
                DeviceBaseTestUtils.HIDppHelper.enable_hidden_features(
                    self, device_index=gotthard_device_index, port_index=self.gotthard_receiver_port_index)
            # end with

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Disable Gotthard protocol')
            # ----------------------------------------------------------------------------------------------------------
            disable_features_req = ufy_feature_1e02.disable_features_cls(
                gotthard_device_index, ufy_manage_deact_idx, disable_gothard=True)
            with self.time_tracking("Disable Gotthard protocol", timers_results):
                ChannelUtils.send(
                    test_case=self,
                    report=disable_features_req,
                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                    response_class_type=ufy_feature_1e02.disable_features_response_cls
                )
            # end with
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check TDE nominal case duration')
        # --------------------------------------------------------------------------------------------------------------
        full_time = sum(t for t in timers_results)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_title_2(self, f'Pre-pairing full time : {full_time}')
        # --------------------------------------------------------------------------------------------------------------
        self.assertLess(full_time, self.TDE_MAX_DURATION,
                        "TDE nominal case should not be longer than maximum accepted duration")
    # end def _tde_nominal_case

    def _update_ble_feature_mapping(self):
        """
        Update feature mapping for BLE
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_title_2(self, 'Update feature mapping (BLE)')
        # --------------------------------------------------------------------------------------------------------------
        DeviceManagerUtils.set_channel(
            test_case=self,
            new_channel_id=ChannelIdentifier(
                port_index=ChannelUtils.get_port_index(test_case=self), device_index=self.original_device_index))
        ble_enable_hidden_features_idx = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=EnableHidden.FEATURE_ID)
        ble_wireless_device_status_idx = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=WirelessDeviceStatus.FEATURE_ID)
        ble_oob_state_idx = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=OobState.FEATURE_ID)
        ble_device_info_idx = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=DeviceInformation.FEATURE_ID)
        ble_device_reset_feature_id = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=DeviceReset.FEATURE_ID)
        ble_feature_index_1816 = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=BleProPrepairing.FEATURE_ID)
        ble_manage_deact_idx = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=ManageDeactivatableFeaturesAuth.FEATURE_ID)
        ble_passwd_auth_idx = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=PasswordAuthentication.FEATURE_ID)

        # Features index will be the same for self.rcv_prepairing_slot device index
        self.current_channel.hid_dispatcher.add_feature_entry(
            feature_index=Root.FEATURE_INDEX, feature_id=Root.FEATURE_ID,
            feature_version=self.current_channel.hid_dispatcher.get_feature_entry_by_index(Root.FEATURE_INDEX)[1])
        self.current_channel.hid_dispatcher.add_feature_entry(
            feature_index=ble_enable_hidden_features_idx, feature_id=EnableHidden.FEATURE_ID,
            feature_version=self.current_channel.hid_dispatcher.get_feature_entry_by_index(
                feature_index=ble_enable_hidden_features_idx)[1])
        self.current_channel.hid_dispatcher.add_feature_entry(
            feature_index=ble_wireless_device_status_idx, feature_id=WirelessDeviceStatus.FEATURE_ID,
            feature_version=self.current_channel.hid_dispatcher.get_feature_entry_by_index(
                feature_index=ble_wireless_device_status_idx)[1])
        self.current_channel.hid_dispatcher.add_feature_entry(
            feature_index=ble_oob_state_idx, feature_id=OobState.FEATURE_ID,
            feature_version=self.current_channel.hid_dispatcher.get_feature_entry_by_index(ble_oob_state_idx)[1])
        self.current_channel.hid_dispatcher.add_feature_entry(
            feature_index=ble_device_info_idx, feature_id=DeviceInformation.FEATURE_ID,
            feature_version=self.current_channel.hid_dispatcher.get_feature_entry_by_index(ble_device_info_idx)[1])
        self.current_channel.hid_dispatcher.add_feature_entry(
            feature_index=ble_device_reset_feature_id, feature_id=DeviceInformation.FEATURE_ID,
            feature_version=self.current_channel.hid_dispatcher.get_feature_entry_by_index(
                feature_index=ble_device_reset_feature_id)[1])
        self.current_channel.hid_dispatcher.add_feature_entry(
            feature_index=ble_feature_index_1816, feature_id=DeviceInformation.FEATURE_ID,
            feature_version=self.current_channel.hid_dispatcher.get_feature_entry_by_index(ble_feature_index_1816)[1])
        self.current_channel.hid_dispatcher.add_feature_entry(
            feature_index=ble_manage_deact_idx, feature_id=ManageDeactivatableFeaturesAuth.FEATURE_ID,
            feature_version=self.current_channel.hid_dispatcher.get_feature_entry_by_index(ble_manage_deact_idx)[1])
        self.current_channel.hid_dispatcher.add_feature_entry(
            feature_index=ble_passwd_auth_idx, feature_id=PasswordAuthentication.FEATURE_ID,
            feature_version=self.current_channel.hid_dispatcher.get_feature_entry_by_index(ble_passwd_auth_idx)[1])

        self.ble_oob_state_idx = ble_oob_state_idx
        self.ble_device_info_idx = ble_device_info_idx
        self.ble_device_info = DeviceInformationFactory.create(
            ChannelUtils.get_feature_version(test_case=self, feature_index=self.ble_device_info_idx))
    # end def _update_ble_feature_mapping

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @level('Business')
    @services('MultiHost')
    @services('Gotthard')
    def test_business_nominal_case_with_gotthard(self):
        """
        Run pre-pairing sequence using Gotthard receiver and check device connects on pre-paired receiver when slot is
        empty and pre-paired receiver is in range
        """
        try:
            self.gotthard_receiver_port_index = self._get_gotthard_receiver_port_index()
            self._update_ble_feature_mapping()
            self.channel_switch(device_uid=ChannelUtils.get_channel_identifier(
                test_case=self, channel=self.backup_dut_channel))
            DeviceTestUtils.HIDppHelper.activate_features(self, gotthard=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, 'Set OOB State')
            # ----------------------------------------------------------------------------------------------------------
            DeviceBaseTestUtils.HIDppHelper.set_oob_state(self)
            # Reset device
            self.debugger.reset(soft_reset=False)

            self._tde_nominal_case()
        finally:
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=LinkQualityInfoShort)
        # end try

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0040")
    # end def test_business_nominal_case_with_gotthard

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @level('Business')
    @services('MultiHost')
    @services('Gotthard')
    def test_business_rework_case_with_gotthard(self):
        """
        Run pre-pairing sequence twice using Gotthard receiver to check a rework is possible
        """
        try:
            self.gotthard_receiver_port_index = self._get_gotthard_receiver_port_index()
            self._update_ble_feature_mapping()
            self.channel_switch(device_uid=ChannelUtils.get_channel_identifier(
                test_case=self, channel=self.backup_dut_channel))
            DeviceTestUtils.HIDppHelper.activate_features(self, gotthard=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, 'Set OOB State')
            # ----------------------------------------------------------------------------------------------------------
            DeviceBaseTestUtils.HIDppHelper.set_oob_state(self)

            self._tde_nominal_case()

            ReceiverTestUtils.switch_to_receiver(self, self.pre_paired_receiver_port_index)
            self.debugger.reset(soft_reset=False)
            ChannelUtils.wait_through_receiver_channel_link_status(
                test_case=self,
                channel=self.current_channel,
                link_status=DeviceConnection.LinkStatus.LINK_ESTABLISHED,
                device_index=self.rcv_prepairing_slot)
            DeviceManagerUtils.set_channel(
                test_case=self, new_channel_id=ChannelIdentifier(
                    port_index=ChannelUtils.get_port_index(test_case=self), device_index=self.rcv_prepairing_slot))
            DeviceTestUtils.HIDppHelper.activate_features(self,
                                                          gotthard=True,
                                                          device_index=self.rcv_prepairing_slot,
                                                          port_index=self.pre_paired_receiver_port_index)

            self._tde_nominal_case()
        finally:
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=LinkQualityInfoShort)
        # end try

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0041")
    # end def test_business_rework_case_with_gotthard

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @level('Business', 'SmokeTests')
    @services('MultiHost')
    def test_empty_slot_receiver_off_on_transition(self):
        """
        Check device connects on pre-paired receiver when receiver is turned on after DUT when slot is empty
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pre Pair Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        self.receiver_address, self.device_address = BleProSafePrePairedReceiverTestUtils.pre_pairing_sequence(
            self,
            self.feature_1816,
            self.feature_1816_index,
            self.rcv_prepairing_slot,
            self.ltk_key,
            self.irk_local_key,
            self.irk_remote_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.close_channel(test_case=self)
        LibusbDriver.disable_usb_port(port_index=self.pre_paired_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force Device in discoverable mode')
        # --------------------------------------------------------------------------------------------------------------
        self._force_host_to_oob_state_in_nvs()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(self, self.spy_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self, PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE)
        self.assertNotNone(
            device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

        BleProSafePrePairedReceiverTestUtils.SpyReceiver.cancel_discovery(self, self.spy_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn on pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.channel_enable(self.pre_paired_receiver_port_index,
                            BleProSafePrePairedReceiverTestUtils.DISCOVERABLE_TIME +
                            BleProSafePrePairedReceiverTestUtils.PRE_PAIRED_RCV_SEARCH_TIME)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.MFG)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check BLE Bond Id Chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self._check_pre_pairing_ble_bond_id_chunk_in_nvs(host_index=self.device_nvs_host_index)

        DevicePairingTestUtils.check_connection_status(
            self, self.rcv_prepairing_slot, DeviceConnection.LinkStatus.LINK_ESTABLISHED, log_step=True, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0002")
    # end def test_empty_slot_receiver_off_on_transition

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @level('Functionality')
    def test_empty_slot_pre_paired_receiver_off_user_pairing(self):
        """
        Check DUT can be paired if pre paired receiver is not present
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pre Pair Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.pre_pairing_sequence(
            self,
            self.feature_1816,
            self.feature_1816_index,
            self.rcv_prepairing_slot,
            self.ltk_key,
            self.irk_local_key,
            self.irk_remote_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.close_channel(test_case=self)
        LibusbDriver.disable_usb_port(port_index=self.pre_paired_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force Device in discoverable mode')
        # --------------------------------------------------------------------------------------------------------------
        self._force_host_to_oob_state_in_nvs()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(self, self.spy_receiver_port_index)

        # Fetch Device USB Descriptors matching the spy receiver interfaces configuration
        ChannelUtils.get_descriptors(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self, PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE)
        self.assertNotNone(
            device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pair device with second receiver')
        # --------------------------------------------------------------------------------------------------------------
        # noinspection PyUnresolvedReferences
        # bluetooth_address is part of the data in device discovery notification part 0
        device_index = BleProSafePrePairedReceiverTestUtils.SpyReceiver.pair_device(
            self,
            self.spy_receiver_port_index,
            device_discovery[DeviceDiscovery.PART.CONFIGURATION].data.bluetooth_address)

        DevicePairingTestUtils.check_connection_status(
            self, device_index, DeviceConnection.LinkStatus.LINK_ESTABLISHED, log_step=True, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.USR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check BLE Bond Id Chunk for pairing slot '
                                  f'{self.device_nvs_host_index} has been created in NVS')
        # --------------------------------------------------------------------------------------------------------------
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)
        self.assertTrue(expr=(1 <= len(ble_bond_id_chunks)),
                        msg=f'We expect at least one chunk in NVS while we dump {len(ble_bond_id_chunks)} chunks.')

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0003")
    # end def test_empty_slot_pre_paired_receiver_off_user_pairing

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @level('Functionality')
    def test_empty_slot_pre_paired_receiver_off_no_pairing(self):
        """
        Check DUT remains discoverable during 3 minutes if pre paired receiver is not present
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pre Pair Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.pre_pairing_sequence(
            self,
            self.feature_1816,
            self.feature_1816_index,
            self.rcv_prepairing_slot,
            self.ltk_key,
            self.irk_local_key,
            self.irk_remote_key, )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.close_channel(test_case=self)
        LibusbDriver.disable_usb_port(port_index=self.pre_paired_receiver_port_index)

        # Long press on the connect button or the Easy Switch CH1
        self._enter_discoverable_mode(channel_id=HOST.CH1, click_count=0)
        start_time = time.perf_counter()

        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT
        tolerance = DiscoveryTestUtils.DEVICE_DISCOVERY_TOLERANCE
        while time.perf_counter() < end_time - tolerance:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            timeout = time.perf_counter() - start_time
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(device_discovery, f'Discovery notifications ended at {timeout}s while expecting '
                                                 f'{DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT}s')

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        # Do not check the discovery notifications around the scheduled timeout with a tolerance of 12s before and after
        time.sleep(float(tolerance * 2))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
            self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device is not discoverable anymore after timeout')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = True
        timeout = None
        infinite_loop_protection_count = 0
        while device_discovery is not None and infinite_loop_protection_count < self.MAX_LOOP_COUNT:
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self,
                float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN),
                max_tries=1,
                raise_err=False
            )
            if device_discovery is not None:
                timeout = time.perf_counter() - start_time
            # end if
            infinite_loop_protection_count += 1
        # end while
        self.assertNone(timeout, f'Discovery notifications received at {timeout}s while it shall stop at '
                                 f'{DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT}s')
        self.assertNone(device_discovery, 'No discovery notifications should have been received')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(self, self.memory_manager, 0, ConnectIdChunkData.PairingSrc.USR)

        pairing_slot = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check BLE Bond Id Chunk for pairing slot {pairing_slot} has not been created in NVS')
        # --------------------------------------------------------------------------------------------------------------
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=pairing_slot)
        self.assertEqual(obtained=len(ble_bond_id_chunks),
                         expected=0,
                         msg=f'No BLE Bond Id chunk for pairing slot {pairing_slot} should be created in NVS')

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0004")
    # end def test_empty_slot_pre_paired_receiver_off_no_pairing

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @level('Functionality')
    def test_empty_slot_pre_paired_receiver_off_no_pairing_user_action(self):
        """
        Check all user actions, except EasySwitch, don't impact the 3 minutes "pairing mode" timeout
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pre Pair Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.pre_pairing_sequence(
            self,
            self.feature_1816,
            self.feature_1816_index,
            self.rcv_prepairing_slot,
            self.ltk_key,
            self.irk_local_key,
            self.irk_remote_key, )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.close_channel(test_case=self)
        LibusbDriver.disable_usb_port(port_index=self.pre_paired_receiver_port_index)

        # Long press on the connect button or the Easy Switch CH1
        self._enter_discoverable_mode(channel_id=HOST.CH1, click_count=0)
        start_time = time.perf_counter()

        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT
        tolerance = DiscoveryTestUtils.DEVICE_DISCOVERY_TOLERANCE
        while time.perf_counter() < end_time - tolerance:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Perform User Action after {time.perf_counter() - start_time}s')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.user_action()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        # Do not check the discovery notifications around the scheduled timeout with a tolerance of 12s before and after
        time.sleep(float(tolerance * 2))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
            self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device is not discoverable anymore after timeout')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self,
            float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN),
            max_tries=1,
            raise_err=False
        )
        self.assertNone(device_discovery, 'No discovery notifications should have been received')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(self, self.memory_manager, expected_host_index=0,
                                                       expected_pairing_source=ConnectIdChunkData.PairingSrc.USR)
        pairing_slot = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check BLE Bond Id Chunk for pairing slot {pairing_slot} has not been created in '
                                  f'NVS')
        # --------------------------------------------------------------------------------------------------------------
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=pairing_slot)
        self.assertEqual(obtained=len(ble_bond_id_chunks),
                         expected=0,
                         msg=f'No BLE Bond Id chunk for pairing slot {pairing_slot} should be created in NVS')

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0005")
    # end def test_empty_slot_pre_paired_receiver_off_no_pairing_user_action

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @level('Functionality')
    @services('PowerSupply')
    def test_empty_slot_pre_paired_receiver_connection_critical_battery(self):
        """
        Check the battery level does not impact the "pairing mode" state machine
        """
        self.device_nvs_host_index = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set battery critical level')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=UnifiedBattery.FEATURE_ID,
            channel=DeviceManagerUtils.get_channel(test_case=self, channel_id=ChannelIdentifier(
                port_index=ChannelUtils.get_port_index(test_case=self), device_index=self.original_device_index)))

        critical_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'critical')
        battery_critical = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, critical_state_of_charge)
        self.power_supply_emulator.set_voltage(battery_critical)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pre Pair Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        self.receiver_address, self.device_address = BleProSafePrePairedReceiverTestUtils.pre_pairing_sequence(
            self,
            self.feature_1816,
            self.feature_1816_index,
            self.rcv_prepairing_slot,
            self.ltk_key,
            self.irk_local_key,
            self.irk_remote_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.close_channel(test_case=self)
        LibusbDriver.disable_usb_port(port_index=self.pre_paired_receiver_port_index)

        # Long press on the connect button or the Easy Switch CH1
        self._enter_discoverable_mode(channel_id=HOST.CH1, click_count=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(self, self.spy_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self, PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE)
        self.assertNotNone(
            device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

        BleProSafePrePairedReceiverTestUtils.SpyReceiver.cancel_discovery(self, self.spy_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn on pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.channel_enable(self.pre_paired_receiver_port_index,
                            BleProSafePrePairedReceiverTestUtils.DISCOVERABLE_TIME +
                            BleProSafePrePairedReceiverTestUtils.PRE_PAIRED_RCV_SEARCH_TIME)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.MFG)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check BLE Bond Id Chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self._check_pre_pairing_ble_bond_id_chunk_in_nvs(host_index=self.device_nvs_host_index)

        DevicePairingTestUtils.check_connection_status(
            self, self.rcv_prepairing_slot, DeviceConnection.LinkStatus.LINK_ESTABLISHED, log_step=True, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0006")
    # end def test_empty_slot_pre_paired_receiver_connection_critical_battery

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @level('Functionality')
    @services('PowerSupply')
    def test_empty_slot_pre_paired_receiver_off_no_pairing_low_to_critical_battery(self):
        """
        Check the battery low level to critical change does not impact the "pairing mode" state machine
        """
        # Get battery levels
        ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=UnifiedBattery.FEATURE_ID,
            channel=DeviceManagerUtils.get_channel(test_case=self, channel_id=ChannelIdentifier(
                port_index=ChannelUtils.get_port_index(test_case=self), device_index=self.original_device_index)))
        low_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'low')
        battery_low = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, low_state_of_charge)
        critical_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'critical')
        battery_critical = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, critical_state_of_charge)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pre Pair Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.pre_pairing_sequence(
            self,
            self.feature_1816,
            self.feature_1816_index,
            self.rcv_prepairing_slot,
            self.ltk_key,
            self.irk_local_key,
            self.irk_remote_key, )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.close_channel(test_case=self)
        LibusbDriver.disable_usb_port(port_index=self.pre_paired_receiver_port_index)

        # Long press on the connect button or the Easy Switch CH1
        self._enter_discoverable_mode(channel_id=HOST.CH1, click_count=0)
        host_index = 1
        start_time = time.perf_counter()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set battery low level')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(battery_low)

        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT
        tolerance = DiscoveryTestUtils.DEVICE_DISCOVERY_TOLERANCE
        critical_battery_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT / 2
        critical_battery = False
        while time.perf_counter() < end_time - tolerance:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            if not critical_battery and time.perf_counter() > critical_battery_time:
                # ----------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Set battery critical level')
                # ----------------------------------------------------------------------------------------------------------
                self.power_supply_emulator.set_voltage(battery_critical)
                critical_battery = True
            # end if

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        # Do not check the discovery notifications around the scheduled timeout with a tolerance of 12s before and after
        time.sleep(float(tolerance * 2))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
            self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device is not discoverable anymore after timeout')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self,
            float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN),
            max_tries=1,
            raise_err=False
        )
        self.assertNone(device_discovery, 'No discovery notifications should have been received')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        expected_host_index = 0
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, expected_host_index, ConnectIdChunkData.PairingSrc.USR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check BLE Bond Id Chunk for pairing slot {host_index} has not been created in NVS')
        # --------------------------------------------------------------------------------------------------------------
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=host_index)
        self.assertEqual(obtained=len(ble_bond_id_chunks),
                         expected=0,
                         msg=f'No BLE Bond Id chunk for pairing slot {host_index} should be created in NVS')

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0007")
    # end def test_empty_slot_pre_paired_receiver_off_no_pairing_low_to_critical_battery

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @level('Functionality')
    def test_empty_slot_pre_pairing_erased_in_receiver(self):
        """
        Check DUT remains discoverable during 3 minutes if pre paired slot has been erased in receiver
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pre Pair Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.pre_pairing_sequence(
            self,
            self.feature_1816,
            self.feature_1816_index,
            self.rcv_prepairing_slot,
            self.ltk_key,
            self.irk_local_key,
            self.irk_remote_key, )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Erase pre pairing')
        # --------------------------------------------------------------------------------------------------------------
        # Enable Manufacturing test mode
        ReceiverTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
        BleProReceiverPrepairingTestUtils.set_prepairing_management(
            self, self.rcv_prepairing_slot, PrepairingManagement.PrepairingManagementControl.DELETE)
        TDETestUtils.set_test_mode_control(self, TestModeControl.TestModeEnable.DISABLE_TEST_MODE)

        # Long press on the connect button or the Easy Switch CH1
        self._enter_discoverable_mode(channel_id=HOST.CH1, click_count=0)
        start_time = time.perf_counter()

        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT
        tolerance = DiscoveryTestUtils.DEVICE_DISCOVERY_TOLERANCE
        while time.perf_counter() < end_time - tolerance:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        # Do not check the discovery notifications around the scheduled timeout with a tolerance of 12s before and after
        time.sleep(float(tolerance * 2))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
            self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device is not discoverable anymore after timeout')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self,
            float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN),
            max_tries=1,
            raise_err=False
        )
        self.assertNone(device_discovery, 'No discovery notifications should have been received')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(self, self.memory_manager, 0, ConnectIdChunkData.PairingSrc.USR)

        pairing_slot = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check BLE Bond Id Chunk for pairing slot {pairing_slot} has not been created in '
                                  f'NVS')
        # --------------------------------------------------------------------------------------------------------------
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=pairing_slot)
        self.assertEqual(obtained=len(ble_bond_id_chunks),
                         expected=0,
                         msg=f'No BLE Bond Id chunk for pairing slot {pairing_slot} should be created in NVS')

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0008")
    # end def test_empty_slot_pre_pairing_erased_in_receiver

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @level('Functionality')
    def test_empty_slot_wrong_pre_pairing(self):
        """
        Check DUT remains discoverable during 3 minutes if pre pairing is wrong (either on DUT side or receiver side)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pre Pair Receiver with Device but with a wrong LTK Key')
        # --------------------------------------------------------------------------------------------------------------
        # Enable Manufacturing test mode
        ReceiverTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
        wrong_ltk_key = HexList('0F0E0D0C0B0A09080706050403020100')
        assert wrong_ltk_key != self.ltk_key
        (receiver_address, device_address, ltk_key, irk_local_key, irk_remote_key, csrk_local_key,
         csrk_remote_key) = BleProReceiverPrepairingTestUtils.receiver_prepairing_sequence(
            self,
            self.rcv_prepairing_slot,
            wrong_ltk_key,
            self.irk_local_key,
            self.irk_remote_key,
            pre_pairing_main_class=self.feature_1816,
            pre_pairing_index=self.feature_1816_index
        )

        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index,
            long_term_key=self.ltk_key,
            remote_identity_resolving_key=self.irk_local_key, local_identity_resolving_key=self.irk_remote_key,
            remote_connection_signature_resolving_key=None, local_connection_signature_resolving_key=None,
            receiver_address=receiver_address, start=False)

        ReceiverTestUtils.reset_receiver(self)

        # Long press on the connect button or the Easy Switch CH1
        self._enter_discoverable_mode(channel_id=HOST.CH1, click_count=0)
        start_time = time.perf_counter()

        # The discovery timeout is shorter in this case because the time spent to look for the pre paired receiver is
        # negligible
        discovery_timeout = 28 * 5.0
        end_time = start_time + discovery_timeout
        tolerance = float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
        while time.perf_counter() < end_time - tolerance:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        time.sleep(float(start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT - time.perf_counter()))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
            self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device is not discoverable anymore after timeout')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self,
            float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN),
            max_tries=1,
            raise_err=False
        )
        self.assertNone(device_discovery, 'No discovery notifications should have been received')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(self, self.memory_manager, 0, ConnectIdChunkData.PairingSrc.USR)

        pairing_slot = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check BLE Bond Id Chunk for pairing slot {pairing_slot} has not been created in '
                                  f'NVS')
        # --------------------------------------------------------------------------------------------------------------
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=pairing_slot)
        self.assertEqual(obtained=len(ble_bond_id_chunks),
                         expected=0,
                         msg=f'No BLE Bond Id chunk for pairing slot {pairing_slot} should be created in NVS')

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0009")
    # end def test_empty_slot_wrong_pre_pairing

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @level('Functionality')
    def test_3_minutes_timeout_reset_on_pairing_failure(self):
        """
        Check that the 3 minutes DUT timeout is reset if pairing fails
        """

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pre Pair Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.pre_pairing_sequence(
            self,
            self.feature_1816,
            self.feature_1816_index,
            self.rcv_prepairing_slot,
            self.ltk_key,
            self.irk_local_key,
            self.irk_remote_key, )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.close_channel(test_case=self)
        LibusbDriver.disable_usb_port(port_index=self.pre_paired_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter discoverable mode on channel 1')
        # --------------------------------------------------------------------------------------------------------------
        # Long press on the connect button or the Easy Switch CH1
        self._enter_discoverable_mode(channel_id=HOST.CH1, click_count=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(self, self.spy_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self, PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE)
        self.assertNotNone(
            device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a pairing sequence with a bad passkey on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        # noinspection PyUnresolvedReferences
        # bluetooth_address is part of the data in device discovery notification part 0
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.failed_pairing_sequence(
            self,
            self.spy_receiver_port_index,
            device_discovery[DeviceDiscovery.PART.CONFIGURATION].data.bluetooth_address)
        pairing_failure_time = time.perf_counter()

        start_time = time.perf_counter()
        tolerance = PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN
        end_time = pairing_failure_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT
        while time.perf_counter() < end_time - tolerance:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(self, self.spy_receiver_port_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(self, self.spy_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device is not discoverable anymore after timeout')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = True
        timeout = None
        infinite_loop_protection_count = 0
        while device_discovery is not None and infinite_loop_protection_count < self.MAX_LOOP_COUNT:
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self,
                float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN),
                max_tries=1,
                raise_err=False
            )
            if device_discovery is not None:
                timeout = time.perf_counter() - start_time
            # end if
            infinite_loop_protection_count += 1
        # end while
        self.assertNone(timeout, f'Discovery notifications received at {timeout}s while expecting '
                                 f'{DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT}s (over time counter = '
                                 f'{infinite_loop_protection_count} out of a maximum of {self.MAX_LOOP_COUNT}')
        self.assertNone(device_discovery, 'No discovery notifications should have been received')

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0010")
    # end def test_3_minutes_timeout_reset_on_pairing_failure

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @level('Functionality')
    def test_3_minutes_timeout_reset_on_pairing_timeout(self):
        """
        Check that the 3 minutes DUT timeout is reset if pairing runs out of time
        """

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pre Pair Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.pre_pairing_sequence(
            self,
            self.feature_1816,
            self.feature_1816_index,
            self.rcv_prepairing_slot,
            self.ltk_key,
            self.irk_local_key,
            self.irk_remote_key, )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.close_channel(test_case=self)
        LibusbDriver.disable_usb_port(port_index=self.pre_paired_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter discoverable mode on channel 1')
        # --------------------------------------------------------------------------------------------------------------
        # Long press on the connect button or the Easy Switch CH1
        self._enter_discoverable_mode(channel_id=HOST.CH1, click_count=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(self, self.spy_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self, PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE)
        self.assertNotNone(
            device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start a pairing sequence on spy receiver but let the timeout occurs')
        # --------------------------------------------------------------------------------------------------------------
        # noinspection PyUnresolvedReferences
        # bluetooth_address is part of the data in device discovery notification part 0
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.timeout_pairing_sequence(
            self, self.spy_receiver_port_index, device_discovery[
                DeviceDiscovery.PART.CONFIGURATION].data.bluetooth_address)
        pairing_failure_time = time.perf_counter()

        tolerance = PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN
        end_time = pairing_failure_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT
        while time.perf_counter() < end_time - tolerance:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(self, self.spy_receiver_port_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(self, self.spy_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device is not discoverable anymore after timeout')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = True
        timeout = None
        infinite_loop_protection_count = 0
        while device_discovery is not None and infinite_loop_protection_count < self.MAX_LOOP_COUNT:
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self,
                float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN),
                max_tries=1,
                raise_err=False
            )
            if device_discovery is not None:
                timeout = time.perf_counter() - pairing_failure_time
            # end if
            infinite_loop_protection_count += 1
        # end while
        self.assertNone(timeout, f'Discovery notifications received at {timeout}s while expecting '
                                 f'{DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT}s')
        self.assertNone(device_discovery, 'No discovery notifications should have been received')

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0011")
    # end def test_3_minutes_timeout_reset_on_pairing_timeout

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @level('Functionality')
    def test_prepairing_after_3_minutes_timeout_reset_on_pairing_failure(self):
        """
        Check that the 3 minutes DUT timeout is reset if pairing fails
        """
        self.device_nvs_host_index = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pre Pair Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.pre_pairing_sequence(
            self,
            self.feature_1816,
            self.feature_1816_index,
            self.rcv_prepairing_slot,
            self.ltk_key,
            self.irk_local_key,
            self.irk_remote_key, )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.close_channel(test_case=self)
        LibusbDriver.disable_usb_port(port_index=self.pre_paired_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter discoverable mode on channel 1')
        # --------------------------------------------------------------------------------------------------------------
        # Long press on the connect button or the Easy Switch CH1
        self._enter_discoverable_mode(channel_id=HOST.CH1, click_count=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(self, self.spy_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self, PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE)
        self.assertNotNone(
            device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a pairing sequence with a bad passkey on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        # noinspection PyUnresolvedReferences
        # bluetooth_address is part of the data in device discovery notification part 0
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.failed_pairing_sequence(
            self,
            self.spy_receiver_port_index,
            device_discovery[DeviceDiscovery.PART.CONFIGURATION].data.bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn on pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.channel_enable(self.pre_paired_receiver_port_index,
                            BleProSafePrePairedReceiverTestUtils.DISCOVERABLE_TIME +
                            BleProSafePrePairedReceiverTestUtils.PRE_PAIRED_RCV_SEARCH_TIME,
                            wait_device_notification=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.MFG)

        DevicePairingTestUtils.check_connection_status(
            self, self.rcv_prepairing_slot, DeviceConnection.LinkStatus.LINK_ESTABLISHED, log_step=True, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'check the DUT is able to send an HID report')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0012")
    # end def test_prepairing_after_3_minutes_timeout_reset_on_pairing_failure

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @level('Functionality')
    def test_prepairing_after_3_minutes_timeout_reset_on_pairing_timeout(self):
        """
        Check that the 3 minutes DUT timeout is reset if pairing runs out of time
        """
        self.device_nvs_host_index = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pre Pair Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.pre_pairing_sequence(
            self,
            self.feature_1816,
            self.feature_1816_index,
            self.rcv_prepairing_slot,
            self.ltk_key,
            self.irk_local_key,
            self.irk_remote_key, )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.close_channel(test_case=self)
        LibusbDriver.disable_usb_port(port_index=self.pre_paired_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter discoverable mode on channel 1')
        # --------------------------------------------------------------------------------------------------------------
        # Long press on the connect button or the Easy Switch CH1
        self._enter_discoverable_mode(channel_id=HOST.CH1, click_count=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(self, self.spy_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self, PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE)
        self.assertNotNone(
            device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait half of the 3 minutes discovery time')
        # --------------------------------------------------------------------------------------------------------------
        time.sleep(DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT / 2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start a pairing sequence on spy receiver but let the 30s pairing timeout occur')
        # --------------------------------------------------------------------------------------------------------------
        # noinspection PyUnresolvedReferences
        # bluetooth_address is part of the data in device discovery notification part 0
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.timeout_pairing_sequence(
            self,
            self.spy_receiver_port_index,
            device_discovery[DeviceDiscovery.PART.CONFIGURATION].data.bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for the end of the renewed 3 minutes timeout minus a few seconds (to let time '
                                 'to catch discovery notifications and start pre-paired receiver)')
        # --------------------------------------------------------------------------------------------------------------
        time.sleep(DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT
                   - PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN
                   - BleProSafePrePairedReceiverTestUtils.DISCOVERABLE_TIME
                   - BleProSafePrePairedReceiverTestUtils.PRE_PAIRED_RCV_SEARCH_TIME
                   - 2 * ReceiverTestUtils.RECEIVER_SWITCHING_TIME)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(self, self.spy_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device Discovery notifications are still received near the end of the 3 '
                                  'minutes timeout')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self, PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE)
        self.assertNotNone(
            device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn on pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.channel_enable(self.pre_paired_receiver_port_index,
                            BleProSafePrePairedReceiverTestUtils.DISCOVERABLE_TIME +
                            BleProSafePrePairedReceiverTestUtils.PRE_PAIRED_RCV_SEARCH_TIME)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.MFG)

        DevicePairingTestUtils.check_connection_status(
            self, self.rcv_prepairing_slot, DeviceConnection.LinkStatus.LINK_ESTABLISHED, log_step=True, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'check the DUT is able to send an HID report')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0013")
    # end def test_prepairing_after_3_minutes_timeout_reset_on_pairing_timeout

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    @services('MultiHost')
    def test_reuse_prepairing_on_slot_already_paired(self):
        """
        Check device pre pairing data is reset when a pre-pairing is erased
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pre Pair Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.pre_pairing_sequence(
            self,
            self.feature_1816,
            self.feature_1816_index,
            self.rcv_prepairing_slot,
            self.ltk_key,
            self.irk_local_key,
            self.irk_remote_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Change host on Device')
        # --------------------------------------------------------------------------------------------------------------
        prepaired_channel = DeviceManagerUtils.get_channel(test_case=self, channel_id=ChannelIdentifier(
            port_index=self.pre_paired_receiver_port_index, device_index=self.rcv_prepairing_slot))
        tries_counter = 5
        ChannelUtils.empty_queue(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT)
        time.sleep(.5)
        while tries_counter > 0 and not prepaired_channel.is_device_connected(force_refresh_cache=True):
            DevicePairingTestUtils.change_host_by_link_state(
                self, link_state=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED)
            time.sleep(2)
            tries_counter -= 1
        # end while

        assert tries_counter > 0, "Failed to switch on CH2"

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a user action')
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Switch communication to the spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(self, self.spy_receiver_port_index)

        # Fetch Device USB Descriptors matching the spy receiver interfaces configuration
        ChannelUtils.get_descriptors(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the Easy switch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Restart the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Restart the pairing sequence')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a user action')
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off the spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.close_channel(test_case=self)
        LibusbDriver.disable_usb_port(port_index=self.spy_receiver_port_index)

        try:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Switch communication to the pre-paired receiver')
            # ----------------------------------------------------------------------------------------------------------
            self.channel_enable(self.pre_paired_receiver_port_index, wait_device_notification=False)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check no HID report is received when a user action is performed')
            # ----------------------------------------------------------------------------------------------------------
            DeviceBaseTestUtils.ButtonHelper.check_no_hid_report(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the Easy switch button')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH2)
            # Fetch Device USB Descriptors matching the pre-paired interfaces configuration
            ChannelUtils.get_descriptors(test_case=self)
            time.sleep(BleProSafePrePairedReceiverTestUtils.DISCOVERABLE_TIME +
                       BleProSafePrePairedReceiverTestUtils.PRE_PAIRED_RCV_SEARCH_TIME)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Verify an HID report can be received')
            # ----------------------------------------------------------------------------------------------------------
            DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        finally:
            self.channel_enable(self.spy_receiver_port_index, wait_device_notification=False)
        # end try

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0030")
    # end def test_reuse_prepairing_on_slot_already_paired

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @level('Business')
    @services('MultiHost')
    def test_oob_state(self):
        """
        Check device connects to pre-paired receiver after a reset to OOB state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pre Pair Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        receiver_address, device_address = BleProSafePrePairedReceiverTestUtils.pre_pairing_sequence(
            self,
            self.feature_1816,
            self.feature_1816_index,
            self.rcv_prepairing_slot,
            self.ltk_key,
            self.irk_local_key,
            self.irk_remote_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.close_channel(test_case=self)
        LibusbDriver.disable_usb_port(port_index=self.pre_paired_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter discoverable mode on channel 1')
        # --------------------------------------------------------------------------------------------------------------
        # Long press on the connect button or the Easy Switch CH1
        self._enter_discoverable_mode(channel_id=HOST.CH1, click_count=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Switch communication to the spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        ReceiverTestUtils.switch_to_receiver(self, self.spy_receiver_port_index)

        # Fetch Device USB Descriptors matching the spy receiver interfaces configuration
        ChannelUtils.get_descriptors(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Restart the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Restart the pairing sequence')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection)
        device_index = DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a user action')
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable Hidden features and set OOB state')
        # --------------------------------------------------------------------------------------------------------------
        DeviceManagerUtils.set_channel(
            test_case=self, new_channel_id=ChannelIdentifier(device_index=device_index,
                                                             port_index=self.spy_receiver_port_index))
        DeviceBaseTestUtils.HIDppHelper.set_oob_state(
            self, device_index=device_index, port_index=self.spy_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn on pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.channel_enable(self.pre_paired_receiver_port_index,
                            BleProSafePrePairedReceiverTestUtils.DISCOVERABLE_TIME +
                            BleProSafePrePairedReceiverTestUtils.PRE_PAIRED_RCV_SEARCH_TIME,
                            wait_device_notification=False)

        DeviceManagerUtils.set_channel(
            test_case=self,
            new_channel_id=ChannelIdentifier(
                port_index=ChannelUtils.get_port_index(test_case=self), device_index=self.rcv_prepairing_slot),
            open_channel=False)
        self.backup_dut_channel.hid_dispatcher.dump_mapping_in_other_dispatcher(
            other_dispatcher=self.current_channel.hid_dispatcher)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reset device')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ResetHelper.hardware_reset(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for the device reconnection')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.wait_for_channel_device_to_be_connected(test_case=self)
        ChannelUtils.open_channel(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get Device USB Descriptors matching the pre-paired receiver interfaces configuration')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.get_descriptors(test_case=self)

        expected_host_index = 0

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, expected_host_index, ConnectIdChunkData.PairingSrc.MFG)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check BLE Bond Id Chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=expected_host_index,
                                                                        active_bank_only=True)
        self.assertEqual(obtained=ble_bond_id_chunks[-1].master_bluetooth_address,
                         expected=receiver_address,
                         msg='Master Bluetooth Address in NVS should be the Receiver Address')
        self.assertEqual(obtained=ble_bond_id_chunks[-1].bluetooth_low_energy_address.device_bluetooth_address,
                         expected=device_address,
                         msg='Device Bluetooth Address in NVS should be the device address from pre pairing sequence')
        self.assertEqual(obtained=ble_bond_id_chunks[-1].local_ble_gap_enc_info.enc_info_long_term_key,
                         expected=BleProPrePairingTestUtils.get_key(self, 'long_term_key'),
                         msg='LTK Key should be the pre pairing one')
        self.assertEqual(obtained=ble_bond_id_chunks[-1].remote_identity_key.identity_resolving_key,
                         expected=BleProPrePairingTestUtils.get_key(self, 'remote_identity_resolving_key'),
                         msg='IRK Remote Key should be the pre pairing one')
        self.assertEqual(obtained=ble_bond_id_chunks[-1].local_identity_key.identity_resolving_key,
                         expected=BleProPrePairingTestUtils.get_key(self, 'local_identity_resolving_key'),
                         msg='IRK Local Key should be the pre pairing one')

        DevicePairingTestUtils.check_connection_status(
            self, self.rcv_prepairing_slot, DeviceConnection.LinkStatus.LINK_ESTABLISHED, log_step=True, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0034")
    # end def test_oob_state

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @level('Business')
    @services('MultiHost')
    def test_not_empty_slot_business(self):
        """
        Check device connects on pre-paired receiver when slot is not empty and pre-paired receiver is in range
        """
        self.device_nvs_host_index = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pre Pair Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        ReceiverTestUtils.switch_to_receiver(self, self.pre_paired_receiver_port_index)
        DeviceManagerUtils.set_channel(
            test_case=self, new_channel_id=ChannelIdentifier(
                port_index=ChannelUtils.get_port_index(test_case=self), device_index=self.original_device_index))
        self.receiver_address, self.device_address = self._pre_pair_receiver_with_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on Spy Receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(self, self.spy_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter pairing mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check DUT is never discoverable')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self,
            max(BleProSafePrePairedReceiverTestUtils.PRE_PAIRED_RCV_SEARCH_TIME,
                float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)),
            max_tries=1,
            raise_err=False
        )
        self.assertNone(device_discovery, 'No discovery notifications should have been received')

        BleProSafePrePairedReceiverTestUtils.SpyReceiver.cancel_discovery(self, self.spy_receiver_port_index)
        ReceiverTestUtils.switch_to_receiver(self, self.pre_paired_receiver_port_index)

        # Fetch Device USB Descriptors matching the pre-paired receiver interfaces configuration
        ChannelUtils.get_descriptors(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self._read_pairing_slot_status()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.MFG)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check BLE Bond Id Chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self._check_pre_pairing_ble_bond_id_chunk_in_nvs(host_index=self.device_nvs_host_index,
                                                         chunk_index=-1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a user action')
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Check link is established')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.check_connection_status(
            self, self.rcv_prepairing_slot, DeviceConnection.LinkStatus.LINK_ESTABLISHED, log_step=True, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check BLE Pro device pairing information')
        # --------------------------------------------------------------------------------------------------------------
        self._check_ble_pro_device_pairing_information()

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0014")
    # end def test_not_empty_slot_business

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @level('Functionality')
    @services('MultiHost')
    def test_not_empty_slot_receiver_off_on_transition(self):
        """
        Check device connects on pre-paired receiver when receiver is turned on while this slot 1 isn't empty
        """
        self.device_nvs_host_index = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pre Pair Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        ReceiverTestUtils.switch_to_receiver(self, self.pre_paired_receiver_port_index)
        DeviceManagerUtils.set_channel(
            test_case=self, new_channel_id=ChannelIdentifier(
                port_index=ChannelUtils.get_port_index(test_case=self), device_index=self.original_device_index))
        self.receiver_address, self.device_address = self._pre_pair_receiver_with_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off the pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        self._turn_off_pre_paired_rcv()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(self, self.spy_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter pairing mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
        # --------------------------------------------------------------------------------------------------------------
        self._check_device_discovery_notifications_are_received_while_dut_is_discoverable()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn on pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.channel_enable(self.pre_paired_receiver_port_index,
                            BleProSafePrePairedReceiverTestUtils.DISCOVERABLE_TIME +
                            BleProSafePrePairedReceiverTestUtils.PRE_PAIRED_RCV_SEARCH_TIME)

        # Fetch Device USB Descriptors matching the pre-paired receiver interfaces configuration
        ChannelUtils.get_descriptors(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.MFG)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check BLE Bond Id Chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self._check_pre_pairing_ble_bond_id_chunk_in_nvs(host_index=self.device_nvs_host_index,
                                                         chunk_index=-1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Check link is established')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.check_connection_status(
            self, self.rcv_prepairing_slot, DeviceConnection.LinkStatus.LINK_ESTABLISHED, log_step=True, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0015")
    # end def test_not_empty_slot_receiver_off_on_transition

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    @services('MultiHost')
    def test_not_empty_slot_pre_paired_receiver_off_user_pairing(self):
        """
        Check DUT can be paired an other host if pre paired receiver is not present when slot isn't empty
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pre Pair Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        self._pre_pair_receiver_with_device()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Turn off the pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        self._turn_off_pre_paired_rcv()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair device slot 2 with other receiver')
        # --------------------------------------------------------------------------------------------------------------
        self._pair_slot_2_to_second_receiver()
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=1)
        # record bluetooth addresses before the test
        slot2_master_bluetooth_address = []
        slot2_device_bluetooth_address = []
        slot2_master_bluetooth_address.append(ble_bond_id_chunks[-1].master_bluetooth_address)
        slot2_device_bluetooth_address.append(
            ble_bond_id_chunks[-1].bluetooth_low_energy_address.device_bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(self, self.spy_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter pairing mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = self._check_device_discovery_notifications_are_received_while_dut_is_discoverable()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pair device with second receiver')
        # --------------------------------------------------------------------------------------------------------------
        # noinspection PyUnresolvedReferences
        # bluetooth_address is part of the data in device discovery notification part 0
        device_index = BleProSafePrePairedReceiverTestUtils.SpyReceiver.pair_device(
            self,
            self.spy_receiver_port_index,
            device_discovery[DeviceDiscovery.PART.CONFIGURATION].data.bluetooth_address)

        DevicePairingTestUtils.check_connection_status(
            self, device_index, DeviceConnection.LinkStatus.LINK_ESTABLISHED, log_step=True, log_check=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.USR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device slot 2 address is changed')
        # --------------------------------------------------------------------------------------------------------------
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)
        slot2_master_bluetooth_address.append(ble_bond_id_chunks[-1].master_bluetooth_address)
        slot2_device_bluetooth_address.append(
            ble_bond_id_chunks[-1].bluetooth_low_energy_address.device_bluetooth_address)
        self.assertNotEqual(obtained=str(slot2_device_bluetooth_address[0]),
                            unexpected=str(slot2_device_bluetooth_address[1]),
                            msg=f'BLE device address for pairing slot {self.device_nvs_host_index} should be changed ('
                                f'obtained:' + str(
                                slot2_device_bluetooth_address[0]) + ', expected:' + str(
                                slot2_device_bluetooth_address[1]))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device slot 2 is re-paired to the second receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(obtained=str(slot2_master_bluetooth_address[0]),
                         expected=str(slot2_master_bluetooth_address[1]),
                         msg=f'BLE master (receiver) address for pairing slot {self.device_nvs_host_index} should be '
                             f'unchanged')

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0016")
    # end def test_not_empty_slot_pre_paired_receiver_off_user_pairing

    @features('SafePrePairedReceiver')
    @features('MultipleChannels', HOST.CH2)
    @features('Feature1816')
    @level('Functionality')
    def test_not_empty_slot_pre_paired_receiver_off_no_pairing_no_user_action(self):
        """
         Check DUT remains discoverable during 3 minutes if pre paired receiver is not present
         (without user action on DUT during the 3 minutes) when current slot isn't empty
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair device slot 2 with other receiver')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection)
        self._turn_off_pre_paired_rcv()
        self._pair_slot_2_to_second_receiver()
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=1)
        # record bluetooth addresses before the test
        slot2_master_bluetooth_address = []
        slot2_device_bluetooth_address = []
        slot2_master_bluetooth_address.append(ble_bond_id_chunks[-1].master_bluetooth_address)
        slot2_device_bluetooth_address.append(
            ble_bond_id_chunks[-1].bluetooth_low_energy_address.device_bluetooth_address)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pre Pair Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        self._turn_on_pre_paired_rcv()
        ReceiverTestUtils.switch_to_receiver(self, self.pre_paired_receiver_port_index)
        DeviceManagerUtils.set_channel(
            test_case=self, new_channel_id=ChannelIdentifier(
                port_index=ChannelUtils.get_port_index(test_case=self), device_index=self.original_device_index))
        DeviceBaseTestUtils.NvsHelper.change_host(self, self.memory_manager, 0)
        self.receiver_address, self.device_address = self._pre_pair_receiver_with_device()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Switch to user paired slot on device')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.NvsHelper.change_host(self, self.memory_manager, self.device_nvs_host_index,
                                                  ConnectIdChunkData.PairingSrc.USR)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Turn off the pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        self._turn_off_pre_paired_rcv()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(self, self.spy_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter pairing mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH2)

        start_time = time.perf_counter()

        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT
        tolerance = DiscoveryTestUtils.DEVICE_DISCOVERY_TOLERANCE
        while time.perf_counter() < end_time - tolerance:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        # Do not check the discovery notifications around the scheduled timeout with a tolerance of 12s before and after
        time.sleep(float(tolerance * 2))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
            self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device is not discoverable anymore after timeout')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self,
            float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN),
            max_tries=1,
            raise_err=False
        )
        self.assertNone(device_discovery, 'No discovery notifications should have been received')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.USR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device slot 2 address is not changed')
        # --------------------------------------------------------------------------------------------------------------
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)
        slot2_master_bluetooth_address.append(ble_bond_id_chunks[-1].master_bluetooth_address)
        slot2_device_bluetooth_address.append(
            ble_bond_id_chunks[-1].bluetooth_low_energy_address.device_bluetooth_address)
        self.assertEqual(obtained=str(slot2_device_bluetooth_address[0]),
                         expected=str(slot2_device_bluetooth_address[1]),
                         msg=f'BLE device address for pairing slot {self.device_nvs_host_index} should be changed ('
                             f'obtained:' + str(slot2_device_bluetooth_address[0]) + ', '
                                                                                     f'expected:' + str(
                             slot2_device_bluetooth_address[1]))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device slot 2 is always paired to the second receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(obtained=str(slot2_master_bluetooth_address[0]),
                         expected=str(slot2_master_bluetooth_address[1]),
                         msg=f'BLE master (receiver) address for pairing slot {self.device_nvs_host_index} should be '
                             f'unchanged')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Check link is established')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.check_connection_status(
            self, self.device_nvs_host_index, DeviceConnection.LinkStatus.LINK_ESTABLISHED,
            log_step=True, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a user action')
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0017")
    # end def test_not_empty_slot_pre_paired_receiver_off_no_pairing_no_user_action

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    def test_not_empty_slot_pre_paired_receiver_off_no_pairing_user_action(self):
        """
        Check all user actions, except EasySwitch, don't impact the 3 minutes "pairing mode" timeout
        when slot isn't empty
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair device slot 2 with other receiver')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection)
        self._turn_off_pre_paired_rcv()
        self._pair_slot_2_to_second_receiver()
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=1)
        # record bluetooth addresses before the test
        slot2_master_bluetooth_address = []
        slot2_device_bluetooth_address = []
        slot2_master_bluetooth_address.append(ble_bond_id_chunks[-1].master_bluetooth_address)
        slot2_device_bluetooth_address.append(
            ble_bond_id_chunks[-1].bluetooth_low_energy_address.device_bluetooth_address)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pre Pair Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        self._turn_on_pre_paired_rcv()
        ReceiverTestUtils.switch_to_receiver(self, self.pre_paired_receiver_port_index)
        DeviceManagerUtils.set_channel(
            test_case=self, new_channel_id=ChannelIdentifier(
                port_index=ChannelUtils.get_port_index(test_case=self), device_index=self.original_device_index))
        DeviceBaseTestUtils.NvsHelper.change_host(self, self.memory_manager, 0)
        self.receiver_address, self.device_address = self._pre_pair_receiver_with_device()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Switch to user paired slot on device')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.NvsHelper.change_host(self, self.memory_manager, self.device_nvs_host_index,
                                                  ConnectIdChunkData.PairingSrc.USR)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Turn off the pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        self._turn_off_pre_paired_rcv()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(self, self.spy_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter pairing mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH2)

        start_time = time.perf_counter()

        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT - \
            PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN
        while time.perf_counter() < end_time:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Perform User Action')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.user_action()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            self._check_device_discovery_notifications_are_received_while_dut_is_discoverable()
        # end while

        time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
            self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device is not discoverable anymore after timeout')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self,
            float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN),
            max_tries=1,
            raise_err=False
        )
        self.assertNone(device_discovery, 'No discovery notifications should have been received')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.USR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check BLE Bond Id Chunk for pre-pairing slot has been created in NVS')
        # --------------------------------------------------------------------------------------------------------------
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=0)
        self.assertGreater(len(ble_bond_id_chunks), 0, "BLE Bond Id chunk should have been created in NVS")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device slot 2 address is not changed')
        # --------------------------------------------------------------------------------------------------------------
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)
        slot2_master_bluetooth_address.append(ble_bond_id_chunks[-1].master_bluetooth_address)
        slot2_device_bluetooth_address.append(
            ble_bond_id_chunks[-1].bluetooth_low_energy_address.device_bluetooth_address)
        self.assertEqual(obtained=str(slot2_device_bluetooth_address[0]),
                         expected=str(slot2_device_bluetooth_address[1]),
                         msg=f'BLE device address for pairing slot {self.device_nvs_host_index} should be changed ('
                             f'obtained:' + str(slot2_device_bluetooth_address[0]) + ', '
                                                                                     f'expected:' + str(
                             slot2_device_bluetooth_address[1]))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device slot 2 is always paired to the second receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(obtained=str(slot2_master_bluetooth_address[0]),
                         expected=str(slot2_master_bluetooth_address[1]),
                         msg=f'BLE master (receiver) address for pairing slot {self.device_nvs_host_index} should be '
                             f'unchanged')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Check link is established')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.check_connection_status(
            self, self.device_nvs_host_index, DeviceConnection.LinkStatus.LINK_ESTABLISHED,
            log_step=True, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a user action')
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0018")
    # end def test_not_empty_slot_pre_paired_receiver_off_no_pairing_user_action

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    @services('PowerSupply')
    def test_not_empty_slot_pre_paired_receiver_connection_critical_battery(self):
        """
        Check the battery level does not impact the "pairing mode" state machine when slot isn't empty
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair device slot 2 with other receiver')
        # --------------------------------------------------------------------------------------------------------------
        self._turn_off_pre_paired_rcv()
        self._pair_slot_2_to_second_receiver()
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)
        # record bluetooth addresses before the test
        slot2_master_bluetooth_address = []
        slot2_device_bluetooth_address = []
        slot2_master_bluetooth_address.append(ble_bond_id_chunks[-1].master_bluetooth_address)
        slot2_device_bluetooth_address.append(
            ble_bond_id_chunks[-1].bluetooth_low_energy_address.device_bluetooth_address)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pre Pair Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        self._turn_on_pre_paired_rcv()
        ReceiverTestUtils.switch_to_receiver(self, self.pre_paired_receiver_port_index)
        DeviceBaseTestUtils.NvsHelper.change_host(self, self.memory_manager, 0)
        self.receiver_address, self.device_address = self._pre_pair_receiver_with_device()
        # get battery critical value
        ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=UnifiedBattery.FEATURE_ID,
            channel=DeviceManagerUtils.get_channel(test_case=self, channel_id=ChannelIdentifier(
                port_index=ChannelUtils.get_port_index(test_case=self), device_index=self.original_device_index)))

        critical_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'critical')
        battery_critical = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, critical_state_of_charge)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Switch to user paired slot on device')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.NvsHelper.change_host(self, self.memory_manager, self.device_nvs_host_index,
                                                  ConnectIdChunkData.PairingSrc.USR)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Turn off the pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        self._turn_off_pre_paired_rcv()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set battery critical level')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(battery_critical)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(self, self.spy_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter pairing mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
        # --------------------------------------------------------------------------------------------------------------
        self._check_device_discovery_notifications_are_received_while_dut_is_discoverable()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn on pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.channel_enable(self.pre_paired_receiver_port_index,
                            BleProSafePrePairedReceiverTestUtils.DISCOVERABLE_TIME +
                            BleProSafePrePairedReceiverTestUtils.PRE_PAIRED_RCV_SEARCH_TIME)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.MFG)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check BLE Bond Id Chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self._check_pre_pairing_ble_bond_id_chunk_in_nvs(host_index=self.device_nvs_host_index,
                                                         chunk_index=-1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check link is established')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.check_connection_status(
            self, self.rcv_prepairing_slot, DeviceConnection.LinkStatus.LINK_ESTABLISHED, log_step=True, log_check=True)

        # Fetch Device USB Descriptors matching the pre-paired receiver interfaces configuration
        ChannelUtils.get_descriptors(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a user action')
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0019")
    # end def test_not_empty_slot_pre_paired_receiver_connection_critical_battery

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    @services('PowerSupply')
    def test_not_empty_slot_pre_paired_receiver_off_no_pairing_low_to_critical_battery(self):
        """
        Check the battery low level to critical change does not impact the "pairing mode" state machine
        when slot isn't empty
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair device slot 2 with other receiver')
        # --------------------------------------------------------------------------------------------------------------
        self._turn_off_pre_paired_rcv()
        self._pair_slot_2_to_second_receiver()
        initial_ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)
        # record bluetooth addresses before the test
        slot2_master_bluetooth_address = []
        slot2_device_bluetooth_address = []
        slot2_master_bluetooth_address.append(initial_ble_bond_id_chunks[-1].master_bluetooth_address)
        slot2_device_bluetooth_address.append(
            initial_ble_bond_id_chunks[-1].bluetooth_low_energy_address.device_bluetooth_address)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pre Pair Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        self._turn_on_pre_paired_rcv()
        ReceiverTestUtils.switch_to_receiver(self, self.pre_paired_receiver_port_index)
        DeviceBaseTestUtils.NvsHelper.change_host(self, self.memory_manager, 0)
        self.receiver_address, self.device_address = self._pre_pair_receiver_with_device()
        # Get battery levels
        ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=UnifiedBattery.FEATURE_ID,
            channel=DeviceManagerUtils.get_channel(test_case=self, channel_id=ChannelIdentifier(
                port_index=ChannelUtils.get_port_index(test_case=self), device_index=self.original_device_index)))
        low_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'low')
        battery_low = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, low_state_of_charge)
        critical_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'critical')
        battery_critical = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, critical_state_of_charge)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Switch to user paired slot on device')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.NvsHelper.change_host(self, self.memory_manager, self.device_nvs_host_index,
                                                  ConnectIdChunkData.PairingSrc.USR)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Turn off the pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        self._turn_off_pre_paired_rcv()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Change Host')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.NvsHelper.change_host(
            self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.USR)
        start_time = time.perf_counter()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter pairing mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set battery low level')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(battery_low)

        critical_battery_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT / 2
        critical_battery = False
        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT
        tolerance = DiscoveryTestUtils.DEVICE_DISCOVERY_TOLERANCE
        while time.perf_counter() < end_time - tolerance:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            if not critical_battery and time.perf_counter() > critical_battery_time:
                # ----------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Set battery critical level')
                # ----------------------------------------------------------------------------------------------------------
                self.power_supply_emulator.set_voltage(battery_critical)
                critical_battery = True
            # end if

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        # Do not check the discovery notifications around the scheduled timeout with a tolerance of 12s before and after
        time.sleep(float(tolerance * 2))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
            self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device is not discoverable anymore after timeout')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self,
            float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN),
            max_tries=1,
            raise_err=False
        )
        self.assertNone(device_discovery, 'No discovery notifications should have been received')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.USR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check BLE Bond Id Chunk for pairing slot {self.device_nvs_host_index} has not '
                                  f'been created in NVS')
        # --------------------------------------------------------------------------------------------------------------
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)
        self.assertEqual(obtained=len(ble_bond_id_chunks),
                         expected=len(initial_ble_bond_id_chunks),
                         msg=f'No BLE Bond Id chunk for pairing slot {self.device_nvs_host_index} '
                             f'should be created in NVS')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check link is established')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.check_connection_status(
            self, self.device_nvs_host_index, DeviceConnection.LinkStatus.LINK_ESTABLISHED,
            log_step=True, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a user action')
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0020")
    # end def test_not_empty_slot_pre_paired_receiver_off_no_pairing_low_to_critical_battery

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    def test_not_empty_slot_pre_pairing_erased_in_receiver_slot_paired_with_second_receiver(self):
        """
        Check DUT remains discoverable during 3 minutes if pre paired slot has been erased in receiver
        when slot is paired with a second receiver
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'pre-pairing is erased')
        # --------------------------------------------------------------------------------------------------------------
        # Pre Pair Receiver with Device
        self._pre_pair_receiver_with_device()
        # Enable Manufacturing test mode
        ReceiverTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
        BleProReceiverPrepairingTestUtils.set_prepairing_management(
            self, self.rcv_prepairing_slot, PrepairingManagement.PrepairingManagementControl.DELETE)
        TDETestUtils.set_test_mode_control(self, TestModeControl.TestModeEnable.DISABLE_TEST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair device slot 2 with other receiver')
        # --------------------------------------------------------------------------------------------------------------
        self._turn_off_pre_paired_rcv()
        self._pair_slot_2_to_second_receiver()
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)
        # record bluetooth addresses before the test
        slot2_master_bluetooth_address = []
        slot2_device_bluetooth_address = []
        slot2_master_bluetooth_address.append(ble_bond_id_chunks[-1].master_bluetooth_address)
        slot2_device_bluetooth_address.append(
            ble_bond_id_chunks[-1].bluetooth_low_energy_address.device_bluetooth_address)

        self.memory_manager.read_nvs()
        initial_ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)

        self._turn_on_pre_paired_rcv()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter pairing mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH2)

        # --------------------------------------------------------------------------------------------------------------
        start_time = time.perf_counter()

        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT
        tolerance = DiscoveryTestUtils.DEVICE_DISCOVERY_TOLERANCE
        while time.perf_counter() < end_time - tolerance:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        # Do not check the discovery notifications around the scheduled timeout with a tolerance of 12s before and after
        time.sleep(float(tolerance * 2))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
            self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device is not discoverable anymore after timeout')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self,
            float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN),
            max_tries=1,
            raise_err=False
        )
        self.assertNone(device_discovery, 'No discovery notifications should have been received')
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.USR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check BLE Bond Id Chunk for pairing slot {self.device_nvs_host_index} has not '
                                  f'been created in NVS')
        # --------------------------------------------------------------------------------------------------------------
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)
        self.assertEqual(obtained=len(ble_bond_id_chunks),
                         expected=len(initial_ble_bond_id_chunks),
                         msg=f'No BLE Bond Id chunk for pairing slot {self.device_nvs_host_index} '
                             f'should be created in NVS')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check link is established')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.check_connection_status(
            self, self.device_nvs_host_index, DeviceConnection.LinkStatus.LINK_ESTABLISHED,
            log_step=True, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a user action')
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0021")
    # end def test_not_empty_slot_pre_pairing_erased_in_receiver_slot_paired_with_second_receiver

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    def test_not_empty_slot_pre_pairing_erased_in_receiver_slot_paired_with_pre_paired_receiver(self):
        """
        Check DUT remains discoverable during 3 minutes if pre paired slot has been erased in receiver
        when slot was paired with the pre-paired receiver
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Use Pre Paired Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        self.test_empty_slot_business()

        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)
        # record bluetooth addresses before the test
        slot2_master_bluetooth_address = []
        slot2_device_bluetooth_address = []
        slot2_master_bluetooth_address.append(ble_bond_id_chunks[-1].master_bluetooth_address)
        slot2_device_bluetooth_address.append(
            ble_bond_id_chunks[-1].bluetooth_low_energy_address.device_bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'pre-pairing is erased')
        # --------------------------------------------------------------------------------------------------------------
        # Enable Manufacturing test mode
        ReceiverTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
        BleProReceiverPrepairingTestUtils.set_prepairing_management(
            self, self.rcv_prepairing_slot, PrepairingManagement.PrepairingManagementControl.DELETE)
        TDETestUtils.set_test_mode_control(self, TestModeControl.TestModeEnable.DISABLE_TEST_MODE)

        initial_ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter pairing mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH2)

        # --------------------------------------------------------------------------------------------------------------
        start_time = time.perf_counter()

        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT
        tolerance = DiscoveryTestUtils.DEVICE_DISCOVERY_TOLERANCE
        while time.perf_counter() < end_time - tolerance:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=(DeviceDiscovery, DiscoveryStatus))
        # end while

        # Do not check the discovery notifications around the scheduled timeout with a tolerance of 12s before and after
        time.sleep(float(tolerance * 2))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
            self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DiscoveryStatus)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device is not discoverable anymore after timeout')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self,
            float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN),
            max_tries=1,
            raise_err=False
        )
        self.assertNone(device_discovery, 'No discovery notifications should have been received')
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.MFG)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check BLE Bond Id Chunk for pairing slot '
                                  f'{self.device_nvs_host_index} has not been created in NVS')
        # --------------------------------------------------------------------------------------------------------------
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)
        self.assertEqual(obtained=len(ble_bond_id_chunks),
                         expected=len(initial_ble_bond_id_chunks),
                         msg=f'No BLE Bond Id chunk for pairing slot {self.device_nvs_host_index} '
                             f'should be created in NVS')

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0022")
    # end def test_not_empty_slot_pre_pairing_erased_in_receiver_slot_paired_with_pre_paired_receiver

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    def test_not_empty_slot_wrong_pre_pairing(self):
        """
        Check DUT remains discoverable during 3 minutes if pre pairing is wrong (either on DUT side or receiver side)
        when slot isn't empty
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pre Pair Receiver with Device but with a wrong LTK Key')
        # ----------------------------------------------------------------------------------------------------------------
        # Enable Manufacturing test mode
        ReceiverTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
        wrong_ltk_key = HexList('0F0E0D0C0B0A09080706050403020100')
        assert wrong_ltk_key != self.ltk_key
        (receiver_address, device_address, ltk_key, irk_local_key, irk_remote_key, csrk_local_key,
         csrk_remote_key) = BleProReceiverPrepairingTestUtils.receiver_prepairing_sequence(
            self,
            self.rcv_prepairing_slot,
            wrong_ltk_key,
            self.irk_local_key,
            self.irk_remote_key,
            pre_pairing_main_class=self.feature_1816,
            pre_pairing_index=self.feature_1816_index
        )

        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index,
            long_term_key=self.ltk_key,
            remote_identity_resolving_key=self.irk_local_key, local_identity_resolving_key=self.irk_remote_key,
            remote_connection_signature_resolving_key=None, local_connection_signature_resolving_key=None,
            receiver_address=receiver_address, start=False)

        ReceiverTestUtils.reset_receiver(self)

        ChannelUtils.get_only(
            test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, class_type=WirelessDeviceStatusBroadcastEvent,
            check_first_message=False, allow_no_message=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair device slot 2 with other receiver')
        # --------------------------------------------------------------------------------------------------------------
        self._turn_off_pre_paired_rcv()
        self._pair_slot_2_to_second_receiver()
        self._turn_on_pre_paired_rcv()

        self.memory_manager.read_nvs()
        initial_ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter pairing mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH2)

        # --------------------------------------------------------------------------------------------------------------
        start_time = time.perf_counter()

        # The discovery timeout is shorter in this case because the time spent to look for the pre paired receiver is
        # negligible
        discovery_timeout = 28 * 5.0
        end_time = start_time + discovery_timeout
        tolerance = float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
        while time.perf_counter() < end_time - tolerance:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        time.sleep(float(start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT - time.perf_counter()))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
            self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device is not discoverable anymore after timeout')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self,
            float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN),
            max_tries=1,
            raise_err=False
        )
        self.assertNone(device_discovery, 'No discovery notifications should have been received')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.USR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check BLE Bond Id Chunk for pairing slot {self.device_nvs_host_index} has not '
                                  f'been created in NVS')
        # --------------------------------------------------------------------------------------------------------------
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)
        self.assertEqual(obtained=len(ble_bond_id_chunks),
                         expected=len(initial_ble_bond_id_chunks),
                         msg=f'No BLE Bond Id chunk for pairing slot {self.device_nvs_host_index} '
                             f'should be created in NVS')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check link is established')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.check_connection_status(
            self, self.device_nvs_host_index, DeviceConnection.LinkStatus.LINK_ESTABLISHED,
            log_step=True, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a user action')
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0023")
    # end def test_not_empty_slot_wrong_pre_pairing

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    def test_3_minutes_discoverable_pre_pairing_used_on_current_slot(self):
        """
        Check DUT remains discoverable during 3 minutes if pre paired receiver is already used on current slot
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Use Pre Paired Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        self._pre_pairing_channel_1(check_connection=True)
        initial_ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter pairing mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH1)
        # --------------------------------------------------------------------------------------------------------------
        start_time = time.perf_counter()

        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT
        tolerance = DiscoveryTestUtils.DEVICE_DISCOVERY_TOLERANCE
        while time.perf_counter() < end_time - tolerance:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self,
                channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                class_type=(DeviceDiscovery, DiscoveryStatus))
        # end while

        # Do not check the discovery notifications around the scheduled timeout with a tolerance of 12s before and after
        time.sleep(float(tolerance * 2))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
            self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DiscoveryStatus)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device is not discoverable anymore after timeout')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self,
            float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN),
            max_tries=1,
            raise_err=False
        )
        self.assertNone(device_discovery, 'No discovery notifications should have been received')
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.MFG)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check BLE Bond Id Chunk for pairing slot {self.device_nvs_host_index} has not '
                                  f'been created in NVS')
        # --------------------------------------------------------------------------------------------------------------
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)
        self.assertEqual(expected=len(initial_ble_bond_id_chunks),
                         obtained=len(ble_bond_id_chunks),
                         msg=f'We expect the number of chunk in NVS to match the initial countfor pairing slot '
                             f'{self.device_nvs_host_index}.')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check selected current slot')
        # --------------------------------------------------------------------------------------------------------------
        device_slot_state = self._read_pairing_slot_status()
        self.assertEqual(obtained=device_slot_state.current_slot,
                         expected=self.device_nvs_host_index,
                         msg=f'Current device selected slot is not the slot #{self.device_nvs_host_index}.')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check link is established')
        # --------------------------------------------------------------------------------------------------------------
        ReceiverTestUtils.switch_to_receiver(self, self.pre_paired_receiver_port_index)
        DevicePairingTestUtils.check_connection_status(
            self, pairing_slot=self.rcv_prepairing_slot,
            expected_connection_status=DeviceConnection.LinkStatus.LINK_ESTABLISHED, log_step=True, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a user action')
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0024")
    # end def test_3_minutes_discoverable_pre_pairing_used_on_current_slot

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @features('MultipleChannels', HOST.CH3)
    @level('Functionality')
    def test_3_minutes_discoverable_pre_pairing_used_on_other_slot(self):
        """
        Check DUT remains discoverable during 3 minutes if pre paired receiver is already used on an other slot
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Use Pre Paired Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        self.test_empty_slot_business()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair device slot 3 with other receiver')
        # --------------------------------------------------------------------------------------------------------------
        self._turn_off_pre_paired_rcv()
        self._pair_to_second_receiver(slot=3)
        self._turn_on_pre_paired_rcv()
        initial_ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter discoverable mode on channel 3')
        # --------------------------------------------------------------------------------------------------------------
        self._enter_discoverable_mode(channel_id=HOST.CH3, click_count=0)

        # --------------------------------------------------------------------------------------------------------------
        start_time = time.perf_counter()

        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT
        tolerance = DiscoveryTestUtils.DEVICE_DISCOVERY_TOLERANCE
        while time.perf_counter() < end_time - tolerance:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        # Do not check the discovery notifications around the scheduled timeout with a tolerance of 12s before and after
        time.sleep(float(tolerance * 2))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
            self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device is not discoverable anymore after timeout')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self,
            float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN),
            max_tries=1,
            raise_err=False
        )
        self.assertNone(device_discovery, 'No discovery notifications should have been received')
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.USR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check BLE Bond Id Chunk for pairing slot {self.device_nvs_host_index} has not '
                                  f'been created in NVS')
        # --------------------------------------------------------------------------------------------------------------
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)
        self.assertEqual(expected=len(initial_ble_bond_id_chunks),
                         obtained=len(ble_bond_id_chunks),
                         msg=f'We expect the number of chunk in NVS to match the initial countfor pairing slot '
                             f'{self.device_nvs_host_index}.')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check selected current slot')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 1
        device_slot_state = self._read_pairing_slot_status()
        self.assertEqual(obtained=device_slot_state.current_slot,
                         expected=self.device_nvs_host_index,
                         msg=f'Current device selected slot is not the slot #{self.device_nvs_host_index + 1}.')
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check link is established')
        # --------------------------------------------------------------------------------------------------------------
        ReceiverTestUtils.switch_to_receiver(self, self.spy_receiver_port_index)
        DevicePairingTestUtils.check_connection_status(
            self, pairing_slot=host_index, expected_connection_status=DeviceConnection.LinkStatus.LINK_ESTABLISHED,
            log_step=True, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a user action')
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0025")
    # end def test_3_minutes_discoverable_pre_pairing_used_on_other_slot

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    def test_repair_pre_pairing_used_on_current_slot(self):
        """
        Check BLE/BLEPro pairing if pre paired receiver is already used on current slot
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Use Pre Paired Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        self.test_empty_slot_business()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter pairing mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(self, self.spy_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self, PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE)
        self.assertNotNone(
            device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pair device with second receiver')
        # --------------------------------------------------------------------------------------------------------------
        # noinspection PyUnresolvedReferences
        # bluetooth_address is part of the data in device discovery notification part 0
        device_index = BleProSafePrePairedReceiverTestUtils.SpyReceiver.pair_device(
            self,
            self.spy_receiver_port_index,
            device_discovery[DeviceDiscovery.PART.CONFIGURATION].data.bluetooth_address)

        DevicePairingTestUtils.check_connection_status(
            self, device_index, DeviceConnection.LinkStatus.LINK_ESTABLISHED)

        # Fetch Device USB Descriptors matching the spy receiver interfaces configuration
        ChannelUtils.get_descriptors(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.USR)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check User action -> Button')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0026")
    # end def test_repair_pre_pairing_used_on_current_slot

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @features('MultipleChannels', HOST.CH3)
    @level('Functionality')
    def test_repair_pre_pairing_used_on_other_slot(self):
        """
        Check BLE/BLEPro pairing if pre paired receiver is already used on an other slot
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Use Pre Paired Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        self.test_empty_slot_business()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair device slot 3 with other receiver')
        # --------------------------------------------------------------------------------------------------------------
        self._turn_off_pre_paired_rcv()
        self._pair_to_second_receiver(slot=3)
        self._turn_on_pre_paired_rcv()
        # record bluetooth addresses before the test
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=2)
        slot2_master_bluetooth_address = []
        slot2_device_bluetooth_address = []
        slot2_master_bluetooth_address.append(ble_bond_id_chunks[-1].master_bluetooth_address)
        slot2_device_bluetooth_address.append(
            ble_bond_id_chunks[-1].bluetooth_low_energy_address.device_bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter pairing mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(self, self.spy_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self, PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE)
        self.assertNotNone(
            device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pair device with second receiver')
        # --------------------------------------------------------------------------------------------------------------
        # noinspection PyUnresolvedReferences
        # bluetooth_address is part of the data in device discovery notification part 0
        device_index = BleProSafePrePairedReceiverTestUtils.SpyReceiver.pair_device(
            self,
            self.spy_receiver_port_index,
            device_discovery[DeviceDiscovery.PART.CONFIGURATION].data.bluetooth_address)

        DevicePairingTestUtils.check_connection_status(
            self, device_index, DeviceConnection.LinkStatus.LINK_ESTABLISHED)

        # Fetch Device USB Descriptors matching the spy receiver interfaces configuration
        ChannelUtils.get_descriptors(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.USR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check User action -> Button')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device slot 3 address is changed')
        # --------------------------------------------------------------------------------------------------------------
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)
        slot2_master_bluetooth_address.append(ble_bond_id_chunks[-1].master_bluetooth_address)
        slot2_device_bluetooth_address.append(
            ble_bond_id_chunks[-1].bluetooth_low_energy_address.device_bluetooth_address)

        self.assertNotEqual(obtained=str(slot2_device_bluetooth_address[0]),
                            unexpected=str(slot2_device_bluetooth_address[1]),
                            msg=f'BLE device address for pairing slot {self.device_nvs_host_index} should be changed ('
                                f'obtained:' + str(
                                slot2_device_bluetooth_address[0]) + ', expected:' + str(
                                slot2_device_bluetooth_address[1]))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device slot 2 is pre-paired to the second receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(obtained=str(slot2_master_bluetooth_address[0]),
                         expected=str(slot2_master_bluetooth_address[1]),
                         msg=f'BLE master (receiver) address for pairing slot {self.device_nvs_host_index} should be '
                             f'unchanged')

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0027")
    # end def test_repair_pre_pairing_used_on_other_slot

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    def test_prepairing_after_3_minutes_timeout_reset_on_pairing_failure_pre_paired_use_on_current_slot(self):
        """
        Check the 3 minutes timer is resetted when a BLE/BLEPro pairing failure occurs
        if pre paired receiver is already used on current slot
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Use Pre Paired Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        self.test_empty_slot_business()
        initial_ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Turn off pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        self._turn_off_pre_paired_rcv()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter pairing mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Device is discoverable until 1 minutes')
        # --------------------------------------------------------------------------------------------------------------
        start_time = time.perf_counter()
        # check discoverable 60 seconds
        end_time = start_time + 60
        device_discovery = None
        while time.perf_counter() < end_time:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a pairing sequence with a bad passkey on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        # noinspection PyUnresolvedReferences
        # bluetooth_address is part of the data in device discovery notification part 0
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.failed_pairing_sequence(
            self,
            self.spy_receiver_port_index,
            device_discovery[DeviceDiscovery.PART.CONFIGURATION].data.bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device is discoverable until 3 minutes (timeout should be reset)')
        # --------------------------------------------------------------------------------------------------------------
        start_time = time.perf_counter()

        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT
        tolerance = DiscoveryTestUtils.DEVICE_DISCOVERY_TOLERANCE
        while time.perf_counter() < end_time - tolerance:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        # Do not check the discovery notifications around the scheduled timeout with a tolerance of 12s before and after
        time.sleep(float(tolerance * 2))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
            self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device is not discoverable anymore after timeout')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self,
            float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN),
            max_tries=1,
            raise_err=False
        )
        self.assertNone(device_discovery, 'No discovery notifications should have been received')
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.MFG)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check BLE Bond Id Chunk for pairing slot {self.device_nvs_host_index} has not '
                                  f'been created in NVS')
        # --------------------------------------------------------------------------------------------------------------
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)
        self.assertEqual(obtained=len(ble_bond_id_chunks),
                         expected=len(initial_ble_bond_id_chunks),
                         msg=f'No BLE Bond Id chunk for pairing slot {self.device_nvs_host_index} should be created '
                             f'in NVS')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check selected current slot')
        # --------------------------------------------------------------------------------------------------------------
        device_slot_state = self._read_pairing_slot_status()
        self.assertEqual(obtained=device_slot_state.current_slot,
                         expected=self.device_nvs_host_index,
                         msg=f'Current device selected slot is not the slot #{self.device_nvs_host_index + 1}.')
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn on pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 2
        self._turn_on_pre_paired_rcv()
        ReceiverTestUtils.switch_to_receiver(self, self.pre_paired_receiver_port_index)
        DevicePairingTestUtils.check_connection_status(
            self, pairing_slot=host_index, expected_connection_status=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED,
            log_step=True, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a user action')
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check link is established')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.check_connection_status(
            self, pairing_slot=host_index, expected_connection_status=DeviceConnection.LinkStatus.LINK_ESTABLISHED,
            log_step=True, log_check=True)

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0028")
    # end def test_prepairing_after_3_minutes_timeout_reset_on_pairing_failure_pre_paired_use_on_current_slot

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @features('MultipleChannels', HOST.CH3)
    @level('Functionality')
    def test_prepairing_after_3_minutes_timeout_reset_on_pairing_failure_pre_paired_use_on_other_slot(self):
        """
        Check the 3 minutes timer is resetted when a BLE/BLEPro pairing failure occurs
        if pre paired receiver is already used on an other current slot
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Use Pre Paired Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        self.test_empty_slot_business()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Turn off pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        self._turn_off_pre_paired_rcv()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair device slot 3 with other receiver')
        # --------------------------------------------------------------------------------------------------------------
        self._pair_to_second_receiver(slot=3)
        initial_ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter pairing mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Device is discoverable until 1 minutes')
        # --------------------------------------------------------------------------------------------------------------
        start_time = time.perf_counter()
        # check discoverable 60 seconds
        end_time = start_time + 60
        device_discovery = None
        while time.perf_counter() < end_time:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a pairing sequence with a bad passkey on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        # noinspection PyUnresolvedReferences
        # bluetooth_address is part of the data in device discovery notification part 0
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.failed_pairing_sequence(
            self,
            self.spy_receiver_port_index,
            device_discovery[DeviceDiscovery.PART.CONFIGURATION].data.bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device is discoverable until 3 minutes (timeout should be reset)')
        # --------------------------------------------------------------------------------------------------------------
        start_time = time.perf_counter()

        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT
        tolerance = DiscoveryTestUtils.DEVICE_DISCOVERY_TOLERANCE
        while time.perf_counter() < end_time - tolerance:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        # Do not check the discovery notifications around the scheduled timeout with a tolerance of 12s before and after
        time.sleep(float(tolerance * 2))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
            self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device is not discoverable anymore after timeout')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self,
            float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN),
            max_tries=1,
            raise_err=False
        )
        self.assertNone(device_discovery, 'No discovery notifications should have been received')
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.USR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check BLE Bond Id Chunk for pairing slot {self.device_nvs_host_index} has not '
                                  f'been created in NVS')
        # --------------------------------------------------------------------------------------------------------------
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)
        self.assertEqual(obtained=len(ble_bond_id_chunks),
                         expected=len(initial_ble_bond_id_chunks),
                         msg=f'No BLE Bond Id chunk for pairing slot {self.device_nvs_host_index} '
                             f'should be created in NVS')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check selected current slot')
        # --------------------------------------------------------------------------------------------------------------
        device_slot_state = self._read_pairing_slot_status()
        self.assertEqual(obtained=device_slot_state.current_slot,
                         expected=self.device_nvs_host_index,
                         msg=f'Current device selected slot is not the slot #{self.device_nvs_host_index + 1}.')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check link is established')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 1
        ReceiverTestUtils.switch_to_receiver(self, self.spy_receiver_port_index)
        DevicePairingTestUtils.check_connection_status(
            self, pairing_slot=host_index, expected_connection_status=DeviceConnection.LinkStatus.LINK_ESTABLISHED,
            log_step=True, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a user action')
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0029")
    # end def test_prepairing_after_3_minutes_timeout_reset_on_pairing_failure_pre_paired_use_on_other_slot

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    def test_prepairing_after_3_minutes_timeout_reset_on_pairing_failure_pre_paired_never_used(self):
        """
        Check the 3 minutes timer is resetted when a BLE/BLEPro pairing failure occurs
        if pre paired receiver is not used
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair device slot 2 with other receiver')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection)
        self._turn_off_pre_paired_rcv()
        self._pair_slot_2_to_second_receiver()
        DeviceManagerUtils.set_channel(
            test_case=self, new_channel_id=ChannelIdentifier(port_index=self.spy_receiver_port_index))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pre Pair Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        self._turn_on_pre_paired_rcv()
        ReceiverTestUtils.switch_to_receiver(self, self.pre_paired_receiver_port_index)
        DeviceBaseTestUtils.NvsHelper.change_host(self, self.memory_manager, 0)
        DeviceManagerUtils.set_channel(
            test_case=self,
            new_channel_id=ChannelIdentifier(
                port_index=ChannelUtils.get_port_index(test_case=self), device_index=self.original_device_index))
        self.receiver_address, self.device_address = self._pre_pair_receiver_with_device()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Switch to user paired slot on device')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.NvsHelper.change_host(self, self.memory_manager, self.device_nvs_host_index,
                                                  ConnectIdChunkData.PairingSrc.USR)
        ReceiverTestUtils.switch_to_receiver(self, self.spy_receiver_port_index)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Turn off the pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        self._turn_off_pre_paired_rcv()
        initial_ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter pairing mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Device is discoverable until 1 minute')
        # --------------------------------------------------------------------------------------------------------------
        start_time = time.perf_counter()
        # check discoverable 60 seconds
        end_time = start_time + 60
        device_discovery = None
        while time.perf_counter() < end_time:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a pairing sequence with a bad passkey on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        # noinspection PyUnresolvedReferences
        # bluetooth_address is part of the data in device discovery notification part 0
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.failed_pairing_sequence(
            self,
            self.spy_receiver_port_index,
            device_discovery[DeviceDiscovery.PART.CONFIGURATION].data.bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device is discoverable until 3 minutes (timeout should be reset)')
        # --------------------------------------------------------------------------------------------------------------
        start_time = time.perf_counter()

        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT
        tolerance = DiscoveryTestUtils.DEVICE_DISCOVERY_TOLERANCE
        while time.perf_counter() < end_time - tolerance:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        # Do not check the discovery notifications around the scheduled timeout with a tolerance of 12s before and after
        time.sleep(float(tolerance * 2))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
            self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device is not discoverable anymore after timeout')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self,
            float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN),
            max_tries=1,
            raise_err=False
        )
        self.assertNone(device_discovery, 'No discovery notifications should have been received')
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.USR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check BLE Bond Id Chunk for pairing slot {self.device_nvs_host_index} has not '
                                  f'been created in NVS')
        # --------------------------------------------------------------------------------------------------------------
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)
        self.assertEqual(obtained=len(ble_bond_id_chunks),
                         expected=len(initial_ble_bond_id_chunks),
                         msg=f'No BLE Bond Id chunk for pairing slot {self.device_nvs_host_index} should be created '
                             f'in NVS')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check selected current slot')
        # --------------------------------------------------------------------------------------------------------------
        device_slot_state = self._read_pairing_slot_status()
        self.assertEqual(obtained=device_slot_state.current_slot,
                         expected=self.device_nvs_host_index,
                         msg=f'Current device selected slot is not the slot #{self.device_nvs_host_index + 1}.')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check link is established')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 1
        ReceiverTestUtils.switch_to_receiver(self, self.spy_receiver_port_index)
        DevicePairingTestUtils.check_connection_status(
            self, pairing_slot=host_index, expected_connection_status=DeviceConnection.LinkStatus.LINK_ESTABLISHED,
            log_step=True, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a user action')
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0031")
    # end def test_prepairing_after_3_minutes_timeout_reset_on_pairing_failure_pre_paired_never_used

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    def test_prepairing_after_3_minutes_timeout_reset_on_pairing_failure_pre_paired_use_on_current_slot_plug_pre_pair_receiver_no_effect(self):
        """
        Check the 3 minutes timer is resetted when a BLE/BLEPro pairing failure occurs
        if pre paired receiver is already used on current slot
        check plug pre-pair receiver has no effect
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Use Pre Paired Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        self.test_empty_slot_business()
        initial_ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Turn off pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        self._turn_off_pre_paired_rcv()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter pairing mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Device is discoverable')
        # --------------------------------------------------------------------------------------------------------------
        start_time = time.perf_counter()
        # check discoverable 20 seconds
        end_time = start_time + 20
        device_discovery = None
        while time.perf_counter() < end_time:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a pairing sequence with a bad passkey on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        # noinspection PyUnresolvedReferences
        # bluetooth_address is part of the data in device discovery notification part 0
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.failed_pairing_sequence(
            self,
            self.spy_receiver_port_index,
            device_discovery[DeviceDiscovery.PART.CONFIGURATION].data.bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device is always discoverable')
        # --------------------------------------------------------------------------------------------------------------
        start_time = time.perf_counter()
        # check discoverable 20 seconds
        end_time = start_time + 20
        tolerance = float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
        while time.perf_counter() < end_time - tolerance:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn on pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        self._turn_on_pre_paired_rcv()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check link is not established')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 2
        ReceiverTestUtils.switch_to_receiver(self, self.pre_paired_receiver_port_index)
        DevicePairingTestUtils.check_connection_status(
            self, pairing_slot=host_index, expected_connection_status=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED,
            log_step=True, log_check=True)

        # wait 3 minutes timeout
        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT
        tolerance = PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN
        while time.perf_counter() < end_time - tolerance:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
            self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device is not discoverable anymore after timeout')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self,
            float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN),
            max_tries=1,
            raise_err=False
        )
        self.assertNone(device_discovery, 'No discovery notifications should have been received')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.MFG)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check BLE Bond Id Chunk for pairing slot {self.device_nvs_host_index} has not '
                                  f'been created in NVS')
        # --------------------------------------------------------------------------------------------------------------
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)
        self.assertEqual(obtained=len(ble_bond_id_chunks),
                         expected=len(initial_ble_bond_id_chunks),
                         msg=f'No BLE Bond Id chunk for pairing slot {self.device_nvs_host_index} '
                             f'should be created in NVS')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check selected current slot')
        # --------------------------------------------------------------------------------------------------------------
        device_slot_state = self._read_pairing_slot_status()
        self.assertEqual(obtained=device_slot_state.current_slot,
                         expected=self.device_nvs_host_index,
                         msg=f'Current device selected slot is not the slot #{self.device_nvs_host_index + 1}.')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a user action')
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        ReceiverTestUtils.switch_to_receiver(self, self.pre_paired_receiver_port_index)
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check link is established')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.check_connection_status(
            self, pairing_slot=host_index, expected_connection_status=DeviceConnection.LinkStatus.LINK_ESTABLISHED,
            log_step=True, log_check=True)

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0032")
    # end def test_prepairing_after_3_minutes_timeout_reset_on_pairing_failure_pre_paired_use_on_current_slot_plug_pre_pair_receiver_no_effect

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @features('MultipleChannels', HOST.CH3)
    @level('Functionality')
    def test_prepairing_after_3_minutes_timeout_reset_on_pairing_failure_pre_paired_use_on_other_slot_plug_pre_pair_receiver_no_effect(self):
        """
        Check the 3 minutes timer is resetted when a BLE/BLEPro pairing failure occurs
        if pre paired receiver is already used on an other current slot
        check plug pre-pair receiver has no effect
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Use Pre Paired Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        self.test_empty_slot_business()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Turn off pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        self._turn_off_pre_paired_rcv()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair device slot 3 with other receiver')
        # --------------------------------------------------------------------------------------------------------------
        self._pair_to_second_receiver(slot=3)
        initial_ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter pairing mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Device is discoverable')
        # --------------------------------------------------------------------------------------------------------------
        start_time = time.perf_counter()
        # check discoverable 20 seconds
        end_time = start_time + 20
        device_discovery = None
        while time.perf_counter() < end_time:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a pairing sequence with a bad passkey on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        # noinspection PyUnresolvedReferences
        # bluetooth_address is part of the data in device discovery notification part 0
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.failed_pairing_sequence(
            self,
            self.spy_receiver_port_index,
            device_discovery[DeviceDiscovery.PART.CONFIGURATION].data.bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device is always discoverable')
        # --------------------------------------------------------------------------------------------------------------
        start_time = time.perf_counter()
        # check discoverable 20 seconds
        end_time = start_time + 20
        tolerance = float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
        while time.perf_counter() < end_time - tolerance:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn on pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        self._turn_on_pre_paired_rcv()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check link is not established')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 2
        ReceiverTestUtils.switch_to_receiver(self, self.pre_paired_receiver_port_index)
        DevicePairingTestUtils.check_connection_status(
            self, pairing_slot=host_index, expected_connection_status=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED,
            log_step=True, log_check=True)

        # wait 3 minutes timeout
        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT
        tolerance = DiscoveryTestUtils.DEVICE_DISCOVERY_TOLERANCE
        while time.perf_counter() < end_time - tolerance:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        # Do not check the discovery notifications around the scheduled timeout with a tolerance of 12s before and after
        time.sleep(float(tolerance * 2))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
            self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device is not discoverable anymore after timeout')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self,
            float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN),
            max_tries=1,
            raise_err=False
        )
        self.assertNone(device_discovery, 'No discovery notifications should have been received')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.USR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check BLE Bond Id Chunk for pairing slot {self.device_nvs_host_index} has not '
                                  f'been created in NVS')
        # --------------------------------------------------------------------------------------------------------------
        ble_bond_id_chunks = self.memory_manager.get_ble_bond_id_chunks(pairing_slot=self.device_nvs_host_index)
        self.assertEqual(obtained=len(ble_bond_id_chunks),
                         expected=len(initial_ble_bond_id_chunks),
                         msg=f'No BLE Bond Id chunk for pairing slot {self.device_nvs_host_index} '
                             f'should be created in NVS')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check selected current slot')
        # --------------------------------------------------------------------------------------------------------------
        device_slot_state = self._read_pairing_slot_status()
        self.assertEqual(obtained=device_slot_state.current_slot,
                         expected=self.device_nvs_host_index,
                         msg=f'Current device selected slot is not the slot #{self.device_nvs_host_index + 1}.')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a user action')
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        ReceiverTestUtils.switch_to_receiver(self, self.spy_receiver_port_index)
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check link is established')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 1
        DevicePairingTestUtils.check_connection_status(
            self, pairing_slot=host_index, expected_connection_status=DeviceConnection.LinkStatus.LINK_ESTABLISHED,
            log_step=True, log_check=True)

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0033")
    # end def test_prepairing_after_3_minutes_timeout_reset_on_pairing_failure_pre_paired_use_on_other_slot_plug_pre_pair_receiver_no_effect

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    def test_prepairing_recover_after_pairing_failure_pre_paired_never_used_before(self):
        """
        Check the pre-paired receiver recover when a BLE/BLEPro pairing failure occurs
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair device slot 2 with other receiver')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection)
        self._turn_off_pre_paired_rcv()
        self._pair_slot_2_to_second_receiver()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pre Pair Receiver with Device')
        # --------------------------------------------------------------------------------------------------------------
        self._turn_on_pre_paired_rcv()
        ReceiverTestUtils.switch_to_receiver(self, self.pre_paired_receiver_port_index)
        DeviceManagerUtils.set_channel(
            test_case=self, new_channel_id=ChannelIdentifier(
                port_index=ChannelUtils.get_port_index(test_case=self), device_index=self.original_device_index))
        DeviceBaseTestUtils.NvsHelper.change_host(self, self.memory_manager, 0)
        self.receiver_address, self.device_address = self._pre_pair_receiver_with_device()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Switch to user paired slot on device')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.NvsHelper.change_host(self, self.memory_manager, self.device_nvs_host_index,
                                                  ConnectIdChunkData.PairingSrc.USR)
        ReceiverTestUtils.switch_to_receiver(self, self.spy_receiver_port_index)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Turn off the pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        self._turn_off_pre_paired_rcv()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter pairing mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Device is discoverable')
        # --------------------------------------------------------------------------------------------------------------
        start_time = time.perf_counter()
        # check discoverable 20 seconds
        end_time = start_time + 20
        device_discovery = None
        while time.perf_counter() < end_time:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform a pairing sequence with a bad passkey on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        # noinspection PyUnresolvedReferences
        # bluetooth_address is part of the data in device discovery notification part 0
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.failed_pairing_sequence(
            self,
            self.spy_receiver_port_index,
            device_discovery[DeviceDiscovery.PART.CONFIGURATION].data.bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device is always discoverable')
        # --------------------------------------------------------------------------------------------------------------
        start_time = time.perf_counter()
        # check discoverable 20 seconds
        end_time = start_time + 20
        tolerance = float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
        while time.perf_counter() < end_time - tolerance:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start Discovery on spy receiver')
            # ----------------------------------------------------------------------------------------------------------
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Discovery notifications are received while DUT is discoverable')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn on pre paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        self._turn_on_pre_paired_rcv()
        time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, self.device_nvs_host_index, ConnectIdChunkData.PairingSrc.MFG)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check selected current slot')
        # --------------------------------------------------------------------------------------------------------------
        device_slot_state = self._read_pairing_slot_status()
        self.assertEqual(obtained=device_slot_state.current_slot,
                         expected=self.device_nvs_host_index,
                         msg=f'Current device selected slot is not the slot #{self.device_nvs_host_index + 1}.')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Check link is established')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 2
        ReceiverTestUtils.switch_to_receiver(self, self.pre_paired_receiver_port_index)

        # Fetch Device USB Descriptors matching the pre-paired receiver interfaces configuration
        ChannelUtils.get_descriptors(test_case=self)

        DevicePairingTestUtils.check_connection_status(
            self, pairing_slot=host_index, expected_connection_status=DeviceConnection.LinkStatus.LINK_ESTABLISHED,
            log_step=True, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check BLE Bond Id Chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self._check_pre_pairing_ble_bond_id_chunk_in_nvs(host_index=self.device_nvs_host_index,
                                                         chunk_index=-1)

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0035")
    # end def test_prepairing_recover_after_pairing_failure_pre_paired_never_used_before

    @features('SafePrePairedReceiver')
    @features('Feature1816')
    @features('Feature1830powerMode', 3)
    @level('Functionality')
    @services('MultiHost')
    @bugtracker('User_Activity_Advertising_Twice')
    def test_oob_state_pairing_mode_timeout(self):
        """
        In OOB state, with no pre-paired receiver plugged, discoverable mode shall last 3 minutes. Then device
        should go to deep sleep mode. Then a user action shall wake up the device and trigger a new discoverable mode
        which shall last 3 minutes.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set OOB State')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.HIDppHelper.set_oob_state(self, device_index=self.original_device_index)
        self.last_ble_address = None

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reset device')
        # ---------------------------------------------------------------------------
        self.device_debugger.reset(soft_reset=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device is discoverable for 3 minutes')
        # --------------------------------------------------------------------------------------------------------------
        start_time = time.perf_counter()
        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT
        tolerance = DiscoveryTestUtils.DEVICE_DISCOVERY_TOLERANCE
        while time.perf_counter() < end_time - tolerance:
            LogHelper.log_info(self, f'Elapsed time: {time.perf_counter() - start_time}')
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            if self.last_ble_address is None and self.device_debugger is not None:
                # Retrieve the last BLE address in the DUT NVS to correctly filter Device Discovery notifications
                self.device_memory_manager.read_nvs()
                self.last_ble_address = DeviceBaseTestUtils.NvsHelper.get_last_gap_address(
                    test_case=self, memory_manager=self.device_memory_manager)
            # end if

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        # Do not check the discovery notifications around the scheduled timeout with a tolerance of 12s before and after
        time.sleep(float(tolerance * 2))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
            self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device is not discoverable anymore after timeout')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self,
            float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN),
            max_tries=1,
            raise_err=False
        )
        self.assertNone(device_discovery, 'No discovery notifications should have been received')

        if self.power_supply_emulator:
            # If power supply is available, then deep sleep mode can be checked with current consumption.
            # Else, deep sleep mode can't be checked
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Get current value from power supply')
            # ----------------------------------------------------------------------------------------------------------
            current = CommonBaseTestUtils.EmulatorHelper.get_current(self, delay=60.0, samples=150) * 1000
            LogHelper.log_info(self, f'Current = {current}uA')

            expected_value = self.f.PRODUCT.FEATURES.COMMON.POWER_MODES.F_CurrentThresholdDeepSleep
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate if the current is below {expected_value}uA')
            # ----------------------------------------------------------------------------------------------------------
            try:
                self.assertLess(current, expected_value,
                                msg=f'The current value {current}uA shall be below {expected_value}uA')
            except TestException:
                self.log_traceback_as_warning(f'If Jlink IO switch is not connected, then current consumption will '
                                              f'be higher than expected.'
                                              f'The test should not fail in this case.'
                                              f'Remove this try/except if debugger can always be disconnected and '
                                              f'current consumption can be checked in any case.')
            # end try
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'User action')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device is discoverable for 3 minutes')
        # --------------------------------------------------------------------------------------------------------------
        start_time = time.perf_counter()
        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT
        tolerance = DiscoveryTestUtils.DEVICE_DISCOVERY_TOLERANCE
        while time.perf_counter() < end_time - tolerance:
            LogHelper.log_info(self, f'Elapsed time: {time.perf_counter() - start_time}')
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        # Do not check the discovery notifications around the scheduled timeout with a tolerance of 12s before and after
        time.sleep(float(tolerance * 2))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
            self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device is not discoverable anymore after timeout')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self,
            float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN),
            max_tries=1,
            raise_err=False
        )
        self.assertNone(device_discovery, 'No discovery notifications should have been received')

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0036")
    # end def test_oob_state_pairing_mode_timeout

    @features('SafePrePairedReceiver')
    @level('Functionality')
    @services('MultiHost')
    @bugtracker('User_Activity_Advertising_Twice')
    def test_oob_state_pairing_mode_timeout_user_activity(self):
        """
        In OOB state, with no pre-paired receiver plugged, discoverable mode shall last 3 minutes. Then device
        should go to deep sleep mode regardless of the user's activity at the same time.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set OOB State')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.HIDppHelper.set_oob_state(self, device_index=self.original_device_index)
        self.last_ble_address = None

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reset device')
        # ---------------------------------------------------------------------------
        self.device_debugger.reset(soft_reset=False)

        # Perform a key press on the key linked to the standard user action to emulate user activity
        # cf https://jira.logitech.io/browse/NRF52-104
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device is discoverable for 3 minutes')
        # --------------------------------------------------------------------------------------------------------------
        start_time = time.perf_counter()
        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT
        tolerance = DiscoveryTestUtils.DEVICE_DISCOVERY_TOLERANCE
        while time.perf_counter() < end_time - tolerance:
            LogHelper.log_info(self, f'Elapsed time: {time.perf_counter() - start_time}')
            BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
                self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            self.assertNotNone(
                device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

            if self.last_ble_address is None and self.device_debugger is not None:
                # Retrieve the last BLE address in the DUT NVS to correctly filter Device Discovery notifications
                self.device_memory_manager.read_nvs()
                self.last_ble_address = DeviceBaseTestUtils.NvsHelper.get_last_gap_address(
                    test_case=self, memory_manager=self.device_memory_manager)
            # end if

            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)
        # end while

        # Do not check the discovery notifications around the scheduled timeout with a tolerance of 12s before and after
        time.sleep(float(tolerance * 2))
        ChannelUtils.clean_messages(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceDiscovery)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start discovery on spy receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.SpyReceiver.start_discovery(
            self, self.spy_receiver_port_index, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device is not discoverable anymore after timeout')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self,
            float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN),
            max_tries=1,
            raise_err=False
        )
        self.assertNone(device_discovery, 'No discovery notifications should have been received')

        self.testCaseChecked("FNT_SAFE_PRE_PAIR_0037")
    # end def test_oob_state_pairing_mode_timeout_user_activity
# end class SafePrePairedRcvrTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
