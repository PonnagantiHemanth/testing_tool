#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.feature.common.test.powermodes_test
:brief: HID++ 2.0 PowerModes test module
:author: Stanislas Cottard
:date: 2019/04/04
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidpp.features.common.powermodes import PowerModes
from pyhid.hidpp.features.common.powermodes import PowerModesFactory
from pyhid.hidpp.features.common.powermodes import PowerModesV0
from pyhid.hidpp.features.common.powermodes import GetPowerModesTotalNumber
from pyhid.hidpp.features.common.powermodes import GetPowerModesTotalNumberResponse
from pyhid.hidpp.features.common.powermodes import SetPowerMode
from pyhid.hidpp.features.common.powermodes import SetPowerModeResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from unittest import TestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class PowerModesInstantiationTestCase(TestCase):
    """
    PowerModes testing class
    """
    @staticmethod
    def test_power_modes():
        """
        Tests PowerModes class instantiation
        """
        my_class = PowerModes(device_index=0,
                              feature_index=0)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_power_modes

    @staticmethod
    def test_get_power_modes_total_number():
        """
        Tests GetPowerModesTotalNumber class instantiation
        """
        my_class = GetPowerModesTotalNumber(device_index=0,
                                            feature_index=0)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_power_modes_total_number

    @staticmethod
    def test_set_power_mode():
        """
        Tests SetPowerMode class instantiation
        """
        my_class = SetPowerMode(device_index=0,
                                feature_index=0,
                                power_mode_number=0)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_power_mode

    @staticmethod
    def test_get_power_modes_total_number_response():
        """
        Tests GetPowerModesTotalNumberResponse class instantiation
        """
        my_class = GetPowerModesTotalNumberResponse(device_index=0,
                                                    feature_index=0,
                                                    total_number_of_power_modes=1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_power_modes_total_number_response

    @staticmethod
    def test_set_power_mode_response():
        """
        Tests SetPowerModeResponse class instantiation
        """
        my_class = SetPowerModeResponse(device_index=0,
                                        feature_index=0,
                                        power_mode_number=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_power_mode_response
# end class PowerModesInstantiationTestCase


class PowerModesTestCase(TestCase):
    """
    ``Power Modes`` factory model testing class
    """
    @classmethod
    def setUpClass(cls):
        cls.expected = {
            0: {
                "cls": PowerModesV0,
                "interfaces": {
                    "get_power_modes_total_number_cls": GetPowerModesTotalNumber,
                    "get_power_modes_total_number_response_cls": GetPowerModesTotalNumberResponse,
                    "set_power_mode_cls": SetPowerMode,
                    "set_power_mode_response_cls": SetPowerModeResponse,
                },
                "max_function_index": 1
            },
        }
    # end def setUpClass

    def test_power_modes_factory(self):
        """
        Test power modes Factory.
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(PowerModesFactory.create(version)), expected["cls"])
        # end for loop
    # end def test_power_modes_factory

    def test_power_modes_factory_version_out_of_range(self):
        """
        Test power modes Factory with out of range versions.
        """
        for version in [1, 2, 3]:
            with self.assertRaises(KeyError):
                PowerModesFactory.create(version)
            # end with
        # end for
    # end def test_power_modes_factory_version_out_of_range

    def test_power_modes_factory_interfaces(self):
        """
        Check the power modes factory returns its expected interfaces.
        """
        for version, cls_map in self.expected.items():
            power_modes = PowerModesFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(power_modes, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(power_modes, interface)
                # end if
            # end for loop
        # end for loop
    # end def test_power_modes_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check get_max_function_index returns correct value at each version.
        """
        for version, expected in self.expected.items():
            power_modes = PowerModesFactory.create(version)
            self.assertEqual(power_modes.get_max_function_index(), expected["max_function_index"])
        # end for loop
    # end def test_get_max_function_index
# end class PowerModesTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
