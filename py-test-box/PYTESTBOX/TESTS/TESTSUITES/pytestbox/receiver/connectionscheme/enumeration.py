#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.connectionscheme.enumeration
:brief: Validate paired device enumeration feature
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2020/02/19
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from copy import deepcopy
from random import randint
from time import sleep
from unittest import skip

from pychannel.channelinterfaceclasses import ChannelException
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetBLEProDeviceDeviceNameRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetBLEProDevicePairingInfoRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDeviceNameRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDeviceNameResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetFwVersionRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetFwVersionResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetUsbSerialNumberRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetUsbSerialNumberResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import NonVolatilePairingInformation
from pyhid.hidpp.hidpp1.registers.receiverfwinformation import GetReceiverFwInfoRequest
from pyhid.hidpp.hidpp1.registers.receiverfwinformation import GetReceiverFwInfoResponse
from pyhid.hidpp.hidpp1.registers.reset import SetResetRequest
from pyhid.hidpp.hidpp1.registers.uniqueidentifier import GetUniqueIdentifierRequest
from pyhid.hidpp.hidpp1.registers.uniqueidentifier import GetUniqueIdentifierResponse
from pylibrary.mcu.nrf52.blenvschunks import ReceiverBleBondInfoIdV0
from pylibrary.mcu.nrf52.blenvschunks import ReceiverBleBondInfoIdV1
from pylibrary.mcu.securitychunks import DfuCheckFwInfoChunk
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pylibrary.tools.nvsparser import MODE
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.basetest import ReceiverBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.shared.base.enumerationutils import EnumerationTestUtils
from pytestbox.shared.connectionscheme.enumeration import SharedEnumerationTestCase
from pytransport.transportcontext import TransportContextException
from pyusb.libusbdriver import ChannelIdentifier


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class EnumerationTestCase(SharedEnumerationTestCase, ReceiverBaseTestCase):
    """
    Validate Enumeration TestCases in Receiver mode
    """

    @features('RcvReadSerialNumber')
    @level('Interface')
    def test_read_serial_number(self):
        """
        Validate read receiver serial number (B5 01)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Read receiver serial number')
        # --------------------------------------------------------------------------------------------------------------
        read_serial_number = GetUsbSerialNumberRequest()
        read_serial_number_response = ChannelUtils.send(
            test_case=self,
            report=read_serial_number,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=GetUsbSerialNumberResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate receiver serial number')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=HexList(self.f.PRODUCT.RECEIVER.ENUMERATION.F_SerialNumber),
                         obtained=HexList(read_serial_number_response.serial_number),
                         msg="Serial number should be as defined in configuration")

        self.testCaseChecked("INT_ENUM_0001")
    # end def test_read_serial_number

    @features('RcvEnumeration')
    @level('Interface')
    def test_read_fw_version(self):
        """
        Validate read receiver fw version (B5 02)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Read receiver fw version')
        # --------------------------------------------------------------------------------------------------------------
        read_fw_version = GetFwVersionRequest()
        read_fw_version_response = ChannelUtils.send(
            test_case=self,
            report=read_fw_version,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=GetFwVersionResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate receiver fw version')
        # --------------------------------------------------------------------------------------------------------------
        EnumerationTestUtils.FwVersionResponseChecker.check_fields(self, read_fw_version_response, GetFwVersionResponse)

        self.testCaseChecked("INT_ENUM_0002")
    # end def test_read_fw_version
    
    @features('RcvBLEEnumeration')
    @level('ErrorHandling')
    def test_ble_pro_device_pairing_info_no_device(self):
        """
        Reading an unused Pairing slot should raise an error with error code ERR_INVALID_PARAM_VALUE
        """

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over all pairing slots')
        # --------------------------------------------------------------------------------------------------------------
        for pairing_slot in range(1, self.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send Read BLE Pro device pairing information request')
            LogHelper.log_check(self, 'Validate Error message is received with error code ERR_UNKNOWN_DEVICE')
            # ----------------------------------------------------------------------------------------------------------
            device_pairing_info_req = GetBLEProDevicePairingInfoRequest(
                NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_PAIRING_INFO_MIN + pairing_slot)

            error_response = ChannelUtils.send(
                test_case=self,
                report=device_pairing_info_req,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                response_class_type=Hidpp1ErrorCodes)

            self.assertEqual(obtained=int(Numeral(error_response.errorCode)),
                             expected=Hidpp1ErrorCodes.ERR_UNKNOWN_DEVICE,
                             msg="The error_code parameter should be as expected")
        # end for

        self.testCaseChecked("ERR_ENUM_0009")
    # end def test_ble_pro_device_pairing_info_no_device

    @features('RcvBLEEnumeration')
    @level('ErrorHandling')
    def test_ble_pro_device_name_no_device(self):
        """
        Reading an unused Pairing slot should raise an error with error code ERR_INVALID_PARAM_VALUE
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over all pairing slots')
        # --------------------------------------------------------------------------------------------------------------
        for pairing_slot in range(1, self.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send Read BLE Pro device name request')
            LogHelper.log_check(self, 'Validate Error message is received with error code ERR_UNKNOWN_DEVICE')
            # ----------------------------------------------------------------------------------------------------------
            device_pairing_info_req = GetBLEProDeviceDeviceNameRequest(
                NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_DEVICE_NAME_MIN + pairing_slot)

            error_response = ChannelUtils.send(
                test_case=self,
                report=device_pairing_info_req,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                response_class_type=Hidpp1ErrorCodes)

            self.assertEqual(obtained=int(Numeral(error_response.errorCode)),
                             expected=Hidpp1ErrorCodes.ERR_UNKNOWN_DEVICE,
                             msg="The error_code parameter should be as expected")
        # end for

        self.testCaseChecked("ERR_ENUM_0010")
    # end def test_ble_pro_device_name_no_device

    @features('RcvEnumeration')
    @level('Functionality')
    @skip('The Mezzy receiver is stuck when processing the command!')
    def test_reset_request_transceiver(self):
        """
        Check reset command is supported when sent to Transceiver
        """
        try:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send Reset request')
            # ----------------------------------------------------------------------------------------------------------
            reset_req = SetResetRequest(Hidpp1Data.DeviceIndex.TRANSCEIVER)
            try:
                ChannelUtils.send_only(test_case=self, report=reset_req)
            except TransportContextException as e:
                if e.get_cause() in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                                     TransportContextException.Cause.CONTEXT_ERROR_IO,
                                     TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
                    pass
                else:
                    raise
                # end if
            # end try
            sleep(1.0)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate no error message is received')
            # ----------------------------------------------------------------------------------------------------------
            self.assertListEqual(
                ChannelUtils.clean_messages(
                    test_case=self, queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                    class_type=Hidpp1ErrorCodes),
                [],
                "No error should be raised when sending reset command")
        finally:
            self.reset()
        # end try
        self.testCaseChecked("FUN_ENUM_0011")
    # end def test_reset_request_transceiver

    @features('RcvBLEEnumeration')
    @level('Functionality')
    def test_receiver_fw_info(self):
        """
        Check receiver FW information
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over entities')
        # --------------------------------------------------------------------------------------------------------------
        for entity_idx in range(len(self.config_manager.get_feature(ConfigurationManager.ID.FW_TYPE))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Read receiver fw information')
            # ----------------------------------------------------------------------------------------------------------
            receiver_fw_info_req = GetReceiverFwInfoRequest(entity_idx)

            receiver_fw_info_resp = ChannelUtils.send(
                test_case=self,
                report=receiver_fw_info_req,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=GetReceiverFwInfoResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate receiver fw information')
            # ----------------------------------------------------------------------------------------------------------
            EnumerationTestUtils.ReceiverFwInfoResponseChecker.check_fields(
                self, receiver_fw_info_resp, GetReceiverFwInfoResponse,
                EnumerationTestUtils.ReceiverFwInfoResponseChecker.get_check_map_for_entity(self, entity_idx))
        # end for
        self.testCaseChecked("FUN_ENUM_0012")
    # end def test_receiver_fw_info

    @features('RcvBLEEnumeration')
    @level('Functionality')
    def test_get_unique_identifier(self):
        """
        Validate Get Unique Identifier (0xFB)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get Receiver Unique Identifier')
        # --------------------------------------------------------------------------------------------------------------
        get_unique_identifier = GetUniqueIdentifierRequest()
        get_unique_identifier_response = ChannelUtils.send(
            test_case=self,
            report=get_unique_identifier,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=GetUniqueIdentifierResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate receiver unique identifier')
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(expr=HexList(get_unique_identifier_response.unique_identifier) in [HexList.fromString(x) for x
                        in self.f.RECEIVER.ENUMERATION.F_UniqueIdentifierList],
                        msg="Unique Identifier should be as defined in configuration")

        self.testCaseChecked("FUN_ENUM_0017")
    # end def test_get_unique_identifier

    @features('RcvBLEEnumeration')
    @level('Robustness')
    def test_ble_pro_device_pairing_info_index_out_of_range(self):
        """
        Reading a pairing slot out of range should raise an error with error code ERR_INVALID_PARAM_VALUE
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over pairing slot significant values')
        # --------------------------------------------------------------------------------------------------------------
        for pairing_slot in [0x50] + compute_sup_values(NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_PAIRING_INFO_MIN
                                                        + self.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send BLE Pro Device Pairing Info request')
            # ----------------------------------------------------------------------------------------------------------
            device_pairing_info_req = GetBLEProDevicePairingInfoRequest(pairing_slot)

            error_response = ChannelUtils.send(
                test_case=self,
                report=device_pairing_info_req,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                response_class_type=Hidpp1ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check error message is received with error code ERR_INVALID_PARAM_VALUE')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(obtained=int(Numeral(error_response.errorCode)),
                             expected=Hidpp1ErrorCodes.ERR_INVALID_PARAM_VALUE,
                             msg="The error_code parameter should be as expected")
        # end for

        self.testCaseChecked("ROB_ENUM_0001")
    # end def test_ble_pro_device_pairing_info_index_out_of_range

    @features('RcvBLEEnumeration')
    @level('Robustness')
    def test_ble_pro_device_name_index_out_of_range(self):
        """
        Reading a pairing slot out of range should raise an error with error code ERR_INVALID_PARAM_VALUE
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over pairing slot significant values')
        # --------------------------------------------------------------------------------------------------------------
        test_values = [NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_DEVICE_NAME_MIN - 1]
        test_values += compute_sup_values(NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_DEVICE_NAME_MIN +
                                          self.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots)
        for pairing_slot in test_values:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send BLE Pro Device Name request')
            # ----------------------------------------------------------------------------------------------------------
            device_name_req = GetBLEProDeviceDeviceNameRequest(pairing_slot)

            error_response = ChannelUtils.send(
                test_case=self,
                report=device_name_req,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                response_class_type=Hidpp1ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check error message is received with error code ERR_INVALID_PARAM_VALUE')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(obtained=int(Numeral(error_response.errorCode)),
                             expected=Hidpp1ErrorCodes.ERR_INVALID_PARAM_VALUE,
                             msg="The error_code parameter should be as expected")
        # end for

        self.testCaseChecked("ROB_ENUM_0002")
    # end def test_ble_pro_device_name_index_out_of_range

    @features('NoRcvUFYEnumeration')
    @level('Robustness')
    def test_no_equad_device_name(self):
        """
        Validate read eQuad device name (B5 4n) is not supported
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Read EQuad device name request')
        # --------------------------------------------------------------------------------------------------------------
        e_quad_device_name_req = GetEQuadDeviceNameRequest(NonVolatilePairingInformation.R0.EQUAD_STEP4_DEVICE_NAME_MIN)

        ChannelUtils.send_only(test_case=self, report=e_quad_device_name_req)
        sleep(0.5)
        resp = ChannelUtils.clean_messages(
            test_case=self, queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            class_type=GetEQuadDeviceNameResponse)
        err_resp = ChannelUtils.clean_messages(
            test_case=self, queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
            class_type=Hidpp1ErrorCodes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check no valid response is received')
        # --------------------------------------------------------------------------------------------------------------
        self.assertListEqual(resp, [], f'Read eQUAD Device Name request should not be accepted')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check error message returned by the device')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreater(len(err_resp), 0, f'Read eQUAD Device Name request should raise an error')
        self.assertTupleEqual(
            (Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
             Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_PAIRING_INFORMATION),
            (int(Numeral(err_resp[0].command_sub_id)), int(Numeral(err_resp[0].address))),
            f'eQUAD Device Name request should raise an error')

        self.assertEqual(Hidpp1ErrorCodes.ERR_INVALID_PARAM_VALUE, int(err_resp[0].error_code),
                         f'eQUAD Device Name request should raise an ERR_INVALID_PARAM_VALUE error')

        self.testCaseChecked("ROB_ENUM_0003")
    # end def test_no_equad_device_name

    @features('RcvEnumeration')
    @features('NoRcvReadSerialNumber')
    @level('Robustness')
    def test_read_serial_number_not_supported(self):
        """
        Validate read receiver serial number (B5 01) is not supported by the DUT
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Read receiver serial number')
        # --------------------------------------------------------------------------------------------------------------
        read_serial_number = GetUsbSerialNumberRequest()
        read_serial_number_response = ChannelUtils.send(
                test_case=self,
                report=read_serial_number,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                response_class_type=Hidpp1ErrorCodes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check HID++ 1.0 ERR_INVALID_PARAM_VALUE (11) Error Code returned by the device')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=Hidpp1ErrorCodes.ERR_INVALID_PARAM_VALUE,
                         obtained=int(Numeral(read_serial_number_response.errorCode)),
                         msg='The errorCode parameter differs from the one expected')

        self.testCaseChecked("ROB_ENUM_0004")
    # end def test_read_serial_number_not_supported

    @features('RcvBLEDeviceEnumeration')
    @level("ErrorHandling")
    @services('Debugger')
    def test_bond_info_chunk_corrupted(self):
        """
        Goal: Check that the receiver re-enumerate the device to retrieve the bonding information if the existing
        chunk is corrupted (i.e. bad CRC)
        Verify the corrupted chunk is deleted (i.e. invalidated)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Invalidate all the Bond Info chunk in NVS")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.close_channel(test_case=self)
        self.receiver_memory_manager.read_nvs()
        pairing_slot = 0
        chunk_id = f'NVS_BLE_BOND_INFO_ID_{pairing_slot}'
        last_chunk_data = self.receiver_memory_manager.nvs_parser.get_chunk(chunk_id=chunk_id).chunk_data
        self.receiver_memory_manager.invalidate_chunks([chunk_id, ])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Add a clone of the last bond info chunk but with a wrong CRC')
        # --------------------------------------------------------------------------------------------------------------
        bond_id = ReceiverBleBondInfoIdV1.fromHexList(HexList(last_chunk_data))
        self.receiver_memory_manager.nvs_parser.add_new_chunk(chunk_id=chunk_id, data=HexList(bond_id))
        chunk = self.receiver_memory_manager.nvs_parser.get_chunk(chunk_id=chunk_id)
        chunk.chunk_crc += 1
        corrupted_chunk_crc = int(chunk.chunk_crc)
        self.post_requisite_reload_receiver_nvs = True
        self.receiver_memory_manager.load_nvs()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reset the receiver to trigger the bond info verification')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, recover_time_needed=True, verify_connection_reset=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Perform User Action to force the device reconnection')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        device_pairing_slot = 1 + pairing_slot
        DeviceManagerUtils.set_channel(
            test_case=self,
            new_channel_id=ChannelIdentifier(
                port_index=ChannelUtils.get_port_index(test_case=self), device_index=device_pairing_slot))
        ChannelUtils.wait_through_receiver_channel_link_status(
            test_case=self, channel=self.current_channel, link_status=DeviceConnection.LinkStatus.LINK_ESTABLISHED)

        if to_int(self.config_manager.get_feature(ConfigurationManager.ID.BLE_PRO_SRV_VERSION)[0]) >= 2:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Verify a 0x1D4B notification is returned when the sequence is completed')
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.get_only(
                test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, class_type=WirelessDeviceStatusBroadcastEvent,
                check_first_message=False)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Test the connection by sending the enable Manufacturing Features')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True, device_index=device_pairing_slot)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Dump the NVS and verify 2 new chunks has been created')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        new_bond_info_chunk_history = self.memory_manager.nvs_parser.get_chunk_history(
            chunk_id=chunk_id, mode=MODE.RECEIVER)
        self.assertEqual(expected=2,
                         obtained=len(new_bond_info_chunk_history),
                         msg='2 new chunks shall been created')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the corrupted chunk has been deleted')
        # --------------------------------------------------------------------------------------------------------------
        self.assertNotEqual(unexpected=corrupted_chunk_crc,
                            obtained=new_bond_info_chunk_history[0].ref.chunk_crc,
                            msg='The new chunk CRC shall not match the corrupted value')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify the enumeration pending flag is set in this first instance')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=ReceiverBleBondInfoIdV0.ENUMERATION.ENABLED,
                         obtained=to_int(new_bond_info_chunk_history[0].enumeration_pending),
                         msg='The enumeration pending flag differs from the expected one')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify the enumeration pending flag is reset in the last instance')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=ReceiverBleBondInfoIdV0.ENUMERATION.DISABLED,
                         obtained=to_int(new_bond_info_chunk_history[-1].enumeration_pending),
                         msg='The enumeration pending flag differs from the expected one')

        self.testCaseChecked("ERR_ENUM_0022")
    # end def test_bond_info_chunk_corrupted

    @features('RcvBLEDeviceEnumeration')
    @level('Functionality')
    @services('Debugger')
    def test_no_enumeration_when_bond_info_version_changed(self):
        """
        Validate the receiver do not force device services re-enumeration after a change in Bond info chunk format.
        """
        self.post_requisite_reload_receiver_nvs = True

        pairing_slot = 0
        ChannelUtils.close_channel(test_case=self)
        self.receiver_memory_manager.read_nvs()
        nvs_parser_copy = deepcopy(self.receiver_memory_manager.nvs_parser)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Dump the NVS and keep the initial bond info chunk history')
        # --------------------------------------------------------------------------------------------------------------
        bond_info_chunk_id = f'NVS_BLE_BOND_INFO_ID_{pairing_slot}'
        bond_info_chunk_history = nvs_parser_copy.get_chunk_history(chunk_id=bond_info_chunk_id, mode=MODE.RECEIVER)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Save the initial system attribute user services chunk history')
        # --------------------------------------------------------------------------------------------------------------
        self.device_memory_manager.read_nvs()
        sys_attr_user_services_chunk_id = f'NVS_BLE_SYS_ATTR_USR_SRVCS_ID_{pairing_slot}'
        sys_attr_user_services_chunk_history = self.device_memory_manager.nvs_parser.get_chunk_history(
            chunk_id=sys_attr_user_services_chunk_id, mode=MODE.DEVICE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Replace the last bond info chunk version 1 by an equivalent matching version 0')
        # --------------------------------------------------------------------------------------------------------------
        nvs_parser_copy.add_new_chunk(
            chunk_id=f'NVS_BLE_BOND_INFO_ID_V0_{pairing_slot}',
            data=bond_info_chunk_history[-1].convert_to_v0())

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Delete all instances of bond info chunk version 1 and reload the NVS')
        # --------------------------------------------------------------------------------------------------------------
        nvs_parser_copy.delete_all_chunks(chunk_id=bond_info_chunk_id)
        self.receiver_debugger.reload_file(nvs_hex_file=nvs_parser_copy.to_hex_file(), no_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reset the receiver to force the services structure verification')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, recover_time_needed=True, verify_connection_reset=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Dump the NVS and verify 1 chunk version 1 has been re-created')
        # --------------------------------------------------------------------------------------------------------------
        self.receiver_memory_manager.read_nvs()
        new_bond_info_chunk_history = self.receiver_memory_manager.nvs_parser.get_chunk_history(
            chunk_id=bond_info_chunk_id, mode=MODE.RECEIVER)
        self.assertEqual(expected=1,
                         obtained=len(new_bond_info_chunk_history),
                         msg='The number of BLE Bond Info v1 chunk in history is not the expected one')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify the bond info chunk version 0 has been deleted')
        # --------------------------------------------------------------------------------------------------------------
        new_bond_info_chunk_v0_history = self.receiver_memory_manager.nvs_parser.get_chunk_history(
            chunk_id=f'NVS_BLE_BOND_INFO_ID_V0_{pairing_slot}', mode=MODE.RECEIVER)
        self.assertEqual(expected=0,
                         obtained=len(new_bond_info_chunk_v0_history),
                         msg='The number of BLE Bond Info v0 chunk in history is not the expected one')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify the enumeration pending flag is NOT set in this instance')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=ReceiverBleBondInfoIdV0.ENUMERATION.DISABLED,
                         obtained=to_int(new_bond_info_chunk_history[-1].enumeration_pending),
                         msg='The enumeration pending flag differs from the expected one')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Perform User Action to force the device reconnection')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        device_pairing_slot = 1 + pairing_slot
        DeviceManagerUtils.set_channel(
            test_case=self,
            new_channel_id=ChannelIdentifier(
                port_index=ChannelUtils.get_port_index(test_case=self), device_index=device_pairing_slot))
        ChannelUtils.wait_through_receiver_channel_link_status(
            test_case=self, channel=self.current_channel, link_status=DeviceConnection.LinkStatus.LINK_ESTABLISHED)

        if to_int(new_bond_info_chunk_history[-1].ble_pro_service_version) >= 2:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Verify a 0x1D4B notification is returned when the sequence is completed')
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.get_only(
                test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, class_type=WirelessDeviceStatusBroadcastEvent,
                check_first_message=False)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Test the connection by sending the enable Manufacturing Features')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True, device_index=device_pairing_slot)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Dump the NVS and verify other chunks version 1 are present')
        # --------------------------------------------------------------------------------------------------------------
        self.receiver_memory_manager.read_nvs()
        final_bond_info_chunk_history = self.receiver_memory_manager.nvs_parser.get_chunk_history(
            chunk_id=bond_info_chunk_id, mode=MODE.RECEIVER)
        self.assertTrue(expr=len(final_bond_info_chunk_history) == 1,
                        msg=f'The number of DFU chunk in history {len(final_bond_info_chunk_history)} shall be 1')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify bond info chunks version 0 are absent')
        # --------------------------------------------------------------------------------------------------------------
        new_bond_info_chunk_v0_history = self.receiver_memory_manager.nvs_parser.get_chunk_history(
            chunk_id=f'NVS_BLE_BOND_INFO_ID_V0_{pairing_slot}', mode=MODE.RECEIVER)
        self.assertEqual(expected=0,
                         obtained=len(new_bond_info_chunk_v0_history),
                         msg='The number of BLE Bond Info v0 chunk in history is not the expected one')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify the enumeration pending flag is reset in the last instance')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=ReceiverBleBondInfoIdV0.ENUMERATION.DISABLED,
                         obtained=to_int(final_bond_info_chunk_history[-1].enumeration_pending),
                         msg='The enumeration pending flag differs from the expected one')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Dump the device NVS and save the final system attribute user services chunk history')
        # --------------------------------------------------------------------------------------------------------------
        self.device_memory_manager.read_nvs()
        new_sys_attr_user_services_chunk_history = self.device_memory_manager.nvs_parser.get_chunk_history(
            chunk_id=sys_attr_user_services_chunk_id, mode=MODE.DEVICE)
        self.assertEqual(expected=new_sys_attr_user_services_chunk_history,
                         obtained=sys_attr_user_services_chunk_history,
                         msg='The system attribute user services chunks shall be unchanged')

        self.testCaseChecked("FUN_ENUM_0020")
    # end def test_re_enumeration_bond_info_version

    @features('RcvBLEDeviceEnumeration')
    @features('RcvWithDevice')
    @level('Business')
    @services('Debugger')
    def test_re_enumeration_after_dfu_upgrade(self):
        """
        Validate the receiver forces device services re-enumeration when the FW build value in NVS is lower than the
        one from the application.

        RQ_C-RCV-DFU-001#1: When a DFU of the receiver is done, it shall force service re-enumeration
        on each paired device at the first next connection
        """
        ChannelUtils.close_channel(test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Dump the NVS and keep the initial bond info chunk history')
        # --------------------------------------------------------------------------------------------------------------
        self.pairing_slot = 0
        self.chunk_id = f'NVS_BLE_BOND_INFO_ID_{self.pairing_slot}'
        self.receiver_memory_manager.read_nvs()
        self.bond_info_chunk_history = self.receiver_memory_manager.nvs_parser.get_chunk_history(
            chunk_id=self.chunk_id, mode=MODE.RECEIVER)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Add a DFU check FW Info chunk in NVS with value lower than the application FW build')
        # --------------------------------------------------------------------------------------------------------------
        app_entity_idx = self.config_manager.get_feature(ConfigurationManager.ID.FW_TYPE).index(
            str(HexList(DeviceInformation.EntityTypeV1.MAIN_APP)))
        build = self.config_manager.get_feature(ConfigurationManager.ID.BUILD)[app_entity_idx]
        dfu_check = DfuCheckFwInfoChunk(
            fw_build=HexList(Numeral(int(build) - 1, DfuCheckFwInfoChunk.LEN.FW_BUILD // 8)))
        self.receiver_memory_manager.nvs_parser.add_new_chunk(
            chunk_id='NVS_DFU_CHECK_ID', data=HexList(dfu_check))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reload the NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_receiver_nvs = True
        self.receiver_debugger.reload_file(
            nvs_hex_file=self.receiver_memory_manager.nvs_parser.to_hex_file(), no_reset=True)

        self._test_dfu_check_processing()

        self.testCaseChecked("BUS_ENUM_0023")
    # end def test_re_enumeration_after_dfu_upgrade

    @features('RcvBLEDeviceEnumeration')
    @level('Business')
    @services('Debugger')
    def test_re_enumeration_after_dfu_downgrade(self):
        """
        Validate the receiver forces device services re-enumeration when the FW build value in NVS is greater than the
        one from the application.

        RQ_C-RCV-DFU-001#1: When a DFU of the receiver is done, it shall force service re-enumeration
        on each paired device at the first next connection
        """
        ChannelUtils.close_channel(test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Dump the NVS and keep the initial bond info chunk history')
        # --------------------------------------------------------------------------------------------------------------
        self.pairing_slot = 0
        self.chunk_id = f'NVS_BLE_BOND_INFO_ID_{self.pairing_slot}'
        self.receiver_memory_manager.read_nvs()
        self.bond_info_chunk_history = self.receiver_memory_manager.nvs_parser.get_chunk_history(
            chunk_id=self.chunk_id, mode=MODE.RECEIVER)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Add a DFU check FW Info chunk in NVS with value lower than the application FW build')
        # --------------------------------------------------------------------------------------------------------------
        app_entity_idx = self.config_manager.get_feature(ConfigurationManager.ID.FW_TYPE).index(
            str(HexList(DeviceInformation.EntityTypeV1.MAIN_APP)))
        build = self.config_manager.get_feature(ConfigurationManager.ID.BUILD)[app_entity_idx]
        dfu_check = DfuCheckFwInfoChunk(
            fw_build=HexList(Numeral(int(build) + 1, DfuCheckFwInfoChunk.LEN.FW_BUILD // 8)))
        self.receiver_memory_manager.nvs_parser.add_new_chunk(
            chunk_id='NVS_DFU_CHECK_ID', data=HexList(dfu_check))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reload the NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_receiver_nvs = True
        self.receiver_debugger.reload_file(
            nvs_hex_file=self.receiver_memory_manager.nvs_parser.to_hex_file(), no_reset=True)

        self._test_dfu_check_processing()

        self.testCaseChecked("BUS_ENUM_0024")
    # end def test_re_enumeration_after_dfu_downgrade

    @features('RcvBLEDeviceEnumeration')
    @level('Functionality')
    @services('Debugger')
    def test_re_enumeration_after_big_leap_dfu_upgrade(self):
        """
        Validate the receiver forces device services re-enumeration when the FW build value in NVS is lower than the
        previous version compared to the application.

        RQ_C-RCV-DFU-001#1: When a DFU of the receiver is done, it shall force service re-enumeration
        on each paired device at the first next connection
        """
        ChannelUtils.close_channel(test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Dump the NVS and keep the initial bond info chunk history')
        # --------------------------------------------------------------------------------------------------------------
        self.pairing_slot = 0
        self.chunk_id = f'NVS_BLE_BOND_INFO_ID_{self.pairing_slot}'
        self.receiver_memory_manager.read_nvs()
        self.bond_info_chunk_history = self.receiver_memory_manager.nvs_parser.get_chunk_history(
            chunk_id=self.chunk_id, mode=MODE.RECEIVER)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Add a DFU check FW Info chunk in NVS with value lower than the previous application '
                                 'FW build version')
        # --------------------------------------------------------------------------------------------------------------
        app_entity_idx = self.config_manager.get_feature(ConfigurationManager.ID.FW_TYPE).index(
            str(HexList(DeviceInformation.EntityTypeV1.MAIN_APP)))
        build = self.config_manager.get_feature(ConfigurationManager.ID.BUILD)[app_entity_idx]
        build_id_in_nvs = randint(0, int(build) - 2) if int(build) > 2 else 0
        dfu_check = DfuCheckFwInfoChunk(
            fw_build=HexList(Numeral(build_id_in_nvs, DfuCheckFwInfoChunk.LEN.FW_BUILD // 8)))
        self.receiver_memory_manager.nvs_parser.add_new_chunk(
            chunk_id='NVS_DFU_CHECK_ID', data=HexList(dfu_check))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reload the NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_receiver_nvs = True
        self.receiver_debugger.reload_file(
            nvs_hex_file=self.receiver_memory_manager.nvs_parser.to_hex_file(), no_reset=True)

        self._test_dfu_check_processing()

        self.testCaseChecked("FUN_ENUM_0025")
    # end def test_re_enumeration_after_big_leap_dfu_upgrade

    @features('RcvBLEDeviceEnumeration')
    @level('Functionality')
    @services('Debugger')
    def test_no_re_enumeration_when_fw_build_matches(self):
        """
        Validate the receiver doesn't force device services re-enumeration when the FW build value in NVS matches the
        one from the application.
        """
        ChannelUtils.close_channel(test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Dump the NVS and keep the initial bond info chunk history')
        # --------------------------------------------------------------------------------------------------------------
        self.pairing_slot = 0
        self.chunk_id = f'NVS_BLE_BOND_INFO_ID_{self.pairing_slot}'
        self.receiver_memory_manager.read_nvs()
        self.bond_info_chunk_history = self.receiver_memory_manager.nvs_parser.get_chunk_history(
            chunk_id=self.chunk_id, mode=MODE.RECEIVER)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Add a DFU check FW Info chunk in NVS with a build number equal to the application FW '
                                 'build but a reserved field set to a random value')
        # --------------------------------------------------------------------------------------------------------------
        app_entity_idx = self.config_manager.get_feature(ConfigurationManager.ID.FW_TYPE).index(
            str(HexList(DeviceInformation.EntityTypeV1.MAIN_APP)))
        build = self.config_manager.get_feature(ConfigurationManager.ID.BUILD)[app_entity_idx]
        dfu_check = DfuCheckFwInfoChunk(fw_build=HexList(Numeral(int(build), DfuCheckFwInfoChunk.LEN.FW_BUILD // 8)))
        self.receiver_memory_manager.nvs_parser.add_new_chunk(
            chunk_id='NVS_DFU_CHECK_ID', data=HexList(dfu_check))
        initial_dfu_check_chunk_history = self.receiver_memory_manager.nvs_parser.get_chunk_history(
            chunk_id='NVS_DFU_CHECK_ID', mode=MODE.RECEIVER)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reload the NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_receiver_nvs = True
        self.receiver_debugger.reload_file(
            nvs_hex_file=self.receiver_memory_manager.nvs_parser.to_hex_file(), no_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reset the receiver to force the DFU check FW info processing')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, recover_time_needed=True, verify_connection_reset=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Dump the NVS and verify chunk history is not altered')
        # --------------------------------------------------------------------------------------------------------------
        self.receiver_memory_manager.read_nvs()
        dfu_check_chunk_history = self.receiver_memory_manager.nvs_parser.get_chunk_history(
            chunk_id='NVS_DFU_CHECK_ID', mode=MODE.RECEIVER)
        self.assertEqual(expected=len(initial_dfu_check_chunk_history),
                         obtained=len(dfu_check_chunk_history),
                         msg='The number of DFU check FW Info chunks shall not be incremented')
        dfu_check_bond_info_chunk_history = self.receiver_memory_manager.nvs_parser.get_chunk_history(
            chunk_id=self.chunk_id, mode=MODE.RECEIVER)
        self.assertEqual(expected=len(self.bond_info_chunk_history),
                         obtained=len(dfu_check_bond_info_chunk_history),
                         msg='The number of BLE Bond Info chunks shall not be incremented')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify the enumeration pending flag is not set in this instance')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=ReceiverBleBondInfoIdV0.ENUMERATION.DISABLED,
                         obtained=to_int(dfu_check_bond_info_chunk_history[-1].enumeration_pending),
                         msg='The enumeration pending flag differs from the expected one')

        self.testCaseChecked("FUN_ENUM_0026")
    # end def test_no_re_enumeration_when_fw_build_matches

    @features('RcvBLEDeviceEnumeration')
    @level('Functionality')
    @services('Debugger')
    def test_no_re_enumeration_reserved_ignored(self):
        """
        Validate the receiver doesn't force device services re-enumeration when the FW build value in NVS matches the
        one from the application.
        Verify the reserved field of the dfu check fw info chunk is ignored.
        """
        ChannelUtils.close_channel(test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Dump the NVS and keep the initial bond info chunk history')
        # --------------------------------------------------------------------------------------------------------------
        self.pairing_slot = 0
        self.chunk_id = f'NVS_BLE_BOND_INFO_ID_{self.pairing_slot}'
        self.receiver_memory_manager.read_nvs()
        self.bond_info_chunk_history = self.receiver_memory_manager.nvs_parser.get_chunk_history(
            chunk_id=self.chunk_id, mode=MODE.RECEIVER)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Add a DFU check FW Info chunk in NVS with a build number equal to the application FW '
                                 'build but a reserved field set to a random value')
        # --------------------------------------------------------------------------------------------------------------
        app_entity_idx = self.config_manager.get_feature(ConfigurationManager.ID.FW_TYPE).index(
            str(HexList(DeviceInformation.EntityTypeV1.MAIN_APP)))
        build = self.config_manager.get_feature(ConfigurationManager.ID.BUILD)[app_entity_idx]
        dfu_check = DfuCheckFwInfoChunk(fw_build=HexList(Numeral(int(build), DfuCheckFwInfoChunk.LEN.FW_BUILD // 8)))
        dfu_check.reserved = RandHexList(2)
        self.receiver_memory_manager.nvs_parser.add_new_chunk(
            chunk_id='NVS_DFU_CHECK_ID', data=HexList(dfu_check))
        initial_dfu_check_chunk_history = self.receiver_memory_manager.nvs_parser.get_chunk_history(
            chunk_id='NVS_DFU_CHECK_ID', mode=MODE.RECEIVER)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reload the NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_receiver_nvs = True
        self.receiver_debugger.reload_file(
            nvs_hex_file=self.receiver_memory_manager.nvs_parser.to_hex_file(), no_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reset the receiver to force the DFU check FW info processing')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, recover_time_needed=True, verify_connection_reset=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Dump the NVS and verify chunk history is not altered')
        # --------------------------------------------------------------------------------------------------------------
        self.receiver_memory_manager.read_nvs()
        dfu_check_chunk_history = self.receiver_memory_manager.nvs_parser.get_chunk_history(
            chunk_id='NVS_DFU_CHECK_ID', mode=MODE.RECEIVER)
        self.assertEqual(expected=len(initial_dfu_check_chunk_history) + 1,
                         obtained=len(dfu_check_chunk_history),
                         msg='The number of DFU check FW Info chunks shall not be incremented')
        dfu_check_bond_info_chunk_history = self.receiver_memory_manager.nvs_parser.get_chunk_history(
            chunk_id=self.chunk_id, mode=MODE.RECEIVER)
        self.assertEqual(expected=len(self.bond_info_chunk_history),
                         obtained=len(dfu_check_bond_info_chunk_history),
                         msg='The number of BLE Bond Info chunks shall not be incremented')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify the enumeration pending flag is not set in this instance')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=ReceiverBleBondInfoIdV0.ENUMERATION.DISABLED,
                         obtained=to_int(dfu_check_bond_info_chunk_history[-1].enumeration_pending),
                         msg='The enumeration pending flag differs from the expected one')

        self.testCaseChecked("FUN_ENUM_0026")
    # end def test_no_re_enumeration_reserved_ignored

    @features('RcvBLEDeviceEnumeration')
    @level('ErrorHandling')
    @services('Debugger')
    def test_re_enumeration_dfu_check_chunk_corrupted(self):
        """
        Validate the receiver forces device services re-enumeration when the DFU check FW info chunk is corrupted

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
        chunk_id = 'NVS_DFU_CHECK_ID'
        self.receiver_memory_manager.invalidate_chunks([chunk_id, ])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Add a DFU check FW Info chunk in NVS with a build number equal to the application FW '
                                 'build but with a wrong CRC')
        # --------------------------------------------------------------------------------------------------------------
        app_entity_idx = self.config_manager.get_feature(ConfigurationManager.ID.FW_TYPE).index(
            str(HexList(DeviceInformation.EntityTypeV1.MAIN_APP)))
        build = self.config_manager.get_feature(ConfigurationManager.ID.BUILD)[app_entity_idx]
        dfu_check = DfuCheckFwInfoChunk(fw_build=HexList(Numeral(int(build), DfuCheckFwInfoChunk.LEN.FW_BUILD // 8)))
        self.receiver_memory_manager.nvs_parser.add_new_chunk(chunk_id='NVS_DFU_CHECK_ID', data=HexList(dfu_check))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Corrupt the last DFU check FW info chunk CRC")
        # --------------------------------------------------------------------------------------------------------------
        chunk = self.receiver_memory_manager.nvs_parser.get_chunk(chunk_id=chunk_id)
        chunk.chunk_crc += 1
        self.post_requisite_reload_receiver_nvs = True
        self.receiver_memory_manager.load_nvs()

        self._test_dfu_check_processing()

        self.testCaseChecked("ERR_ENUM_0027")
    # end def test_re_enumeration_dfu_check_chunk_corrupted

    @features('RcvBLEDeviceEnumeration')
    @level('Functionality')
    @services('Debugger')
    def test_re_enumeration_after_receiver_and_device_dfus(self):
        """
        Validate the presence of 0x41 and 0x1D4B notifications when the receiver trigers a device re-enumeration (
        through both the DFU check chunk & Bond Info chunk version check) and the device requires a service change (
        through a missing System attribute user service chunk)

        RQ_C-RCV-DFU-001#1: When a DFU of the receiver is done, it shall force service re-enumeration
        on each paired device at the first next connection
        """
        nvs_parser_copy = deepcopy(self.receiver_memory_manager.nvs_parser)

        ChannelUtils.close_channel(test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Add a DFU check FW Info chunk in NVS with value lower than the receiver FW build')
        # --------------------------------------------------------------------------------------------------------------
        app_entity_idx = self.config_manager.get_feature(ConfigurationManager.ID.FW_TYPE).index(
            str(HexList(DeviceInformation.EntityTypeV1.MAIN_APP)))
        build = self.config_manager.get_feature(ConfigurationManager.ID.BUILD)[app_entity_idx]
        dfu_check = DfuCheckFwInfoChunk(
            fw_build=HexList(Numeral(int(build) - 2, DfuCheckFwInfoChunk.LEN.FW_BUILD // 8)))
        nvs_parser_copy.add_new_chunk(chunk_id='NVS_DFU_CHECK_ID', data=HexList(dfu_check))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Replace the last bond info chunk version 1 by an equivalent matching version 0')
        # --------------------------------------------------------------------------------------------------------------
        pairing_slot = 0
        bond_info_chunk_id = f'NVS_BLE_BOND_INFO_ID_{pairing_slot}'
        bond_info_chunk_history = nvs_parser_copy.get_chunk_history(
            chunk_id=bond_info_chunk_id, mode=MODE.RECEIVER)
        nvs_parser_copy.add_new_chunk(
            chunk_id=f'NVS_BLE_BOND_INFO_ID_V0_{pairing_slot}', data=bond_info_chunk_history[-1].convert_to_v0())

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Delete all instances of bond info chunk version 1')
        # --------------------------------------------------------------------------------------------------------------
        nvs_parser_copy.delete_all_chunks(chunk_id=bond_info_chunk_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reload the Receiver NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_receiver_nvs = True
        self.receiver_debugger.reload_file(nvs_hex_file=nvs_parser_copy.to_hex_file(), no_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reset the receiver to force the services structure verification')
        # --------------------------------------------------------------------------------------------------------------
        self.receiver_debugger.reset(soft_reset=False)
        sleep(.5)
        counter = 1
        while counter <= ChannelUtils.GENERIC_RESET_TIMEOUT:
            try:
                sleep(.1)
                ChannelUtils.open_channel(test_case=self)
                break
            except ChannelException as e:
                if e.get_cause() != ChannelException.Cause.DEVICE_NOT_CONNECTED or counter == \
                        ChannelUtils.GENERIC_RESET_TIMEOUT:
                    self.log_traceback_as_warning(
                        supplementary_message=f'Exception in USB channel reconnection with {str(e.get_cause())} '
                                              f'and retry counter = {counter}')
                    raise
                else:
                    counter += 1
                # end if
            # end try
        # end while
        ChannelUtils.set_hidpp_reporting(test_case=self, enable=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Perform User Action to force the device reconnection')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        device_pairing_slot = 1 + pairing_slot
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

        if to_int(bond_info_chunk_history[-1].ble_pro_service_version) >= 2:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Verify a 0x1D4B notification is returned when the sequence is completed')
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.get_only(
                test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, class_type=WirelessDeviceStatusBroadcastEvent,
                check_first_message=False)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Test the connection by sending the enable hidden Features')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.enable_hidden_features(self, device_index=device_pairing_slot)
        # Let sometime for the receiver to complete the procedure
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify the enumeration pending flag is reset in the last instance')
        # --------------------------------------------------------------------------------------------------------------
        self.receiver_memory_manager.read_nvs()
        final_bond_info_chunk_history = self.receiver_memory_manager.nvs_parser.get_chunk_history(
            chunk_id=bond_info_chunk_id, mode=MODE.RECEIVER)
        self.assertEqual(expected=ReceiverBleBondInfoIdV0.ENUMERATION.DISABLED,
                         obtained=to_int(final_bond_info_chunk_history[-1].enumeration_pending),
                         msg='The enumeration pending flag differs from the expected one')

        if to_int(bond_info_chunk_history[-1].ble_pro_service_version) >= 2:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Verify device re-enumeration did occur only if the device exposes a BLE Pro '
                                      'service version greater or equal to 2')
            # ----------------------------------------------------------------------------------------------------------
            self.assertTrue(expr=len(final_bond_info_chunk_history) >= 3,
                            msg=f'The number of DFU chunk in history {len(final_bond_info_chunk_history)} is not '
                                f'greater than 3')
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify bond info chunks version 0 are absent')
        # --------------------------------------------------------------------------------------------------------------
        new_bond_info_chunk_v0_history = self.receiver_memory_manager.nvs_parser.get_chunk_history(
            chunk_id=f'NVS_BLE_BOND_INFO_ID_V0_{pairing_slot}', mode=MODE.RECEIVER)
        self.assertEqual(expected=0,
                         obtained=len(new_bond_info_chunk_v0_history),
                         msg='The number of BLE Bond Info v0 chunk in history is not the expected one')

        self.testCaseChecked("FUN_ENUM_0028")
    # end def test_re_enumeration_after_receiver_and_device_dfus

# end class EnumerationTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
