#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pytransport.usb.libusbcontext.usbtasks
:brief: Define Tasks managing USB communication.
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2021/04/28
"""
# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
import os
import sys
from threading import Event
import time

from pylibrary.system.tracelogger import TraceLevel
from pylibrary.system.tracelogger import TraceLogger
from pylibrary.tools.threadutils import Task
from pylibrary.tools.tracebacklog import TracebackLogWrapper
from pytransport.usb.usbcontext import UsbContext
from pytransport.usb.usbcontext import UsbContextDevice

# Import libusb python wrapper through pysetup
try:
    # noinspection PyUnresolvedReferences
    import pysetup
    # noinspection PyUnresolvedReferences
    os.environ['PATH'] = "%s;%s" % (pysetup.LIBUSB, os.environ['PATH'])
    # noinspection PyUnresolvedReferences
    import usb1
except ImportError:
    pass
# end try


# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------
TRACE_LOGGER = TraceLogger.get_instance()

# Timeout for interrupt polling [milliseconds]
if sys.platform == 'linux':
    # 1 task for context event handle
    # 3 tasks per usb device (mouse, keyboard and hid++ interfaces)
    # = 1 + ( 3 * 4 ) = 13 tasks simultaneously
    MAX_THREADS = 13
    # Greater timing to let libusb fully handle the polling mechanism
    USB_TIMEOUT = 2
else:
    # On windows, only 2 threads
    MAX_THREADS = 2
    # Short timeout to allow a task load balancing with the 2 available threads
    USB_TIMEOUT = 0.1
# end if


# ------------------------------------------------------------------------------
# Implementation
# ------------------------------------------------------------------------------
class ContextEventHandleTask(Task):
    """
    Task that call the method ``usb1.USBContext.handleEventsTimeout``. This is used for example for hotplug purposes.
    """

    def __init__(self, libusb_context, trace_level=None, trace_file_name=None, trace_name=None):
        """
        :param libusb_context: Context that create that task
        :type libusb_context: ``usb1.USBContext``
        :param trace_level: Trace level for this object - OPTIONAL
        :type trace_level: ``TraceLevel`` or ``None``
        :param trace_file_name: Trace output as a file name. If ``None``, ``sys.stdout`` will be used - OPTIONAL
        :type trace_file_name: ``str`` or ``None``
        :param trace_name: Trace name for this object - OPTIONAL
        :type trace_name: ``str`` or ``None``
        """
        # noinspection PyProtectedMember
        self._libusb_context = libusb_context
        self.stop_event = Event()
        self.end_event = Event()
        TRACE_LOGGER.subscribe(
            subscription_owner=self, trace_level=trace_level, trace_file_name=trace_file_name, trace_name=trace_name)

        TRACE_LOGGER.log_trace(
            subscription_owner=self, message="Start thread", trace_level=TraceLevel.DEBUG)
        super().__init__(self._run)
    # end def __init__

    def __del__(self):
        if TRACE_LOGGER.is_subscribe(subscription_owner=self):
            TRACE_LOGGER.unsubscribe(subscription_owner=self)
        # end if
    # end def __del__

    def _run(self):
        """
        Run method for the event handle thread.
        """
        # noinspection PyBroadException
        try:
            while not self.stop_event.is_set():
                self._libusb_context.handleEventsTimeout(tv=USB_TIMEOUT)
            # end while
        except (KeyboardInterrupt, SystemExit):
            # Normal kill behavior
            self.stop_event.set()
        except Exception:
            exception_stack = TracebackLogWrapper.get_exception_stack()
            TRACE_LOGGER.log_trace(subscription_owner=self,
                                   message=f"Exception in thread:\n{exception_stack}",
                                   trace_level=TraceLevel.ERROR)
        # end try

        if self.stop_event.is_set():
            TRACE_LOGGER.log_trace(
                subscription_owner=self, message="End thread", trace_level=TraceLevel.DEBUG)
            TRACE_LOGGER.unsubscribe(self)
            self.end_event.set()
        else:
            return (self,)
        # end if
    # end def _run
# end class ContextEventHandleTask


class InterruptPollingTask(Task):
    """
    Task that does the polling on the interrupt endpoint.
    """
        
    def __init__(self, libusb_usb_context, usb_context_device, endpoint_number, data_size, time_stamped_msg_queue=None,
                 trace_name=None):
        """
        :param libusb_usb_context: Context that create that task
        :type libusb_usb_context: ``UsbContext``
        :param usb_context_device: Context device associated with the task
        :type usb_context_device: ``UsbContextDevice``
        :param endpoint_number: Endpoint to get the data from
        :type endpoint_number: ``int``
        :param data_size: Length of the buffer to receive data
        :type data_size: ``int``
        :param time_stamped_msg_queue: Queue to get all USB message received - OPTIONAL
        :type time_stamped_msg_queue: ``Queue`` or ``None``
        :param trace_name: Trace name of the task - OPTIONAL
        :type trace_name: ``str`` or ``None``
        """
        self._libusb_usb_context = libusb_usb_context
        self._usb_context_device = usb_context_device
        self._interrupt_ep_in = endpoint_number
        self._data_size = data_size
        self._time_stamped_msg_queue = time_stamped_msg_queue

        self.stop_event = Event()
        self.end_event = Event()
        self.polling_started_event = Event()

        TRACE_LOGGER.subscribe(
            subscription_owner=self,
            trace_file_name=self._libusb_usb_context.trace_file_name,
            trace_name=trace_name,
            linked_owner=self._libusb_usb_context)

        TRACE_LOGGER.log_trace(subscription_owner=self,
                               message=f"{self._usb_context_device.reader_name}, Start thread",
                               trace_level=TraceLevel.DEBUG)
        super().__init__(self._run)
    # end def __init__

    def __del__(self):
        if TRACE_LOGGER.is_subscribe(subscription_owner=self):
            TRACE_LOGGER.unsubscribe(subscription_owner=self)
        # end if
    # end def __del__

    def _run(self):
        """
        Run method for the interrupt polling.
        """
        # noinspection PyBroadException
        try:
            TRACE_LOGGER.log_trace(subscription_owner=self,
                                   message=f"{self._usb_context_device.reader_name}, Thread started, "
                                           f"{time.perf_counter_ns()//1e6}ms",
                                   trace_level=TraceLevel.EXTRA_DEBUG)
            while not self.stop_event.is_set():
                self.polling_started_event.set()
                usb_message = self._libusb_usb_context.interrupt_read(
                    usb_context_device=self._usb_context_device,
                    endpoint=self._interrupt_ep_in,
                    w_length=self._data_size,
                    timeout=USB_TIMEOUT,
                    trace_owner=self)
                self.polling_started_event.clear()

                if self._time_stamped_msg_queue is not None:
                    self._time_stamped_msg_queue.put_nowait(usb_message)
                # end if

                interrupt_callback = self._usb_context_device.get_transfer_callback(
                    transfer_type_key=self._interrupt_ep_in)

                if interrupt_callback is not None:
                    # Give the interrupt buffer to the callback method
                    interrupt_callback(transport_message=usb_message)
                # end if
            # end while
        except (KeyboardInterrupt, SystemExit):
            # Normal kill behavior
            self.stop_event.set()
        except usb1.libusb1.USBError as e:
            if str(e) == 'LIBUSB_ERROR_IO [-1]' or \
                    str(e) == 'LIBUSB_ERROR_TIMEOUT [-7]' or \
                    str(e) == 'LIBUSB_ERROR_BUSY [-6]':
                TRACE_LOGGER.log_trace(subscription_owner=self,
                                       message=f"{self._usb_context_device.reader_name}, Libusb Exception in thread: "
                                               f"{str(e)}, {int(time.perf_counter_ns()//1e6)}ms",
                                       trace_level=TraceLevel.EXTRA_DEBUG)
            elif str(e) == 'LIBUSB_ERROR_NO_DEVICE [-4]':
                # Device Reset sent
                TRACE_LOGGER.log_trace(subscription_owner=self,
                                       message=f"{self._usb_context_device.reader_name}, Libusb "
                                               f"Exception in thread: {str(e)}",
                                       trace_level=TraceLevel.EXTRA_DEBUG)
                self.stop_event.set()
            else:
                exception_stack = TracebackLogWrapper.get_exception_stack()
                TRACE_LOGGER.log_trace(subscription_owner=self,
                                       message=f"{self._usb_context_device.reader_name}, Libusb "
                                               f"Exception in thread:\n{exception_stack}",
                                       trace_level=TraceLevel.ERROR)
            # end if
        except Exception:
            exception_stack = TracebackLogWrapper.get_exception_stack()
            TRACE_LOGGER.log_trace(subscription_owner=self,
                                   message=f"{self._usb_context_device.reader_name}, Exception "
                                           f"in thread:\n{exception_stack}",
                                   trace_level=TraceLevel.ERROR)
        finally:
            self.polling_started_event.clear()
        # end try

        if self.stop_event.is_set():
            TRACE_LOGGER.log_trace(subscription_owner=self,
                                   message=f"{self._usb_context_device.reader_name}, End thread",
                                   trace_level=TraceLevel.DEBUG)
            TRACE_LOGGER.unsubscribe(self)
            self.end_event.set()
        else:
            return (self,)
        # end if
    # end def _run
# end class InterruptPollingTask

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
