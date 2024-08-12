#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytransport.ble.nrfblelibblecontext.nrfblelibconstants
:brief: Define the Constants of nrf-ble-lib.
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2023/05/30
"""
# ----------------------------------------------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------------------------------------------
from enum import Enum
from enum import IntEnum
from enum import auto

from pylibrary.tools.util import ContainsEnumMeta
from pylibrary.tools.util import ContainsIntEnumMeta


# ----------------------------------------------------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------------------------------------------------
class IoCapability(Enum, metaclass=ContainsEnumMeta):
    """
    GAP IO Capabilities to use with ``Adapter.sm_set_io_capabilities``.
    """
    DISPLAY_ONLY = "display_only"
    DISPLAY_YES_NO = "display_yes_no"
    KEYBOARD_ONLY = "keyboard_only"
    NO_INPUT_NO_OUTPUT = "no_input_no_output"
    KEYBOARD_DISPLAY = "keyboard_display"
# end class IoCapability


class WriteOperation(Enum, metaclass=ContainsEnumMeta):
    """
    Write operation to use with ``Connection.write_characteristic``.
    """
    AUTOMATIC = "automatic"
    WRITE_REQUEST = "write_request"
    WRITE_COMMAND = "write_command"
    WRITE_LONG = "write_long"
# end class WriteOperation


class ReadOperation(Enum, metaclass=ContainsEnumMeta):
    """
    Read operation to use with ``Connection.read_characteristic``.
    """
    READ = "read"
    READ_LONG = "read_long"
# end class ReadOperation


class NrfBleLibProcessMessageType(IntEnum):
    """
    Requests, responses, and events types for and from the nrf-ble-lib process.
    Format of a message: ``tuple[NrfBleLibProcessMessageType, tuple[arguments]]``.

    |

    Arguments for each request:

    * STOP_REQUEST has no arguments, so it should have an empty tuple as arguments
    * SCAN_REQUEST arguments: The scan parameters, scan filters and scan timeout
    * SCAN_STOP_REQUEST has no arguments, so it should have an empty tuple as arguments
    * CONNECT_REQUEST arguments: device address as a ``dict`` with the address string and type
      (see ``NrfBleLibStructureTranslator.get_driver_ble_gap_address``), and optionally the connection parameters
    * DISCONNECT_REQUEST arguments: nrf-ble-lib connection handle in nrf-ble-lib process internal cache
    * PERFORM_SERVICE_DISCOVERY_REQUEST arguments: nrf-ble-lib connection handle in nrf-ble-lib process internal cache
    * PAIR_REQUEST arguments: nrf-ble-lib connection handle in nrf-ble-lib process internal cache, IO capabilities
      (see ``IoCapability``), and authentication requirements
    * DELETE_BOND_REQUEST arguments: device address as a ``dict`` with the address string and type
    * UPDATE_CONNECTION_PARAMETERS_REQUEST arguments: nrf-ble-lib connection handle in nrf-ble-lib process internal
      cache, and the new connection parameters
    * GET_CONNECTION_SECURITY_PARAMETERS_REQUEST arguments: nrf-ble-lib connection handle in nrf-ble-lib process
      internal cache
    * CHARACTERISTIC_WRITE_REQUEST arguments: nrf-ble-lib connection handle in nrf-ble-lib process internal
      cache, the characteristic to use, the write operation (see ``WriteOperation``), and the data to write
    * UPDATE_GATT_TABLE_REQUEST arguments: Service to add
    * CHARACTERISTIC_READ_REQUEST arguments: nrf-ble-lib connection handle in nrf-ble-lib process internal cache, the
      characteristic to use, and the read operation (see ``ReadOperation``)
    * DESCRIPTOR_READ_REQUEST arguments: nrf-ble-lib connection handle in nrf-ble-lib process internal cache, the
      descriptor to use, and the read operation (see ``ReadOperation``)
    * SET_NOTIFICATION_STATUS_REQUEST arguments: nrf-ble-lib connection handle in nrf-ble-lib process internal cache,
      the characteristic to use, the status to set
    * SET_INDICATION_STATUS_REQUEST arguments: nrf-ble-lib connection handle in nrf-ble-lib process internal cache,
      the characteristic to use, the status to set
    * GET_CENTRAL_ADDRESS_REQUEST has no arguments, so it should have an empty tuple as arguments
    * SET_CONNECTION_PARAMETERS_RANGE_REQUEST arguments: wanted range as a ``BleGapConnectionParametersRange``

    |

    Arguments for each response:

    * STOP_RESPONSE has no arguments, so it should have an empty tuple as arguments
    * SCAN_RESPONSE arguments: device scanned dictionary of their address mapped to a list of their advertising type,
      advertising data, list of advertising timestamp, scan response (``None`` if no scan response) and list of scan
      response timestamp (``None`` if no scan response)
    * SCAN_STOP_RESPONSE has no arguments, so it should have an empty tuple as arguments
    * CONNECT_RESPONSE arguments: device address as a ``dict`` with the address string and type
      (see ``NrfBleLibStructureTranslator.get_driver_ble_gap_address``) and nrf-ble-lib connection handle in
      nrf-ble-lib process internal cache
    * DISCONNECT_RESPONSE arguments: device address as a ``dict`` with the address string and type
      (see ``NrfBleLibStructureTranslator.get_driver_ble_gap_address``), If None, it means that the disconnect
      already occurred.
    * PERFORM_SERVICE_DISCOVERY_RESPONSE arguments: the discovered gatt table as a list of ``BleService``
    * PAIR_RESPONSE has no arguments, so it should have an empty tuple as arguments
    * DELETE_BOND_RESPONSE has no arguments, so it should have an empty tuple as arguments
    * UPDATE_CONNECTION_PARAMETERS_RESPONSE has no arguments, so it should have an empty tuple as arguments
    * GET_CONNECTION_SECURITY_PARAMETERS_RESPONSE arguments: nrf-ble-lib connection handle in nrf-ble-lib process
      internal cache, its connection security parameters
    * CHARACTERISTIC_WRITE_RESPONSE arguments: nrf-ble-lib connection handle in nrf-ble-lib process internal
      cache, the characteristic used, the write operation (see ``WriteOperation``), and the data written
    * UPDATE_GATT_TABLE_REQUEST has no arguments, so it should have an empty tuple as arguments
    * CHARACTERISTIC_READ_RESPONSE arguments: nrf-ble-lib connection handle in nrf-ble-lib process internal cache, the
      characteristic used, the read operation (see ``ReadOperation``), and the data read
    * DESCRIPTOR_READ_RESPONSE arguments: nrf-ble-lib connection handle in nrf-ble-lib process internal cache, the
      descriptor used, the read operation (see ``ReadOperation``), and the data read
    * SET_NOTIFICATION_STATUS_RESPONSE arguments: nrf-ble-lib connection handle in nrf-ble-lib process internal cache,
      the characteristic used, the status set
    * SET_INDICATION_STATUS_RESPONSE arguments: nrf-ble-lib connection handle in nrf-ble-lib process internal cache,
      the characteristic used, the status set
    * GET_CENTRAL_ADDRESS_RESPONSE arguments: device address as a ``dict`` with the address string and type
    * SET_CONNECTION_PARAMETERS_RANGE_RESPONSE arguments: used range as a ``BleGapConnectionParametersRange``

    |

    Arguments for each error response:

    * ERROR_RESPONSE arguments: the concerned request, its arguments, the error code (See ErrorId for format), and
      optionally a string
    * CRITICAL_ERROR_RESPONSE arguments are the same as ERROR_RESPONSE, this response just mean that the process is
      stopped by it

    |

    Arguments for each event:

    * NRF_BLE_LIB_EVENT arguments: nrf-ble-lib event as a ``dict`` (see nrf-ble-lib spec for format)
    * NOTIFICATION_EVENT arguments: nrf-ble-lib connection handle in nrf-ble-lib process internal cache, characteristic
      used, data received, and its timestamp
    * INDICATION_EVENT arguments: nrf-ble-lib connection handle in nrf-ble-lib process internal cache, characteristic
      used, data received, and its timestamp
    * L2CAP_CONNECTION_PARAMETER_UPDATE_REQUEST_EVENT arguments: nrf-ble-lib event data as a ``dict`` (see nrf-ble-lib
      spec for format), the event timestamp, and if it is accepted or not
    * ERROR_EVENT arguments: the concerned event, its arguments (for NRF_BLE_LIB_EVENT, only the event type is added
      there because the arguments could be triggering the error), the error code (See ErrorId for format), and
      optionally a string
    * CRITICAL_ERROR_EVENT arguments are the same as ERROR_EVENT, this event just mean that the process is stopped by it
    * LOG_EVENT arguments: log level (see pylibrary.system.tracelogger.TraceLevel) and log message
    """
    # Requests
    STOP_REQUEST = 0
    SCAN_REQUEST = auto()
    SCAN_STOP_REQUEST = auto()
    CONNECT_REQUEST = auto()
    DISCONNECT_REQUEST = auto()
    PERFORM_SERVICE_DISCOVERY_REQUEST = auto()
    PAIR_REQUEST = auto()
    DELETE_BOND_REQUEST = auto()
    UPDATE_CONNECTION_PARAMETERS_REQUEST = auto()
    GET_CONNECTION_SECURITY_PARAMETERS_REQUEST = auto()
    CHARACTERISTIC_WRITE_REQUEST = auto()
    UPDATE_GATT_TABLE_REQUEST = auto()
    CHARACTERISTIC_READ_REQUEST = auto()
    DESCRIPTOR_READ_REQUEST = auto()
    SET_NOTIFICATION_STATUS_REQUEST = auto()
    SET_INDICATION_STATUS_REQUEST = auto()
    GET_CENTRAL_ADDRESS_REQUEST = auto()
    SET_CONNECTION_PARAMETERS_RANGE_REQUEST = auto()  # TODO: add get request/response

    # Response
    STOP_RESPONSE = auto()
    SCAN_RESPONSE = auto()
    SCAN_STOP_RESPONSE = auto()
    CONNECT_RESPONSE = auto()
    DISCONNECT_RESPONSE = auto()
    PERFORM_SERVICE_DISCOVERY_RESPONSE = auto()
    PAIR_RESPONSE = auto()
    DELETE_BOND_RESPONSE = auto()
    UPDATE_CONNECTION_PARAMETERS_RESPONSE = auto()
    GET_CONNECTION_SECURITY_PARAMETERS_RESPONSE = auto()
    CHARACTERISTIC_WRITE_RESPONSE = auto()
    UPDATE_GATT_TABLE_RESPONSE = auto()
    CHARACTERISTIC_READ_RESPONSE = auto()
    DESCRIPTOR_READ_RESPONSE = auto()
    SET_NOTIFICATION_STATUS_RESPONSE = auto()
    SET_INDICATION_STATUS_RESPONSE = auto()
    GET_CENTRAL_ADDRESS_RESPONSE = auto()
    SET_CONNECTION_PARAMETERS_RANGE_RESPONSE = auto()

    # Error response
    ERROR_RESPONSE = auto()
    CRITICAL_ERROR_RESPONSE = auto()

    # Events
    NRF_BLE_LIB_EVENT = auto()
    NOTIFICATION_EVENT = auto()
    INDICATION_EVENT = auto()
    L2CAP_CONNECTION_PARAMETER_UPDATE_REQUEST_EVENT = auto()
    PAIRED_EVENT = auto()
    ERROR_EVENT = auto()
    CRITICAL_ERROR_EVENT = auto()
    LOG_EVENT = auto()
# end class NrfBleLibProcessMessageType


class ScanStartRequestArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.SCAN_REQUEST``.
    """
    SCAN_PARAMETERS = 0
    SCAN_FILTERS = auto()
    SCAN_TIMEOUT = auto()
