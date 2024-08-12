#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.gaming.test.gaminggkeys_test
:brief: HID++ 2.0 ``GamingGKeys`` test module
:author: Gautham S B <gsb@logitech.com>
:date: 2023/11/17
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.gaming.gaminggkeys import EnableSoftwareControl
from pyhid.hidpp.features.gaming.gaminggkeys import EnableSoftwareControlResponse
from pyhid.hidpp.features.gaming.gaminggkeys import GamingGKeys
from pyhid.hidpp.features.gaming.gaminggkeys import GamingGKeysFactory
from pyhid.hidpp.features.gaming.gaminggkeys import GamingGKeysV0
from pyhid.hidpp.features.gaming.gaminggkeys import GetCount
from pyhid.hidpp.features.gaming.gaminggkeys import GetCountResponse
from pyhid.hidpp.features.gaming.gaminggkeys import GetPhysicalLayout
from pyhid.hidpp.features.gaming.gaminggkeys import GetPhysicalLayoutResponse
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class GamingGKeysInstantiationTestCase(TestCase):
    """
    Test ``GamingGKeys`` testing classes instantiations
    """

    @staticmethod
    def test_gaming_g_keys():
        """
        Test ``GamingGKeys`` class instantiation
        """
        my_class = GamingGKeys(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = GamingGKeys(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_gaming_g_keys

    @staticmethod
    def test_getcount():
        """
        Test ``GetCount`` class instantiation
        """
        my_class = GetCount(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetCount(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_getcount

    @staticmethod
    def test_getphysicallayout():
        """
        Test ``GetPhysicalLayout`` class instantiation
        """
        my_class = GetPhysicalLayout(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetPhysicalLayout(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_getphysicallayout

    @staticmethod
    def test_enablesoftwarecontrol():
        """
        Test ``EnableSoftwareControl`` class instantiation
        """
        my_class = EnableSoftwareControl(device_index=0, feature_index=0,
                                         enable=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = EnableSoftwareControl(device_index=0xFF, feature_index=0xFF,
                                         enable=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_enablesoftwarecontrol

    @staticmethod
    def test_getcount_response():
        """
        Test ``GetCountResponse`` class instantiation
        """
        my_class = GetCountResponse(device_index=0, feature_index=0,
                                    nbbuttons=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCountResponse(device_index=0xFF, feature_index=0xFF,
                                    nbbuttons=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_getcount_response

    @staticmethod
    def test_getphysicallayout_response():
        """
        Test ``GetPhysicalLayoutResponse`` class instantiation
        """
        my_class = GetPhysicalLayoutResponse(device_index=0, feature_index=0,
                                             gkeylayout=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetPhysicalLayoutResponse(device_index=0xFF, feature_index=0xFF,
                                             gkeylayout=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_getphysicallayout_response

    @staticmethod
    def test_enablesoftwarecontrol_response():
        """
        Test ``EnableSoftwareControlResponse`` class instantiation
        """
        my_class = EnableSoftwareControlResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = EnableSoftwareControlResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_enablesoftwarecontrol_response
# end class GamingGKeysInstantiationTestCase


class GamingGKeysTestCase(TestCase):
    """
    Test ``GamingGKeys`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            GamingGKeysV0.VERSION: {
                "cls": GamingGKeysV0,
                "interfaces": {
                    "get_count_cls": GetCount,
                    "get_count_response_cls": GetCountResponse,
                    "get_physical_layout_cls": GetPhysicalLayout,
                    "get_physical_layout_response_cls": GetPhysicalLayoutResponse,
                    "enable_software_control_cls": EnableSoftwareControl,
                    "enable_software_control_response_cls": EnableSoftwareControlResponse,
                },
                "max_function_index": 2
            },
        }
        cls.max_version = 0
    # end def setUpClass

    def test_factory(self):
        """
        Test ``GamingGKeysFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(GamingGKeysFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``GamingGKeysFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [self.max_version + 1, self.max_version + 2]:
            with self.assertRaises(KeyError):
                GamingGKeysFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``GamingGKeysFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = GamingGKeysFactory.create(version)
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

        :raise ``AssertionError``: Assert max_function_index that raise an exception
        """
        for version, expected in self.expected.items():
            obj = GamingGKeysFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class GamingGKeysTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
