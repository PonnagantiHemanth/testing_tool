#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.base.serial_logger
:brief: module to log serial output into separate files
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/05/23
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import perf_counter_ns

import serial


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
def print_serial_debug(source, logger, thread):
    """
    Run a thread that read the UART and print it to a logger. to be called in a ``StoppableThread``

    :param source: Source for the uart ex. "/dev/ttyUSB4"
    :type source: ``str``
    :param logger: Logger to print
    :type logger: ``Logger``
    :param thread: thread object
    :type thread: ``StoppableThread``
    """
    logger.logRaw(f"\nSTARTING UART LISTENING ON {source!s}\n")
    try:
        ser = serial.Serial(
            str(source), 1000000, rtscts=0, parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0.5)
    except Exception as e:
        logger.logError(f"ERROR Starting UART: {e}")
        return
    # end try
    logger.logRaw("UART session started\n")

    while not thread.stopped():
        read_text = ser.readline()
        if not read_text == b'':
            logger.logRaw(f"[UART@{perf_counter_ns()}ns] {read_text!s}")
        # end if
    # end while
    ser.close()
    logger.logRaw("UART session closed\n")
# end def print_serial_debug

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
