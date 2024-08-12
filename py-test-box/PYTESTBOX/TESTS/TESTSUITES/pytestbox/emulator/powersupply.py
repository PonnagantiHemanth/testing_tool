#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
""" @package pytestbox.emulator.powersupply

@brief  Demonstrates Power Supply Board v2 capabilities

@author christophe roquebert

@date   2020/01/16
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import sleep

from pytestbox.base.basetest import BaseTestCase
from pyharness.selector import features
from pyharness.selector import services
from pyharness.extensions import level
from pyraspi.services.mcp4725 import MCP4725

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------


class DemoPowerSupplyTestCase(BaseTestCase):
    """
    Demonstrates Power Supply Board v2 capabilities
    """
    DELAY_BETWEEN_STEP = 6

    def setUp(self):
        """
        Handles test prerequisites.
        """
        super(DemoPowerSupplyTestCase, self).setUp()

        # ---------------------------------------------------------------------------
        self.logTitle2('Pre-requisite: Power Board initialization')
        # ---------------------------------------------------------------------------
        if not MCP4725.discover():
            raise Exception('Power supply board v2 not found')
        # end if

        self.log_step = 0
    # end def setUp

    @features('PeripheralEmulation')
    @level('Business')
    @services('PowerSupply')
    def test_power_control(self):
        """
        @tc_synopsis Validates all possible power supply emulator API
        """
        # Starts with voltage = 0V
        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step {self.log_step}: Starts with voltage = 0V')
        # ---------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(0)
        self._go_to_next_step()

        # Set voltage to max value
        max_value = 4.2
        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step {self.log_step}: Set voltage to max value = {max_value}')
        # ---------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(max_value)
        self._go_to_next_step()

        f = self.getFeatures()
        # Put back nominal voltage
        nominal_value = f.PRODUCT.DEVICE.BATTERY.F_NominalVoltage
        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step {self.log_step}: Put back nominal voltage = {nominal_value}')
        # ---------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(voltage=nominal_value)
        self._go_to_next_step()

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step {self.log_step}: Validate 10mV Resolution from {nominal_value} to {nominal_value-1}')
        # ---------------------------------------------------------------------------
        for decrement in range(0, 10):
            # ---------------------------------------------------------------------------
            self.logTrace(f'Force voltage to {nominal_value - decrement/100}')
            # ---------------------------------------------------------------------------
            self.power_supply_emulator.set_voltage(voltage=nominal_value-decrement/100)
            sleep(2)
        # end for
        self._go_to_next_step()

        # Test the Hardware reset
        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step {self.log_step}: Test the Hardware reset to return to nominal voltage = {nominal_value}')
        # ---------------------------------------------------------------------------
        self.power_supply_emulator.restart_device(nominal_value)
        self._go_to_next_step()

        # Force a DUT power-off
        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step {self.log_step}: Force a DUT power-off')
        # ---------------------------------------------------------------------------
        self.power_supply_emulator.turn_off()
        self._go_to_next_step()
        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step {self.log_step}: Wait {self.DELAY_BETWEEN_STEP}s then turn on the device with the last known '
              f'voltage value')
        # ---------------------------------------------------------------------------
        # Turn on the device battery with the last known voltage value
        self.power_supply_emulator.turn_on(voltage=nominal_value)
        self._go_to_next_step()

        # ---------------------------------------------------------------------------
        self.logTitle2(f'End of Test Steps')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("FNT_DEMO_EMULATOR_0010")
    # end def test_power_control

    @features('PeripheralEmulation')
    @level('Business')
    @services('PowerSupply')
    def test_current_measurement(self):
        """
        @tc_synopsis Validates all possible power supply emulator API
        """
        f = self.getFeatures()
        # Put back nominal voltage
        nominal_value = f.PRODUCT.DEVICE.BATTERY.F_NominalVoltage
        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step {self.log_step}: Put nominal voltage = {nominal_value}')
        # ---------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(voltage=nominal_value)
        self._go_to_next_step()

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step {self.log_step}: Configure board in current mode')
        # ---------------------------------------------------------------------------
        self.power_supply_emulator.configure_measurement_mode('current')
        self._go_to_next_step()

        # We do this measure 5 time to let the user do an action that can change the RGB profile,
        # thus changing the consumption
        for _ in range(5):
            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step {self.log_step}: Read current value')
            # ---------------------------------------------------------------------------
            self.logTrace(f'current = {self.power_supply_emulator.get_current()}mA')
            self._go_to_next_step()

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step {self.log_step}: Read current value in sleep mode')
        # ---------------------------------------------------------------------------
        sleep(30)
        self.logTrace(f'current = {self.power_supply_emulator.get_current()}mA')
        self._go_to_next_step()

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step {self.log_step}: Configure board in tension mode')
        # ---------------------------------------------------------------------------
        self.power_supply_emulator.configure_measurement_mode('tension')

        # ---------------------------------------------------------------------------
        self.logTitle2(f'End of Test Steps')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("FNT_DEMO_EMULATOR_0011")
    # end def test_current_measurement

    def _go_to_next_step(self):
        sleep(self.DELAY_BETWEEN_STEP)
        self.log_step += 1
    # end def _go_next_step


# end class DemoPowerSupplyTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
