#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytransport.ble.nrfblelibblecontext.nrfblelibprocess
:brief: Define the Process managing nrf-ble-lib asyncio main loop.
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2023/04/21
"""
# ----------------------------------------------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------------------------------------------
from asyncio import CancelledError
from asyncio import Event
from asyncio import Lock
from asyncio import TimeoutError as asyncio_TimeoutError
from asyncio import get_event_loop
from asyncio import new_event_loop
from asyncio import set_event_loop
from asyncio import wait
from asyncio import wait_for
from contextlib import suppress
from os import SCHED_RR
from os import getpid
from os import sched_get_priority_max
from os import sched_param
from os import sched_setscheduler
from queue import Empty
from sys import stdout
from time import time

from aioprocessing import AioProcess
from aioprocessing import AioQueue

from pylibrary.system.tracelogger import TraceLevel
from pylibrary.tools.tracebacklog import TracebackLogWrapper
from pytransport.ble.bleconstants import BleAdvertisingHciEventType
from pytransport.ble.bleconstants import BleAdvertisingPduType
from pytransport.ble.bleconstants import BleCharacteristicPropertiesMask
from pytransport.ble.bleconstants import BleGapAddressType
from pytransport.ble.bleconstants import BleGenericFloatConstant
from pytransport.ble.bleconstants import BleGenericIntConstant
from pytransport.ble.bleconstants import BleUuid128bits
from pytransport.ble.blecontext import BleContext
from pytransport.ble.bleinterfaceclasses import BleAdvertisingData
from pytransport.ble.bleinterfaceclasses import BleCharacteristic
from pytransport.ble.bleinterfaceclasses import BleCharacteristicProperties
from pytransport.ble.bleinterfaceclasses import BleDescriptor
from pytransport.ble.bleinterfaceclasses import BleGapAddress
from pytransport.ble.bleinterfaceclasses import BleGapConnectionParameters
from pytransport.ble.bleinterfaceclasses import BleGapConnectionParametersRange
from pytransport.ble.bleinterfaceclasses import BleGapConnectionSecurityParameters
from pytransport.ble.bleinterfaceclasses import BleService
from pytransport.ble.bleinterfaceclasses import BleUuid
# noinspection PyUnresolvedReferences
from pytransport.ble.nrfblelibblecontext.nrf_ble_lib import Adapter
# noinspection PyUnresolvedReferences
from pytransport.ble.nrfblelibblecontext.nrf_ble_lib import CharacteristicSetup
# noinspection PyUnresolvedReferences
from pytransport.ble.nrfblelibblecontext.nrf_ble_lib import Connection
# noinspection PyUnresolvedReferences
from pytransport.ble.nrfblelibblecontext.nrf_ble_lib import DescriptorSetup
# noinspection PyUnresolvedReferences
from pytransport.ble.nrfblelibblecontext.nrf_ble_lib import GattDbSetup
# noinspection PyUnresolvedReferences
from pytransport.ble.nrfblelibblecontext.nrf_ble_lib import NrfblError
# noinspection PyUnresolvedReferences
from pytransport.ble.nrfblelibblecontext.nrf_ble_lib import ServiceSetup
# noinspection PyUnresolvedReferences
from pytransport.ble.nrfblelibblecontext.nrf_ble_lib import Uuid
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import AddServiceToCentralGattTableRequestArgsInd
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import CharacteristicReadRequestArgsInd
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import CharacteristicWriteRequestArgsInd
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import ConnectRequestArgsInd
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import DeleteBondRequestArgsInd
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import DescriptorReadRequestArgsInd
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import DeviceAdvertisingInformationIndex
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import DisconnectRequestArgsInd
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import ErrorId
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import GetConnectionSecurityParametersRequestArgsInd
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import IoCapability
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import NrfBleLibConnectionCacheTupleIndex
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import NrfBleLibHciOpcode
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import NrfBleLibProcessMessageType
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import NrfBleLibProcessUtil
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import PairRequestArgsInd
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import PerformServiceDiscoveryRequestArgsInd
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import ReadOperation
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import ScanStartRequestArgsInd
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import SetConnectionParametersRangeRequestArgsInd
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import SetIndicationStatusRequestArgsInd
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import SetNotificationStatusRequestArgsInd
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import UpdateConnectionParametersRequestArgsInd
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import WriteOperation
from pytransport.transportcontext import TransportContextException

# ----------------------------------------------------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------------------------------------------------
VERBOSE = False
VERBOSE_ERROR = False
# For some reason, PyCharm decided that it is duplicated code while after verification it is not
# noinspection DuplicatedCode
REQUEST_TO_RESPONSE = {
    NrfBleLibProcessMessageType.STOP_REQUEST: NrfBleLibProcessMessageType.STOP_RESPONSE,
    NrfBleLibProcessMessageType.SCAN_REQUEST: NrfBleLibProcessMessageType.SCAN_RESPONSE,
    NrfBleLibProcessMessageType.SCAN_STOP_REQUEST: NrfBleLibProcessMessageType.SCAN_STOP_RESPONSE,
    NrfBleLibProcessMessageType.CONNECT_REQUEST: NrfBleLibProcessMessageType.CONNECT_RESPONSE,
    NrfBleLibProcessMessageType.DISCONNECT_REQUEST: NrfBleLibProcessMessageType.DISCONNECT_RESPONSE,
    NrfBleLibProcessMessageType.PERFORM_SERVICE_DISCOVERY_REQUEST:
        NrfBleLibProcessMessageType.PERFORM_SERVICE_DISCOVERY_RESPONSE,
    NrfBleLibProcessMessageType.PAIR_REQUEST: NrfBleLibProcessMessageType.PAIR_RESPONSE,
    NrfBleLibProcessMessageType.DELETE_BOND_REQUEST: NrfBleLibProcessMessageType.DELETE_BOND_RESPONSE,
    NrfBleLibProcessMessageType.UPDATE_CONNECTION_PARAMETERS_REQUEST:
        NrfBleLibProcessMessageType.UPDATE_CONNECTION_PARAMETERS_RESPONSE,
    NrfBleLibProcessMessageType.GET_CONNECTION_SECURITY_PARAMETERS_REQUEST:
        NrfBleLibProcessMessageType.GET_CONNECTION_SECURITY_PARAMETERS_REQUEST,
    NrfBleLibProcessMessageType.CHARACTERISTIC_WRITE_REQUEST: NrfBleLibProcessMessageType.CHARACTERISTIC_WRITE_RESPONSE,
    NrfBleLibProcessMessageType.UPDATE_GATT_TABLE_REQUEST: NrfBleLibProcessMessageType.UPDATE_GATT_TABLE_RESPONSE,
    NrfBleLibProcessMessageType.CHARACTERISTIC_READ_REQUEST: NrfBleLibProcessMessageType.CHARACTERISTIC_READ_RESPONSE,
    NrfBleLibProcessMessageType.DESCRIPTOR_READ_REQUEST: NrfBleLibProcessMessageType.DESCRIPTOR_READ_RESPONSE,
    NrfBleLibProcessMessageType.SET_NOTIFICATION_STATUS_REQUEST:
        NrfBleLibProcessMessageType.SET_NOTIFICATION_STATUS_RESPONSE,
    NrfBleLibProcessMessageType.SET_INDICATION_STATUS_REQUEST:
        NrfBleLibProcessMessageType.SET_INDICATION_STATUS_RESPONSE,
    NrfBleLibProcessMessageType.GET_CENTRAL_ADDRESS_REQUEST: NrfBleLibProcessMessageType.GET_CENTRAL_ADDRESS_RESPONSE,
    NrfBleLibProcessMessageType.SET_CONNECTION_PARAMETERS_RANGE_REQUEST:
        NrfBleLibProcessMessageType.SET_CONNECTION_PARAMETERS_RANGE_RESPONSE,
}
ERROR_TYPES = [NrfBleLibProcessMessageType.ERROR_RESPONSE, NrfBleLibProcessMessageType.ERROR_EVENT,
               NrfBleLibProcessMessageType.CRITICAL_ERROR_RESPONSE,
               NrfBleLibProcessMessageType.CRITICAL_ERROR_EVENT]
# Events simply forwarded to higher levels
MESSAGE_FORWARD = [
    "le_connection_complete",
    "sm_passkey_input_number",
    "sm_passkey_display_number",
    "sm_numeric_comparison_request",
    "sm_keypress_notification",
    "le_connection_update_complete",
    "sm_pairing_started",
    "sm_pairing_complete",
]
# ----------------------------------------------------------------------------------------------------------------------
# Implementation
# ----------------------------------------------------------------------------------------------------------------------
async def event_wait(event, timeout):
    """
    Wait for an asyncio event adding the timeout possibility

    :param event: Event to wait on
    :type event: ``Event``
    :param timeout: timeout of the event, ``None`` to deactivate it and wait forever
    :type timeout: ``int``
    :return:
    """
    # suppress TimeoutError because it will return False in case of timeout
    with suppress(asyncio_TimeoutError):
        await wait_for(fut=event.wait(), timeout=timeout)
    # end with
    return event.is_set()
# end def event_wait


class NrfBleLibStructureTranslator:
    """
    Class to use to translate driver structures and values to interface structures and values
    """
    BLE_ADVERTISING_TYPE_MAP_FROM_DRIVER = {
        BleAdvertisingHciEventType.CONNECTABLE_UNDIRECTED: BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
        BleAdvertisingHciEventType.CONNECTABLE_DIRECTED: BleAdvertisingPduType.CONNECTABLE_DIRECTED,
        BleAdvertisingHciEventType.NON_CONNECTABLE_UNDIRECTED: BleAdvertisingPduType.NON_CONNECTABLE_UNDIRECTED,
        BleAdvertisingHciEventType.SCANNABLE_UNDIRECTED: BleAdvertisingPduType.SCANNABLE_UNDIRECTED,
        BleAdvertisingHciEventType.SCAN_RSP: BleAdvertisingPduType.SCAN_RSP,
    }

    @classmethod
    def get_interface_ble_gap_address(cls, driver_ble_gap_address):
        """
        Get the interface structure from the driver structure.

        :param driver_ble_gap_address: Dictionary containing the address information in the driver format
        :type driver_ble_gap_address: ``dict``

        :return: Corresponding interface structure
        :rtype: ``BleGapAddress``
        """
        return BleGapAddress(address_type=BleGapAddressType(driver_ble_gap_address["address_type"]),
                             address=driver_ble_gap_address["address"].replace(":", ""))
    # end def get_interface_ble_gap_address

    @classmethod
    def get_driver_ble_gap_address(cls, interface_ble_gap_address):
        """
        Get the interface structure from the driver structure.

        :param interface_ble_gap_address: Interface structure for BLE advertising data
        :type interface_ble_gap_address: ``BleGapAddress``

        :return: Corresponding dictionary containing the address information in the driver format
        :rtype: ``dict``
        """
        address_type = interface_ble_gap_address.address_type.value
        address_str = ""
        # Add colons
        for i in range(0, len(interface_ble_gap_address.address), 2):
            address_str += interface_ble_gap_address.address[i:i + 2] + ":"
        # end for
        # Remove the last colon
        address_str = address_str[:-1]
        return {"address_type": address_type, "address": address_str}
    # end def get_driver_ble_gap_address

    @staticmethod
    def get_interface_ble_uuid(driver_uuid):
        """
        Get the interface structure from the driver structure.

        :param driver_uuid: Driver structure for UUID
        :type driver_uuid: ``dict``

        :return: Corresponding interface structure
        :rtype: ``BleUuid``
        """
        if driver_uuid["uuid16"] != 0:
            return BleUuid(value=driver_uuid["uuid16"])
        else:
            return BleUuid.from_array(uuid_array=list(driver_uuid["uuid128"]))
        # end if
    # end def get_interface_ble_uuid

    @staticmethod
    def get_driver_ble_uuid(interface_uuid):
        """
        Get the driver structure from the interface structure.

        :param interface_uuid: Interface structure for UUID
        :type interface_uuid: ``BleUuid``

        :return: Corresponding driver structure
        :rtype: ``dict``
        """
        if interface_uuid.base == BleUuid128bits.BLE_BASE_16_BITS_UUID:
            return {"uuid16": interface_uuid.value, "uuid128": interface_uuid.to_array()}
        else:
            return {"uuid16": 0, "uuid128": interface_uuid.to_array()}
        # end if
    # end def get_driver_ble_uuid

    @staticmethod
    def get_interface_characteristic_properties(driver_characteristic_properties):
        """
        Get the interface structure from the driver structure.

        :param driver_characteristic_properties: Driver structure for UUID
        :type driver_characteristic_properties: ``int``

        :return: Corresponding interface structure
        :rtype: ``BleCharacteristicProperties``
        """
        return BleCharacteristicProperties(
            broadcast=bool(driver_characteristic_properties & BleCharacteristicPropertiesMask.BROADCAST),
            read=bool(driver_characteristic_properties & BleCharacteristicPropertiesMask.READ),
            write_wo_resp=bool(
                driver_characteristic_properties & BleCharacteristicPropertiesMask.WRITE_WITHOUT_RESPONSE),
            write=bool(driver_characteristic_properties & BleCharacteristicPropertiesMask.WRITE),
            notify=bool(driver_characteristic_properties & BleCharacteristicPropertiesMask.NOTIFY),
            indicate=bool(driver_characteristic_properties & BleCharacteristicPropertiesMask.INDICATE),
            auth_signed_wr=bool(
                driver_characteristic_properties & BleCharacteristicPropertiesMask.AUTHENTICATED_SIGNED_WRITES))
    # end def get_interface_characteristic_properties

    @staticmethod
    def get_driver_characteristic_properties(interface_characteristic_properties, to_add_characteristics=False):
        """
        Get the driver structure from the interface structure. There can be different structure depending on the
        situation:

        * ``dict`` when adding a characteristic to a GATT table
        * ``int`` when creating a GATT table

        :param interface_characteristic_properties: Interface structure for UUID
        :type interface_characteristic_properties: ``BleCharacteristicProperties``
        :param to_add_characteristics: Flag indicating if it is to add a characteristic to a GATT table - OPTIONAL
        :type to_add_characteristics: ``bool``

        :return: Corresponding driver structure
        :rtype: ``dict`` or ``int``
        """
        if to_add_characteristics:
            return {"broadcast": interface_characteristic_properties.broadcast,
                    "read": interface_characteristic_properties.read,
                    "write_without_response": interface_characteristic_properties.write_wo_resp,
                    "write": interface_characteristic_properties.write,
                    "notify": interface_characteristic_properties.notify,
                    "indicate": interface_characteristic_properties.indicate,
                    "authenticated_signed_write": interface_characteristic_properties.auth_signed_wr}
        else:
            properties = 0

            if interface_characteristic_properties.broadcast:
                properties += BleCharacteristicPropertiesMask.BROADCAST
            # end if

            if interface_characteristic_properties.read:
                properties += BleCharacteristicPropertiesMask.READ
            # end if

            if interface_characteristic_properties.write_wo_resp:
                properties += BleCharacteristicPropertiesMask.WRITE_WITHOUT_RESPONSE
            # end if

            if interface_characteristic_properties.write:
                properties += BleCharacteristicPropertiesMask.WRITE
            # end if

            if interface_characteristic_properties.notify:
                properties += BleCharacteristicPropertiesMask.NOTIFY
            # end if

            if interface_characteristic_properties.indicate:
                properties += BleCharacteristicPropertiesMask.INDICATE
            # end if

            if interface_characteristic_properties.auth_signed_wr:
                properties += BleCharacteristicPropertiesMask.AUTHENTICATED_SIGNED_WRITES
            # end if

            return properties
        # end if
    # end def get_driver_characteristic_properties

    @classmethod
    def get_interface_service(cls, driver_service):
        """
        Get the interface structure from the driver structure.

        :param driver_service: Driver structure for BLE service
        :type driver_service: ``dict``

        :return: Corresponding interface structure
        :rtype: ``BleService``
        """
        return BleService(
            uuid=cls.get_interface_ble_uuid(driver_uuid={"uuid16": driver_service["uuid16"],
                                                         "uuid128": driver_service["uuid128"]}),
            start_handle=driver_service["start_group_handle"],
            end_handle=driver_service["end_group_handle"])
    # end def get_interface_service

    @classmethod
    def get_driver_service(cls, interface_service):
        """
        Get the driver structure from the interface structure.

        :param interface_service: Interface structure for BLE service
        :type interface_service: ``BleService``

        :return: Corresponding driver structure
        :rtype: ``dict``
        """
        return {
            "uuid16": int(interface_service.uuid.value),
            "uuid128": interface_service.uuid.to_array(),
            "start_group_handle": interface_service.handle,
            "end_group_handle": interface_service.end_handle}
    # end def get_driver_service

    @classmethod
    def get_interface_characteristic(cls, driver_characteristic):
        """
        Get the interface structure from the driver structure.

        :param driver_characteristic: Driver structure for BLE characteristic
        :type driver_characteristic: ``dict``

        :return: Corresponding interface structure
        :rtype: ``BleCharacteristic``
        """
        return BleCharacteristic(
            uuid=cls.get_interface_ble_uuid(driver_uuid={"uuid16": driver_characteristic["uuid16"],
                                                         "uuid128": driver_characteristic["uuid128"]}),
            properties=cls.get_interface_characteristic_properties(
                driver_characteristic["properties"]),
            declaration_handle=driver_characteristic["start_handle"],
            value_handle=driver_characteristic["value_handle"])
    # end def get_interface_characteristic

    @classmethod
    def get_driver_characteristic(cls, interface_characteristic):
        """
        Get the driver structure from the interface structure.

        :param interface_characteristic: Interface structure for BLE characteristic
        :type interface_characteristic: ``BleCharacteristic``

        :return: Corresponding driver structure
        :rtype: ``dict``
        """
        end_handle = interface_characteristic.handle
        for descriptor in interface_characteristic.descriptors:
            if descriptor.handle > end_handle:
                end_handle = descriptor.handle
            # end if
        # end for

        return {
            "uuid16": int(interface_characteristic.uuid.value),
            "uuid128": interface_characteristic.uuid.to_array(),
            "properties": cls.get_driver_characteristic_properties(
                interface_characteristic_properties=interface_characteristic.properties),
            "start_handle": interface_characteristic.declaration.handle,
            "value_handle": interface_characteristic.handle,
            "end_handle": end_handle}
    # end def get_driver_characteristic

    @classmethod
    def get_interface_descriptor(cls, driver_descriptor):
        """
        Get the interface structure from the driver structure.

        :param driver_descriptor: Driver structure for BLE descriptor
        :type driver_descriptor: ``dict``

        :return: Corresponding interface structure
        :rtype: ``BleDescriptor``
        """
        return BleDescriptor(uuid=cls.get_interface_ble_uuid(driver_uuid={"uuid16": driver_descriptor["uuid16"],
                                                                          "uuid128": driver_descriptor["uuid128"]}),
                             handle=driver_descriptor["handle"])
    # end def get_interface_descriptor

    @classmethod
    def get_driver_descriptor(cls, interface_descriptor):
        """
        Get the driver structure from the interface structure.

        :param interface_descriptor: Interface structure for BLE descriptor
        :type interface_descriptor: ``BleDescriptor``

        :return: Corresponding driver structure
        :rtype: ``dict``
        """
        return {
            "uuid16": int(interface_descriptor.uuid.value),
            "uuid128": interface_descriptor.uuid.to_array(),
            "handle": interface_descriptor.handle}
    # end def get_driver_descriptor

    @staticmethod
    def get_interface_connection_parameters(driver_connection_parameters):
        """
        Get the interface structure from the driver structure.

        :param driver_connection_parameters: Driver structure for BLE connection parameters
        :type driver_connection_parameters: ``dict``

        :return: Corresponding interface structure
        :rtype: ``BleGapConnectionParameters``
        """
        if "interval_min" in driver_connection_parameters.keys():
            # From L2CapConnectionParameterUpdateRequest event
            return BleGapConnectionParameters(
                min_connection_interval=driver_connection_parameters[
                    "interval_min"] * BleGenericFloatConstant.CONNECTION_INTERVAL_GRANULARITY,
                max_connection_interval=driver_connection_parameters[
                    "interval_max"] * BleGenericFloatConstant.CONNECTION_INTERVAL_GRANULARITY,
                supervision_timeout=driver_connection_parameters[
                    "supervision_timeout"] * BleGenericIntConstant.SUPERVISION_TIMEOUT_GRANULARITY,
                slave_latency=driver_connection_parameters["max_latency"])
        elif "connection_interval" in driver_connection_parameters.keys():
            # From LeConnectionUpdateComplete event
            return BleGapConnectionParameters(
                min_connection_interval=driver_connection_parameters[
                    "connection_interval"] * BleGenericFloatConstant.CONNECTION_INTERVAL_GRANULARITY,
                max_connection_interval=driver_connection_parameters[
                    "connection_interval"] * BleGenericFloatConstant.CONNECTION_INTERVAL_GRANULARITY,
                supervision_timeout=driver_connection_parameters[
                    "supervision_timeout"] * BleGenericIntConstant.SUPERVISION_TIMEOUT_GRANULARITY,
                slave_latency=driver_connection_parameters["peripheral_latency"])
        else:
            raise ValueError(f"Unknown driver_connection_parameters = {driver_connection_parameters}")
        # end if
    # end def get_interface_connection_parameters

    @staticmethod
    def get_driver_connection_parameters(interface_connection_parameters):
        """
        Get the driver structure from the interface structure.

        :param interface_connection_parameters: Interface structure for BLE connection parameters
        :type interface_connection_parameters: ``BleGapConnectionParameters``

        :return: Corresponding driver structure
        :rtype: ``dict``
        """
        assert interface_connection_parameters.min_connection_interval % \
               BleGenericFloatConstant.CONNECTION_INTERVAL_GRANULARITY == 0, \
               f"min_connection_interval should be a multiple of " \
               f"{BleGenericFloatConstant.CONNECTION_INTERVAL_GRANULARITY}, " \
               f"{interface_connection_parameters.min_connection_interval} is not"
        assert interface_connection_parameters.max_connection_interval % \
               BleGenericFloatConstant.CONNECTION_INTERVAL_GRANULARITY == 0, \
               f"max_connection_interval should be a multiple of " \
               f"{BleGenericFloatConstant.CONNECTION_INTERVAL_GRANULARITY}, " \
               f"{interface_connection_parameters.max_connection_interval} is not"
        assert interface_connection_parameters.slave_latency >= 0, \
            f"slave_latency should be a positive value, {interface_connection_parameters.slave_latency} is not"
        assert interface_connection_parameters.supervision_timeout % \
               BleGenericIntConstant.SUPERVISION_TIMEOUT_GRANULARITY == 0, \
               f"supervision_timeout should be a multiple of " \
               f"{BleGenericIntConstant.SUPERVISION_TIMEOUT_GRANULARITY}, " \
               f"{interface_connection_parameters.supervision_timeout} is not"

        return {
            "connection_interval_min": int(interface_connection_parameters.min_connection_interval /
                                           BleGenericFloatConstant.CONNECTION_INTERVAL_GRANULARITY),
            "connection_interval_max": int(interface_connection_parameters.max_connection_interval /
                                           BleGenericFloatConstant.CONNECTION_INTERVAL_GRANULARITY),
            "max_latency": interface_connection_parameters.slave_latency,
            "supervision_timeout": int(interface_connection_parameters.supervision_timeout /
                                       BleGenericIntConstant.SUPERVISION_TIMEOUT_GRANULARITY)
        }
    # end def get_driver_connection_parameters

    @staticmethod
    def get_driver_connection_parameters_range(interface_connection_parameters_range):
        """
        Get the driver structure from the interface structure.

        :param interface_connection_parameters_range: Interface structure for BLE connection parameters
        :type interface_connection_parameters_range: ``BleGapConnectionParametersRange``

        :return: Corresponding driver structure
        :rtype: ``dict``
        """
        assert interface_connection_parameters_range.min_connection_interval % \
               BleGenericFloatConstant.CONNECTION_INTERVAL_GRANULARITY == 0, \
               f"min_connection_interval should be a multiple of " \
               f"{BleGenericFloatConstant.CONNECTION_INTERVAL_GRANULARITY}, " \
               f"{interface_connection_parameters_range.min_connection_interval} is not"
        assert interface_connection_parameters_range.max_connection_interval % \
               BleGenericFloatConstant.CONNECTION_INTERVAL_GRANULARITY == 0, \
               f"max_connection_interval should be a multiple of " \
               f"{BleGenericFloatConstant.CONNECTION_INTERVAL_GRANULARITY}, " \
               f"{interface_connection_parameters_range.max_connection_interval} is not"
        assert interface_connection_parameters_range.min_slave_latency >= 0, \
            f"min_slave_latency should be a positive value, " \
            f"{interface_connection_parameters_range.min_slave_latency} is not"
        assert interface_connection_parameters_range.max_slave_latency >= 0, \
            f"max_slave_latency should be a positive value, " \
            f"{interface_connection_parameters_range.max_slave_latency} is not"
        assert interface_connection_parameters_range.min_supervision_timeout % \
               BleGenericIntConstant.SUPERVISION_TIMEOUT_GRANULARITY == 0, \
               f"min_supervision_timeout should be a multiple of " \
               f"{BleGenericIntConstant.SUPERVISION_TIMEOUT_GRANULARITY}, " \
               f"{interface_connection_parameters_range.min_supervision_timeout} is not"
        assert interface_connection_parameters_range.max_supervision_timeout % \
               BleGenericIntConstant.SUPERVISION_TIMEOUT_GRANULARITY == 0, \
               f"max_supervision_timeout should be a multiple of " \
               f"{BleGenericIntConstant.SUPERVISION_TIMEOUT_GRANULARITY}, " \
               f"{interface_connection_parameters_range.max_supervision_timeout} is not"

        return {
            "connection_interval_min": int(interface_connection_parameters_range.min_connection_interval /
                                           BleGenericFloatConstant.CONNECTION_INTERVAL_GRANULARITY),
            "connection_interval_max": int(interface_connection_parameters_range.max_connection_interval /
                                           BleGenericFloatConstant.CONNECTION_INTERVAL_GRANULARITY),
            "connection_latency_min": interface_connection_parameters_range.min_slave_latency,
            "connection_latency_max": interface_connection_parameters_range.max_slave_latency,
            "supervision_timeout_min": int(interface_connection_parameters_range.min_supervision_timeout /
                                           BleGenericIntConstant.SUPERVISION_TIMEOUT_GRANULARITY),
            "supervision_timeout_max": int(interface_connection_parameters_range.max_supervision_timeout /
                                           BleGenericIntConstant.SUPERVISION_TIMEOUT_GRANULARITY)
        }
    # end def get_driver_connection_parameters_range

    @staticmethod
    def get_interface_connection_security_parameters(driver_connection_security_parameters):
        """
        Get the interface structure from the driver structure.

        :param driver_connection_security_parameters: Driver structure for BLE connection security parameters
        :type driver_connection_security_parameters: ``dict``

        :return: Corresponding interface structure
        :rtype: ``BleGapConnectionSecurityParameters``
        """
        return BleGapConnectionSecurityParameters(
            encrypted=driver_connection_security_parameters["encrypted"],
            mitm=driver_connection_security_parameters["authenticated"],
            lesc=driver_connection_security_parameters["secure_connection"],
            encryption_key_size=driver_connection_security_parameters["key_size"],
            bonded=driver_connection_security_parameters["bonded"])
    # end def get_interface_connection_security_parameters

    @staticmethod
    def get_driver_connection_security_parameters(interface_connection_security_parameters):
        """
        Get the driver structure from the interface structure.

        :param interface_connection_security_parameters: Interface structure for BLE connection security parameters
        :type interface_connection_security_parameters: ``BleGapConnectionSecurityParameters``

        :return: Corresponding driver structure
        :rtype: ``dict``
        """
        return {
            "encrypted": interface_connection_security_parameters.encrypted,
            "authenticated": interface_connection_security_parameters.mitm,
            "secure_connection": interface_connection_security_parameters.lesc,
            "key_size": interface_connection_security_parameters.encryption_key_size,
            "bonded": interface_connection_security_parameters.bonded,
        }
    # end def get_driver_connection_security_parameters

    @classmethod
    def get_driver_gatt_db_setup(cls, interface_gatt_table):
        """
        Get the driver structure from the interface structure.

        :param interface_gatt_table: Interface structure for BLE GATT table
        :type interface_gatt_table: ``list[BleService]``

        :return: Corresponding driver structure
        :rtype: ``GattDbSetup``
        """
        gatt_db_setup = GattDbSetup()

        for service in interface_gatt_table:
            service_setup = ServiceSetup(
                uuid=Uuid.uuid16(service.uuid.value) if service.uuid.is_16_bits_uuid else Uuid.uuid128(
                    service.uuid.to_array()))

            for characteristic in service.characteristics:
                # TODO add read and write security: See Jira ticket for pc-ble-driver-py:
                #  https://jira.logitech.io/browse/PTB-1657
                uuid = Uuid.uuid16(characteristic.uuid.value) if characteristic.uuid.is_16_bits_uuid else Uuid.uuid128(
                    characteristic.uuid.to_array())
                characteristic_setup = CharacteristicSetup(
                    uuid=uuid,
                    properties=cls.get_driver_characteristic_properties(
                        interface_characteristic_properties=characteristic.properties, to_add_characteristics=True),
                    read_security='none',
                    write_security='none',
                    value_options={
                        'initial_value': list(characteristic.value) if characteristic.value is not None else []})

                for descriptor in characteristic.descriptors:
                    # TODO add read and write security: See Jira ticket for pc-ble-driver-py:
                    #  https://jira.logitech.io/browse/PTB-1657
                    # TODO add read and write permission, for now they are put to True by default
                    uuid = Uuid.uuid16(descriptor.uuid.value) if descriptor.uuid.is_16_bits_uuid else Uuid.uuid128(
                        descriptor.uuid.to_array())
                    descriptor_setup = DescriptorSetup(
                        uuid=uuid,
                        properties={'read': True, 'write': True},
                        read_security='none',
                        write_security='none',
                        value_options={'initial_value': list(descriptor.value) if descriptor.value is not None else []})

                    characteristic_setup.add_descriptor(descriptor=descriptor_setup)
                # end for

                service_setup.add_characteristic(characteristic=characteristic_setup)
            # end for

            gatt_db_setup.add_service(service=service_setup)
        # end for

        return gatt_db_setup
    # end def get_driver_gatt_db_setup
# end class NrfBleLibStructureTranslator


class NrfBleLibScanFilters:
    """
    Filters used during the scan procedure
    """

    def __init__(self, expected_addresses=None, expected_company_id=None, directed_device_address_to_find=None,
                 stop_at_first_advertising=False, stop_at_first_scan_response=False):
        """
        :param expected_addresses: The expected address filter - OPTIONAL
        :type expected_addresses: ``list[BleGapAddress]`` or ``None``
        :param expected_company_id: The expected company ID filter - OPTIONAL
        :type expected_company_id: ``int`` or ``None``
        :param directed_device_address_to_find: Device to find as directed advertising - OPTIONAL
        :type directed_device_address_to_find: ``BleGapAddress`` or ``None``
        :param stop_at_first_advertising: Flag indicating to stop scanning when the first advertising packet of the
                                          wanted device is found - OPTIONAL
        :type stop_at_first_advertising: ``bool``
        :param stop_at_first_scan_response: Flag indicating to stop scanning when the first scan response packet of the
                                            wanted device is found - OPTIONAL
        :type stop_at_first_scan_response: ``bool``
        """
        self.expected_addresses = expected_addresses
        self.expected_company_id = expected_company_id
        self.directed_device_address_to_find = directed_device_address_to_find
        self.stop_at_first_advertising = stop_at_first_advertising
        self.stop_at_first_scan_response = stop_at_first_scan_response
    # end def __init__

    def clear_filters(self):
        """
        Clear the filters values to default values
        """
        self.expected_addresses = None
        self.expected_company_id = None
        self.directed_device_address_to_find = None
        self.stop_at_first_advertising = False
        self.stop_at_first_scan_response = False
    # end def clear_filters

    def copy_filters(self, other_scan_filters):
        """
        Copy the filters values of another instance to this one

        :param other_scan_filters: Other scan filters to copy in this one
        :type other_scan_filters: ``NrfBleLibScanFilters``
        """
        self.expected_addresses = other_scan_filters.expected_addresses
        self.expected_company_id = other_scan_filters.expected_company_id
        self.directed_device_address_to_find = other_scan_filters.directed_device_address_to_find
        self.stop_at_first_advertising = other_scan_filters.stop_at_first_advertising
        self.stop_at_first_scan_response = other_scan_filters.stop_at_first_scan_response
    # end def copy_filters
# end class NrfBleLibScanFilters


class NrfBleLibAsyncioProcess:
    """
    Process that runs the asyncio main loop for the nrf-ble-lib calls.
    """
    BLOCKING_DEFAULT_TIMEOUT = 15  # In seconds
    PROCESS_CONSECUTIVE_ERROR_MAX_COUNT = 50  # TODO Find a better value or even remove the concept all together

    def __init__(self, com_port, request_queue=None, response_queue=None, event_queue=None):
        """
        Main method for the nrf-ble-lib process.

        :param com_port: COM port to use
        :type com_port: ``str``
        :param request_queue: The request queue to be able to call the nrf-ble-lib methods from the main process,
                              if ``None`` is given, a new Queue will be created - OPTIONAL
        :type request_queue: ``AioQueue`` or ``None``
        :param response_queue: The response queue to be able to receive the nrf-ble-lib response in the main process,
                               if ``None`` is given, a new Queue will be created - OPTIONAL
        :type response_queue: ``AioQueue`` or ``None``
        :param event_queue: The event queue to be able to receive the nrf-ble-lib event in the main process,
                            if ``None`` is given, a new Queue will be created - OPTIONAL
        :type event_queue: ``AioQueue`` or ``None``
        """
        self._com_port = com_port
        self._request_queue = request_queue if request_queue is not None else AioQueue()
        self._response_queue = response_queue if response_queue is not None else AioQueue()
        self._event_queue = event_queue if event_queue is not None else AioQueue()

        # TODO: why use spawn (see "Contexts and start methods" in
        #  https://docs.python.org/3.7/library/multiprocessing.html#multiprocessing.Process)
        # set_start_method('spawn', force=True)
        self._nrf_ble_lib_process = None
    # end def __init__

    @classmethod
    def _run_nrf_ble_lib_process(cls, com_port, request_queue, response_queue, event_queue):
        """
        Main method for the nrf-ble-lib process.

        :param com_port: COM port to use
        :type com_port: ``str``
        :param request_queue: The request queue to be able to call the nrf-ble-lib methods from the main process
        :type request_queue: ``AioQueue``
        :param response_queue: The response queue to be able to receive the nrf-ble-lib response in the main process
        :type response_queue: ``AioQueue``
        :param event_queue: The event queue to be able to receive the nrf-ble-lib event in the main process
        :type event_queue: ``AioQueue``
        """
        if VERBOSE:
            stdout.write(f"Start nrf-ble-lib process, process PID = {getpid()}\n")
        # end if

        ble_adapter = Adapter(com_port)

        try:
            asyncio_loop = get_event_loop()
        except RuntimeError as e:
            if "There is no current event loop" in str(e):
                asyncio_loop = new_event_loop()
                set_event_loop(asyncio_loop)
            else:
                raise
            # end if
        # end try

        connection_cache = {}
        devices_scanned = {}
        scan_filters = NrfBleLibScanFilters()
        # Event to wait on when starting scan
        start_scan_event = Event()
        start_scan_event.set()
        # Event to wait on when stopping scan
        stop_scan_event = Event()
        stop_scan_event.set()
        # Event to wait on when stopping scan
        stop_scan_before_timeout_event = Event()
        stop_scan_before_timeout_event.set()
        # Event giving the scanning status: cleared = True and set = False
        scanning = Event()
        scanning.set()
        # Event to wait on when starting and stopping scan
        scan_events_lock = Lock()

        async def _stop_scan():
            """
            Stop the scan

            :raise ``TransportContextException``: If the stop timed out
            """
            await scan_events_lock.acquire()
            try:
                if scanning.is_set():
                    return
                # end if
                stop_scan_event.clear()
                ble_adapter.gap_stop_scan()
                if not await event_wait(event=stop_scan_event, timeout=NrfBleLibProcessUtil.SCAN_START_STOP_TIMEOUT):
                    raise TransportContextException(
                        TransportContextException.Cause.CONTEXT_INTERNAL_ERROR, "Advertising did not stop")
                # end if
            finally:
                scan_events_lock.release()
            # end try
        # end def _stop_scan

        def log_trace(message, trace_level):
            """
            Put a log message on the queue to be logged by the main process
            
            :param message: message of the log
            :type message: ``str``
            :param trace_level: level of logging
            :type trace_level: ``TraceLevel``
            """
            event_arguments = (trace_level, message)

            event_queue.put(
                (NrfBleLibProcessMessageType.LOG_EVENT, event_arguments))
        # end def log_trace

        def _get_connection_in_cache_from_args(args_tuple, connection_handle_index):
            """
            Get the (connection_handle, address, connection) tuple in cache
            associated with a connection handle from arguments received with a request

            :param args_tuple: The args to get the connection handle
            :type args_tuple: ``tuple``
            :param connection_handle_index: The index of the connection handle in the arguments tuple
            :type connection_handle_index: ``int``

            :return: The connection handle and its cache
            :rtype: ``tuple``

            :raise ``TransportContextException``: If the connection could not be found
            """
            connection_handle = args_tuple[connection_handle_index]
            cache = connection_cache.get(connection_handle, None)
            if cache is None:
                raise TransportContextException(TransportContextException.Cause.DEVICE_NOT_CONNECTED)
            # end if

            return connection_handle, cache[NrfBleLibConnectionCacheTupleIndex.ADDRESS_INDEX_IN_CACHED_TUPLE], \
                cache[NrfBleLibConnectionCacheTupleIndex.CONNECTION_INDEX_IN_CACHED_TUPLE]
        # end def _get_connection_in_cache_from_args

        def _treat_advertising_event(advertising_report, timestamp):
            """
            Treat an advertising event received in the event thread

            :param advertising_report: The dictionary representing the event
            :type advertising_report: ``dict``
            :param timestamp: Monotonic timestamp in nanoseconds
            :type timestamp: ``int``
            """
            device_address = NrfBleLibStructureTranslator.get_interface_ble_gap_address(
                driver_ble_gap_address=advertising_report)
            advertising_type = BleAdvertisingHciEventType(advertising_report["event_type"])
            advertising_data = list(advertising_report["data"])
            company_id = BleContext.get_company_id(advertising_data=BleAdvertisingData.from_list(
                advertising_data_list=advertising_data, timestamp=timestamp))

            expected_addresses = scan_filters.expected_addresses
            expected_company_id = scan_filters.expected_company_id
            stop_at_first_advertising = scan_filters.stop_at_first_advertising
            stop_at_first_scan_response = scan_filters.stop_at_first_scan_response
            directed_device_address_to_find = scan_filters.directed_device_address_to_find

            device_already_scanned = devices_scanned.get(device_address, None)

            if directed_device_address_to_find is not None:
                # If directed_device_address_to_find is not None, we should focus on directed advertising
                # and ignore other advertising types, having this ``if`` alone permits to ignore all other devices
                # when scanning for a specific device
                if advertising_type == BleAdvertisingHciEventType.CONNECTABLE_DIRECTED and \
                        device_address == directed_device_address_to_find:

                    log_trace(
                        message="[Advertising event] Found wanted direct advertising device: "
                                f"{directed_device_address_to_find}",
                        trace_level=TraceLevel.DEBUG)
                    if devices_scanned.get(directed_device_address_to_find, None) is None:
                        devices_scanned[directed_device_address_to_find] = (
                            BleAdvertisingPduType.CONNECTABLE_DIRECTED, advertising_data, [timestamp],
                            None, None)
                        stop_scan_before_timeout_event.set()
                    # end if
                # end if
            elif expected_addresses is None or device_address in expected_addresses:
                if advertising_type == BleAdvertisingHciEventType.CONNECTABLE_DIRECTED or \
                        (advertising_type in [BleAdvertisingHciEventType.CONNECTABLE_UNDIRECTED,
                                              BleAdvertisingHciEventType.NON_CONNECTABLE_UNDIRECTED,
                                              BleAdvertisingHciEventType.SCANNABLE_UNDIRECTED] and
                         (expected_company_id is None or company_id == expected_company_id)):
                    # Either a directed advertising or an indirect one with the right company ID (if requested)
                    if device_already_scanned is None:
                        scanned_device = [NrfBleLibStructureTranslator.BLE_ADVERTISING_TYPE_MAP_FROM_DRIVER[
                                    advertising_type], [advertising_data], [[timestamp]], None, None, None]
                        devices_scanned[device_address] = scanned_device

                        log_trace(
                            message=f"\tFound wanted advertising device with address: {device_address}",
                            trace_level=TraceLevel.DEBUG)

                        if stop_at_first_advertising:
                            stop_scan_before_timeout_event.set()
                        # end if
                    else:
                        if advertising_data in device_already_scanned[
                            DeviceAdvertisingInformationIndex.ADVERTISING_DATA]:
                            log_trace(
                                message="\tNew packet for already found advertising device with "
                                        f"address: {device_address}, with known data={advertising_data}",
                                trace_level=TraceLevel.DEBUG)
                            timestamp_index= \
                                device_already_scanned[DeviceAdvertisingInformationIndex.ADVERTISING_DATA]\
                                    .index(advertising_data)
                        else:
                            log_trace(
                                message="\tNew packet for already found advertising device with "
                                        f"address: {device_address}, with new data={advertising_data}",
                                trace_level=TraceLevel.DEBUG)
                            device_already_scanned[DeviceAdvertisingInformationIndex.ADVERTISING_DATA].append(advertising_data)
                            device_already_scanned[DeviceAdvertisingInformationIndex.ADVERTISING_TIMESTAMPS].append([])
                            timestamp_index = len(
                                device_already_scanned[DeviceAdvertisingInformationIndex.ADVERTISING_DATA]) - 1
                        # end if
                        device_already_scanned[DeviceAdvertisingInformationIndex.ADVERTISING_TIMESTAMPS][timestamp_index].append(
                            timestamp)
                    # end if
                elif advertising_type == BleAdvertisingHciEventType.SCAN_RSP and \
                        device_already_scanned is not None:
                    if device_already_scanned[DeviceAdvertisingInformationIndex.SCAN_RESPONSE_DATA] is None:
                        log_trace(
                            message=f"\tScan response for device with address: {device_address}",
                            trace_level=TraceLevel.DEBUG)
                        device_already_scanned[DeviceAdvertisingInformationIndex.SCAN_RESPONSE_DATA] = [advertising_data]
                        device_already_scanned[DeviceAdvertisingInformationIndex.SCAN_RESPONSE_TIMESTAMPS] = [[timestamp]]

                        if stop_at_first_scan_response:
                            stop_scan_before_timeout_event.set()
                        # end if
                    else:
                        if advertising_data in \
                                device_already_scanned[DeviceAdvertisingInformationIndex.SCAN_RESPONSE_DATA]:
                            log_trace(
                                message=f"\tNew packet for scan response for device with address: "
                                        f"{device_address}, with known data={advertising_data}",
                                trace_level=TraceLevel.DEBUG)
                            timestamp_index = \
                                device_already_scanned[DeviceAdvertisingInformationIndex.SCAN_RESPONSE_DATA] \
                                    .index(advertising_data)
                        else:
                            log_trace(
                                message=f"\tNew packet for scan response for device with address: "
                                        f"{device_address}, with new data={advertising_data}",
                                trace_level=TraceLevel.DEBUG)
                            device_already_scanned[DeviceAdvertisingInformationIndex.SCAN_RESPONSE_DATA].append(
                                advertising_data)
                            device_already_scanned[DeviceAdvertisingInformationIndex.SCAN_RESPONSE_TIMESTAMPS].append([])
                            timestamp_index = len(
                                device_already_scanned[DeviceAdvertisingInformationIndex.SCAN_RESPONSE_DATA]) - 1
                        # end if
                        device_already_scanned[DeviceAdvertisingInformationIndex.SCAN_RESPONSE_TIMESTAMPS][
                            timestamp_index].append(
                            timestamp)
                    # end if
                else:
                    log_trace(
                        message=f"\tUnknown advertising type: {advertising_type}",
                        trace_level=TraceLevel.DEBUG)

                # end if
            # end if
        # end def _treat_advertising_event

        async def _async_scan_timout_task(scan_timeout):
            """
            Asyncio method for the scan timeout, it can also be stopped using the event ``scanning``.

            :param scan_timeout: The scan timeout in seconds
            :type scan_timeout: ``int`` or ``float``
            """
            # noinspection PyBroadException
            try:
                if VERBOSE:
                    stdout.write(f"Scan timeout Task started for {scan_timeout}s\n")
                # end if

                start_time = time()
                await event_wait(event=stop_scan_before_timeout_event, timeout=scan_timeout)
                await _stop_scan()

                if VERBOSE:
                    stdout.write(f"Scan timeout Task finished after {time() - start_time}s\n")
                # end if
                await response_queue.coro_put((NrfBleLibProcessMessageType.SCAN_RESPONSE, (devices_scanned,)))
            except CancelledError:
                if VERBOSE:
                    stdout.write("Scan timeout Task canceled\n")
                # end if
            except TransportContextException as transport_context_exception:
                if VERBOSE_ERROR:
                    stdout.write("Scan timeout Task raised a transport exception: "
                                 f"{TracebackLogWrapper.get_exception_stack()}\n")
                # end if
                error_code = ErrorId.TRANSPORT_CONTEXT_EXCEPTION + transport_context_exception.get_cause()
                error_event_arguments = (NrfBleLibProcessMessageType.SCAN_REQUEST, tuple(), error_code)
                error_message = transport_context_exception.get_message()
                if len(error_message) > 0:
                    error_event_arguments += (error_message,)
                # end if
                await response_queue.coro_put(
                    (NrfBleLibProcessMessageType.ERROR_RESPONSE, error_event_arguments))
            except Exception as other_exception:
                if VERBOSE_ERROR:
                    stdout.write("Scan timeout Task raised an exception: "
                                 f"{TracebackLogWrapper.get_exception_stack()}\n")
                # end if
                error_event_arguments = (NrfBleLibProcessMessageType.SCAN_REQUEST, tuple(), ErrorId.OTHER_EXCEPTIONS)
                error_message = str(other_exception)
                if len(error_message) > 0:
                    error_event_arguments += (error_message,)
                # end if
                await response_queue.coro_put(
                    (NrfBleLibProcessMessageType.ERROR_RESPONSE, error_event_arguments))
            # end try
        # end def _async_scan_timout_task

        async def _async_event_treatment_task():
            """
            Asyncio method for the task to treat the events gotten from the adapter
            """
            # noinspection PyBroadException
            try:
                if VERBOSE:
                    stdout.write("Event Task started\n")
                # end if

                event_stream = await ble_adapter.events()

                consecutive_other_exception_count = 0
                event = await event_stream.next()
                while event is not None:
                    try:
                        if event["type"] in MESSAGE_FORWARD:
                            if VERBOSE:
                                stdout.write(f"{event['type']} received {event} and forwarded\n")
                            # end if
                            await event_queue.coro_put((NrfBleLibProcessMessageType.NRF_BLE_LIB_EVENT, (event,)))
                        elif event["type"] == "gatt_notification":
                            if VERBOSE:
                                stdout.write(f"gatt_notification received {event}\n")
                            # end if
                            await event_queue.coro_put(
                                (NrfBleLibProcessMessageType.NOTIFICATION_EVENT,
                                 (event["event_data"]["connection_handle"], event["event_data"]["value_handle"],
                                  event["event_data"]["value"], event["timestamp"])))
                        elif event["type"] == "gatt_indication":
                            if VERBOSE:
                                stdout.write(f"gatt_indication received {event}\n")
                            # end if
                            await event_queue.coro_put(
                                (NrfBleLibProcessMessageType.INDICATION_EVENT,
                                 (event["event_data"]["connection_handle"], event["event_data"]["value_handle"],
                                  event["event_data"]["value"], event["timestamp"])))
                        elif event["type"] == "hci_disconnection_complete":
                            if VERBOSE:
                                stdout.write(f"hci_disconnection_complete received {event}, remove from connection "
                                             "cache\n")
                            # end if
                            # Disconnection: remove the connection from the internal cache
                            cache = connection_cache.pop(event["event_data"]["connection_handle"], None)
                            await event_queue.coro_put((NrfBleLibProcessMessageType.NRF_BLE_LIB_EVENT, (event,)))
                        elif event["type"] == 'sm_just_works_request':
                            if VERBOSE:
                                stdout.write(f"sm_just_works_request received {event}\n")
                            # end if
                            cache = connection_cache.get(event["event_data"]["connection_handle"], None)
                            if cache is not None:
                                connection = cache[NrfBleLibConnectionCacheTupleIndex.CONNECTION_INDEX_IN_CACHED_TUPLE]
                                await connection.sm_just_works_confirm()
                            # end if
                        elif event["type"] == "l2_cap_connection_parameter_update_request":
                            if VERBOSE:
                                stdout.write(f"l2_cap_connection_parameter_update_request received {event}\n")
                            # end if
                            log_trace(f"l2_cap_connection_parameter_update_request received at {event['timestamp']}",
                                      TraceLevel.DEBUG)
                            connection_parameters = {
                                "connection_interval_min": event["event_data"]["interval_min"],
                                "connection_interval_max": event["event_data"]["interval_max"],
                                "max_latency": event["event_data"]["max_latency"],
                                "supervision_timeout": event["event_data"]["supervision_timeout"]
                            }
                            accepted = ble_adapter.connection_parameters_are_in_accepted_range_for_update_requests(
                                connection_parameters=connection_parameters)
                            await event_queue.coro_put(
                                (NrfBleLibProcessMessageType.L2CAP_CONNECTION_PARAMETER_UPDATE_REQUEST_EVENT,
                                 (event["event_data"], event["timestamp"], accepted)))
                        elif event["type"] == "hci_command_complete":
                            if VERBOSE:
                                stdout.write(f"hci_command_complete received {event}\n")
                            # end if

                            if event["event_data"]["command_opcode"] == NrfBleLibHciOpcode.LE_SET_SCAN_ENABLE:
                                to_log = ""
                                if not stop_scan_event.is_set():
                                    scanning.set()
                                    stop_scan_event.set()
                                    to_log = ", stopping scanning"
                                elif not start_scan_event.is_set():
                                    scanning.clear()
                                    start_scan_event.set()
                                    to_log = ", starting scanning"
                                # end if
                                log_trace(f"hci_command_complete LE_SET_SCAN_ENABLE received{to_log} at {event['timestamp']}",
                                          TraceLevel.DEBUG)

                            elif event["event_data"]["command_opcode"] in [
                                    NrfBleLibHciOpcode.LE_REMOTE_CONNECTION_PARAMETER_REQUEST_REPLY,
                                    NrfBleLibHciOpcode.LE_REMOTE_CONNECTION_PARAMETER_REQUEST_NEGATIVE_REPLY]:
                                await event_queue.coro_put((NrfBleLibProcessMessageType.NRF_BLE_LIB_EVENT, (event,)))
                            # end if
                        elif event["type"] == "gap_event_advertising_report":
                            if VERBOSE:
                                stdout.write(f"gap_event_advertising_report received {event}\n")
                            # end if
                            if not scanning.is_set():
                                _treat_advertising_event(
                                    advertising_report=event["event_data"], timestamp=event["timestamp"])
                            # end if
                        elif event["type"] != "other":
                            if VERBOSE:
                                stdout.write(f"{event['type']} received {event}, untreated\n")
                            # end if
                        # end if

                        # Reset the consecutive exception count because no exceptions arise for this event
                        consecutive_other_exception_count = 0
                    except CancelledError:
                        raise
                    except Exception as other_exception:
                        consecutive_other_exception_count += 1
                        error_event_arguments = (NrfBleLibProcessMessageType.NRF_BLE_LIB_EVENT, (event["type"],),
                                                 ErrorId.OTHER_EXCEPTIONS)
                        error_message = str(other_exception)
                        if len(error_message) > 0:
                            error_event_arguments += (error_message,)
                        # end if
                        if consecutive_other_exception_count > cls.PROCESS_CONSECUTIVE_ERROR_MAX_COUNT:
                            if VERBOSE_ERROR:
                                stdout.write("Event Task Finished in a raise condition inside the run loop: "
                                             f"{TracebackLogWrapper.get_exception_stack()}\n")
                            # end if
                            await event_queue.coro_put(
                                (NrfBleLibProcessMessageType.CRITICAL_ERROR_EVENT, error_event_arguments))
                            await request_queue.coro_put((NrfBleLibProcessMessageType.STOP_REQUEST, tuple()))
                            return
                        else:
                            if VERBOSE_ERROR:
                                stdout.write("Event Task raised an exception inside the run loop: "
                                             f"{TracebackLogWrapper.get_exception_stack()}\n")
                            # end if
                            await event_queue.coro_put(
                                (NrfBleLibProcessMessageType.ERROR_EVENT, error_event_arguments))
                        # end if
                    # end try
                    event = await event_stream.next()
                # end while
            except CancelledError:
                if "event_stream" in locals():
                    # noinspection PyUnboundLocalVariable
                    event_stream.stop()
                # end if
                if VERBOSE:
                    stdout.write("Event Task canceled\n")
                # end if
            except Exception:
                if VERBOSE_ERROR:
                    stdout.write("Event Task raised an exception outside the run loop: "
                                 f"{TracebackLogWrapper.get_exception_stack()}\n")
                # end if
            else:
                if VERBOSE:
                    stdout.write("Event Task finished\n")
                # end if
            # end try
        # end def _async_event_treatment_task

        # Create the event task here to be able to call its cancel method in _async_request_treatment_task
        event_task = asyncio_loop.create_task(_async_event_treatment_task())

        async def _async_request_treatment_task():
            """
            Asyncio method for the task to treat the request gotten from the main process
            """

            async def _clean_stop():
                """
                Clean all associated tasks and connection before stopping the request task
                """
                event_task.cancel()
                connection_cache_list = list(connection_cache.values())
                # Disconnect all connected devices
                for _, conn in connection_cache_list:
                    try:
                        await conn.disconnect()
                    except Exception as other_ex:
                        if str(other_ex) != "Connection has already been closed":
                            raise
                        # end if
                    # end try
                # end for
                await wait_for(fut=event_task, timeout=None)
                connection_cache.clear()
            # end def _clean_stop

            # noinspection PyBroadException
            try:
                if VERBOSE:
                    stdout.write("Request Task started\n")
                # end if

                # TODO add connections to cache instead of disconnecting them when the possibility to get notification
                #  and indication streams is possible
                current_connections = ble_adapter.connections()
                for connection in current_connections:
                    try:
                        await connection.disconnect()
                    except Exception as ex:
                        if str(ex) != "Connection has already been closed":
                            raise
                        # end if
                    # end try
                # end for

                consecutive_other_exception_count = 0
                scanning_timeout_task = None
                run = True
                while run:
                    request, args = await request_queue.coro_get()
                    try:
                        if request == NrfBleLibProcessMessageType.STOP_REQUEST:
                            if VERBOSE:
                                stdout.write("Stopping Request Task\n")
                            # end if
                            run = False
                            await _clean_stop()
                            await response_queue.coro_put((REQUEST_TO_RESPONSE[request], tuple()))
                            continue
                        elif request == NrfBleLibProcessMessageType.SCAN_REQUEST:
                            scan_parameters = args[ScanStartRequestArgsInd.SCAN_PARAMETERS]
                            scan_filters.copy_filters(other_scan_filters=args[ScanStartRequestArgsInd.SCAN_FILTERS])
                            scan_timeout = args[ScanStartRequestArgsInd.SCAN_TIMEOUT]
                            devices_scanned.clear()
                            start_scan_event.clear()
                            stop_scan_before_timeout_event.clear()
                            await ble_adapter.gap_start_scan(scan_parameters)
                            if not await event_wait(
                                    event=start_scan_event, timeout=NrfBleLibProcessUtil.SCAN_START_STOP_TIMEOUT):
                                raise TransportContextException(
                                    TransportContextException.Cause.CONTEXT_INTERNAL_ERROR, "Advertising did not start")
                            # end if
                            scanning_timeout_task = asyncio_loop.create_task(_async_scan_timout_task(
                                scan_timeout=scan_timeout))
                            # Response is sent in the timeout task, this permit to unlock the request task and
                            # stop scanning by request if wanted
                        elif request == NrfBleLibProcessMessageType.SCAN_STOP_REQUEST:
                            await _stop_scan()
                            if scanning_timeout_task is not None:
                                # Suppress TimeoutError because it will return False in case of timeout
                                with suppress(asyncio_TimeoutError):
                                    await wait_for(
                                        fut=scanning_timeout_task, timeout=NrfBleLibProcessUtil.SCAN_START_STOP_TIMEOUT)
                                # end with
                                if not scanning_timeout_task.done():
                                    scanning_timeout_task.cancel()
                                # end if
                                scanning_timeout_task = None
                            # end if
                            await response_queue.coro_put((REQUEST_TO_RESPONSE[request], tuple()))
                        elif request == NrfBleLibProcessMessageType.CONNECT_REQUEST:
                            address = args[ConnectRequestArgsInd.DEVICE_ADDRESS]
                            if len(args) > ConnectRequestArgsInd.CONNECTION_PARAMETERS:
                                connection_parameters = args[ConnectRequestArgsInd.CONNECTION_PARAMETERS]
                                connection = await ble_adapter.gap_connect(
                                    address["address"], address["address_type"], connection_parameters)
                            else:
                                connection = await ble_adapter.gap_connect(address["address"], address["address_type"])
                            # end if
                            connection_handle = await connection.handle()
                            connection_cache[connection_handle] = (address, connection)
                            await response_queue.coro_put((REQUEST_TO_RESPONSE[request], (address, connection_handle)))
                        elif request == NrfBleLibProcessMessageType.DISCONNECT_REQUEST:
                            try:
                                _, address, connection = \
                                    _get_connection_in_cache_from_args(
                                        args_tuple=args,
                                        connection_handle_index=DisconnectRequestArgsInd.CONNECTION_HANDLE)
                            except TransportContextException as exp:
                                if exp.get_cause() == TransportContextException.Cause.DEVICE_NOT_CONNECTED:
                                    await response_queue.coro_put((REQUEST_TO_RESPONSE[request], (None,)))
                                else:
                                    raise
                                # end if
                            else:
                                if connection is not None:
                                    try:
                                        await connection.disconnect()
                                    except Exception as ex:
                                        if str(ex) != "Connection has already been closed":
                                            raise
                                        # end if
                                    # end try
                                # end if
                                await response_queue.coro_put((REQUEST_TO_RESPONSE[request], (address,)))
                            # end try
                        elif request == NrfBleLibProcessMessageType.PERFORM_SERVICE_DISCOVERY_REQUEST:
                            _, _, connection = _get_connection_in_cache_from_args(
                                args_tuple=args,
                                connection_handle_index=PerformServiceDiscoveryRequestArgsInd.CONNECTION_HANDLE)

                            driver_services = await connection.discover_primary_services()
                            gatt_table = []
                            for driver_service in driver_services:
                                interface_service = NrfBleLibStructureTranslator.get_interface_service(
                                    driver_service=driver_service)
                                gatt_table.append(interface_service)
                                driver_characteristics = await connection.discover_characteristics_for_service(
                                    driver_service)
                                for driver_characteristic in driver_characteristics:
                                    interface_characteristic = \
                                        NrfBleLibStructureTranslator.get_interface_characteristic(
                                            driver_characteristic=driver_characteristic)
                                    interface_service.characteristics.append(interface_characteristic)

                                    driver_descriptors = await connection.discover_descriptors_for_characteristic(
                                        driver_characteristic)
                                    for driver_descriptor in driver_descriptors:
                                        interface_characteristic.descriptors.append(
                                            NrfBleLibStructureTranslator.get_interface_descriptor(
                                                driver_descriptor=driver_descriptor))
                                    # end for
                                # end for
                            # end for

                            await response_queue.coro_put((REQUEST_TO_RESPONSE[request], (gatt_table,)))
                        elif request == NrfBleLibProcessMessageType.PAIR_REQUEST:
                            _, _, connection = _get_connection_in_cache_from_args(
                                args_tuple=args, connection_handle_index=PairRequestArgsInd.CONNECTION_HANDLE)

                            io_capabilities = args[PairRequestArgsInd.IO_CAPABILITIES]
                            if isinstance(io_capabilities, IoCapability):
                                io_capabilities = io_capabilities.value
                            # end if

                            await ble_adapter.sm_set_io_capabilities(io_capabilities)
                            await ble_adapter.sm_set_authentication_requirements(
                                args[PairRequestArgsInd.AUTHENTICATION_REQUIREMENTS])

                            if args[PairRequestArgsInd.ASYNC]:
                                await response_queue.coro_put((REQUEST_TO_RESPONSE[request], tuple()))
                                await connection.pair()
                                await event_queue.coro_put((NrfBleLibProcessMessageType.PAIRED_EVENT, tuple()))
                            else:
                                await connection.pair()
                                await response_queue.coro_put((REQUEST_TO_RESPONSE[request], tuple()))
                            # end if
                        elif request == NrfBleLibProcessMessageType.DELETE_BOND_REQUEST:
                            address = args[DeleteBondRequestArgsInd.DEVICE_ADDRESS]

                            device_db = ble_adapter.device_db()
                            # TODO add error management if device bonding already deleted
                            device_db.remove_entry_for_address(address["address"], address["address_type"])

                            await response_queue.coro_put((REQUEST_TO_RESPONSE[request], tuple()))
                        elif request == NrfBleLibProcessMessageType.UPDATE_CONNECTION_PARAMETERS_REQUEST:
                            _, _, connection = _get_connection_in_cache_from_args(
                                args_tuple=args,
                                connection_handle_index=UpdateConnectionParametersRequestArgsInd.CONNECTION_HANDLE)

                            await connection.update_connection_parameters(
                                args[UpdateConnectionParametersRequestArgsInd.CONNECTION_PARAMETERS])
                            await response_queue.coro_put((REQUEST_TO_RESPONSE[request], tuple()))
                        elif request == NrfBleLibProcessMessageType.GET_CONNECTION_SECURITY_PARAMETERS_REQUEST:
                            connection_handle, _, connection = _get_connection_in_cache_from_args(
                                args_tuple=args,
                                connection_handle_index=GetConnectionSecurityParametersRequestArgsInd.CONNECTION_HANDLE)

                            security_parameters = connection.security_parameters()
                            await response_queue.coro_put(
                                (REQUEST_TO_RESPONSE[request], (connection_handle, security_parameters)))
                        elif request == NrfBleLibProcessMessageType.CHARACTERISTIC_WRITE_REQUEST:
                            connection_handle, _, connection = _get_connection_in_cache_from_args(
                                args_tuple=args,
                                connection_handle_index=CharacteristicWriteRequestArgsInd.CONNECTION_HANDLE)

                            characteristic = args[CharacteristicWriteRequestArgsInd.CHARACTERISTIC]
                            characteristic_write = args[
                                CharacteristicWriteRequestArgsInd.CHARACTERISTIC_WRITE_OPERATION]
                            if isinstance(characteristic_write, WriteOperation):
                                characteristic_write = characteristic_write.value
                            # end if
                            data_to_write = args[CharacteristicWriteRequestArgsInd.DATA_TO_WRITE]

                            await connection.write_characteristic(characteristic, data_to_write, characteristic_write)

                            await response_queue.coro_put(
                                (REQUEST_TO_RESPONSE[request],
                                 (connection_handle, characteristic, args[
                                     CharacteristicWriteRequestArgsInd.CHARACTERISTIC_WRITE_OPERATION], data_to_write)))
                        elif request == NrfBleLibProcessMessageType.UPDATE_GATT_TABLE_REQUEST:
                            gatt_db_setup = NrfBleLibStructureTranslator.get_driver_gatt_db_setup(
                                interface_gatt_table=args[
                                    AddServiceToCentralGattTableRequestArgsInd.GATT_DB_SETUP])

                            gatt_db = ble_adapter.gatt_db()
                            gatt_db.apply_db_setup(gatt_db_setup)

                            await response_queue.coro_put((REQUEST_TO_RESPONSE[request], tuple()))
                        elif request == NrfBleLibProcessMessageType.CHARACTERISTIC_READ_REQUEST:
                            connection_handle, _, connection = _get_connection_in_cache_from_args(
                                args_tuple=args,
                                connection_handle_index=CharacteristicReadRequestArgsInd.CONNECTION_HANDLE)

                            characteristic = args[CharacteristicReadRequestArgsInd.CHARACTERISTIC]
                            read_operation = args[CharacteristicReadRequestArgsInd.READ_OPERATION]
                            if isinstance(read_operation, ReadOperation):
                                read_operation = read_operation.value
                            # end if

                            # TODO verify value type
                            value = await connection.read_characteristic(
                                characteristic=characteristic, read_operation=read_operation)

                            await response_queue.coro_put(
                                (REQUEST_TO_RESPONSE[request], (connection_handle, characteristic, args[
                                     CharacteristicWriteRequestArgsInd.CHARACTERISTIC_WRITE_OPERATION], value)))
                        elif request == NrfBleLibProcessMessageType.DESCRIPTOR_READ_REQUEST:
                            connection_handle, _, connection = _get_connection_in_cache_from_args(
                                args_tuple=args,
                                connection_handle_index=DescriptorReadRequestArgsInd.CONNECTION_HANDLE)

                            descriptor = args[DescriptorReadRequestArgsInd.DESCRIPTOR]
                            read_operation = args[DescriptorReadRequestArgsInd.READ_OPERATION]
                            if isinstance(read_operation, ReadOperation):
                                read_operation = read_operation.value
                            # end if

                            # TODO verify value type
                            value = await connection.read_descriptor(
                                descriptor=descriptor, read_operation=read_operation)

                            await response_queue.coro_put(
                                (REQUEST_TO_RESPONSE[request], (connection_handle, descriptor, args[
                                     CharacteristicWriteRequestArgsInd.CHARACTERISTIC_WRITE_OPERATION], value)))
                        elif request == NrfBleLibProcessMessageType.SET_NOTIFICATION_STATUS_REQUEST:
                            connection_handle, address, connection = _get_connection_in_cache_from_args(
                                    args_tuple=args,
                                    connection_handle_index=(
                                        SetNotificationStatusRequestArgsInd.CONNECTION_HANDLE))
                            status = args[SetNotificationStatusRequestArgsInd.NOTIFICATION_STATUS]
                            characteristic = args[SetNotificationStatusRequestArgsInd.CHARACTERISTIC]

                            if status:
                                await connection.subscribe_to_characteristic_notifications(
                                    characteristic=characteristic)
                            else:
                                await connection.stop_subscription(characteristic=characteristic)
                            # end if

                            await response_queue.coro_put(
                                (REQUEST_TO_RESPONSE[request], (connection_handle, characteristic, status)))
                        elif request == NrfBleLibProcessMessageType.SET_INDICATION_STATUS_REQUEST:
                            connection_handle, address, connection = _get_connection_in_cache_from_args(
                                    args_tuple=args,
                                    connection_handle_index=SetIndicationStatusRequestArgsInd.CONNECTION_HANDLE)
                            status = args[SetNotificationStatusRequestArgsInd.NOTIFICATION_STATUS]
                            characteristic = args[SetNotificationStatusRequestArgsInd.CHARACTERISTIC]

                            if status:
                                await connection.subscribe_to_characteristic_indications(
                                    characteristic=characteristic)
                            else:
                                await connection.stop_subscription(characteristic=characteristic)
                            # end if

                            await response_queue.coro_put(
                                (REQUEST_TO_RESPONSE[request], (connection_handle, characteristic, status)))
                        elif request == NrfBleLibProcessMessageType.GET_CENTRAL_ADDRESS_REQUEST:
                            address = ble_adapter.address()
                            await response_queue.coro_put((REQUEST_TO_RESPONSE[request], (address,)))
                        elif request == NrfBleLibProcessMessageType.SET_CONNECTION_PARAMETERS_RANGE_REQUEST:
                            connection_parameter_range = \
                                NrfBleLibStructureTranslator.get_driver_connection_parameters_range(
                                    interface_connection_parameters_range=(
                                        args[SetConnectionParametersRangeRequestArgsInd.RANGE]))
                            await ble_adapter.set_accepted_connection_parameter_range_for_update_requests(
                                connection_parameter_range)
                            await response_queue.coro_put((REQUEST_TO_RESPONSE[request], (
                                args[SetConnectionParametersRangeRequestArgsInd.RANGE],)))
                        # end if

                        # Reset the consecutive exception count because no exceptions arise for this request
                        consecutive_other_exception_count = 0
                    except TransportContextException as transport_context_exception:
                        error_code = ErrorId.TRANSPORT_CONTEXT_EXCEPTION + transport_context_exception.get_cause()
                        error_event_arguments = (request, args, error_code)
                        error_message = transport_context_exception.get_message()
                        if len(error_message) > 0:
                            error_event_arguments += (error_message,)
                        # end if
                        if run:
                            if VERBOSE_ERROR:
                                stdout.write("Request Task raised an exception inside the run loop: "
                                             f"{TracebackLogWrapper.get_exception_stack()}\n")
                            # end if
                            await response_queue.coro_put(
                                (NrfBleLibProcessMessageType.ERROR_RESPONSE, error_event_arguments))
                        else:
                            if VERBOSE_ERROR:
                                stdout.write("Request Task Finished in a raise condition inside the run loop: "
                                             f"{TracebackLogWrapper.get_exception_stack()}\n")
                            # end if
                            await response_queue.coro_put(
                                (NrfBleLibProcessMessageType.CRITICAL_ERROR_RESPONSE, error_event_arguments))
                            raise
                        # end if
                    except NrfblError as nrf_ble_lib_error:
                        if nrf_ble_lib_error.args[0] == "InsufficientAuthentication":
                            error_code = ErrorId.TRANSPORT_CONTEXT_EXCEPTION + \
                                         TransportContextException.Cause.INSUFFICIENT_AUTHENTICATION
                            error_event_arguments = (request, args, error_code)
                            error_message = nrf_ble_lib_error.args[1:]
                        elif nrf_ble_lib_error.args[0] == "HciDisconnectReceived":
                            error_code = ErrorId.TRANSPORT_CONTEXT_EXCEPTION + \
                                         TransportContextException.Cause.DEVICE_DISCONNECTION_DURING_OPERATION
                            error_event_arguments = (request, args, error_code)
                            error_message = nrf_ble_lib_error.args[1:]
                        elif nrf_ble_lib_error.args[0] == "Disconnected":
                            error_code = ErrorId.TRANSPORT_CONTEXT_EXCEPTION + \
                                         TransportContextException.Cause.DEVICE_NOT_CONNECTED
                            error_event_arguments = (request, args, error_code)
                            error_message = nrf_ble_lib_error.args[1:]
                        else:
                            error_event_arguments = (request, args, ErrorId.OTHER_EXCEPTIONS)
                            error_message = str(nrf_ble_lib_error)
                        # end if
                        if len(error_message) > 0:
                            error_event_arguments += (error_message,)
                        # end if
                        if run:
                            if VERBOSE_ERROR:
                                stdout.write("Request Task raised an exception inside the run loop: "
                                             f"{TracebackLogWrapper.get_exception_stack()}\n")
                            # end if
                            await response_queue.coro_put(
                                (NrfBleLibProcessMessageType.ERROR_RESPONSE, error_event_arguments))
                        else:
                            if VERBOSE_ERROR:
                                stdout.write("Request Task Finished in a raise condition inside the run loop: "
                                             f"{TracebackLogWrapper.get_exception_stack()}\n")
                            # end if
                            await response_queue.coro_put(
                                (NrfBleLibProcessMessageType.CRITICAL_ERROR_RESPONSE, error_event_arguments))
                            raise
                        # end if
                    except CancelledError:
                        raise
                    except Exception as other_exception:
                        consecutive_other_exception_count += 1
                        error_event_arguments = (request, args, ErrorId.OTHER_EXCEPTIONS)
                        error_message = str(other_exception)
                        if len(error_message) > 0:
                            error_event_arguments += (error_message,)
                        # end if
                        if run and consecutive_other_exception_count <= cls.PROCESS_CONSECUTIVE_ERROR_MAX_COUNT:
                            if VERBOSE_ERROR:
                                stdout.write("Request Task raised an exception inside the run loop: "
                                             f"{TracebackLogWrapper.get_exception_stack()}\n")
                            # end if
                            await response_queue.coro_put(
                                (NrfBleLibProcessMessageType.ERROR_RESPONSE, error_event_arguments))
                        else:
                            if VERBOSE_ERROR:
                                stdout.write("Request Task Finished in a raise condition inside the run loop: "
                                             f"{TracebackLogWrapper.get_exception_stack()}\n")
                            # end if
                            await response_queue.coro_put(
                                (NrfBleLibProcessMessageType.CRITICAL_ERROR_RESPONSE, error_event_arguments))
                            raise
                        # end if
                    # end try
                # end while
            except CancelledError:
                if VERBOSE:
                    stdout.write("Request Task canceled\n")
                # end if
                await _clean_stop()
            except Exception:
                if VERBOSE_ERROR:
                    stdout.write("Request Task Finished in a raise condition outside the run loop: "
                                 f"{TracebackLogWrapper.get_exception_stack()}\n")
                # end if
                await _clean_stop()
            else:
                if VERBOSE:
                    stdout.write("Request Task Finished\n")
                # end if
            # end try
        # end def _async_request_treatment_task

        request_task = asyncio_loop.create_task(_async_request_treatment_task())
        asyncio_loop.run_until_complete(wait([request_task, event_task]))

        if VERBOSE:
            stdout.write("Close nrf-ble-lib process\n")
        # end if
    # end def _run_nrf_ble_lib_process

    def _clear_process_queues(self):
        """
        Clear all messages in the process queues
        """
        for queue in [self._request_queue, self._response_queue, self._event_queue]:
            cleaning = True
            while cleaning:
                try:
                    queue.get_nowait()
                except Empty:
                    cleaning = False
                # end try
            # end while
        # end for
    # end def _clear_process_queues

    def start_process(self):
        """
        Start the nrf-ble-lib process. The request/event queues are cleared at the beginning of this method.

        :raise ``TransportContextException``: If the process is already running
        """
        if self.is_process_alive():
            raise TransportContextException(TransportContextException.Cause.CONTEXT_INTERNAL_ERROR,
                                            f"The nrf-ble-lib process is already running")
        # end if

        self._clear_process_queues()

        if VERBOSE:
            stdout.write(f"Main process PID = {getpid()}\n")
        # end if

        self._nrf_ble_lib_process = AioProcess(
            target=type(self)._run_nrf_ble_lib_process,
            args=(self._com_port, self._request_queue, self._response_queue, self._event_queue))
        self._nrf_ble_lib_process.start()
        sched_setscheduler(self._nrf_ble_lib_process.pid, SCHED_RR, sched_param(sched_get_priority_max(SCHED_RR) - 1))
    # end def start_process

    def stop_process(self):
        """
        Stop the nrf-ble-lib process. The request/event queues are cleared at the end of this method.
        """
        if not self.is_process_alive():
            return
        # end if

        try:
            # TODO add error treatment
            self.send_request_wait_for_response(request_type=NrfBleLibProcessMessageType.STOP_REQUEST)
            self._nrf_ble_lib_process.join(timeout=NrfBleLibAsyncioProcess.BLOCKING_DEFAULT_TIMEOUT)
        finally:
            if self._nrf_ble_lib_process.is_alive():
                if VERBOSE:
                    stdout.write("nrf-ble-lib process had to be killed\n")
                # end if
                self._nrf_ble_lib_process.kill()
            # end if
            self._clear_process_queues()
            self._nrf_ble_lib_process = None
        # end try
    # end def stop_process

    def is_process_alive(self):
        """
        Check if the nrf-ble-lib process is alive. If the process is not alive, it will clear the request/event queues.

        :return: Flag indicating that the process is alive or not
        :rtype: ``bool``
        """
        if self._nrf_ble_lib_process is None or not self._nrf_ble_lib_process.is_alive():
            self._clear_process_queues()
            self._nrf_ble_lib_process = None
            return False
        else:
            return True
        # end if
    # end def is_process_alive

    def send_request_wait_for_response(self, request_type, request_arguments=tuple(), timeout=BLOCKING_DEFAULT_TIMEOUT):
        """
        send a request to the process then wait for the response

        :param request_type: the type of the request
        :type request_type: ``NrfBleLibProcessMessageType``
        :param request_arguments: the arguments of the response - Optional
        :type request_arguments: ``tuple``
        :param timeout: timeout of the request in second - Optional
        :type timeout: ``float``

        :return: the response
        :rtype: ``tuple``
        """
        self._request_queue.put((request_type, request_arguments))

        response_type = REQUEST_TO_RESPONSE[request_type]

        star_time = time()
        response = self._response_queue.get(timeout=timeout)
        while self.get_message_type(message=response) != response_type and \
                (self.get_message_type(message=response) not in ERROR_TYPES or
                 self.get_message_type_associated_with_error(error=response) != request_type):
            if VERBOSE:
                stdout.write(f"Unknown response received while waiting for {response_type.name}: {response}\n")
            # end if
            new_timeout = timeout - (time() - star_time)
            if new_timeout <= 0:
                raise Empty
            # end if
            response = self._response_queue.get(timeout=new_timeout)
        # end while

        return response
    # end def send_request_wait_for_response

    def send_request(self, request_type, request_arguments=tuple()):
        """
        Send a request without waiting for the response

        :param request_type: the type of the request
        :type request_type: ``NrfBleLibProcessMessageType``
        :param request_arguments: the arguments of the response - Optional
        :type request_arguments: ``tuple``

        :return: The expected Response type
        :rtype: ``NrfBleLibProcessMessageType``
        """
        self._request_queue.put((request_type, request_arguments))
    # end def send_request

    def get_response(self, original_request_type, timeout=BLOCKING_DEFAULT_TIMEOUT):
        """
        Return the corresponding response for a request previously sent

        :param original_request_type: the type of the previous request
        :type original_request_type: ``NrfBleLibProcessMessageType``
        :param timeout: timeout to wait, starting on this method call
        :type timeout: ``float``

        :return: response obtained
        :rtype: ``tuple``

        :raise: ``Empty`` if no response found during allowed time
        """

        response_type = REQUEST_TO_RESPONSE[original_request_type]
        response = self._response_queue.get(timeout=timeout)
        star_time = time()
        while self.get_message_type(message=response) != response_type and \
                (self.get_message_type(message=response) not in ERROR_TYPES or
                 self.get_message_type_associated_with_error(error=response) != original_request_type):
            if VERBOSE:
                stdout.write(f"Unknown response received while waiting for {response_type}: {response}\n")
            # end if
            new_timeout = timeout - (time() - star_time)
            if new_timeout <= 0:
                raise Empty
            # end if
            response = self._response_queue.get(timeout=new_timeout)
        # end while

        return response
    # end def get_response

    def wait_for_event(self, timeout):
        """
        Wait for an event

        :param timeout: Timeout in seconds to get the event
        :type timeout: ``int`` or ``float``

        :return: The event gotten
        :rtype: ``tuple``
        """
        return self._event_queue.get(timeout=timeout)
    # end def wait_for_event

    @staticmethod
    def get_message_type(message):
        """
        Get the message type inside a message tuple

        :param message: Message tuple
        :type message: ``tuple``

        :return: The message type
        :rtype: ``NrfBleLibProcessMessageType``
        """
        assert message[0] in NrfBleLibProcessMessageType, "Not a message type"

        return NrfBleLibProcessMessageType(message[0])
    # end def get_message_type

    @staticmethod
    def get_message_arguments(message):
        """
        Get the message arguments inside a message tuple

        :param message: Message tuple
        :type message: ``tuple``

        :return: The message arguments
        :rtype: ``tuple``
        """
        return message[1]
    # end def get_message_arguments

    @staticmethod
    def get_message_type_associated_with_error(error):
        """
        Get the message type inside an error argument tuple

        :param error: Error tuple
        :type error: ``tuple``

        :return: The message type associated with the error
        :rtype: ``NrfBleLibProcessMessageType``
        """
        # Sanity check
        assert error[0] in ERROR_TYPES, "Not an error"
        assert error[1][0] in NrfBleLibProcessMessageType, "Not a message type"

        return NrfBleLibProcessMessageType(error[1][0])
    # end def get_message_type_associated_with_error
# end class NrfBleLibAsyncioProcess

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
