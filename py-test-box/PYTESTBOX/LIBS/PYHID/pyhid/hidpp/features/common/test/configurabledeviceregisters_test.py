#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.common.test.configurabledeviceregisters_test
:brief: HID++ 2.0 ``ConfigurableDeviceRegisters`` test module
:author: Udayathilagan <uelamaran@logitech.com>
:date: 2024/05/08
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.common.configurabledeviceregisters import ConfigurableDeviceRegisters
from pyhid.hidpp.features.common.configurabledeviceregisters import ConfigurableDeviceRegistersFactory
from pyhid.hidpp.features.common.configurabledeviceregisters import ConfigurableDeviceRegistersV0
from pyhid.hidpp.features.common.configurabledeviceregisters import GetCapabilities
from pyhid.hidpp.features.common.configurabledeviceregisters import GetCapabilitiesResponse
from pyhid.hidpp.features.common.configurabledeviceregisters import GetRegisterInfo
from pyhid.hidpp.features.common.configurabledeviceregisters import GetRegisterInfoResponse
from pyhid.hidpp.features.common.configurabledeviceregisters import GetRegisterValue
from pyhid.hidpp.features.common.configurabledeviceregisters import GetRegisterValueResponse
from pyhid.hidpp.features.common.configurabledeviceregisters import SetRegisterValue
from pyhid.hidpp.features.common.configurabledeviceregisters import SetRegisterValueResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ConfigurableDeviceRegistersInstantiationTestCase(TestCase):
    """
    Test ``ConfigurableDeviceRegisters`` testing classes instantiations
    """

    @staticmethod
    def test_configurable_device_registers():
        """
        Test ``ConfigurableDeviceRegisters`` class instantiation
        """
        my_class = ConfigurableDeviceRegisters(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = ConfigurableDeviceRegisters(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_configurable_device_registers

    @staticmethod
    def test_get_capabilities():
        """
        Test ``GetCapabilities`` class instantiation
        """
        my_class = GetCapabilities(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetCapabilities(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_capabilities

    @staticmethod
    def test_get_register_info():
        """
        Test ``GetRegisterInfo`` class instantiation
        """
        my_class = GetRegisterInfo(device_index=0, feature_index=0,
                                   register_id=HexList(0))

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetRegisterInfo(device_index=0xFF, feature_index=0xFF,
                                   register_id=HexList("FF" * (GetRegisterInfo.LEN.REGISTER_ID // 8)))

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_register_info

    @staticmethod
    def test_get_register_value():
        """
        Test ``GetRegisterValue`` class instantiation
        """
        my_class = GetRegisterValue(device_index=0, feature_index=0,
                                    register_id=HexList(0))

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetRegisterValue(device_index=0xFF, feature_index=0xFF,
                                    register_id=HexList("FF" * (GetRegisterValue.LEN.REGISTER_ID // 8)))

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_register_value

    @staticmethod
    def test_set_register_value():
        """
        Test ``SetRegisterValue`` class instantiation
        """
        my_class = SetRegisterValue(device_index=0, feature_index=0,
                                    register_id=HexList(0),
                                    register_value=HexList(0))

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRegisterValue(device_index=0xFF, feature_index=0xFF,
                                    register_id=HexList("FF" * (SetRegisterValue.LEN.REGISTER_ID // 8)),
                                    register_value=HexList("FF" * (SetRegisterValue.LEN.REGISTER_VALUE // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_register_value

    @staticmethod
    def test_get_capabilities_response():
        """
        Test ``GetCapabilitiesResponse`` class instantiation
        """
        my_class = GetCapabilitiesResponse(device_index=0, feature_index=0,
                                           capabilities=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCapabilitiesResponse(device_index=0xFF, feature_index=0xFF,
                                           capabilities=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_capabilities_response

    @staticmethod
    def test_get_register_info_response():
        """
        Test ``GetRegisterInfoResponse`` class instantiation
        """
        my_class = GetRegisterInfoResponse(device_index=0, feature_index=0,
                                           configurable=False,
                                           supported=False,
                                           register_size=HexList(0))

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetRegisterInfoResponse(device_index=0xFF, feature_index=0xFF,
                                           configurable=True,
                                           supported=True,
                                           register_size=HexList("FF" * (GetRegisterInfoResponse.LEN.REGISTER_SIZE // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_register_info_response

    @staticmethod
    def test_get_register_value_response():
        """
        Test ``GetRegisterValueResponse`` class instantiation
        """
        my_class = GetRegisterValueResponse(device_index=0, feature_index=0,registervalue=HexList(0),
                                            registersize=HexList(0), payload=HexList(0x00)*16)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetRegisterValueResponse(device_index=0xFF, feature_index=0xFF,registervalue=HexList(0xff),
                                            registersize=HexList(0xff), payload=HexList(0xff)*16)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_register_value_response

    @staticmethod
    def test_set_register_value_response():
        """
        Test ``SetRegisterValueResponse`` class instantiation
        """
        my_class = SetRegisterValueResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRegisterValueResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_register_value_response
# end class ConfigurableDeviceRegistersInstantiationTestCase


class ConfigurableDeviceRegistersTestCase(TestCase):
    """
    Test ``ConfigurableDeviceRegisters`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            ConfigurableDeviceRegistersV0.VERSION: {
                "cls": ConfigurableDeviceRegistersV0,
                "interfaces": {
                    "get_capabilities_cls": GetCapabilities,
                    "get_capabilities_response_cls": GetCapabilitiesResponse,
                    "get_register_info_cls": GetRegisterInfo,
                    "get_register_info_response_cls": GetRegisterInfoResponse,
                    "get_register_value_cls": GetRegisterValue,
                    "get_register_value_response_cls": GetRegisterValueResponse,
                    "set_register_value_cls": SetRegisterValue,
                    "set_register_value_response_cls": SetRegisterValueResponse,
                },
                "max_function_index": 3
            },
        }
        cls.max_version = 0
    # end def setUpClass

    def test_factory(self):
        """
        Test ``ConfigurableDeviceRegistersFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(ConfigurableDeviceRegistersFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``ConfigurableDeviceRegistersFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [self.max_version + 1, self.max_version + 2]:
            with self.assertRaises(KeyError):
                ConfigurableDeviceRegistersFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``ConfigurableDeviceRegistersFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = ConfigurableDeviceRegistersFactory.create(version)
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
            obj = ConfigurableDeviceRegistersFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class ConfigurableDeviceRegistersTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
