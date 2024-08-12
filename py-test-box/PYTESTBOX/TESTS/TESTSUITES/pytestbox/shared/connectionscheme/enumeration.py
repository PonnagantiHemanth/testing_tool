#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.connectionscheme.enumeration
:brief: Validate device enumeration feature
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/04/30
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.configurableproperties import ConfigurableProperties
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatus
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetBLEProDeviceDeviceNameRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetBLEProDeviceDeviceNameResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetBLEProDevicePairingInfoRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetBLEProDevicePairingInfoResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDeviceNameRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDeviceNameResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import NonVolatilePairingInformation
from pylibrary.mcu.nrf52.blenvschunks import ReceiverBleBondInfoIdV0
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pylibrary.tools.nvsparser import MODE
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.configurablepropertiesutils import ConfigurablePropertiesTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.receiver.base.receiverbasetestutils import ReceiverBaseTestUtils
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.enumerationutils import EnumerationTestUtils
from pyusb.libusbdriver import ChannelIdentifier


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SharedEnumerationTestCase(CommonBaseTestCase, ABC):
    """
    Define shared Enumeration TestCases
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.post_requisite_reload_receiver_nvs = False
        self.post_requisite_reload_device_nvs = False
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Device not connected and in non-discoverable mode')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.NvsManager.clean_pairing_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Enable HID++ notifications')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.set_hidpp_reporting(test_case=self, enable=True)

        # Initialize the authentication method parameter
        DevicePairingTestUtils.set_authentication_method(self, self.config_manager)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup receiver initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        if self.receiver_memory_manager is not None:
            self.receiver_memory_manager.read_nvs(backup=True)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup device initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        if self.device_memory_manager is not None:
            self.device_memory_manager.read_nvs(backup=True)
        # end if

        DeviceManagerUtils.set_channel(
            test_case=self,
            new_channel_id=ChannelIdentifier(port_index=ChannelUtils.get_port_index(test_case=self), device_index=1))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x1D4B)')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=WirelessDeviceStatus.FEATURE_ID)
        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.current_channel.receiver_channel)
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            if self.post_requisite_reload_receiver_nvs and self.receiver_memory_manager is not None:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload receiver initial NVS")
                # ------------------------------------------------------------------------------------------------------
                ChannelUtils.close_channel(test_case=self, channel=self.current_channel.receiver_channel)
                self.receiver_memory_manager.load_nvs(backup=True)

                self.post_requisite_reload_receiver_nvs = False
            # end if
        # end with
        with self.manage_post_requisite():
            if self.post_requisite_reload_device_nvs and self.device_memory_manager is not None:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload device initial NVS")
                # ------------------------------------------------------------------------------------------------------
                self.device_memory_manager.load_nvs(backup=True)
                self.post_requisite_reload_device_nvs = False
            # end if
        # end with
        super().tearDown()
    # end def tearDown

    def _setup_rcv_with_device(self):
        """
        Basic button emulator and device setup only for Receiver with Device tests
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Use Easy Switch button to select host on device')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.change_host_by_link_state(
            self, link_state=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED)
    # end def _setup_rcv_with_device

    @features('RcvEnumeration')
    @features('RcvUFYEnumeration')
    @features('RcvWithDevice')
    @level('Functionality')
    def test_equad_device_name(self):
        """
        Validate the read equad device name (B5 4n) API
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Read EQuad device name request and')
        LogHelper.log_check(self, 'Validate EQuad device name response is received')
        # --------------------------------------------------------------------------------------------------------------
        e_quad_device_name_req = GetEQuadDeviceNameRequest(NonVolatilePairingInformation.R0.EQUAD_STEP4_DEVICE_NAME_MIN)

        ChannelUtils.send(
            test_case=self,
            report=e_quad_device_name_req,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=GetEQuadDeviceNameResponse)

        self.testCaseChecked("FUN_RCV-B5_0003")
    # end def test_equad_device_name

    @features('RcvBLEEnumeration')
    @features('RcvWithDevice')
    @level('Interface')
    def test_ble_pro_device_pairing_info_api(self):
        """
        Validate the read BLE Pro device pairing information (B5 5n) API
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Read BLE Pro device pairing information request and')
        LogHelper.log_check(self, 'Validate BLE PRo device pairing information response is received')
        # --------------------------------------------------------------------------------------------------------------
        device_pairing_info_req = GetBLEProDevicePairingInfoRequest(
            NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_PAIRING_INFO_MIN)

        device_pairing_info_resp = ChannelUtils.send(
            test_case=self,
            report=device_pairing_info_req,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=GetBLEProDevicePairingInfoResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check response fields')
        # --------------------------------------------------------------------------------------------------------------
        EnumerationTestUtils.BLEProDevicePairingInfoResponseChecker.check_fields(
            self, device_pairing_info_resp, GetBLEProDevicePairingInfoResponse)

        self.testCaseChecked("INT_ENUM_0004")
    # end def test_ble_pro_device_pairing_info_api

    @features('RcvBLEEnumeration')
    @features('RcvWithDevice')
    @features('BLEDevicePairing')
    @level('Functionality')
    def test_ble_pro_device_pairing_info_all_slots(self):
        """
        Check that all pairing slots can be read
        """
        self._setup_rcv_with_device()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair all slots with only one device')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.pair_all_slots(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over pairing slots')
        # --------------------------------------------------------------------------------------------------------------
        for pairing_slot in range(self.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send Read BLE Pro device pairing information request and')
            LogHelper.log_check(self, 'Validate BLE PRo device pairing information response is received')
            # ----------------------------------------------------------------------------------------------------------
            device_pairing_info_req = GetBLEProDevicePairingInfoRequest(
                NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_PAIRING_INFO_MIN + pairing_slot)

            device_pairing_info_resp = ChannelUtils.send(
                test_case=self,
                report=device_pairing_info_req,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=GetBLEProDevicePairingInfoResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check response fields')
            # ----------------------------------------------------------------------------------------------------------
            checks = EnumerationTestUtils.BLEProDevicePairingInfoResponseChecker.get_default_check_map(self)
            checks["pairing_slot"] = (
                EnumerationTestUtils.BLEProDevicePairingInfoResponseChecker.check_pairing_slot,
                NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_PAIRING_INFO_MIN + pairing_slot)
            EnumerationTestUtils.BLEProDevicePairingInfoResponseChecker.check_fields(
                self, device_pairing_info_resp, GetBLEProDevicePairingInfoResponse, checks)

        self.testCaseChecked("FUN_ENUM_0007")
    # end def test_ble_pro_device_pairing_info_all_slots

    @features('RcvBLEEnumeration')
    @features('RcvWithDevice')
    @level('Interface')
    def test_ble_pro_device_name_api(self):
        """
        Validate the read BLE Pro device name (B5 6n) API
        """
        self._setup_rcv_with_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over BLE Pro Device Name parts')
        # --------------------------------------------------------------------------------------------------------------
        device_name_resps = []
        for part in NonVolatilePairingInformation.BleProDeviceNamePart:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send Read BLE Pro device name request and')
            LogHelper.log_check(self, 'Validate BLE Pro device name response is received')
            # ----------------------------------------------------------------------------------------------------------
            device_name_req = GetBLEProDeviceDeviceNameRequest(
                NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_DEVICE_NAME_MIN,
                part)

            device_name_resp = ChannelUtils.send(
                test_case=self,
                report=device_name_req,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                channel=ChannelUtils.get_receiver_channel(test_case=self),
                response_class_type=GetBLEProDeviceDeviceNameResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check response fields')
            # ----------------------------------------------------------------------------------------------------------
            checks = EnumerationTestUtils.BLEProDeviceNameResponseChecker.get_default_check_map(self)
            checks["device_name_part"] = (
                EnumerationTestUtils.BLEProDeviceNameResponseChecker.check_device_name_part, part)
            EnumerationTestUtils.BLEProDeviceNameResponseChecker.check_fields(
                self, device_name_resp, GetBLEProDeviceDeviceNameResponse, checks)

            device_name_resps.append(device_name_resp)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device Name')
        # --------------------------------------------------------------------------------------------------------------
        EnumerationTestUtils.check_device_name(self, device_name_resps, self.f.SHARED.DEVICES.F_Name[0])

        self.testCaseChecked("INT_ENUM_0005")
    # end def test_ble_pro_device_name_api

    @features('RcvBLEEnumeration')
    @features('RcvWithDevice')
    @features('BLEDevicePairing')
    @level('Functionality')
    def test_ble_pro_device_name_all_slots(self):
        """
        Check device name can be read for all pairing slots
        """
        self._setup_rcv_with_device()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair all slots with only one device')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.pair_all_slots(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over pairing slots')
        # --------------------------------------------------------------------------------------------------------------
        for pairing_slot in range(self.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots):
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Loop over BLE Pro Device Name parts')
            # ----------------------------------------------------------------------------------------------------------
            device_name_resps = []
            for part in NonVolatilePairingInformation.BleProDeviceNamePart:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Send Read BLE Pro device name request and')
                LogHelper.log_check(self, 'Validate BLE PRo device name response is received')
                # ------------------------------------------------------------------------------------------------------
                device_name_req = GetBLEProDeviceDeviceNameRequest(
                    NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_DEVICE_NAME_MIN + pairing_slot,
                    part)

                device_name_resp = ChannelUtils.send(
                    test_case=self,
                    report=device_name_req,
                    response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                    response_class_type=GetBLEProDeviceDeviceNameResponse)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check response fields')
                # ------------------------------------------------------------------------------------------------------
                checks = EnumerationTestUtils.BLEProDeviceNameResponseChecker.get_default_check_map(self)
                checks["pairing_slot"] = (
                    EnumerationTestUtils.BLEProDeviceNameResponseChecker.check_pairing_slot,
                    NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_DEVICE_NAME_MIN + pairing_slot)
                checks["device_name_part"] = (
                    EnumerationTestUtils.BLEProDeviceNameResponseChecker.check_device_name_part, part)
                EnumerationTestUtils.BLEProDeviceNameResponseChecker.check_fields(
                    self, device_name_resp, GetBLEProDeviceDeviceNameResponse, checks)

                device_name_resps.append(device_name_resp)
            # end for

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Name')
            # ----------------------------------------------------------------------------------------------------------
            EnumerationTestUtils.check_device_name(self, device_name_resps, self.f.SHARED.DEVICES.F_Name[0])
        # end for

        self.testCaseChecked("FUN_ENUM_0008")
    # end def test_ble_pro_device_name_all_slots

    @features('RcvBLEEnumeration')
    @features('RcvWithDevice')
    @level('Functionality')
    def test_paired_device_enumeration_business_case(self):
        """
        Check standard Paired Device Enumeration sequence can be executed
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Run paired device enumeration standard sequence')
        # --------------------------------------------------------------------------------------------------------------
        EnumerationTestUtils.paired_device_enumeration_sequence(self)
        self.testCaseChecked("BUS_ENUM_0006")
    # end def test_paired_device_enumeration_business_case

    @features('RcvBLEEnumeration')
    @features('RcvWithDevice')
    @level('Functionality')
    def test_connected_device_enum(self):
        """
        Check standard Connected Device Enumeration sequence can be executed
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Run connected device enumeration standard sequence')
        # --------------------------------------------------------------------------------------------------------------
        EnumerationTestUtils.connected_device_enumeration_sequence(self)
        self.testCaseChecked("FUN_ENUM_0013")
    # end def test_connected_device_enum

    @features('RcvBLEEnumeration')
    @features('RcvWithDevice')
    @features('BLEDevicePairing')
    @level('Functionality')
    def test_ble_pro_device_pairing_info_link_status(self):
        """
        Check that the connection shall be established when paired device is in range and not established when device is
        out of range.
        """
        self._setup_rcv_with_device()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pair all slots')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.pair_all_slots(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check link is established with last pairing slot'
                                  f' {self.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots}')
        # --------------------------------------------------------------------------------------------------------------
        resp = EnumerationTestUtils.get_device_pairing_information(
            self, self.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots)
        EnumerationTestUtils.BLEProDevicePairingInfoResponseChecker.check_link_status(
            self, resp, DeviceConnection.LinkStatus.LINK_ESTABLISHED)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over pairing slots except last one')
        # --------------------------------------------------------------------------------------------------------------
        for pairing_slot in range(1, self.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots):
            resp = EnumerationTestUtils.get_device_pairing_information(self, pairing_slot)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Check link is not established with pairing slot {pairing_slot}')
            # ----------------------------------------------------------------------------------------------------------
            EnumerationTestUtils.BLEProDevicePairingInfoResponseChecker.check_link_status(
                self, resp, DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_ENUM_0014")
    # end def test_ble_pro_device_pairing_info_link_status

    @features('RcvBLEEnumeration')
    @features('RcvWithDevice')
    @features('BLEDevicePairing')
    @level('Functionality')
    def test_extended_model_id_ble_pro_device_pairing_info_and_0003(self):
        """
        Verify that the extended model id field in BLE Pro Device Pairing Info response should reflect the extended
        model id of the device. Note that it shall match the value in Device Information (feature 0x0003)
        """
        self._setup_rcv_with_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pair with device and get device index')
        # --------------------------------------------------------------------------------------------------------------
        ble_addr = DiscoveryTestUtils.discover_device(self)
        device_index = DevicePairingTestUtils.pair_device(self, ble_addr)
        DeviceManagerUtils.set_channel(
            test_case=self,
            new_channel_id=ChannelIdentifier(
                port_index=ChannelUtils.get_port_index(test_case=self), device_index=device_index))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Get Device Info request and get Extended Model Id from feature 0x0003')
        # --------------------------------------------------------------------------------------------------------------
        get_device_info_resp = DeviceInformationTestUtils.HIDppHelper.get_device_info(
            test_case=self, device_index=device_index)

        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.current_channel.receiver_channel)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Read extended model id using B5 5n')
        # --------------------------------------------------------------------------------------------------------------
        pairing_info = EnumerationTestUtils.get_device_pairing_information(self, device_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Extended model id from 0003 and B5 5n should match')
        # --------------------------------------------------------------------------------------------------------------
        EnumerationTestUtils.BLEProDevicePairingInfoResponseChecker.check_extended_model_id(
            self, pairing_info, int(Numeral(get_device_info_resp.extended_model_id)))

        self.testCaseChecked("FUN_ENUM_0015")
    # end def test_extended_model_id_ble_pro_device_pairing_info_and_0003

    @features('RcvBLEEnumeration')
    @features('RcvWithDevice')
    @features('BLEDevicePairing')
    @features("Feature1807")
    @level('Functionality')
    def test_extended_model_id_ble_pro_device_pairing_info_and_1807(self):
        """
        Verify that the extended model id in BLE Pro Device Pairing Info response should reflect the extended model
        id of the device. Note that it shall match the value in Configurable Properties (feature 0x1807)
        """
        try:
            self._setup_rcv_with_device()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Pair with device and get device index')
            # ----------------------------------------------------------------------------------------------------------
            ble_addr = DiscoveryTestUtils.discover_device(self)
            device_index = DevicePairingTestUtils.pair_device(self, ble_addr)

            device_hid_dispatcher = self.current_channel.hid_dispatcher

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'Test Loop over extended model id significant values')
            # ----------------------------------------------------------------------------------------------------------
            for extended_model_id in compute_sup_values(0x00, is_equal=True):
                DeviceManagerUtils.set_channel(
                    test_case=self,
                    new_channel_id=ChannelIdentifier(
                        port_index=ChannelUtils.get_port_index(test_case=self), device_index=device_index))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Enable Manufacturing Features')
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True, device_index=device_index)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Set extended model id (using 1807)')
                # ------------------------------------------------------------------------------------------------------
                property_id = ConfigurableProperties.PropertyId.EXTENDED_MODEL_ID
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Select property {repr(property_id)}")
                # ------------------------------------------------------------------------------------------------------
                ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Write property {repr(property_id)}")
                # ------------------------------------------------------------------------------------------------------
                self.post_requisite_reload_device_nvs = True
                ConfigurablePropertiesTestUtils.HIDppHelper.write_data(self, HexList(extended_model_id))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Reset the device')
                # ------------------------------------------------------------------------------------------------------
                self.device_memory_manager.reset()

                DeviceManagerUtils.set_channel(test_case=self, new_channel=self.current_channel.receiver_channel)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Pair with device and get device index')
                # ------------------------------------------------------------------------------------------------------
                DevicePairingTestUtils.unpair_slot(self, device_index)
                ble_addr = DiscoveryTestUtils.discover_device(self)
                device_index = DevicePairingTestUtils.pair_device(
                    self, ble_addr, hid_dispatcher_to_dump=device_hid_dispatcher)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Read extended model id (using B5 5n)')
                # ------------------------------------------------------------------------------------------------------
                pairing_info_resp = EnumerationTestUtils.get_device_pairing_information(self, pairing_slot=device_index)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Extended model id from 1807 and B5 5n should match')
                # ------------------------------------------------------------------------------------------------------
                EnumerationTestUtils.BLEProDevicePairingInfoResponseChecker.check_extended_model_id(
                    self, pairing_info_resp, extended_model_id)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'End Test Loop')
            # ----------------------------------------------------------------------------------------------------------
        finally:
            if self.device_memory_manager is not None:
                self.device_memory_manager.read_nvs()
                self.device_memory_manager.invalidate_chunks(["NVS_EXTENDED_MODEL_ID", ])
                self.device_memory_manager.load_nvs()
            # end if
        # end try

        self.testCaseChecked("FUN_ENUM_0016")
    # end def test_extended_model_id_ble_pro_device_pairing_info_and_1807

    @features('RcvBLEDeviceEnumeration')
    @level('ErrorHandling')
    @services('Debugger')
    def test_re_enumeration_dfu_check_chunk_missing(self):
        """
        Validate the receiver forces device services re-enumeration when the DFU check FW info chunk is missing

        RQ_C-RCV-DFU-001#1: When a DFU of the receiver is done, it shall force service re-enumeration
        on each paired device at the first next connection
        """
        self.pairing_slot = 0
        self.chunk_id = f'NVS_BLE_BOND_INFO_ID_{self.pairing_slot}'

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Invalidate all DFU check FW info chunks in NVS")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.close_channel(test_case=self)
        self.receiver_memory_manager.read_nvs()
        self.bond_info_chunk_history = self.receiver_memory_manager.nvs_parser.get_chunk_history(
            chunk_id=self.chunk_id, mode=MODE.RECEIVER)
        self.receiver_memory_manager.invalidate_chunks(["NVS_DFU_CHECK_ID", ])
        self.post_requisite_reload_receiver_nvs = True
        self.receiver_memory_manager.load_nvs()

        self._test_dfu_check_processing()

        self.testCaseChecked("ERR_ENUM_0027")
    # end def test_re_enumeration_dfu_check_chunk_missing

    def _test_dfu_check_processing(self):
        """
        Common part of the test verifying the processing of the DFU Check FW Info chunk presence and state in NVS.
        """
        dfu_check_bond_info_chunk_history = []
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reset the receiver to force the DFU check FW info processing')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.close_channel(test_case=self)
        ReceiverBaseTestUtils.ResetHelper.hardware_reset(self)
        CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(test_case=self)
        ChannelUtils.open_channel(test_case=self)
        ChannelUtils.set_idle(test_case=self)
        ChannelUtils.set_hidpp_reporting(test_case=self, enable=True)

        ble_pro_service_version = to_int(self.bond_info_chunk_history[-1].ble_pro_service_version) if len(
            self.bond_info_chunk_history) > 0 else to_int(
            self.config_manager.get_feature(ConfigurationManager.ID.BLE_PRO_SRV_VERSION)[0])

        if self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER and ble_pro_service_version >= 2:
            # Let time to the firmware to complete its startup
            sleep(.2)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Dump the NVS and verify a new chunk has been re-created')
            # ----------------------------------------------------------------------------------------------------------
            self.receiver_memory_manager.read_nvs()
            dfu_check_bond_info_chunk_history = self.receiver_memory_manager.nvs_parser.get_chunk_history(
                chunk_id=self.chunk_id, mode=MODE.RECEIVER)
            self.assertEqual(expected=len(self.bond_info_chunk_history) + 1,
                             obtained=len(dfu_check_bond_info_chunk_history),
                             msg='The number of BLE Bond Info chunks shall be incremented by 1')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Verify the enumeration pending flag is set in this instance')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=ReceiverBleBondInfoIdV0.ENUMERATION.ENABLED,
                             obtained=to_int(dfu_check_bond_info_chunk_history[-1].enumeration_pending),
                             msg='The enumeration pending flag differs from the expected one')
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Perform User Action to force the device reconnection')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        device_pairing_slot = 1 + self.pairing_slot
        DeviceManagerUtils.set_channel(
            test_case=self,
            new_channel_id=ChannelIdentifier(
                port_index=ChannelUtils.get_port_index(test_case=self), device_index=device_pairing_slot))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify a 0x41 notification with link established is returned after the '
                                  'completion of the device re-enumeration')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.wait_through_receiver_channel_link_status(
            test_case=self, channel=self.current_channel, link_status=DeviceConnection.LinkStatus.LINK_ESTABLISHED)

        if to_int(self.bond_info_chunk_history[-1].ble_pro_service_version) >= 2:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Verify a 0x1D4B notification is returned when the sequence is completed')
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.get_only(
                test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=WirelessDeviceStatusBroadcastEvent, check_first_message=False)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Test the connection by sending the enable Manufacturing Features')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True, device_index=device_pairing_slot)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Dump the NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.receiver_memory_manager.read_nvs()
        reconnection_bond_info_chunk_history = self.receiver_memory_manager.nvs_parser.get_chunk_history(
            chunk_id=self.chunk_id, mode=MODE.RECEIVER)

        if to_int(self.bond_info_chunk_history[-1].ble_pro_service_version) >= 2:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Verify device re-enumeration did occur only if the device exposes a BLE Pro '
                                      'service version greater or equal to 2')
            # ----------------------------------------------------------------------------------------------------------
            self.assertTrue(
                expr=len(reconnection_bond_info_chunk_history) >= len(dfu_check_bond_info_chunk_history) + 2,
                msg=f'The number of DFU chunk in history shall be increased by 2 during re-enumeration')
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify the enumeration pending flag is reset in the last instance')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=ReceiverBleBondInfoIdV0.ENUMERATION.DISABLED,
                         obtained=to_int(reconnection_bond_info_chunk_history[-1].enumeration_pending),
                         msg='The enumeration pending flag differs from the expected one')

        ChannelUtils.clean_messages(
            test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, class_type=WirelessDeviceStatusBroadcastEvent)
    # end def _test_dfu_check_processing

    @features('RcvBLEDeviceEnumeration')
    @level('Functionality')
    @services('Debugger')
    def test_re_enumeration_service_change(self):
        """
        Validate the presence of 0x41 and 0x1D4B notifications when the device requires a service change (
        through a missing System attribute user service chunk)

        RQ_C-RCV-DFU-001#1: When a DFU of the receiver is done, it shall force service re-enumeration
        on each paired device at the first next connection
        """
        self.post_requisite_reload_receiver_nvs = True

        pairing_slot = 0
        device_pairing_slot = 1 + pairing_slot
        DeviceManagerUtils.set_channel(
            test_case=self,
            new_channel_id=ChannelIdentifier(
                port_index=ChannelUtils.get_port_index(test_case=self), device_index=device_pairing_slot))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x1D4B)')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=WirelessDeviceStatus.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Delete all instances of system attribute user services chunks and reload the '
                                 'device NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.device_memory_manager.read_nvs()
        sys_attr_user_services_chunk_id = f'NVS_BLE_SYS_ATTR_USR_SRVCS_ID_{pairing_slot}'
        self.device_memory_manager.nvs_parser.delete_all_chunks(chunk_id=sys_attr_user_services_chunk_id)
        self.device_debugger.reload_file(nvs_hex_file=self.device_memory_manager.nvs_parser.to_hex_file())

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify a first 0x41 notification with link established is returned before the '
                                  'receiver received the service change indictation from the device')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.wait_through_receiver_channel_link_status(
            test_case=self, channel=self.current_channel, link_status=DeviceConnection.LinkStatus.LINK_ESTABLISHED)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify a second 0x41 notification with link NOT established is returned when the '
                                  'receiver starts the enumeration sequence')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.wait_through_receiver_channel_link_status(
            test_case=self, channel=self.current_channel, link_status=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify a third 0x41 notification with link established is returned after the '
                                  'completion of the device re-enumeration')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.wait_through_receiver_channel_link_status(
            test_case=self, channel=self.current_channel, link_status=DeviceConnection.LinkStatus.LINK_ESTABLISHED)

        if to_int(self.config_manager.get_feature(ConfigurationManager.ID.BLE_PRO_SRV_VERSION)[0]) >= 2:
            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Verify a 0x1D4B notification is returned when the sequence is completed')
            # --------------------------------------------------------------------------------------------------------------
            ChannelUtils.get_only(
                test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, 
                class_type=WirelessDeviceStatusBroadcastEvent, check_first_message=False)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Test the connection by sending the enable Manufacturing Features')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True, device_index=device_pairing_slot)

        self.testCaseChecked("FUN_ENUM_0029")
    # end def test_re_enumeration_service_change

# end class SharedEnumerationTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
