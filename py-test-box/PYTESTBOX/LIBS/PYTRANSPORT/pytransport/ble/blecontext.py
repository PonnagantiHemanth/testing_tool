#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytransport.ble.blecontext
:brief: BLE context interface classes
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2021/02/18
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from configparser import ConfigParser
from enum import Enum
from enum import auto
from enum import unique
from os import R_OK
from os import access
from os.path import join
from queue import Queue
from threading import Event
from threading import RLock

from xlsxwriter import Workbook

from pylibrary.system.tracelogger import TraceLevel
from pylibrary.tools.threadutils import synchronize_with_object_inner_lock
from pylibrary.tools.util import NotImplementedAbstractMethodError
from pytransport.ble.bleconstants import BleAdvertisingDataType
from pytransport.ble.bleconstants import BleAdvertisingPduType
from pytransport.ble.bleconstants import BleGapAddressType
from pytransport.ble.bleinterfaceclasses import BleAdvertisingData
from pytransport.ble.bleinterfaceclasses import BleDeviceBondingStates
from pytransport.ble.bleinterfaceclasses import BleGapAddress
from pytransport.ble.bleinterfaceclasses import BleGapConnectionParameters
from pytransport.ble.bleinterfaceclasses import BleGapConnectionParametersRange
from pytransport.ble.bleinterfaceclasses import BleGapConnectionSecurityParameters
from pytransport.ble.bleinterfaceclasses import BleService
from pytransport.ble.bleinterfaceclasses import BleUuid
from pytransport.ble.blemessage import BleEventQueue
from pytransport.ble.blemessage import BleMessage
from pytransport.transportcontext import TransportContext
from pytransport.transportcontext import TransportContextDevice

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
# Configure BLE traces verbosity
#  - None: disable all traces (Default)
#  - TraceLevel.ERROR and TraceLevel.WARNING are self explanatory
#  - TraceLevel.INFO: Info level will be used for packets only
#  - TraceLevel.DEBUG: Debug level will be for every context actions
FORCE_AT_CREATION_ALL_BLE_TRACE_LEVEL = None
FORCE_AT_CREATION_ALL_BLE_TRACE_FILE_NAME = None


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
@unique
class BleContextCallbackEvents(Enum):
    """
    Define the possible events that can be used for callbacks in the ble context
    """
    CONNECTION_COMPLETE = auto()
    DISCONNECTION_COMPLETE = auto()
    COMMAND_COMPLETE = auto()
    CONNECTION_UPDATE_COMPLETE = auto()
    NOTIFICATION_EVENT = auto()
    INDICATION_EVENT = auto()
    CONNECTION_UPDATE_REQUEST_EVENT = auto()
# end class BleContextCallbackEvents


