#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.test.cmods6_test
:brief: Kosmos CMODS6 Module Test Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2021/10/18
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from random import uniform
from time import sleep
from unittest import TestCase

from math import ceil

from pyraspi.services.kosmos.module.cmods6 import Cmods6
from pyraspi.services.kosmos.module.cmods6 import Cmods6Manager
from pyraspi.services.kosmos.module.dac import Dac
from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.kosmos.module.test.module_test import require_kosmos_device
from pyraspi.services.kosmos.protocol.generated.messages import swm_job_descriptor_t
from pyraspi.services.kosmos.protocol.generated.messages import swm_reg_map_t
from pyraspi.services.kosmos.test.kosmos_test import KosmosCommonTestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class Cmods6TestCase(TestCase):
    """
    Kosmos CMODS6 Module Test Class

    Instantiation Test Case
    """

    VOLTAGES_RANGE = [i/10 for i in range(ceil(Dac.MAX_VOLTAGE * 10))] + \
                     [Dac.MAX_VOLTAGE] + \
                     [uniform(0, Dac.MAX_VOLTAGE) for _ in range(10)]

    def test_swm_job_descriptor(self):
        """
        Validating ``swm_job_descriptor_t()`` structure
        """
        job_desc = swm_job_descriptor_t()
        self.assertEqual(0, job_desc.reg)

        # Set number of bytes for PGA+ADC combination
        job_desc.reg = 0
        job_desc.bit.pga_adc_vbat_bytes_nb = 7
        self.assertEqual(7, job_desc.reg)

        # Enable PGA+ADC VBAT
        job_desc.reg = 0
        job_desc.bit.pga_adc_vbat_enable = 1
        self.assertEqual(1 << 3, job_desc.reg)

        # Enable SHIFTER USB
        job_desc.reg = 0
        job_desc.bit.shifter_usb_enable = 1
        self.assertEqual(1 << 16, job_desc.reg)

        # Enable SHIFTER BAT
        job_desc.reg = 0
        job_desc.bit.shifter_bat_enable = 1
        self.assertEqual(1 << 17, job_desc.reg)

        # Enable DAC VUSB
        job_desc.reg = 0
        job_desc.bit.dac_v_usb_enable = 1
        self.assertEqual(1 << 18, job_desc.reg)

        # Enable DAC VBAT
        job_desc.reg = 0
        job_desc.bit.dac_v_bat_enable = 1
        self.assertEqual(1 << 19, job_desc.reg)

        # Enable NTC POT
        job_desc.reg = 0
        job_desc.bit.bat_ntc_value_enable = 1
        self.assertEqual(1 << 30, job_desc.reg)

        # Set Master bit
        job_desc.reg = 0
        job_desc.bit.master_enable = 1
        self.assertEqual(1 << 31, job_desc.reg)
    # end def test_swm_job_descriptor

    def test_swm_reg_map(self):
        """
        Validate ``swm_reg_map_t()`` structure
        """
        reg_map = swm_reg_map_t()

        # SWM Register #1: DAC VBAT
        reg_map.dac_vbat.bit.command = 0x1
        reg_map.dac_vbat.bit.address = 0x2
        reg_map.dac_vbat.bit.data = 0x3456
        self.assertEqual(0x0123456,  reg_map.dac_vbat.reg)

        # SWM Register #2: DAC VUSB
        reg_map.dac_vusb.bit.command = 0xA
        reg_map.dac_vusb.bit.address = 0xB
        reg_map.dac_vusb.bit.data = 0xCDEF
        self.assertEqual(0x0ABCDEF,  reg_map.dac_vusb.reg)

        # SWM Register #3 (LSB): SHIFTER USB
        reg_map.shifter_usb.bit.gate_control_0 = 1
        reg_map.shifter_usb.bit.gate_control_1 = 0
        reg_map.shifter_usb.bit.gate_control_2 = 1
        reg_map.shifter_usb.bit.gate_control_3 = 0
        reg_map.shifter_usb.bit.gate_control_4 = 1
        reg_map.shifter_usb.bit.gate_control_5 = 0
        reg_map.shifter_usb.bit.relay_1 = 1
        reg_map.shifter_usb.bit.relay_2 = 0
        reg_map.shifter_usb.bit.relay_3 = 1
        self.assertEqual(0x0515,  reg_map.shifter_usb.reg)

        # SWM Register #3 (MSB): SHIFTER BAT
        reg_map.shifter_bat.bit.gate_control_0 = 0
        reg_map.shifter_bat.bit.gate_control_1 = 1
        reg_map.shifter_bat.bit.gate_control_2 = 0
        reg_map.shifter_bat.bit.gate_control_3 = 1
        reg_map.shifter_bat.bit.gate_control_4 = 0
        reg_map.shifter_bat.bit.gate_control_5 = 1
        reg_map.shifter_bat.bit.relay_1 = 0
        reg_map.shifter_bat.bit.relay_2 = 1
        reg_map.shifter_bat.bit.relay_3 = 0
        self.assertEqual(0x022A,  reg_map.shifter_bat.reg)

        # SWM Registers #4 & #5: PGA ADC VBAT
        reg_map.pga_adc_vbat.bit.reg1 = 0x01234567
        reg_map.pga_adc_vbat.bit.reg2 = 0x89ABCDEF
        self.assertEqual(0x01234567,  reg_map.pga_adc_vbat.reg[0])
        self.assertEqual(0x89ABCDEF,  reg_map.pga_adc_vbat.reg[1])

        # SWM Registers #6 & #7: PGA ADC IBAT
        reg_map.pga_adc_ibat.bit.reg1 = 0xF0123456
        reg_map.pga_adc_ibat.bit.reg2 = 0x789ABCDE
        self.assertEqual(0xF0123456,  reg_map.pga_adc_ibat.reg[0])
        self.assertEqual(0x789ABCDE,  reg_map.pga_adc_ibat.reg[1])

        # SWM Registers #8 & #9: PGA ADC VUSB
        reg_map.pga_adc_vusb.bit.reg1 = 0xEF012345
        reg_map.pga_adc_vusb.bit.reg2 = 0x6789ABCD
        self.assertEqual(0xEF012345,  reg_map.pga_adc_vusb.reg[0])
        self.assertEqual(0x6789ABCD,  reg_map.pga_adc_vusb.reg[1])

        # SWM Registers #10 & #11: PGA ADC IUSB
        reg_map.pga_adc_iusb.bit.reg1 = 0xDEF01234
        reg_map.pga_adc_iusb.bit.reg2 = 0x56789ABC
        self.assertEqual(0xDEF01234,  reg_map.pga_adc_iusb.reg[0])
        self.assertEqual(0x56789ABC,  reg_map.pga_adc_iusb.reg[1])

        # SWM Registers #12 & #13: Reserved for future usage
        reg_map.reg_12_reserved = 0
        reg_map.reg_13_reserved = 0

        # SWM Register #14: NTC POT
        reg_map.ntc_pot.bit.data = 0x45670123
        self.assertEqual(0x45670123,  reg_map.ntc_pot.reg)
    # end def test_swm_reg_map

    def test_reset_dac(self):
        """
        Validate reset_dac() method.
        """
        # Expected DAC register value
        dac_reg_val = (0x2 << 20) | (0xF << 16)

        cmods6 = Cmods6()
        cmods6.reset_dac(Cmods6.CHANNEL.BATTERY)
        self.assertEqual((1 << 19), cmods6.job_desc.reg)
        self.assertEqual(dac_reg_val, cmods6.reg_map.dac_vbat.reg)
        self.assertEqual(0, cmods6.reg_map.dac_vusb.reg)

        cmods6 = Cmods6()
        cmods6.reset_dac(Cmods6.CHANNEL.USB)
        self.assertEqual((1 << 18), cmods6.job_desc.reg)
        self.assertEqual(0, cmods6.reg_map.dac_vbat.reg)
        self.assertEqual(dac_reg_val, cmods6.reg_map.dac_vusb.reg)

        cmods6 = Cmods6()
        cmods6.reset_dac(Cmods6.ALL_CHANNELS)
        self.assertEqual((1 << 18) | (1 << 19), cmods6.job_desc.reg)
        self.assertEqual(dac_reg_val, cmods6.reg_map.dac_vbat.reg)
        self.assertEqual(dac_reg_val, cmods6.reg_map.dac_vusb.reg)
    # end def test_reset_dac

    def test_set_output_voltage(self):
        """
        Validate set_output_voltage() method.
        """
        for output_voltage in self.VOLTAGES_RANGE:
            # Expected DAC register value
            dac_value = Dac.volt_to_dac_value(output_voltage)
            dac_reg_val = (0x2 << 20) | (0x0 << 16) | dac_value

            cmods6 = Cmods6()
            cmods6.set_output_voltage(Cmods6.CHANNEL.BATTERY, output_voltage)
            self.assertEqual((1 << 19), cmods6.job_desc.reg)
            self.assertEqual(dac_reg_val, cmods6.reg_map.dac_vbat.reg)
            self.assertEqual(0, cmods6.reg_map.dac_vusb.reg)

            cmods6 = Cmods6()
            cmods6.set_output_voltage(Cmods6.CHANNEL.USB, output_voltage)
            self.assertEqual((1 << 18), cmods6.job_desc.reg)
            self.assertEqual(0, cmods6.reg_map.dac_vbat.reg)
            self.assertEqual(dac_reg_val, cmods6.reg_map.dac_vusb.reg)

            cmods6 = Cmods6()
            cmods6.set_output_voltage(Cmods6.ALL_CHANNELS, output_voltage)
            self.assertEqual((1 << 18) | (1 << 19), cmods6.job_desc.reg)
            self.assertEqual(dac_reg_val, cmods6.reg_map.dac_vbat.reg)
            self.assertEqual(dac_reg_val, cmods6.reg_map.dac_vusb.reg)
        # end for
    # end def test_set_output_voltage

    def test_set_sink_current(self):
        """
        Validate set_sink_current() method.
        """
        for sink_current in self.VOLTAGES_RANGE:
            # Expected DAC register value
            dac_value = Dac.volt_to_dac_value(sink_current)
            dac_reg_val = (0x2 << 20) | (0x1 << 16) | dac_value

            cmods6 = Cmods6()
            cmods6.set_sink_current(Cmods6.CHANNEL.BATTERY, sink_current)
            self.assertEqual((1 << 19), cmods6.job_desc.reg)
            self.assertEqual(dac_reg_val, cmods6.reg_map.dac_vbat.reg)
            self.assertEqual(0, cmods6.reg_map.dac_vusb.reg)

            cmods6 = Cmods6()
            cmods6.set_sink_current(Cmods6.CHANNEL.USB, sink_current)
            self.assertEqual((1 << 18), cmods6.job_desc.reg)
            self.assertEqual(0, cmods6.reg_map.dac_vbat.reg)
            self.assertEqual(dac_reg_val, cmods6.reg_map.dac_vusb.reg)

            cmods6 = Cmods6()
            cmods6.set_sink_current(Cmods6.ALL_CHANNELS, sink_current)
            self.assertEqual((1 << 18) | (1 << 19), cmods6.job_desc.reg)
            self.assertEqual(dac_reg_val, cmods6.reg_map.dac_vbat.reg)
            self.assertEqual(dac_reg_val, cmods6.reg_map.dac_vusb.reg)
        # end for
    # end def test_set_sink_current

    def test_set_source_current(self):
        """
        Validate set_source_current() method.
        """
        for source_current in self.VOLTAGES_RANGE:
            # Expected DAC register value
            dac_value = Dac.volt_to_dac_value(source_current)
            dac_reg_val = (0x2 << 20) | (0x2 << 16) | dac_value

            cmods6 = Cmods6()
            cmods6.set_source_current(Cmods6.CHANNEL.BATTERY, source_current)
            self.assertEqual((1 << 19), cmods6.job_desc.reg)
            self.assertEqual(dac_reg_val, cmods6.reg_map.dac_vbat.reg)
            self.assertEqual(0, cmods6.reg_map.dac_vusb.reg)

            cmods6 = Cmods6()
            cmods6.set_source_current(Cmods6.CHANNEL.USB, source_current)
            self.assertEqual((1 << 18), cmods6.job_desc.reg)
            self.assertEqual(0, cmods6.reg_map.dac_vbat.reg)
            self.assertEqual(dac_reg_val, cmods6.reg_map.dac_vusb.reg)

            cmods6 = Cmods6()
            cmods6.set_source_current(Cmods6.ALL_CHANNELS, source_current)
            self.assertEqual((1 << 18) | (1 << 19), cmods6.job_desc.reg)
            self.assertEqual(dac_reg_val, cmods6.reg_map.dac_vbat.reg)
            self.assertEqual(dac_reg_val, cmods6.reg_map.dac_vusb.reg)
        # end for
    # end def test_set_source_current

    def test_set_serie_resistance(self):
        """
        Validate set_serie_resistance() method.
        """
        for source_current in self.VOLTAGES_RANGE:
            # Expected DAC register value
            dac_value = Dac.volt_to_dac_value(source_current)
            dac_reg_val = (0x2 << 20) | (0x3 << 16) | dac_value

            cmods6 = Cmods6()
            cmods6.set_serie_resistance(Cmods6.CHANNEL.BATTERY, source_current)
            self.assertEqual((1 << 19), cmods6.job_desc.reg)
            self.assertEqual(dac_reg_val, cmods6.reg_map.dac_vbat.reg)
            self.assertEqual(0, cmods6.reg_map.dac_vusb.reg)

            cmods6 = Cmods6()
            cmods6.set_serie_resistance(Cmods6.CHANNEL.USB, source_current)
            self.assertEqual((1 << 18), cmods6.job_desc.reg)
            self.assertEqual(0, cmods6.reg_map.dac_vbat.reg)
            self.assertEqual(dac_reg_val, cmods6.reg_map.dac_vusb.reg)

            cmods6 = Cmods6()
            cmods6.set_serie_resistance(Cmods6.ALL_CHANNELS, source_current)
            self.assertEqual((1 << 18) | (1 << 19), cmods6.job_desc.reg)
            self.assertEqual(dac_reg_val, cmods6.reg_map.dac_vbat.reg)
            self.assertEqual(dac_reg_val, cmods6.reg_map.dac_vusb.reg)
        # end for
    # end def test_set_serie_resistance

    def test_enable_output_voltage(self):
        """
        Validate enable_output_voltage() method.
        """
        for state in [0, 1, False, True]:
            # Expected SHIFTER register value
            shifter_reg = (int(state) << 8)

            cmods6 = Cmods6()
            cmods6.enable_output_voltage(Cmods6.CHANNEL.BATTERY, enable=state)
            self.assertEqual((1 << 17), cmods6.job_desc.reg)
            self.assertEqual(shifter_reg, cmods6.reg_map.shifter_bat.reg)
            self.assertEqual(0, cmods6.reg_map.shifter_usb.reg)

            cmods6 = Cmods6()
            cmods6.enable_output_voltage(Cmods6.CHANNEL.USB, enable=state)
            self.assertEqual((1 << 16), cmods6.job_desc.reg)
            self.assertEqual(0, cmods6.reg_map.dac_vbat.reg)
            self.assertEqual(shifter_reg, cmods6.reg_map.shifter_usb.reg)

            cmods6 = Cmods6()
            cmods6.enable_output_voltage(Cmods6.ALL_CHANNELS, enable=state)
            self.assertEqual((1 << 16) | (1 << 17), cmods6.job_desc.reg)
            self.assertEqual(shifter_reg, cmods6.reg_map.shifter_bat.reg)
            self.assertEqual(shifter_reg, cmods6.reg_map.shifter_usb.reg)
        # end for
    # end def test_enable_output_voltage

    def test_enable_voltage_feedback(self):
        """
        Validate enable_voltage_feedback() method.
        """
        for state in [0, 1, False, True]:
            # Expected SHIFTER register value
            shifter_reg = (int(state) << 9)

            cmods6 = Cmods6()
            cmods6.enable_voltage_feedback(Cmods6.CHANNEL.BATTERY, enable=state)
            self.assertEqual((1 << 17), cmods6.job_desc.reg)
            self.assertEqual(shifter_reg, cmods6.reg_map.shifter_bat.reg)
            self.assertEqual(0, cmods6.reg_map.shifter_usb.reg)

            cmods6 = Cmods6()
            cmods6.enable_voltage_feedback(Cmods6.CHANNEL.USB, enable=state)
            self.assertEqual((1 << 16), cmods6.job_desc.reg)
            self.assertEqual(0, cmods6.reg_map.dac_vbat.reg)
            self.assertEqual(shifter_reg, cmods6.reg_map.shifter_usb.reg)

            cmods6 = Cmods6()
            cmods6.enable_voltage_feedback(Cmods6.ALL_CHANNELS, enable=state)
            self.assertEqual((1 << 16) | (1 << 17), cmods6.job_desc.reg)
            self.assertEqual(shifter_reg, cmods6.reg_map.shifter_bat.reg)
            self.assertEqual(shifter_reg, cmods6.reg_map.shifter_usb.reg)
        # end for
    # end def test_enable_voltage_feedback

    def test_enable_current_sink(self):
        """
        Validate enable_current_sink() method.
        """
        for state in [0, 1, False, True]:
            cmods6 = Cmods6()
            cmods6.enable_current_sink(enable=state)
            self.assertEqual((1 << 17), cmods6.job_desc.reg)
            self.assertEqual((int(state) << 10), cmods6.reg_map.shifter_bat.reg)
            self.assertEqual(0, cmods6.reg_map.shifter_usb.reg)
        # end for
    # end def test_enable_current_sink

    def test_set_current_sink_channel(self):
        """
        Validate set_current_sink_channel() method.
        """
        cmods6 = Cmods6()
        cmods6.set_current_sink_channel(channel=Cmods6.CHANNEL.BATTERY)
        self.assertEqual((1 << 16), cmods6.job_desc.reg)
        self.assertEqual(0, cmods6.reg_map.shifter_bat.reg)
        self.assertEqual((1 << 10), cmods6.reg_map.shifter_usb.reg)

        cmods6 = Cmods6()
        cmods6.set_current_sink_channel(channel=Cmods6.CHANNEL.USB)
        self.assertEqual((1 << 16), cmods6.job_desc.reg)
        self.assertEqual(0, cmods6.reg_map.shifter_bat.reg)
        self.assertEqual((0 << 10), cmods6.reg_map.shifter_usb.reg)

        self.assertRaises(AssertionError, cmods6.set_current_sink_channel, Cmods6.ALL_CHANNELS)
        self.assertRaises(AssertionError, cmods6.set_current_sink_channel, Cmods6.CHANNEL(4))
    # end def test_set_current_sink_channel

    def test_is_valid_channel(self):
        """
        Validate is_channel_valid() and assert_channel_valid() methods.
        """
        cmods6 = Cmods6()
        self.assertFalse(cmods6.is_channel_valid(0))
        self.assertFalse(cmods6.is_channel_valid(Cmods6.CHANNEL(0)))
        self.assertTrue(cmods6.is_channel_valid(Cmods6.CHANNEL.BATTERY))
        self.assertTrue(cmods6.is_channel_valid(Cmods6.CHANNEL.USB))
        self.assertTrue(cmods6.is_channel_valid(Cmods6.CHANNEL.BATTERY | Cmods6.CHANNEL.USB))
        self.assertTrue(cmods6.is_channel_valid(Cmods6.ALL_CHANNELS))
        self.assertRaises(AssertionError, cmods6.assert_channel_valid, 8)
    # end def test_is_valid_channel
