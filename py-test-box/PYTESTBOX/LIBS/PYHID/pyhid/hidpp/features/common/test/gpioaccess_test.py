#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.common.test.gpioaccess_test
:brief: HID++ 2.0 ``GpioAccess`` test module
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/06/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.common.gpioaccess import GpioAccess
from pyhid.hidpp.features.common.gpioaccess import GpioAccessFactory
from pyhid.hidpp.features.common.gpioaccess import GpioAccessV0
from pyhid.hidpp.features.common.gpioaccess import GpioAccessV1
from pyhid.hidpp.features.common.gpioaccess import ReadGroup
from pyhid.hidpp.features.common.gpioaccess import ReadGroupOutResponseV1
from pyhid.hidpp.features.common.gpioaccess import ReadGroupOutV1
from pyhid.hidpp.features.common.gpioaccess import ReadGroupResponse
from pyhid.hidpp.features.common.gpioaccess import SetGroupIn
from pyhid.hidpp.features.common.gpioaccess import SetGroupInResponse
from pyhid.hidpp.features.common.gpioaccess import WriteGroup
from pyhid.hidpp.features.common.gpioaccess import WriteGroupOut
from pyhid.hidpp.features.common.gpioaccess import WriteGroupOutResponse
from pyhid.hidpp.features.common.gpioaccess import WriteGroupResponse
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class GpioAccessInstantiationTestCase(TestCase):
    """
    Test ``GpioAccess`` testing classes instantiations
    """

    @staticmethod
    def test_gpio_access():
        """
        Test ``GpioAccess`` class instantiation
        """
        my_class = GpioAccess(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = GpioAccess(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_gpio_access

    @staticmethod
    def test_set_group_in():
        """
        Test ``SetGroupIn`` class instantiation
        """
        my_class = SetGroupIn(device_index=0, feature_index=0,
                              port_number=0,
                              gpio_mask=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetGroupIn(device_index=0xFF, feature_index=0xFF,
                              port_number=0xFF,
                              gpio_mask=0xFFFFFFFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_group_in

    @staticmethod
    def test_write_group_out():
        """
        Test ``WriteGroupOut`` class instantiation
        """
        my_class = WriteGroupOut(device_index=0, feature_index=0,
                                 port_number=0,
                                 gpio_mask=0,
                                 value=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = WriteGroupOut(device_index=0xFF, feature_index=0xFF,
                                 port_number=0xFF,
                                 gpio_mask=0xFFFFFFFF,
                                 value=0xFFFFFFFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_write_group_out

    @staticmethod
    def test_read_group():
        """
        Test ``ReadGroup`` class instantiation
        """
        my_class = ReadGroup(device_index=0, feature_index=0,
                             port_number=0,
                             gpio_mask=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ReadGroup(device_index=0xFF, feature_index=0xFF,
                             port_number=0xFF,
                             gpio_mask=0xFFFFFFFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_read_group

    @staticmethod
    def test_write_group():
        """
        Test ``WriteGroup`` class instantiation
        """
        my_class = WriteGroup(device_index=0, feature_index=0,
                              port_number=0,
                              gpio_mask=0,
                              value=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = WriteGroup(device_index=0xFF, feature_index=0xFF,
                              port_number=0xFF,
                              gpio_mask=0xFFFFFFFF,
                              value=0xFFFFFFFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_write_group

    @staticmethod
    def test_read_group_out_v1():
        """
        Test ``ReadGroupOutV1`` class instantiation
        """
        my_class = ReadGroupOutV1(device_index=0, feature_index=0,
                                  port_number=0,
                                  gpio_mask=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ReadGroupOutV1(device_index=0xFF, feature_index=0xFF,
                                  port_number=0xFF,
                                  gpio_mask=0xFFFFFFFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_read_group_out_v1

    @staticmethod
    def test_set_group_in_response():
        """
        Test ``SetGroupInResponse`` class instantiation
        """
        my_class = SetGroupInResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetGroupInResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_group_in_response

    @staticmethod
    def test_write_group_out_response():
        """
        Test ``WriteGroupOutResponse`` class instantiation
        """
        my_class = WriteGroupOutResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = WriteGroupOutResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_write_group_out_response

    @staticmethod
    def test_read_group_response():
        """
        Test ``ReadGroupResponse`` class instantiation
        """
        my_class = ReadGroupResponse(device_index=0, feature_index=0,
                                     port_number=0,
                                     gpio_mask=0,
                                     value=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ReadGroupResponse(device_index=0xFF, feature_index=0xFF,
                                     port_number=0xFF,
                                     gpio_mask=0xFFFFFFFF,
                                     value=0xFFFFFFFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_read_group_response

    @staticmethod
    def test_write_group_response():
        """
        Test ``WriteGroupResponse`` class instantiation
        """
        my_class = WriteGroupResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = WriteGroupResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_write_group_response

    @staticmethod
    def test_read_group_out_response_v1():
        """
        Test ``ReadGroupOutResponseV1`` class instantiation
        """
        my_class = ReadGroupOutResponseV1(device_index=0, feature_index=0,
                                          port_number=0,
                                          gpio_mask=0,
                                          value=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ReadGroupOutResponseV1(device_index=0xFF, feature_index=0xFF,
                                          port_number=0xFF,
                                          gpio_mask=0xFFFFFFFF,
                                          value=0xFFFFFFFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_read_group_out_response_v1
# end class GpioAccessInstantiationTestCase


class GpioAccessTestCase(TestCase):
    """
    Test ``GpioAccess`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            GpioAccessV0.VERSION: {
                "cls": GpioAccessV0,
                "interfaces": {
                    "set_group_in_cls": SetGroupIn,
                    "set_group_in_response_cls": SetGroupInResponse,
                    "write_group_out_cls": WriteGroupOut,
                    "write_group_out_response_cls": WriteGroupOutResponse,
                    "read_group_cls": ReadGroup,
                    "read_group_response_cls": ReadGroupResponse,
                    "write_group_cls": WriteGroup,
                    "write_group_response_cls": WriteGroupResponse,
                },
                "max_function_index": 3
            },
            GpioAccessV1.VERSION: {
                "cls": GpioAccessV1,
                "interfaces": {
                    "set_group_in_cls": SetGroupIn,
                    "set_group_in_response_cls": SetGroupInResponse,
                    "write_group_out_cls": WriteGroupOut,
                    "write_group_out_response_cls": WriteGroupOutResponse,
                    "read_group_cls": ReadGroup,
                    "read_group_response_cls": ReadGroupResponse,
                    "write_group_cls": WriteGroup,
                    "write_group_response_cls": WriteGroupResponse,
                    "read_group_out_cls": ReadGroupOutV1,
                    "read_group_out_response_cls": ReadGroupOutResponseV1,
                },
                "max_function_index": 4
            },
        }
        cls.max_version = 1
    # end def setUpClass

    def test_factory(self):
        """
        Test ``GpioAccessFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(GpioAccessFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``GpioAccessFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [self.max_version + 1, self.max_version + 2]:
            with self.assertRaises(KeyError):
                GpioAccessFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``GpioAccessFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = GpioAccessFactory.create(version)
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
            obj = GpioAccessFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class GpioAccessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