# end class ScanStartRequestArgsInd


class ConnectRequestArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.CONNECT_REQUEST``.
    """
    DEVICE_ADDRESS = 0
    CONNECTION_PARAMETERS = auto()
# end class ConnectRequestArgsInd


class DisconnectRequestArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.DISCONNECT_REQUEST``.
    """
    CONNECTION_HANDLE = 0
# end class DisconnectRequestArgsInd


class PerformServiceDiscoveryRequestArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.PERFORM_SERVICE_DISCOVERY_REQUEST``.
    """
    CONNECTION_HANDLE = 0
# end class PerformServiceDiscoveryRequestArgsInd


class PairRequestArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.PAIR_REQUEST``.
    """
    CONNECTION_HANDLE = 0
    IO_CAPABILITIES = auto()
    AUTHENTICATION_REQUIREMENTS = auto()
    ASYNC = auto()
# end class PairRequestArgsInd


class DeleteBondRequestArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.DELETE_BOND_REQUEST``.
    """
    DEVICE_ADDRESS = 0
# end class DeleteBondRequestArgsInd


class UpdateConnectionParametersRequestArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.UPDATE_CONNECTION_PARAMETERS_REQUEST``.
    """
    CONNECTION_HANDLE = 0
    CONNECTION_PARAMETERS = auto()