# end class Cmods6TestCase


@require_kosmos_device(DeviceName.CMODS6)
class Cmods6ManagerTestCase(KosmosCommonTestCase):
    """
    Kosmos CMODS6 Module Test Class
    """

    VOLTAGE_LIMIT = {
        Cmods6.CHANNEL.BATTERY: 4.5,  # Volts
        Cmods6.CHANNEL.USB: 5.2,  # Volts
    }

    @classmethod
    def setUpClass(cls):
        """
        Setup CMODS6 Manager instance
        """
        super().setUpClass()

        cls.kosmos.cmods6.set_max_voltage_limit(channels=Cmods6.CHANNEL.BATTERY,
                                                voltage=cls.VOLTAGE_LIMIT[Cmods6.CHANNEL.BATTERY])
        cls.kosmos.cmods6.set_max_voltage_limit(channels=Cmods6.CHANNEL.USB,
                                                voltage=cls.VOLTAGE_LIMIT[Cmods6.CHANNEL.USB])
    # end def setUpClass

    def tearDown(self):
        """
        Reset CMODS6 Manager instance
        """
        # Ensure Analog Module is reset after each test
        cmods6 = Cmods6()
        cmods6.reset_all()
        self.kosmos.cmods6.send(cmods6)

        super().tearDown()
    # end def tearDown

    def test_spec_demo(self):
        """
        Implement the demo code given as example in Analog Subsystem Communication Protocol document
        https://docs.google.com/document/d/12GwaeoYTcblNTBfYehJKWSYv9CKUgV0SaoWf1KIUYsU

        This demo applies to both BATTERY and USB channels.
        """
        channels = Cmods6.ALL_CHANNELS

        cmods6 = Cmods6()
        cmods6.reset_all()
        self.kosmos.cmods6.send(cmods6)

        cmods6 = Cmods6()
        cmods6.set_sink_current(channels=channels, current=Dac.MAX_VOLTAGE)
        cmods6.set_source_current(channels=channels, current=Dac.MAX_VOLTAGE)
        cmods6.set_output_voltage(channels=channels, voltage=0)
        self.kosmos.cmods6.send(cmods6)

        cmods6 = Cmods6()
        cmods6.enable_output_voltage(channels=channels, enable=True)
        self.kosmos.cmods6.send(cmods6)

        cmods6 = Cmods6()
        cmods6.set_output_voltage(channels=channels, voltage=1.0)
        self.kosmos.cmods6.send(cmods6)

        #######################################
        # Measure output voltage manually with a voltmeter, expect 1 Volt
        sleep(3)
        #######################################
    # end def test_spec_demo

    def test_voltage_ramp_up(self):
        """
        Implement a DAC voltage ramp up, on USB channel.

        The voltage ramp will not go above voltage limit, to protect the DUT.
        """
        voltage_limit_channel = Cmods6.CHANNEL.BATTERY
        voltage_ramp = [i/10 for i in range(ceil(self.VOLTAGE_LIMIT[voltage_limit_channel] * 10))]\
                        + [self.VOLTAGE_LIMIT[voltage_limit_channel]]

        channel = Cmods6.CHANNEL.USB

        cmods6 = Cmods6()
        cmods6.reset_all()
        self.kosmos.cmods6.send(cmods6)

        cmods6 = Cmods6()
        cmods6.set_sink_current(channels=channel, current=Dac.MAX_VOLTAGE)
        cmods6.set_source_current(channels=channel, current=Dac.MAX_VOLTAGE)
        cmods6.set_output_voltage(channels=channel, voltage=0)
        self.kosmos.cmods6.send(cmods6)

        cmods6 = Cmods6()
        cmods6.enable_output_voltage(channels=channel, enable=True)
        self.kosmos.cmods6.send(cmods6)

        for dac_volt in voltage_ramp:
            cmods6 = Cmods6()
            print(f'{dac_volt} Volts')
            cmods6.set_output_voltage(channels=channel, voltage=dac_volt)
            self.kosmos.cmods6.send(cmods6)
            sleep(0.1)
        # end for

        #######################################
        # Measure output voltage manually with a voltmeter, expect 1 Volt
        sleep(3)
        #######################################

        # Reset DAC before exiting the test
        cmods6 = Cmods6()
        cmods6.reset_all()
        self.kosmos.cmods6.send(cmods6)
    # end def test_voltage_ramp_up

    def test_set_max_voltage_limit(self):
        """
        Test output voltage cannot be set above voltage limit.

        This test does not use the hardware, so there is no risk to damage the DUT.
        """
        for channel in Cmods6.CHANNEL:
            cmods6_manager = Cmods6Manager()

            # Test default constructor value
            self.assertEqual(Dac.MAX_VOLTAGE, cmods6_manager.get_max_voltage_limit(channel), 'Wrong default limit value')
            cmods6 = Cmods6()
            cmods6_manager.assert_safety_checks(cmods6.reg_map)

            # Test upmost limit
            cmods6_manager.set_max_voltage_limit(channels=channel, voltage=Dac.MAX_VOLTAGE)
            cmods6.set_output_voltage(channels=channel, voltage=Dac.MAX_VOLTAGE)
            cmods6_manager.assert_safety_checks(cmods6.reg_map)

            # Test lowest limit
            cmods6_manager.set_max_voltage_limit(channels=channel, voltage=0)
            cmods6.set_output_voltage(channels=channel, voltage=0)
            cmods6_manager.assert_safety_checks(cmods6.reg_map)

            # Test setting a voltage (5V) above the voltage limit (4.5V)
            cmods6_manager.set_max_voltage_limit(channels=channel, voltage=4.5)
            cmods6.set_output_voltage(channels=channel, voltage=5)
            with self.assertRaisesRegex(AssertionError, r'is set above limit'):
                cmods6_manager.assert_safety_checks(cmods6.reg_map)
            # end with

            # Test setting a voltage (4V) below the voltage limit (4.5V)
            cmods6_manager.set_max_voltage_limit(channels=channel, voltage=4.5)
            cmods6.set_output_voltage(channels=channel, voltage=4)
            cmods6_manager.assert_safety_checks(cmods6.reg_map)
        # end for
    # end def test_set_max_voltage_limit
# end class Cmods6ManagerTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
