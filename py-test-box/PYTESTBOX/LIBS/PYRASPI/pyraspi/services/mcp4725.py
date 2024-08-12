#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package:   pyraspi.services.mcp4725
:brief:     CircuitPython module for the MCP4725 digital to analog converter.
            See examples/mcp4725_simpletest.py for a demo of the usage.
:author:    Tony DiCola
            Fred Chen
:date:      2019/07/22
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import sys
from threading import Lock
from warnings import warn

from pylibrary.tools.threadutils import synchronized
from pyraspi.bus.i2c import I2C
from pyraspi.services.daemon import Daemon

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MCP4725.git"


# Internal constants:
_MCP4725_DEFAULT_ADDRESS = 0b01100000   # 0x60
_MCP4725_WRITE_FAST_MODE = 0b00000000

MCP4725_LOCK = Lock()


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class MCP4725:
    """
    MCP4725 12-bit digital to analog converter.  This class has a similar
    interface as the CircuitPython AnalogOut class and can be used in place
    of that module.

    This device doesn't use registers and instead just accepts a single
    command string over I2C.  As a result we don't use bus device or
    other abstractions and just talk raw I2C protocol.
    """
    _instance = None

    @classmethod
    def discover(cls):
        """
        Has a quick availability check of MCP4725

        :return: MCP4725 is available or not
        :rtype: ``bool``
        """
        if sys.platform != 'linux':
            return False
        elif Daemon.is_host_kosmos():
            return False
        # end if
        mcp4725 = MCP4725.get_instance()
        if mcp4725 is None:
            return False
        else:
            if mcp4725.value is None:
                return False
            else:
                return True
            # end if
        # end if
    # end def discover

    @staticmethod
    @synchronized(MCP4725_LOCK)
    def get_instance(address=_MCP4725_DEFAULT_ADDRESS):
        """
        Get MCP4725 instance. Shall not create MCP4725 object by different way.

        :param address: MCP4725 I2C address, defaults to ``_MCP4725_DEFAULT_ADDRESS`` - OPTIONAL
        :type address: ``int``

        :return: An instance of MCP4725
        :rtype: ``MCP4725``
        """
        if MCP4725._instance is None:
            MCP4725(address)

            if MCP4725._instance is None:
                warn('Cannot communicate with MCP4725 by I2C! Please check power source and I2C connection.')
            # end if
        # end if

        return MCP4725._instance
    # end def get_instance

    def __init__(self, address=_MCP4725_DEFAULT_ADDRESS):
        """
        :param address: MCP4725 I2C address, defaults to ``_MCP4725_DEFAULT_ADDRESS`` - OPTIONAL
        :type address: ``int``

        :raise ``AssertionError``: If another MCP4725 instance is already initialized.
        """
        assert MCP4725._instance is None, 'Allowed a single MCP4725 instance only!'
        self._i2c = I2C.get_instance()
        if self._i2c is not None:
            self._address = address
            self._buffer = bytearray(3)
            MCP4725._instance = self
        # end if
    # end def __init__

    def __del__(self):
        if MCP4725._instance is not None:
            MCP4725._instance = None
        # end if
    # end def __del__

    def _write_fast_mode(self, val=None):
        """
        Perform a 'fast mode' write to update the DAC value.
        Will not enter power down, update EEPROM, or any other state beyond
        the 12-bit DAC value.

        :param val: data, defaults to None - OPTIONAL
        :type val: ``int``

        :raise ``AssertionError``: Out of range `val` value
        """
        assert 0 <= val <= 4095, f"Cannot use the value {val}"
        val &= 0xFFF
        data = bytearray(1)
        data[0] = val & 0xFF

        # 3 bytes write fast mode
        self._i2c.write_i2c_block_data(self._address, val >> 8, data)
    # end def _write_fast_mode

    def _read(self):
        """
        Perform a read of the DAC value.  Returns the 12-bit value.
        Read 3 bytes from device.

        :return: Data from DAC
        :rtype: ``int``
        """

        self._buffer = self._i2c.read_i2c_block_data(self._address, 0, 3)
        # Grab the DAC value from last two bytes.
        dac_high = self._buffer[1]
        dac_low = self._buffer[2] >> 4
        # Reconstruct 12-bit value and return it.
        return ((dac_high << 4) | dac_low) & 0xFFF
    # end def _read

    @property
    def value(self):
        """
        The DAC value as a 16-bit unsigned value compatible with the `~analogio.AnalogOut` class.

        Note that the MCP4725 is still just a 12-bit device so quantization will occur.  If you'd
        like to instead deal with the raw 12-bit value use the ``raw_value`` property, or the
        ``normalized_value`` property to deal with a 0...1 float value.

        :return: The DAC value
        :rtype: ``int``
        """
        result = None
        try:
            raw_value = self._read()
            # Scale up to 16-bit range.
            result = raw_value << 4
        except:
            pass
        # end try
        return result
    # end def property getter value

    @value.setter
    def value(self, val):
        """
        Set 16 bits value to 12 bits MCP4725 raw value

        :param val: Value in range 0 to 65535
        :type val: ``int``

        :raise ``AssertionError``: Out of range `val` value
        """
        assert 0 <= val <= 65535
        # Scale from 16-bit to 12-bit value (quantization errors will occur!).
        raw_value = val >> 4
        self._write_fast_mode(val=raw_value)
    # end def property setter value

    @property
    def raw_value(self):
        """
        The DAC value as a 12-bit unsigned value.  This is the true resolution of the DAC
        and will never perform scaling or run into quantization error.

        :return: RAW DAC value
        :rtype: ``int``
        """
        return self._read()
    # end def property getter raw_value

    @raw_value.setter
    def raw_value(self, val):
        """
        Set raw value to MCP4725

        :param val: Value from 0 to 4095
        :type val: ``int``
        """
        self._write_fast_mode(val=val)
    # end def property setter raw_value

    @property
    def normalized_value(self):
        """
        The DAC value as a floating point number in the range 0.0 to 1.0.

        :return: the normalized raw value
        :rtype: ``float``
        """
        return self._read()/4095.0
    # end def property getter normalized_value

    @normalized_value.setter
    def normalized_value(self, val):
        """
        Set normalized value to MCP4725 raw value

        :param val: The voltage percentage
        :type val: ``float``

        :raise ``AssertionError``: Out of range `val` value
        """
        assert 0.0 <= val <= 1.0
        raw_value = int(val * 4095.0)
        self._write_fast_mode(val=raw_value)
    # end def property setter normalized_value
# end class MCP4725

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
