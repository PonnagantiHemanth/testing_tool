# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------
"""
:package: ciscripts.power_supply
:brief:   Utility for power supply board rev.2 and later
:author:  Fred Chen <fchen7@logitech.com>
:date:    2019/12/02
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from argparse import ArgumentParser
from io import TextIOBase

from math import ceil
from os import path
from time import sleep
import sys
import warnings


FILE_PATH = path.abspath(__file__)
WS_DIR = FILE_PATH[:FILE_PATH.rfind("CICD")]
PYRASPI_DIR = path.join(WS_DIR, "LIBS", "PYRASPI")
PYLIBRARY_DIR = path.join(WS_DIR, "LIBS", "PYLIBRARY")
PYHID_DIR = path.join(WS_DIR, "LIBS", "PYHID")
PYUSB_DIR = path.join(WS_DIR, "LIBS", "PYUSB")
PYTRANSPORT_DIR = path.join(WS_DIR, "LIBS", "PYTRANSPORT")
LOGIUSB_DIR = path.join(WS_DIR, "LIBS", "PYTRANSPORT", "pytransport", "usb", "logiusbcontext", "logiusb")
PYCHANNEL_DIR = path.join(WS_DIR, "LIBS", "PYCHANNEL")
PYSETUP_DIR = path.join(WS_DIR, "LIBS", "PYSETUP", "PYTHON")
if PYRASPI_DIR not in sys.path:
    sys.path.insert(0, PYRASPI_DIR)
# end if
if PYLIBRARY_DIR not in sys.path:
    sys.path.insert(0, PYLIBRARY_DIR)
# end if
if PYHID_DIR not in sys.path:
    sys.path.insert(0, PYHID_DIR)
# end if
if PYTRANSPORT_DIR not in sys.path:
    sys.path.insert(0, PYTRANSPORT_DIR)
# end if
if LOGIUSB_DIR not in sys.path:
    sys.path.insert(0, LOGIUSB_DIR)
# end if
if PYCHANNEL_DIR not in sys.path:
    sys.path.insert(0, PYCHANNEL_DIR)
# end if
if PYUSB_DIR not in sys.path:
    sys.path.insert(0, PYUSB_DIR)
# end if
if PYSETUP_DIR not in sys.path:
    sys.path.insert(0, PYSETUP_DIR)
# end if
# Exclude PEP8 rule: module level import not at top of file
from pyraspi.services.powersupply import MCP4725PowerSupplyEmulationInterface  # noqa: E402
from pyraspi.services.powersupply import MILLI_FACTOR  # noqa: E402
from pyraspi.services.powersupply import OverVoltageProtection  # noqa: E402
from pyraspi.services.powersupply import PowerSupplyConstant  # noqa: E402
from pyraspi.services.jlinkconnectioncontrol import PowerSupplyBoardJlinkConnectionControl  # noqa: E402
from pyraspi.raspi import Raspi  # noqa: E402
from pyusb.libusbdriver import LibusbDriver  # noqa: E402


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class PowerSupplyUtility(object):
    """
    Control interface of MCP4725 power supply
    """
    VERSION = '0.1.0.0'

    def __init__(self, stdout, stderr):
        """
        Constructor and main program entry point

        :param stdout: The standard output stream
        :type stdout: ``TextIOBase``
        :param stderr: The standard error stream
        :type stderr: ``TextIOBase``
        """
        self._stdout = stdout
        self._stderr = stderr
        self._parser = None
        self.calibration = False
        self.over_voltage_level = None
        self.voltage = None
        self.precise_voltage = None
        self.on = False
        self.off = False
        self.init = False
        self.end = None
        self.duration = None
        self.recharge = None
        self.measure_current = False
        self.measure_voltage = False
        self.switch_state = None
        self.port_5_state = None
        self.set_gpio_to_input = False

        self.parse_args()

        if self.port_5_state is not None or self.end:
            self.power_supply = MCP4725PowerSupplyEmulationInterface.get_instance(starting_voltage=0,
                                                                                  reset_gpio=self.init)
            if self.port_5_state is not None:
                self.set_phidgets_port_5_state(self.port_5_state)
            # end if
        else:
            # Keep previous USB port settings
            self.power_supply = MCP4725PowerSupplyEmulationInterface.get_instance(starting_voltage=0,
                                                                                  reset_gpio=self.init,
                                                                                  discover_usb_hub=False)
        # end if

        if self.power_supply is None:
            # The script shouldn't raise any exceptions on setup without the power board
            warnings.warn(f'Power supply board not found')
            return
        # end if

        if self.set_gpio_to_input:
            self.power_supply.set_gpio_to_input()
        # end if

        if self.switch_state is not None and PowerSupplyBoardJlinkConnectionControl.is_control_pin_connected(
                control_pin=Raspi.PIN.JLINK_IO_SWITCH):
            if self.switch_state:
                PowerSupplyBoardJlinkConnectionControl(Raspi.PIN.JLINK_IO_SWITCH).connect()
            else:
                PowerSupplyBoardJlinkConnectionControl(Raspi.PIN.JLINK_IO_SWITCH).disconnect()
            # end if
        # end if

        if self.calibration:
            self.power_supply.voltage_calibration()
        # end if

        if self.over_voltage_level:
            try:
                self.measure_over_voltage()
            except Exception as e:
                print(f'Error: {e}')
            # end try
        # end if

        if self.voltage is not None:
            self.power_supply.set_raw_voltage(self.voltage)
            # Wait voltage stable
            sleep(.2)
        # end if

        if self.precise_voltage is not None and self.power_supply.set_voltage(self.precise_voltage):
            self.power_supply.update_calibration_file()
        # end if

        if self.duration:
            self.output_by_duration()
        else:
            if self.on:
                self.power_supply.output_on()
            # end if

            if self.off:
                self.power_supply.output_off()
            # end if
        # end if

        if self.recharge is not None:
            self.power_supply.recharge(enable=self.recharge)
        # end if

        if self.measure_current:
            self.print_current()
        # end if

        if self.measure_voltage:
            self.print_voltage()
        # end if

        if self.end:
            self.destroy()
        # end if
    # end def __init__

    def get_parser(self):
        """
        Get the ArgumentParser instance

        :return: ArgumentParser instance
        :rtype: ``ArgumentParser``
        """
        if self._parser is None:
            parser = ArgumentParser()
            parser.add_argument('--version', action='version', version=self.VERSION)
            parser.add_argument('-a', '--measure_current', dest='measure_current', default=False, action='store_true',
                                help='Get current in uA')
            parser.add_argument('-c', '--calibration', dest='calibration', default=False, action='store_true',
                                help='Perform voltage calibration')
            parser.add_argument('-d', '--duration', dest='duration', default=None, metavar='SET_DURATION',
                                help='The duration of turn on to turn off')
            parser.add_argument('-e', '--end', dest='end', default=False, action='store_true', help='End power supply')
            parser.add_argument('-f', '--off', dest='off', default=False, action='store_true',
                                help='Turn off voltage output')
            parser.add_argument('-i', '--init', dest='init', default=False, action='store_true',
                                help='Init power supply')
            parser.add_argument('-m', '--measure-over-voltage', dest='measure_over_voltage', default=None,
                                metavar='MEASURE_OVER_VOLTAGE', help='Measure over voltage level')
            parser.add_argument('-o', '--on', dest='on', default=False, action='store_true',
                                help='Turn on voltage output')
            parser.add_argument('-p', '--port_5_state', dest='port_5_state', default=None, metavar='SET_PORT_5_STATE',
                                help='Set port 5 on/off')
            parser.add_argument('-r', '--recharge', dest='recharge', default=None, metavar='SET_RECHARGE',
                                help='Enable/disable rechargeable feature')
            parser.add_argument('-s', '--switch_state', dest='switch_state', default=None, metavar='SET_SWITCH_STATE',
                                help='Set switch on/off')
            parser.add_argument('-V', '--precise_voltage', dest='precise_voltage', default=None,
                                metavar='SET_PRECISE_VOLTAGE', help='Set precise voltage value')
            parser.add_argument('-v', '--voltage', dest='voltage', default=None, metavar='SET_VOLTAGE',
                                help='Set voltage value')
            parser.add_argument('-z', '--measure_voltage', dest='measure_voltage', default=False, action='store_true',
                                help='Get voltage in V')
            parser.add_argument('-g', '--gpio_to_input', dest='set_gpio_to_input', default=False, action='store_true',
                                help='Set up the GPIOs to input for keyboard and mouse.')
            parser.epilog = """