# end class UpdateConnectionParametersRequestArgsInd


class GetConnectionSecurityParametersRequestArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.GET_CONNECTION_SECURITY_PARAMETERS_REQUEST``.
    """
    CONNECTION_HANDLE = 0
# end class GetConnectionSecurityParametersRequestArgsInd


class CharacteristicWriteRequestArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.CHARACTERISTIC_WRITE_REQUEST``.
    """
    CONNECTION_HANDLE = 0
    CHARACTERISTIC = auto()
    CHARACTERISTIC_WRITE_OPERATION = auto()
    DATA_TO_WRITE = auto()
# end class CharacteristicWriteRequestArgsInd


class AddServiceToCentralGattTableRequestArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.ADD_SERVICE_TO_CENTRAL_GATT_TABLE_REQUEST``.
    """
    GATT_DB_SETUP = 0
# end class AddServiceToCentralGattTableRequestArgsInd


class CharacteristicReadRequestArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.CHARACTERISTIC_READ_REQUEST``.
    """
    CONNECTION_HANDLE = 0
    CHARACTERISTIC = auto()
    READ_OPERATION = auto()
# end class CharacteristicReadRequestArgsInd


class DescriptorReadRequestArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.DESCRIPTOR_READ_REQUEST``.
    """
    CONNECTION_HANDLE = 0
    DESCRIPTOR = auto()
    READ_OPERATION = auto()
# end class DescriptorReadRequestArgsInd


class SetNotificationStatusRequestArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.SET_NOTIFICATION_STATUS_REQUEST``.
    """
    CONNECTION_HANDLE = 0
    CHARACTERISTIC = auto()
    NOTIFICATION_STATUS = auto()
