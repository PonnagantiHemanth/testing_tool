#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: pyraspi.bus.spidev.linux_spi_spidev
:brief: Python portage of <linux/spi/spidev.h>
:author: Thomas Preston (original author, 2013/09/11); Lila Viollette <lviollette@logitech.com>
:date: 2021/04/12
:source: https://github.com/microstack-IoT/python3-microstackcommon/blob/master/microstackcommon/linux_spi_spidev.py

Converted from <linux/spi/spidev.h>
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import ctypes
from .asm_generic_ioctl import _IOC_SIZEBITS
from .asm_generic_ioctl import _IOR
from .asm_generic_ioctl import _IOW


# ------------------------------------------------------------------------------
# constants and macros (as Python methods)
# ------------------------------------------------------------------------------
"""
Clock Phase and Polarity settings
:ivar SPI_CPHA : Clock phase bitmask
:ivar SPI_CPOL : Clock polarity bitmask
"""
SPI_CPHA = 0x01
SPI_CPOL = 0x02

"""
SPI mode: combined Clock Phase and Polarity settings
:ivar SPI_MODE_0 :
:ivar SPI_MODE_1 :
:ivar SPI_MODE_2 :
:ivar SPI_MODE_3 :
"""
SPI_MODE_0 = 0
SPI_MODE_1 = SPI_CPHA
SPI_MODE_2 = SPI_CPOL
SPI_MODE_3 = SPI_CPOL | SPI_CPHA

"""
Other SPI settings.
Note: Some settings may not be supported depending on the hardware/software.

:ivar SPI_CS_HIGH   : Chip select active state bitmask
:ivar SPI_LSB_FIRST : LSB-first mode bitmask
:ivar SPI_3WIRE     : 3-Wire mode bitmask
:ivar SPI_LOOP      : Loopback test mode bitmask
:ivar SPI_NO_CS     : No Chip Select mode bitmask
:ivar SPI_READY     :
"""
SPI_CS_HIGH = 0x04
SPI_LSB_FIRST = 0x08
SPI_3WIRE = 0x10
SPI_LOOP = 0x20
SPI_NO_CS = 0x40
SPI_READY = 0x80

"""
IOCTL commands
The magic number is an identifier used by `ioctl` kernel interface.
:ivar SPI_IOC_MAGIC : SPI device are identified by the value 107 (character 'k').
"""
SPI_IOC_MAGIC = 107  # ord('k')


class spi_ioc_transfer(ctypes.Structure):
    """
    struct spi_ioc_transfer - describes a single SPI transfer
    Python implementation of C structure ``struct spi_ioc_transfer`` from `<linux/spi/spidev.h>`

    Structure members:

    :ivar tx_buf:        Holds pointer to userspace buffer with transmit data, or null.
                         If no data is provided, zeroes are shifted out.
    :ivar rx_buf:        Holds pointer to userspace buffer for receive data, or null.
    :ivar len:           Length of tx and rx buffers, in bytes.
    :ivar speed_hz:      Temporary override of the device's bitrate.
    :ivar bits_per_word: Temporary override of the device's wordsize.
    :ivar delay_usecs:   If nonzero, how long to delay after the last bit transfer
                         before optionally deselecting the device before the next transfer.
    :ivar cs_change:     True to deselect device before starting the next transfer.

    :vartype tx_buf:        ctypes.c_uint64
    :vartype rx_buf:        ctypes.c_uint64
    :vartype len:           ctypes.c_uint32
    :vartype speed_hz:      ctypes.c_uint32
    :vartype delay_usecs:   ctypes.c_uint16
    :vartype bits_per_word: ctypes.c_uint8
    :vartype cs_change:     ctypes.c_uint8
    :vartype pad:           ctypes.c_uint32

    NOTE: struct layout is the same in 64bit and 32bit userspace.

    This structure is mapped directly to the kernel spi_transfer structure;
    the fields have the same meanings, except of course that the pointers
    are in a different address space (and may be of different sizes in some
    cases, such as 32-bit i386 userspace over a 64-bit x86_64 kernel).
    Zero-initialize the structure, including currently unused fields, to
    accommodate potential future updates.

    ``SPI_IOC_MESSAGE`` gives userspace the equivalent of kernel spi_sync().
    Pass it an array of related transfers, they'll execute together.
    Each transfer may be half duplex (either direction) or full duplex.::

      struct spi_ioc_transfer mesg[4];
      ...
      status = ioctl(fd, SPI_IOC_MESSAGE(4), mesg);

    So for example one transfer might send a nine bit command (right aligned
    in a 16-bit word), the next could read a block of 8-bit data before
    terminating that command by temporarily deselecting the chip; the next
    could send a different nine bit command (re-selecting the chip), and the
    last transfer might write some register values.
    """
    _fields_ = [
        ("tx_buf",        ctypes.c_uint64),
        ("rx_buf",        ctypes.c_uint64),
        ("len",           ctypes.c_uint32),
        ("speed_hz",      ctypes.c_uint32),
        ("delay_usecs",   ctypes.c_uint16),
        ("bits_per_word", ctypes.c_uint8),
        ("cs_change",     ctypes.c_uint8),
        ("pad",           ctypes.c_uint32)]

    __slots__ = [name for name, type in _fields_]