Examples:
  -i                        # Initialize GPIO setup, without -i the GPIO will keep previous setting
  -e                        # Cleanup GPIO settings. Shall use this command to end up power supply.
  -c                        # Voltage calibration
  -m                        # Over voltage measurement, MUST remove USB charging cable if DUT supported
  -o                        # Keep output on
  -f                        # Keep output off
  -v 3.8                    # Set voltage to 3.8v
  -V 3.8                    # Set voltage to 3.80v in +- 2mV tolerance
  -d 6                      # Set the voltage output duration in seconds then output off
  -r True                   # Set True to enable rechargeable, False to disable rechargeable
  -a                        # Current measurement
  -z                        # Voltage measurement
  -s True                   # Set switch ON (True) or OFF (False) for J-Link programming IOs
  -p True                   # Enable (True) or disable (False) port for USB charging cable
or
  --init                    # Initialize GPIO setup, without -i the GPIO will keep previous setting
  --end                     # Cleanup GPIO settings. Shall use this command to end up power supply.
  --calibration             # Voltage calibration
  --voltage 3.8             # Set voltage to 3.8v (valid range: 0.70 ~ 5.00 v)
  --precise-voltage 3.8     # Set voltage to 3.80v in +- 2mV tolerance
  --on                      # Set voltage output on
  --off                     # Set voltage output off
  --duration 6              # Set the voltage output duration in seconds then output off
  --recharge True           # Set True to enable rechargeable, False to disable rechargeable
  --measure_current         # Current measurement
  --measure_voltage         # Voltage measurement
  --switch_state True       # Set switch on for J-Link programming IOs
  --port_5_state True       # Enable logical port 5 on Phidgets USB Hub


    Use case 1 : calibration
    -i -c -e                 # Initialize GPIO setup, calibration, cleanup GPIO settings

    Use case 2 : measure voltage range of over-voltage in medium level
    -i -m Medium -e          # Initialize GPIO setup, measure over voltage range in medium level, cleanup GPIO
    settings

    Use case 3 : Output On/Off, voltage settings
    -i -v 3.8 -o             # Initialize power supply, calibration, set voltage to 3.8v and keep voltage output on
    -v 4.2                   # Set voltage to 4.2v
    -f                       # Turn off voltage output
    -v 3.8                   # Set voltage to 3.8v
    -o                       # Turn on voltage output
    -e                       # Cleanup GPIO settings

    Use case 4 : Get battery statue: discharging, charge, full-charge
    -p False                 # Run shell command to power off USB cable usb_cable_port
    -i -v 3.8 -o             # Give a nominal voltage to Herzog
    -r True                  # Enable recharge
    -p True                  # After power on USB usb_cable_port, DUT shall be under "Recharging State".
    -r False                 # Disable recharge, DUT shall be under "Charge Complete State".
    -e                       # Cleanup

    Use case 5 : (Power board v3) Get battery level: critical, low, good, full
    -TDB
