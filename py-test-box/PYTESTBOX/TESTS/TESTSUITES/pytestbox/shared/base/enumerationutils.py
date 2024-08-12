#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.shared.base.enumerationutils
    :brief:  Helpers for device enumeration feature
    :author: Martin Cryonnet
    :date: 2020/04/30
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from queue import Empty

from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.registers.connectionstate import SetConnectionStateRequest
from pyhid.hidpp.hidpp1.registers.connectionstate import SetConnectionStateResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetBLEProDeviceDeviceNameRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetBLEProDeviceDeviceNameResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetBLEProDevicePairingInfoRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetBLEProDevicePairingInfoResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetFwVersionRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetFwVersionResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetUsbSerialNumberRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetUsbSerialNumberResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import NonVolatilePairingInformation
from pyhid.hidpp.hidpp1.registers.receiverfwinformation import GetReceiverFwInfoRequest
from pyhid.hidpp.hidpp1.registers.receiverfwinformation import GetReceiverFwInfoResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class EnumerationTestUtils(CommonBaseTestUtils):
    """
    This class provides helpers for common checks on device enumeration feature
    """
    class FwVersionResponseChecker(CommonBaseTestUtils.MessageChecker):
        """
        This class provides helpers for common checks on FW version response message
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the FW Version API

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "r0": (EnumerationTestUtils.check_r0, NonVolatilePairingInformation.R0.FW_VERSION),
                "fw_number": (cls.check_fw_number, test_case.f.RECEIVER.ENUMERATION.F_Fw_Name),
                "fw_version": (cls.check_fw_version, test_case.f.RECEIVER.ENUMERATION.F_Fw_Version),
                "fw_build_number": (cls.check_fw_build_number, test_case.f.RECEIVER.ENUMERATION.F_Fw_Build_Number),
                "bluetooth_pid": (cls.check_bluetooth_pid, test_case.f.RECEIVER.ENUMERATION.F_Bluetooth_PID),
                "ble_protocol_version": (cls.check_ble_protocol_version,
                                         test_case.f.RECEIVER.ENUMERATION.F_Ble_Protocol_Version),
                "number_of_pairing_slots": (cls.check_number_of_pairing_slots,
                                            test_case.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots)
            }
        # end def get_default_check_map

        @classmethod
        def check_fw_number(cls, test_case, fw_version_response, expected):
            """
            Check fw number field in FW Version response
            """
            test_case.assertEqual(expected=HexList(expected),
                                  obtained=HexList(fw_version_response.fw_number),
                                  msg="FW number should be as expected")
        # end def check_fw_number

        @classmethod
        def check_fw_version(cls, test_case, fw_version_response, expected):
            """
            Check fw version field in FW Version response
            """
            test_case.assertEqual(expected=HexList(expected),
                                  obtained=HexList(fw_version_response.fw_version),
                                  msg="FW version should be as expected")
        # end def check_fw_version

        @classmethod
        def check_fw_build_number(cls, test_case, fw_version_response, expected):
            """
            Check fw build number field in FW Version response
            """
            test_case.assertEqual(expected=HexList(Numeral(expected, 2)),
                                  obtained=HexList(fw_version_response.fw_build_number),
                                  msg="FW build number should be as expected")
        # end def check_fw_build_number

        @classmethod
        def check_bluetooth_pid(cls, test_case, fw_version_response, expected):
            """
            Check bluetooth PID field in FW Version response
            """
            test_case.assertEqual(expected=HexList(Numeral(expected)),
                                  obtained=HexList(fw_version_response.bluetooth_pid),
                                  msg="FW bluetooth PID should be as expected")
        # end def check_bluetooth_pid

        @classmethod
        def check_ble_protocol_version(cls, test_case, fw_version_response, expected):
            """
            Check BLE Protocol version field in FW Version response
            """
            test_case.assertEqual(expected=HexList(expected),
                                  obtained=HexList(fw_version_response.ble_protocol_version),
                                  msg="FW ble protocol version should be as expected")
        # end def check_ble_protocol_version

        @classmethod
        def check_number_of_pairing_slots(cls, test_case, fw_version_response, expected):
            """
            Check number of pairing slots field in FW Version response
            """
            test_case.assertEqual(expected=HexList(expected),
                                  obtained=HexList(fw_version_response.number_of_pairing_slots),
                                  msg="Number of pairing slots should be as expected")
        # end def check_number_of_pairing_slots
    # end class FwVersionResponseChecker

    class EQuadDeviceNameResponseChecker(CommonBaseTestUtils.MessageChecker):
        """
        TODO
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            TODO
            """
            return {
                "r0": (EnumerationTestUtils.check_r0, NonVolatilePairingInformation.R0.EQUAD_STEP4_DEVICE_NAME_MIN),
                "segment_length": (cls.check_segment_length, test_case.f.RECEIVER.ENUMERATION.F_Name_Length),
                "name_string": (cls.check_name_string, test_case.f.RECEIVER.ENUMERATION.F_Name_String),
            }
        # end def get_default_check_map

        @classmethod
        def check_segment_length(cls, test_case, e_quad_device_name_response, expected):
            """
            TODO
            """
            test_case.assertEqual(expected=HexList(expected),
                                  obtained=HexList(e_quad_device_name_response.segment_length),
                                  msg="Segment length should be as expected")
        # end def check_segment_length

        @classmethod
        def check_name_string(cls, test_case, e_quad_device_name_response, expected):
            """
            TODO
            """
            test_case.assertEqual(expected=HexList(expected),
                                  obtained=HexList(e_quad_device_name_response.name_string),
                                  msg="Name string should be as expected")
        # end def check_name_string
    # end class EQuadDeviceNameResponseChecker

    class BLEProDevicePairingInfoResponseChecker(CommonBaseTestUtils.MessageChecker):
        """
        This class provides helpers for common checks on BLE Pro device - pairing information response message
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for BLE Pro Device Pairing information
            """
            bluetooth_pid = test_case.config_manager.get_feature(ConfigurationManager.ID.DEVICES_BLUETOOTH_PIDS)[0]
            bluetooth_pid = HexList(bluetooth_pid)
            bluetooth_pid.reverse()
            return {
                "pairing_slot": (cls.check_pairing_slot,
                                 NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_PAIRING_INFO_MIN),
                "device_type": (cls.check_device_type, test_case.f.SHARED.DEVICES.F_Type[0]),
                "device_info_reserved_4_5": (cls.check_device_info_reserved_4_5, 0),
                "link_status": None,
                "device_info_reserved_7": (cls.check_device_info_reserved_7, 0),
                "bluetooth_pid": (cls.check_bluetooth_pid, bluetooth_pid),
                "device_unit_id": (cls.check_device_unit_id, test_case.f.SHARED.DEVICES.F_UnitIds_1),
                "ble_pro_service_version": (cls.check_ble_pro_service_version,
                                            test_case.config_manager.get_feature(
                                                ConfigurationManager.ID.BLE_PRO_SRV_VERSION)[0]),
                "extended_model_id": (cls.check_extended_model_id, test_case.f.SHARED.DEVICES.F_ExtendedModelId[0]),
                "prepairing_auth_method": (cls.check_prepairing_auth_method,
                                           test_case.f.SHARED.DEVICES.F_PrePairingAuthMethod[0]),
                "reserved_auth_method": (cls.check_reserved_auth_method, 0),
                "emu_2_buttons_auth_method": (cls.check_emu_2_buttons_auth_method,
                                              test_case.f.SHARED.DEVICES.F_Passkey2ButtonsAuthMethod[0] if
                                              test_case.f.PRODUCT.F_IsMice else 0),
                "passkey_auth_method": (cls.check_passkey_auth_method,
                                        0 if test_case.f.PRODUCT.F_IsMice else
                                        test_case.f.SHARED.DEVICES.F_PasskeyAuthMethod[0]),
                "auth_entropy": (cls.check_auth_entropy, test_case.f.SHARED.DEVICES.F_AuthEntropy[0]),
                "device_state": (cls.check_device_state,
                                 NonVolatilePairingInformation.DeviceState.APPLICATION_BOOTLOADER_RECONNECTION)
            }
        # end def get_default_check_map

        @classmethod
        def check_pairing_slot(cls, test_case, response_message, expected):
            """
            Check pairing slot field
            """
            test_case.assertEqual(expected=expected,
                                  obtained=int(Numeral(response_message.pairing_slot)),
                                  msg="Pairing slot should be as expected")
        # end def check_pairing_slot

        @classmethod
        def check_device_type(cls, test_case, response_message, expected):
            """
            Check device type field
            """
            test_case.assertEqual(obtained=int(Numeral(response_message.device_type)),
                                  expected=int(expected),
                                  msg="The device type should be as expected")
        # end def check_device_type

        @classmethod
        def check_device_info_reserved_4_5(cls, test_case, response_message, expected):
            """
            Check device info reserved bits 4-5
            """
            test_case.assertEqual(expected=int(expected),
                                  obtained=int(Numeral(response_message.device_info_reserved_4_5)),
                                  msg="Device info reserved bits should be as expected")
        # end def check_device_info_reserved_4_5

        @classmethod
        def check_link_status(cls, test_case, response_message, expected):
            """
            Check link status
            """
            test_case.assertEqual(expected=int(expected),
                                  obtained=int(Numeral(response_message.link_status)),
                                  msg="Link status should be as expected")
        # end def check_link_status

        @classmethod
        def check_device_info_reserved_7(cls, test_case, response_message, expected):
            """
            Check device info reserved bit 7
            """
            test_case.assertEqual(expected=int(expected),
                                  obtained=int(Numeral(response_message.device_info_reserved_7)),
                                  msg="Device info reserved bits should be as expected")
        # end def check_device_info_reserved_7

        @classmethod
        def check_bluetooth_pid(cls, test_case, response_message, expected):
            """
            Check pairing slot field
            """
            test_case.assertEqual(expected=HexList(expected),
                                  obtained=HexList(response_message.bluetooth_pid),
                                  msg="Bluetooth PID should be as expected")
        # end def check_bluetooth_pid

        @classmethod
        def check_device_unit_id(cls, test_case, response_message, expected):
            """
            Check pairing slot field
            """
            test_case.assertIn(member=str(HexList(response_message.device_unit_id)),
                               container=expected,
                               msg="The device unit id should be in the expected list")
        # end def check_device_unit_id

        @classmethod
        def check_ble_pro_service_version(cls, test_case, response_message, expected):
            """
            Check BLE Pro Service Version
            """
            test_case.assertEqual(expected=HexList(expected),
                                  obtained=HexList(response_message.ble_pro_service_version),
                                  msg="BLE Pro Service Version should be as expected")
        # end def check_ble_pro_service_version

        @classmethod
        def check_extended_model_id(cls, test_case, response_message, expected):
            """
            Check Product Specific Data / Extended Model ID
            """
            test_case.assertEqual(expected=int(expected),
                                  obtained=int(Numeral(response_message.extended_model_id)),
                                  msg="Product Specific Data / Extended Model ID should be as expected")
        # end def check_extended_model_id

        @classmethod
        def check_reserved_auth_method(cls, test_case, response_message, expected):
            """
            Check authentification method reserved bits
            """
            test_case.assertEqual(expected=int(expected),
                                  obtained=int(Numeral(response_message.reserved_auth_method)),
                                  msg="Authentification Method reserved bits should be as expected")
        # end def check_reserved_auth_method

        @classmethod
        def check_emu_2_buttons_auth_method(cls, test_case, response_message, expected):
            """
            Check Passkey emulation with 2 buttons authentication method
            """
            test_case.assertEqual(expected=int(expected),
                                  obtained=int(Numeral(response_message.emu_2_buttons_auth_method)),
                                  msg="Passkey emulation with 2 buttons authentication method should be as expected")
        # end def check_emu_2_buttons_auth_method

        @classmethod
        def check_passkey_auth_method(cls, test_case, response_message, expected):
            """
            Check Passkey authentication method
            """
            test_case.assertEqual(expected=int(expected),
                                  obtained=int(Numeral(response_message.passkey_auth_method)),
                                  msg="Passkey authentication method should be as expected")
        # end def check_passkey_auth_method

        @classmethod
        def check_prepairing_auth_method(cls, test_case, response_message, expected):
            """
            Check Pre Pairing authentication method
            """
            test_case.assertEqual(expected=int(expected),
                                  obtained=int(Numeral(response_message.prepairing_auth_method)),
                                  msg="Pre Pairing authentication method should be as expected")
        # end def check_prepairing_auth_method

        @classmethod
        def check_device_state(cls, test_case, response_message, expected):
            """
            Check Device State field
            """
            test_case.assertEqual(expected=int(expected),
                                  obtained=int(Numeral(response_message.device_state)),
                                  msg="Device State should be as expected")

        # end def check_passkey_auth_method

        @classmethod
        def check_auth_entropy(cls, test_case, response_message, expected):
            """
            Check authentication entropy
            """
            test_case.assertEqual(expected=int(expected),
                                  obtained=int(Numeral(response_message.auth_entropy)),
                                  msg="Authentication entropy should be as expected")
        # end def check_auth_entropy
    # end class BLEProDevicePairingInfoResponseChecker

    class BLEProDeviceNameResponseChecker(CommonBaseTestUtils.MessageChecker):
        """
        This class provides helpers for common checks on BLE Pro device - device name response message
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for BLE Pro Device Pairing information
            """
            return {
                "pairing_slot": (cls.check_pairing_slot,
                                 NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_DEVICE_NAME_MIN),
                "device_name_part": (cls.check_device_name_part,
                                     NonVolatilePairingInformation.BleProDeviceNamePart.PART_1),
                "data": None
            }
        # end def get_default_check_map

        @classmethod
        def check_pairing_slot(cls, test_case, response_message, expected):
            """
            Check pairing slot field
            """
            test_case.assertEqual(expected=expected,
                                  obtained=int(Numeral(response_message.pairing_slot)),
                                  msg="Pairing slot should be as expected")
        # end def check_pairing_slot

        @classmethod
        def check_device_name_part(cls, test_case, response_message, expected):
            """
            Check device name part field
            """
            test_case.assertEqual(expected=expected,
                                  obtained=int(Numeral(response_message.device_name_part)),
                                  msg="Device name part should be as expected")
        # end def check_device_name_part
    # end class BLEProDeviceNameResponseChecker

    class ReceiverFwInfoResponseChecker(CommonBaseTestUtils.MessageChecker):
        """
        This class provides helpers for common checks on Receiver FW Information response message
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values
            """
            return cls.get_check_map_for_entity(test_case, 0)
        # end def get_default_check_map

        @classmethod
        def get_check_map_for_entity(cls, test_case, entity_idx):
            """
            Get the default check methods and expected values
            """
            return {
                "entity_type": (cls.check_entity_type,
                                test_case.config_manager.get_feature(ConfigurationManager.ID.FW_TYPE)[entity_idx]),
                "fw_number": (cls.check_fw_number,
                              test_case.config_manager.get_feature(ConfigurationManager.ID.FW_NUMBER)[entity_idx]),
                "fw_revision": (cls.check_fw_revision,
                                test_case.config_manager.get_feature(ConfigurationManager.ID.REVISION)[entity_idx]),
                "fw_build": (cls.check_fw_build,
                             test_case.config_manager.get_feature(ConfigurationManager.ID.BUILD)[entity_idx]),
                "extra_ver": None
            }
        # end def get_default_check_map

        @classmethod
        def check_entity_type(cls, test_case, response_message, expected):
            """
            Check entity type field
            """
            test_case.assertEqual(expected=int(expected),
                                  obtained=int(Numeral(response_message.entity_type)),
                                  msg="Entity type should be as expected")
        # end def check_entity_type

        @staticmethod
        def check_fw_number(test_case, get_fw_info_response, expected):
            """
            Check fw number field
            """
            test_case.assertEqual(
                obtained=HexList(get_fw_info_response.fw_number),
                expected=HexList(expected),
                msg="FW number should be as expected")
        # end def check_fw_number

        @staticmethod
        def check_fw_revision(test_case, get_fw_info_response, expected):
            """
            Check fw revision field
            """
            test_case.assertEqual(
                obtained=HexList(get_fw_info_response.fw_revision),
                expected=HexList(expected),
                msg="FW revision should be as expected")
        # end def check_fw_revision

        @staticmethod
        def check_fw_build(test_case, get_fw_info_response, expected):
            """
            Check build field
            """
            test_case.assertEqual(
                obtained=HexList(get_fw_info_response.fw_build),
                expected=HexList(expected),
                msg="FW build should be as expected")
        # end def check_fw_build
    # end class ReceiverFwInfoResponseChecker

    @classmethod
    def check_r0(cls, test_case, response, expected):
        """
        Check R0 field in response
        """
        test_case.assertEqual(expected=HexList(expected), obtained=HexList(response.r0), msg="R0 should be as expected")
    # end def check_r0

    @classmethod
    def get_serial_number(cls, test_case):
        """
        Read Serial Number (B5 01)

        :param test_case: The current test case
        :type test_case: ``ReceiverBaseTestCase``
        :return: The response to the read command
        :rtype: ``GetUsbSerialNumberResponse``
        """
        return ChannelUtils.send(
            test_case=test_case,
            report=GetUsbSerialNumberRequest(),
            channel=ChannelUtils.get_receiver_channel(test_case=test_case),
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=GetUsbSerialNumberResponse)
    # end def get_serial_number

    @classmethod
    def get_receiver_fw_version(cls, test_case, entity_idx):
        """
        Retrieve receiver FW information (F4)

        :param test_case: The current test case
        :type test_case: ``ReceiverBaseTestCase``
        :param entity_idx: Targeted entity index
        :type entity_idx: ``int``

        :return: The response to the read command
        :rtype: ``GetReceiverFwInfoResponse``
        """
        return ChannelUtils.send(
            test_case=test_case,
            report=GetReceiverFwInfoRequest(entity_idx),
            channel=ChannelUtils.get_receiver_channel(test_case=test_case),
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=GetReceiverFwInfoResponse)
    # end def get_receiver_fw_version

    @classmethod
    def get_fw_version(cls, test_case):
        """
        Read FW Version (B5 02)

        :param test_case: The current test case
        :type test_case: ``ReceiverBaseTestCase``
        :return: The response to the read command
        :rtype: ``GetFwVersionResponse``
        """
        return ChannelUtils.send(
            test_case=test_case,
            report=GetFwVersionRequest(),
            channel=ChannelUtils.get_receiver_channel(test_case=test_case),
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=GetFwVersionResponse)
    # end def get_fw_version

    @classmethod
    def get_device_pairing_information(cls, test_case, pairing_slot=1):
        """
        Read BLE Pro device pairing information (B5 5n)

        :param test_case: The current test case
        :type test_case: ``ReceiverBaseTestCase``
        :param pairing_slot: The pairing slot to read
        :type pairing_slot: ``int``
        :return: The response to the read command
        :rtype: ``GetBLEProDevicePairingInfoResponse``
        """
        return ChannelUtils.send(
            test_case=test_case,
            report=GetBLEProDevicePairingInfoRequest(
                NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_PAIRING_INFO_MIN + pairing_slot - 1),
            channel=ChannelUtils.get_receiver_channel(test_case=test_case),
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=GetBLEProDevicePairingInfoResponse)
    # end def get_device_pairing_information

    @classmethod
    def get_device_name_part(cls, test_case, pairing_slot=1, part=1):
        """
        Get BLE Pro device name part for a pairing slot (B5 6n nn)

        :param test_case: The current test case
        :type test_case: ``ReceiverBaseTestCase``
        :param pairing_slot: The pairing slot index
        :type pairing_slot: ``int``
        :param part: The part number
        :type part: ``NonVolatilePairingInformation.BleProDeviceNamePart``
        """
        return ChannelUtils.send(
            test_case=test_case,
            report=GetBLEProDeviceDeviceNameRequest(
                NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_DEVICE_NAME_MIN + pairing_slot - 1, part),
            channel=ChannelUtils.get_receiver_channel(test_case=test_case),
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=GetBLEProDeviceDeviceNameResponse)
    # end get_device_name_part

    @classmethod
    def get_device_name(cls, test_case, pairing_slot=1):
        """
        Get the device name at a pairing slot

        :param test_case: The current test case
        :type test_case: ``ReceiverBaseTestCase``
        :param pairing_slot: The pairing slot index
        :type pairing_slot: ``int``
        :return: The device name
        :rtype: ``str``
        """
        device_name_part_2 = None
        device_name_part_3 = None

        device_name_part_1 = cls.get_device_name_part(
            test_case, pairing_slot, NonVolatilePairingInformation.BleProDeviceNamePart.PART_1)
        if (isinstance(device_name_part_1, Hidpp1ErrorCodes) and int(Numeral(device_name_part_1.errorCode)) is
                Hidpp1ErrorCodes.ERR_UNKNOWN_DEVICE):
            return None

        name_length = int(Numeral(device_name_part_1.data.device_name_length))

        if name_length > (GetBLEProDeviceDeviceNameResponse.DeviceNamePart1.LEN.DEVICE_NAME_START // 8):
            device_name_part_2 = cls.get_device_name_part(
                test_case, pairing_slot, NonVolatilePairingInformation.BleProDeviceNamePart.PART_2)

            if name_length > ((GetBLEProDeviceDeviceNameResponse.DeviceNamePart1.LEN.DEVICE_NAME_START +
                              GetBLEProDeviceDeviceNameResponse.DeviceNamePart2or3.LEN.DEVICE_NAME_CHUNK) // 8):
                device_name_part_3 = cls.get_device_name_part(
                    test_case, pairing_slot, NonVolatilePairingInformation.BleProDeviceNamePart.PART_3)

        device_name_parts = [device_name_part_1, device_name_part_2, device_name_part_3]

        return cls.retrieve_device_name(device_name_parts)
    # end def get_device_name

    @classmethod
    def retrieve_device_name(cls, device_name_parts):
        """
        Retrieve device name from device name parts
        """
        name_length = int(Numeral(device_name_parts[0].data.device_name_length))
        name = device_name_parts[0].data.device_name_start.toString()
        name += device_name_parts[1].data.device_name_chunk.toString() if device_name_parts[1] is not None else ''
        name += device_name_parts[2].data.device_name_chunk.toString() if device_name_parts[2] is not None else ''
        return name[:name_length]
    # retrieve_device_name

    @classmethod
    def check_device_name(cls, test_case, responses, expected):
        """
        Check device name
        """
        name = cls.retrieve_device_name(responses)
        test_case.assertEqual(obtained=name, expected=expected,
                              msg='Device name should be as expected')
    # end def check_device_name

    @classmethod
    def paired_device_enumeration_sequence(cls, test_case):
        """
        Run the standard Paired Device Enumeration Sequence

        Sequence diagram:
            SW -> Receiver: Read Receiver Serial Number
            SW -> Receiver: Read Receiver FW version
            loop for each pairing slot
                SW -> Receiver: Read Device Pairing Information
                SW -> Receiver: Read Device Name
            end

        :param test_case: The current test case
        :type test_case: ``ReceiverBaseTestCase``
        :return: Responses received during the sequence
        :rtype: ``Responses``
        """
        if test_case.f.RECEIVER.ENUMERATION.F_ReadSerialNumber:
            serial_number_resp = cls.get_serial_number(test_case)
        else:
            serial_number_resp = None
        # end if

        fw_version_resp = cls.get_fw_version(test_case)

        pairing_infos = []
        devices_names = []
        for pairing_slot in range(1, test_case.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots + 1):
            try:
                pairing_infos.append(cls.get_device_pairing_information(test_case, pairing_slot))
                devices_names.append(cls.get_device_name(test_case, pairing_slot))
            except (AssertionError, Empty):
                test_case.clean_message_type_in_queue(
                    test_case.hidDispatcher.receiver_error_message_queue, Hidpp1ErrorCodes)
                break
            # end try
        # end for

        return serial_number_resp, fw_version_resp, pairing_infos, devices_names
    # end def paired_device_enumeration_sequence

    @classmethod
    def connected_device_enumeration_sequence(cls, test_case):
        """
        Run the standard Connected Device Enumeration sequence

        Sequence diagram:
            SW -> Receiver: Enable HID++ notifications
            SW -> Receiver: Connection State - Fake Arrival
            loop for each connected
                SW <- Receiver: Device Connect Notification
            end
            SW <- Receiver: Fake Arrival response
        """
        test_case.enable_hidpp_reporting()

        connection_state_req = SetConnectionStateRequest(write_action_on_connection_fake_device_arrival=1)
        connection_state_resp = ChannelUtils.send(
            test_case=test_case,
            report=connection_state_req,
            channel=ChannelUtils.get_receiver_channel(test_case=test_case),
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=SetConnectionStateResponse)

        device_connect_notifications = test_case.clean_message_type_in_queue(
            test_case.hidDispatcher.receiver_connection_event_queue, DeviceConnection)

        return device_connect_notifications, connection_state_resp
    # end def connected_device_enumeration_sequence
# end class EnumerationTestUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
