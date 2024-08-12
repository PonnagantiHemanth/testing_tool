# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: logidevice.example.getmousemovement
:brief:   Example of logidevicehandler to get mouse movement.
:author:  Jerry Lin
:date:    2020/04/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from os import path
from sys import stdout
import sys

FILE_PATH = path.abspath(__file__)
WS_DIR = FILE_PATH[:FILE_PATH.rfind("TESTS")]
TOOLS_DIR = path.join(WS_DIR, "TESTS", "TOOLS")
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)
# end if
from logidevice.logidevicehandler import LogiDeviceHandler
from pychannel.channelinterfaceclasses import LogitechReportType

# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# RECOLL
# PID = 'C53F'
# TID = '4074'
# # G502 Hyjal
# PID = 'C07D'
# TID = 'C07D'

# Bazooka 2
PID = 'C54D'
TID = ('40A9',)

# Artanis Core
# PID = 'C547'
# TID = ('409F',)

FILE = None

BITS = 12


def get_value(num):
    """Unsigned num to signed num"""
    mask = num & ((1 << BITS) - 1)
    result = mask if mask < (1 << (BITS-1)) else mask - (1 << BITS)
    return result
# end def get_value


def get_mouse_movement(pid, tid, file=None):
    """
    Get mouse message from DUT via logidevicehandler.

    Continuously get the message from framework and show on screen until keyboard interrupt.

    :param pid: The product ID of the device. None for the default PID(HERZOG).
    :type pid: ``str`` or ``None``
    :param tid: The transpose ID of the device. None for the default TID(HERZOG).
    :type tid: ``tuple`` or ``None``
    :param file: A string of the output file name. None for no file - OPTIONAL
    :type file: ``str`` or ``None``
    """

    with LogiDeviceHandler(pid=pid, tid=tid, file=file) as handler:
        handler.mouse_reset()

        while True:
            # get HidMouse and HidKeyboard
            messages = handler.get_hid_message_from_hid_queue(report_type=LogitechReportType.MOUSE)
            # only HidMouse
            messages = list(filter(
                lambda x: x['messageType'] == 'HidMouse' or x['messageType'] == 'HidMouseNvidiaExtension', messages))

            for msg in messages:
                stdout.write(f"(dx, dy, timestamp) = {get_value(msg['x'])},{get_value(msg['y'])},{msg['time_stamp']}\n")
            # end for
        # end while
    # end with
# end def get_mouse_movement


if __name__ == '__main__':
    get_mouse_movement(pid=PID, tid=TID, file=FILE)
# end if

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