# end class SetNotificationStatusRequestArgsInd


class SetIndicationStatusRequestArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.SET_INDICATION_STATUS_REQUEST``.
    """
    CONNECTION_HANDLE = 0
    CHARACTERISTIC = auto()
    INDICATION_STATUS = auto()
# end class SetIndicationStatusRequestArgsInd


class SetConnectionParametersRangeRequestArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.SET_CONNECTION_PARAMETERS_RANGE_REQUEST``.
    """
    RANGE = 0
# end class SetConnectionParametersRangeRequestArgsInd


class ScanStartResponseArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.SCAN_RESPONSE``.
    """
    DEVICE_SCANNED_DICT = 0
# end class ScanStartResponseArgsInd


class PerformServiceDiscoveryResponseArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.PERFORM_SERVICE_DISCOVERY_RESPONSE``.
    """
    GATT_TABLE = 0
# end class PerformServiceDiscoveryResponseArgsInd


class GetConnectionSecurityParametersResponseArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.GET_CONNECTION_SECURITY_PARAMETERS_RESPONSE``.
    """
    CONNECTION_HANDLE = 0
    CONNECTION_SECURITY_PARAMETERS = auto()
# end class GetConnectionSecurityParametersResponseArgsInd


class CharacteristicWriteResponseArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.CHARACTERISTIC_WRITE_RESPONSE``.
    """
    CONNECTION_HANDLE = 0
    CHARACTERISTIC = auto()
    CHARACTERISTIC_WRITE_OPERATION = auto()
    DATA_TO_WRITE = auto()
# end class CharacteristicWriteResponseArgsInd


class CharacteristicReadResponseArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.CHARACTERISTIC_READ_RESPONSE``.
    """
    CONNECTION_HANDLE = 0
    CHARACTERISTIC = auto()
    READ_OPERATION = auto()
    DATA_READ = auto()
# end class CharacteristicReadResponseArgsInd


class DescriptorReadResponseArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.DESCRIPTOR_READ_RESPONSE``.
    """
    CONNECTION_HANDLE = 0
    DESCRIPTOR = auto()
    READ_OPERATION = auto()
    DATA_READ = auto()
# end class DescriptorReadResponseArgsInd


class GetCentralAddressResponseArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.GET_CENTRAL_ADDRESS_RESPONSE``.
    """
    CENTRAL_ADDRESS = 0
# end class GetCentralAddressResponseArgsInd


class SetConnectionParametersRangeResponseArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.SET_CONNECTION_PARAMETERS_RANGE_RESPONSE``.
    """
    RANGE = 0
# end class SetConnectionParametersRangeResponseArgsInd


class NrfBleLibEventArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.NRF_BLE_LIB_EVENT``.
    """
    NRF_BLE_LIB_EVENT = 0
# end class NrfBleLibEventArgsInd


class NotificationEventArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.NOTIFICATION_EVENT``.
    """
    CONNECTION_HANDLE = 0
    CHARACTERISTIC_HANDLE = auto()
    NOTIFICATION_DATA = auto()
    TIMESTAMP = auto()
# end class NotificationEventArgsInd


class IndicationEventArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.INDICATION_EVENT``.
    """
    CONNECTION_HANDLE = 0
    CHARACTERISTIC_HANDLE = auto()
    INDICATION_DATA = auto()
    TIMESTAMP = auto()
# end class IndicationEventArgsInd


class L2capConnectionParameterUpdateRequestEventArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.L2CAP_CONNECTION_PARAMETER_UPDATE_REQUEST_EVENT``.
    """
    EVENT_DATA = 0
    TIMESTAMP = auto()
    ACCEPTED_STATUS = auto()
# end class L2capConnectionParameterUpdateRequestEventArgsInd

class LogEventArgsInd(IntEnum, metaclass=ContainsEnumMeta):
    """
    Argument indexes for ``NrfBleLibProcessMessageType.LOG_EVENT``.
    """
    LOG_LEVEL = 0
    LOG_MESSAGE = auto()
# end class LogEventArgsInd

class ErrorId(IntEnum):
    """
    Error IDs for NrfBleLibProcessCommandEvent.ERROR_EVENT.

    |

    Format of the error on 32 bits: (error ID) << 16 + (error code), error ID should be on 16 bits and error code too
    """
    TRANSPORT_CONTEXT_EXCEPTION = 0x00010000
    OTHER_EXCEPTIONS = 0xFFFF0000
# end class ErrorId


class NrfBleLibConnectionCacheTupleIndex(IntEnum, metaclass=ContainsEnumMeta):
    """
    Indexes in the connection cache tuples
    """
    ADDRESS_INDEX_IN_CACHED_TUPLE = 0
    CONNECTION_INDEX_IN_CACHED_TUPLE = auto()
# end class NrfBleLibConnectionCacheTupleIndex


class NrfBleLibHciOpcode(IntEnum, metaclass=ContainsEnumMeta):
    """
    HCI opcode as defined in nrf-ble-lib/btstack-sys/btstack/src/hci_cmd.h
    """
    LE_REMOTE_CONNECTION_PARAMETER_REQUEST_REPLY = 0x2020
    LE_REMOTE_CONNECTION_PARAMETER_REQUEST_NEGATIVE_REPLY = 0x2021
    LE_SET_SCAN_ENABLE = 0x200C
# end class NrfBleLibHciOpcode


class DeviceAdvertisingInformationIndex(IntEnum, metaclass=ContainsIntEnumMeta):
    """
    Indexes for the information in the list for each device returned by the scan procedure
    """
    ADVERTISING_TYPE = 0
    ADVERTISING_DATA = auto()
    ADVERTISING_TIMESTAMPS = auto()
    SCAN_RESPONSE_DATA = auto()
    SCAN_RESPONSE_TIMESTAMPS = auto()
# end class DeviceAdvertisingInformationIndex


class NrfBleLibProcessUtil:
    """
    Various util values for the nrf-ble-lib process
    """
    SCAN_START_STOP_TIMEOUT = 1  # in second
# end class NrfBleLibProcessUtil

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
