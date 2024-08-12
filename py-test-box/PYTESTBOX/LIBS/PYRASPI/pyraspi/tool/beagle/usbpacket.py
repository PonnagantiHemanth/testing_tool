#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyraspi.tool.beagle.usbpacket
:brief: Beagle USB packet class
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2024/04/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from typing import List
from typing import Optional

from pyraspi.tool.beagle.beagle_py import BG_EVENT_USB_CHIRP_J
from pyraspi.tool.beagle.beagle_py import BG_EVENT_USB_CHIRP_K
from pyraspi.tool.beagle.beagle_py import BG_EVENT_USB_DIGITAL_INPUT
from pyraspi.tool.beagle.beagle_py import BG_EVENT_USB_DIGITAL_INPUT_MASK
from pyraspi.tool.beagle.beagle_py import BG_EVENT_USB_FULL_SPEED
from pyraspi.tool.beagle.beagle_py import BG_EVENT_USB_HIGH_SPEED
from pyraspi.tool.beagle.beagle_py import BG_EVENT_USB_HOST_CONNECT
from pyraspi.tool.beagle.beagle_py import BG_EVENT_USB_HOST_DISCONNECT
from pyraspi.tool.beagle.beagle_py import BG_EVENT_USB_KEEP_ALIVE
from pyraspi.tool.beagle.beagle_py import BG_EVENT_USB_LOW_OVER_FULL_SPEED
from pyraspi.tool.beagle.beagle_py import BG_EVENT_USB_LOW_SPEED
from pyraspi.tool.beagle.beagle_py import BG_EVENT_USB_RESET
from pyraspi.tool.beagle.beagle_py import BG_EVENT_USB_RESUME
from pyraspi.tool.beagle.beagle_py import BG_EVENT_USB_SPEED_UNKNOWN
from pyraspi.tool.beagle.beagle_py import BG_EVENT_USB_SUSPEND
from pyraspi.tool.beagle.beagle_py import BG_EVENT_USB_TARGET_CONNECT
from pyraspi.tool.beagle.beagle_py import BG_EVENT_USB_TARGET_DISCONNECT
from pyraspi.tool.beagle.beagle_py import BG_READ_ERR_MIDDLE_OF_PACKET
from pyraspi.tool.beagle.beagle_py import BG_READ_ERR_PARTIAL_LAST_BYTE
from pyraspi.tool.beagle.beagle_py import BG_READ_ERR_SHORT_BUFFER
from pyraspi.tool.beagle.beagle_py import BG_READ_ERR_UNEXPECTED
from pyraspi.tool.beagle.beagle_py import BG_READ_OK
from pyraspi.tool.beagle.beagle_py import BG_READ_TIMEOUT
from pyraspi.tool.beagle.beagle_py import BG_READ_USB_END_OF_CAPTURE
from pyraspi.tool.beagle.beagle_py import BG_READ_USB_ERR_BAD_CRC
from pyraspi.tool.beagle.beagle_py import BG_READ_USB_ERR_BAD_PID
from pyraspi.tool.beagle.beagle_py import BG_READ_USB_ERR_BAD_SIGNALS
from pyraspi.tool.beagle.beagle_py import BG_READ_USB_ERR_BAD_SYNC
from pyraspi.tool.beagle.beagle_py import BG_READ_USB_ERR_BIT_STUFF
from pyraspi.tool.beagle.beagle_py import BG_READ_USB_ERR_FALSE_EOP
from pyraspi.tool.beagle.beagle_py import BG_READ_USB_ERR_LONG_EOP
from pyraspi.tool.beagle.beagle_py import BG_READ_USB_TRUNCATION_MODE
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_ACK
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_DATA0
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_DATA1
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_DATA2
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_EXT
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_IN
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_MDATA
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_NAK
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_NYET
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_OUT
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_PING
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_PRE
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_SETUP
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_SOF
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_SPLIT
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_STALL


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class UsbPacket:
    """
    Define the structure to store the USB packet information
    """
    def __init__(self, pid, data, crc, timestamp):
        """
        :param pid: USB packet identifier, refer to `pid_to_str` method
        :type pid: ``int``
        :param data: USB packet data
        :type data: ``list[int] or None``
        :param crc: USB packet CRC
        :type crc: ``int``
        :param timestamp: USB packet timestamp, in nanoseconds
        :type timestamp: ``int``
        """
        self.__status: int = None
        self.__event: int = None
        self.pid: int = pid
        self.data: Optional[List[int]] = data
        self.crc: int = crc
        self.timestamp: int = timestamp
    # end def __init__

    @property
    def status(self):
        """
        Property getter of ``status``.

        :return: ``status`` value
        :rtype: ``int``
        """
        return self.__status
    # end def property getter status

    @status.setter
    def status(self, value):
        """
        Property setter of ``status``.

        :param value: ``status`` value
        :type value: ``int``

        :raise ``AssertionError``: If ``value`` is not a ``LogitechProtocol``
        """
        assert isinstance(value, int), \
            f"{self.__class__.__name__} status attribute is a ``int``, {value} is not"
        self.__status = value
    # end def property setter status

    @property
    def event(self):
        """
        Property getter of ``event``.

        :return: ``event`` value
        :rtype: ``int``
        """
        return self.__event
    # end def property getter event

    @event.setter
    def event(self, value):
        """
        Property setter of ``event``.

        :param value: ``event`` value
        :type value: ``int``

        :raise ``AssertionError``: If ``value`` is not a ``LogitechProtocol``
        """
        assert isinstance(value, int), \
            f"{self.__class__.__name__} event attribute is a ``int``, {value} is not"
        self.__event = value
    # end def property setter event

    def __str__(self):
        str_to_return = f"{self.__class__.__name__}(status: {self.status},  event: {self.event}"

        str_to_return += f", PID: {self.pid_to_str(self.pid)}"
        if self.data is not None:
            str_to_return += f", Data: {self.data}"
        # end if
        str_to_return += f", CRC: {self.crc}"

        return str_to_return
    # end def __str__

    @staticmethod
    def pid_to_str(pid):
        """
        Return the packet identifier string

        :param pid: packet identifier
        :type pid: ``int``

        :return: packet identifier string
        :rtype: ``str``
        """
        if pid == BG_USB_PID_OUT:
            pid_string = "OUT"
        elif pid == BG_USB_PID_IN:
            pid_string = "IN"
        elif pid == BG_USB_PID_SOF:
            pid_string = "SOF"
        elif pid == BG_USB_PID_SETUP:
            pid_string = "SETUP"
        elif pid == BG_USB_PID_DATA0:
            pid_string = "DATA0"
        elif pid == BG_USB_PID_DATA1:
            pid_string = "DATA1"
        elif pid == BG_USB_PID_DATA2:
            pid_string = "DATA2"
        elif pid == BG_USB_PID_MDATA:
            pid_string = "MDATA"
        elif pid == BG_USB_PID_ACK:
            pid_string = "ACK"
        elif pid == BG_USB_PID_NAK:
            pid_string = "NAK"
        elif pid == BG_USB_PID_STALL:
            pid_string = "STALL"
        elif pid == BG_USB_PID_NYET:
            pid_string = "NYET"
        elif pid == BG_USB_PID_PRE:
            pid_string = "PRE"
        elif pid == BG_USB_PID_SPLIT:
            pid_string = "SPLIT"
        elif pid == BG_USB_PID_PING:
            pid_string = "PING"
        elif pid == BG_USB_PID_EXT:
            pid_string = "EXT"
        else:
            pid_string = "INVALID"
        # end if
        return pid_string
    # end def pid_to_str

    @staticmethod
    def general_status_to_str(status):
        """
        Return general status codes string

        :param status: common Beagle read status codes
        :type status: ``int``

        :return: read status string
        :rtype: ``str``
        """
        status_string = ''
        if status == BG_READ_OK:
            status_string = "OK"
        else:
            if status & BG_READ_TIMEOUT:
                status_string = "TIMEOUT;"
            # end if
            if status & BG_READ_ERR_UNEXPECTED:
                status_string += "UNEXPECTED;"
            # end if
            if status & BG_READ_ERR_MIDDLE_OF_PACKET:
                status_string += "MIDDLE;"
            # end if
            if status & BG_READ_ERR_SHORT_BUFFER:
                status_string += "SHORT BUFFER;"
            # end if
            if status & BG_READ_ERR_PARTIAL_LAST_BYTE:
                status_string += f"PARTIAL_BYTE(bit {status & 0xff})"
            # end if
        # end if
        return status_string
    # end def general_status_to_str

    @staticmethod
    def usb_status_to_str(status):
        """
        Return USB status codes string

        :param status: common Beagle read status codes
        :type status: ``int``

        :return: USB status codes string
        :rtype: ``str``
        """
        status_string = ''
        if status & BG_READ_USB_ERR_BAD_SIGNALS:
            status_string += "BAD_SIGNAL;"
        # end if
        if status & BG_READ_USB_ERR_BAD_SYNC:
            status_string += "BAD_SYNC;"
        # end if
        if status & BG_READ_USB_ERR_BIT_STUFF:
            status_string += "BAD_STUFF;"
        # end if
        if status & BG_READ_USB_ERR_FALSE_EOP:
            status_string += "BAD_EOP;"
        # end if
        if status & BG_READ_USB_ERR_LONG_EOP:
            status_string += "LONG_EOP;"
        # end if
        if status & BG_READ_USB_ERR_BAD_PID:
            status_string += "BAD_PID;"
        # end if
        if status & BG_READ_USB_ERR_BAD_CRC:
            status_string += "BAD_CRC;"
        # end if
        if status & BG_READ_USB_TRUNCATION_MODE:
            status_string += "TRUNCATION_MODE;"
        # end if
        if status & BG_READ_USB_END_OF_CAPTURE:
            status_string += "END_OF_CAPTURE;"
        # end if
        return status_string
    # end def usb_status_to_str

    @staticmethod
    def usb_events_to_str(events):
        """
        Return USB event codes string

        :param events: common Beagle event codes
        :type events: ``int``

        :return: USB event string
        :rtype: ``str``
        """
        usb_event_string = ''
        if events & BG_EVENT_USB_HOST_DISCONNECT:
            usb_event_string = "HOST_DISCON;"
        # end if
        if events & BG_EVENT_USB_TARGET_DISCONNECT:
            usb_event_string += "TGT_DISCON;"
        # end if
        if events & BG_EVENT_USB_RESET:
            usb_event_string += "RESET;"
        # end if
        if events & BG_EVENT_USB_HOST_CONNECT:
            usb_event_string += "HOST_CONNECT;"
        # end if
        if events & BG_EVENT_USB_TARGET_CONNECT:
            usb_event_string += "TGT_CONNECT/UNRST;"
        # end if
        if events & BG_EVENT_USB_DIGITAL_INPUT:
            usb_event_string += f"INPUT_TRIGGER {events & BG_EVENT_USB_DIGITAL_INPUT_MASK}"
        # end if
        if events & BG_EVENT_USB_CHIRP_J:
            usb_event_string += "CHIRP_J;"
        # end if
        if events & BG_EVENT_USB_CHIRP_K:
            usb_event_string += "CHIRP_K;"
        # end if
        if events & BG_EVENT_USB_KEEP_ALIVE:
            usb_event_string += "KEEP_ALIVE;"
        # end if
        if events & BG_EVENT_USB_SUSPEND:
            usb_event_string += "SUSPEND;"
        # end if
        if events & BG_EVENT_USB_RESUME:
            usb_event_string += "RESUME;"
        # end if
        if events & BG_EVENT_USB_LOW_SPEED:
            usb_event_string += "LOW_SPEED;"
        # end if
        if events & BG_EVENT_USB_FULL_SPEED:
            usb_event_string += "FULL_SPEED;"
        # end if
        if events & BG_EVENT_USB_HIGH_SPEED:
            usb_event_string += "HIGH_SPEED;"
        # end if
        if events & BG_EVENT_USB_SPEED_UNKNOWN:
            usb_event_string += "UNKNOWN_SPEED;"
        # end if
        if events & BG_EVENT_USB_LOW_OVER_FULL_SPEED:
            usb_event_string += "LOW_OVER_FULL_SPEED;"
        # end if
        return usb_event_string
    # end def usb_events_to_str
# end class UsbPacket

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
