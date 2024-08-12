#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.feature.common.test.forcepairing_test
:brief: HID++ 2.0 ForcePairing test module
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/05/07
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidpp.features.common.forcepairing import ForcePairing
from pyhid.hidpp.features.common.forcepairing import ForcePairingFactory
from pyhid.hidpp.features.common.forcepairing import ForcePairingV0
from pyhid.hidpp.features.common.forcepairing import ForcePairingTimeoutEvent
from pyhid.hidpp.features.common.forcepairing import GetCapabilities
from pyhid.hidpp.features.common.forcepairing import GetCapabilitiesResponse
from pyhid.hidpp.features.common.forcepairing import SetForcePairing
from pyhid.hidpp.features.common.forcepairing import SetForcePairingResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList
from unittest import TestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ForcePairingInstantiationTestCase(TestCase):
    """
    ForcePairing testing class
    """
    @staticmethod
    def test_force_pairing():
        """
        Tests ForcePairing class instantiation
        """
        my_class = ForcePairing(device_index=0,
                                feature_index=0)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_force_pairing

    @staticmethod
    def test_get_capabilities():
        """
        Tests GetCapabilities class instantiation
        """
        my_class = GetCapabilities(device_index=0, feature_index=0)
        RootTestCase._short_function_class_checker(my_class)

        my_class = GetCapabilities(device_index=0xFF, feature_index=0xFF)
        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_capabilities

    @staticmethod
    def test_set_force_pairing():
        """
        Tests SetForcePairing class instantiation
        """
        my_class = SetForcePairing(device_index=0, feature_index=0, pairing_address=HexList(
            '00'*(SetForcePairing.LEN.PAIRING_ADDRESS//8)))
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetForcePairing(device_index=0xFF, feature_index=0xFF, pairing_address=HexList(
            'FF'*(SetForcePairing.LEN.PAIRING_ADDRESS//8)))
        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_force_pairing

    @staticmethod
    def test_get_capabilities_response():
        """
        Tests GetForcePairingTotalNumberResponse class instantiation
        """
        my_class = GetCapabilitiesResponse(device_index=0, feature_index=0, force_pairing_timeout=0, 
                                           force_pairing_action_type=0)
        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCapabilitiesResponse(device_index=0xFF, feature_index=0xFF, force_pairing_timeout=0xFF, 
                                           force_pairing_action_type=0xFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_capabilities_response

    @staticmethod
    def test_set_force_pairing_response():
        """
        Tests SetForcePairingResponse class instantiation
        """
        my_class = SetForcePairingResponse(device_index=0, feature_index=0)
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetForcePairingResponse(device_index=0xFF, feature_index=0xFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_force_pairing_response

    @staticmethod
    def test_force_pairing_timeout_event():
        """
        Tests ForcePairingTimeoutEvent class instantiation
        """
        my_class = ForcePairingTimeoutEvent(device_index=0, feature_index=0)
        RootTestCase._long_function_class_checker(my_class)

        my_class = ForcePairingTimeoutEvent(device_index=0xFF, feature_index=0xFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_force_pairing_timeout_event
# end class ForcePairingInstantiationTestCase


class ForcePairingTestCase(TestCase):
    """
    ``Power Modes`` factory model testing class
    """
    @classmethod
    def setUpClass(cls):
        cls.expected = {
            0: {
                "cls": ForcePairingV0,
                "interfaces": {
                    "get_capabilities_cls": GetCapabilities,
                    "get_capabilities_response_cls": GetCapabilitiesResponse,
                    "set_force_pairing_cls": SetForcePairing,
                    "set_force_pairing_response_cls": SetForcePairingResponse,
                    "force_pairing_timeout_event_cls": ForcePairingTimeoutEvent,
                },
                "max_function_index": 1
            },
        }
    # end def setUpClass

    def test_force_pairing_factory(self):
        """
        Test force pairing Factory.
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(ForcePairingFactory.create(version)), expected["cls"])
        # end for loop
    # end def test_force_pairing_factory

    def test_force_pairing_factory_version_out_of_range(self):
        """
        Test force pairing Factory with out of range versions.
        """
        for version in [1, 2, 3]:
            with self.assertRaises(KeyError):
                ForcePairingFactory.create(version)
            # end with
        # end for
    # end def test_force_pairing_factory_version_out_of_range

    def test_force_pairing_factory_interfaces(self):
        """
        Check the force pairing factory returns its expected interfaces.
        """
        for version, cls_map in self.expected.items():
            force_pairing = ForcePairingFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(force_pairing, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(force_pairing, interface)
                # end if
            # end for loop
        # end for loop
    # end def test_force_pairing_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check get_max_function_index returns correct value at each version.
        """
        for version, expected in self.expected.items():
            force_pairing = ForcePairingFactory.create(version)
            self.assertEqual(force_pairing.get_max_function_index(), expected["max_function_index"])
        # end for loop
    # end def test_get_max_function_index
# end class ForcePairingTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
