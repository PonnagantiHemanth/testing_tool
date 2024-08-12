#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package:   pyraspi.services.ina226
:brief:     Raspi INA226 Control Class
            System Setup Reference: https://spaces.logitech.com/display/ptb/INA226
:author:    fred.chen
date:       2019/6/19
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyraspi.bus.i2c import I2C
from ctypes import c_int16
from math import ceil
from threading import Lock
from pylibrary.tools.threadutils import synchronized
from pylibrary.tools.tracebacklog import TracebackLogWrapper

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
INA226_ADDRESS              =(0x40)

INA226_REG_CONFIG           =(0x00)
INA226_REG_SHUNTVOLTAGE     =(0x01)
INA226_REG_BUSVOLTAGE       =(0x02)
INA226_REG_POWER            =(0x03)
INA226_REG_CURRENT          =(0x04)
INA226_REG_CALIBRATION      =(0x05)
INA226_REG_MASKENABLE       =(0x06)
INA226_REG_ALERTLIMIT       =(0x07)
INA226_REG_MANUFACTURERID   =(0xFE)
INA226_REG_DIEID            =(0xFF)

INA226_BIT_SOL              =(0x8000)
INA226_BIT_SUL              =(0x4000)
INA226_BIT_BOL              =(0x2000)
INA226_BIT_BUL              =(0x1000)
INA226_BIT_POL              =(0x0800)
INA226_BIT_CNVR             =(0x0400)
INA226_BIT_AFF              =(0x0010)
INA226_BIT_CVRF             =(0x0008)
INA226_BIT_OVF              =(0x0004)
INA226_BIT_APOL             =(0x0002)
INA226_BIT_LEN              =(0x0001)

ina226_averages_t = dict(
    INA226_AVERAGES_1             = 0b000,
    INA226_AVERAGES_4             = 0b001,
    INA226_AVERAGES_16            = 0b010,
    INA226_AVERAGES_64            = 0b011,
    INA226_AVERAGES_128           = 0b100,
    INA226_AVERAGES_256           = 0b101,
    INA226_AVERAGES_512           = 0b110,
    INA226_AVERAGES_1024          = 0b111)

ina226_busConvTime_t = dict(
    INA226_BUS_CONV_TIME_140US    = 0b000,
    INA226_BUS_CONV_TIME_204US    = 0b001,
    INA226_BUS_CONV_TIME_332US    = 0b010,
    INA226_BUS_CONV_TIME_588US    = 0b011,
    INA226_BUS_CONV_TIME_1100US   = 0b100,
    INA226_BUS_CONV_TIME_2116US   = 0b101,
    INA226_BUS_CONV_TIME_4156US   = 0b110,
    INA226_BUS_CONV_TIME_8244US   = 0b111)

ina226_shuntConvTime_t = dict(
    INA226_SHUNT_CONV_TIME_140US   = 0b000,
    INA226_SHUNT_CONV_TIME_204US   = 0b001,
    INA226_SHUNT_CONV_TIME_332US   = 0b010,
    INA226_SHUNT_CONV_TIME_588US   = 0b011,
    INA226_SHUNT_CONV_TIME_1100US  = 0b100,
    INA226_SHUNT_CONV_TIME_2116US  = 0b101,
    INA226_SHUNT_CONV_TIME_4156US  = 0b110,
    INA226_SHUNT_CONV_TIME_8244US  = 0b111)

ina226_mode_t = dict(
    INA226_MODE_POWER_DOWN      = 0b000,
    INA226_MODE_SHUNT_TRIG      = 0b001,
    INA226_MODE_BUS_TRIG        = 0b010,
    INA226_MODE_SHUNT_BUS_TRIG  = 0b011,
    INA226_MODE_ADC_OFF         = 0b100,
    INA226_MODE_SHUNT_CONT      = 0b101,
    INA226_MODE_BUS_CONT        = 0b110,
    INA226_MODE_SHUNT_BUS_CONT  = 0b111)

