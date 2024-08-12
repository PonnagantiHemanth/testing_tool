#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.powersupply
:brief: Control library for power supply board rev.2 and later
:author: Fred Chen <fchen7@logitech.com>
:date: 2020/01/02
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import json
import sys
from os import mkdir
from os import path
from pathlib import Path
from threading import Lock
from time import sleep
from warnings import warn

from pylibrary.emulator.emulatorinterfaces import PowerSupplyEmulationInterface
from pylibrary.tools.threadutils import synchronized
from pyraspi.raspi import Raspi
from pyraspi.services.ina226 import INA226
from pyraspi.services.ina226 import ina226_averages_t
from pyraspi.services.ina226 import ina226_busConvTime_t
from pyraspi.services.ina226 import ina226_mode_t
from pyraspi.services.ina226 import ina226_shuntConvTime_t
from pyraspi.services.mcp4725 import MCP4725
from pyusb.libusbdriver import LibusbDriver

if sys.platform == 'linux':
    import RPi.GPIO as GPIO
# end if


# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
__version__ = "0.0.0-auto.0"

_FRAMEWORK_DIR_PATH = f'{str(Path.home())}/framework'
_CALIBRATION_FILE_PATH = f'{_FRAMEWORK_DIR_PATH}/mcp4725.json'

MILLI_FACTOR = 1000
POWER_SUPPLY_LOCK = Lock()


class PowerSupplyConstant:
    """
    Power supply Constants
    """
    MILLI_VOLTAGE_LOWER_BOUND = 800  # mV
    MILLI_VOLTAGE_UPPER_BOUND = 4350
    MILLI_VOLTAGE_RESOLUTION = 5
    VOLTAGE_SIGNIFICANT_DIGITS = 3  # Number of significant digits after the decimal point
    CURRENT_SIGNIFICANT_DIGITS = 6
    MCP4725_DAC_START = 496
    MCP4725_DAC_END = 4096
# end class PowerSupplyConstant


class OverVoltageProtection:
    """
    Over voltage protection threshold definition
    """
    HIGH_TRIGGER = 4.8
    HIGH_RESUME = 4.3
    MEDIUM_TRIGGER = 3.8
    MEDIUM_RESUME = 3.4
    LOW_TRIGGER = 1.8
    LOW_RESUME = 1.6
