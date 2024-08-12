#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.feature.common.test.securedfucontrol_test
    :brief: HID++ 2.0 Secure Dfu Control test module
    :author: Christophe Roquebert
    :date:   2020/05/19
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList
from pyhid.hidpp.features.common.securedfucontrol import SecureDfuControlFactory
from pyhid.hidpp.features.common.securedfucontrol import SecureDfuControlV0
from pyhid.hidpp.features.common.securedfucontrol import SecureDfuControlV1
from pyhid.hidpp.features.common.securedfucontrol import SecureDfuControl
from pyhid.hidpp.features.common.securedfucontrol import GetDfuControlV0
from pyhid.hidpp.features.common.securedfucontrol import GetDfuControlResponseV0
from pyhid.hidpp.features.common.securedfucontrol import SetDfuControlV0
from pyhid.hidpp.features.common.securedfucontrol import SetDfuControlResponseV0
from pyhid.hidpp.features.test.root_test import RootTestCase
from unittest import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class SecureDfuControlInstantiationTestCase(TestCase):
    """
    SecureDfuControl testing class
    """

    @staticmethod
    def test_secure_dfu_control():
        """
        Tests SecureDfuControl class instantiation
        """
        my_class = SecureDfuControl(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = SecureDfuControl(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_secure_dfu_control

    @staticmethod
    def test_get_dfu_control():
        """
        Tests GetDfuControl class instantiation
        """
        my_class = GetDfuControlV0(device_index=0x00, feature_index=0x00)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetDfuControlV0(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_dfu_control

    @staticmethod
    def test_get_dfu_control_response():
        """
        Tests GetDfuControlResponse class instantiation
        """
        my_class = GetDfuControlResponseV0(
            device_index=0x00,
            feature_index=0x00,
            enable_dfu=False,
            dfu_control_param=0x00,
            dfu_control_timeout=0x00,
            dfu_control_action_type=0x00,
            dfu_control_action_data=HexList("000000")
        )

        RootTestCase._long_function_class_checker(my_class)

        # Test alias
        my_class = GetDfuControlResponseV0(
            device_index=0x00,
            feature_index=0x00,
            enter_dfu=False,
            dfu_control_param=0x00,
            dfu_control_timeout=0x00,
            dfu_control_action_type=0x00,
            dfu_control_action_data=HexList("000000")
        )

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetDfuControlResponseV0(
            device_index=0xFF,
            feature_index=0xFF,
            enable_dfu=True,
            dfu_control_param=0xFF,
            dfu_control_timeout=0xFF,
            dfu_control_action_type=0xFF,
            dfu_control_action_data=HexList("FFFFFF")
        )

        RootTestCase._long_function_class_checker(my_class)

        # Test alias
        my_class = GetDfuControlResponseV0(
            device_index=0xFF,
            feature_index=0xFF,
            enter_dfu=True,
            dfu_control_param=0xFF,
            dfu_control_timeout=0xFF,
            dfu_control_action_type=0xFF,
            dfu_control_action_data=HexList("FFFFFF")
        )

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_dfu_control_response

    @staticmethod
    def test_set_dfu_control():
        """
        Tests SetDfuControl class instantiation
        """
        my_class = SetDfuControlV0(device_index=0x00, feature_index=0x00, enable_dfu=False, dfu_control_param=0x00,
                                   dfu_magic_key=0x00)

        RootTestCase._long_function_class_checker(my_class)

        # Test alias
        my_class = SetDfuControlV0(device_index=0x00, feature_index=0x00, enter_dfu=False, dfu_control_param=0x00,
                                   dfu_magic_key=0x00)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetDfuControlV0(device_index=0xFF, feature_index=0xFF, enable_dfu=True, dfu_control_param=0xFF,
                                   dfu_magic_key=0xFFFFFF)

        RootTestCase._long_function_class_checker(my_class)

        # Test alias
        my_class = SetDfuControlV0(device_index=0xFF, feature_index=0xFF, enter_dfu=True, dfu_control_param=0xFF,
                                   dfu_magic_key=0xFFFFFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_dfu_control

    @staticmethod
    def test_set_dfu_control_response():
        """
        Tests SetDfuControlResponse class instantiation
        """
        my_class = SetDfuControlResponseV0(
            device_index=0x00,
            feature_index=0x00
        )

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetDfuControlResponseV0(
            device_index=0xFF,
            feature_index=0xFF
        )

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_dfu_control_response
# end class SecureDfuControlInstantiationTestCase


class SecureDfuControlTestCase(TestCase):
    """
    Secure Dfu Control factory testing
    """

    @classmethod
    def setUpClass(cls):
        cls.expected = {
            SecureDfuControlV0.VERSION: {
                "cls": SecureDfuControlV0,
                "interfaces": {
                    "get_dfu_control_cls": GetDfuControlV0,
                    "set_dfu_control_cls": SetDfuControlV0,
                },
                "max_function_index": 1
            },
            SecureDfuControlV1.VERSION: {
                "cls": SecureDfuControlV1,
                "interfaces": {
                    "get_dfu_control_cls": GetDfuControlV0,
                    "set_dfu_control_cls": SetDfuControlV0,
                },
                "max_function_index": 1
            },
        }
    # end def setUpClass

    def test_secure_dfu_control_factory(self):
        """
        Tests Secure Dfu Control Factory
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(SecureDfuControlFactory.create(version)), expected["cls"])
        # end for loop
    # end def test_secure_dfu_control_factory

    def test_secure_dfu_control_factory_version_out_of_range(self):
        """
        Tests Secure Dfu Control Factory with, out of range versions
        """
        for version in [2, 3, 4]:
            with self.assertRaises(KeyError):
                SecureDfuControlFactory.create(version)
            # end with
        # end for
    # end def test_secure_dfu_control_factory_version_out_of_range

    def test_secure_dfu_control_factory_interfaces(self):
        """
        Check Secure Dfu Control Factory returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            secure_dfu_control = SecureDfuControlFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(secure_dfu_control, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(secure_dfu_control, interface)
                # end if
            # end for loop
        # end for loop
    # end def test_secure_dfu_control_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check get_max_function_index returns correct value at each version
        """
        for version, expected in self.expected.items():
            secure_dfu_control = SecureDfuControlFactory.create(version)
            self.assertEqual(secure_dfu_control.get_max_function_index(), expected["max_function_index"])
        # end for loop
    # end def test_get_max_function_index
# end class SecureDfuControlTestCase


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
