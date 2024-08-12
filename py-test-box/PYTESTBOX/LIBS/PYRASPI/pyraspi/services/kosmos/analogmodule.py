#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.analogmodule
:brief: Kosmos Analog Module Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2021/11/25
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import sleep

from pylibrary.emulator.emulatorinterfaces import PowerSupplyEmulationInterface
from pyraspi.services.daemon import Daemon
from pyraspi.services.kosmos.module.cmods6 import Cmods6
from pyraspi.services.kosmos.module.dac import Dac


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class AnalogModule(PowerSupplyEmulationInterface):
    """
    Kosmos power supply emulation.
    """

    VOLTAGE_LIMIT = {
        Cmods6.CHANNEL.BATTERY: 4.5,  # Volts
        Cmods6.CHANNEL.USB: 5.2,  # Volts
    }

    # Channel(s) under control
    CHANNELS = Cmods6.ALL_CHANNELS  # FIXME: this should be set to Cmods6.CHANNEL.BATTERY

    def __init__(self, kosmos):
        """
        :param kosmos: an instance of a Kosmos class
        :type kosmos: ``Kosmos``

        :raise ``AssertionError``: Attempt to instantiate this class on a non-Kosmos hardware
        """
        assert Daemon.is_host_kosmos(), 'This class supports only Kosmos hardware'

        self._cmods6_manager = kosmos.cmods6
        self._cmods6_manager.set_max_voltage_limit(channels=Cmods6.CHANNEL.BATTERY,
                                                   voltage=self.VOLTAGE_LIMIT[Cmods6.CHANNEL.BATTERY])
        self._cmods6_manager.set_max_voltage_limit(channels=Cmods6.CHANNEL.USB,
                                                   voltage=self.VOLTAGE_LIMIT[Cmods6.CHANNEL.USB])

        self._output_voltage = 0
        self._output_enabled = False

        self.reset()
        self.init()
    # end def __init__

    def reset(self):
        """
        Reset all four DAC channels + Reset relays
        """
        cmods6 = Cmods6()
        cmods6.enable_output_voltage(channels=self.CHANNELS, enable=False)
        cmods6.reset_dac(channels=self.CHANNELS)
        self._cmods6_manager.send(cmods6)
        self._output_enabled = False
        sleep(0.1)
    # end def reset

    def init(self):
        """
        Initialize DAC:
         - Reset channel A (Output Voltage)
         - Set channel B (Sink Current)
         - Set channel C (Source Current)
        """
        cmods6 = Cmods6()
        cmods6.set_sink_current(channels=self.CHANNELS, current=Dac.MAX_VOLTAGE)
        cmods6.set_source_current(channels=self.CHANNELS, current=Dac.MAX_VOLTAGE)
        cmods6.set_output_voltage(channels=self.CHANNELS, voltage=0)
        self._cmods6_manager.send(cmods6)
        sleep(0.1)
    # end def init

    def turn_on(self):
        # See ``PowerSupplyEmulationInterface.turn_on``
        self.output_enabled = True
    # end def turn_on

    def turn_off(self):
        # See ``PowerSupplyEmulationInterface.turn_off``
        self.output_enabled = False
    # end def turn_off

    @property
    def output_enabled(self):
        """
        Return state of the voltage output.

        :return: output state: True if output is connected, False if disconnected
        :rtype: ``bool``
        """
        return self._output_enabled
    # end def output_enabled

    @output_enabled.setter
    def output_enabled(self, state):
        """
        Set voltage output state: connected or disconnected.

        :param state: output state: set True to connect output, False to disconnected
        :type state: ``bool``
        """
        cmods6 = Cmods6()
        cmods6.enable_output_voltage(channels=self.CHANNELS, enable=state)
        self._cmods6_manager.send(cmods6)
        self._output_enabled = state
        sleep(0.1)
    # end def property setter output_enabled

    def set_voltage(self, voltage, fast_ramp=False):
        # See ``PowerSupplyEmulationInterface.set_voltage``
        cmods6 = Cmods6()
        cmods6.set_output_voltage(channels=self.CHANNELS, voltage=voltage)
        self._cmods6_manager.send(cmods6)
        self._output_voltage = voltage
        sleep(0.1)
    # end def set_voltage

    def configure_measurement_mode(self, mode="tension"):
        # See ``PowerSupplyEmulationInterface.configure_measurement_mode``
        raise NotImplementedError('The method `configure_measurement_mode` cannot be implemented for this class.')
    # end def configure_measurement_mode

    def get_voltage(self):
        # See ``PowerSupplyEmulationInterface.get_voltage``
        return self._output_voltage
    # end def get_voltage

    def get_current(self):
        # See ``PowerSupplyEmulationInterface.get_current``
        raise NotImplementedError('The method `get_current` is not yet implemented for this class, '
                                  'as FPGA design is not ready.')
    # end def get_current

    def restart_device(self, starting_voltage=None):
        # See ``PowerSupplyEmulationInterface.restart_device``
        self.turn_off()
        if starting_voltage is not None:
            self.set_voltage(starting_voltage)
        # end if
        sleep(0.5)  # second
        self.turn_on()
        sleep(0.5)  # second
    # end def restart_device

    def recharge(self, enable):
        """
        Set recharge mode to enable or disable (enable/disable current sink capabilities).

        See ``PowerSupplyEmulationInterface.recharge``

        :param enable: enable or disable the recharge mode
        :type enable: ``bool``
        """
        if enable:
            cmods6 = Cmods6()
            cmods6.set_current_sink_channel(channel=Cmods6.CHANNEL.BATTERY)
            self._cmods6_manager.send(cmods6)
            sleep(0.1)  # second
        # end if

        cmods6 = Cmods6()
        cmods6.enable_current_sink(enable=enable)
        self._cmods6_manager.send(cmods6)
        sleep(0.1)  # second
    # end def recharge
# end class AnalogModule

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
