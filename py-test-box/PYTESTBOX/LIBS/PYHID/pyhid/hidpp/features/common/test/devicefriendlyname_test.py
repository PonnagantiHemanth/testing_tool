#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.common.devicefriendlyname_test
:brief: HID++ 2.0 DeviceFriendlyName test module
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2020/09/07
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidpp.features.common.devicefriendlyname import DeviceFriendlyName
from pyhid.hidpp.features.common.devicefriendlyname import DeviceFriendlyNameFactory
from pyhid.hidpp.features.common.devicefriendlyname import DeviceFriendlyNameV0
from pyhid.hidpp.features.common.devicefriendlyname import GetDefaultFriendlyName
from pyhid.hidpp.features.common.devicefriendlyname import GetDefaultFriendlyNameResponse
from pyhid.hidpp.features.common.devicefriendlyname import GetFriendlyName
from pyhid.hidpp.features.common.devicefriendlyname import GetFriendlyNameLen
from pyhid.hidpp.features.common.devicefriendlyname import GetFriendlyNameLenResponse
from pyhid.hidpp.features.common.devicefriendlyname import GetFriendlyNameResponse
from pyhid.hidpp.features.common.devicefriendlyname import ResetFriendlyName
from pyhid.hidpp.features.common.devicefriendlyname import ResetFriendlyNameResponse
from pyhid.hidpp.features.common.devicefriendlyname import SetFriendlyName
from pyhid.hidpp.features.common.devicefriendlyname import SetFriendlyNameResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList
from unittest import TestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class DeviceFriendlyNameInstantiationTestCase(TestCase):
    """
    DeviceFriendlyName testing classes instantiations
    """
    @staticmethod
    def test_device_friendly_name():
        """
        Tests DeviceFriendlyName class instantiation
        """
        my_class = DeviceFriendlyName(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = DeviceFriendlyName(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_device_friendly_name

    @staticmethod
    def test_get_friendly_name_length():
        """
        Tests GetFriendlyNameLen class instantiation
        """
        my_class = GetFriendlyNameLen(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetFriendlyNameLen(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_friendly_name_length

    @staticmethod
    def test_get_friendly_name_length_response():
        """
        Tests GetFriendlyNameLenResponse class instantiation
        """
        my_class = GetFriendlyNameLenResponse(device_index=0, feature_index=0, name_len=0, name_max_len=0,
                                              default_name_len=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetFriendlyNameLenResponse(device_index=0xFF, feature_index=0xFF, name_len=0xFF, name_max_len=0xFF,
                                              default_name_len=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_friendly_name_length_response

    @staticmethod
    def test_get_friendly_name():
        """
        Tests GetFriendlyName class instantiation
        """
        my_class = GetFriendlyName(device_index=0, feature_index=0, byte_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetFriendlyName(device_index=0xFF, feature_index=0xFF, byte_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_friendly_name

    @staticmethod
    def test_get_friendly_name_response():
        """
        Tests GetFriendlyNameResponse class instantiation
        """
        my_class = GetFriendlyNameResponse(device_index=0, feature_index=0, byte_index=0,
                                           name_chunk=HexList("TEST_NAME_X0007".encode()))

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetFriendlyNameResponse(device_index=0xFF, feature_index=0xFF, byte_index=0xFF,
                                           name_chunk=HexList("TEST_NAME_X0007".encode()))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_friendly_name_response

    @staticmethod
    def test_get_default_friendly_name():
        """
        Tests GetDefaultFriendlyName class instantiation
        """
        my_class = GetDefaultFriendlyName(device_index=0, feature_index=0, byte_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetDefaultFriendlyName(device_index=0xFF, feature_index=0xFF, byte_index=0)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_default_friendly_name

    @staticmethod
    def test_get_default_friendly_name_response():
        """
        Tests GetDefaultFriendlyNameResponse class instantiation
        """
        my_class = GetDefaultFriendlyNameResponse(device_index=0, feature_index=0, byte_index=0,
                                                  name_chunk=HexList("TEST_NAME_X0007".encode()))

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetDefaultFriendlyNameResponse(device_index=0xFF, feature_index=0xFF, byte_index=0xFF,
                                                  name_chunk=HexList("TEST_NAME_X0007".encode()))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_default_friendly_name_response

    @staticmethod
    def test_set_friendly_name():
        """
        Tests SetFriendlyName class instantiation
        """
        my_class = SetFriendlyName(device_index=0, feature_index=0, byte_index=0,
                                   name_chunk=HexList("TEST_NAME_X0007".encode()))

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetFriendlyName(device_index=0xFF, feature_index=0xFF, byte_index=0xFF,
                                   name_chunk=HexList("TEST_NAME_X0007".encode()))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_friendly_name

    @staticmethod
    def test_set_friendly_name_response():
        """
        Tests SetFriendlyNameResponse class instantiation
        """
        my_class = SetFriendlyNameResponse(device_index=0, feature_index=0, name_len=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetFriendlyNameResponse(device_index=0xFF, feature_index=0xFF, name_len=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_friendly_name_response

    @staticmethod
    def test_reset_friendly_name():
        """
        Tests ResetFriendlyName class instantiation
        """
        my_class = ResetFriendlyName(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = ResetFriendlyName(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_reset_friendly_name

    @staticmethod
    def test_reset_friendly_name_response():
        """
        Tests ResetFriendlyNameResponse class instantiation
        """
        my_class = ResetFriendlyNameResponse(device_index=0, feature_index=0, name_len=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ResetFriendlyNameResponse(device_index=0xFF, feature_index=0xFF, name_len=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_reset_friendly_name_response
# end class DeviceFriendlyNameInstantiationTestCase


class DeviceFriendlyNameTestCase(TestCase):
    """
    DeviceFriendlyName factory testing
    """
    @classmethod
    def setUpClass(cls):
        cls.expected = {
                DeviceFriendlyNameV0.VERSION: {
                        "cls": DeviceFriendlyNameV0,
                        "interfaces": {
                                "get_friendly_name_len_cls": GetFriendlyNameLen,
                                "get_friendly_name_len_response_cls": GetFriendlyNameLenResponse,
                                "get_friendly_name_cls": GetFriendlyName,
                                "get_friendly_name_response_cls": GetFriendlyNameResponse,
                                "get_default_friendly_name_cls": GetDefaultFriendlyName,
                                "get_default_friendly_name_response_cls": GetDefaultFriendlyNameResponse,
                                "set_friendly_name_cls": SetFriendlyName,
                                "set_friendly_name_response_cls": SetFriendlyNameResponse,
                                "reset_friendly_name_cls": ResetFriendlyName,
                                "reset_friendly_name_response_cls": ResetFriendlyNameResponse,
                        },
                        "max_function_index": 4
                },
        }
    # end def setUpClass

    def test_device_friendly_name_factory(self):
        """
        Tests DeviceFriendlyNameFactory
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(DeviceFriendlyNameFactory.create(version)), expected["cls"])
        # end for
    # end def test_device_friendly_name_factory

    def test_device_friendly_name_factory_version_out_of_range(self):
        """
        Tests DeviceFriendlyNameFactory with out of range versions
        """
        for version in [1, 2]:
            with self.assertRaises(KeyError):
                DeviceFriendlyNameFactory.create(version)
            # end with
        # end for
    # end def test_device_friendly_name_factory_version_out_of_range

    def test_device_friendly_name_factory_interfaces(self):
        """
        Check DeviceFriendlyNameFactory returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            device_friendly_name = DeviceFriendlyNameFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(device_friendly_name, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(device_friendly_name, interface)
                    # end with
                # end if
            # end for
        # end for
    # end def test_device_friendly_name_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check get_max_function_index returns correct value at each version
        """
        for version, expected in self.expected.items():
            device_friendly_name = DeviceFriendlyNameFactory.create(version)
            self.assertEqual(device_friendly_name.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class DeviceFriendlyNameTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