class BleContextDevice(TransportContextDevice):
    """
    Class for BLE device used in a BLE context
    """

    def __init__(self, address=None, advertising_type=None, advertising_data=None, scan_response=None, bonded=False,
                 bonding_state=None, connected=False, connection_security_parameters=None, connection_parameters=None,
                 transfer_callbacks=None):
        """
        :param address: The BLE GAP address of the device - OPTIONAL
        :type address: ``BleGapAddress`` or ``None``
        :param advertising_type: Tuple of the advertising type and data - OPTIONAL
        :type advertising_type: ``int`` or ``BleAdvertisingPduType`` or ``None``
        :param advertising_data: List of advertising data, one entry per different packet - OPTIONAL
        :type advertising_data: ``list[BleAdvertisingData]`` or ``None``
        :param scan_response:  list of data in the scan response packet, one entry per different packet - OPTIONAL
        :type scan_response: ``List[BleAdvertisingData]`` or ``None``
        :param bonded: Flag indicating if the device is bonded - OPTIONAL
        :type bonded: ``bool``
        :param bonding_state: Tuple of bonding state and state related data - OPTIONAL
        :type bonding_state: ``tuple[BleDeviceBondingStates, object]`` or ``None``
        :param connected: Flag indicating if the device is connected - OPTIONAL
        :type connected: ``bool``
        :param connection_security_parameters: Connection security parameters, only relevant when connected - OPTIONAL
        :type connection_security_parameters: ``BleGapConnectionSecurityParameters`` or ``None``
        :param connection_parameters: Connection parameters, only relevant when connected - OPTIONAL
        :type connection_parameters: ``BleGapConnectionParameters`` or ``None``
        :param transfer_callbacks: The callbacks that will be used when a transfer is received for each transfer type
                                   (HID mouse, HID keyboard, HID++, etc...), its format is a thread safe dictionary
                                   (the keys are BLE characteristic handles). If ``None``, it will be set as an
                                   empty thread safe dictionary - OPTIONAL
        :type transfer_callbacks: ``RLockedDict`` or ``None``
        """
        super().__init__(connected=connected, transfer_callbacks=transfer_callbacks)

        # Properties
        self._lock_address = RLock()
        self._address = address
        self._lock_advertising_type = RLock()
        self._advertising_type = advertising_type
        self._lock_advertising_data = RLock()
        self._advertising_data = advertising_data
        self._lock_scan_response = RLock()
        self._scan_response = scan_response
        self._lock_bonded = RLock()
        self._bonded = bonded
        self._lock_bonding_state = RLock()
        self._bonding_state = bonding_state if bonding_state is not None else (BleDeviceBondingStates.NO_BONDING, None)
        self._lock_connection_security_parameters = RLock()
        self._connection_security_parameters = connection_security_parameters
        self._lock_connection_parameters = RLock()
        self._connection_parameters = connection_parameters

        # BLE context event queue
        self.ble_context_event_queue = BleEventQueue()

        # This event is used to wait for the device to be scanned
        # It is set when not used
        self.found_device_event = Event()
        self.found_device_event.set()
    # end def __init__

    @property
    @synchronize_with_object_inner_lock("_lock_address")
    def address(self):
        """
        Property getter of ``address``.

        :return: ``address`` object
        :rtype: ``BleGapAddress`` or ``None``
        """
        return self._address
    # end def property getter address

    @address.setter
    @synchronize_with_object_inner_lock("_lock_address")
    def address(self, address):
        """
        Property setter of ``address``.

        :param address: ``address`` object
        :type address: ``BleGapAddress`` or ``None``

        :raise ``AssertionError``: If ``address`` is not a ``BleGapAddress`` or ``None``
        """
        assert isinstance(address, (BleGapAddress, type(None))), \
            f"{self.__class__.__name__} address attribute is a BleGapAddress or None, {address} is neither"
        self._address = address
    # end def property setter address

    @property
    @synchronize_with_object_inner_lock("_lock_advertising_type")
    def advertising_type(self):
        """
        Property getter of ``advertising_type``.

        :return: ``advertising_type`` object
        :rtype: ``int`` or ``BleAdvertisingPduType`` or ``None``
        """
        return self._advertising_type
    # end def property getter advertising_type

    @advertising_type.setter
    @synchronize_with_object_inner_lock("_lock_advertising_type")
    def advertising_type(self, advertising_type):
        """
        Property setter of ``advertising_type``.

        :param advertising_type: ``advertising_type`` object
        :type advertising_type: ``int`` or ``BleAdvertisingPduType`` or ``None``

        :raise ``AssertionError``: If ``advertising_type`` is not an ``int`` nor ``BleAdvertisingPduType`` nor ``None``
        """
        assert isinstance(advertising_type, (int, BleAdvertisingPduType, type(None))), \
            f"{self.__class__.__name__} advertising_type attribute is an int or BleAdvertisingPduType or None, " \
            f"{advertising_type} is neither"
        self._advertising_type = advertising_type
    # end def property setter advertising_type

    @property
    @synchronize_with_object_inner_lock("_lock_advertising_data")
    def advertising_data(self):
        """
        Property getter of ``advertising_data``.

        :return: ``advertising_data`` object
        :rtype: ``list[BleAdvertisingData]`` or ``None``
        """
        return self._advertising_data
    # end def property getter advertising_data

    @advertising_data.setter
    @synchronize_with_object_inner_lock("_lock_advertising_data")
    def advertising_data(self, advertising_data):
        """
        Property setter of ``advertising_data``.

        :param advertising_data: ``advertising_data`` object
        :type advertising_data: ``list[BleAdvertisingData]`` or ``None``

        :raise ``AssertionError``: If ``advertising_data`` is not a ``BleAdvertisingData`` or ``None``
        """
        assert isinstance(advertising_data, (list, type(None))), \
            f"{self.__class__.__name__} advertising_data attribute is a list of BleAdvertisingData or None, " \
            f"{advertising_data} is neither"
        for data in advertising_data:
            assert isinstance(data, (BleAdvertisingData, type(None))), \
                f"{self.__class__.__name__} advertising_data attribute elements is BleAdvertisingData or None, " \
                f"{data} is neither"
        # end for
        self._advertising_data = advertising_data
    # end def property setter advertising_data

    @property
    @synchronize_with_object_inner_lock("_lock_scan_response")
    def scan_response(self):
        """
        Property getter of ``scan_response``.

        :return: ``scan_response`` object
        :rtype: ``list[BleAdvertisingData]`` or ``None``
        """
        return self._scan_response
    # end def property getter scan_response

    @scan_response.setter
    @synchronize_with_object_inner_lock("_lock_scan_response")
    def scan_response(self, scan_response):
        """
        Property setter of ``scan_response``.

        :param scan_response: ``scan_response`` object
        :type scan_response: ``list[BleAdvertisingData]`` or ``None``

        :raise ``AssertionError``: If ``scan_response`` is not a ``BleAdvertisingData`` or ``None``
        """
        assert isinstance(scan_response, (list, type(None))), \
            f"{self.__class__.__name__} scan_response attribute is a list of BleAdvertisingData or None, " \
            f"{scan_response} is neither"
        for data in scan_response:
            assert isinstance(data, (BleAdvertisingData, type(None))), \
                f"{self.__class__.__name__} scan_response attribute elements are BleAdvertisingData or None, " \
                f"{data} is neither"
        # end for
        self._scan_response = scan_response
    # end def property setter scan_response

    @property
    @synchronize_with_object_inner_lock("_lock_bonded")
    def bonded(self):
        """
        Property getter of ``bonded``.

        :return: ``bonded`` value
        :rtype: ``bool``
        """

        return self._bonding_state[0] == BleDeviceBondingStates.BONDED
    # end def property getter bonded

    @bonded.setter
    @synchronize_with_object_inner_lock("_lock_bonded")
    def bonded(self, bonded):
        """
        Property setter of ``bonded``.

        :param bonded: ``bonded`` value
        :type bonded: ``bool``

        :raise ``AssertionError``: If ``bonded`` is not a ``bool``
        """
        assert isinstance(bonded, bool), \
            f"{self.__class__.__name__} bonded attribute is a bool, {bonded} is not"
        self._bonding_state = (BleDeviceBondingStates.BONDED, None) if bonded else \
            (BleDeviceBondingStates.NO_BONDING, None)
    # end def property setter bonded

    @property
    @synchronize_with_object_inner_lock("_lock_bonded")
    def bonding_state(self):
        """
        Property getter of ``bonding_state``.

        :return: ``bonded`` value
        :rtype: ``tuple[BleDeviceBondingStates, object]``
        """
        return self._bonding_state
    # end def property getter bonding_state

    @bonding_state.setter
    @synchronize_with_object_inner_lock("_lock_bonded")
    def bonding_state(self, bonding_state):
        """
        Property setter of ``bonding_state``.

        :param bonding_state: ``bonding_state`` value
        :type bonding_state: ``tuple[BleDeviceBondingStates, object]``

        :raise ``AssertionError``: If ``bonded`` is not a ``tuple`` of the right format
        """
        assert isinstance(bonding_state, tuple), \
            f"{self.__class__.__name__} bonding state attribute is a tuple, {bonding_state} is not"
        assert len(bonding_state) == 2,  (f"{self.__class__.__name__} bonding state attribute is a tuple of length 2,"
                                          f" {bonding_state} is not")
        assert isinstance(bonding_state[0], BleDeviceBondingStates),  \
            (f"{self.__class__.__name__} bonding state attribute is a tuple with a "
             f"``BleDeviceBondingStates`` as a first element, {bonding_state} is not")

        self._bonding_state = bonding_state
    # end def property setter bonding_state

    @property
    @synchronize_with_object_inner_lock("_lock_connection_security_parameters")
    def connection_security_parameters(self):
        """
        Property getter of ``connection_security_parameters``.

        :return: ``connection_security_parameters`` object
        :rtype: ``BleGapConnectionSecurityParameters`` or ``None``
        """
        return self._connection_security_parameters
    # end def property getter connection_security_parameters

    @connection_security_parameters.setter
    @synchronize_with_object_inner_lock("_lock_connection_security_parameters")
    def connection_security_parameters(self, connection_security_parameters):
        """
        Property setter of ``connection_security_parameters``.

        :param connection_security_parameters: ``connection_security_parameters`` object
        :type connection_security_parameters: ``BleGapConnectionSecurityParameters`` or ``None``

        :raise ``AssertionError``: If ``connection_security_parameters`` is not a
                                   ``BleGapConnectionSecurityParameters`` or ``None``
        """
        assert isinstance(connection_security_parameters, (BleGapConnectionSecurityParameters, type(None))), \
            f"{self.__class__.__name__} connection_security_parameters attribute is a " \
            f"BleGapConnectionSecurityParameters or None, {connection_security_parameters} is neither"
        self._connection_security_parameters = connection_security_parameters
    # end def property setter connection_security_parameters

    @property
    @synchronize_with_object_inner_lock("_lock_connection_parameters")
    def connection_parameters(self):
        """
        Property getter of connection_parameters.

        :return: connection_parameters value
        :rtype: ``BleGapConnectionParameters`` or ``None``
        """
        return self._connection_parameters
    # end def property getter connection_parameters

    @connection_parameters.setter
    @synchronize_with_object_inner_lock("_lock_connection_parameters")
    def connection_parameters(self, value):
        """
        Property setter of connection_parameters.

        :param value: connection_parameters value
        :type value: ``BleGapConnectionParameters`` or ``None``

        :raise ``AssertionError``: If ``value`` is not a ``BleGapConnectionParameters``
        """
        assert isinstance(value, (BleGapConnectionParameters, type(None))), \
            f"{self.__class__.__name__} connection_parameters attribute is a BleGapConnectionParameters, " \
            f"{value} is not"
        self._connection_parameters = value
    # end def property setter connection_parameters

    def __repr__(self):
        return f"BLE device:\n\t- address: {self._address}\n\t- advertising type: {self.advertising_type}\n" \
               f"\t- advertising data: {self.advertising_data}\n\t- scan response: {self.scan_response}\n\t- " \
               f"connection parameters requested: {self._connection_parameters}\n"
    # end def __repr__
