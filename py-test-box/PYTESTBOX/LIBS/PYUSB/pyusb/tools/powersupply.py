#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pylibrary.emulator.powersupply
:brief:   Agilent and MCP4725 power supply implementation.
:author:  christophe roquebert
:date:    2019/07/09
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.emulator.emulatorinterfaces import PowerSupplyEmulationInterface
from pyraspi.services.powersupply import MILLI_FACTOR
from pytransport.tools.agilent import Agilent
from time import sleep


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class AgilentPowerSupplyEmulationInterface(PowerSupplyEmulationInterface):
    """
    Interface for power supply emulation.
    """

    def __init__(self, test_features):
        """
        Emulate a turn on of the device.
        """
        self.features = test_features
    # end __init__

    def turn_on(self):
        """
        Emulate a turn on of the device.
        """
        agilent = Agilent.get_instance()
        assert(agilent is not None)
        agilent.output_voltage('on')
    # end turn_on

    def turn_off(self):
        """
        Emulate a turn off of the device.
        """
        agilent = Agilent.get_instance()
        assert(agilent is not None)
        agilent.output_voltage('off')
    # end turn_off

    def set_voltage(self, voltage, fast_ramp=True):
        """
        Set the battery to a certain level.
        """
        agilent = Agilent.get_instance()
        assert(agilent is not None)
        voltage_value = agilent.set_voltage(voltage)
        assert(voltage == voltage_value)
        sleep(2)
    # end set_voltage

    def configure_measurement_mode(self, mode="tension"):
        """
        Do nothing.
        """
        pass
    # end configure_measurement_mode

    def get_voltage(self):
        """
        Get the battery level.
        """
        agilent = Agilent.get_instance()
        assert(agilent is not None)
        voltage_value = agilent.read_voltage()
        return voltage_value
    # end get_voltage

    def get_current(self):
        """
        Get the actual current consumption.
        """
        agilent = Agilent.get_instance()
        assert(agilent is not None)
        current_value = agilent.read_current() * MILLI_FACTOR
        assert(current_value is not None)
        return current_value
    # end get_current

    def restart_device(self, starting_voltage=None):
        """
        Turn off the power on the Device under test,
        then set voltage the nominal value
        finally turn on the power.

        :param starting_voltage: The voltage to use after restart, if None the Nominal value will be used
        :type starting_voltage: ``float``
        """
        self.turn_off()
        sleep(.5)
        if starting_voltage is None:
            voltage = self.features.PRODUCT.DEVICE.BATTERY.F_NominalVoltage
        else:
            voltage = starting_voltage
        # end if

        self.set_voltage(voltage)
        self.turn_on()
        sleep(1)
    # end restart_device

    def recharge(self, enable):
        """
        Set recharge enable or disable

        :param enable: enable or disable the function
        :type enable: ``bool``
        """
        raise NotImplementedError('The function recharge is not implemented on Agilent')
    # end def recharge
# end class AgilentPowerSupplyEmulationInterface


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
