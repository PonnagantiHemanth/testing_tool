#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.base.receiverinfoutils
:brief:  Helpers for receiver information feature
:author: Zane Lu <zlu@logitech.com>
:date: 2022/06/30
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.registers.nonvolatilememoryoperation import SetNonVolatileMemoryOperationRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilememoryoperation import SetNonVolatileMemoryOperationResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDeviceExtendedPairingInfoRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDeviceExtendedPairingInfoResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDeviceNameRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDeviceNameResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDevicePairingInfoRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDevicePairingInfoResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetFwVersionRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetFwVersionResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetTransceiverEQuadInformation
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetTransceiverEQuadInformationResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import SetAesEncryptionKeyRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import SetAesEncryptionKeyResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import SetEQuadDevicePairingInformationRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import SetEQuadDevicePairingInformationResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import SetEQuadDeviceExtendedPairingInfoRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import SetEQuadDeviceExtendedPairingInfoResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import SetEQuadDeviceNameRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import SetEQuadDeviceNameResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import SetTransceiverEQuadInformationRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import SetTransceiverEQuadInformationResponse
from pyhid.hidpp.hidpp1.setgetregister import SetRegisterResponse
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.receiver.base.receiverbasetestutils import ReceiverBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ReceiverInfoUtils(ReceiverBaseTestUtils):
    """
    This class provides helpers for receiver information features
    """
    @staticmethod
    def get_receiver_pairing_info(test_case):
        """
        Get the receiver pairing information

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``

        :return: GetEQuadDevicePairingInfoResponse
        :rtype: ``GetEQuadDevicePairingInfoResponse``
        """
        report = GetEQuadDevicePairingInfoRequest()
        return ChannelUtils.send(
            test_case=test_case,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=GetEQuadDevicePairingInfoResponse)
    # end def get_receiver_pairing_info

    @staticmethod
    def get_receiver_extended_pairing_info(test_case):
        """
        Get the receiver extended pairing information

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``

        :return: GetEQuadDeviceExtendedPairingInfoResponse
        :rtype: ``GetEQuadDeviceExtendedPairingInfoResponse``
        """
        report = GetEQuadDeviceExtendedPairingInfoRequest()
        return ChannelUtils.send(
            test_case=test_case,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=GetEQuadDeviceExtendedPairingInfoResponse)
    # end def get_receiver_extended_pairing_info

    @staticmethod
    def get_equad_device_name(test_case):
        """
        Get the receiver extended pairing information

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``

        :return: GetEQuadDeviceNameResponse
        :rtype: ``GetEQuadDeviceNameResponse``
        """
        report = GetEQuadDeviceNameRequest()
        return ChannelUtils.send(
            test_case=test_case,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=GetEQuadDeviceNameResponse)
    # end def get_equad_device_name

    @staticmethod
    def get_receiver_fw_information(test_case):
        """
        Get the receiver FW name, version, build number, eQuad Id and eQuad version

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``

        :return: GetFwVersionResponse
        :rtype: ``GetFwVersionResponse``
        """
        report = GetFwVersionRequest()
        return ChannelUtils.send(
            test_case=test_case,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=GetFwVersionResponse)
    # end def get_receiver_fw_version

    @staticmethod
    def get_receiver_equad_info(test_case):
        """
        Get the receiver equad information

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``

        :return: GetTransceiverEQuadInformationResponse
        :rtype: ``GetTransceiverEQuadInformationResponse``
        """
        report = GetTransceiverEQuadInformation()
        return ChannelUtils.send(
            test_case=test_case,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=GetTransceiverEQuadInformationResponse)
    # end def get_receiver_equad_info

    @staticmethod
    def erase_receiver_pairing_info(test_case):
        """
        Erase the receiver's pairing information

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``

        :return: SetNonVolatileMemoryOperationResponse
        :rtype: ``SetNonVolatileMemoryOperationResponse``
        """
        report = SetNonVolatileMemoryOperationRequest(
            device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
            nvm_operation=SetNonVolatileMemoryOperationRequest.NvmOperation.ERASE_PAIRING_DATA,
            target_selection=SetNonVolatileMemoryOperationRequest.TargetSelection.EEPROM)
        return ChannelUtils.send(test_case=test_case,
                                 report=report,
                                 response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                                 response_class_type=SetNonVolatileMemoryOperationResponse)
    # end def erase_receiver_pairing_info

    @staticmethod
    def set_equad_info_to_receiver(test_case, base_address, rf_channel_index, number_of_pairing_slots, last_dest_id):
        """
        Set the equad information to receiver

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param base_address: eQuad base address
        :type base_address: ``HexList``
        :param rf_channel_index: RF channel index, 0=reserved, 1-24=valid channel index, 24-255=reserved
        :type rf_channel_index: ``HexList``
        :param number_of_pairing_slots: number of pairing slots
        :type number_of_pairing_slots: ``HexList``
        :param last_dest_id: last dest id assigned
        :type last_dest_id: ``HexList``

        :return: SetTransceiverEQuadInformationResponse
        :rtype: ``SetTransceiverEQuadInformationResponse | SetRegisterResponse``
        """
        report = SetTransceiverEQuadInformationRequest(
            base_address=base_address,
            rf_channel_index=rf_channel_index,
            number_of_pairing_slots=number_of_pairing_slots,
            last_dest_id=last_dest_id)
        return ChannelUtils.send(test_case=test_case,
                                 report=report,
                                 response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                                 response_class_type=(SetTransceiverEQuadInformationResponse, SetRegisterResponse))
    # end def set_equad_info_to_receiver

    @staticmethod
    def set_device_pairing_info_to_receiver(test_case, destination_id, default_report_interval, device_quid,
                                            equad_major_version, equad_minor_version, equad_device_subclass,
                                            equad_attributes):
        """
        Set the device pairing information to receiver

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param destination_id: Destination ID parameter value
        :type destination_id: ``int`` or ``HexList``
        :param default_report_interval: Default report interval parameter value
        :type default_report_interval: ``int`` or ``HexList``
        :param device_quid: Device QUID parameter value
        :type device_quid: ``int`` or ``HexList``
        :param equad_major_version: eQuad major version parameter value
        :type equad_major_version: ``int`` or ``HexList``
        :param equad_minor_version: eQuad minor version parameter value
        :type equad_minor_version: ``int`` or ``HexList``
        :param equad_device_subclass: eQuad device subclass parameter value
        :type equad_device_subclass: ``int`` or ``HexList``
        :param equad_attributes: eQuad attributes parameter value
        :type equad_attributes: ``int`` or ``HexList``

        :return: SetEQuadDevicePairingInformationResponse
        :rtype: ``SetEQuadDevicePairingInformationResponse | SetRegisterResponse``
        """
        report = SetEQuadDevicePairingInformationRequest(
            destination_id=destination_id,
            default_report_interval=default_report_interval,
            device_quid=device_quid,
            equad_major_version=equad_major_version,
            equad_minor_version=equad_minor_version,
            equad_device_subclass=equad_device_subclass,
            equad_attributes=equad_attributes)
        return ChannelUtils.send(test_case=test_case,
                                 report=report,
                                 response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                                 response_class_type=(SetEQuadDevicePairingInformationResponse, SetRegisterResponse))
    # end def set_device_pairing_info_to_receiver

    @staticmethod
    def set_device_extended_pairing_info_to_receiver(test_case, serial_number, report_types, usability_info):
        """
        Set the device extended pairing information to receiver

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param serial_number: Serial number parameter value
        :type serial_number: ``int`` or ``HexList``
        :param report_types: Report types parameter value
        :type report_types: ``int`` or ``HexList``
        :param usability_info: Device usability info parameter value
        :type usability_info: ``int`` or ``HexList``

        :return: SetEQuadDeviceExtendedPairingInfoResponse
        :rtype: ``SetEQuadDeviceExtendedPairingInfoResponse | SetRegisterResponse``
        """
        report = SetEQuadDeviceExtendedPairingInfoRequest(
            serial_number=serial_number,
            report_types=report_types,
            usability_info=usability_info)
        return ChannelUtils.send(test_case=test_case,
                                 report=report,
                                 response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                                 response_class_type=(SetEQuadDeviceExtendedPairingInfoResponse, SetRegisterResponse))
    # end def set_device_extended_pairing_info_to_receiver

    @staticmethod
    def set_device_name_to_receiver(test_case, segment_length, name_string):
        """
        Set the device name to receiver

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param segment_length: Segment length parameter value
        :type segment_length: ``int`` or ``HexList``
        :param name_string: Name string parameter value
        :type name_string: ``int`` or ``HexList``

        :return: SetEQuadDeviceNameResponse
        :rtype: ``SetEQuadDeviceNameResponse | SetRegisterResponse``
        """
        report = SetEQuadDeviceNameRequest(
            segment_length=segment_length,
            name_string=name_string)
        return ChannelUtils.send(test_case=test_case,
                                 report=report,
                                 response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                                 response_class_type=(SetEQuadDeviceNameResponse, SetRegisterResponse))
    # end def set_device_name_to_receiver

    @staticmethod
    def set_ltk_to_receiver(test_case, aes_encryption_key_byte_1_to_6, aes_encryption_key_byte_9_to_16):
        """
        Set the device Long Term Key to receiver

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param aes_encryption_key_byte_1_to_6: AES encryption key bytes 1 to 6 parameter value
        :type aes_encryption_key_byte_1_to_6: ``HexList``
        :param aes_encryption_key_byte_9_to_16: AES encryption key bytes 9 to 16 parameter value
        :type aes_encryption_key_byte_9_to_16: ``HexList``

        :return: SetAesEncryptionKeyResponse
        :rtype: ``SetAesEncryptionKeyResponse | SetRegisterResponse``
        """
        report = SetAesEncryptionKeyRequest(
            aes_encryption_key_byte_1_to_6=aes_encryption_key_byte_1_to_6,
            aes_encryption_key_byte_9_to_16=aes_encryption_key_byte_9_to_16)
        return ChannelUtils.send(test_case=test_case,
                                 report=report,
                                 response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                                 response_class_type=(SetAesEncryptionKeyResponse, SetRegisterResponse))
    # end def set_ltk_to_receiver

    @staticmethod
    def reload_receiver_params(test_case):
        """
        Reload receiver parameters

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``

        :return: SetNonVolatileMemoryOperationResponse
        :rtype: ``SetNonVolatileMemoryOperationResponse``
        """
        report = SetNonVolatileMemoryOperationRequest(
            device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
            nvm_operation=SetNonVolatileMemoryOperationRequest.NvmOperation.RELOAD,
            target_selection=SetNonVolatileMemoryOperationRequest.TargetSelection.EEPROM)
        return ChannelUtils.send(test_case=test_case,
                                 report=report,
                                 response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                                 response_class_type=SetNonVolatileMemoryOperationResponse)
    # end def reload_receiver_params
# end class ReceiverInfoUtils

# ----------------------------------------------------------------------------------------------------------------------
# End of file
# ----------------------------------------------------------------------------------------------------------------------
