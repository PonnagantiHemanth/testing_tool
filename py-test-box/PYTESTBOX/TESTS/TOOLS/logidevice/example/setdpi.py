# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: logidevice.example.setdpi
:brief:   Example of logidevicehandler to set dpi.
:author:  Jerry Lin
:date:    2020/04/21
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from os import path
from random import choice
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
from pyhid.hidpp.features.mouse.adjustabledpi import AdjustableDpi
from pyhid.hidpp.features.mouse.adjustabledpi import AdjustableDpiModel
from pytestbox.device.base.adjustabledpiutils import AdjustableDpiTestUtils
from pylibrary.tools.hexlist import HexList

# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------


# HERZOG
# PID = 'C52B'
# TID = '4082'

# Artanis
# PID = 'C547'
# TID = ('4099',)

# G502 Hyjal
# PID = 'C07D'
# TID = ('C07D',)

# G705 Garnet
#PID = 'C547'
#TID = ('409D',)

# Artanis Core
# PID = 'C547'
# TID = ('409F',)

# Bazooka2
PID = 'C54D'
TID = ('40A9',)

FILE = None


def set_dpi(pid, tid, file=None):
    """
    Get/Set Dpi from DUT via logidevicehandler.

    First get the total number of motion sensors. For each sensor, report its current DPI , default DPI(only version 1
    since version 0 is not able to show it), acceptable DPI, and set a random valid DPI.

    :param pid: The product ID of the device. None for the default PID(HERZOG).
    :type pid: ``str`` or ``None``
    :param tid: The transpose ID of the device. None for the default TID(HERZOG).
    :type tid: ``tuple`` or ``None``
    :param file: A string of the output file name. None for no file - OPTIONAL
    :type file: ``str`` or ``None``
    """
    handler = LogiDeviceHandler(pid=pid, tid=tid, file=file)
    handler.start()

    feature_id = AdjustableDpi.FEATURE_ID
    sensor_count = handler.send_message(
        feature_id=feature_id, function_id=AdjustableDpiModel.INDEX.GET_SENSOR_COUNT)['sensor_count']
    stdout.write(f'\nThere are {sensor_count} motion sensor(s) in the device.\n')

    for i in range(sensor_count):
        sensor_idx = f"{i:02x}"

        result = handler.send_message(feature_id=feature_id,
                                      function_id=AdjustableDpiModel.INDEX.GET_SENSOR_DPI,
                                      sensor_idx=sensor_idx)
        if result['version'] >= 1:
            stdout.write(f"Default DPI of sensor {i}: {result['default_dpi']}\n")
        # end if
        stdout.write(f"Current DPI of sensor {i}: {result['dpi']}\n")

        dpi_list = handler.send_message(feature_id=feature_id,
                                        function_id=AdjustableDpiModel.INDEX.GET_SENSOR_DPI_LIST,
                                        sensor_idx=sensor_idx)['dpi_list']
        is_range, range_dict, list_list = AdjustableDpiTestUtils.parse_raw_dpi_list(HexList('{:030X}'.format(dpi_list)))
        if is_range:
            dpi_min, dpi_max, dpi_step = range_dict['min'], range_dict['max'], range_dict['step']
            stdout.write(f'Accepted DPI: from {dpi_min} dpi to {dpi_max} dpi, in step of {dpi_step} dpi.\n')
            dpi = choice(range((dpi_max - dpi_min)//dpi_step + 1))
            dpi = dpi_min + dpi * dpi_step
        else:
            stdout.write('Accepted DPI: ')
            stdout.write(' '.join(map(str, list_list)))
            stdout.write('\n')
            dpi = choice(list_list)
        # end if

        handler.send_message(feature_id=feature_id,
                             function_id=AdjustableDpiModel.INDEX.SET_SENSOR_DPI,
                             sensor_idx=sensor_idx, dpi='{:04X}'.format(dpi), dpi_level=0)
        result = handler.send_message(feature_id=feature_id,
                                      function_id=AdjustableDpiModel.INDEX.GET_SENSOR_DPI,
                                      sensor_idx=sensor_idx)
        stdout.write(f"New DPI of sensor {i}: {result['dpi']}\n")
    # end for

    handler.close()
# end def set_dpi


if __name__ == '__main__':
    set_dpi(pid=PID, tid=TID, file=FILE)
# end if

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
