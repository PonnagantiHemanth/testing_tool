#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: pyraspi.bus.spidev.asm_generic_ioctl
:brief: Python portage of <asm-generic/ioctl.h>
:author: Thomas Preston <tompreston@monzo.com>; Lila Viollette <lviollette@logitech.com>
:date: 2021/04/12
:source: https://github.com/microstack-IoT/python3-microstackcommon/blob/master/microstackcommon/asm_generic_ioctl.py

Converted from <asm-generic/ioctl.h>

ioctl command encoding: 32 bits total, command in lower 16 bits,
size of the parameter structure in the lower 14 bits of the
upper 16 bits.

Encoding the size of the parameter structure in the ioctl request
is useful for catching programs compiled with old versions
and to avoid overwriting user space outside the user buffer area.
The highest 2 bits are reserved for indicating the ``access mode''.

NOTE: This limits the max parameter size to 16kB -1 !
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import ctypes


# ------------------------------------------------------------------------------
# constants and macros (as Python methods)
# ------------------------------------------------------------------------------
"""
The following is for compatibility across the various Linux
platforms.  The generic ioctl numbering scheme doesn't really enforce
a type field.  De facto, however, the top 8 bits of the lower 16
bits are indeed used as a type field, so we might just as well make
this explicit here.  Please be sure to use the decoding macros
below from now on.

:ivar _IOC_NRBITS    :
:ivar _IOC_TYPEBITS  :
:ivar _IOC_SIZEBITS  :
:ivar _IOC_DIRBITS   :
:ivar _IOC_NRMASK    :
:ivar _IOC_SIZEMASK  :
:ivar _IOC_DIRMASK   :
:ivar _IOC_NRSHIFT   :
:ivar _IOC_TYPESHIFT :
:ivar _IOC_TYPESHIFT :
:ivar _IOC_SIZESHIFT :
:ivar _IOC_DIRSHIFT  :
"""
_IOC_NRBITS = 8
_IOC_TYPEBITS = 8

_IOC_SIZEBITS = 14
_IOC_DIRBITS = 2

_IOC_NRMASK = (1 << _IOC_NRBITS) - 1
_IOC_TYPEMASK = (1 << _IOC_TYPEBITS) - 1
_IOC_SIZEMASK = (1 << _IOC_SIZEBITS) - 1
_IOC_DIRMASK = (1 << _IOC_DIRBITS) - 1

_IOC_NRSHIFT = 0
_IOC_TYPESHIFT = _IOC_NRSHIFT + _IOC_NRBITS
_IOC_SIZESHIFT = _IOC_TYPESHIFT + _IOC_TYPEBITS
_IOC_DIRSHIFT = _IOC_SIZESHIFT + _IOC_SIZEBITS


"""
Direction bits

:ivar _IOC_NONE  :
:ivar _IOC_WRITE : means userland is writing and kernel is reading.
:ivar _IOC_READ  : means userland is reading and kernel is writing.
"""
_IOC_NONE = 0
_IOC_WRITE = 1
_IOC_READ = 2


def _IOC(dir, type, nr, size):
    """
    Return formated IOCTL command.

    :param dir: IOCTL command Direction
    :type dir: ``int``
    :param type: IOCTL command Type
    :type type: ``int``
    :param nr: IOCTL command Number
    :type nr: ``int``
    :param size: IOCTL command data Size
    :type size: ``int``

    :return: formated IOCTL command
    :rtype: ``int``
    """
    return (dir << _IOC_DIRSHIFT) | \
        (type << _IOC_TYPESHIFT) | \
        (nr << _IOC_NRSHIFT) | \
        (size << _IOC_SIZESHIFT)
# end def _IOC


def _IOC_TYPECHECK(t):
    """
    Return the byte size of the given ctype value.

    :param t: ctype value
    :type t: ``int``

    :return: byte size of the given ctype value
    :rtype: ``int``
    """
    return ctypes.sizeof(t)
# end def _IOC_TYPECHECK


"""
Used to create ioctl numbers
 NOTE:
   ``_IOW`` means userland is writing and kernel is reading.
   ``_IOR`` means userland is reading and kernel is writing.
"""


def _IO(type, nr):
    """
    Return formated IOCTL command.

    :param type: IOCTL command Type
    :type type: ``int``
    :param nr: IOCTL command number
    :type nr: ``int``

    :return: formated IOCTL command
    :rtype: ``int``
    """
    return _IOC(_IOC_NONE, type, nr, 0)
# end def _IO


def _IOR(type, nr, size):
    """
    Return formated IOCTL READ command (userland is reading and kernel is writing).

    :param type: IOCTL command Type
    :type type: ``int``
    :param nr: IOCTL command number
    :type nr: ``int``
    :param size: IOCTL command data Size
    :type size: ``int``

    :return: formated IOCTL command
    :rtype: ``int``
    """
    return _IOC(_IOC_READ, type, nr, _IOC_TYPECHECK(size))
# end def _IOR


def _IOW(type, nr, size):
    """
    Return formated IOCTL WRITE command (userland is writing and kernel is reading).

    :param type: IOCTL command Type
    :type type: ``int``
    :param nr: IOCTL command number
    :type nr: ``int``
    :param size: IOCTL command data Size
    :type size: ``int``

    :return: formated IOCTL command
    :rtype: ``int``
    """
    return _IOC(_IOC_WRITE, type, nr, _IOC_TYPECHECK(size))
# end def _IOW


def _IOWR(type, nr, size):
    """
    Return formated IOCTL READ/WRITE command.

    :param type: IOCTL command Type
    :type type: ``int``
    :param nr: IOCTL command number
    :type nr: ``int``
    :param size: IOCTL command data Size
    :type size: ``int``

    :return: formated IOCTL command
    :rtype: ``int``
    """
    return _IOC(_IOC_READ | _IOC_WRITE, type, nr, _IOC_TYPECHECK(size))
# end def _IOWR

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
