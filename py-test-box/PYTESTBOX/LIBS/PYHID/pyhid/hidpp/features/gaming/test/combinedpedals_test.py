#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.gaming.test.combinedpedals_test
:brief: HID++ 2.0 ``CombinedPedals`` test module
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/02/25
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.gaming.combinedpedals import CombinedPedals
from pyhid.hidpp.features.gaming.combinedpedals import CombinedPedalsChangedEvent
from pyhid.hidpp.features.gaming.combinedpedals import CombinedPedalsFactory
from pyhid.hidpp.features.gaming.combinedpedals import CombinedPedalsV0
from pyhid.hidpp.features.gaming.combinedpedals import GetCombinedPedals
from pyhid.hidpp.features.gaming.combinedpedals import GetCombinedPedalsResponse
from pyhid.hidpp.features.gaming.combinedpedals import SetCombinedPedals
from pyhid.hidpp.features.gaming.combinedpedals import SetCombinedPedalsResponse
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class CombinedPedalsInstantiationTestCase(TestCase):
    """
    ``CombinedPedals`` testing classes instantiations
    """
    @staticmethod
    def test_combined_pedals():
        """
        Tests ``CombinedPedals`` class instantiation
        """
        my_class = CombinedPedals(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = CombinedPedals(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_combined_pedals

    @staticmethod
    def test_get_combined_pedals():
        """
        Tests ``GetCombinedPedals`` class instantiation
        """
        my_class = GetCombinedPedals(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetCombinedPedals(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_combined_pedals

    @staticmethod
    def test_get_combined_pedals_response():
        """
        Tests ``GetCombinedPedalsResponse`` class instantiation
        """
        my_class = GetCombinedPedalsResponse(device_index=0, feature_index=0,
                                             combined_pedals_enabled=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCombinedPedalsResponse(device_index=0xff, feature_index=0xff,
                                             combined_pedals_enabled=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_combined_pedals_response

    @staticmethod
    def test_set_combined_pedals():
        """
        Tests ``SetCombinedPedals`` class instantiation
        """
        my_class = SetCombinedPedals(device_index=0, feature_index=0,
                                     enable_combined_pedals=False)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetCombinedPedals(device_index=0xff, feature_index=0xff,
                                     enable_combined_pedals=True)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_combined_pedals

    @staticmethod
    def test_set_combined_pedals_response():
        """
        Tests ``SetCombinedPedalsResponse`` class instantiation
        """
        my_class = SetCombinedPedalsResponse(device_index=0, feature_index=0,
                                             combined_pedals_enabled=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetCombinedPedalsResponse(device_index=0xff, feature_index=0xff,
                                             combined_pedals_enabled=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_combined_pedals_response

    @staticmethod
    def test_combined_pedals_changed_event():
        """
        Tests ``CombinedPedalsChangedEvent`` class instantiation
        """
        my_class = CombinedPedalsChangedEvent(device_index=0, feature_index=0,
                                              combined_pedals_enabled=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = CombinedPedalsChangedEvent(device_index=0xff, feature_index=0xff,
                                              combined_pedals_enabled=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_combined_pedals_changed_event
# end class CombinedPedalsInstantiationTestCase


class CombinedPedalsTestCase(TestCase):
    """
    ``CombinedPedals`` factory testing
    """
    @classmethod
    def setUpClass(cls):
        cls.expected = {
            CombinedPedalsV0.VERSION: {
                "cls": CombinedPedalsV0,
                "interfaces": {
                    "get_combined_pedals_cls": GetCombinedPedals,
                    "get_combined_pedals_response_cls": GetCombinedPedalsResponse,
                    "set_combined_pedals_cls": SetCombinedPedals,
                    "set_combined_pedals_response_cls": SetCombinedPedalsResponse,
                    "combined_pedals_changed_event_cls": CombinedPedalsChangedEvent,
                },
                "max_function_index": 1
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Tests ``CombinedPedalsFactory``
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(CombinedPedalsFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Tests ``CombinedPedalsFactory`` with out of range versions
        """
        for version in [1, 2]:
            with self.assertRaises(KeyError):
                CombinedPedalsFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``CombinedPedalsFactory`` returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            obj = CombinedPedalsFactory.create(version)
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
            obj = CombinedPedalsFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class CombinedPedalsTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
