#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.bus.i2c
:brief: I2C bus controller
:author: fred.chen
:date: 2019/6/24
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyraspi.raspi import Raspi
from threading import Lock
from pylibrary.tools.threadutils import synchronized


if Raspi.is_host_raspberry_pi():
    from smbus2 import SMBus
# end if

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
I2C_LOCK = Lock()


class I2C:
    """
    I2C Bus Class
    """

    _instance = None

    @staticmethod
    @synchronized(I2C_LOCK)
    def get_instance():
        """
        Get I2C instance. Shall not create I2C object by different way.

        :return: An instance of I2C controller
        :rtype: ``I2C``
        """
        if I2C._instance is None:
            I2C()
        # end if
        return I2C._instance
    # end def get_instance

    def __init__(self):
        """
        :raise ``AssertionError``: An I2C instance was already instantiated
        """
        assert I2C._instance is None, 'Allowed one I2C instance only!'

        if Raspi.is_host_raspberry_pi():
            self._bus = SMBus(1)
            I2C._instance = self
        # end if
    # end def __init__

    def __del__(self):
        """
        Close I2C bus
        """
        if self._instance is not None:
            if self._bus is not None:
                self._bus.close()
            # end if
            self._instance = None
        # end if
    # end def __del__

    @synchronized(I2C_LOCK)
    def read_i2c_block_data(self, i2c_addr, register, length, force=None):
        """
        Read a block of byte data from a given register.

        :param i2c_addr: I2c address
        :type i2c_addr: ``int``
        :param register: Start register
        :type register: ``int``
        :param length: Desired block length
        :type length: ``int``
        :param force: Force update, defaults to None - OPTIONAL
        :type force: ``bool``

        :return: List of bytes
        :rtype: ``list``
        """
        return self._bus.read_i2c_block_data(i2c_addr, register, length, force)
    # end def read_i2c_block_data

    @synchronized(I2C_LOCK)
    def write_i2c_block_data(self, i2c_addr, register, data, force=None):
        """
        Write a block of byte data to a given register.

        :param i2c_addr: I2c address
        :type i2c_addr: ``int``
        :param register: Start register
        :type register: ``int``
        :param data: List of bytes
        :type data: ``list``
        :param force: Force update, defaults to None - OPTIONAL
        :type force: ``bool``
        """
        self._bus.write_i2c_block_data(i2c_addr, register, data, force)
    # end def write_i2c_block_data

# end class I2C

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
