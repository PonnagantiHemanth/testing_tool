#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.common.test.configurableproperties_test
:brief: HID++ 2.0 ``ConfigurableProperties`` test module
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/09/14
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.common.configurableproperties import ConfigurableProperties
from pyhid.hidpp.features.common.configurableproperties import ConfigurablePropertiesFactory
from pyhid.hidpp.features.common.configurableproperties import ConfigurablePropertiesV0
from pyhid.hidpp.features.common.configurableproperties import ConfigurablePropertiesV1
from pyhid.hidpp.features.common.configurableproperties import ConfigurablePropertiesV2
from pyhid.hidpp.features.common.configurableproperties import ConfigurablePropertiesV3
from pyhid.hidpp.features.common.configurableproperties import ConfigurablePropertiesV4
from pyhid.hidpp.features.common.configurableproperties import DeleteProperty
from pyhid.hidpp.features.common.configurableproperties import DeletePropertyResponse
from pyhid.hidpp.features.common.configurableproperties import GetPropertyInfo
from pyhid.hidpp.features.common.configurableproperties import GetPropertyInfoResponse
from pyhid.hidpp.features.common.configurableproperties import ReadProperty
from pyhid.hidpp.features.common.configurableproperties import ReadPropertyResponse
from pyhid.hidpp.features.common.configurableproperties import SelectProperty
from pyhid.hidpp.features.common.configurableproperties import SelectPropertyResponse
from pyhid.hidpp.features.common.configurableproperties import WriteProperty
from pyhid.hidpp.features.common.configurableproperties import WritePropertyResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ConfigurablePropertiesInstantiationTestCase(TestCase):
    """
    Test ``ConfigurableProperties`` testing classes instantiations
    """

    @staticmethod
    def test_configurable_properties():
        """
        Test ``ConfigurableProperties`` class instantiation
        """
        my_class = ConfigurableProperties(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = ConfigurableProperties(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_configurable_properties

    @staticmethod
    def test_get_property_info():
        """
        Test ``GetPropertyInfo`` class instantiation
        """
        my_class = GetPropertyInfo(device_index=0, feature_index=0,
                                   property_id=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetPropertyInfo(device_index=0xFF, feature_index=0xFF,
                                   property_id=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_property_info

    @staticmethod
    def test_select_property():
        """
        Test ``SelectProperty`` class instantiation
        """
        my_class = SelectProperty(device_index=0, feature_index=0,
                                  property_id=0,
                                  rd_offset=0,
                                  wr_offset=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SelectProperty(device_index=0xFF, feature_index=0xFF,
                                  property_id=0xFF,
                                  rd_offset=0xFFFF,
                                  wr_offset=0xFFFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_select_property

    @staticmethod
    def test_read_property():
        """
        Test ``ReadProperty`` class instantiation
        """
        my_class = ReadProperty(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = ReadProperty(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_read_property

    @staticmethod
    def test_write_property():
        """
        Test ``WriteProperty`` class instantiation
        """
        my_class = WriteProperty(device_index=0, feature_index=0,
                                 data=HexList("00" * (WriteProperty.LEN.DATA // 8)))

        RootTestCase._long_function_class_checker(my_class)

        my_class = WriteProperty(device_index=0xFF, feature_index=0xFF,
                                 data=HexList("FF" * (WriteProperty.LEN.DATA // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_write_property

    @staticmethod
    def test_delete_property():
        """
        Test ``DeleteProperty`` class instantiation
        """
        my_class = DeleteProperty(device_index=0, feature_index=0,
                                  property_id=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = DeleteProperty(device_index=0xFF, feature_index=0xFF,
                                  property_id=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_delete_property

    @staticmethod
    def test_get_property_info_response():
        """
        Test ``GetPropertyInfoResponse`` class instantiation
        """
        my_class = GetPropertyInfoResponse(device_index=0, feature_index=0,
                                           corrupted=False,
                                           present=False,
                                           supported=False,
                                           size=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetPropertyInfoResponse(device_index=0xFF, feature_index=0xFF,
                                           corrupted=True,
                                           present=True,
                                           supported=True,
                                           size=0xFFFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_property_info_response

    @staticmethod
    def test_select_property_response():
        """
        Test ``SelectPropertyResponse`` class instantiation
        """
        my_class = SelectPropertyResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SelectPropertyResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_select_property_response

    @staticmethod
    def test_read_property_response():
        """
        Test ``ReadPropertyResponse`` class instantiation
        """
        my_class = ReadPropertyResponse(device_index=0, feature_index=0,
                                        data=HexList("00" * (ReadPropertyResponse.LEN.DATA // 8)))

        RootTestCase._long_function_class_checker(my_class)

        my_class = ReadPropertyResponse(device_index=0, feature_index=0,
                                        data=HexList([0x00] * (ReadPropertyResponse.LEN.DATA // 8)))

        RootTestCase._long_function_class_checker(my_class)

        my_class = ReadPropertyResponse(device_index=0xFF, feature_index=0xFF,
                                        data=HexList("FF" * (ReadPropertyResponse.LEN.DATA // 8)))

        RootTestCase._long_function_class_checker(my_class)

        my_class = ReadPropertyResponse(device_index=0, feature_index=0,
                                        data=HexList([0xFF] * (ReadPropertyResponse.LEN.DATA // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_read_property_response

    @staticmethod
    def test_write_property_response():
        """
        Test ``WritePropertyResponse`` class instantiation
        """
        my_class = WritePropertyResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = WritePropertyResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_write_property_response

    @staticmethod
    def test_delete_property_response():
        """
        Test ``DeletePropertyResponse`` class instantiation
        """
        my_class = DeletePropertyResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = DeletePropertyResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_delete_property_response
# end class ConfigurablePropertiesInstantiationTestCase


class ConfigurablePropertiesTestCase(TestCase):
    """
    Test ``ConfigurableProperties`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        interfaces = {
            "get_property_info_cls": GetPropertyInfo,
            "get_property_info_response_cls": GetPropertyInfoResponse,
            "select_property_cls": SelectProperty,
            "select_property_response_cls": SelectPropertyResponse,
            "read_property_cls": ReadProperty,
            "read_property_response_cls": ReadPropertyResponse,
            "write_property_cls": WriteProperty,
            "write_property_response_cls": WritePropertyResponse,
            "delete_property_cls": DeleteProperty,
            "delete_property_response_cls": DeletePropertyResponse,
        }
        cls.expected = {
            ConfigurablePropertiesV0.VERSION: {
                "cls": ConfigurablePropertiesV0,
                "interfaces": interfaces,
                "max_function_index": 4
            },
            ConfigurablePropertiesV1.VERSION: {
                "cls": ConfigurablePropertiesV1,
                "interfaces": interfaces,
                "max_function_index": 4
            },
            ConfigurablePropertiesV2.VERSION: {
                "cls": ConfigurablePropertiesV2,
                "interfaces": interfaces,
                "max_function_index": 4
            },
            ConfigurablePropertiesV3.VERSION: {
                "cls": ConfigurablePropertiesV3,
                "interfaces": interfaces,
                "max_function_index": 4
            },
            ConfigurablePropertiesV4.VERSION: {
                "cls": ConfigurablePropertiesV4,
                "interfaces": interfaces,
                "max_function_index": 4
            },
        }
        cls.max_version = 4
    # end def setUpClass

    def test_factory(self):
        """
        Test ``ConfigurablePropertiesFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(ConfigurablePropertiesFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``ConfigurablePropertiesFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [self.max_version + 1, self.max_version + 2]:
            with self.assertRaises(KeyError):
                ConfigurablePropertiesFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``ConfigurablePropertiesFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = ConfigurablePropertiesFactory.create(version)
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
            obj = ConfigurablePropertiesFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class ConfigurablePropertiesTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
