#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: pyraspi.bus.spidev.spi
:brief: SPI device driver based on Linux IOCTL kernel commands.
:author: Thomas Preston (original author, 2014/08/22); Lila Viollette <lviollette@logitech.com>
:date: 2021/04/12
:source: https://github.com/microstack-IoT/python3-microstackcommon/blob/master/microstackcommon/spi.py
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------

import posix
import struct

from fcntl import LOCK_EX
from fcntl import LOCK_NB
from fcntl import LOCK_UN
from fcntl import flock
from fcntl import ioctl

from .linux_spi_spidev import *

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
SPIDEV = '/dev/spidev'


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class SPIInitError(Exception):
    """
    Exception raised when the SPI device file cannot be opened by the system.
    """
    pass
# end class SPIInitError


class SPIDevice(object):
    """
    An SPI Device at /dev/spi<bus>.<chip_select>.

    Note: instantiating this class does not open the SPI port. You have to call `SPIDevice.open` method for that.
    """
    def __init__(self, bus=0, chip_select=0):
        """
        :param bus: The SPI device bus number, defaults to 0 - OPTIONAL
        :type bus: ``int``
        :param chip_select: The SPI device chip_select number, defaults to 0 - OPTIONAL
        :type chip_select: ``int``
        """
        self.bus = bus
        self.chip_select = chip_select
        self.fd = None
        self.spi_device_string = f'{SPIDEV}{self.bus}.{self.chip_select}'
    # end def __init__

    def __del__(self):
        self.close()
    # end def __del__

    def open(self):
        """
        Opens the SPI device file descriptor.

        :raise ``SPIInitError``: if SPI file descriptor could not be opened
        """
        try:
            self.fd = posix.open(self.spi_device_string, posix.O_RDWR)
            try:
                flock(self.fd, LOCK_EX | LOCK_NB)
            except BlockingIOError as e:
                raise SPIInitError(f'The SPI device {self.spi_device_string} cannot be opened exclusively. '
                                   f'The file may be already locked.') from e
            # end try
        except OSError as e:
            raise SPIInitError(f'The SPI device {self.spi_device_string} cannot be open. '
                               f'Is the SPI kernel module enabled?') from e
        # end try
    # end def open

    def close(self):
        """
        Closes the SPI device file descriptor.
        """
        if getattr(self, 'fd', None) is not None:
            try:
                flock(self.fd, LOCK_UN)
            finally:
                posix.close(self.fd)
                self.fd = None
            # end try
        # end if
    # end def close

    def transaction(self, tx_bytes):
        """
        Sends bytes via the SPI bus.

        :param tx_bytes: data to send on the SPI device.
        :type tx_bytes: ``bytes``

        :return: returned data from SPI device
        :rtype: ``bytes``

        :raise ``AssertionError``: Reply message byte count does not match sent message byte count
        """
        tx_bytes = bytes(tx_bytes)

        # make some buffer space to store reading/writing
        wbuffer = ctypes.create_string_buffer(tx_bytes, len(tx_bytes))
        rbuffer = ctypes.create_string_buffer(len(tx_bytes))

        # create the spi transfer struct
        transfer = spi_ioc_transfer(
            tx_buf=ctypes.addressof(wbuffer),
            rx_buf=ctypes.addressof(rbuffer),
            len=ctypes.sizeof(wbuffer))

        # send the spi command
        byte_count = ioctl(self.fd, SPI_IOC_MESSAGE(1), transfer)
        assert byte_count == len(tx_bytes), byte_count
        return ctypes.string_at(rbuffer, ctypes.sizeof(rbuffer))
    # end def transaction

    @property
    def clock_mode(self):
        """
        Returns the current clock mode for the SPI bus.

        :return: SPI bus current clock mode: ``SPI_MODE_0``, ``SPI_MODE_1``, ``SPI_MODE_2`` or ``SPI_MODE_3``
        :rtype: ``int``
        """
        return struct.unpack('B', ioctl(self.fd, SPI_IOC_RD_MODE, ' '))[0]
    # end def property getter clock_mode

    @clock_mode.setter
    def clock_mode(self, mode):
        """
        Changes the clock mode for this SPI bus.

        +----------------+------+------+------------------------------+------------------------------------------------+
        |    ``mode``    | CPOL | CPHA | Clock Polarity in Idle State | Clock Phase Used to Sample                     |
        |                |      |      |                              | and/or Shift the Data                          |
        +================+======+======+==============================+================================================+
        | ``SPI_MODE_0`` |  0   |  0   |          Logic low           | Data sampled on rising edge and shifted out    |
        |                |      |      |                              | on the falling edge                            |
        +----------------+------+------+------------------------------+------------------------------------------------+
        | ``SPI_MODE_1`` |  0   |  1   |          Logic low           | Data sampled on the falling edge and shifted   |
        |                |      |      |                              | out on the rising edge                         |
        +----------------+------+------+------------------------------+------------------------------------------------+
        | ``SPI_MODE_2`` |  1   |  0   |          Logic high          | Data sampled on the falling edge and shifted   |
        |                |      |      |                              | out on the rising edge                         |
        +----------------+------+------+------------------------------+------------------------------------------------+
        | ``SPI_MODE_3`` |  1   |  1   |          Logic high          | Data sampled on the rising edge and shifted    |
        |                |      |      |                              | out on the falling edge                        |
        +----------------+------+------+------------------------------+------------------------------------------------+

        :param mode: SPI bus current clock mode: ``SPI_MODE_0``, ``SPI_MODE_1``, ``SPI_MODE_2`` or ``SPI_MODE_3``
        :type mode: ``int``

        :raise ``AssertionError``: Invalid SPI mode
        """
        assert mode in (SPI_MODE_0, SPI_MODE_1, SPI_MODE_2, SPI_MODE_3), f'Invalid SPI mode: {mode}'
        ioctl(self.fd, SPI_IOC_WR_MODE, struct.pack('I', mode))
    # end def property setter clock_mode

    @property
    def speed_hz(self):
        """
        Returns the current speed in Hz for this SPI bus

        :return: SPI bus current clock frequency, in Hertz
        :rtype: ``int``
        """
        return struct.unpack('I', ioctl(self.fd, SPI_IOC_RD_MAX_SPEED_HZ, ' ' * 4))[0]
    # end def property getter speed_hz

    @speed_hz.setter
    def speed_hz(self, speedhz):
        """
        Changes the speed in Hz for this SPI bus

        :param speedhz: SPI bus current clock frequency, in Hertz
        :type speedhz: ``int``
        """
        ioctl(self.fd, SPI_IOC_WR_MAX_SPEED_HZ, struct.pack('I', speedhz))
    # end def property setter speed_hz
# end class SPIDevice

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