# end class spi_ioc_transfer


def SPI_MSGSIZE(N):
    """
    IOCTL command helper: computes the  transfer descriptor array byte size.

    Used in ``SPI_IOC_MESSAGE``.

    :param N: the number of spi transfer struct stored in `transfer` array
    :type N: ``int``

    :return: byte size, or zero if it overflows a certain size
    :rtype: ``int``
    """
    if (N * ctypes.sizeof(spi_ioc_transfer)) < (1 << _IOC_SIZEBITS):
        return N * ctypes.sizeof(spi_ioc_transfer)
    else:
        return 0
    # end if
# end def SPI_MSGSIZE


def SPI_IOC_MESSAGE(N):
    """
    IOCTL command generator: Starts a SPI transfer

    Usage:
       `ioctl(self.fd, SPI_IOC_MESSAGE(1), transfer)`

    :param N: the number of spi transfer struct stored in `transfer` array
    :type N: ``int``

    :return: raw IOCTL command
    :rtype: ``int``
    """
    return _IOW(SPI_IOC_MAGIC, 0, ctypes.c_char * SPI_MSGSIZE(N))
# end def SPI_IOC_MESSAGE


"""
Read / Write of SPI mode (``SPI_MODE_0`` ... ``SPI_MODE_3``)
:ivar SPI_IOC_RD_MODE : Command to read the SPI mode setting
:ivar SPI_IOC_WR_MODE : Command to write the SPI mode setting
"""
SPI_IOC_RD_MODE = _IOR(SPI_IOC_MAGIC, 1, ctypes.c_uint8)
SPI_IOC_WR_MODE = _IOW(SPI_IOC_MAGIC, 1, ctypes.c_uint8)

"""
Read / Write SPI bit justification
:ivar SPI_IOC_RD_LSB_FIRST : Command to read the LSB-first setting
:ivar SPI_IOC_WR_LSB_FIRST : Command to write the LSB-first setting
"""
SPI_IOC_RD_LSB_FIRST = _IOR(SPI_IOC_MAGIC, 2, ctypes.c_uint8)
SPI_IOC_WR_LSB_FIRST = _IOW(SPI_IOC_MAGIC, 2, ctypes.c_uint8)

"""
Read / Write SPI device word length (1..N)
:ivar SPI_IOC_RD_BITS_PER_WORD : Command to read the number of bits per word setting
:ivar SPI_IOC_WR_BITS_PER_WORD : Command to write the number of bits per word setting
"""
SPI_IOC_RD_BITS_PER_WORD = _IOR(SPI_IOC_MAGIC, 3, ctypes.c_uint8)
SPI_IOC_WR_BITS_PER_WORD = _IOW(SPI_IOC_MAGIC, 3, ctypes.c_uint8)

"""
Read / Write SPI device default max speed hz
# :ivar SPI_IOC_RD_MAX_SPEED_HZ : Command to read maximum SPI clock speed setting [Hz]
# :ivar SPI_IOC_WR_MAX_SPEED_HZ : Command to write maximum SPI clock speed setting [Hz]
# """
SPI_IOC_RD_MAX_SPEED_HZ = _IOR(SPI_IOC_MAGIC, 4, ctypes.c_uint32)
SPI_IOC_WR_MAX_SPEED_HZ = _IOW(SPI_IOC_MAGIC, 4, ctypes.c_uint32)


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