# end class OverVoltageProtection


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class MCP4725PowerSupplyEmulationInterface(PowerSupplyEmulationInterface):
    """
    Power supply control class for power supply board rev.2 and later
    """
    _instance = None
    _has_config_gpio = False

    @classmethod
    def set_gpio_to_input(cls):
        """
        Set GPIOs that be used for keyboard and mouse to GPIO input
        """
        if sys.platform != 'linux':
            return
        # end if

        for gpio in Raspi.PRESET_GPIO_LIST:
            GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
        # end for
    # end def set_gpio_to_input

    @classmethod
    def discover(cls):
        """
        Has a quick availability check

        :return: power supply is available or not
        :rtype: ``bool``
        """
        if sys.platform != 'linux':
            return False
        # end if
        power_supply = MCP4725PowerSupplyEmulationInterface.get_instance()
        if power_supply is None:
            return False
        else:
            return True
        # end if
    # end def discover

    @staticmethod
    @synchronized(POWER_SUPPLY_LOCK)
    def get_instance(starting_voltage, reset_gpio=True, discover_usb_hub=True):
        """
        Get power supply instance. Shall not create MCP4725PowerSupplyEmulationInterface object by different way.

            Note:
            The voltage output state is based on the reset_gpio flag
            - True: disable voltage output (default setting) and set Vout = 0
            - False: the voltage output state depends on previous settings

        :param starting_voltage: The starting voltage that will be used as default value
        :type starting_voltage: ``float``
        :param reset_gpio: set False to keep previous GPIO settings - OPTIONAL
        :type reset_gpio: ``bool``
        :param discover_usb_hub: True to scan for USB HUB presence and force port 5 to off,
                                otherwise False to keep USB port states unchanged - OPTIONAL
        :type discover_usb_hub: ``bool``

        :return: Power supply object
        :rtype: ``MCP4725PowerSupplyEmulationInterface``
        """
        if MCP4725PowerSupplyEmulationInterface._instance is None:
            MCP4725PowerSupplyEmulationInterface(starting_voltage)
            # Discover Phidget USB Hub
            # If Phidget USB Hub presented, will power off USB charging cable before doing voltage calibration
            if discover_usb_hub:
                LibusbDriver.discover_usb_hub()
            # end if
        # end if

        if MCP4725PowerSupplyEmulationInterface._instance is not None and \
                not MCP4725PowerSupplyEmulationInterface._has_config_gpio:
            MCP4725PowerSupplyEmulationInterface._instance.gpio_setup(reset_gpio)
        # end if

        return MCP4725PowerSupplyEmulationInterface._instance
    # end def get_instance

    def __init__(self, starting_voltage, verbose=False):
        """
        :param starting_voltage: The starting voltage that will be used as default value
        :type starting_voltage: ``float``
        :param verbose: True to output debug message, False otherwise - OPTIONAL
        :type verbose: ``bool``

        :raise ``AssertionError``: Another instance of MCP4725PowerSupplyEmulationInterface was already initialized
        """
        assert MCP4725PowerSupplyEmulationInterface._instance is None, 'Allowed a single power supply instance only!'

        # Get MCP4725 and INA226 instances and apply default settings.
        try:
            self._mcp4725 = MCP4725.get_instance()
            assert self._mcp4725 is not None
            self._ina226 = INA226.get_instance()
            assert self._ina226 is not None
            self.configure_measurement_mode()
            self._v_table = None
            self._output = False
            self._over_voltage = None
            self._ignore_over_voltage_warning = False
            self._starting_voltage = starting_voltage
            self._verbose = verbose
            MCP4725PowerSupplyEmulationInterface._instance = self
        except Exception as e:
            warn(e)
        # end try
    # end def __init__

    def __del__(self):
        """
        Clean-up GPIO settings and de-reference power supply object
        """
        if MCP4725PowerSupplyEmulationInterface._instance is not None:
            self.gpio_cleanup()
            MCP4725PowerSupplyEmulationInterface._instance = None
        # end if
    # end def __del__

    @property
    def output(self):
        """
        Return the output state of the power supply (True: ON, False: OFF).

        :return: output state of the power supply (True: ON, False: OFF)
        :rtype: ``bool``
        """
        return self._output
    # end def property getter output

    @property
    def has_sink_current_capability(self):
        # See ``PowerSupplyEmulationInterface.has_sink_current_capability``
        return False
    # end def property getter has_sink_current_capability

    @staticmethod
    def gpio_cleanup():
        """
        Clean-up GPIO settings on raspberry Pi
        """
        if MCP4725PowerSupplyEmulationInterface._has_config_gpio:
            GPIO.cleanup([Raspi.PIN.VOLTAGE_OUTPUT, Raspi.PIN.RECHARGEABLE, Raspi.PIN.OVER_VOLTAGE_ALERT, ])
            MCP4725PowerSupplyEmulationInterface._has_config_gpio = False
        # end if
    # end def gpio_cleanup

    def gpio_setup(self, reset_gpio=True):
        """
        Configure GPIOs on Raspberry Pi.

            Note:
            The voltage output state is based on the reset_gpio flag
            - True: disable voltage output (default setting) and set Vout = 0
            - False: the voltage output state depends on previous settings

        :param reset_gpio: set False to keep previous GPIO settings - OPTIONAL
        :type reset_gpio: ``bool``
        """
        try:
            if not MCP4725PowerSupplyEmulationInterface._has_config_gpio:
                MCP4725PowerSupplyEmulationInterface._has_config_gpio = True
                GPIO.setmode(GPIO.BOARD)
                GPIO.setwarnings(False)
                GPIO.setup(Raspi.PIN.OVER_VOLTAGE_ALERT, GPIO.IN)
                GPIO.add_event_detect(Raspi.PIN.OVER_VOLTAGE_ALERT, GPIO.BOTH, callback=self.over_voltage_alert)
                if reset_gpio:
                    self._mcp4725.raw_value = 0
                    GPIO.setup(Raspi.PIN.VOLTAGE_OUTPUT, GPIO.OUT, initial=GPIO.LOW)
                    GPIO.setup(Raspi.PIN.RECHARGEABLE, GPIO.OUT, initial=GPIO.LOW)
                else:
                    GPIO.setup(Raspi.PIN.VOLTAGE_OUTPUT, GPIO.OUT)
                    GPIO.setup(Raspi.PIN.RECHARGEABLE, GPIO.OUT)
                    if GPIO.input(Raspi.PIN.VOLTAGE_OUTPUT):
                        self._output = True
                    # end if
                # end if
            # end if
        except IOError as io_err:
            warn(io_err)
        except Exception as e:
            warn(e)
        # end try
    # end def gpio_setup

    def get_v_table(self, json_path=_CALIBRATION_FILE_PATH, reload=False):
        """
        Get the voltage to MCP4725 raw value mapping table

        :param json_path: The full path to mcp4725.json, defaults to `_CALIBRATION_FILE_PATH` - OPTIONAL
        :type json_path: ``string``
        :param reload: Set True if it is needed to reload mapping file again, defaults to False - OPTIONAL
        :type reload: ``bool``

        :return: The voltage to MCP4725 raw value mapping table
        :rtype: ``dict``
        """
        if self._v_table is None or reload is True:
            try:
                with open(json_path) as fp:
                    self._v_table = json.loads(fp.read())
                # end with
            except Exception as e:
                warn(str(e))
                self._v_table = None
            # end try
        # end if
        return self._v_table
    # end def get_v_table

    def get_voltage_from_table(self, reload=False):
        """
        Get the mapping voltage to MCP4725 raw value

        :param reload: Set True if it is needed to reload mapping file again, defaults to False - OPTIONAL
        :type reload: ``bool``

        :return: The mapping voltage to MCP4725 raw value - OPTIONAL
        :rtype: ``float``

        :raise ``AssertionError``: Cannot load voltage mapping table
        """
        if self._v_table is None:
            assert self.get_v_table(reload=reload) is not None, 'Cannot load voltage mapping table!'
        # end if

        try:
            v = self._v_table['r'][str(self._mcp4725.raw_value)]
        except KeyError:
            v = self._starting_voltage
            if self._verbose:
                print(f'Cannot find the voltage value with mcp4725 raw value! Use starting voltage: {v}')
            # end if
        # end try
        return v
    # end def get_voltage_from_table

    def set_raw_voltage(self, v, reload=False):
        """
        Set supported voltage in mcp4725.json. The resolution is 10mV.

        :param v: The supported voltage in mcp4725.json.
        :type v: ``float``
        :param reload: Set True if it is needed to reload mapping file again, defaults to False - OPTIONAL
        :type reload: ``bool``

        :return: The mapping voltage
        :rtype: ``float``

        :raise ``AssertionError``: Cannot load voltage mapping table
        """
        if self._v_table is None:
            assert self.get_v_table(reload=reload) is not None, 'Cannot load voltage mapping table!'
        # end if

        if v > 0:
            self._mcp4725.raw_value = self._v_table['v'][str(v)]
        else:
            self._mcp4725.raw_value = 0
        # end if

        return self._v_table['r'][str(self._mcp4725.raw_value)]
    # end def set_raw_voltage

    def read_voltage(self, digits=3):
        """
        Read the voltage value on Vout.

            Note:
            The Vout value isn't affected by output enable/disable.

        :param digits: The milli volt precision - OPTIONAL
        :type digits: ``int``

        :return: The actual voltage on Vout.
        :rtype: ``float``
        """
        return round(self._ina226.read_bus_voltage(), digits)
    # end def read_voltage

    @synchronized(POWER_SUPPLY_LOCK)
    def output_off(self):
        """
        Turn off voltage output
        """
        GPIO.output(Raspi.PIN.VOLTAGE_OUTPUT, GPIO.LOW)
        sleep(.5)
        self._output = False
    # end def output_off

    @synchronized(POWER_SUPPLY_LOCK)
    def output_on(self):
        """
        Turn on voltage output
        """
        GPIO.output(Raspi.PIN.VOLTAGE_OUTPUT, GPIO.HIGH)
        sleep(.05)
        self._output = True
    # end def output_on

    def log_voltage(self, voltage, class_name):
        """
        Send voltage value to the console.

        :param voltage: The output voltage value
        :type voltage: ``float``
        :param class_name: The class name of caller
        :type class_name: ``str``
        """
        if self._verbose:
            print(f'{class_name} {voltage * MILLI_FACTOR} mV')
        # end if
    # end def log_voltage

    def over_voltage_alert(self, channel):
        """
        Output warning message if received over voltage notification.
        The OVP pin is LOW active.

        :param channel: Raspberry Pi over voltage pin
        :type channel: ``int``
        """
        if GPIO.input(channel) == 0:
            self._over_voltage = self.read_voltage(digits=PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS)
            if not self._ignore_over_voltage_warning:
                warn(f'Over voltage {self.get_voltage_from_table()}v detected!')
            # end if
        else:
            self._over_voltage = None
        # end if
    # end def over_voltage_alert

    def is_over_voltage_triggered(self):
        """
        Get the current over voltage status

        :return: status of over voltage
        :rtype: ``bool``
        """
        if self._over_voltage is None:
            return False
        else:
            return True
        # end if
    # end def is_over_voltage_triggered

    def set_ignore_voltage_warning(self, ignore=False):
        """
        Enable/disable over-voltage warning message

        :param ignore: True to disable over voltage warning messages, False otherwise - OPTIONAL
        :type ignore: ``bool``
        """
        self._ignore_over_voltage_warning = ignore
    # end def set_ignore_voltage_warning

    def voltage_calibration(self):
        """
        Voltage calibration for MCP4725 12bit DAC

            Note:
                Shall power OFF USB charging cable before doing the calibration
        """
        LibusbDriver.turn_off_usb_charging_cable()

        try:
            # Store previous status
            shall_turn_off_then_on = self._output
            if shall_turn_off_then_on:
                self.output_off()
            # end if
            self.set_ignore_voltage_warning(ignore=True)
            self._mcp4725.raw_value = 0

            # wait for voltage dropping under 500mV
            self.wait_voltage_dropping_under_500mv()

            v_table = dict()
            r_table = dict()
            # Set the first record
            v_table[0] = 0
            r_table[0] = 0

            cur_v = round(PowerSupplyConstant.MILLI_VOLTAGE_LOWER_BOUND / MILLI_FACTOR,
                          PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS)
            v_step = round(PowerSupplyConstant.MILLI_VOLTAGE_RESOLUTION / MILLI_FACTOR,
                           PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS)
            v_upper_bound = round(PowerSupplyConstant.MILLI_VOLTAGE_UPPER_BOUND / MILLI_FACTOR,
                                  PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS)
            for x in range(PowerSupplyConstant.MCP4725_DAC_START, PowerSupplyConstant.MCP4725_DAC_END):
                self._mcp4725.raw_value = x
                sleep(.05)
                v = self.read_voltage(digits=PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS + 1)

                if v >= cur_v:
                    v_table[cur_v] = x
                    r_table[x] = cur_v
                    cur_v = round(cur_v + v_step, PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS)
                # end if

                if cur_v > v_upper_bound:
                    break
                # end if
            # end for
            print('Voltage calibration .. ok')

            # create framework directory if didn't exist
            if not path.isdir(_FRAMEWORK_DIR_PATH):
                mkdir(_FRAMEWORK_DIR_PATH)
            # end if

            # save to file
            c_table = dict()
            c_table['v'] = v_table
            c_table['r'] = r_table
            with open(_CALIBRATION_FILE_PATH, 'w') as fp:
                json.dump(c_table, fp)
            # end with

            # Restore previous status
            self.set_ignore_voltage_warning(ignore=False)
            if shall_turn_off_then_on:
                self.output_on()
            # end if
        except Exception as e:
            print(e)
        # end try
    # end def voltage_calibration

    def turn_on(self, voltage=None):
        """
        Plug-in the device battery.

        :param voltage: Power ON voltage, defaults to None (use predefined starting voltage) - OPTIONAL
        :type voltage: ``float``
        """
        if not voltage:
            self.set_voltage(voltage=self._starting_voltage)
        else:
            self.set_voltage(voltage=voltage)
        # end if
        sleep(.1)
        self.output_on()
    # end def turn_on

    def turn_off(self):
        """
        Plug out the battery of the device.
        """
        self.set_voltage(voltage=0)
        self.output_off()
    # end def turn_off

    def set_voltage(self, voltage=None, fast_ramp=True):
        """
        Set the battery to a certain level.

        :param voltage: Targeted voltage value in V. if voltage is None, starting voltage will be used - OPTIONAL
        :type voltage: ``float``
        :param fast_ramp: Voltage incrementation method - OPTIONAL
                          - True: enable several increment values to get faster to the expected value
                          - False: increment the voltage by small step (around 1mV by step)
        :type fast_ramp: ``bool``

        :return: Voltage calibration has been updated or not
        :rtype: ``bool``

        :raise ``AssertionError``: Out-of-bound voltage
        """
        if voltage is None:
            voltage = self._starting_voltage
        # end if

        # TODO use fast_ramp, we need to keep the parameter even if not used because it is used in some feature 1000's
        #  tests
        v = round(float(voltage), PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS)
        assert voltage == 0 or \
               PowerSupplyConstant.MILLI_VOLTAGE_LOWER_BOUND <= v * MILLI_FACTOR <= \
               PowerSupplyConstant.MILLI_VOLTAGE_UPPER_BOUND

        pre_v = self.get_voltage_from_table()
        self.set_raw_voltage(v=v)
        self.log_voltage(v, 'set_voltage input')

        timeout = 0
        updated_table = False
        while True:
            actual_v = self.read_voltage()
            dv = int((actual_v - v) * MILLI_FACTOR)

            # When setting v=3.7, values in range [3.698 .. 3.702] are accepted
            if -2 <= dv <= 2:
                break
            else:
                timeout += 1
                if timeout > 20:
                    if v != 0:
                        if self._verbose:
                            print(f'Voltage {actual_v}V is out of valid range. Expected: {v}V +- 2mV, '
                                  f'Previous setting: {pre_v}V. Tuning voltage output...')
                        # end if
                        self.update_v_table(v=v, dac_value_delta=-int(dv / 2))
                        self.set_raw_voltage(v=v)
                        updated_table = True
                    else:
                        break
                    # end if
                # end if
                sleep(.05)
            # end if
        # end while

        return updated_table
    # end def set_voltage

    def configure_measurement_mode(self, mode="tension"):
        """
        Configure ina226 register with 1 or 16 samples per measure

        :param mode: Set 'tension' for voltage measurement and 'current' for current measurement - OPTIONAL
        :type mode: ``str``
        """
        if mode == "tension":
            average_parameter = 'INA226_AVERAGES_1'
        elif mode == "current":
            average_parameter = 'INA226_AVERAGES_16'
        else:
            return
        # end if
        self._ina226.configure(avg=ina226_averages_t[average_parameter],
                               busConvTime=ina226_busConvTime_t['INA226_BUS_CONV_TIME_8244US'],
                               shuntConvTime=ina226_shuntConvTime_t['INA226_SHUNT_CONV_TIME_8244US'],
                               mode=ina226_mode_t['INA226_MODE_SHUNT_BUS_CONT'])
        self._ina226.calibrate(rShuntValue=0.5, iMaxExcepted=0.16)
    # end def configure_measurement_mode

    def get_voltage(self):
        """
        Get the voltage value on Vout.

        :return: Voltage value in V
        :rtype: ``float``
        """
        if self.output:
            return self.read_voltage()
        else:
            return 0.0
        # end if
    # end def get_voltage

    def get_current(self):
        """
        Get the actual current consumption

        :return: Current_value value in mA unit
        :rtype: ``float``
        """
        return round(self._ina226.read_shunt_current() * MILLI_FACTOR, PowerSupplyConstant.CURRENT_SIGNIFICANT_DIGITS)
    # end def get_current

    def restart_device(self, starting_voltage=None):
        """
        Turn off the power on the Device under test (wait for Vdd to get below 50mV),
        then set voltage the nominal value (cf test configuration)

        :param starting_voltage: The voltage to use after restart, if None the Nominal value will be used. - OPTIONAL
        :type starting_voltage: ``float``
        """
        self.turn_off()
        sleep(.5)
        self.turn_on(voltage=starting_voltage)
        sleep(1)
    # end def restart_device

    @synchronized(POWER_SUPPLY_LOCK)
    def recharge(self, enable=False):
        """
        Enable/Disable Rechargeable feature

            Note:
                Enable recharge will heat up components on the power supply board.
                Recommend to enable recharge not exceed 2 hours.

        :param enable: enable rechargeable or not - OPTIONAL
        :type enable: ``bool``
        """
        if enable:
            GPIO.output(Raspi.PIN.RECHARGEABLE, GPIO.HIGH)
        else:
            GPIO.output(Raspi.PIN.RECHARGEABLE, GPIO.LOW)
        # end if
        sleep(.05)
    # end def recharge

    def update_v_table(self, v, dac_value_delta):
        """
        Update voltage calibration table while the voltage measured by INA226 is out of valid range.

            Note:
                It's a temporary update and won't override mcp4825.json.

        :param v: target voltage in Volt
        :type v: ``float``
        :param dac_value_delta: delta DAC value for voltage output adjustment
        :type dac_value_delta: ``int``
        """
        v_table = self.get_v_table()
        dac_value = v_table['v'][str(v)]
        v_table['v'][str(v)] = dac_value + dac_value_delta
        v_table['r'].pop(str(dac_value), None)
        v_table['r'][str(dac_value + dac_value_delta)] = v
    # end def update_v_table

    def update_calibration_file(self):
        """
        Update calibration file by _v_table
        """
        with open(_CALIBRATION_FILE_PATH, 'w') as fp:
            json.dump(self._v_table, fp)
        # end with
    # end def update_calibration_file

    def wait_voltage_dropping_under_500mv(self):
        """
        Wait output voltage dropping under 500 mV (the upper bound threshold of 0 volt).

        :raise ``AssertionError``: Cannot drop voltage lower than 0.5v in 15s
        """
        count = 0
        zero_volt_upper_threshold = 500
        sleep_count = 150
        while (self.read_voltage(digits=PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS) * MILLI_FACTOR) > \
                zero_volt_upper_threshold:
            sleep(.1)
            count += 1
            assert count <= sleep_count, 'Cannot drop voltage lower than 0.5v in 15s. ' \
                                         'Please remove USB charging cable on DUT.'
        # end while
    # end def wait_voltage_dropping_under_500mv
# end class MCP4725PowerSupplyEmulationInterface

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
