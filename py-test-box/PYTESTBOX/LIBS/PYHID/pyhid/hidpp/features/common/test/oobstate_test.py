#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pyhid.hidpp.features.common.test.oobstate_test
:brief: HID++ 2.0 ``OobState`` test module
:author: Sanjib Hazra <shazra@logitech.com>
:date: 2022/03/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.common.oobstate import OobState
from pyhid.hidpp.features.common.oobstate import OobStateFactory
from pyhid.hidpp.features.common.oobstate import OobStateV0
from pyhid.hidpp.features.common.oobstate import SetOobState
from pyhid.hidpp.features.common.oobstate import SetOobStateResponse
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class OobStateInstantiationTestCase(TestCase):
    """
    Test ``OobState`` testing classes instantiations
    """

    @staticmethod
    def test_oob_state():
        """
        Test ``OobState`` class instantiation
        """
        my_class = OobState(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = OobState(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_oob_state

    @staticmethod
    def test_set_oob_state():
        """
        Test ``SetOobState`` class instantiation
        """
        my_class = SetOobState(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetOobState(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_oob_state

    @staticmethod
    def test_set_oob_state_response():
        """
        Test ``SetOobStateResponse`` class instantiation
        """
        my_class = SetOobStateResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetOobStateResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_oob_state_response
# end class OobStateInstantiationTestCase


class OobStateTestCase(TestCase):
    """
    Test ``OobState`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            OobStateV0.VERSION: {
                "cls": OobStateV0,
                "interfaces": {
                    "set_oob_state_cls": SetOobState,
                    "set_oob_state_response_cls": SetOobStateResponse,
                },
                "max_function_index": 0
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Test ``OobStateFactory``
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(OobStateFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``OobStateFactory`` using out of range versions
        """
        for version in [1, 2]:
            with self.assertRaises(KeyError):
                OobStateFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``OobStateFactory`` returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            obj = OobStateFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(obj, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(obj, interface)
                    # end with
                # end if
            # end for
        # end for
    # end def test_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check ``get_max_function_index`` returns correct value at each version
        """
        for version, expected in self.expected.items():
            obj = OobStateFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class OobStateTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
