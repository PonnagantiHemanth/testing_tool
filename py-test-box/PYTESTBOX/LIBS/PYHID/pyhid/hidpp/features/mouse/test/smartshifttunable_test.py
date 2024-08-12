#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.mouse.test.smartshifttunable_test
:brief: HID++ 2.0 SmartShift 3G/EPM wheel with tunable torque feature test module
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/02/17
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.mouse.smartshifttunable import GetCapabilitiesResponseV0
from pyhid.hidpp.features.mouse.smartshifttunable import GetCapabilitiesV0
from pyhid.hidpp.features.mouse.smartshifttunable import GetRatchetControlModeResponseV0
from pyhid.hidpp.features.mouse.smartshifttunable import GetRatchetControlModeV0
from pyhid.hidpp.features.mouse.smartshifttunable import SetRatchetControlModeResponseV0
from pyhid.hidpp.features.mouse.smartshifttunable import SetRatchetControlModeV0
from pyhid.hidpp.features.mouse.smartshifttunable import SmartShiftTunable
from pyhid.hidpp.features.mouse.smartshifttunable import SmartShiftTunableFactory
from pyhid.hidpp.features.mouse.smartshifttunable import SmartShiftTunableV0
from pyhid.hidpp.features.test.root_test import RootTestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class SmartShiftTunableInstantiationTestCase(TestCase):
    """
    SmartShiftTunable testing classes instantiations
    """
    @staticmethod
    def test_smart_shift_tunable():
        """
        Test SmartShiftTunable class instantiation
        """
        my_class = SmartShiftTunable(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = SmartShiftTunable(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_smart_shift_tunable

    @staticmethod
    def test_get_capabilities_v0():
        """
        Test GetCapabilitiesV0 class instantiation
        """
        my_class = GetCapabilitiesV0(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetCapabilitiesV0(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_capabilities_v0

    @staticmethod
    def test_get_capabilities_response_v0():
        """
        Test GetCapabilitiesResponseV0 class instantiation
        """
        my_class = GetCapabilitiesResponseV0(device_index=0,
                                             feature_index=0,
                                             tunable_torque=0,
                                             auto_disengage_default=0,
                                             default_tunable_torque=0,
                                             max_force=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCapabilitiesResponseV0(device_index=0xFF,
                                             feature_index=0xFF,
                                             tunable_torque=0x01,
                                             auto_disengage_default=0xFF,
                                             default_tunable_torque=0xFF,
                                             max_force=0xFF)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCapabilitiesResponseV0(device_index=0,
                                             feature_index=0,
                                             tunable_torque=False,
                                             auto_disengage_default=0,
                                             default_tunable_torque=0,
                                             max_force=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCapabilitiesResponseV0(device_index=0xFF,
                                             feature_index=0xFF,
                                             tunable_torque=True,
                                             auto_disengage_default=0xFF,
                                             default_tunable_torque=0xFF,
                                             max_force=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_capabilities_response_v0

    @staticmethod
    def test_get_ratchet_control_mode_v0():
        """
        Test GetRatchetControlModeV0 class instantiation
        """
        my_class = GetRatchetControlModeV0(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetRatchetControlModeV0(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_ratchet_control_mode_v0

    @staticmethod
    def test_get_ratchet_control_mode_response_v0():
        """
        Test GetRatchetControlModeResponseV0 class instantiation
        """
        my_class = GetRatchetControlModeResponseV0(
            device_index=0x00, feature_index=0x00, wheel_mode=0x00, auto_disengage=0x00, current_tunable_torque=0x00)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetRatchetControlModeResponseV0(
            device_index=0xFF, feature_index=0xFF, wheel_mode=0xFF, auto_disengage=0xFF, current_tunable_torque=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_ratchet_control_mode_response_v0

    @staticmethod
    def test_set_ratchet_control_mode_v0():
        """
        Test SetRatchetControlModeV0 class instantiation
        """
        my_class = SetRatchetControlModeV0(
            device_index=0, feature_index=0, wheel_mode=0, auto_disengage=0, current_tunable_torque=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetRatchetControlModeV0(
            device_index=0xFF, feature_index=0xFF, wheel_mode=0xFF, auto_disengage=0xFF, current_tunable_torque=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_ratchet_control_mode_v0

    @staticmethod
    def test_set_ratchet_control_mode_response_v0():
        """
        Test SetRatchetControlModeResponseV0 class instantiation
        """
        my_class = SetRatchetControlModeResponseV0(
            device_index=0x00, feature_index=0x00, wheel_mode=0x00, auto_disengage=0x00, current_tunable_torque=0x00)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRatchetControlModeResponseV0(
            device_index=0xFF, feature_index=0xFF, wheel_mode=0xFF, auto_disengage=0xFF, current_tunable_torque=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_ratchet_control_mode_response_v0
# end class SmartShiftTunableInstantiationTestCase


class SmartShiftTunableTestCase(TestCase):
    """
    Device information factory testing
    """
    @classmethod
    def setUpClass(cls):
        cls.expected = {
            0: {
                "cls": SmartShiftTunableV0,
                "interfaces": {
                    "get_capabilities_cls": GetCapabilitiesV0,
                    "get_capabilities_response_cls": GetCapabilitiesResponseV0,
                    "get_ratchet_control_mode_cls": GetRatchetControlModeV0,
                    "get_ratchet_control_mode_response_cls": GetRatchetControlModeResponseV0,
                    "set_ratchet_control_mode_cls": SetRatchetControlModeV0,
                    "set_ratchet_control_mode_response_cls": SetRatchetControlModeResponseV0,
                },
                "max_function_index": 2
            },
        }
    # end def setUpClass

    def test_smart_shift_tunable_factory(self):
        """
        Tests SmartShiftTunable factory
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(SmartShiftTunableFactory.create(version)), expected["cls"])
        # end for
    # end def test_smart_shift_tunable_factory

    def test_smart_shift_tunable_factory_version_out_of_range(self):
        """
        Tests SmartShiftTunableFactory with out of range versions
        """
        for version in [1]:
            with self.assertRaises(KeyError):
                SmartShiftTunableFactory.create(version)
            # end with
        # end for
    # end def test_smart_shift_tunable_factory_version_out_of_range

    def test_smart_shift_tunable_factory_interfaces(self):
        """
        Check SmartShiftTunableFactory returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            device_information = SmartShiftTunableFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(device_information, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(device_information, interface)
                    # end with
                # end if
            # end for
        # end for
    # end def test_smart_shift_tunable_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check get_max_function_index returns correct value at each version
        """
        for version, expected in self.expected.items():
            device_information = SmartShiftTunableFactory.create(version)
            self.assertEqual(device_information.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class SmartShiftTunableTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
