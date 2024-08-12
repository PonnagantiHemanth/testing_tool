#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytransport.ble.nrfblelibblecontext.nrfblelibblecontext
:brief: nrf-ble-lib BLE context classes
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2023/03/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import queue
from _weakref import ref
from copy import copy
from ctypes import c_long
from ctypes import py_object
from ctypes import pythonapi
from os import path
from queue import Empty
from queue import Queue
from sys import stdout
from threading import Event
from threading import RLock
from threading import Thread
from time import perf_counter_ns
from time import sleep
from time import time
from typing import Dict

from aioprocessing import AioQueue
from serial.tools.list_ports import comports

from pylibrary.system.tracelogger import TIMESTAMP_UNIT_DIVIDER_MAP
from pylibrary.system.tracelogger import TraceLevel
from pylibrary.system.tracelogger import TraceLogger
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pylibrary.tools.threadutils import RLockedDict
from pylibrary.tools.threadutils import synchronize_with_object_inner_lock
from pytransport.ble.bleconstants import BleAdvertisingPduType
from pytransport.ble.bleconstants import BleContextConnectionParameterUpdateRequestResult
from pytransport.ble.bleconstants import BleContextEventDataType
from pytransport.ble.bleconstants import BleContextEventType
from pytransport.ble.bleconstants import BleControllerErrorCodes
from pytransport.ble.bleconstants import BleGapAddressType
from pytransport.ble.bleconstants import BleGenericFloatConstant
from pytransport.ble.bleconstants import BleGenericIntConstant
from pytransport.ble.bleconstants import BlePairingFailReason
from pytransport.ble.bleconstants import BleScanIntervalWindowRange
from pytransport.ble.bleconstants import BleScanType
from pytransport.ble.bleconstants import BleScanningFilterPolicy
from pytransport.ble.bleconstants import BleSmpKeypress
from pytransport.ble.bleconstants import BleUuidStandardDescriptor
from pytransport.ble.blecontext import BleContext
from pytransport.ble.blecontext import BleContextCallbackEvents
from pytransport.ble.blecontext import BleContextDevice
from pytransport.ble.blecontext import FORCE_AT_CREATION_ALL_BLE_TRACE_FILE_NAME
from pytransport.ble.blecontext import FORCE_AT_CREATION_ALL_BLE_TRACE_LEVEL
from pytransport.ble.bleinterfaceclasses import BleAdvertisingData
from pytransport.ble.bleinterfaceclasses import BleCharacteristic
from pytransport.ble.bleinterfaceclasses import BleDescriptor
from pytransport.ble.bleinterfaceclasses import BleDeviceBondingStates
from pytransport.ble.bleinterfaceclasses import BleGapAddress
from pytransport.ble.bleinterfaceclasses import BleGapConnectionParameters
from pytransport.ble.bleinterfaceclasses import BleGapConnectionParametersRange
from pytransport.ble.bleinterfaceclasses import BleGapConnectionSecurityParameters
from pytransport.ble.bleinterfaceclasses import BleService
from pytransport.ble.bleinterfaceclasses import BleUuid
from pytransport.ble.blemessage import BleContextEvent
from pytransport.ble.blemessage import BleMessage
# noinspection PyUnresolvedReferences
from pytransport.ble.nrfblelibblecontext.nrf_ble_lib import Adapter
# noinspection PyUnresolvedReferences
from pytransport.ble.nrfblelibblecontext.nrf_ble_lib import Connection
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import CharacteristicReadResponseArgsInd
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import DeviceAdvertisingInformationIndex
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import ErrorId
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import GetCentralAddressResponseArgsInd
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import GetConnectionSecurityParametersResponseArgsInd
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import IndicationEventArgsInd
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import IoCapability
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import L2capConnectionParameterUpdateRequestEventArgsInd
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import LogEventArgsInd
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import NotificationEventArgsInd
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import NrfBleLibHciOpcode
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import NrfBleLibProcessMessageType
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import NrfBleLibProcessUtil
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import PerformServiceDiscoveryResponseArgsInd
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import ReadOperation
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import ScanStartResponseArgsInd
from pytransport.ble.nrfblelibblecontext.nrfblelibconstants import WriteOperation
from pytransport.ble.nrfblelibblecontext.nrfblelibprocess import ERROR_TYPES
from pytransport.ble.nrfblelibblecontext.nrfblelibprocess import NrfBleLibAsyncioProcess
from pytransport.ble.nrfblelibblecontext.nrfblelibprocess import NrfBleLibScanFilters
from pytransport.ble.nrfblelibblecontext.nrfblelibprocess import NrfBleLibStructureTranslator
from pytransport.transportcontext import TransportContextException

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
TRACE_LOGGER = TraceLogger.get_instance()
RECONNECT_HARDWARE_TIMEOUT = 10
# Extra timeout time added to getting the results of scan
# so the end of a scan and getting the results isn't a race condition
SCAN_FINISH_EXTRA_TIME = 2  # in seconds

BLE_CALLBACK_EVENT_TO_KEY = {
    BleContextCallbackEvents.CONNECTION_COMPLETE: "le_connection_complete",
    BleContextCallbackEvents.DISCONNECTION_COMPLETE: "hci_disconnection_complete",
    BleContextCallbackEvents.COMMAND_COMPLETE: "hci_command_complete",
    BleContextCallbackEvents.CONNECTION_UPDATE_COMPLETE: "le_connection_update_complete",
    BleContextCallbackEvents.NOTIFICATION_EVENT: NrfBleLibProcessMessageType.NOTIFICATION_EVENT,
    BleContextCallbackEvents.INDICATION_EVENT: NrfBleLibProcessMessageType.INDICATION_EVENT,
    BleContextCallbackEvents.CONNECTION_UPDATE_REQUEST_EVENT:
        NrfBleLibProcessMessageType.L2CAP_CONNECTION_PARAMETER_UPDATE_REQUEST_EVENT,
}


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class NrfBleLibBleContextDevice(BleContextDevice):
    """
    Class for BLE device used in a nrf-ble-lib context
    """

    def __init__(self, nrf_ble_lib_connection_handle=None, address=None, advertising_type=None, advertising_data=None,
                 scan_response=None, bonded=False, connected=False, connection_security_parameters=None,
                 transfer_callbacks=None):
        """
        :param nrf_ble_lib_connection_handle: The connection object (according to nordic nrf-ble-lib) index in the
                                             process internal cache (see ``NrfBleLibAsyncioProcess``) - OPTIONAL
        :type nrf_ble_lib_connection_handle: ``int`` or ``None``
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
        :param connected: Flag indicating if the device is connected - OPTIONAL
        :type connected: ``bool``
        :param connection_security_parameters: Connection security parameters, only relevant when connected - OPTIONAL
        :type connection_security_parameters: ``BleGapConnectionSecurityParameters`` or ``None``
        :param transfer_callbacks: The callbacks that will be used when a transfer is received for each transfer type
                                   (HID mouse, HID keyboard, HID++, etc...), its format is a thread safe dictionary
                                   (the keys are BLE characteristic handles). If ``None``, it will be set as an
                                   empty thread safe dictionary - OPTIONAL
        :type transfer_callbacks: ``RLockedDict`` or ``None``
        """
        super().__init__(address=address, advertising_type=advertising_type, advertising_data=advertising_data,
                         scan_response=scan_response, bonded=bonded, connected=connected,
                         connection_security_parameters=connection_security_parameters,
                         transfer_callbacks=transfer_callbacks)

        self._lock_nrf_ble_lib_connection_handle = RLock()
        self._nrf_ble_lib_connection_handle = nrf_ble_lib_connection_handle

        self._lock_gatt_table = RLock()
        self._gatt_table = None
    # end def __init__

    @property
    @synchronize_with_object_inner_lock("_lock_nrf_ble_lib_connection_handle")
    def nrf_ble_lib_connection_handle(self):
        """
        Property getter of ``nrf_ble_lib_connection_handle``.

        :return: ``nrf_ble_lib_connection_handle`` value
        :rtype: ``int`` or ``None``
        """
        return self._nrf_ble_lib_connection_handle
    # end def property getter nrf_ble_lib_connection_handle

    @nrf_ble_lib_connection_handle.setter
    @synchronize_with_object_inner_lock("_lock_nrf_ble_lib_connection_handle")
    def nrf_ble_lib_connection_handle(self, nrf_ble_lib_connection_handle):
        """
        Property setter of ``nrf_ble_lib_connection_handle``.

        :param nrf_ble_lib_connection_handle: ``nrf_ble_lib_connection_handle`` value
        :type nrf_ble_lib_connection_handle: ``int`` or ``None``
        """
        assert isinstance(nrf_ble_lib_connection_handle, (int, type(None))), \
            f"{self.__class__.__name__}.nrf_ble_lib_connection_handle is an int or None, " \
            f"{nrf_ble_lib_connection_handle} is neither"

        self._nrf_ble_lib_connection_handle = nrf_ble_lib_connection_handle
    # end def property setter nrf_ble_lib_connection_handle

    @property
    @synchronize_with_object_inner_lock("_lock_gatt_table")
    def gatt_table(self):
        """
        Property getter of ``gatt_table``.

        :return: ``gatt_table`` value
        :rtype: ``list`` or ``None``
        """
        return self._gatt_table
    # end def property getter gatt_table

    @gatt_table.setter
    @synchronize_with_object_inner_lock("_lock_gatt_table")
    def gatt_table(self, gatt_table):
        """
        Property setter of ``gatt_table``.

        :param gatt_table: ``gatt_table`` value
        :type gatt_table: ``list`` or ``None``
        """
        assert isinstance(gatt_table, (list, type(None))), \
            f"{self.__class__.__name__}.gatt_table is a list or None, {gatt_table} is neither"

        self._gatt_table = gatt_table
    # end def property setter gatt_table
# end class NrfBleLibBleContextDevice


