#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.gaming.test.pedalstatus_test
:brief: HID++ 2.0 ``PedalStatus`` test module
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/02/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.gaming.pedalstatus import GetPedalStatus
from pyhid.hidpp.features.gaming.pedalstatus import GetPedalStatusResponse
from pyhid.hidpp.features.gaming.pedalstatus import PedalStatus
from pyhid.hidpp.features.gaming.pedalstatus import PedalStatusFactory
from pyhid.hidpp.features.gaming.pedalstatus import PedalStatusV0
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PedalStatusInstantiationTestCase(TestCase):
    """
    Test ``PedalStatus`` testing classes instantiations
    """

    @staticmethod
    def test_pedal_status():
        """
        Test ``PedalStatus`` class instantiation
        """
        my_class = PedalStatus(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = PedalStatus(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_pedal_status

    @staticmethod
    def test_get_pedal_status():
        """
        Test ``GetPedalStatus`` class instantiation
        """
        my_class = GetPedalStatus(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetPedalStatus(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_pedal_status

    @staticmethod
    def test_get_pedal_status_response():
        """
        Test ``GetPedalStatusResponse`` class instantiation
        """
        my_class = GetPedalStatusResponse(device_index=0, feature_index=0,
                                          entry_count=0,
                                          entry_1_port_type=0,
                                          entry_1_port_status=0,
                                          entry_2_port_type=0,
                                          entry_2_port_status=0,
                                          entry_3_port_type=0,
                                          entry_3_port_status=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetPedalStatusResponse(device_index=0xff, feature_index=0xff,
                                          entry_count=0xff,
                                          entry_1_port_type=0xff,
                                          entry_1_port_status=0xff,
                                          entry_2_port_type=0xff,
                                          entry_2_port_status=0xff,
                                          entry_3_port_type=0xff,
                                          entry_3_port_status=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_pedal_status_response
# end class PedalStatusInstantiationTestCase


class PedalStatusTestCase(TestCase):
    """
    Test ``PedalStatus`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        cls.expected = {
            PedalStatusV0.VERSION: {
                "cls": PedalStatusV0,
                "interfaces": {
                    "get_pedal_status_cls": GetPedalStatus,
                    "get_pedal_status_response_cls": GetPedalStatusResponse,
                },
                "max_function_index": 0
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Test ``PedalStatusFactory``
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(PedalStatusFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``PedalStatusFactory`` with out of range versions
        """
        for version in [1, 2]:
            with self.assertRaises(KeyError):
                PedalStatusFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``PedalStatusFactory`` returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            obj = PedalStatusFactory.create(version)
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
            obj = PedalStatusFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class PedalStatusTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
