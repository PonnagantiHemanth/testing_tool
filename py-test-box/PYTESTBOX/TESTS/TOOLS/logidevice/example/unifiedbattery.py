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
from time import sleep
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
from pyhid.hidpp.features.common.unifiedbattery import UnifiedBattery
from pyhid.hidpp.features.common.unifiedbattery import UnifiedBatteryModel

# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------


# HERZOG
# PID = 'C52B'
# TID = '4082'

# PID = 'C547'
# TID = '4099'

# G502 Hyjal
# PID = 'C07D'
# TID = ('C07D',)

# G705 Garnet
# PID = 'C547'
# TID = ('409D',)

# Artanis Core
# PID = 'C547'
# TID = ('409F',)

# Artanis Premium
# PID = 'C547'
# TID = ('4099',)

# Bazooka2
PID = 'C54D'
TID = ('40A9',)

FILE = None


def unified_battery(pid, tid, file=None):
    """
    Example of unified battery from the DUT via logidevicehandler.

    :param pid: The product ID of the device. None for the default PID(HERZOG).
    :type pid: ``str`` or ``None``
    :param tid: The transpose ID of the device. None for the default TID(HERZOG).
    :type tid: ``tuple`` or ``None``
    :param file: A string of the output file name. None for no file - OPTIONAL
    :type file: ``str`` or ``None``
    """
    handler = LogiDeviceHandler(pid=pid, tid=tid, file=file)
    handler.start()

    feature_id = UnifiedBattery.FEATURE_ID

    # Get capabilities
    get_capabilities = handler.send_message(feature_id=feature_id,
                                            function_id=UnifiedBatteryModel.INDEX.GET_CAPABILITIES)
    stdout.write(f'get_capabilities = {get_capabilities}\n')

    # Get status
    get_status_response = handler.send_message(feature_id=feature_id, function_id=UnifiedBatteryModel.INDEX.GET_STATUS)
    stdout.write(f'get_status_response = {get_status_response}\n')

    # Show battery status
    show_battery_status_response = handler.send_message(feature_id=feature_id,
                                                        function_id=UnifiedBatteryModel.INDEX.SHOW_BATTERY_STATUS)
    stdout.write(f'show_battery_status_response  = {show_battery_status_response}\n')

    # Wait for the SoC decrease
    sleep(10)

    battery_status_event = handler.get_hidpp_event()
    stdout.write(f'battery_status_event = {battery_status_event}\n')

    handler.close()
# end def unified_battery


if __name__ == '__main__':
    unified_battery(pid=PID, tid=TID, file=FILE)
# end if

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
