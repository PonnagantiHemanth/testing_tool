# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: logidevice.example.unifiedbattery
:brief:   Example of logidevicehandler to get battery status.
:author:  YY Liu  <yliu5@logitech.com>
:date:    2022/06/29
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
TESTSUITES_DIR = path.join(WS_DIR, "TESTS", "TESTSUITES")
if TESTSUITES_DIR not in sys.path:
    sys.path.insert(0, TESTSUITES_DIR)
# end if
# Get dpi list from raw data
PYLIBRARY_DIR = path.join(WS_DIR, "LIBS", "PYLIBRARY")

if PYLIBRARY_DIR not in sys.path:
    sys.path.insert(0, PYLIBRARY_DIR)
# end if
from logidevice.logidevicehandler import LogiDeviceHandler
from pyhid.hidpp.features.gaming.brightnesscontrol import BrightnessControl
from pyhid.hidpp.features.gaming.brightnesscontrol import BrightnessControlModel

# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------


# G915
PID = 'C547'
TID = ('408E',)

FILE = None


def brightness_control(pid, tid, file=None):
    """
    Example of brightness control from the DUT via logidevicehandler.

    :param pid: The product ID of the device. None for the default PID(HERZOG).
    :type pid: ``str`` or ``None``
    :param tid: The transpose ID of the device. None for the default TID(HERZOG).
    :type tid: ``tuple`` or ``None``
    :param file: A string of the output file name. None for no file - OPTIONAL
    :type file: ``str`` or ``None``
    """
    handler = LogiDeviceHandler(pid=pid, tid=tid, file=file)
    handler.start()

    feature_id = BrightnessControl.FEATURE_ID

    # Get info
    get_info_response = handler.send_message(feature_id=feature_id,
                                             function_id=BrightnessControlModel.INDEX.GET_INFO)
    stdout.write(f'get_info response = {get_info_response}\n')

    # Get brightness
    get_brightness_response = handler.send_message(feature_id=feature_id,
                                                   function_id=BrightnessControlModel.INDEX.GET_BRIGHTNESS)
    stdout.write(f'get_brightness response = {get_brightness_response}\n')

    # Set brightness
    set_brightness_response = handler.send_message(feature_id=feature_id,
                                                   function_id=BrightnessControlModel.INDEX.SET_BRIGHTNESS,
                                                   brightness=50)
    stdout.write(f'set_brightness response  = {set_brightness_response}\n')

    handler.close()
# end def brightness_control


if __name__ == '__main__':
    brightness_control(pid=PID, tid=TID, file=FILE)
# end if

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
