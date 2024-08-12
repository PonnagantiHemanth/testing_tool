#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.1'
:package: pyhid.hidpp.features.common.test.tdeaccesstonvm_test
:brief: HID++ 2.0 ``TdeAccessToNvm`` test module
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2020/07/01
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.common.tdeaccesstonvm import GetTdeMemLength
from pyhid.hidpp.features.common.tdeaccesstonvm import GetTdeMemLengthResponse
from pyhid.hidpp.features.common.tdeaccesstonvm import TdeAccessToNvm
from pyhid.hidpp.features.common.tdeaccesstonvm import TdeAccessToNvmFactory
from pyhid.hidpp.features.common.tdeaccesstonvm import TdeAccessToNvmV0
from pyhid.hidpp.features.common.tdeaccesstonvm import TdeClearData
from pyhid.hidpp.features.common.tdeaccesstonvm import TdeClearDataResponse
from pyhid.hidpp.features.common.tdeaccesstonvm import TdeReadData
from pyhid.hidpp.features.common.tdeaccesstonvm import TdeReadDataResponse
from pyhid.hidpp.features.common.tdeaccesstonvm import TdeWriteData
from pyhid.hidpp.features.common.tdeaccesstonvm import TdeWriteDataResponse
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TdeAccessToNvmInstantiationTestCase(TestCase):
    """
    Test ``TdeAccessToNvm`` testing classes instantiations
    """

    @staticmethod
    def test_tde_access_to_nvm():
        """
        Test ``TdeAccessToNvm`` class instantiation
        """
        my_class = TdeAccessToNvm(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = TdeAccessToNvm(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_tde_access_to_nvm

    @staticmethod
    def test_get_tde_mem_length():
        """
        Test ``GetTdeMemLength`` class instantiation
        """
        my_class = GetTdeMemLength(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetTdeMemLength(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_tde_mem_length

    @staticmethod
    def test_get_tde_mem_length_response():
        """
        Test ``GetTdeMemLengthResponse`` class instantiation
        """
        my_class = GetTdeMemLengthResponse(device_index=0, feature_index=0,
                                           memory_length=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetTdeMemLengthResponse(device_index=0xff, feature_index=0xff,
                                           memory_length=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_tde_mem_length_response

    @staticmethod
    def test_tde_write_data():
        """
        Test ``TdeWriteData`` class instantiation
        """
        my_class = TdeWriteData(device_index=0, feature_index=0,
                                starting_position=0,
                                number_of_bytes_to_read_or_write=0,
                                data_byte_0=0,
                                data_byte_1=0,
                                data_byte_2=0,
                                data_byte_3=0,
                                data_byte_4=0,
                                data_byte_5=0,
                                data_byte_6=0,
                                data_byte_7=0,
                                data_byte_8=0,
                                data_byte_9=0,
                                data_byte_10=0,
                                data_byte_11=0,
                                data_byte_12=0,
                                data_byte_13=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = TdeWriteData(device_index=0xff, feature_index=0xff,
                                starting_position=0xff,
                                number_of_bytes_to_read_or_write=0xff,
                                data_byte_0=0xff,
                                data_byte_1=0xff,
                                data_byte_2=0xff,
                                data_byte_3=0xff,
                                data_byte_4=0xff,
                                data_byte_5=0xff,
                                data_byte_6=0xff,
                                data_byte_7=0xff,
                                data_byte_8=0xff,
                                data_byte_9=0xff,
                                data_byte_10=0xff,
                                data_byte_11=0xff,
                                data_byte_12=0xff,
                                data_byte_13=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_tde_write_data

    @staticmethod
    def test_tde_write_data_response():
        """
        Test ``TdeWriteDataResponse`` class instantiation
        """
        my_class = TdeWriteDataResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = TdeWriteDataResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_tde_write_data_response

    @staticmethod
    def test_tde_read_data():
        """
        Test ``TdeReadData`` class instantiation
        """
        my_class = TdeReadData(device_index=0, feature_index=0,
                               starting_position=0,
                               number_of_bytes_to_read=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = TdeReadData(device_index=0xff, feature_index=0xff,
                               starting_position=0xff,
                               number_of_bytes_to_read=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_tde_read_data

    @staticmethod
    def test_tde_read_data_response():
        """
        Test ``TdeReadDataResponse`` class instantiation
        """
        my_class = TdeReadDataResponse(device_index=0, feature_index=0,
                                       starting_position=0,
                                       number_of_bytes_to_read_or_write=0,
                                       data_byte_0=0,
                                       data_byte_1=0,
                                       data_byte_2=0,
                                       data_byte_3=0,
                                       data_byte_4=0,
                                       data_byte_5=0,
                                       data_byte_6=0,
                                       data_byte_7=0,
                                       data_byte_8=0,
                                       data_byte_9=0,
                                       data_byte_10=0,
                                       data_byte_11=0,
                                       data_byte_12=0,
                                       data_byte_13=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = TdeReadDataResponse(device_index=0xff, feature_index=0xff,
                                       starting_position=0xff,
                                       number_of_bytes_to_read_or_write=0xff,
                                       data_byte_0=0xff,
                                       data_byte_1=0xff,
                                       data_byte_2=0xff,
                                       data_byte_3=0xff,
                                       data_byte_4=0xff,
                                       data_byte_5=0xff,
                                       data_byte_6=0xff,
                                       data_byte_7=0xff,
                                       data_byte_8=0xff,
                                       data_byte_9=0xff,
                                       data_byte_10=0xff,
                                       data_byte_11=0xff,
                                       data_byte_12=0xff,
                                       data_byte_13=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_tde_read_data_response

    @staticmethod
    def test_tde_clear_data():
        """
        Test ``TdeClearData`` class instantiation
        """
        my_class = TdeClearData(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = TdeClearData(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_tde_clear_data

    @staticmethod
    def test_tde_clear_data_response():
        """
        Test ``TdeClearDataResponse`` class instantiation
        """
        my_class = TdeClearDataResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = TdeClearDataResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_tde_clear_data_response
# end class TdeAccessToNvmInstantiationTestCase


class TdeAccessToNvmTestCase(TestCase):
    """
    Test ``TdeAccessToNvm`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            TdeAccessToNvmV0.VERSION: {
                "cls": TdeAccessToNvmV0,
                "interfaces": {
                    "get_tde_mem_length_cls": GetTdeMemLength,
                    "get_tde_mem_length_response_cls": GetTdeMemLengthResponse,
                    "tde_write_data_cls": TdeWriteData,
                    "tde_write_data_response_cls": TdeWriteDataResponse,
                    "tde_read_data_cls": TdeReadData,
                    "tde_read_data_response_cls": TdeReadDataResponse,
                    "tde_clear_data_cls": TdeClearData,
                    "tde_clear_data_response_cls": TdeClearDataResponse,
                },
                "max_function_index": 3
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Test ``TdeAccessToNvmFactory``
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(TdeAccessToNvmFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``TdeAccessToNvmFactory`` using out of range versions
        """
        for version in [1, 2]:
            with self.assertRaises(KeyError):
                TdeAccessToNvmFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``TdeAccessToNvmFactory`` returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            obj = TdeAccessToNvmFactory.create(version)
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
            obj = TdeAccessToNvmFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class TdeAccessToNvmTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
