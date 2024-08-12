#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pytransport.usb.libusbcontext.logiusbtasks
:brief: Define Tasks managing USB communication.
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2022/12/09
"""
# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from enum import IntEnum
from enum import auto
from queue import Queue
from threading import Event

from logiusb_py.logiusb_constants import LogiusbPacketIndex
from logiusb_py.logiusb_constants import LogiusbTransferOptionsFlags
from logiusb_py.logiusb_stuctures import LogiusbTransferOptions
from logiusb_py.logiusb_utils import LogiusbException
from pylibrary.system.tracelogger import TraceLevel
from pylibrary.system.tracelogger import TraceLogger
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.threadutils import Task
from pylibrary.tools.tracebacklog import TracebackLogWrapper
from pytransport.usb.usbmessage import UsbMessage

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------
TRACE_LOGGER = TraceLogger.get_instance()
MAX_THREADS = 20


# ------------------------------------------------------------------------------
# Implementation
# ------------------------------------------------------------------------------
class InterruptPollingTask(Task):
    """
    Task that does the polling on the interrupt endpoint.
    """

    class TaskAction(IntEnum):
        """
        Enumeration of action for InterruptPollingTask
        """
        CANCEL = auto()
        MUTE = auto()
    # end class TaskAction

    def __init__(self, logiusb_context, logiusb_context_device, packet_maximum_length, endpoint_address,
                 time_stamped_msg_queue=None, trace_name=None, discard_report=False):
        """
        :param logiusb_context: Associated Logiusb context
        :type logiusb_context: ``pytransport.usb.logiusbcontext.logiusbcontext.LogiusbUsbContext``
        :param logiusb_context_device: Associated Logiusb context device
        :type logiusb_context_device: ``pytransport.usb.logiusbcontext.logiusbcontext.LogiusbUsbContextDevice``
        :param packet_maximum_length: The maximum length of the packet to receive, it should be an uint32
        :type packet_maximum_length: ``int``
        :param endpoint_address: Endpoint address, it should be an uint8
        :type endpoint_address: ``int``
        :param time_stamped_msg_queue: Queue to get all USB message received - OPTIONAL
        :type time_stamped_msg_queue: ``Queue`` or ``None``
        :param trace_name: Trace name of the task - OPTIONAL
        :type trace_name: ``str`` or ``None``
        :param discard_report: Flag indicating to discard any message received on this endpoint - OPTIONAL
        :type discard_report: ``bool``
        """
        # The device is added to the task to avoid losing the object before closing the task
        self._usb_context_device = logiusb_context_device
        self._transfer_queue = Queue()
        self._time_stamped_msg_queue = time_stamped_msg_queue
        self.end_event = Event()
        self.mute_event = Event()
        self.unmute_event = Event()

        # Values for logging
        self._reader_name = self._usb_context_device.get_basic_reader_name()
        self._endpoint_address = endpoint_address
        self._endpoint_address_str = f"0x{endpoint_address:02X}"

        TRACE_LOGGER.subscribe(
            subscription_owner=self, trace_file_name=logiusb_context.trace_file_name, trace_name=trace_name,
            linked_owner=logiusb_context)

        TRACE_LOGGER.log_trace(subscription_owner=self,
                               message=f"{self._reader_name}, Start thread on endpoint {self._endpoint_address_str}",
                               trace_level=TraceLevel.DEBUG)

        try:
            self._transfer = self._usb_context_device.logiusb_device.create_interrupt_read_transfer(
                packet_maximum_length=packet_maximum_length, endpoint_address=endpoint_address,
                receiving_queue=self._transfer_queue if not discard_report else None,
                options=LogiusbTransferOptions(
                    flags=(LogiusbTransferOptionsFlags.TRANSFER_OPTIONS_RESUBMIT |
                           LogiusbTransferOptionsFlags.TRANSFER_OPTIONS_BUFFERED),
                    resubmit_count=-1))

            self._transfer.asynchronous_submit()
        except LogiusbException as logiusb_exception:
            logiusb_context.transfer_exception_treatment(logiusb_exception=logiusb_exception)
        # end try

        super().__init__(self._run)
    # end def __init__

    # noinspection PyBroadException
    def __del__(self):
        try:
            self.stop_task()
        except Exception:
            pass
        # end try

        try:
            if TRACE_LOGGER.is_subscribe(subscription_owner=self):
                TRACE_LOGGER.unsubscribe(subscription_owner=self)
            # end if
        except Exception:
            pass
        # end try
    # end def __del__

    def _run(self):
        """
        Run method for the interrupt polling.
        """
        stop_task = False
        on_hold = False
        # noinspection PyBroadException
        try:
            TRACE_LOGGER.log_trace(
                subscription_owner=self,
                message=f"{self._reader_name}, Thread on endpoint {self._endpoint_address_str} started",
                trace_level=TraceLevel.EXTRA_DEBUG)
            while not stop_task:
                if on_hold:
                    self.mute_event.set()
                    self.unmute_event.wait()
                    on_hold = False
                    self.unmute_event.clear()
                    continue
                else:
                    message = self._transfer_queue.get()
                # end if

                if isinstance(message, InterruptPollingTask.TaskAction) and \
                        message == InterruptPollingTask.TaskAction.CANCEL:
                    stop_task = True
                elif isinstance(message, InterruptPollingTask.TaskAction) and \
                        message == InterruptPollingTask.TaskAction.MUTE:
                    on_hold = True
                else:
                    usb_message = UsbMessage(data=HexList(message[LogiusbPacketIndex.MESSAGE_INDEX]),
                                             timestamp=int(message[LogiusbPacketIndex.TIMESTAMP_INDEX]))

                    if self._time_stamped_msg_queue is not None:
                        self._time_stamped_msg_queue.put(usb_message)
                    # end if

                    interrupt_callback = self._usb_context_device.get_transfer_callback(
                        transfer_type_key=self._endpoint_address)

                    if interrupt_callback is not None:
                        # Give the interrupt buffer to the callback method
                        interrupt_callback(transport_message=usb_message)
                    # end if

                    TRACE_LOGGER.log_trace(
                        subscription_owner=self,
                        message=f"{self._reader_name}, Interrupt read on endpoint "
                                f"{self._endpoint_address_str}: {usb_message.data} at {usb_message.timestamp}ns",
                        trace_level=TraceLevel.INFO)
                # end if
            # end while
        except (KeyboardInterrupt, SystemExit):
            # Normal kill behavior
            stop_task = True
        except LogiusbException as e:
            exception_stack = TracebackLogWrapper.get_exception_stack()
            TRACE_LOGGER.log_trace(subscription_owner=self,
                                   message=f"{self._reader_name}, Exception in thread:\n{exception_stack}",
                                   trace_level=TraceLevel.ERROR)
            if e.get_cause() == LogiusbException.Cause.DOOMED:
                stop_task = True
            # end if
        except Exception:
            exception_stack = TracebackLogWrapper.get_exception_stack()
            TRACE_LOGGER.log_trace(subscription_owner=self,
                                   message=f"{self._reader_name}, Exception in thread:\n{exception_stack}",
                                   trace_level=TraceLevel.ERROR)
        # end try

        if stop_task:
            TRACE_LOGGER.log_trace(subscription_owner=self,
                                   message=f"{self._reader_name}, End thread",
                                   trace_level=TraceLevel.DEBUG)
            TRACE_LOGGER.unsubscribe(self)
            self.end_event.set()
        else:
            return (self,)
        # end if
    # end def _run

    def stop_task(self):
        """
        Stop the task (and cancel its associated transfer).
        """
        try:
            self._transfer.cancel()
        except LogiusbException as e:
            if e.get_cause() not in [LogiusbException.Cause.TRANSFER_NOT_SUBMITTED, LogiusbException.Cause.DOOMED]:
                raise
            # end if
        finally:
            if self._transfer_queue is not None:
                self._transfer_queue.put(InterruptPollingTask.TaskAction.CANCEL)
            # end if
            self.end_event.wait(1)
        # end try
    # end def stop_task

    def mute_task(self):
        """
        Set the flag to mute the task
        """
        if self._transfer_queue is not None:
            self._transfer_queue.put(InterruptPollingTask.TaskAction.MUTE)
        # end if
        self.mute_event.wait(1)
        self.mute_event.clear()
    # end def mute_task

    def unmute_task(self):
        """
        Reset the flag to unmute the task
        """
        self.unmute_event.set()
    # end def unmute_task
# end class InterruptPollingTask

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