"""
            self._parser = parser
        # end if

        return self._parser
    # end def get_parser

    parser = property(get_parser)

    def parse_args(self):
        """
        Parses the program arguments
        """
        parser = self.get_parser()
        args = parser.parse_args()

        # Iterate over the args.
        self.calibration = args.calibration
        self.on = args.on
        self.off = args.off
        self.init = args.init
        self.end = args.end
        self.measure_current = args.measure_current
        self.measure_voltage = args.measure_voltage
        self.set_gpio_to_input = args.set_gpio_to_input

        if args.measure_over_voltage:
            self.over_voltage_level = args.measure_over_voltage
        # end if

        if args.voltage:
            self.voltage = self._round_input_voltage(
                round(float(args.voltage), PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS))
        # end if

        if args.precise_voltage:
            self.precise_voltage = self._round_input_voltage(
                round(float(args.precise_voltage), PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS))
        # end if

        if args.duration:
            self.duration = float(args.duration)
        # end if

        if args.recharge is not None:
            self.recharge = (args.recharge == 'True')
        # end if

        if args.switch_state is not None:
            self.switch_state = (args.switch_state == 'True')
        # end if

        if args.port_5_state is not None:
            self.port_5_state = (args.port_5_state == 'True')
        # end if
    # end def parse_args

    @staticmethod
    def _round_input_voltage(voltage):
        """
        Round input voltage up to the third decimal places

        :param voltage: User inputs voltage
        :type voltage: ``float``

        :return: The rounded voltage
        :rtype: ``float``
        """
        v = int(ceil(voltage * MILLI_FACTOR))
        assert v % PowerSupplyConstant.MILLI_VOLTAGE_RESOLUTION == 0, f'Invalid voltage {voltage}'
        assert v == 0 or \
               PowerSupplyConstant.MILLI_VOLTAGE_LOWER_BOUND <= v <= PowerSupplyConstant.MILLI_VOLTAGE_UPPER_BOUND, \
               f'Voltage {voltage} is not in the valid range ' \
               f'{PowerSupplyConstant.MILLI_VOLTAGE_LOWER_BOUND / MILLI_FACTOR} ~ ' \
               f'{PowerSupplyConstant.MILLI_VOLTAGE_UPPER_BOUND / MILLI_FACTOR} V'
        return round(v / MILLI_FACTOR, PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS)
    # end def _round_input_voltage

    def destroy(self):
        """
        Clean-up GPIO settings and remove reference of power supply object
        """
        if PowerSupplyBoardJlinkConnectionControl.is_control_pin_connected(control_pin=Raspi.PIN.JLINK_IO_SWITCH):
            PowerSupplyBoardJlinkConnectionControl(Raspi.PIN.JLINK_IO_SWITCH).connect()
        # end if
        self.power_supply.set_raw_voltage(v=0)
        self.power_supply.output_off()
        self.power_supply.__del__()
    # end def destroy

    def output_by_duration(self):
        """
        Enable the output voltage for the given duration value. The time unit is second.
        """
        self.power_supply.output_on()
        sleep(self.duration)
        self.power_supply.output_off()
    # end def output_by_duration

    def measure_over_voltage(self):
        """
        Measure the range of over voltage at a specific level. (high, medium, low)

        Note: Shall power off USB charging cable while doing the measurement
        """
        # Turn off usb charging cable on Phidgets USB Hub
        LibusbDriver.turn_off_usb_charging_cable(force=True)

        # Store previous status
        shall_turn_off_then_on = self.power_supply.output
        if shall_turn_off_then_on:
            self.power_supply.output_off()
        # end if
        current_voltage = self.power_supply.get_voltage_from_table()

        cut_off_voltage, resume_voltage = None, None
        trigger, resume = None, None
        if self.over_voltage_level.lower() == 'high':
            cut_off_voltage, resume_voltage = self._check_over_voltage_range(
                    reference_voltage=3.3, cutoff_lower_bound=4.3, cutoff_upper_bound=4.95, resume_lower_bound=4.2)
            trigger = OverVoltageProtection.HIGH_TRIGGER
            resume = OverVoltageProtection.HIGH_RESUME
        elif self.over_voltage_level.lower() == 'medium':
            cut_off_voltage, resume_voltage = self._check_over_voltage_range(
                    reference_voltage=2.3, cutoff_lower_bound=3.4, cutoff_upper_bound=3.8, resume_lower_bound=3.3)
            trigger = OverVoltageProtection.MEDIUM_TRIGGER
            resume = OverVoltageProtection.MEDIUM_RESUME
        elif self.over_voltage_level.lower() == 'low':
            cut_off_voltage, resume_voltage = self._check_over_voltage_range(
                    reference_voltage=0.7, cutoff_lower_bound=1.6, cutoff_upper_bound=1.9, resume_lower_bound=1.5)
            trigger = OverVoltageProtection.LOW_TRIGGER
            resume = OverVoltageProtection.LOW_RESUME
        else:
            warnings.warn(f'Unknown over-voltage level: {self.over_voltage_level}')
        # end if

        result = f'cut_off_voltage={cut_off_voltage}, resume_voltage={resume_voltage}'
        assert trigger >= cut_off_voltage, result
        assert resume <= resume_voltage, result

        print(f'{self.over_voltage_level}: {result}')

        # Restore previous status
        self.power_supply.set_raw_voltage(v=current_voltage)
        if shall_turn_off_then_on:
            self.power_supply.output_on()
        # end if
    # end def measure_over_voltage

    def _check_over_voltage_range(self, reference_voltage, cutoff_lower_bound, cutoff_upper_bound, resume_lower_bound):
        """
        Check the voltage range against the over-voltage protection.
        Shall power off USB charging cable during the check procedure.

        :param reference_voltage: The reference voltage for each checking step
        :type reference_voltage: ``float``
        :param cutoff_lower_bound: The lower bound value for checking cut-off voltage
        :type cutoff_lower_bound: ``float``
        :param cutoff_upper_bound: The Upper bound value for checking cut-off voltage
        :type cutoff_upper_bound: ``float``
        :param resume_lower_bound: The lower bound value for checking resume voltage
        :type resume_lower_bound: ``float``

        :return: The measured cut-off and resume voltages
        :rtype: ``float``, ``float``
        """
        self.power_supply.set_raw_voltage(v=0)
        self.power_supply.wait_voltage_dropping_under_500mv()
        self.power_supply.set_ignore_voltage_warning(ignore=True)

        voltage_steps = list(range(int(float(cutoff_lower_bound) * MILLI_FACTOR),
                                   int(float(cutoff_upper_bound) * MILLI_FACTOR),
                                   10))
        cut_off_voltage = 0
        for v in voltage_steps:
            self.power_supply.set_raw_voltage(v=reference_voltage)
            sleep(.6)

            self.power_supply.set_raw_voltage(v=round(v / MILLI_FACTOR, PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS))
            sleep(.6)

            if self.power_supply.is_over_voltage_triggered():
                cut_off_voltage = round(v / MILLI_FACTOR, PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS)
                break
            # end if
        # end for

        resume_voltage = 0
        if cut_off_voltage > resume_lower_bound:
            voltage_steps = list(range(int(float(cut_off_voltage) * MILLI_FACTOR),
                                       int(float(resume_lower_bound) * MILLI_FACTOR),
                                       -10))
            for v in voltage_steps:
                self.power_supply.set_raw_voltage(
                    v=round(v / MILLI_FACTOR, PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS))
                sleep(.3)
                if not self.power_supply.is_over_voltage_triggered():
                    resume_voltage = round(v / MILLI_FACTOR, PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS)
                    break
                # end if
            # end for
        # end if

        self.power_supply.set_ignore_voltage_warning(ignore=False)
        return cut_off_voltage, resume_voltage
    # end def _check_over_voltage_range

    def print_current(self):
        """
        Print current value
        """
        self.power_supply.configure_measurement_mode(mode='current')
        sleep(0.15)
        print(f'Current: {self.power_supply.get_current() * MILLI_FACTOR} uA')
        self.power_supply.configure_measurement_mode(mode='tension')
    # end def print_current

    def print_voltage(self):
        """
        Print voltage value
        """
        print(f'Voltage: {self.power_supply.read_voltage(digits=PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS)} V')
    # end def print_voltage

    @staticmethod
    def set_phidgets_port_5_state(state):
        """
        Enable/disable port 5 (USB charging cable)

        Note:
            Shall invoke LibusbDriver.discover_usb_hub() first before using this function.

        :param state: Set True or False to change port 5 state
        :type state: ``bool``
        """
        if state:
            LibusbDriver.turn_on_usb_charging_cable(force=True)
        else:
            LibusbDriver.turn_off_usb_charging_cable(force=True)
        # end if
    # end def set_phidgets_port_5_state
# end class PowerSupplyUtility


if __name__ == '__main__':
    PowerSupplyUtility(sys.stdout, sys.stderr)
# end if

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