INA226_LOCK = Lock()

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class INA226:
    """
    INA226 Control Class
    """

    _instance = None

    @staticmethod
    @synchronized(INA226_LOCK)
    def get_instance():
        """
        Get INA226 instance. Shall not create INA226 object by different way.

        :return: An instance of I2C controller
        :rtype: ``INA226``
        """
        if INA226._instance is None:
            INA226()
        # end if
        return INA226._instance
    # end def get_instance

    @classmethod
    def discover(cls):
        """
        Has a quick availability check of INA226 functionality

        :return: INA226 is available or not
        :rtype: ``bool``
        """
        ina226 = INA226.get_instance()
        if ina226 is None:
            return False
        else:
            if ina226.get_mode() is None:
                return False
            else:
                return True
            # end if
        # end if
    # end def discover

    def __init__(self, ina226_addr=INA226_ADDRESS):
        """
        :param ina226_addr: I2C address of INA226, defaults to `INA226_ADDRESS` - OPTIONAL
        :type ina226_addr: ``int``

        :raise ``AssertionError``: Another INA226 instance was already created
        """
        assert INA226._instance is None, 'Allowed one INA226 instance only!'

        # Get I2C instances and apply default settings.
        # noinspection PyBroadException
        try:
            self.i2c_bus = I2C.get_instance()
            self._address = ina226_addr
            self.vBusMax = 36
            self.vShuntMax = 0.08192
            self.rShunt = 0.1
            self.currentLSB = 0
            self.powerLSB = 0
            self.iMaxPossible = 0
            INA226._instance = self
        except:
            exception_stack = TracebackLogWrapper.get_exception_stack()
            print(exception_stack)
        # end try
    # end def __init__

    def read_register16(self, register):
        """
        Read a word data from INA226 register

        :param register: Register address
        :type register: ``int``

        :return: Value in register
        :rtype: ``int``
        """
        # higher_byte = self.i2c_bus.read_byte_data(self.ina226_address,register)
        # lower_byte = self.i2c_bus.read_byte_data(self.ina226_address,register+1)
        data = self.i2c_bus.read_i2c_block_data(self._address, register, 2)
        higher_byte = data[0]
        lower_byte = data[1]
        # there is still some issue in read which we need to fix, we are not able to print negative
        # current--done--fixed using ctypes int16 return
        word_data = higher_byte << 8 | lower_byte
        # return word_data
        return c_int16(word_data).value
    # end def read_register16

    def write_register16(self, register, data_word):
        """
        Write a word data to INA226 register

        :param register: Register address
        :type register: ``int``
        :param data_word: Data to the register
        :type data_word: ``int``
        """
        higher_byte = (data_word >> 8) & 0xff
        lower_byte = data_word & 0xff  # truncating the data_word to byte
        self.i2c_bus.write_i2c_block_data(self._address, register, [higher_byte, lower_byte])
    # end def write_register16

    def configure(self,
                  avg=ina226_averages_t['INA226_AVERAGES_1'],
                  busConvTime=ina226_busConvTime_t['INA226_BUS_CONV_TIME_1100US'],
                  shuntConvTime=ina226_shuntConvTime_t['INA226_SHUNT_CONV_TIME_1100US'],
                  mode=ina226_mode_t['INA226_MODE_SHUNT_BUS_CONT']):
        """
        INA226 configuration

        :param avg: Number of samples to average, defaults to ``ina226_averages_t['INA226_AVERAGES_1']`` - OPTIONAL
        :type avg: ``int``
        :param busConvTime: Bus conversion time,
                            defaults to ``ina226_busConvTime_t['INA226_BUS_CONV_TIME_1100US']`` - OPTIONAL
        :type busConvTime: ``int``
        :param shuntConvTime: Shunt conversion time,
                              defaults to ``ina226_shuntConvTime_t['INA226_SHUNT_CONV_TIME_1100US']`` - OPTIONAL
        :type shuntConvTime: ``int``
        :param mode: Ina226 mode, defaults to ``ina226_mode_t['INA226_MODE_SHUNT_BUS_CONT']`` - OPTIONAL
        :type mode: ``int``
        """
        config = 0
        config |= (avg << 9 | busConvTime << 6 | shuntConvTime << 3 | mode)
        self.write_register16(INA226_REG_CONFIG, config)
    # end def configure

    def calibrate(self, rShuntValue=0.1, iMaxExcepted=2.0):
        """
        Calibrate INA226 by Rshunt and max possible current

        :param rShuntValue: Set Rshunt value, defaults to 0.1 - OPTIONAL
        :type rShuntValue: ``float``
        :param iMaxExcepted: Set max possible current, defaults to 2.0 - OPTIONAL
        :type iMaxExcepted: ``float``
        """
        self.rShunt = rShuntValue

        self.iMaxPossible = self.vShuntMax / self.rShunt

        minimumLSB = iMaxExcepted / 32767

        self.currentLSB = int((minimumLSB * 100000000))
        # print("currentLSB:" + str(self.currentLSB))
        self.currentLSB /= 100000000.0
        self.currentLSB /= 0.000001
        self.currentLSB = ceil(self.currentLSB)
        self.currentLSB *= 0.000001

        self.powerLSB = self.currentLSB * 25

        # if we get error need to convert this to unsigned int 16 bit instead
        calibrationValue = int(((0.00512) / (self.currentLSB * self.rShunt)))

        self.write_register16(INA226_REG_CALIBRATION, calibrationValue)
    # end def calibrate

    def get_averages(self):
        """
        Get config of average count

        :return: Average count
        :rtype: ``byte``
        """
        value = self.read_register16(INA226_REG_CONFIG)
        value &= 0b0000111000000000
        value >>= 9
        return value
    # end def get_averages

    def get_max_possible_current(self):
        """
        Get max possible current

        :return: Max possible current
        :rtype: ``float``
        """
        return (self.vShuntMax / self.rShunt)
    # end def get_max_possible_current

    def get_max_current(self):
        """
        Get max current

        :return: Max current
        :rtype: ``float``
        """
        maxCurrent = (self.currentLSB * 32767)
        maxPossible = self.get_max_possible_current()

        if maxCurrent > maxPossible:
            return maxPossible
        else:
            return maxCurrent
        # end if
    # end def get_max_current

    def get_max_shunt_voltage(self):
        """
        Get max Vshunt voltage

        :return: Max Vshunt
        :rtype: ``float``
        """
        maxVoltage = self.get_max_current() * self.rShunt
        if maxVoltage >= self.vShuntMax:
            return self.vShuntMax
        else:
            return maxVoltage
        # end if
    # end def get_max_shunt_voltage

    def get_max_power(self):
        """
        Get max power

        :return: Max power
        :rtype: ``float``
        """
        return self.get_max_current() * self.vBusMax
    # end def get_max_power

    def read_bus_power(self):
        """
        Read bus power

        :return: Bus power
        :rtype: ``float``
        """
        return self.read_register16(INA226_REG_POWER) * self.powerLSB
    # end def read_bus_power

    def read_shunt_current(self):
        """
        Read current

        :return: Current
        :rtype: ``float``
        """
        return self.read_register16(INA226_REG_CURRENT) * self.currentLSB
    # end def read_shunt_current

    def read_shunt_voltage(self):
        """
        Read voltage

        :return: Voltage
        :rtype: ``float``
        """
        voltage = self.read_register16(INA226_REG_SHUNTVOLTAGE)
        return voltage * 0.0000025
    # end def read_shunt_voltage

    def read_bus_voltage(self):
        """
        Read bus voltage

        :return: Voltage
        :rtype: ``float``
        """
        voltage = self.read_register16(INA226_REG_BUSVOLTAGE)
        return voltage * 0.00125
    # end def read_bus_voltage

    def get_bus_conversion_time(self):
        """
        Get bus conversion time

        :return: Conversion time
        :rtype: ``int``
        """
        value = self.read_register16(INA226_REG_CONFIG)
        value &= 0b0000000111000000
        value >>= 6
        return value
    # end def get_bus_conversion_time

    def get_shunt_conversion_time(self):
        """
        Get shunt conversion time

        :return: Conversion time
        :rtype: ``int``
        """
        value = self.read_register16(INA226_REG_CONFIG)
        value &= 0b0000000000111000
        value >>= 3
        return value
    # end def get_shunt_conversion_time

    def get_mode(self):
        """
        Get INA226 mode

        :return: Mode
        :rtype: ``int``
        """
        value = None
        try:
            value = self.read_register16(INA226_REG_CONFIG)
            value &= 0b0000000000000111
        except:
            pass
        # end try
        return value
    # end def get_mode

    def get_manufacturer_id(self):
        """
        Read Manufacturer ID

        :return: Manufacturer ID: 0x5449
        :rtype: ``int``
        """
        return self.read_register16(INA226_REG_MANUFACTURERID)
    # end def get_manufacturer_id

    def get_die_id(self):
        """
        Read Die ID

        :return: Die ID: 0x2260
        :rtype: ``int``
        """
        return self.read_register16(INA226_REG_DIEID)
    # end def get_die_id

    def set_mask_enable(self, mask):
        """
        Set the alerts enable/disable

        :param mask: Mask of alert options
        :type mask: ``int``
        """
        self.write_register16(INA226_REG_MASKENABLE, mask)
    # end def set_mask_enable

    def get_mask_enable(self):
        """
        Get the alerts settings

        :return: Mask of alert options
        :rtype: ``int``
        """
        return self.read_register16(INA226_REG_MASKENABLE)
    # end def get_mask_enable

    def enable_shunt_over_limit_alert(self):
        """
        Enable shunt over limit alert
        """
        self.write_register16(INA226_REG_MASKENABLE, INA226_BIT_SOL)
    # end def enable_shunt_over_limit_alert

    def enable_bus_over_limit_alert(self):
        """
        Enable bus over limit alert
        """
        self.write_register16(INA226_REG_MASKENABLE, INA226_BIT_BOL)
    # end def enable_bus_over_limit_alert

    def enable_bus_under_limit_alert(self):
        """
        Enable bus under limit alert
        """
        self.write_register16(INA226_REG_MASKENABLE, INA226_BIT_BUL)
    # end def enable_bus_under_limit_alert

    def enable_over_power_limit_alert(self):
        """
        Enable over power limit alert
        """
        self.write_register16(INA226_REG_MASKENABLE, INA226_BIT_POL)
    # end def enable_over_power_limit_alert

    def enable_conversion_ready_alert(self):
        """
        Enable conversion ready alert
        """
        self.write_register16(INA226_REG_MASKENABLE, INA226_BIT_CNVR)
    # end def enable_conversion_ready_alert

    def set_bus_voltage_limit(self, voltage):
        """
        Set bus voltage limit

        :param voltage: Bus voltage limit
        :type voltage: ``float``
        """
        value = voltage / 0.00125
        self.write_register16(INA226_REG_ALERTLIMIT, value)
    # end def set_bus_voltage_limit

    def set_shunt_voltage_limit(self, voltage):
        """
        Set shunt voltage limit

        :param voltage: Shunt voltage limit
        :type voltage: ``float``
        """
        value = voltage * 25000
        self.write_register16(INA226_REG_ALERTLIMIT, value)
    # end def set_shunt_voltage_limit

    def set_power_limit(self, watts):
        """
        Set power limit

        :param watts: Power limit
        :type watts: ``float``
        """
        value = watts / self.powerLSB
        self.write_register16(INA226_REG_ALERTLIMIT, value)
    # end def set_power_limit

    def set_alert_inverted_polarity(self, inverted):
        """
        Set alert inverted polarity

        :param inverted: Inverted or not
        :type inverted: ``bool``
        """
        temp = self.get_mask_enable()

        if inverted:
            temp |= INA226_BIT_APOL
        else:
            temp &= ~INA226_BIT_APOL
        # end if
        self.set_mask_enable(temp)
    # end def set_alert_inverted_polarity

    def set_alert_latch(self, latch):
        """
        Set alert latch

        :param latch: Latch or not
        :type latch: ``bool``
        """
        temp = self.get_mask_enable()
        if latch:
            temp |= INA226_BIT_LEN
        else:
            temp &= ~INA226_BIT_LEN
        # end if
        self.set_mask_enable(temp)
    # end def set_alert_latch

    def is_math_overflow(self):
        """
        Check there is a math overflow or not

        :return: Overflow or not
        :rtype: ``bool``
        """
        return (self.get_mask_enable() & INA226_BIT_OVF) == INA226_BIT_OVF
    # end def is_math_overflow

    def is_alert(self):
        """
        Check there is in alert or not

        :return: In alert or not
        :rtype: ``bool``
        """
        return (self.get_mask_enable() & INA226_BIT_AFF) == INA226_BIT_AFF
    # end def is_alert

# end class INA226

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