# end class BleContextDevice


class BleContext(TransportContext):
    """
    This is the definition of the common implementation of a BLE context
    """
    CONFIG_FILE_NAME = "ble_context.ini"  # Name of the configuration file
    BONDING_KEY_PICKLE_FILE_NAME_PREFIX = "ble_bonding_keys_"
    BLOCKING_DEFAULT_TIMEOUT = 5
    GENERIC_SCAN_TIME = 5
    DISCONNECTION_STATE_SYNC_UP = 6
    CHECK_CONNECT_WORKED_TIMEOUT = .5  # TODO: research for the best value
    # Class to use for configuring the class cache, it should be BleContextDevice or its child class
    BLE_CONTEXT_DEVICE_CLASS = BleContextDevice

    def __init__(self, trace_level=TraceLevel.NO_TRACE, trace_file_name=None):
        """
        :param trace_level: Trace level of the transport context - OPTIONAL
        :type trace_level: ``TraceLevel`` or ``int``
        :param trace_file_name: Trace output of the transport context - OPTIONAL
        :type trace_file_name: ``str`` or ``None``
        """
        if FORCE_AT_CREATION_ALL_BLE_TRACE_LEVEL is not None:
            trace_level = FORCE_AT_CREATION_ALL_BLE_TRACE_LEVEL
        # end if

        if FORCE_AT_CREATION_ALL_BLE_TRACE_FILE_NAME is not None:
            trace_file_name = FORCE_AT_CREATION_ALL_BLE_TRACE_FILE_NAME
        # end if

        super().__init__(trace_level=trace_level, trace_file_name=trace_file_name)

        # This range set the accepted parameters for automatic update of the connection parameters when a Connection
        # Parameters Update Request is received from a device, None means all are accepted
        self.__connection_parameter_range = None
        self._lock_connection_parameter_range = RLock()

        self.__display_key_storage = dict()
        self._lock_display_key_storage = RLock()
    # end def __init__

    @property
    @synchronize_with_object_inner_lock("_lock_connection_parameter_range")
    def connection_parameters_range(self):
        """
        Property getter of connection_parameter_range.

        :return: connection_parameter_range value
        :rtype: ``BleGapConnectionParametersRange`` or ``None``
        """
        return self.__connection_parameter_range
    # end def property getter connection_parameters_range

    @connection_parameters_range.setter
    @synchronize_with_object_inner_lock("_lock_connection_parameter_range")
    def connection_parameters_range(self, value):
        """
        Property setter of connection_parameters_range.

        :param value: connection_parameter_range value
        :type value: ``BleGapConnectionParametersRange`` or ``None``

        :raise ``AssertionError``: If ``value`` is not a ``BleGapConnectionParametersRange`` or ``None``
        """
        self._set_connection_parameters_range(value=value)
    # end def property setter connection_parameters_range

    def _set_connection_parameters_range(self, value):
        """
        Internal method for the property setter of connection_parameters_range. This was done to be able to easily
        override it in a child class.

        :param value: connection_parameter_range value
        :type value: ``BleGapConnectionParametersRange`` or ``None``

        :raise ``AssertionError``: If ``value`` is not a ``BleGapConnectionParametersRange`` or ``None``
        """
        assert isinstance(value, BleGapConnectionParametersRange) or value is None, \
            f"{self.__class__.__name__} connection_parameter_range attribute is a ``BleGapConnectionParametersRange``" \
            f" or None, {value} is not"
        self.__connection_parameter_range = value
    # end def _set_connection_parameters_range

    @property
    @synchronize_with_object_inner_lock("_lock_display_key_storage")
    def display_key_storage(self):
        """
        Property getter of connection_parameter_range.

        :return: display_key_storage value
        :rtype: ``BleGapConnectionParametersRange`` or ``None``
        """
        return self.__display_key_storage
    # end def property getter display_key_storage

    @synchronize_with_object_inner_lock("_lock_display_key_storage")
    def _append_display_key_storage(self, address, passkey):
        """
        Add a passkey for a specific address.

        :param address: address of the device this passkey correspond to
        :type value: ``BleGapAddress``
        :param passkey: the passkey to store
        :type passkey: ``int``

        :raise ``AssertionError``: If ``address`` is not a ``BleGapAddress`` or if ``passkey`` is not a ``int``
        """
        assert isinstance(address, BleGapAddress), (f"{self.__class__.__name__} address attribute should be a"
                                                    f" ``BleGapAddress``, {address} is not")
        assert isinstance(passkey,  int), (f"{self.__class__.__name__} passkey attribute should be an "
                                                    f"``int``, {passkey} is not")
        self.__display_key_storage[address] = passkey
    # end def _append_display_key_storage

    @classmethod
    def generate_configuration_file(cls, path, *args, **kwargs):
        # See ``TransportContext.generate_configuration_file``
        raise NotImplementedAbstractMethodError()
    # end def generate_configuration_file

    @classmethod
    def configure_device_cache(cls, path, force_reconfiguration=False, *args, **kwargs):
        # See ``TransportContext.configure_device_cache``
        if len(cls._DEVICE_CACHE) != 0:
            if force_reconfiguration:
                cls._DEVICE_CACHE.clear()
            else:
                return
            # end if
        # end if

        full_path = join(path, cls.CONFIG_FILE_NAME)

        if not access(full_path, R_OK):
            cls.generate_configuration_file(path=path)
        # end if

        config = ConfigParser()
        config.read([full_path])

        index = 0
        while config.has_section(f'READER_{index}'):
            ble_address_type = BleGapAddressType(config.get(section=f'READER_{index}', option="ble_address_type"))
            ble_address = config.get(section=f'READER_{index}', option="ble_address")
            if ble_address is not None and ble_address != 'None':
                cls._DEVICE_CACHE.append(cls.BLE_CONTEXT_DEVICE_CLASS(address=BleGapAddress(
                    address_type=ble_address_type, address=ble_address)))
            # end if
            index += 1
        # end while

        if index == 0:
            raise ValueError('Empty config file: %s' % (full_path,))
        # end if
    # end def configure_device_cache

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def open(self):
        # See ``TransportContext.open``
        raise NotImplementedAbstractMethodError(
            message='This function should be implemented in inheriting class, and use property is_open')
    # end def open

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def close(self):
        # See ``TransportContext.close``
        raise NotImplementedAbstractMethodError(
            message='This function should be implemented in inheriting class, and use property is_open')
    # end def close

    def reset(self):
        # See ``TransportContext.reset``
        raise NotImplementedAbstractMethodError()
    # end def reset

    def update_device_list(self):
        """
        Update the device list. For example when a hardware change has been performed and the context do not have any
        capabilities to automatically change the value of connected device.

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def update_device_list

    def get_devices(self, index_in_cache=None, address=None, *args, **kwargs):
        """
        Get context devices in the cache. Multiple filters can be used:

        * If ``index_in_cache`` is given, ``address`` is ignored and the index in the cache is used to get the device
        * If ``address`` is given, the devices (there should be only one normally) with this BLE address in the cache is
          returned
        * Child class can add new filters as parameters

        :param index_in_cache: The index in the cache of the device to get - OPTIONAL
        :type index_in_cache: ``int`` or ``None``
        :param address: The BLE address of the device to get - OPTIONAL
        :type address: ``BleGapAddress`` or ``None``
        :param args: Potential future parameters - OPTIONAL
        :type args: ``object``
        :param kwargs: Potential future keyword parameters - OPTIONAL
        :type kwargs: ``object``

        :return: The device found with the given filters (None if no device found)
        :rtype: ``list[BleContextDevice]``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_devices

    def add_service_to_central_gatt_table(self, service):
        """
        Add a service to the GATT table of the central of this context. The service structure given should have all
        substructures in it (characteristics, descriptors, ...). This method will add all of it to the GATT table.

        :param service: Complete structure of the service to add
        :type service: ``BleService``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def add_service_to_central_gatt_table

    def reset_central_gatt_table(self):
        """
        Remove everything from the GATT table of the central of this context.

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def reset_central_gatt_table

    def is_central_gatt_table_empty(self):
        """
        Check if the GATT table of the central of this context is empty.

        :return: Flag indicating if the central's GATT table is empty
        :rtype: ``bool``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def is_central_gatt_table_empty

    def is_service_in_central_gatt_table(self, service_uuid):
        """
        Check if a service is in the GATT table of the central of this context.

        :param service_uuid: UUID of the service to check
        :type service_uuid: ``BleUuid``

        :return: Flag indicating if the service is present in the central's GATT table
        :rtype: ``bool``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def is_service_in_central_gatt_table

    def scan(self, scan_time=GENERIC_SCAN_TIME, send_scan_request=False, scan_interval=None, scan_window=None):
        """
        Scan for a set time. This is a blocking method. It will return the advertising packets (and scanning response
        if requested)

        :param scan_time: The scan time - OPTIONAL
        :type scan_time: ``int`` or ``float``
        :param send_scan_request: Flag indicating if scan responses are requested - OPTIONAL
        :type send_scan_request: ``bool``
        :param scan_interval: Interval in ms between scan window - OPTIONAL
        :type scan_interval: ``int`` or ``float`` or ``None``
        :param scan_window: Scan window in ms - OPTIONAL
        :type scan_window: ``int`` or ``float`` or ``None``

        :return: List of ble device scanned with their associated advertising packet (and optionally scan response)
        :rtype: ``list[BleContextDevice]``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def scan

    def start_scan(self, scan_time=GENERIC_SCAN_TIME, send_scan_request=False, scan_interval=None, scan_window=None):
        """
        Start a scan for a set time. This is a non-blocking method.

        :param scan_time: The scan time - OPTIONAL
        :type scan_time: ``int`` or ``float``
        :param send_scan_request: Flag indicating if scan responses are requested - OPTIONAL
        :type send_scan_request: ``bool``
        :param scan_interval: Interval in ms between scan window - OPTIONAL
        :type scan_interval: ``int`` or ``float`` or ``None``
        :param scan_window: Scan window in ms - OPTIONAL
        :type scan_window: ``int`` or ``float`` or ``None``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def start_scan

    def scan_for_devices(self, ble_addresses=None, manufacturer_data_company_id=None, scan_time=GENERIC_SCAN_TIME,
                         send_scan_request=False):
        """
        Scan for specific devices. This is a blocking method.

        :param ble_addresses: List of BLE device addresses to get - OPTIONAL
        :type ble_addresses: ``list[BleGapAddress]`` or ``None``
        :param manufacturer_data_company_id: The company ID in the advertising manufacturer data (in big endian), some
                                             values can be found in ``ManufacturerDataCompanyId`` - OPTIONAL
        :type manufacturer_data_company_id: ``int`` or ``None``
        :param scan_time: The scan time - OPTIONAL
        :type scan_time: ``int`` or ``float``
        :param send_scan_request: Flag indicating if scan responses are requested - OPTIONAL
        :type send_scan_request: ``bool``

        :return: List of ble device scanned with their associated advertising packet (and optionally scan response)
        :rtype: ``list[BleContextDevice]``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def scan_for_devices

    def scan_for_first_device_found(self, ble_addresses=None, manufacturer_data_company_id=None,
                                    scan_timeout=GENERIC_SCAN_TIME, send_scan_request=False):
        """
        Scan for the first device found following the given parameter. This is a blocking method, it will stop as soon
        as it finds a device.

        :param ble_addresses: List of BLE device addresses to get - OPTIONAL
        :type ble_addresses: ``list[BleGapAddress]`` or ``None``
        :param manufacturer_data_company_id: The company ID in the advertising manufacturer data (in big endian), some
                                             values can be found in ``ManufacturerDataCompanyId`` - OPTIONAL
        :type manufacturer_data_company_id: ``int`` or ``None``
        :param scan_timeout: The scan timeout - OPTIONAL
        :type scan_timeout: ``int`` or ``float``
        :param send_scan_request: Flag indicating if scan responses are requested - OPTIONAL
        :type send_scan_request: ``bool``

        :return: The first ble device found with its associated advertising packet (and optionally scan response)
        :rtype: ``BleContextDevice``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def scan_for_first_device_found

    def start_scan_for_device(self, ble_addresses=None, manufacturer_data_company_id=None,
                              scan_time=GENERIC_SCAN_TIME,
                              send_scan_request=False):
        """
        Scan for specific devices. This is a non-blocking method. The scanning will start and results will be available
        with ``get_scanning_result``

        :param ble_addresses: List of BLE device addresses to get - OPTIONAL
        :type ble_addresses: ``list[BleGapAddress]`` or ``None``
        :param manufacturer_data_company_id: The company ID in the advertising manufacturer data (in big endian), some
                                             values can be found in ``ManufacturerDataCompanyId`` - OPTIONAL
        :type manufacturer_data_company_id: ``int`` or ``None``
        :param scan_time: The scan time - OPTIONAL
        :type scan_time: ``int`` or ``float``
        :param send_scan_request: Flag indicating if scan responses are requested - OPTIONAL
        :type send_scan_request: ``bool``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def start_scan_for_device

    def start_scan_for_first_device_found(self, ble_addresses=None, manufacturer_data_company_id=None,
                                          scan_timeout=GENERIC_SCAN_TIME, send_scan_request=False):
        """
        Scan for the first device found following the given parameter. This is a non-blocking method. The scanning will
        start and results will be available with ``get_scanning_result`` as soon as one device is found

        :param ble_addresses: List of BLE device addresses to get - OPTIONAL
        :type ble_addresses: ``list[BleGapAddress]`` or ``None``
        :param manufacturer_data_company_id: The company ID in the advertising manufacturer data (in big endian), some
                                             values can be found in ``ManufacturerDataCompanyId`` - OPTIONAL
        :type manufacturer_data_company_id: ``int`` or ``None``
        :param scan_timeout: The scan timeout - OPTIONAL
        :type scan_timeout: ``int`` or ``float``
        :param send_scan_request: Flag indicating if scan responses are requested - OPTIONAL
        :type send_scan_request: ``bool``


        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def start_scan_for_first_device_found

    def get_scanning_result(self, timeout):
        """
        Read the result of asynchronous scanning started earlier, Will block until they are ready

        :param timeout:  The scan timeout
        :type timeout: ``int`` or ``float``
        :return: List of ble device scanned with their associated advertising packet (and optionally scan response)
        :rtype: ``list[BleContextDevice]``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_scanning_result

    def is_direct_advertising_device_present(self, ble_context_device, scan_time=GENERIC_SCAN_TIME):
        """
        Verify if a specific device is direct advertising. This is a blocking method.

        :param ble_context_device: The BLE device to connect to
        :type ble_context_device: ``BleContextDevice``
        :param scan_time: The scan time - OPTIONAL
        :type scan_time: ``int`` or ``float``

        :return: Flag indicating if the wanted device has been found
        :rtype: ``bool``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def is_direct_advertising_device_present

    def connect(self, ble_context_device, connection_parameters=None, timeout=BLOCKING_DEFAULT_TIMEOUT,
                service_discovery=True, confirm_connect=False):
        """
        Connect to a device

        :param ble_context_device: The BLE device to connect to
        :type ble_context_device: ``PcBleDriverPyBleContextDevice``
        :param connection_parameters: Connection parameters - OPTIONAL
        :type connection_parameters: ``BleGapConnectionParameters`` or ``None``
        :param timeout: Timeout in seconds. If 0, it is a non-blocking operation - OPTIONAL
        :type timeout: ``int`` or ``float``
        :param service_discovery: Flag indicating if performing a service discovery when connected is wanted - OPTIONAL
        :type service_discovery: ``bool``
        :param confirm_connect: Flag indicating if the connection shall be verified - OPTIONAL
        :type confirm_connect: ``bool``

        :return: Flag indicating if the connection worked
        :rtype: ``bool``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def connect

    def disconnect(self, ble_context_device, timeout=BLOCKING_DEFAULT_TIMEOUT):
        """
        Disconnect from the current device.

        :param ble_context_device: The BLE device to disconnect from
        :type ble_context_device: ``BleContextDevice``
        :param timeout: Timeout in seconds. If 0, it is a non-blocking operation - OPTIONAL
        :type timeout: ``int`` or ``float``

        :return: Flag indicating if the disconnect worked
        :rtype: ``bool``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def disconnect

    def perform_service_discovery(self, ble_context_device, vendor_uuid_bases_to_add=None):
        """
        Perform service discovery on a connected device

        :param ble_context_device: The BLE device to perform service discovery on
        :type ble_context_device: ``BleContextDevice``
        :param vendor_uuid_bases_to_add: A list of UUID base in form of list of int to add to the known table before
                                         the discovery - OPTIONAL
        :type vendor_uuid_bases_to_add: ``list[list[int]]`` or ``None``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def perform_service_discovery

    def authenticate_just_works(self, ble_context_device, lesc=False):
        """
        Bond with a device, or encrypt communication with an already bonded device.

        :param ble_context_device: The BLE device to bond/encrypt with
        :type ble_context_device: ``BleContextDevice``
        :param lesc: Flag indicating to permit LE secure connection
        :type lesc: ``bool``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def authenticate_just_works

    def authenticate_keypress_start(self, ble_context_device, lesc=False):
        """
        Start bonding with a device using keypress method,

        :param ble_context_device: The BLE device to bond/encrypt with
        :type ble_context_device: ``BleContextDevice``
        :param lesc: Flag indicating to permit LE secure connection - OPTIONAL
        :type lesc: ``bool``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def authenticate_keypress_start

    def delete_bond(self, ble_context_device):
        """
        Delete the bond (if exist) with a device. This will disconnect the device if it is connected.

        :param ble_context_device: The BLE device of which to delete the bond
        :type ble_context_device: ``BleContextDevice``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def delete_bond

    def get_pairing_event(self, ble_context_device, block=True, timeout=BLOCKING_DEFAULT_TIMEOUT):
        """
        Return the top pairing event in the queue

        :param ble_context_device: The BLE device of which to get the status
        :type ble_context_device: ``BleContextDevice``
        :param block: Flag indicating if the queue operation should block waiting for an event
                      or return immediately - OPTIONAL
        :type block: ``bool``
        :param timeout: Timeout if blocking - OPTIONAL
        :type timeout: ``int`` or ``float`` or ``None``

        :return: The action corresponding to the event, or ``None`` if no event were found in the queue
        :rtype: ``BleSmpKeypress`` or ``None``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_pairing_event

    def update_connection_parameters(self, ble_context_device, connection_parameters):
        """
        Update the connection parameters on a connected device

        :param ble_context_device: The BLE device to update the connection parameters on
        :type ble_context_device: ``BleContextDevice``
        :param connection_parameters: Connection parameters
        :type connection_parameters: ``BleGapConnectionParameters``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def update_connection_parameters

    def get_connection_security_parameters(self, ble_context_device):
        """
        Get the connection security parameters on a connected device

        :param ble_context_device: The BLE device to get the connection security parameters from
        :type ble_context_device: ``BleContextDevice``

        :return: Connection security parameters
        :rtype: ``BleGapConnectionSecurityParameters``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_connection_security_parameters

    def register_ble_event_callback(self, ble_event, callback):
        """
        Register a callback for a specific context event, the call back is called immediately to optimize timings computation,
        standard processing happens after

        :param ble_event: the event to listen for
        :type ble_event: ``BleContextCallbackEvents``
        :param callback: function to call when the event is received
        :type callback: ``callable``
        """
        raise NotImplementedAbstractMethodError()
    # end def register_ble_event_callback

    def clear_ble_event_callback(self):
        """
        Clear the callbacks of the ble context
        """
        raise NotImplementedAbstractMethodError()
    # end def clear_ble_event_callback

    def characteristic_write(self, ble_context_device, characteristic, data):
        """
        Write data on a characteristic. Use a write-with-response exchange.

        :param ble_context_device: The BLE device to disconnect from
        :type ble_context_device: ``BleContextDevice``
        :param characteristic: Characteristic object to use to send data
        :type characteristic: ``BleCharacteristic``
        :param data: The data to send
        :type data: ``BleMessage``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def characteristic_write

    def characteristic_write_without_response(self, ble_context_device, characteristic, data):
        """
        Write data on a characteristic. Use a write-without-response exchange.

        :param ble_context_device: The BLE device to disconnect from
        :type ble_context_device: ``BleContextDevice``
        :param characteristic: Characteristic object to use to send data
        :type characteristic: ``BleCharacteristic``
        :param data: The data to send
        :type data: ``BleMessage``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def characteristic_write_without_response

    def characteristic_long_write(self, ble_context_device, characteristic, data):
        """
        Long write data on a characteristic.

        :param ble_context_device: The BLE device to disconnect from
        :type ble_context_device: ``BleContextDevice``
        :param characteristic: Characteristic object to use to send data
        :type characteristic: ``BleCharacteristic``
        :param data: The data to send
        :type data: ``BleMessage``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def characteristic_long_write

    def attribute_read(self, ble_context_device, attribute):
        """
        Read data of a characteristic.

        :param ble_context_device: The BLE device to use
        :type ble_context_device: ``BleContextDevice``
        :param attribute: Attribute object to read from
        :type attribute: ``BleAttribute``

        :return: The data read from the attribute
        :rtype: ``BleMessage``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def attribute_read

    def get_notification_status(self, ble_context_device, characteristic):
        """
        Get the notification status (enabled/disabled) on a characteristic.

        :param ble_context_device: The BLE device to use
        :type ble_context_device: ``BleContextDevice``
        :param characteristic: Characteristic object to enable notification from
        :type characteristic: ``BleCharacteristic``

        :return: The notification status as a boolean: ``True`` for enabled and ``False`` for disabled
        :rtype: ``bool``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_notification_status

    def enable_notification(self, ble_context_device, characteristic, time_stamped_queue=None):
        """
        Enable notification on a characteristic.

        :param ble_context_device: The BLE device to use
        :type ble_context_device: ``BleContextDevice``
        :param characteristic: Characteristic object to enable notification status of
        :type characteristic: ``BleCharacteristic``
        :param time_stamped_queue: Queue for time stamped data received by notification - OPTIONAL
        :type time_stamped_queue: ``Queue`` or ``None``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def enable_notification

    def write_on_cccd_notification(self, ble_context_device, characteristic, enabled):
        """
        Write on the device CCCD to set a notification value.
        this can be done to rewrite the same value as currently written.
        If no notification queue already added the notification will not be valid

        :param ble_context_device: The BLE device to use
        :type ble_context_device: ``BleContextDevice``
        :param characteristic: Characteristic object to enable notification status of
        :type characteristic: ``BleCharacteristic``
        :param enabled: Flag indicating if the notification need to be enabled
        :type enabled: ``bool``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def write_on_cccd_notification

    def update_notification_queue(self, ble_context_device, characteristic, time_stamped_queue=None):
        """
        Update the time stamped queue for notification on a characteristic. The notification had to be enabled prior
        to this method.

        :param ble_context_device: The BLE device to use
        :type ble_context_device: ``BleContextDevice``
        :param characteristic: Characteristic object to update the queue from
        :type characteristic: ``BleCharacteristic``
        :param time_stamped_queue: Queue for time stamped data received by notification - OPTIONAL
        :type time_stamped_queue: ``Queue`` or ``None``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def update_notification_queue

    def disable_notification(self, ble_context_device, characteristic):
        """
        Disable notification on a characteristic.

        :param ble_context_device: The BLE device to use
        :type ble_context_device: ``BleContextDevice``
        :param characteristic: Characteristic object to disable notification from
        :type characteristic: ``BleCharacteristic``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def disable_notification

    def get_indication_status(self, ble_context_device, characteristic):
        """
        Get the indication status (enabled/disabled) on a characteristic.

        :param ble_context_device: The BLE device to use
        :type ble_context_device: ``BleContextDevice``
        :param characteristic: Characteristic object to get the indication status of
        :type characteristic: ``BleCharacteristic``

        :return: The indication status as a boolean: ``True`` for enabled and ``False`` for disabled
        :rtype: ``bool``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_indication_status

    def enable_indication(self, ble_context_device, characteristic, time_stamped_queue=None):
        """
        Enable indication on a characteristic.

        :param ble_context_device: The BLE device to use
        :type ble_context_device: ``BleContextDevice``
        :param characteristic: Characteristic object to enable indication from
        :type characteristic: ``BleCharacteristic``
        :param time_stamped_queue: Queue for time stamped data received by indication - OPTIONAL
        :type time_stamped_queue: ``Queue`` or ``None``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def enable_indication

    def update_indication_queue(self, ble_context_device, characteristic, time_stamped_queue=None):
        """
        Update the time stamped queue for indication on a characteristic. The indication had to be enabled prior
        to this method.

        :param ble_context_device: The BLE device to use
        :type ble_context_device: ``BleContextDevice``
        :param characteristic: Characteristic object to update the queue from
        :type characteristic: ``BleCharacteristic``
        :param time_stamped_queue: Queue for time stamped data received by indication - OPTIONAL
        :type time_stamped_queue: ``Queue`` or ``None``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def update_indication_queue

    def disable_indication(self, ble_context_device, characteristic):
        """
        Disable indication on a characteristic.

        :param ble_context_device: The BLE device to use
        :type ble_context_device: ``BleContextDevice``
        :param characteristic: Characteristic object to disable indication from
        :type characteristic: ``BleCharacteristic``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def disable_indication

    def get_gatt_table(self, ble_context_device):
        """
        Get the GATT table of the connected device.

        :param ble_context_device: The BLE device to bond/encrypt with
        :type ble_context_device: ``BleContextDevice``

        :return: Gatt table as a list of services
        :rtype: ``list[BleService]``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_gatt_table

    def get_central_address(self):
        """
        Get the GAP address of the central used for this context.

        :return: The central GAP address
        :rtype: ``BleGapAddress``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_central_address

    def get_service(self, ble_context_device, uuid):
        """
        Get service in GATT table

        :param ble_context_device: The BLE device to get the service from
        :type ble_context_device: ``BleContextDevice``
        :param uuid: UUID of the service
        :type uuid: ``BleUuid``

        :return: Matching service (if found)
        :rtype: ``BleService`` or ``None``
        """
        gatt_table = self.get_gatt_table(ble_context_device)
        for service in gatt_table:
            if service.uuid == uuid:
                return service
            # end if
        # end for
    # end def get_service

    def dump_gatt_table(self, ble_context_device, xlsx_file_path=None):
        """
        Dump the GATT table of the connected device.

        :param ble_context_device: The BLE device to bond/encrypt with
        :type ble_context_device: ``BleContextDevice``
        :param xlsx_file_path: The path of the xlsx file to write in, if None, the GATT table will be printed in
                               console - OPTIONAL
        :type xlsx_file_path: ``str``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        gatt_table = self.get_gatt_table(ble_context_device)

        if xlsx_file_path is not None:
            workbook = Workbook('gatt_table.xlsx')

            format_first_line = workbook.add_format({
                'bold': True,
                'border': 1,
                'bottom': 6,
                'bottom_color': '#cfcfcf',
                'align': 'center',
                'valign': 'vcenter',
                'fg_color': '#000000',
                'font_color': '#ffffff',
                'text_wrap': True})
            format_service = workbook.add_format({
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
                'fg_color': '#8dbbe3',
                'font_color': '#000000',
                'text_wrap': True})
            format_characteristic_declaration = workbook.add_format({
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
                'fg_color': '#90e681',
                'font_color': '#000000',
                'text_wrap': True})
            format_characteristic_value = workbook.add_format({
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
                'fg_color': '#baffad',
                'font_color': '#000000',
                'text_wrap': True})
            format_descriptor = workbook.add_format({
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
                'fg_color': '#f4ffa1',
                'font_color': '#000000',
                'text_wrap': True})

            new_worksheet = workbook.add_worksheet(name="gatt_table")
            new_worksheet.set_column(0, 2, 50)
            new_worksheet.set_row(0, 60)
            new_worksheet.write("A1", "Handle", format_first_line)
            new_worksheet.write("B1", "UUID", format_first_line)
            new_worksheet.write("C1", "Characteristic permission", format_first_line)

            # Caption
            new_worksheet.set_column(5, 6, 40)
            new_worksheet.write("F1", "Service", format_service)
            new_worksheet.write("G1", "Characteristic declaration", format_characteristic_declaration)
            new_worksheet.write("F2", "Characteristic value", format_characteristic_value)
            new_worksheet.write("G2", "Descriptor", format_descriptor)

            line_number = 2

            for service in gatt_table:
                new_worksheet.set_row(line_number - 1, 60)
                new_worksheet.write(f"A{line_number}", f"{service.handle}", format_service)
                new_worksheet.write(f"B{line_number}", f"{service.uuid}", format_service)
                new_worksheet.write(f"C{line_number}", "-", format_service)
                line_number += 1
                for characteristic in service.characteristics:
                    new_worksheet.set_row(line_number - 1, 60)
                    new_worksheet.write(f"A{line_number}", f"{characteristic.declaration.handle}",
                                        format_characteristic_declaration)
                    new_worksheet.write(f"B{line_number}", f"{characteristic.declaration.uuid}",
                                        format_characteristic_declaration)
                    new_worksheet.write(f"C{line_number}", "-", format_characteristic_declaration)
                    line_number += 1
                    new_worksheet.set_row(line_number - 1, 60)
                    new_worksheet.write(f"A{line_number}", f"{characteristic.handle}", format_characteristic_value)
                    new_worksheet.write(f"B{line_number}", f"{characteristic.uuid}", format_characteristic_value)
                    new_worksheet.write(f"C{line_number}", f"{characteristic.properties}", format_characteristic_value)
                    line_number += 1
                    for descriptor in characteristic.descriptors:
                        # Do not print value handle
                        if descriptor.uuid.value != characteristic.uuid.value:
                            new_worksheet.set_row(line_number - 1, 60)
                            new_worksheet.write(f"A{line_number}", f"{descriptor.handle}", format_descriptor)
                            new_worksheet.write(f"B{line_number}", f"{descriptor.uuid}", format_descriptor)
                            new_worksheet.write(f"C{line_number}", "-", format_descriptor)
                            line_number += 1
                        # end if
                    # end for
                # end for
            # end for

            workbook.close()
        else:
            for service in gatt_table:
                print(service)
                for characteristic in service.characteristics:
                    print(f"\t{characteristic}")
                    for descriptor in characteristic.descriptors:
                        # Do not print value handle
                        if descriptor.uuid.value != characteristic.uuid.value:
                            print(f"\t\t{descriptor}")
                        # end if
                    # end for
                # end for
            # end for
        # end if
    # end def dump_gatt_table

    # ------------------------------------------------------------------------------------------------------------------
    # Class and static methods
    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def reset_context_hardware(cls, *args, **kwargs):
        """
        Perform a reset on the BLE context hardware

        :param args: Potential future parameters - OPTIONAL
        :type args: ``list``
        :param kwargs: Potential future parameters - OPTIONAL
        :type kwargs: ``dict``
        """
        raise NotImplementedAbstractMethodError()
    # end def reset_context_hardware

    @classmethod
    def update_context_hardware(cls, *args, **kwargs):
        """
        Update the BLE context hardware

        :param args: Potential future parameters - OPTIONAL
        :type args: ``list``
        :param kwargs: Potential future parameters - OPTIONAL
        :type kwargs: ``dict``

        :return: Flag indicating if the firmware on the DK is up-to-date
        :rtype: ``bool``
        """
        raise NotImplementedAbstractMethodError()
    # end def update_context_hardware

    @staticmethod
    def get_company_id(advertising_data):
        """
        Get the company ID form the manufacturer data (if present) in advertising data.

        :param advertising_data: Advertising data structure from driver layer
        :type advertising_data: ``BleAdvertisingData``

        :return: The company ID
        :rtype: ``int`` or ``None``

         :raise ``ValueError``: if wong data type
        """
        if not isinstance(advertising_data, BleAdvertisingData):
            raise ValueError(f"Wrong type for adv_data. It should be BLEAdvData or BleAdvertisingData but it "
                             f"is {type(advertising_data)}")
        # end if

        if BleAdvertisingDataType.MANUFACTURER_SPECIFIC_DATA not in advertising_data.records:
            return None
        # end if

        return advertising_data.records[BleAdvertisingDataType.MANUFACTURER_SPECIFIC_DATA][0][0] + \
            (advertising_data.records[BleAdvertisingDataType.MANUFACTURER_SPECIFIC_DATA][0][1] << 8)
    # end def get_company_id
# end class BleContext

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
