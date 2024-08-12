#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pyhid.hidpp.features.common.test.devicetypeandname_test
:brief: HID++ 2.0 ``DeviceTypeAndName`` test module
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/12/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.common.devicetypeandname import DeviceTypeAndName
from pyhid.hidpp.features.common.devicetypeandname import DeviceTypeAndNameFactory
from pyhid.hidpp.features.common.devicetypeandname import DeviceTypeAndNameV0
from pyhid.hidpp.features.common.devicetypeandname import DeviceTypeAndNameV1
from pyhid.hidpp.features.common.devicetypeandname import DeviceTypeAndNameV2
from pyhid.hidpp.features.common.devicetypeandname import DeviceTypeAndNameV3
from pyhid.hidpp.features.common.devicetypeandname import DeviceTypeAndNameV4
from pyhid.hidpp.features.common.devicetypeandname import DeviceTypeAndNameV5
from pyhid.hidpp.features.common.devicetypeandname import GetDeviceName
from pyhid.hidpp.features.common.devicetypeandname import GetDeviceNameCount
from pyhid.hidpp.features.common.devicetypeandname import GetDeviceNameCountResponse
from pyhid.hidpp.features.common.devicetypeandname import GetDeviceNameResponse
from pyhid.hidpp.features.common.devicetypeandname import GetDeviceType
from pyhid.hidpp.features.common.devicetypeandname import GetDeviceTypeResponse
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceTypeAndNameInstantiationTestCase(TestCase):
    """
    Test ``DeviceTypeAndName`` testing classes instantiations
    """

    @staticmethod
    def test_device_type_and_name():
        """
        Test ``DeviceTypeAndName`` class instantiation
        """
        my_class = DeviceTypeAndName(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = DeviceTypeAndName(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_device_type_and_name

    @staticmethod
    def test_get_device_name_count():
        """
        Test ``GetDeviceNameCount`` class instantiation
        """
        my_class = GetDeviceNameCount(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetDeviceNameCount(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_device_name_count

    @staticmethod
    def test_get_device_name_count_response():
        """
        Test ``GetDeviceNameCountResponse`` class instantiation
        """
        my_class = GetDeviceNameCountResponse(device_index=0, feature_index=0,
                                              device_name_count=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetDeviceNameCountResponse(device_index=0xff, feature_index=0xff,
                                              device_name_count=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_device_name_count_response

    @staticmethod
    def test_get_device_name():
        """
        Test ``GetDeviceName`` class instantiation
        """
        my_class = GetDeviceName(device_index=0, feature_index=0,
                                 char_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetDeviceName(device_index=0xff, feature_index=0xff,
                                 char_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_device_name

    @staticmethod
    def test_get_device_name_response():
        """
        Test ``GetDeviceNameResponse`` class instantiation
        """
        my_class = GetDeviceNameResponse(device_index=0, feature_index=0,
                                         device_name=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetDeviceNameResponse(device_index=0xff, feature_index=0xff,
                                         device_name=0xffffffffffffffffffffffffffffffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_device_name_response

    @staticmethod
    def test_get_device_type():
        """
        Test ``GetDeviceType`` class instantiation
        """
        my_class = GetDeviceType(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetDeviceType(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_device_type

    @staticmethod
    def test_get_device_type_response():
        """
        Test ``GetDeviceTypeResponse`` class instantiation
        """
        my_class = GetDeviceTypeResponse(device_index=0, feature_index=0,
                                         device_type=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetDeviceTypeResponse(device_index=0xff, feature_index=0xff,
                                         device_type=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_device_type_response
# end class DeviceTypeAndNameInstantiationTestCase


class DeviceTypeAndNameTestCase(TestCase):
    """
    Test ``DeviceTypeAndName`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            DeviceTypeAndNameV0.VERSION: {
                "cls": DeviceTypeAndNameV0,
                "interfaces": {
                    "get_device_name_count_cls": GetDeviceNameCount,
                    "get_device_name_count_response_cls": GetDeviceNameCountResponse,
                    "get_device_name_cls": GetDeviceName,
                    "get_device_name_response_cls": GetDeviceNameResponse,
                    "get_device_type_cls": GetDeviceType,
                    "get_device_type_response_cls": GetDeviceTypeResponse,
                },
                "max_function_index": 2
            },
            DeviceTypeAndNameV1.VERSION: {
                "cls": DeviceTypeAndNameV1,
                "interfaces": {
                    "get_device_name_count_cls": GetDeviceNameCount,
                    "get_device_name_count_response_cls": GetDeviceNameCountResponse,
                    "get_device_name_cls": GetDeviceName,
                    "get_device_name_response_cls": GetDeviceNameResponse,
                    "get_device_type_cls": GetDeviceType,
                    "get_device_type_response_cls": GetDeviceTypeResponse,
                },
                "max_function_index": 2
            },
            DeviceTypeAndNameV2.VERSION: {
                "cls": DeviceTypeAndNameV2,
                "interfaces": {
                    "get_device_name_count_cls": GetDeviceNameCount,
                    "get_device_name_count_response_cls": GetDeviceNameCountResponse,
                    "get_device_name_cls": GetDeviceName,
                    "get_device_name_response_cls": GetDeviceNameResponse,
                    "get_device_type_cls": GetDeviceType,
                    "get_device_type_response_cls": GetDeviceTypeResponse,
                },
                "max_function_index": 2
            },
            DeviceTypeAndNameV3.VERSION: {
                "cls": DeviceTypeAndNameV3,
                "interfaces": {
                    "get_device_name_count_cls": GetDeviceNameCount,
                    "get_device_name_count_response_cls": GetDeviceNameCountResponse,
                    "get_device_name_cls": GetDeviceName,
                    "get_device_name_response_cls": GetDeviceNameResponse,
                    "get_device_type_cls": GetDeviceType,
                    "get_device_type_response_cls": GetDeviceTypeResponse,
                },
                "max_function_index": 2
            },
            DeviceTypeAndNameV4.VERSION: {
                "cls": DeviceTypeAndNameV4,
                "interfaces": {
                    "get_device_name_count_cls": GetDeviceNameCount,
                    "get_device_name_count_response_cls": GetDeviceNameCountResponse,
                    "get_device_name_cls": GetDeviceName,
                    "get_device_name_response_cls": GetDeviceNameResponse,
                    "get_device_type_cls": GetDeviceType,
                    "get_device_type_response_cls": GetDeviceTypeResponse,
                },
                "max_function_index": 2
            },
            DeviceTypeAndNameV5.VERSION: {
                "cls": DeviceTypeAndNameV5,
                "interfaces": {
                    "get_device_name_count_cls": GetDeviceNameCount,
                    "get_device_name_count_response_cls": GetDeviceNameCountResponse,
                    "get_device_name_cls": GetDeviceName,
                    "get_device_name_response_cls": GetDeviceNameResponse,
                    "get_device_type_cls": GetDeviceType,
                    "get_device_type_response_cls": GetDeviceTypeResponse,
                },
                "max_function_index": 2
            },

        }
    # end def setUpClass

    def test_factory(self):
        """
        Test ``DeviceTypeAndNameFactory``
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(DeviceTypeAndNameFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``DeviceTypeAndNameFactory`` using out of range versions
        """
        for version in [6, 7]:
            with self.assertRaises(KeyError):
                DeviceTypeAndNameFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``DeviceTypeAndNameFactory`` returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            obj = DeviceTypeAndNameFactory.create(version)
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
            obj = DeviceTypeAndNameFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class DeviceTypeAndNameTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