class NrfBleLibBleContext(BleContext):
    """
    This is the definition of the BLE Stack Emulator object using nrf-ble-lib v5 with some custom changes
    for nRF52840 with connectivity app
    """
    MCU_NAME = "NRF52840_XXAA"
    CLASS_METHOD_TRACE_LEVEL = FORCE_AT_CREATION_ALL_BLE_TRACE_LEVEL if \
        FORCE_AT_CREATION_ALL_BLE_TRACE_LEVEL is not None else TraceLevel.NO_TRACE
    CLASS_METHOD_TRACE_FILE_NAME = FORCE_AT_CREATION_ALL_BLE_TRACE_FILE_NAME
    # Class to use for configuring the class cache, it should be BleContextDevice or its child class
    BLE_CONTEXT_DEVICE_CLASS = NrfBleLibBleContextDevice
    BT_STACK_DEVICES = None
    # The VID and PID of nordic USB devices to automatically get the plugged DK with the BT-stack application
    BT_STACK_DEVICE_VID = 0x2FE3
    BT_STACK_DEVICE_PID = 0x0100
    CHECK_CONNECT_WORKED_TIMEOUT = .5  # TODO: research for the best value
    # Object to put on the event queue to stop the event thread
    STOP_EVENT_THREAD_SIGNAL = None
    ASYNCHRONOUS_CONNECTION_DISCONNECTION_CAPABILITY = True  # GAP connection/disconnection events
    DOOMED = False

    def __init__(self, com_port=None, trace_level=TraceLevel.NO_TRACE, trace_file_name=None):
        """
        :param com_port: COM port to use, if None it will get the first one with the right VID and PID - OPTIONAL
        :type com_port: ``str`` or ``None``
        :param trace_level: Trace level of the transport context - OPTIONAL
        :type trace_level: ``TraceLevel``
        :param trace_file_name: Trace output of the transport context - OPTIONAL
        :type trace_file_name: ``str``

        :raise ``TransportContextException``: If no hardware is found to have a BLE context
        """
        super().__init__(trace_level=trace_level, trace_file_name=trace_file_name)

        if com_port is None:
            serial_ports = self.get_bt_stack_devices_com_ports()
            if len(serial_ports) <= 0:
                raise TransportContextException(TransportContextException.Cause.CONTEXT_CONFIG_UNKNOWN,
                                                "No NRF central device found in serial ports")
            elif len(serial_ports) > 1:
                TRACE_LOGGER.log_trace(
                    subscription_owner=self,
                    message=f"More than one NRF central device found: {serial_ports}\n{serial_ports[0]} will be used",
                    trace_level=TraceLevel.WARNING)
            # end if
            self._serial_port = serial_ports[0]
        else:
            self._serial_port = com_port
        # end if

        self._scan_filters = NrfBleLibScanFilters()
        self._connecting_devices = RLockedDict()
        self._connected_devices = RLockedDict()
        self._disconnecting_devices = RLockedDict()
        self._notification_time_stamped_queues = RLockedDict()
        self._indication_time_stamped_queues = RLockedDict()
        self._callbacks = RLockedDict()
        # We only set the event queue as it is used to stop the event thread
        self._event_queue = AioQueue()
        self._nrf_ble_lib_process = NrfBleLibAsyncioProcess(com_port=self._serial_port, event_queue=self._event_queue)
        self._event_thread = None
        self._central_gatt_table = []

        self._pairing_event_queues = RLockedDict()
    # end def __init__

    def __del__(self):
        # noinspection PyBroadException
        try:
            self.close()
        except Exception:
            self._stop_event_thread()
            self._nrf_ble_lib_process.stop_process()
        # end try
    # end def __del__

    def _stop_event_thread(self):
        """
        Stop the event thread if possible. If it cannot be stopped, it will be killed
        """
        if self._event_thread is not None and self._event_thread.is_alive():
            self._event_queue.put(NrfBleLibBleContext.STOP_EVENT_THREAD_SIGNAL)
            self._event_thread.join(timeout=BleContext.BLOCKING_DEFAULT_TIMEOUT)
            if self._event_thread.is_alive():
                stdout.write("Could not stop event thread, force killing it\n")
                self._force_kill_event_thread()
            # end if
        # end if
    # end def _stop_event_thread

    def _force_kill_event_thread(self):
        """
        Kill the thread event
        """
        if not self._event_thread.is_alive():
            return
        # end if

        result = pythonapi.PyThreadState_SetAsyncExc(c_long(self._event_thread.ident), py_object(SystemExit))
        if result == 0:
            raise ValueError("Invalid thread ID")
        elif result > 1:
            pythonapi.PyThreadState_SetAsyncExc(c_long(self._event_thread.ident), 0)
            raise SystemError("Force kill thread failure: Exception raise failure")
        # end if
    # end def _force_kill_event_thread

    def _get_nrf_ble_lib_event_thread_method(self):
        """
        Get the event thread event method
        """
        event_queue = self._event_queue
        connecting_devices = self._connecting_devices
        connected_devices = self._connected_devices
        disconnecting_devices = self._disconnecting_devices
        nrf_ble_lib_process = self._nrf_ble_lib_process
        notification_time_stamped_queues = self._notification_time_stamped_queues
        indication_time_stamped_queues = self._indication_time_stamped_queues
        callbacks = self._callbacks
        pairing_event_queues = self._pairing_event_queues

        # A weak reference is needed for logging purpose, it will be instantiated then deleted directly after
        weak_self = ref(self)

        def log_trace(message, trace_level=TraceLevel.NO_TRACE, end_line="\n"):
            """
            The log trace method to use in the thread

            :param message: Message to trace in the log
            :type message: ``str``
            :param trace_level: The trace level of this message - OPTIONAL
            :type trace_level: ``TraceLevel`` or ``int``
            :param end_line: End line string, by default it is a new line character. If ``None``, no end line is
                             added - OPTIONAL
            :type end_line: ``str``
            """
            context_object = weak_self()
            if context_object is not None:
                TRACE_LOGGER.log_trace(
                    subscription_owner=context_object, message=message, trace_level=trace_level, end_line=end_line)
            # end if
        # end def log_trace

        def treat_connection_event(event_data, timestamp):
            """
            Treat a connection event received in the event thread

            :param event_data: The dictionary representing the event data
            :type event_data: ``dict``
            :param timestamp: Monotonic timestamp in nanoseconds
            :type timestamp: ``int``
            """
            status = event_data["status"]
            connection_handle = event_data["connection_handle"]
            device_address = NrfBleLibStructureTranslator.get_interface_ble_gap_address(
                driver_ble_gap_address={"address_type": event_data["peer_address_type"],
                                        "address": event_data["peer_address"]})

            # TODO 0 = ERROR_CODE_SUCCESS (see nrf-ble-lib/btstack-sys/btstack/src/bluetooth.h), add error codes
            #  constants
            if status == 0:
                with connecting_devices:
                    ble_device = connecting_devices.pop(device_address, None)
                # end with

                if ble_device is not None:
                    ble_device: NrfBleLibBleContextDevice

                    log_trace(message=f"[Connection event] Connection event ({event_data}) to the expected device "
                                      f"({ble_device}) at {timestamp}ns",
                              trace_level=TraceLevel.DEBUG)

                    with connected_devices:
                        ble_device.connected = True
                        ble_device.connection_security_parameters = BleGapConnectionSecurityParameters()
                        connection_interval = event_data["connection_interval"] * \
                            BleGenericFloatConstant.CONNECTION_INTERVAL_GRANULARITY
                        supervision_timeout = event_data["supervision_timeout"] * \
                            BleGenericIntConstant.SUPERVISION_TIMEOUT_GRANULARITY
                        ble_device.connection_parameters = BleGapConnectionParameters(
                            min_connection_interval=connection_interval, max_connection_interval=connection_interval,
                            supervision_timeout=supervision_timeout, slave_latency=event_data["peripheral_latency"])
                        ble_device.nrf_ble_lib_connection_handle = connection_handle
                        connected_devices[connection_handle] = ble_device
                    # end with

                    ble_device.ble_context_event_queue.put(BleContextEvent(
                        event_type=BleContextEventType.CONNECTION_EVENT, event_data={}, timestamp=timestamp))
                    ble_device.wait_for_connection_event.set()
                else:
                    log_trace(message="[Connection event] Connection to an unexpected device: "
                                      f"{event_data}",
                              trace_level=TraceLevel.WARNING)
                # end if
            else:
                # TODO error treatment
                log_trace(message=f"[Connection event] Error: {event_data}",
                          trace_level=TraceLevel.WARNING)
            # end if
        # end def treat_connection_event

        def treat_disconnection_event(event_data, timestamp):
            """
            Treat a disconnection event received in the event thread

            :param event_data: The dictionary representing the event data
            :type event_data: ``dict``
            :param timestamp: Monotonic timestamp in nanoseconds
            :type timestamp: ``int``
            """

            status = event_data["status"]
            connection_handle = event_data["connection_handle"]

            with disconnecting_devices:
                ble_device = disconnecting_devices.pop(connection_handle, None)
            # end with

            # TODO 0 = ERROR_CODE_SUCCESS (see nrf-ble-lib/btstack-sys/btstack/src/bluetooth.h), add error codes
            #  constants
            if status == 0:
                if ble_device is not None:
                    log_trace(message=f"[Disconnection event] Disconnected ({event_data}) from the expected device "
                                      f"({ble_device}) at {timestamp}ns",
                              trace_level=TraceLevel.DEBUG)

                    # Sanity check
                    if not isinstance(ble_device, NrfBleLibBleContextDevice):
                        TRACE_LOGGER.log_trace(
                            subscription_owner=self,
                            message=f"[Disconnection event] Sanity check about the context device structure type "
                                    f"failed, the disconnecting device should be a NrfBleLibBleContextDevice and not "
                                    f"a {type(ble_device).__name__}",
                            trace_level=TraceLevel.ERROR)
                        # No exception are raised as the event reception thread should not stop
                        return
                    # end if

                    try:
                        with connected_devices:
                            ble_device.connected = False
                            ble_device.connection_security_parameters = None
                            ble_device.nrf_ble_lib_connection_handle = None
                            connected_devices.pop(connection_handle, None)
                        # end with

                        if not ble_device.bonded:
                            with self._notification_time_stamped_queues:
                                self._notification_time_stamped_queues.pop(ble_device.address, None)
                            # end with
                            with self._indication_time_stamped_queues:
                                self._indication_time_stamped_queues.pop(ble_device.address, None)
                            # end with
                        # end if
                    finally:
                        # TODO add reason to event
                        ble_device.ble_context_event_queue.put(BleContextEvent(
                            event_type=BleContextEventType.DISCONNECTION_EVENT, event_data={}, timestamp=timestamp))
                        ble_device.wait_for_disconnection_event.set()
                    # end try
                else:
                    with connected_devices:
                        ble_device = connected_devices.pop(connection_handle, None)
                    # end with

                    if ble_device is not None:
                        # TODO automatic reconnect, but because of the timing limitation of this driver it cannot be
                        #  done properly. It uses USB polling to communicate so it can have several hundreds of
                        #  milliseconds delay and miss the reconnection window of the device. Therefore for now no
                        #  reconnection is done.
                        log_trace(message=f"[Disconnection event] Disconnected ({event_data}) from an unexpected "
                                          f"device ({ble_device}) at {timestamp}ns",
                                  trace_level=TraceLevel.WARNING)

                        # Sanity check
                        if not isinstance(ble_device, NrfBleLibBleContextDevice):
                            TRACE_LOGGER.log_trace(
                                subscription_owner=self,
                                message=f"[Disconnection event] Sanity check about the context device structure type "
                                        f"failed, the disconnecting device should be a NrfBleLibBleContextDevice "
                                        f"and not a {type(ble_device).__name__}",
                                trace_level=TraceLevel.ERROR)
                            # No exception are raised as the event reception thread should not stop
                            return
                        # end if

                        try:
                            with connected_devices:
                                ble_device.connected = False
                                ble_device.connection_security_parameters = None
                                ble_device.nrf_ble_lib_connection_handle = None
                                connected_devices.pop(connection_handle, None)
                            # end with

                            if not ble_device.bonded:
                                with self._notification_time_stamped_queues:
                                    self._notification_time_stamped_queues.pop(ble_device.address, None)
                                # end with
                                with self._indication_time_stamped_queues:
                                    self._indication_time_stamped_queues.pop(ble_device.address, None)
                                # end with
                            # end if
                        finally:
                            # TODO add reason to event
                            ble_device.ble_context_event_queue.put(BleContextEvent(
                                event_type=BleContextEventType.DISCONNECTION_EVENT, event_data={}, timestamp=timestamp))
                            ble_device.wait_for_disconnection_event.set()
                        # end try
                    else:
                        log_trace(message=f"[Disconnection event] Disconnected ({event_data}) from an unknown device",
                                  trace_level=TraceLevel.WARNING)
                    # end if
                # end if
            else:
                # TODO error treatment
                log_trace(message=f"[Disconnection event] Error: {event_data}",
                          trace_level=TraceLevel.WARNING)
            # end if
        # end def treat_disconnection_event

        def treat_hci_command_complete_event(event_data, timestamp):
            """
            Treat an HCI command complete event received in the event thread

            :param event_data: The dictionary representing the event data
            :type event_data: ``dict``
            :param timestamp: Monotonic timestamp in nanoseconds
            :type timestamp: ``int``
            """
            command_opcode = event_data["command_opcode"]
            return_parameters = event_data["return_parameters"]

            if command_opcode in [NrfBleLibHciOpcode.LE_REMOTE_CONNECTION_PARAMETER_REQUEST_REPLY,
                                  NrfBleLibHciOpcode.LE_REMOTE_CONNECTION_PARAMETER_REQUEST_NEGATIVE_REPLY]:
                connection_handle = return_parameters[0] + (return_parameters[1] << 8)
                ble_device = connected_devices.get(connection_handle, None)

                if ble_device is not None:
                    if command_opcode == NrfBleLibHciOpcode.LE_REMOTE_CONNECTION_PARAMETER_REQUEST_REPLY:
                        TRACE_LOGGER.log_trace(
                            subscription_owner=self,
                            message=f"Automatic update of the connection parameters accepted the parameters "
                                    f"for: {ble_device}",
                            trace_level=TraceLevel.DEBUG)
                        result = BleContextConnectionParameterUpdateRequestResult.ACCEPTED
                    else:
                        # NrfBleLibHciOpcode.LE_REMOTE_CONNECTION_PARAMETER_REQUEST_NEGATIVE_REPLY
                        TRACE_LOGGER.log_trace(
                            subscription_owner=self,
                            message=f"Automatic update of the connection parameters refused the parameters "
                                    f"for: {ble_device}",
                            trace_level=TraceLevel.DEBUG)
                        result = BleContextConnectionParameterUpdateRequestResult.REJECTED
                    # end if
                    ble_device.ble_context_event_queue.put(BleContextEvent(
                        event_type=BleContextEventType.CONNECTION_PARAMETERS_UPDATE_REQUEST_RESULT,
                        event_data={BleContextEventDataType.CONNECTION_PARAMETERS_UPDATE_REQUEST_RESULT: result},
                        timestamp=timestamp))
                # end if
            # end if
        # end def treat_hci_command_complete_event

        def treat_connection_update_complete(event_data, timestamp):
            """
            Treat a connection update complete event received in the event thread

            :param event_data: The dictionary representing the event data
            :type event_data: ``dict``
            :param timestamp: Monotonic timestamp in nanoseconds
            :type timestamp: ``int``
            """
            # TODO check event_data["status"]
            connection_handle = event_data["connection_handle"]
            ble_device = connected_devices.get(connection_handle, None)

            if ble_device is not None:
                ble_device.connection_parameters = NrfBleLibStructureTranslator.get_interface_connection_parameters(
                    driver_connection_parameters=event_data)
                ble_device.ble_context_event_queue.put(BleContextEvent(
                    event_type=BleContextEventType.CONNECTION_PARAMETERS_UPDATE_COMPLETED,
                    event_data={BleContextEventDataType.CONNECTION_PARAMETERS_UPDATE_COMPLETED:
                                ble_device.connection_parameters},
                    timestamp=timestamp))
                TRACE_LOGGER.log_trace(
                    subscription_owner=self,
                    message="Connection update complete event "
                            f"(connection handle {connection_handle}) at {timestamp}ns",
                    trace_level=TraceLevel.DEBUG)
            else:
                TRACE_LOGGER.log_trace(
                    subscription_owner=self,
                    message="Connection update complete event from an unknown device"
                            f" (connection handle {connection_handle}) at {timestamp}ns",
                    trace_level=TraceLevel.WARNING)
            # end if
        # end def treat_connection_update_complete

        def treat_l2cap_connection_parameter_update_request_event(event):
            """
            Treat a L2CAP connection parameter update request event received in the event thread

            :param event: The tuple representing the event
            :type event: ``tuple``
            """
            event_arguments = NrfBleLibAsyncioProcess.get_message_arguments(message=event)
            event_data = event_arguments[L2capConnectionParameterUpdateRequestEventArgsInd.EVENT_DATA]
            timestamp = event_arguments[L2capConnectionParameterUpdateRequestEventArgsInd.TIMESTAMP]
            accepted_status = event_arguments[L2capConnectionParameterUpdateRequestEventArgsInd.ACCEPTED_STATUS]
            # TODO check event_data["status"]
            connection_handle = event_data["connection_handle"]
            ble_device = connected_devices.get(connection_handle, None)

            if ble_device is not None:
                connection_parameters_requested = NrfBleLibStructureTranslator.get_interface_connection_parameters(
                    driver_connection_parameters=event_data)

                ble_device.ble_context_event_queue.put(BleContextEvent(
                    event_type=BleContextEventType.L2CAP_CONNECTION_PARAMETERS_UPDATE_REQUEST,
                    event_data={BleContextEventDataType.CONNECTION_PARAMETERS_REQUESTED:
                                connection_parameters_requested},
                    timestamp=timestamp))

                TRACE_LOGGER.log_trace(
                    subscription_owner=self,
                    message="L2CAP connection parameter update request event "
                            f"(connection handle {connection_handle} at {timestamp})",
                    trace_level=TraceLevel.DEBUG)

                if accepted_status:
                    TRACE_LOGGER.log_trace(
                        subscription_owner=self,
                        message=f"Automatic update of the connection parameters accepted the parameters "
                                f"for: {ble_device}",
                        trace_level=TraceLevel.DEBUG)
                    result = BleContextConnectionParameterUpdateRequestResult.ACCEPTED
                else:
                    TRACE_LOGGER.log_trace(
                        subscription_owner=self,
                        message=f"Automatic update of the connection parameters refused the parameters "
                                f"for: {ble_device}",
                        trace_level=TraceLevel.DEBUG)
                    result = BleContextConnectionParameterUpdateRequestResult.REJECTED
                # end if
                ble_device.ble_context_event_queue.put(BleContextEvent(
                    event_type=BleContextEventType.CONNECTION_PARAMETERS_UPDATE_REQUEST_RESULT,
                    event_data={BleContextEventDataType.CONNECTION_PARAMETERS_UPDATE_REQUEST_RESULT: result},
                    timestamp=timestamp))
            else:
                TRACE_LOGGER.log_trace(
                    subscription_owner=self,
                    message="L2CAP connection parameter update request event from an unknown device"
                            f"(connection handle {connection_handle})",
                    trace_level=TraceLevel.WARNING)
            # end if
        # end def treat_l2cap_connection_parameter_update_request_event

        def treat_keypress_notification(event_data, timestamp):
            """
            Treat a pairing keypress event received in the event thread

            :param event_data: The dictionary representing the event data
            :type event_data: ``dict``
            :param timestamp: Monotonic timestamp in nanoseconds
            :type timestamp: ``int``
            """
            connection_handle = event_data["connection_handle"]
            action = BleSmpKeypress(event_data["action"])

            ble_device: NrfBleLibBleContextDevice = connected_devices.get(connection_handle, None)

            if ble_device is not None:
                # if in an error state further notification are ignored
                if ble_device.bonding_state[0] == BleDeviceBondingStates.ERROR:
                    return
                # end if

                log_trace(
                    message=f"Received keypress notification action {action} "
                            f"sent by device {ble_device.address}),  at {timestamp}",
                    trace_level=TraceLevel.INFO)

                match action:
                    case BleSmpKeypress.PASSKEY_ENTRY_STARTED:
                        if ble_device.bonding_state[0] == BleDeviceBondingStates.STARTED:
                            ble_device.bonding_state = (BleDeviceBondingStates.KEY_PASS_BONDING, 0)
                        else:
                            ble_device.bonding_state = (BleDeviceBondingStates.ERROR,
                                                        "key press start notification "
                                                        f"when in state {ble_device.bonding_state}")
                        # end if
                    case BleSmpKeypress.PASSKEY_DIGIT_ENTERED:
                        if ble_device.bonding_state[0] == BleDeviceBondingStates.KEY_PASS_BONDING:
                            ble_device.bonding_state = (BleDeviceBondingStates.KEY_PASS_BONDING,
                                                        int(ble_device.bonding_state[1])+1)
                        else:
                            ble_device.bonding_state = (BleDeviceBondingStates.ERROR,
                                                        "key press digit entered notification "
                                                        f"when in state {ble_device.bonding_state}")
                        # end if
                    case BleSmpKeypress.PASSKEY_DIGIT_ERASED:
                        if ble_device.bonding_state[0] == BleDeviceBondingStates.KEY_PASS_BONDING:
                            ble_device.bonding_state = (BleDeviceBondingStates.KEY_PASS_BONDING,
                                                        int(ble_device.bonding_state[1]) - 1)
                        else:
                            ble_device.bonding_state = (BleDeviceBondingStates.ERROR,
                                                        "key press digit erased notification "
                                                        f"when in state {ble_device.bonding_state}")
                        # end if
                    case BleSmpKeypress.PASSKEY_CLEARED:
                        if ble_device.bonding_state[0] == BleDeviceBondingStates.KEY_PASS_BONDING:
                            ble_device.bonding_state = (BleDeviceBondingStates.KEY_PASS_BONDING, 0)
                        else:
                            ble_device.bonding_state = (BleDeviceBondingStates.ERROR,
                                                        "key press digit cleared notification "
                                                        f"when in state {ble_device.bonding_state}")
                        # end if
                    case BleSmpKeypress.PASSKEY_ENTRY_COMPLETE:
                        if ble_device.bonding_state[0] == BleDeviceBondingStates.KEY_PASS_BONDING:
                            ble_device.bonding_state = (BleDeviceBondingStates.KEY_PASS_BONDING_COMPLETE,
                                                        ble_device.bonding_state[1])
                        else:
                            ble_device.bonding_state = (BleDeviceBondingStates.ERROR,
                                                        "key press entry complete notification "
                                                        f"when in state {ble_device.bonding_state}")
                        # end if
                    case _:
                        log_trace(
                            message=f"Unhandled keypress notification action {action} sent by device, "
                                    f"address type({event_data['address_type']}), address({event_data['address']}),",
                            trace_level=TraceLevel.ERROR)
                # end match

                pairing_event_queues[ble_device.address].put(action)
            # end if
        # end def treat_keypress_notification

        def treat_passkey_display_number(event_data, timestamp):
            """
            Treat a pass key display number notification, store the number in a map related to the context device

            :param event_data: The dictionary representing the event data
            :type event_data: ``dict``
            :param timestamp: Monotonic timestamp in nanoseconds
            :type timestamp: ``int``
            """
            connection_handle = event_data["connection_handle"]
            passkey = event_data["passkey"]

            ble_device = connected_devices.get(connection_handle, None)

            if ble_device is not None:
                ble_device.ble_context_event_queue.put(BleContextEvent(
                    event_type=BleContextEventType.DISPLAY_PASSKEY,
                    event_data={BleContextEventDataType.DISPLAY_PASSKEY_PASSKEY: passkey},
                    timestamp=timestamp))
                self._append_display_key_storage(ble_device.address, passkey)
            else:
                log_trace(
                    message="Received passkey display number report from an unknown device, connection"
                            f"handle({connection_handle}),address type({event_data['address_type']}),"
                            f" address({event_data['address']}), passkey({passkey}) at {timestamp}ns",
                    trace_level=TraceLevel.WARNING)
            # end if
        # end def treat_passkey_display_number

        def treat_pairing_started(event_data, timestamp):
            """
            Treat a pairing started notification

            :param event_data: The dictionary representing the event data
            :type event_data: ``dict``
            :param timestamp: Monotonic timestamp in nanoseconds
            :type timestamp: ``int``
            """
            connection_handle = event_data["connection_handle"]
            ble_device = connected_devices.get(connection_handle, None)

            if ble_device is not None:
                log_trace(f"Pairing Started for {ble_device} {event_data}, at {timestamp}", TraceLevel.INFO)

                match ble_device.bonding_state:
                    case (BleDeviceBondingStates.NO_BONDING, _):
                        ble_device.bonding_state = (BleDeviceBondingStates.STARTED, "")
                    case _:
                        ble_device.bonding_state = (BleDeviceBondingStates.ERROR,
                                                    f"Start received in while in state {ble_device.bonding_state:r}")
                # end match
            else:
                log_trace(
                    message=f"Pairing Started notification from an unknown device, connection"
                            f"handle({connection_handle}),address type({event_data['address_type']}),"
                            f" address({event_data['address']}, at {timestamp})",
                    trace_level=TraceLevel.WARNING)
            # end if
        # end def treat_pairing_started

        def treat_pairing_complete(event_data, timestamp):
            """
            Treat a pairing complete notification, store the status and
            an optional failure reason in a map related to the context device

            :param event_data: The dictionary representing the event data
            :type event_data: ``dict``
            :param timestamp: Monotonic timestamp in nanoseconds
            :type timestamp: ``int``
            """
            connection_handle = event_data["connection_handle"]
            status = event_data["status"]
            reason = event_data["reason"]

            ble_device = connected_devices.get(connection_handle, None)

            if ble_device is not None:
                if status == BleControllerErrorCodes.SUCCESS:
                    match ble_device.bonding_state:
                        case (BleDeviceBondingStates.KEY_PASS_BONDING_COMPLETE, _):
                            reason_string = "Passkey"
                        case _:
                            reason_string = "Unknown"
                    # end match
                    ble_device.bonding_state = (BleDeviceBondingStates.BONDED, reason_string)
                elif status == BleControllerErrorCodes.AUTHENTICATION_FAILURE:
                    reason_enum = BlePairingFailReason(reason)
                    ble_device.bonding_state = (BleDeviceBondingStates.FAILED, reason_enum)
                else:
                    ble_device.bonding_state = (BleDeviceBondingStates.FAILED, "Unhandled status")
                    log_trace(
                        message=f"Unhandled status {repr(BleControllerErrorCodes(status))} sent by device, "
                                f"address type({event_data['address_type']}), address({event_data['address']}),",
                        trace_level=TraceLevel.ERROR)
                # end if
            else:
                log_trace(
                    message="Received pairing complete event from an unknown device, connection "
                            f"handle({connection_handle}),address type({event_data['address_type']}),"
                            f" address({event_data['address']}), status([{status}], reason({reason}) at {timestamp}ns",
                    trace_level=TraceLevel.WARNING)
            # end if
        # end def treat_pairing_complete

        def treat_notification_indication_event(event_type, event):
            """
            Treat a notification/indication event

            :param event_type: The event type, can either be ``NrfBleLibProcessMessageType.NOTIFICATION_EVENT`` or
                               ``NrfBleLibProcessMessageType.INDICATION_EVENT``
            :type event_type: ``NrfBleLibProcessMessageType``
            :param event: The dictionary representing the event
            :type event: ``tuple``
            """
            assert event_type in [NrfBleLibProcessMessageType.NOTIFICATION_EVENT,
                                  NrfBleLibProcessMessageType.INDICATION_EVENT]

            # TODO error treatment
            event_arguments = NrfBleLibAsyncioProcess.get_message_arguments(message=event)

            if event_type == NrfBleLibProcessMessageType.NOTIFICATION_EVENT:
                connection_handle = event_arguments[NotificationEventArgsInd.CONNECTION_HANDLE]
                characteristic_handle = event_arguments[NotificationEventArgsInd.CHARACTERISTIC_HANDLE]
                data = event_arguments[NotificationEventArgsInd.NOTIFICATION_DATA]
                timestamp = event_arguments[NotificationEventArgsInd.TIMESTAMP]
                time_stamped_queues = notification_time_stamped_queues
                report_type = "notification"
            else:
                # Indication
                connection_handle = event_arguments[IndicationEventArgsInd.CONNECTION_HANDLE]
                characteristic_handle = event_arguments[IndicationEventArgsInd.CHARACTERISTIC_HANDLE]
                data = event_arguments[IndicationEventArgsInd.INDICATION_DATA]
                timestamp = event_arguments[IndicationEventArgsInd.TIMESTAMP]
                time_stamped_queues = indication_time_stamped_queues
                report_type = "indication"
            # end if

            ble_device: NrfBleLibBleContextDevice = connected_devices.get(connection_handle, None)

            if ble_device is not None:
                address = ble_device.address
                ble_message = BleMessage(data=HexList(data), timestamp=timestamp)
                log_trace(
                    message=f"Received {report_type} report from address({address.address}), connection "
                            f"handle({connection_handle}), char_handle({characteristic_handle}), "
                            f"data({HexList(data)}) at {timestamp}ns",
                    trace_level=TraceLevel.INFO)

                connection_queues = time_stamped_queues.get(address, None)
                if connection_queues is not None:
                    queue = connection_queues.get(characteristic_handle, None)
                    if queue is not None:
                        log_trace(
                            message=f"Put in queue {report_type} report from address({address.address}), connection "
                                    f"handle({connection_handle}), char_handle({characteristic_handle}), "
                                    f"data({HexList(data)}) at {timestamp}ns",
                            trace_level=TraceLevel.DEBUG)
                        queue.put(ble_message)
                    # end if
                # end if

                transfer_callback = ble_device.get_transfer_callback(transfer_type_key=characteristic_handle)
                if transfer_callback is not None:
                    log_trace(
                        message=f"Call {report_type} callback for report from address({address}), connection "
                                f"handle({connection_handle}), char_handle({characteristic_handle}), "
                                f"data({HexList(data)}) at {timestamp}ns",
                        trace_level=TraceLevel.DEBUG)
                    transfer_callback(transport_message=ble_message)
                # end if
            else:
                log_trace(
                    message=f"Received {report_type} report from an unknown device, connection "
                            f"handle({connection_handle}), char_handle({characteristic_handle}), data({HexList(data)}) "
                            f"at {timestamp}ns",
                    trace_level=TraceLevel.WARNING)
            # end if
        # end def treat_notification_indication_event

        def run():
            """
            Run method for the event thread
            """
            running = True
            consecutive_exception_count = 0
            while running:
                event = event_queue.get()
                try:
                    # check callbacks and logging
                    match event:
                        case (NrfBleLibProcessMessageType.NRF_BLE_LIB_EVENT,
                              ({"type": nrf_ble_lib_event_type, "timestamp": timestamp,
                                "event_data": data},)):
                            log_trace(f"NRF_BLE_LIB_EVENT {nrf_ble_lib_event_type} received at {timestamp}",
                                      trace_level=TraceLevel.DEBUG)
                            if nrf_ble_lib_event_type in callbacks.keys():
                                callbacks[nrf_ble_lib_event_type](event_data=data, timestamps=timestamp)
                            # end if
                        case (event_type, _):
                            if event_type in callbacks.keys():
                                callbacks[event_type](event_type=event_type, event=event)
                            # end if
                    # end match

                    # treat event
                    match event:
                        case NrfBleLibBleContext.STOP_EVENT_THREAD_SIGNAL:
                            running = False
                        case (NrfBleLibProcessMessageType.NRF_BLE_LIB_EVENT,
                              ({"type": "le_connection_complete", "timestamp": timestamp, "event_data": data},)):
                            treat_connection_event(event_data=data, timestamp=timestamp)
                        case (NrfBleLibProcessMessageType.NRF_BLE_LIB_EVENT,
                              ({"type": "hci_disconnection_complete", "timestamp": timestamp, "event_data": data},)):
                            treat_disconnection_event(event_data=data, timestamp=timestamp)
                        case (NrfBleLibProcessMessageType.NRF_BLE_LIB_EVENT,
                              ({"type": "hci_command_complete", "timestamp": timestamp, "event_data": data},)):
                            treat_hci_command_complete_event(event_data=data, timestamp=timestamp)
                        case (NrfBleLibProcessMessageType.NRF_BLE_LIB_EVENT,
                              ({"type": "le_connection_update_complete", "timestamp": timestamp, "event_data": data},)):
                            treat_connection_update_complete(event_data=data, timestamp=timestamp)
                        case (NrfBleLibProcessMessageType.NRF_BLE_LIB_EVENT,
                              ({"type": "sm_keypress_notification", "timestamp": timestamp, "event_data": data},)):
                            treat_keypress_notification(event_data=data, timestamp=timestamp)
                        case (NrfBleLibProcessMessageType.NRF_BLE_LIB_EVENT,
                              ({"type": "sm_passkey_display_number", "timestamp": timestamp, "event_data": data},)):
                            treat_passkey_display_number(event_data=data, timestamp=timestamp)
                        case (NrfBleLibProcessMessageType.NRF_BLE_LIB_EVENT,
                              ({"type": "sm_pairing_started", "timestamp": timestamp, "event_data": data},)):
                            treat_pairing_started(event_data=data, timestamp=timestamp)
                        case (NrfBleLibProcessMessageType.NRF_BLE_LIB_EVENT,
                              ({"type": "sm_pairing_complete", "timestamp": timestamp, "event_data": data}, )):
                            treat_pairing_complete(event_data=data, timestamp=timestamp)
                        case (NrfBleLibProcessMessageType.NOTIFICATION_EVENT, _):
                            treat_notification_indication_event(
                                event_type=NrfBleLibProcessMessageType.NOTIFICATION_EVENT, event=event)
                        case (NrfBleLibProcessMessageType.INDICATION_EVENT, _):
                            treat_notification_indication_event(
                                event_type=NrfBleLibProcessMessageType.INDICATION_EVENT, event=event)
                        case (NrfBleLibProcessMessageType.L2CAP_CONNECTION_PARAMETER_UPDATE_REQUEST_EVENT, _):
                            treat_l2cap_connection_parameter_update_request_event(event=event)
                        case (NrfBleLibProcessMessageType.PAIRED_EVENT, _):
                            print(event)
                        case (NrfBleLibProcessMessageType.ERROR_EVENT, _):
                            # TODO error treatment
                            log_trace("Error event received: "
                                      f"{NrfBleLibAsyncioProcess.get_message_arguments(message=event)}\n",
                                      TraceLevel.ERROR)
                        case (NrfBleLibProcessMessageType.CRITICAL_ERROR_EVENT, _):
                            log_trace("Critical error event received, stopping the event thread: "
                                      f"{NrfBleLibAsyncioProcess.get_message_arguments(message=event)}\n",
                                      TraceLevel.ERROR)
                            running = False
                            connected_devices.clear()
                            context_object = weak_self()
                            if context_object is not None:
                                context_object._event_thread = None
                                context_object.is_open = False
                            # end if
                            del context_object
                        case (NrfBleLibProcessMessageType.LOG_EVENT, _):
                            event_arguments = NrfBleLibAsyncioProcess.get_message_arguments(message=event)
                            log_trace("[log event from process] " + event_arguments[LogEventArgsInd.LOG_MESSAGE],
                                      event_arguments[LogEventArgsInd.LOG_LEVEL])
                        case _:
                            log_trace(f"Unknown event received {event}", TraceLevel.WARNING)
                    # end match

                    # Reset the consecutive exception count because no exceptions arise for this event
                    consecutive_exception_count = 0
                except Exception as e:
                    consecutive_exception_count += 1
                    if consecutive_exception_count > NrfBleLibAsyncioProcess.PROCESS_CONSECUTIVE_ERROR_MAX_COUNT:
                        # TODO error treatment
                        log_trace(message=f"[nrf-ble-lib event thread] Critical error (too many consecutive error): "
                                          f"{type(e)} {e}",
                                  trace_level=TraceLevel.WARNING)
                        try:
                            # Stopping the process will disconnect all connected devices
                            nrf_ble_lib_process.stop_process()
                        finally:
                            connected_devices.clear()
                            context_object = weak_self()
                            if context_object is not None:
                                context_object._event_thread = None
                                context_object.is_open = False
                            # end if
                            del context_object
                        # end try
                        raise
                    else:
                        # TODO error treatment
                        log_trace(message=f"[nrf-ble-lib event thread] Error : {type(e)} {e}",
                                  trace_level=TraceLevel.WARNING)
                    # end if
                # end try
            # end while
        # end def run

        return run
    # end def _get_nrf_ble_lib_event_thread_method

    def _characteristic_write(self, ble_context_device, characteristic, data, characteristic_write_type):
        """
        Common method for characteristic write

        :param ble_context_device: The BLE device to disconnect from
        :type ble_context_device: ``NrfBleLibBleContextDevice``
        :param characteristic: Characteristic object to use to send data
        :type characteristic: ``BleCharacteristic``
        :param data: The data to send
        :type data: ``HexList``
        :param characteristic_write_type: Type of write operation
        :type characteristic_write_type: ``WriteOperation``

        :raise ``TransportContextException``: If the context is not open, the device is not connected, or the write
                                              operation failed
        """
        if not self.is_open:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_NOT_OPEN)
        # end if

        if ble_context_device.nrf_ble_lib_connection_handle is None:
            raise TransportContextException(TransportContextException.Cause.DEVICE_NOT_CONNECTED,
                                            f"Device {ble_context_device.address} is not connected")
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message=f"Writing ({characteristic_write_type}) {data} on characteristic {characteristic.short_string()} "
                    f"on device {ble_context_device.address}...",
            trace_level=TraceLevel.EXTRA_DEBUG)

        # TODO add timeout
        response = self._nrf_ble_lib_process.send_request_wait_for_response(
            request_type=NrfBleLibProcessMessageType.CHARACTERISTIC_WRITE_REQUEST,
            request_arguments=(ble_context_device.nrf_ble_lib_connection_handle,
                               NrfBleLibStructureTranslator.get_driver_characteristic(
                                   interface_characteristic=characteristic), characteristic_write_type, data))

        # TODO add a timestamp gotten in the process and added in the response
        response_timestamp = perf_counter_ns()

        if NrfBleLibAsyncioProcess.get_message_type(message=response) in ERROR_TYPES:
            error_args = NrfBleLibAsyncioProcess.get_message_arguments(message=response)
            if len(error_args) >= 3 and (error_args[2] & 0xFFFF0000) == ErrorId.TRANSPORT_CONTEXT_EXCEPTION:
                if len(error_args) >= 4:
                    raise TransportContextException(
                        TransportContextException.Cause(error_args[2] & 0xFF), *error_args[3])
                else:
                    raise TransportContextException(TransportContextException.Cause(error_args[2] & 0xFF))
                # end if
            # end if
            # TODO error treatment and add it to the raised exception
            raise TransportContextException(
                TransportContextException.Cause.CONTEXT_INTERNAL_ERROR,
                f"Characteristic write to the device {ble_context_device.address} FAILED: {response}")
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message=f"Characteristic ({characteristic.short_string()}) write ({characteristic_write_type.value}) "
                    f"to the device {ble_context_device.address.address}: {data} at {response_timestamp}ns",
            trace_level=TraceLevel.INFO)
    # end def _characteristic_write

    def _update_nrf_ble_lib_central_gatt_table(self, gatt_table, exception_message):
        """
        Send the central GATT table to the nrf-ble-lib process to update it on the hardware

        :param gatt_table: Gatt table to send to the nrf-ble-lib process
        :type gatt_table: ``list[BleService]``
        :param exception_message: Exception message to use if there is an error when updating the GATT table
        :type exception_message: ``str``

        :raise ``TransportContextException``: If the update operation failed
        """
        # TODO add timeout
        response = self._nrf_ble_lib_process.send_request_wait_for_response(
            request_type=NrfBleLibProcessMessageType.UPDATE_GATT_TABLE_REQUEST, request_arguments=(gatt_table,))

        if NrfBleLibAsyncioProcess.get_message_type(message=response) in ERROR_TYPES:
            # TODO error treatment and add it to the raised exception
            raise TransportContextException(TransportContextException.Cause.CONTEXT_INTERNAL_ERROR, exception_message +
                                            f": {response}")
        # end if
    # end def _update_nrf_ble_lib_central_gatt_table

    # ------------------------------------------------------------------------------------------------------------------
    # BleContext methods
    # ------------------------------------------------------------------------------------------------------------------
    def _set_connection_parameters_range(self, value):
        """
        Internal method for the property setter of connection_parameters_range. This was done to be able to easily
        override it in a child class.

        :param value: connection_parameter_range value
        :type value: ``BleGapConnectionParametersRange`` or ``None``

        :raise ``AssertionError``: If ``value`` is not a ``BleGapConnectionParametersRange`` or ``None``
        """
        if not self.is_open:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_NOT_OPEN)
        # end if

        super()._set_connection_parameters_range(value=value)

        if value is None:
            # Put values that will always refuse the update request
            value = BleGapConnectionParametersRange(
                min_connection_interval=0, max_connection_interval=0, min_supervision_timeout=0,
                max_supervision_timeout=0, min_slave_latency=0, max_slave_latency=0)
        # end if

        # TODO add timeout
        response = self._nrf_ble_lib_process.send_request_wait_for_response(
            request_type=NrfBleLibProcessMessageType.SET_CONNECTION_PARAMETERS_RANGE_REQUEST,
            request_arguments=(value,))

        if NrfBleLibAsyncioProcess.get_message_type(message=response) in ERROR_TYPES:
            # TODO error treatment
            raise TransportContextException(
                TransportContextException.Cause.CONTEXT_INTERNAL_ERROR,
                f"Setting connection parameters range FAILED: {response}")
        # end if
    # end def property setter _set_connection_parameters_range

    def update_device_list(self):
        # See ``BleContext.update_device_list``
        # Do nothing since this type of BleContext is updating the connected device automatically
        pass
    # end def update_device_list

    def get_devices(self, index_in_cache=None, address=None, *args, **kwargs):
        """
        Get context devices in the cache. Multiple filters can be used:

        * If index_in_cache is given, address is ignored and the index in the cache is used to get the device
        * If address is given, the function returns the device (there should be only one normally) with this BLE
        address in the cache
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
        return []
    # end def get_devices

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def open(self):
        """
        Open the transport context.

        :raise ``TransportContextException``: If the BLE context class is doomed, if the nrf-ble-lib process is
                                              already running or if the nrf-ble-lib event thread is already running
        """
        if not self.is_open:
            TRACE_LOGGER.log_trace(
                subscription_owner=self, message=f"Opening {self.__class__.__name__}...", trace_level=TraceLevel.DEBUG)

            # Sanity checks
            if self._nrf_ble_lib_process.is_process_alive():
                raise TransportContextException(TransportContextException.Cause.CONTEXT_INTERNAL_ERROR,
                                                f"The nrf-ble-lib process is already running")
            # end if
            if self._event_thread is not None and self._event_thread.is_alive():
                raise TransportContextException(TransportContextException.Cause.CONTEXT_INTERNAL_ERROR,
                                                f"The nrf-ble-lib event thread is already running")
            # end if

            self._event_thread = Thread(target=self._get_nrf_ble_lib_event_thread_method())
            # The thread is a daemon: It will NOT prevent the main thread from dying
            self._event_thread.setDaemon(True)
            self._event_thread.start()

            self._nrf_ble_lib_process.start_process()

            self.is_open = True

            # Start with an empty GATT table
            self.reset_central_gatt_table()
            self.connection_parameters_range = None
        # end if
    # end def open

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def close(self):
        # See ``BleContext.close``
        if self.is_open:
            TRACE_LOGGER.log_trace(
                subscription_owner=self, message=f"Closing {self.__class__.__name__}...", trace_level=TraceLevel.DEBUG)

            try:
                self._stop_event_thread()
                # Stopping the process will disconnect all connected devices
                self._nrf_ble_lib_process.stop_process()
            finally:
                self._scan_filters.clear_filters()
                self._connected_devices.clear()
                self._event_thread = None
                self.is_open = False
            # end try
        # end if
    # end def close

    def reset(self):
        # See ``BleContext.reset``
        # Reset the hardware, this action will also close the context
        self.close()
        self.open()
    # end def reset

    def add_service_to_central_gatt_table(self, service):
        """
        Add a service to the GATT table of the central of this context. The service structure given should have all
        substructures in it (characteristics, descriptors, ...). This method will add all of it to the GATT table.

        :param service: Complete structure of the service to add
        :type service: ``BleService``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        if not self.is_open:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_NOT_OPEN)
        # end if

        # Since the services in the current cache will not be modified, a simple copy is enough
        gatt_table_to_send = self._central_gatt_table.copy()
        gatt_table_to_send.append(service)

        self._update_nrf_ble_lib_central_gatt_table(
            gatt_table=gatt_table_to_send,
            exception_message=f"Adding a service to the central GATT table FAILED, service: {service}")

        self._central_gatt_table = gatt_table_to_send
    # end def add_service_to_central_gatt_table

    def reset_central_gatt_table(self):
        """
        Remove everything from the GATT table of the central of this context.

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        if not self.is_open:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_NOT_OPEN)
        # end if

        self._update_nrf_ble_lib_central_gatt_table(
            gatt_table=[], exception_message="Resetting the central GATT table FAILED")

        self._central_gatt_table = []
    # end def reset_central_gatt_table

    def is_central_gatt_table_empty(self):
        """
        Check if the GATT table of the central of this context is empty.

        :return: Flag indicating if the central's GATT table is empty
        :rtype: ``bool``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        if not self.is_open:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_NOT_OPEN)
        # end if

        return len(self._central_gatt_table) == 0
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
        if not self.is_open:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_NOT_OPEN)
        # end if

        return any([service.uuid == service_uuid for service in self._central_gatt_table])
    # end def is_service_in_central_gatt_table

    def scan(self, scan_time=BleContext.GENERIC_SCAN_TIME, send_scan_request=False, scan_interval=None,
             scan_window=None, event_to_wait_on=None, exception_if_wait_failed=None):
        """
        Scan for a set time. This is a blocking method. It will return the advertising packets (and scan response
        if requested).

        WARNING: nrf-ble-lib only works with integer for scan time, therefore it is round to the upper integer
                 value.

        :param scan_time: The scan time in seconds - OPTIONAL
        :type scan_time: ``int`` or ``float``
        :param send_scan_request: Flag indicating if scan responses are requested, unused for now - OPTIONAL
        :type send_scan_request: ``bool``
        :param scan_interval: Interval in ms between scan window, unused for now - OPTIONAL
        :type scan_interval: ``int`` or ``float`` or ``None``
        :param scan_window: Scan window in ms - OPTIONAL
        :type scan_window: ``int`` or ``float`` or ``None``
        :param event_to_wait_on: Event to wait on after starting the scan, unused for now - OPTIONAL
        :type event_to_wait_on: ``Event`` or ``None``
        :param exception_if_wait_failed: Exception to raise if the wait on ``event_to_wait_on`` fails, unused for
                                         now - OPTIONAL
        :type exception_if_wait_failed: ``Exception`` or ``None``

        :return: List of ble device scanned with their associated advertising packet (and optionally scan response)
        :rtype: ``list[NrfBleLibBleContextDevice]``

        :raise ``TransportContextException``: If context is not open or if an exception from nrf-ble-lib is raised
        """
        if not self.is_open:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_NOT_OPEN)
        # end if

        # TODO group scanning parameters in a class instead of arguments of this method and verify the values validity
        # Issue link: https://jira.logitech.io/browse/PTB-3075

        if scan_interval is None:
            scan_interval = BleScanIntervalWindowRange.INTERVAL_WINDOW_MAX if scan_time > 10 else scan_time*1000
        # end if

        if scan_window is None:
            scan_window = BleScanIntervalWindowRange.INTERVAL_WINDOW_MAX if scan_time > 10 else scan_time*1000
        # end if

        scan_parameters = {
            "scan_type": BleScanType.ACTIVE_SCANNING if send_scan_request else BleScanType.PASSIVE_SCANNING,
            "scan_interval": int(scan_interval / BleGenericFloatConstant.SCAN_INTERVAL_WINDOWS_GRANULARITY),
            "scan_window": int(scan_window / BleGenericFloatConstant.SCAN_INTERVAL_WINDOWS_GRANULARITY),
            "scanning_filter_policy": BleScanningFilterPolicy.BASIC_UNFILTERED,
        }

        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message=f"Scanning for devices...",
            trace_level=TraceLevel.EXTRA_DEBUG)

        # add extra time on the timeout, as the start procedure takes time. extra time scales
        # with the total scan time but cannot be shorter than the scan start timeout.
        scan_timeout = scan_time + max(0.5 * scan_time, NrfBleLibProcessUtil.SCAN_START_STOP_TIMEOUT)
        try:
            # TODO add error treatment
            response = self._nrf_ble_lib_process.send_request_wait_for_response(
                request_type=NrfBleLibProcessMessageType.SCAN_REQUEST,
                request_arguments=(scan_parameters, self._scan_filters, scan_time), timeout=scan_timeout)
        except Empty:
            self._nrf_ble_lib_process.send_request_wait_for_response(
                request_type=NrfBleLibProcessMessageType.SCAN_STOP_REQUEST)
            raise TransportContextException(TransportContextException.Cause.CONTEXT_INTERNAL_ERROR,
                                            f"Process did not stop scanning in time, scan_time = {scan_time}, "
                                            "scan_timeout = scan_time + max(0.5 * scan_time, "
                                            f"{NrfBleLibProcessUtil.SCAN_START_STOP_TIMEOUT}) = {scan_timeout}")
        # end try

        devices_scanned = self._extract_scanning_result(response)

        return devices_scanned
    # end def scan

    def _extract_scanning_result(self, response):
        """
        Extract and parse scanning result coming from the process (advertising data and scan response),
        returns a list of devices

        :param response: a response from the process
        :type response: ``tuple``

        :return: List of ble device scanned with their associated advertising packet (and optionally scan response)
        :rtype: ``list[NrfBleLibBleContextDevice]``
        """
        if NrfBleLibAsyncioProcess.get_message_type(message=response) in ERROR_TYPES:
            # TODO error treatment and add it to the raised exception
            raise TransportContextException(TransportContextException.Cause.CONTEXT_INTERNAL_ERROR,
                                            f"Scanning FAILED: {response}")
        # end if
        arguments = NrfBleLibAsyncioProcess.get_message_arguments(message=response)
        devices_scanned_by_process: Dict[BleGapAddress, list] = arguments[ScanStartResponseArgsInd.DEVICE_SCANNED_DICT]
        devices_scanned = []
        for device_address, device_adv_info in devices_scanned_by_process.items():
            advertising_data_list = []
            scan_response_list = []
            for i, advertising_data_raw in enumerate(device_adv_info[DeviceAdvertisingInformationIndex.ADVERTISING_DATA]):
                advertising_data = BleAdvertisingData.from_list(
                    advertising_data_list=advertising_data_raw,
                    timestamp=device_adv_info[DeviceAdvertisingInformationIndex.ADVERTISING_TIMESTAMPS][i][0])
                for timestamp in device_adv_info[DeviceAdvertisingInformationIndex.ADVERTISING_TIMESTAMPS][i][1:]:
                    advertising_data.add_timestamp(timestamp=timestamp)
                # end for
                advertising_data_list.append(advertising_data)
            # end for
            if device_adv_info[DeviceAdvertisingInformationIndex.SCAN_RESPONSE_DATA] is not None:
                for i, scan_response_raw in enumerate(device_adv_info[DeviceAdvertisingInformationIndex.SCAN_RESPONSE_DATA]):
                    if scan_response_raw is not None:
                        scan_response = BleAdvertisingData.from_list(
                            advertising_data_list=scan_response_raw,
                            timestamp=device_adv_info[DeviceAdvertisingInformationIndex.SCAN_RESPONSE_TIMESTAMPS][i][0])
                        for timestamp in device_adv_info[DeviceAdvertisingInformationIndex.SCAN_RESPONSE_TIMESTAMPS][i][1:]:
                            scan_response.add_timestamp(timestamp=timestamp)
                        # end for
                    else:
                        scan_response = None
                    # end if
                    scan_response_list.append(scan_response)
                # end for
            # end if
            devices_scanned.append(NrfBleLibBleContextDevice(
                address=device_address,
                advertising_type=device_adv_info[DeviceAdvertisingInformationIndex.ADVERTISING_TYPE],
                advertising_data=advertising_data_list, scan_response=scan_response_list))
        # end for
        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message=f"Scanned for devices: {devices_scanned}",
            trace_level=TraceLevel.INFO)
        return devices_scanned
    # end def _extract_scanning_result

    def start_scan(self, scan_time=BleContext.GENERIC_SCAN_TIME, send_scan_request=False, scan_interval=None, scan_window=None):
        # see ``BleContext.start_scan``

        if not self.is_open:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_NOT_OPEN)
        # end if
        # TODO group scanning parameters in a class instead of arguments of this method and verify the values validity
        # Issue link: https://jira.logitech.io/browse/PTB-3075

        if scan_interval is None:
            scan_interval = BleScanIntervalWindowRange.INTERVAL_WINDOW_MAX if scan_time > 10 else scan_time * 1000
        # end if

        if scan_window is None:
            scan_window = BleScanIntervalWindowRange.INTERVAL_WINDOW_MAX if scan_time > 10 else scan_time * 1000
        # end if

        scan_parameters = {
            "scan_type": BleScanType.ACTIVE_SCANNING if send_scan_request else BleScanType.PASSIVE_SCANNING,
            "scan_interval": int(scan_interval / BleGenericFloatConstant.SCAN_INTERVAL_WINDOWS_GRANULARITY),
            "scan_window": int(scan_window / BleGenericFloatConstant.SCAN_INTERVAL_WINDOWS_GRANULARITY),
            "scanning_filter_policy": BleScanningFilterPolicy.BASIC_UNFILTERED,
        }

        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message=f"Asynchronous scanning for devices...",
            trace_level=TraceLevel.DEBUG)

        self._nrf_ble_lib_process.send_request(
            request_type=NrfBleLibProcessMessageType.SCAN_REQUEST,
            request_arguments=(scan_parameters, copy(self._scan_filters), scan_time))
        # explicit copy of scan filters to ensure the current state is sent to the process
    # end def start_scan

    def scan_for_devices(self, ble_addresses=None, manufacturer_data_company_id=None,
                         scan_time=BleContext.GENERIC_SCAN_TIME, send_scan_request=False):
        """
        Scan for specific devices. This is a blocking method.

        :param ble_addresses: List of BLE device addresses to get - OPTIONAL
        :type ble_addresses: ``list[BleGapAddress]`` or ``None``
        :param manufacturer_data_company_id: The company ID in the advertising manufacturer data (in big endian), some
                                             values can be found in ``ManufacturerDataCompanyId`` - OPTIONAL
        :type manufacturer_data_company_id: ``int`` or ``None``
        :param scan_time: The scan time - OPTIONAL
        :type scan_time: ``int`` or ``float``
        :param send_scan_request: Flag indicating if scan responses are requested, unused for now - OPTIONAL
        :type send_scan_request: ``bool``

        :return: List of ble device scanned with their associated advertising packet (and optionally scan response)
        :rtype: ``list[NrfBleLibBleContextDevice]``

        :raise ``TransportContextException``: If context is not open or if an exception from nrf-ble-lib is raised
        """
        if not self.is_open:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_NOT_OPEN)
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message=f"Scanning for devices, param: address = {ble_addresses}, "
                    f"manufacturer_data_company_id = {manufacturer_data_company_id}...",
            trace_level=TraceLevel.EXTRA_DEBUG)

        try:
            self._scan_filters.clear_filters()

            if ble_addresses is not None:
                self._scan_filters.expected_addresses = ble_addresses
            # end if

            if manufacturer_data_company_id is not None:
                self._scan_filters.expected_company_id = manufacturer_data_company_id
            # end if

            return self.scan(scan_time=scan_time, send_scan_request=send_scan_request)
        finally:
            self._scan_filters.clear_filters()
        # end try
    # end def scan_for_devices

    def scan_for_first_device_found(self, ble_addresses=None, manufacturer_data_company_id=None,
                                    scan_timeout=BleContext.GENERIC_SCAN_TIME, send_scan_request=False):
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
        :param send_scan_request: Flag indicating if scan responses are requested, unused for now - OPTIONAL
        :type send_scan_request: ``bool``

        :return: The first ble device found with its associated advertising packet (and optionally scan response)
        :rtype: ``NrfBleLibBleContextDevice``

        :raise ``TransportContextException``: If context is not open, if no device is found or if an exception from
                                              nrf-ble-lib is raised
        """
        if not self.is_open:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_NOT_OPEN)
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message=f"Scanning for the first device found, param: address = {ble_addresses}, "
                    f"manufacturer_data_company_id = {manufacturer_data_company_id}...",
            trace_level=TraceLevel.EXTRA_DEBUG)

        try:
            self._scan_filters.clear_filters()

            if send_scan_request:
                self._scan_filters.stop_at_first_scan_response = True
            else:
                self._scan_filters.stop_at_first_advertising = True
            # end if

            if ble_addresses is not None:
                self._scan_filters.expected_addresses = ble_addresses
            # end if

            if manufacturer_data_company_id is not None:
                self._scan_filters.expected_company_id = manufacturer_data_company_id
            # end if

            devices_scanned = self.scan(scan_time=scan_timeout, send_scan_request=send_scan_request)

            if len(devices_scanned) == 0:
                raise TransportContextException(
                    TransportContextException.Cause.DEVICE_NOT_FOUND,
                    f"Could not find the device with param: {ble_addresses}, "
                    f"manufacturer_data_company_id = {manufacturer_data_company_id}")
            # end if

            device_found = devices_scanned[0]

            TRACE_LOGGER.log_trace(
                subscription_owner=self,
                message=f"Device found: {device_found}",
                trace_level=TraceLevel.DEBUG)

            return device_found
        finally:
            self._scan_filters.clear_filters()
        # end try
    # end def scan_for_first_device_found

    def start_scan_for_device(self, ble_addresses=None, manufacturer_data_company_id=None, scan_time=BleContext.GENERIC_SCAN_TIME,
                              send_scan_request=False):
        # see ``BleContext.start_scan_for_device``

        # TODO check no scan are already running
        # issue link: https://jira.logitech.io/browse/PTB-3076

        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message=f"Asynchronous scanning for devices, param: address = {ble_addresses}, "
                    f"manufacturer_data_company_id = {manufacturer_data_company_id}...",
            trace_level=TraceLevel.EXTRA_DEBUG)

        try:
            self._scan_filters.clear_filters()

            if ble_addresses is not None:
                self._scan_filters.expected_addresses = ble_addresses
            # end if

            if manufacturer_data_company_id is not None:
                self._scan_filters.expected_company_id = manufacturer_data_company_id
            # end if

            self.start_scan(scan_time=scan_time, send_scan_request=send_scan_request)
        finally:
            self._scan_filters.clear_filters()
        # end try
    # end def start_scan_for_device

    def start_scan_for_first_device_found(self, ble_addresses=None, manufacturer_data_company_id=None,
                                          scan_timeout=BleContext.GENERIC_SCAN_TIME, send_scan_request=False):
        # see ``BleContext.start_scan_for_first_device_found``

        # TODO check no scan are already running
        # issue link: https://jira.logitech.io/browse/PTB-3076

        if not self.is_open:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_NOT_OPEN)
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message=f"Scanning for the first device found, param: address = {ble_addresses}, "
                    f"manufacturer_data_company_id = {manufacturer_data_company_id}...",
            trace_level=TraceLevel.EXTRA_DEBUG)

        try:
            self._scan_filters.clear_filters()

            if send_scan_request:
                self._scan_filters.stop_at_first_scan_response = True
            else:
                self._scan_filters.stop_at_first_advertising = True
            # end if

            if ble_addresses is not None:
                self._scan_filters.expected_addresses = ble_addresses
            # end if

            if manufacturer_data_company_id is not None:
                self._scan_filters.expected_company_id = manufacturer_data_company_id
            # end if

            self.start_scan(scan_time=scan_timeout, send_scan_request=send_scan_request)
        finally:
            self._scan_filters.clear_filters()
        # end try
    # end def start_scan_for_first_device_found

    def get_scanning_result(self, timeout):
        # see ``BleContext.get_scanning_result``

        try:
            response = self._nrf_ble_lib_process.get_response(
                original_request_type=NrfBleLibProcessMessageType.SCAN_REQUEST,
                timeout=timeout + SCAN_FINISH_EXTRA_TIME
            )
        except queue.Empty:
            raise TransportContextException(TransportContextException.Cause.DEVICE_NOT_FOUND)
        # end try

        devices_scanned = self._extract_scanning_result(response)
        return devices_scanned
    # end def get_scanning_result

    def is_direct_advertising_device_present(self, ble_context_device, scan_time=BleContext.GENERIC_SCAN_TIME):
        """
        Verify if a specific device is direct advertising. This is a blocking method.

        :param ble_context_device: The BLE device to connect to
        :type ble_context_device: ``NrfBleLibBleContextDevice``
        :param scan_time: The scan time - OPTIONAL
        :type scan_time: ``int`` or ``float``

        :return: Flag indicating if the wanted device has been found
        :rtype: ``bool``

        :raise ``TransportContextException``: If context is not open
        """
        if not self.is_open:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_NOT_OPEN)
        # end if

        # Since the address is used for advertising events, it will be faster to use the address as key in a dict even
        # if it seems a bit redundant (it should also not be None).
        if ble_context_device.address is None:
            raise TransportContextException(
                TransportContextException.Cause.DEVICE_UNKNOWN, "The address of the device to scan should not be None")
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message=f"Checking if the device {ble_context_device.address} is advertising in direct...",
            trace_level=TraceLevel.EXTRA_DEBUG)

        try:
            self._scan_filters.clear_filters()

            self._scan_filters.directed_device_address_to_find = ble_context_device.address

            devices_scanned = self.scan(scan_time=scan_time)

            is_device_found = len(devices_scanned) > 0 and devices_scanned[0].address == ble_context_device.address

            TRACE_LOGGER.log_trace(
                subscription_owner=self,
                message=f"Is the device {ble_context_device.address} advertising in direct: {is_device_found}",
                trace_level=TraceLevel.DEBUG)

            return is_device_found
        finally:
            self._scan_filters.clear_filters()
        # end try
    # end def is_direct_advertising_device_present

    def connect(self, ble_context_device, connection_parameters=None, timeout=BleContext.BLOCKING_DEFAULT_TIMEOUT,
                service_discovery=True, confirm_connect=False):
        """
        Connect to a device.

        :param ble_context_device: The BLE device to connect to
        :type ble_context_device: ``NrfBleLibBleContextDevice``
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

        :raise ``TransportContextException``: If context is not open, if the address of the device is unknown or if an
                                              exception from pc-ble-driver-py is raised
        """
        if not self.is_open:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_NOT_OPEN)
        # end if

        # Since the address is used for connect events, it will be faster to use the address as key in a dict even
        # if it seems a bit redundant (it should also not be None).
        if ble_context_device.address is None:
            raise TransportContextException(
                TransportContextException.Cause.DEVICE_UNKNOWN, "The address of the device to scan should not be None")
        # end if

        if ble_context_device.nrf_ble_lib_connection_handle is not None:
            raise TransportContextException(TransportContextException.Cause.ACTION_ALREADY_DONE,
                                            f"Device {ble_context_device.address} is already connected")
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=self, message=f"Connecting to the device {ble_context_device.address}...",
            trace_level=TraceLevel.EXTRA_DEBUG)

        untreated_connection_event = ble_context_device.ble_context_event_queue.clear_all_events_of_a_type(
            event_type=BleContextEventType.CONNECTION_EVENT)
        if len(untreated_connection_event) > 0:
            TRACE_LOGGER.log_trace(
                subscription_owner=self,
                message=f"Untreated connection event before connecting: {untreated_connection_event}",
                trace_level=TraceLevel.WARNING)
        # end if

        if confirm_connect:
            untreated_disconnection_event = ble_context_device.ble_context_event_queue.clear_all_events_of_a_type(
                event_type=BleContextEventType.DISCONNECTION_EVENT)
            if len(untreated_disconnection_event) > 0:
                TRACE_LOGGER.log_trace(
                    subscription_owner=self,
                    message=f"Untreated disconnection event before connecting: {untreated_disconnection_event}",
                    trace_level=TraceLevel.WARNING)
            # end if
        # end if

        request_arguments = (NrfBleLibStructureTranslator.get_driver_ble_gap_address(
            interface_ble_gap_address=ble_context_device.address),)

        if connection_parameters is not None:
            request_arguments += (NrfBleLibStructureTranslator.get_driver_connection_parameters(
                interface_connection_parameters=connection_parameters),)
        # end if

        with self._connecting_devices:
            self._connecting_devices[ble_context_device.address] = ble_context_device
        # end with

        try:
            start_connection_time = perf_counter_ns()

            # TODO add timeout
            response = self._nrf_ble_lib_process.send_request_wait_for_response(
                request_type=NrfBleLibProcessMessageType.CONNECT_REQUEST, request_arguments=request_arguments)

            if NrfBleLibAsyncioProcess.get_message_type(message=response) in ERROR_TYPES:
                # TODO error treatment
                TRACE_LOGGER.log_trace(
                    subscription_owner=self,
                    message=f"Connection to the device {ble_context_device.address} FAILED: {response}",
                    trace_level=TraceLevel.ERROR)
                return False
            # end if

            if timeout > 0:
                connection_event = ble_context_device.ble_context_event_queue.get_first_event_of_a_type(
                    event_type=BleContextEventType.CONNECTION_EVENT, timeout=timeout, skip_error=True)
                if connection_event is None:
                    TRACE_LOGGER.log_trace(
                        subscription_owner=self,
                        message=f"Connection to the device {ble_context_device.address} FAILED: timeout ({timeout}s)",
                        trace_level=TraceLevel.ERROR)
                    return False
                # end if

                if confirm_connect:
                    disconnection_event = ble_context_device.ble_context_event_queue.get_first_event_of_a_type(
                        event_type=BleContextEventType.DISCONNECTION_EVENT, timeout=self.CHECK_CONNECT_WORKED_TIMEOUT,
                        skip_error=True)
                    if disconnection_event is not None:
                        disconnect_time = (disconnection_event.timestamp -
                                           start_connection_time) / TIMESTAMP_UNIT_DIVIDER_MAP["ms"]

                        TRACE_LOGGER.log_trace(
                            subscription_owner=self,
                            message=f"Connection to the device {ble_context_device.address} "
                                    f"FAILED: auto-disconnect, it took {disconnect_time}ms",
                            trace_level=TraceLevel.ERROR)
                        return False
                    # end if
                # end if

                connect_time = (connection_event.timestamp - start_connection_time) / TIMESTAMP_UNIT_DIVIDER_MAP['ms']
                TRACE_LOGGER.log_trace(
                    subscription_owner=self,
                    message=f"Connected to the device {ble_context_device.address.address}, it took {connect_time}ms",
                    trace_level=TraceLevel.INFO)
            else:
                TRACE_LOGGER.log_trace(
                    subscription_owner=self, message=f"Connection to the device {ble_context_device.address.address} "
                                                     "started",
                    trace_level=TraceLevel.INFO)
            # end if
        finally:
            with self._connecting_devices:
                self._connecting_devices.pop(ble_context_device.address, None)
            # end with
        # end try

        if service_discovery:
            self.perform_service_discovery(ble_context_device=ble_context_device)
        # end if

        # create the queue for the device's pairing events
        self._pairing_event_queues[ble_context_device.address] = AioQueue()

        return True
    # end def connect

    def disconnect(self, ble_context_device, timeout=BleContext.BLOCKING_DEFAULT_TIMEOUT):
        """
        Disconnect from the current device.

        :param ble_context_device: The BLE device to disconnect from
        :type ble_context_device: ``NrfBleLibBleContextDevice``
        :param timeout: Timeout in seconds. If 0, it is a non-blocking operation - OPTIONAL
        :type timeout: ``int`` or ``float``

        :return: Flag indicating if the disconnect worked
        :rtype: ``bool``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        if not self.is_open:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_NOT_OPEN)
        # end if

        if ble_context_device.nrf_ble_lib_connection_handle is None:
            raise TransportContextException(TransportContextException.Cause.DEVICE_NOT_CONNECTED,
                                            f"Device {ble_context_device.address} is not connected")
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=self, message=f"Disconnecting from the device {ble_context_device.address}...",
            trace_level=TraceLevel.EXTRA_DEBUG)

        untreated_disconnection_event = ble_context_device.ble_context_event_queue.clear_all_events_of_a_type(
            event_type=BleContextEventType.DISCONNECTION_EVENT)
        if len(untreated_disconnection_event) > 0:
            TRACE_LOGGER.log_trace(
                subscription_owner=self,
                message=f"Unexpected disconnection event before disconnecting: {untreated_disconnection_event}",
                trace_level=TraceLevel.WARNING)
        # end if

        with self._disconnecting_devices:
            self._disconnecting_devices[ble_context_device.nrf_ble_lib_connection_handle] = ble_context_device
        # end with

        try:
            start_disconnection_time = perf_counter_ns()

            # TODO add timeout
            response = self._nrf_ble_lib_process.send_request_wait_for_response(
                request_type=NrfBleLibProcessMessageType.DISCONNECT_REQUEST,
                request_arguments=(ble_context_device.nrf_ble_lib_connection_handle,))

            if NrfBleLibAsyncioProcess.get_message_type(message=response) in ERROR_TYPES:
                # TODO error treatment
                TRACE_LOGGER.log_trace(
                    subscription_owner=self,
                    message=f"Disconnection from the device {ble_context_device.address} FAILED: {response}",
                    trace_level=TraceLevel.ERROR)
                return False
            # end if

            if timeout > 0:
                disconnection_event = ble_context_device.ble_context_event_queue.get_first_event_of_a_type(
                        event_type=BleContextEventType.DISCONNECTION_EVENT, timeout=timeout, skip_error=True)
                if disconnection_event is None:
                    TRACE_LOGGER.log_trace(
                        subscription_owner=self,
                        message=f"Disconnection from the device {ble_context_device.address} FAILED: "
                                f"timeout ({timeout}s)",
                        trace_level=TraceLevel.ERROR)
                    return False
                # end if

                disconnect_time = (disconnection_event.timestamp -
                                   start_disconnection_time) / TIMESTAMP_UNIT_DIVIDER_MAP['ms']
                TRACE_LOGGER.log_trace(
                    subscription_owner=self,
                    message=f"Disconnected from the device {ble_context_device.address.address}, it took {disconnect_time}ms",
                    trace_level=TraceLevel.INFO)
            else:
                TRACE_LOGGER.log_trace(
                    subscription_owner=self,
                    message=f"Disconnection to the device {ble_context_device.address.address} started",
                    trace_level=TraceLevel.INFO)
            # end if
        finally:
            with self._disconnecting_devices:
                self._disconnecting_devices.pop(ble_context_device.nrf_ble_lib_connection_handle, None)
            # end with
        # end try
        return True
    # end def disconnect

    def perform_service_discovery(self, ble_context_device, vendor_uuid_bases_to_add=None):
        """
        Perform service discovery on a connected device

        :param ble_context_device: The BLE device to perform service discovery on
        :type ble_context_device: ``NrfBleLibBleContextDevice``
        :param vendor_uuid_bases_to_add: A list of UUID base in form of list of int to add to the known table before
                                         the discovery - OPTIONAL
        :type vendor_uuid_bases_to_add: ``list[list[int]]`` or ``None``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        if not self.is_open:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_NOT_OPEN)
        # end if

        if ble_context_device.nrf_ble_lib_connection_handle is None:
            raise TransportContextException(TransportContextException.Cause.DEVICE_NOT_CONNECTED,
                                            f"Device {ble_context_device.address} is not connected")
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message=f"Performing service discovery on the device {ble_context_device.address}...",
            trace_level=TraceLevel.EXTRA_DEBUG)

        # TODO add timeout
        response = self._nrf_ble_lib_process.send_request_wait_for_response(
            request_type=NrfBleLibProcessMessageType.PERFORM_SERVICE_DISCOVERY_REQUEST,
            request_arguments=(ble_context_device.nrf_ble_lib_connection_handle,))

        if NrfBleLibAsyncioProcess.get_message_type(message=response) in ERROR_TYPES:
            error_args = NrfBleLibAsyncioProcess.get_message_arguments(message=response)
            if len(error_args) >= 3 and (error_args[2] & 0xFFFF0000) == ErrorId.TRANSPORT_CONTEXT_EXCEPTION:
                if len(error_args) >= 4:
                    raise TransportContextException(
                        TransportContextException.Cause(error_args[2] & 0xFF), *error_args[3])
                else:
                    raise TransportContextException(TransportContextException.Cause(error_args[2] & 0xFF))
                # end if
            # end if
            # TODO error treatment and add it to the raised exception
            raise TransportContextException(TransportContextException.Cause.CONTEXT_INTERNAL_ERROR,
                                            f"Discovering the device {ble_context_device.address}'s services "
                                            f"FAILED: {response}")
        # end if

        ble_context_device.gatt_table = NrfBleLibAsyncioProcess.get_message_arguments(message=response)[
            PerformServiceDiscoveryResponseArgsInd.GATT_TABLE]

        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message=f"Discovered the device {ble_context_device.address.address}'s services: {ble_context_device.gatt_table}",
            trace_level=TraceLevel.DEBUG)
    # end def perform_service_discovery

    def authenticate_just_works(self, ble_context_device, lesc=False):
        """
        Bond with a device, or encrypt communication with an already bonded device.

        :param ble_context_device: The BLE device to bond/encrypt with
        :type ble_context_device: ``NrfBleLibBleContextDevice``
        :param lesc: Flag indicating to permit LE secure connection
        :type lesc: ``bool``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        if not self.is_open:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_NOT_OPEN)
        # end if

        if ble_context_device.nrf_ble_lib_connection_handle is None:
            raise TransportContextException(TransportContextException.Cause.DEVICE_NOT_CONNECTED,
                                            f"Device {ble_context_device.address} is not connected")
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message=f"Performing just work authentication on {ble_context_device.address}...",
            trace_level=TraceLevel.EXTRA_DEBUG)

        # TODO add timeout
        # send a synchronous pair request (last value in the tuple indicates synchronous treatement)
        response = self._nrf_ble_lib_process.send_request_wait_for_response(
            request_type=NrfBleLibProcessMessageType.PAIR_REQUEST,
            request_arguments=(ble_context_device.nrf_ble_lib_connection_handle, IoCapability.NO_INPUT_NO_OUTPUT, {
                'mitm': False,
                'bonding': True,
                'secure_connection': lesc,
                'keypress_notifications': False},
                               False))

        if NrfBleLibAsyncioProcess.get_message_type(message=response) in ERROR_TYPES:
            # TODO error treatment and add it to the raised exception
            raise TransportContextException(TransportContextException.Cause.AUTHENTICATION_FAILED,
                                            f"Authentication of the device {ble_context_device.address.address} FAILED: "
                                            f"{response}")
        # end if

        ble_context_device.bonded = True

        TRACE_LOGGER.log_trace(
            subscription_owner=self, message=f"Device {ble_context_device.address.address} authenticated using just works",
            trace_level=TraceLevel.DEBUG)
    # end def authenticate_just_works

    def authenticate_keypress_start(self, ble_context_device, lesc=False):
        """
        Start bonding with a device using keypress method

        :param ble_context_device: The BLE device to bond/encrypt with
        :type ble_context_device: ``NrfBleLibBleContextDevice``
        :param lesc: Flag indicating to permit LE secure connection - OPTIONAL
        :type lesc: ``bool``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """

        if ble_context_device.bonding_state[0] not in [BleDeviceBondingStates.NO_BONDING,
                                                       BleDeviceBondingStates.FAILED]:
            raise TransportContextException(TransportContextException.Cause.ACTION_ALREADY_DONE,
                                            f"Authentication procedure started when device "
                                            f"in {repr(ble_context_device.bonding_state[0])}"
                                            f"{ble_context_device.bonding_state}")
        # end if

        if not self.is_open:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_NOT_OPEN)
        # end if

        if ble_context_device.nrf_ble_lib_connection_handle is None:
            raise TransportContextException(TransportContextException.Cause.DEVICE_NOT_CONNECTED,
                                            f"Device {ble_context_device.address} is not connected")
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message=f"Starting keypress authentication on {ble_context_device.address}...",
            trace_level=TraceLevel.EXTRA_DEBUG)

        # TODO add timeout
        # send an asynchronous pair request (last value in the tuple indicate asynchronous treatement)
        response = self._nrf_ble_lib_process.send_request_wait_for_response(
            request_type=NrfBleLibProcessMessageType.PAIR_REQUEST,
            request_arguments=(ble_context_device.nrf_ble_lib_connection_handle, IoCapability.DISPLAY_ONLY, {
                'mitm': True,
                'bonding': True,
                'secure_connection': lesc,
                'keypress_notifications': True},
                               True))

        if NrfBleLibAsyncioProcess.get_message_type(message=response) in ERROR_TYPES:
            # TODO error treatment and add it to the raised exception
            raise TransportContextException(TransportContextException.Cause.AUTHENTICATION_FAILED,
                                            f"Authentication of the device {ble_context_device.address.address} FAILED: "
                                            f"{response}")
        # end if

        pairing_event = self._pairing_event_queues[ble_context_device.address].get(
            timeout=BleContext.BLOCKING_DEFAULT_TIMEOUT)
        if pairing_event != BleSmpKeypress.PASSKEY_ENTRY_STARTED:
            TRACE_LOGGER.log_trace(
                subscription_owner=self,
                message=f"Unexpected pairing event when waiting for pairing started {pairing_event}",
                trace_level=TraceLevel.ERROR
            )
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message=f"Device {ble_context_device.address.address} keypress authentication started ",
            trace_level=TraceLevel.DEBUG)
    # end def authenticate_keypress_start

    def delete_bond(self, ble_context_device):
        """
        Delete the bond (if exist) with a device. This will disconnect the device if it is connected.

        :param ble_context_device: The BLE device of which to delete the bond
        :type ble_context_device: ``NrfBleLibBleContextDevice``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        if not self.is_open:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_NOT_OPEN)
        # end if

        if ble_context_device.nrf_ble_lib_connection_handle is not None:
            self.disconnect(ble_context_device=ble_context_device)
        # end if

        if not ble_context_device.bonded:
            ble_context_device.connection_security_parameters = None
            return
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=self, message=f"Deleting bond on {ble_context_device.address}...",
            trace_level=TraceLevel.EXTRA_DEBUG)

        # TODO add timeout
        response = self._nrf_ble_lib_process.send_request_wait_for_response(
            request_type=NrfBleLibProcessMessageType.DELETE_BOND_REQUEST,
            request_arguments=(NrfBleLibStructureTranslator.get_driver_ble_gap_address(
                interface_ble_gap_address=ble_context_device.address),))

        if NrfBleLibAsyncioProcess.get_message_type(message=response) in ERROR_TYPES:
            # TODO error treatment and add it to the raised exception
            raise TransportContextException(TransportContextException.Cause.CONTEXT_INTERNAL_ERROR,
                                            f"Deleting the device {ble_context_device.address}'s bond FAILED: "
                                            f"{response}")
        # end if

        ble_context_device.bonded = False
        ble_context_device.connection_security_parameters = None

        TRACE_LOGGER.log_trace(
            subscription_owner=self, message=f"Device {ble_context_device.address} bond deleted",
            trace_level=TraceLevel.DEBUG)
    # end def delete_bond

    def get_pairing_event(self, ble_context_device, block=True, timeout=BleContext.BLOCKING_DEFAULT_TIMEOUT):
        # See ``BleContext.get_pairing_event``
        try:
            value = self._pairing_event_queues[ble_context_device.address].get(block=block, timeout=timeout)
        except queue.Empty:
            value = None
        # end try

        return value
    # end def get_pairing_event

    def update_connection_parameters(self, ble_context_device, connection_parameters):
        """
        Update the connection parameters on a connected device

        :param ble_context_device: The BLE device to update the connection parameters on
        :type ble_context_device: ``NrfBleLibBleContextDevice``
        :param connection_parameters: Connection parameters
        :type connection_parameters: ``BleGapConnectionParameters``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        if not self.is_open:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_NOT_OPEN)
        # end if

        if ble_context_device.nrf_ble_lib_connection_handle is None:
            raise TransportContextException(TransportContextException.Cause.DEVICE_NOT_CONNECTED,
                                            f"Device {ble_context_device.address} is not connected")
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message=f"Updating connection parameters on {ble_context_device.address}...",
            trace_level=TraceLevel.EXTRA_DEBUG)

        # TODO add timeout
        response = self._nrf_ble_lib_process.send_request_wait_for_response(
            request_type=NrfBleLibProcessMessageType.UPDATE_CONNECTION_PARAMETERS_REQUEST,
            request_arguments=(ble_context_device.nrf_ble_lib_connection_handle,
                               NrfBleLibStructureTranslator.get_driver_connection_parameters(
                                   interface_connection_parameters=connection_parameters),))

        if NrfBleLibAsyncioProcess.get_message_type(message=response) in ERROR_TYPES:
            # TODO error treatment and add it to the raised exception
            raise TransportContextException(
                TransportContextException.Cause.CONTEXT_INTERNAL_ERROR,
                f"Update connection parameters of the device {ble_context_device.address} FAILED: {response}")
        # end if

        # TODO add wait to the update event to get the chosen connection parameters

        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message=f"Updated connection parameters on {ble_context_device.address.address} to {connection_parameters}",
            trace_level=TraceLevel.INFO)
    # end def update_connection_parameters

    def get_connection_security_parameters(self, ble_context_device):
        """
        Get the connection security parameters on a connected device

        :param ble_context_device: The BLE device to get the connection security parameters from
        :type ble_context_device: ``NrfBleLibBleContextDevice``

        :return: Connection security parameters
        :rtype: ``BleGapConnectionSecurityParameters``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        if not self.is_open:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_NOT_OPEN)
        # end if

        if ble_context_device.nrf_ble_lib_connection_handle is None:
            raise TransportContextException(TransportContextException.Cause.DEVICE_NOT_CONNECTED,
                                            f"Device {ble_context_device.address} is not connected")
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message=f"Getting connection security parameters for {ble_context_device.address}...",
            trace_level=TraceLevel.EXTRA_DEBUG)

        # TODO add timeout
        response = self._nrf_ble_lib_process.send_request_wait_for_response(
            request_type=NrfBleLibProcessMessageType.GET_CONNECTION_SECURITY_PARAMETERS_REQUEST,
            request_arguments=(ble_context_device.nrf_ble_lib_connection_handle,))

        if NrfBleLibAsyncioProcess.get_message_type(message=response) in ERROR_TYPES:
            # TODO error treatment and add it to the raised exception
            raise TransportContextException(
                TransportContextException.Cause.CONTEXT_INTERNAL_ERROR,
                f"Getting connection security parameters for the device {ble_context_device.address} FAILED: "
                f"{response}")
        # end if

        nrf_ble_lib_connection_handle = NrfBleLibAsyncioProcess.get_message_arguments(message=response)[
            GetConnectionSecurityParametersResponseArgsInd.CONNECTION_HANDLE]

        if nrf_ble_lib_connection_handle != ble_context_device.nrf_ble_lib_connection_handle:
            # TODO error treatment and add it to the raised exception
            raise TransportContextException(
                TransportContextException.Cause.CONTEXT_INTERNAL_ERROR,
                f"Getting connection security parameters for the device {ble_context_device.address} ERROR: "
                f"device handle received is {nrf_ble_lib_connection_handle} while device handle used is "
                f"{ble_context_device.nrf_ble_lib_connection_handle}")
        # end if

        driver_connection_security_parameters = NrfBleLibAsyncioProcess.get_message_arguments(message=response)[
            GetConnectionSecurityParametersResponseArgsInd.CONNECTION_SECURITY_PARAMETERS]

        ble_context_device.connection_security_parameters = \
            NrfBleLibStructureTranslator.get_interface_connection_security_parameters(
                driver_connection_security_parameters=driver_connection_security_parameters)

        TRACE_LOGGER.log_trace(
            subscription_owner=self, message=f"Connection security parameters for {ble_context_device.address} are "
                                             f"{ble_context_device.connection_security_parameters}",
            trace_level=TraceLevel.INFO)

        return ble_context_device.connection_security_parameters
    # end def get_connection_security_parameters

    def register_ble_event_callback(self, ble_event, callback):
        # See ``BleContextDevice.register_ble_event_callback``
        key = BLE_CALLBACK_EVENT_TO_KEY[ble_event]
        self._callbacks[key] = callback
    # end def register_ble_event_callback

    def clear_ble_event_callback(self):
        # See ``BleContextDevice.clear_ble_event_callback``
        self._callbacks.clear()
    # end def clear_ble_event_callback

    def characteristic_write(self, ble_context_device, characteristic, data):
        """
        Write data on a characteristic. Use a write-with-response exchange.

        :param ble_context_device: The BLE device to disconnect from
        :type ble_context_device: ``NrfBleLibBleContextDevice``
        :param characteristic: Characteristic object to use to send data
        :type characteristic: ``BleCharacteristic``
        :param data: The data to send
        :type data: ``BleMessage``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        self._characteristic_write(ble_context_device=ble_context_device, characteristic=characteristic, data=data.data,
                                   characteristic_write_type=WriteOperation.WRITE_REQUEST)
    # end def characteristic_write

    def characteristic_write_without_response(self, ble_context_device, characteristic, data):
        """
        Write data on a characteristic. Use a write-without-response exchange.

        :param ble_context_device: The BLE device to disconnect from
        :type ble_context_device: ``NrfBleLibBleContextDevice``
        :param characteristic: Characteristic object to use to send data
        :type characteristic: ``BleCharacteristic``
        :param data: The data to send
        :type data: ``BleMessage``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        self._characteristic_write(ble_context_device=ble_context_device, characteristic=characteristic, data=data.data,
                                   characteristic_write_type=WriteOperation.WRITE_COMMAND)
    # end def characteristic_write_without_response

    def characteristic_long_write_without_response(self, ble_context_device, characteristic, data):
        """
        Long write data on a characteristic.

        :param ble_context_device: The BLE device to disconnect from
        :type ble_context_device: ``NrfBleLibBleContextDevice``
        :param characteristic: Characteristic object to use to send data
        :type characteristic: ``BleCharacteristic``
        :param data: The data to send
        :type data: ``BleMessage``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        self._characteristic_write(ble_context_device=ble_context_device, characteristic=characteristic, data=data.data,
                                   characteristic_write_type=WriteOperation.WRITE_LONG)
    # end def characteristic_long_write_without_response

    def attribute_read(self, ble_context_device, attribute):
        """
        Read data of a characteristic.

        :param ble_context_device: The BLE device to use
        :type ble_context_device: ``NrfBleLibBleContextDevice``
        :param attribute: Attribute object to read from
        :type attribute: ``BleCharacteristic`` or ``BleDescriptor``

        :return: The data read from the attribute
        :rtype: ``BleMessage``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        if not self.is_open:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_NOT_OPEN)
        # end if

        if ble_context_device.nrf_ble_lib_connection_handle is None:
            raise TransportContextException(TransportContextException.Cause.DEVICE_NOT_CONNECTED,
                                            f"Device {ble_context_device.address} is not connected")
        # end if

        if not isinstance(attribute, (BleCharacteristic, BleDescriptor)):
            raise TransportContextException(TransportContextException.Cause.PARAMETER_ERROR,
                                            "attribute parameter should be a BleCharacteristic or BleDescriptor,"
                                            f"{attribute} is not")
        # end if

        if isinstance(attribute, BleCharacteristic):
            # Characteristic read
            request_type = NrfBleLibProcessMessageType.CHARACTERISTIC_READ_REQUEST
            request_arguments = (
                ble_context_device.nrf_ble_lib_connection_handle,
                NrfBleLibStructureTranslator.get_driver_characteristic(interface_characteristic=attribute),
                ReadOperation.READ_LONG)
        else:
            # Descriptor read
            request_type = NrfBleLibProcessMessageType.DESCRIPTOR_READ_REQUEST
            request_arguments = (
                ble_context_device.nrf_ble_lib_connection_handle,
                NrfBleLibStructureTranslator.get_driver_descriptor(interface_descriptor=attribute),
                ReadOperation.READ_LONG)
        # end if

        # TODO add timeout
        response = self._nrf_ble_lib_process.send_request_wait_for_response(
            request_type=request_type, request_arguments=request_arguments)

        if NrfBleLibAsyncioProcess.get_message_type(message=response) in ERROR_TYPES:
            error_args = NrfBleLibAsyncioProcess.get_message_arguments(message=response)
            if len(error_args) >= 3 and (error_args[2] & 0xFFFF0000) == ErrorId.TRANSPORT_CONTEXT_EXCEPTION:
                if len(error_args) >= 4:
                    raise TransportContextException(
                        TransportContextException.Cause(error_args[2] & 0xFF), *error_args[3])
                else:
                    raise TransportContextException(TransportContextException.Cause(error_args[2] & 0xFF))
                # end if
            # end if
            # TODO error treatment and add it to the raised exception
            raise TransportContextException(
                TransportContextException.Cause.CONTEXT_INTERNAL_ERROR,
                f"Attribute read of {attribute} on the device {ble_context_device.address} FAILED: {response}")
        # end if

        response_arguments = NrfBleLibAsyncioProcess.get_message_arguments(message=response)
        # TODO move timestamp to nrf-ble-lib process
        data_read = BleMessage(data=HexList(response_arguments[CharacteristicReadResponseArgsInd.DATA_READ]),
                               timestamp=perf_counter_ns())

        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message=f"Attribute read of {attribute.short_string()} on the device {ble_context_device.address.address}, "
                    f"data: {data_read}",
            trace_level=TraceLevel.INFO)

        return data_read
    # end def attribute_read

    def get_notification_status(self, ble_context_device, characteristic):
        """
        Get the notification status (enabled/disabled) on a characteristic.

        :param ble_context_device: The BLE device to use
        :type ble_context_device: ``NrfBleLibBleContextDevice``
        :param characteristic: Characteristic object to enable notification from
        :type characteristic: ``BleCharacteristic``

        :return: The notification status as a boolean: ``True`` for enabled and ``False`` for disabled
        :rtype: ``bool``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        if not self.is_open:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_NOT_OPEN)
        # end if

        if ble_context_device.nrf_ble_lib_connection_handle is None:
            raise TransportContextException(TransportContextException.Cause.DEVICE_NOT_CONNECTED)
        # end if

        cccd = characteristic.get_descriptors(descriptor_uuid=BleUuid(
            value=BleUuidStandardDescriptor.CLIENT_CHARACTERISTIC_CONFIGURATION))

        if len(cccd) == 0:
            raise TransportContextException(TransportContextException.Cause.PARAMETER_ERROR,
                                            f"No CCCD found for {characteristic}")
        elif len(cccd) > 1:
            raise TransportContextException(TransportContextException.Cause.PARAMETER_ERROR,
                                            f"More than one CCCD found for {characteristic}: {cccd}")
        # end if

        cccd = cccd[0]

        cccd_value = self.attribute_read(ble_context_device=ble_context_device, attribute=cccd)

        is_notification_enabled = (cccd_value.data[0] & BleGenericIntConstant.NOTIFY_STATUS_IN_CCCD_MASK) == \
            BleGenericIntConstant.NOTIFY_STATUS_IN_CCCD_MASK

        if not is_notification_enabled:
            with self._notification_time_stamped_queues:
                queues = self._notification_time_stamped_queues.get(ble_context_device.address, None)
                if queues is not None:
                    # If the characteristic notification is not enabled while a queue for it is present. This means
                    # that it was disabled not using the method disable_notification. Therefore, the internal
                    # mapping of notification queue and characteristic should be updated (in this case removing
                    # the queue)
                    queue = queues.pop(characteristic.handle, None)
                    if queue is not None:
                        TRACE_LOGGER.log_trace(
                            subscription_owner=self,
                            message="[get_notification_status] Notification disabled on characteristic attr_handle("
                                    f"{characteristic.handle}) while a reception queue is still given: {queue}",
                            trace_level=TraceLevel.WARNING)
                    # end if

                    # If the number of queues is 0 (either because of the previous if or because it was missed
                    # somewhere) it should be removed from the dictionary
                    if len(queues) == 0:
                        self._notification_time_stamped_queues.pop(ble_context_device.address, None)
                    # end if
                # end if
            # end with
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message=f"Notification status on the {characteristic.short_string()} "
                    f"on the device {ble_context_device.address.address}, data: {is_notification_enabled}",
            trace_level=TraceLevel.INFO)

        return is_notification_enabled
    # end def get_notification_status

    def enable_notification(self, ble_context_device, characteristic, time_stamped_queue=None):
        """
        Enable notification on a characteristic.

        :param ble_context_device: The BLE device to use
        :type ble_context_device: ``NrfBleLibBleContextDevice``
        :param characteristic: Characteristic object to enable notification status of
        :type characteristic: ``BleCharacteristic``
        :param time_stamped_queue: Queue for time stamped data received by notification - OPTIONAL
        :type time_stamped_queue: ``Queue`` or ``None``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        notification_status = self.get_notification_status(
            ble_context_device=ble_context_device, characteristic=characteristic)

        if notification_status:
            raise TransportContextException(
                TransportContextException.Cause.ACTION_ALREADY_DONE,
                f"Device address {ble_context_device.address}, Characteristic:\n{characteristic}")
        # end if

        with self._notification_time_stamped_queues:
            queues = self._notification_time_stamped_queues.get(ble_context_device.address, None)
            if queues is None:
                self._notification_time_stamped_queues[ble_context_device.address] = {}
            else:
                queue = queues.get(characteristic.handle, None)
                if queue is not None:
                    raise TransportContextException(
                        TransportContextException.Cause.CONTEXT_INTERNAL_ERROR,
                        f"Device address {ble_context_device.address}, Characteristic:\n{characteristic} already "
                        f"have a notification queue: {queue}")
                # end if
            # end if

            self._notification_time_stamped_queues[ble_context_device.address][characteristic.handle] = \
                time_stamped_queue
        # end with

        try:
            self.write_on_cccd_notification(ble_context_device, characteristic, enabled=True)
        except Exception:
            self._notification_time_stamped_queues[ble_context_device.address].pop(characteristic.handle, None)

            if len(self._notification_time_stamped_queues[ble_context_device.address]) == 0:
                self._notification_time_stamped_queues.pop(ble_context_device.address, None)
            # end if
            raise
        # end try
    # end def enable_notification

    def write_on_cccd_notification(self, ble_context_device, characteristic, enabled):
        # See ``BleContext.write_on_cccd_notification``
        prefix = "en" if enabled else "dis"

        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message=f"{prefix}abling notification on {characteristic.short_string()} "
                    f"on the device {ble_context_device.address}...",
            trace_level=TraceLevel.EXTRA_DEBUG)

        # TODO add timeout
        response = self._nrf_ble_lib_process.send_request_wait_for_response(
            request_type=NrfBleLibProcessMessageType.SET_NOTIFICATION_STATUS_REQUEST,
            request_arguments=(ble_context_device.nrf_ble_lib_connection_handle,
                               NrfBleLibStructureTranslator.get_driver_characteristic(
                                   interface_characteristic=characteristic), enabled))

        if NrfBleLibAsyncioProcess.get_message_type(message=response) in ERROR_TYPES:
            error_args = NrfBleLibAsyncioProcess.get_message_arguments(message=response)
            if len(error_args) >= 3 and (error_args[2] & 0xFFFF0000) == ErrorId.TRANSPORT_CONTEXT_EXCEPTION:
                if len(error_args) >= 4:
                    raise TransportContextException(
                        TransportContextException.Cause(error_args[2] & 0xFF), *error_args[3])
                else:
                    raise TransportContextException(TransportContextException.Cause(error_args[2] & 0xFF))
                # end if
            # end if
            # TODO error treatment and add it to the raised exception
            raise TransportContextException(
                TransportContextException.Cause.CONTEXT_INTERNAL_ERROR,
                f"{prefix}abling notification on {characteristic} on the device {ble_context_device.address} FAILED: "
                f"{response}")
        # end if

        # TODO verify returned arguments
        #  response_arguments = NrfBleLibAsyncioProcess.get_message_arguments(message=response)

        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message=f"Notification {prefix}abled on {characteristic.short_string()} on the device "
                    f"{ble_context_device.address.address}",
            trace_level=TraceLevel.INFO)
    # end def write_on_cccd_notification

    def update_notification_queue(self, ble_context_device, characteristic, time_stamped_queue=None):
        """
        Update the time stamped queue for notification on a characteristic. The notification had to be enabled prior
        to this method.

        :param ble_context_device: The BLE device to use
        :type ble_context_device: ``NrfBleLibBleContextDevice``
        :param characteristic: Characteristic object to update the queue from
        :type characteristic: ``BleCharacteristic``
        :param time_stamped_queue: Queue for time stamped data received by notification - OPTIONAL
        :type time_stamped_queue: ``Queue`` or ``None``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        notification_status = self.get_notification_status(
            ble_context_device=ble_context_device, characteristic=characteristic)

        if not notification_status:
            raise TransportContextException(
                TransportContextException.Cause.CONTEXT_INVALID_STATE,
                f"Device address {ble_context_device.address}, Characteristic:\n{characteristic} notification not "
                f"enabled")
        # end if

        with self._notification_time_stamped_queues:
            queues = self._notification_time_stamped_queues.get(ble_context_device.address, None)
            if queues is None:
                self._notification_time_stamped_queues[ble_context_device.address] = {}
            # end if

            old_queue = queues.get(characteristic.handle, None)

            if old_queue != time_stamped_queue:
                self._notification_time_stamped_queues[ble_context_device.address][characteristic.handle] = \
                    time_stamped_queue
            # end if
        # end with

        if old_queue == time_stamped_queue:
            TRACE_LOGGER.log_trace(
                subscription_owner=self,
                message=f"Notification queue for characteristic {characteristic.short_string()} is already the wanted "
                        f"one: {time_stamped_queue}",
                trace_level=TraceLevel.DEBUG)
        else:
            TRACE_LOGGER.log_trace(
                subscription_owner=self,
                message=f"Change notification queue for characteristic {characteristic.short_string()} "
                        f"from {old_queue} to {time_stamped_queue}",
                trace_level=TraceLevel.DEBUG)
        # end if
    # end def update_notification_queue

    def disable_notification(self, ble_context_device, characteristic):
        """
        Disable notification on a characteristic.

        :param ble_context_device: The BLE device to use
        :type ble_context_device: ``NrfBleLibBleContextDevice``
        :param characteristic: Characteristic object to disable notification from
        :type characteristic: ``BleCharacteristic``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        notification_status = self.get_notification_status(
            ble_context_device=ble_context_device, characteristic=characteristic)

        if not notification_status:
            raise TransportContextException(
                TransportContextException.Cause.ACTION_ALREADY_DONE,
                f"Device address {ble_context_device.address}, Characteristic:\n{characteristic}")
        # end if

        self.write_on_cccd_notification(
            ble_context_device=ble_context_device, characteristic=characteristic, enabled=False)

        # TODO verify returned arguments
        #  response_arguments = NrfBleLibAsyncioProcess.get_message_arguments(message=response)

        with self._notification_time_stamped_queues:
            queues = self._notification_time_stamped_queues.get(ble_context_device.address, None)
            if queues is not None:
                queues.pop(characteristic.handle, None)

                if len(queues) == 0:
                    self._notification_time_stamped_queues.pop(ble_context_device.address, None)
                # end if
            # end if
        # end with
    # end def disable_notification

    def get_indication_status(self, ble_context_device, characteristic):
        """
        Get the indication status (enabled/disabled) on a characteristic.

        :param ble_context_device: The BLE device to use
        :type ble_context_device: ``NrfBleLibBleContextDevice``
        :param characteristic: Characteristic object to get the indication status of
        :type characteristic: ``BleCharacteristic``

        :return: The indication status as a boolean: ``True`` for enabled and ``False`` for disabled
        :rtype: ``bool``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        if not self.is_open:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_NOT_OPEN)
        # end if

        if ble_context_device.nrf_ble_lib_connection_handle is None:
            raise TransportContextException(TransportContextException.Cause.DEVICE_NOT_CONNECTED)
        # end if

        cccd = characteristic.get_descriptors(descriptor_uuid=BleUuid(
            value=BleUuidStandardDescriptor.CLIENT_CHARACTERISTIC_CONFIGURATION))

        if len(cccd) == 0:
            raise TransportContextException(TransportContextException.Cause.PARAMETER_ERROR,
                                            f"No CCCD found for {characteristic}")
        elif len(cccd) > 1:
            raise TransportContextException(TransportContextException.Cause.PARAMETER_ERROR,
                                            f"More than one CCCD found for {characteristic}: {cccd}")
        # end if

        cccd_value = self.attribute_read(ble_context_device=ble_context_device, attribute=cccd[0])

        is_indication_enabled = (to_int(cccd_value.data) & BleGenericIntConstant.INDICATE_STATUS_IN_CCCD_MASK) == \
            BleGenericIntConstant.INDICATE_STATUS_IN_CCCD_MASK

        if not is_indication_enabled:
            with self._indication_time_stamped_queues:
                queues = self._indication_time_stamped_queues.get(ble_context_device.address, None)
                if queues is not None:
                    # If the characteristic indication is not enabled while a queue for it is present. This means
                    # that it was disabled not using the method disable_indication. Therefore, the internal
                    # mapping of notification queue and characteristic should be updated (in this case removing
                    # the queue)
                    queue = queues.pop(characteristic.handle, None)
                    if queue is not None:
                        TRACE_LOGGER.log_trace(
                            subscription_owner=self,
                            message="[get_indication_status] Notification disabled on characteristic attr_handle("
                                    f"{characteristic.short_string()}) while a reception queue is still given: {queue}",
                            trace_level=TraceLevel.WARNING)
                    # end if

                    # If the number of queues is 0 (either because of the previous if or because it was missed
                    # somewhere) it should be removed from the dictionary
                    if len(queues) == 0:
                        self._indication_time_stamped_queues.pop(ble_context_device.address, None)
                    # end if
                # end if
            # end with
        # end if
        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message=f"Indication status on the characteristic {characteristic.short_string()} "
                    f"on the device {ble_context_device.address.address}, data: {is_indication_enabled}",
            trace_level=TraceLevel.INFO)

        return is_indication_enabled
    # end def get_indication_status

    def enable_indication(self, ble_context_device, characteristic, time_stamped_queue=None):
        """
        Enable indication on a characteristic.

        :param ble_context_device: The BLE device to use
        :type ble_context_device: ``NrfBleLibBleContextDevice``
        :param characteristic: Characteristic object to enable indication from
        :type characteristic: ``BleCharacteristic``
        :param time_stamped_queue: Queue for time stamped data received by indication - OPTIONAL
        :type time_stamped_queue: ``Queue`` or ``None``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        indication_status = self.get_indication_status(
            ble_context_device=ble_context_device, characteristic=characteristic)

        if indication_status:
            raise TransportContextException(
                TransportContextException.Cause.ACTION_ALREADY_DONE,
                f"Device address {ble_context_device.address}, Characteristic:\n{characteristic}")
        # end if

        with self._indication_time_stamped_queues:
            queues = self._indication_time_stamped_queues.get(ble_context_device.address, None)
            if queues is None:
                self._indication_time_stamped_queues[ble_context_device.address] = {}
            else:
                queue = queues.get(characteristic.handle, None)
                if queue is not None:
                    raise TransportContextException(
                        TransportContextException.Cause.CONTEXT_INTERNAL_ERROR,
                        f"Device address {ble_context_device.address}, Characteristic:\n{characteristic} already "
                        f"have an indication queue: {queue}")
                # end if
            # end if

            self._indication_time_stamped_queues[ble_context_device.address][characteristic.handle] = \
                time_stamped_queue
        # end with

        try:
            TRACE_LOGGER.log_trace(
                subscription_owner=self,
                message=f"Enabling indication on {characteristic.short_string()} "
                        f"on the device {ble_context_device.address}...",
                trace_level=TraceLevel.EXTRA_DEBUG)

            # TODO add timeout
            response = self._nrf_ble_lib_process.send_request_wait_for_response(
                request_type=NrfBleLibProcessMessageType.SET_INDICATION_STATUS_REQUEST,
                request_arguments=(ble_context_device.nrf_ble_lib_connection_handle,
                                   NrfBleLibStructureTranslator.get_driver_characteristic(
                                       interface_characteristic=characteristic), True))

            if NrfBleLibAsyncioProcess.get_message_type(message=response) in ERROR_TYPES:
                error_args = NrfBleLibAsyncioProcess.get_message_arguments(message=response)
                if len(error_args) >= 3 and (error_args[2] & 0xFFFF0000) == ErrorId.TRANSPORT_CONTEXT_EXCEPTION:
                    if len(error_args) >= 4:
                        raise TransportContextException(
                            TransportContextException.Cause(error_args[2] & 0xFF), *error_args[3])
                    else:
                        raise TransportContextException(TransportContextException.Cause(error_args[2] & 0xFF))
                    # end if
                # end if
                # TODO error treatment and add it to the raised exception
                raise TransportContextException(
                    TransportContextException.Cause.CONTEXT_INTERNAL_ERROR,
                    f"Enabling indication on {characteristic} on the device {ble_context_device.address} FAILED: "
                    f"{response}")
            # end if

            # TODO verify returned arguments
            #  response_arguments = NrfBleLibAsyncioProcess.get_message_arguments(message=response)

            TRACE_LOGGER.log_trace(
                subscription_owner=self,
                message=f"Indication enabled on {characteristic.short_string()} on the device "
                        f"{ble_context_device.address.address}",
                trace_level=TraceLevel.INFO)
        except Exception:
            self._indication_time_stamped_queues[ble_context_device.address].pop(characteristic.handle, None)

            if len(self._indication_time_stamped_queues[ble_context_device.address]) == 0:
                self._indication_time_stamped_queues.pop(ble_context_device.address, None)
            # end if
            raise
        # end try
    # end def enable_indication

    def update_indication_queue(self, ble_context_device, characteristic, time_stamped_queue=None):
        """
        Update the time stamped queue for indication on a characteristic. The indication had to be enabled prior
        to this method.

        :param ble_context_device: The BLE device to use
        :type ble_context_device: ``NrfBleLibBleContextDevice``
        :param characteristic: Characteristic object to update the queue from
        :type characteristic: ``BleCharacteristic``
        :param time_stamped_queue: Queue for time stamped data received by indication - OPTIONAL
        :type time_stamped_queue: ``Queue`` or ``None``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        indication_status = self.get_indication_status(
            ble_context_device=ble_context_device, characteristic=characteristic)

        if indication_status:
            raise TransportContextException(
                TransportContextException.Cause.CONTEXT_INVALID_STATE,
                f"Device address {ble_context_device.address}, Characteristic:\n{characteristic} indication not "
                f"enabled")
        # end if

        with self._indication_time_stamped_queues:
            queues = self._indication_time_stamped_queues.get(ble_context_device.address, None)
            if queues is None:
                self._indication_time_stamped_queues[ble_context_device.address] = {}
            # end if

            old_queue = queues.get(characteristic.handle, None)

            if old_queue != time_stamped_queue:
                self._indication_time_stamped_queues[ble_context_device.address][characteristic.handle] = \
                    time_stamped_queue
            # end if
        # end with

        if old_queue == time_stamped_queue:
            TRACE_LOGGER.log_trace(
                subscription_owner=self,
                message=f"Indication queue for characteristic {characteristic.short_string()} is already the wanted "
                        f"one: {time_stamped_queue}",
                trace_level=TraceLevel.DEBUG)
        else:
            TRACE_LOGGER.log_trace(
                subscription_owner=self,
                message=f"Change indication queue for characteristic {characteristic.short_string()} "
                        f"from {old_queue} to {time_stamped_queue}",
                trace_level=TraceLevel.DEBUG)
        # end if
    # end def update_indication_queue

    def disable_indication(self, ble_context_device, characteristic):
        """
        Disable indication on a characteristic.

        :param ble_context_device: The BLE device to use
        :type ble_context_device: ``NrfBleLibBleContextDevice``
        :param characteristic: Characteristic object to disable indication from
        :type characteristic: ``BleCharacteristic``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        indication_status = self.get_indication_status(
            ble_context_device=ble_context_device, characteristic=characteristic)

        if not indication_status:
            raise TransportContextException(
                TransportContextException.Cause.ACTION_ALREADY_DONE,
                f"Device address {ble_context_device.address}, Characteristic:\n{characteristic}")
        # end if

        if not self.is_open:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_NOT_OPEN)
        # end if

        if ble_context_device.nrf_ble_lib_connection_handle is None:
            raise TransportContextException(TransportContextException.Cause.DEVICE_NOT_CONNECTED)
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message=f"Disabling indication on {characteristic.short_string()} "
                    f"on the device {ble_context_device.address}...",
            trace_level=TraceLevel.EXTRA_DEBUG)

        # TODO add timeout
        response = self._nrf_ble_lib_process.send_request_wait_for_response(
            request_type=NrfBleLibProcessMessageType.SET_INDICATION_STATUS_REQUEST,
            request_arguments=(ble_context_device.nrf_ble_lib_connection_handle,
                               NrfBleLibStructureTranslator.get_driver_characteristic(
                                   interface_characteristic=characteristic), False))

        if NrfBleLibAsyncioProcess.get_message_type(message=response) in ERROR_TYPES:
            error_args = NrfBleLibAsyncioProcess.get_message_arguments(message=response)
            if len(error_args) >= 3 and (error_args[2] & 0xFFFF0000) == ErrorId.TRANSPORT_CONTEXT_EXCEPTION:
                if len(error_args) >= 4:
                    raise TransportContextException(
                        TransportContextException.Cause(error_args[2] & 0xFF), *error_args[3])
                else:
                    raise TransportContextException(TransportContextException.Cause(error_args[2] & 0xFF))
                # end if
            # end if
            # TODO error treatment and add it to the raised exception
            raise TransportContextException(
                TransportContextException.Cause.CONTEXT_INTERNAL_ERROR,
                f"Disabling indication on {characteristic} on the device {ble_context_device.address} FAILED: "
                f"{response}")
        # end if

        # TODO verify returned arguments
        #  response_arguments = NrfBleLibAsyncioProcess.get_message_arguments(message=response)

        with self._indication_time_stamped_queues:
            queues = self._indication_time_stamped_queues.get(ble_context_device.address, None)
            if queues is None:
                # No notification is enabled on any characteristic for this device, nothing needs to be done
                return
            # end if

            queues.pop(characteristic.handle, None)

            if len(queues) == 0:
                self._indication_time_stamped_queues.pop(ble_context_device.address, None)
            # end if
        # end with

        TRACE_LOGGER.log_trace(
            subscription_owner=self,
            message=f"Indication disabled on {characteristic.short_string()} "
                    f"on the device {ble_context_device.address.address}",
            trace_level=TraceLevel.INFO)
    # end def disable_indication

    def get_gatt_table(self, ble_context_device):
        """
        Get the GATT table of the connected device.

        :param ble_context_device: The BLE device to bond/encrypt with
        :type ble_context_device: ``NrfBleLibBleContextDevice``

        :return: Gatt table as a list of services
        :rtype: ``list[BleService]``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        if ble_context_device.gatt_table is None:
            self.perform_service_discovery(ble_context_device=ble_context_device)
        # end if

        return ble_context_device.gatt_table
    # end def get_gatt_table

    def get_central_address(self):
        """
        Get the GAP address of the central used for this context.

        :return: The central GAP address
        :rtype: ``BleGapAddress``

        :raise ``TransportContextException``: It can raise for any causes in ``TransportContextException.Cause``
        """
        if not self.is_open:
            raise TransportContextException(TransportContextException.Cause.CONTEXT_NOT_OPEN)
        # end if

        TRACE_LOGGER.log_trace(
            subscription_owner=self, message="Getting central address...", trace_level=TraceLevel.EXTRA_DEBUG)

        # TODO add timeout
        response = self._nrf_ble_lib_process.send_request_wait_for_response(
            request_type=NrfBleLibProcessMessageType.GET_CENTRAL_ADDRESS_REQUEST)

        if NrfBleLibAsyncioProcess.get_message_type(message=response) in ERROR_TYPES:
            # TODO error treatment and add it to the raised exception
            raise TransportContextException(
                TransportContextException.Cause.CONTEXT_INTERNAL_ERROR, f"Getting central address FAILED: {response}")
        # end if

        central_address = BleGapAddress(address_type=BleGapAddressType.RANDOM_STATIC,
                                        address=NrfBleLibAsyncioProcess.get_message_arguments(message=response)[
                                            GetCentralAddressResponseArgsInd.CENTRAL_ADDRESS].replace(":", ""))

        TRACE_LOGGER.log_trace(
            subscription_owner=self, message=f"Get central address: {central_address}", trace_level=TraceLevel.DEBUG)

        return central_address
    # end def get_central_address

    # ------------------------------------------------------------------------------------------------------------------
    # Class and static methods
    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def get_bt_stack_devices_com_ports(cls, force=False):
        """
        Get the list of nRFConnect devices plugged in

        :param force: Flag indicating to force relisting the devices - OPTIONAL
        :type force: ``bool``

        :return: The list of COM port of nRFConnect devices plugged in
        :rtype: ``list[str]``
        """
        if cls.BT_STACK_DEVICES is not None and not force:
            return cls.BT_STACK_DEVICES
        # end if

        bt_stack_devices = []
        for port in comports():
            if port.vid == cls.BT_STACK_DEVICE_VID and port.pid == cls.BT_STACK_DEVICE_PID:
                bt_stack_devices.append(port.device)
            # end if
        # end for
        cls.BT_STACK_DEVICES = bt_stack_devices
        return bt_stack_devices
    # end def get_bt_stack_devices_com_ports

    @classmethod
    def reset_context_hardware(cls, debugger, *args, **kwargs):
        """
        Perform a soft reset of the DK using the debugger. The debugger is a shared resource with the device (as opposed
        to receiver). Therefore, it is important to disconnect the jlink from the device.

        :param debugger: JLink to use to reset the DK
        :type debugger: ``pytestbox.base.jlinkdebugger.JlinkDebugger``
        :param args: Potential future parameters - OPTIONAL
        :type args: ``list``
        :param kwargs: Potential future parameters - OPTIONAL
        :type kwargs: ``dict``
        """
        with debugger.opened_with_mcu_name(mcu_name=cls.MCU_NAME):
            debugger.reset()
        # end with
    # end def reset_context_hardware

    @classmethod
    def update_context_hardware(cls, debugger, force=False, *args, **kwargs):
        """
        Update the firmware on the DK is up-to-date. The debugger is a shared resource with the device (as opposed
        to receiver). Therefore, it is important to disconnect the jlink from the device.

        :param debugger: JLink to use to update the firmware
        :type debugger: ``pytestbox.base.jlinkdebugger.JlinkDebugger``
        :param force: Flag indicating to force the flash, even if the dk is already up-to-date - OPTIONAL
        :type force: ``bool``
        :param args: Potential future parameters - OPTIONAL
        :type args: ``list``
        :param kwargs: Potential future parameters - OPTIONAL
        :type kwargs: ``dict``

        :return: Flag indicating if the firmware on the DK is up-to-date
        :rtype: ``bool``
        """
        if len(cls.get_bt_stack_devices_com_ports(force=True)) > 0 and not force:
            cls.DOOMED = False
            return True
        # end if

        with debugger.opened_with_mcu_name(mcu_name=cls.MCU_NAME, unlock_device=True):
            debugger.flash_firmware(firmware_hex_file=path.join(
                path.dirname(__file__), "nrf_ble_lib", "hci_uart_nrf52840dk_nrf52840_usb_cdc_acm.hex"))
        # end with

        # Add a wait to let the hardware recover
        start_time = time()
        while len(cls.get_bt_stack_devices_com_ports(force=True)) == 0 and \
                time() - start_time < RECONNECT_HARDWARE_TIMEOUT:
            sleep(.1)
        # end while

        is_up_to_date = len(cls.get_bt_stack_devices_com_ports(force=True)) > 0

        # Un-doom the type of context as the dk is now up-to-date
        cls.DOOMED = False if is_up_to_date else True

        return is_up_to_date
    # end def update_context_hardware
# end class NrfBleLibBleContext

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
