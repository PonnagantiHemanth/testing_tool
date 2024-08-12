#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pyhid.hidpp.features.common.test.opticalswitches_test
:brief: HID++ 2.0 ``OpticalSwitches`` test module
:author: Fred Chen <fchen7@logitech.com>
:date: 2023/03/08
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.common.opticalswitches import ConfigEmitTime
from pyhid.hidpp.features.common.opticalswitches import ConfigEmitTimeResponse
from pyhid.hidpp.features.common.opticalswitches import EndTest
from pyhid.hidpp.features.common.opticalswitches import EndTestResponse
from pyhid.hidpp.features.common.opticalswitches import GenerateMaskTable
from pyhid.hidpp.features.common.opticalswitches import GenerateMaskTableResponse
from pyhid.hidpp.features.common.opticalswitches import GetHardwareInfo
from pyhid.hidpp.features.common.opticalswitches import GetHardwareInfoResponse
from pyhid.hidpp.features.common.opticalswitches import GetKeyReleaseTimings
from pyhid.hidpp.features.common.opticalswitches import GetKeyReleaseTimingsResponse
from pyhid.hidpp.features.common.opticalswitches import GetMaskTable
from pyhid.hidpp.features.common.opticalswitches import GetMaskTableResponse
from pyhid.hidpp.features.common.opticalswitches import InitTest
from pyhid.hidpp.features.common.opticalswitches import InitTestResponse
from pyhid.hidpp.features.common.opticalswitches import OpticalSwitches
from pyhid.hidpp.features.common.opticalswitches import OpticalSwitchesFactory
from pyhid.hidpp.features.common.opticalswitches import OpticalSwitchesV0
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class OpticalSwitchesInstantiationTestCase(TestCase):
    """
    Test ``OpticalSwitches`` testing classes instantiations
    """

    @staticmethod
    def test_optical_switches():
        """
        Test ``OpticalSwitches`` class instantiation
        """
        my_class = OpticalSwitches(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = OpticalSwitches(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_optical_switches

    @staticmethod
    def test_get_hardware_info():
        """
        Test ``GetHardwareInfo`` class instantiation
        """
        my_class = GetHardwareInfo(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetHardwareInfo(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_hardware_info

    @staticmethod
    def test_get_hardware_info_response():
        """
        Test ``GetHardwareInfoResponse`` class instantiation
        """
        my_class = GetHardwareInfoResponse(device_index=0, feature_index=0,
                                           nb_columns=0,
                                           nb_rows=0,
                                           timeout_us=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetHardwareInfoResponse(device_index=0xff, feature_index=0xff,
                                           nb_columns=0xff,
                                           nb_rows=0xff,
                                           timeout_us=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_hardware_info_response

    @staticmethod
    def test_generate_mask_table():
        """
        Test ``GenerateMaskTable`` class instantiation
        """
        my_class = GenerateMaskTable(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GenerateMaskTable(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_generate_mask_table

    @staticmethod
    def test_generate_mask_table_response():
        """
        Test ``GenerateMaskTableResponse`` class instantiation
        """
        my_class = GenerateMaskTableResponse(device_index=0, feature_index=0,
                                             nb_available_keys=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GenerateMaskTableResponse(device_index=0xff, feature_index=0xff,
                                             nb_available_keys=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_generate_mask_table_response

    @staticmethod
    def test_get_mask_table():
        """
        Test ``GetMaskTable`` class instantiation
        """
        my_class = GetMaskTable(device_index=0, feature_index=0,
                                column_idx=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetMaskTable(device_index=0xff, feature_index=0xff,
                                column_idx=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_mask_table

    @staticmethod
    def test_get_mask_table_response():
        """
        Test ``GetMaskTableResponse`` class instantiation
        """
        my_class = GetMaskTableResponse(device_index=0, feature_index=0,
                                        port_0_row_mask=0,
                                        port_1_row_mask=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetMaskTableResponse(device_index=0xff, feature_index=0xff,
                                        port_0_row_mask=HexList('FF' * (GetMaskTableResponse.LEN.PORT_0_ROW_MASK // 8)),
                                        port_1_row_mask=HexList('FF' * (GetMaskTableResponse.LEN.PORT_1_ROW_MASK // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_mask_table_response

    @staticmethod
    def test_init_test():
        """
        Test ``InitTest`` class instantiation
        """
        my_class = InitTest(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = InitTest(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_init_test

    @staticmethod
    def test_init_test_response():
        """
        Test ``InitTestResponse`` class instantiation
        """
        my_class = InitTestResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = InitTestResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_init_test_response

    @staticmethod
    def test_get_key_release_timings():
        """
        Test ``GetKeyReleaseTimings`` class instantiation
        """
        my_class = GetKeyReleaseTimings(device_index=0, feature_index=0,
                                        column_idx=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetKeyReleaseTimings(device_index=0xff, feature_index=0xff,
                                        column_idx=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_key_release_timings

    @staticmethod
    def test_get_key_release_timings_response():
        """
        Test ``GetKeyReleaseTimingsResponse`` class instantiation
        """
        my_class = GetKeyReleaseTimingsResponse(device_index=0, feature_index=0,
                                                min_duration=0,
                                                max_duration=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetKeyReleaseTimingsResponse(
            device_index=0xff, feature_index=0xff,
            min_duration=HexList('FF' * (GetKeyReleaseTimingsResponse.LEN.MIN_DURATION // 8)),
            max_duration=HexList('FF' * (GetKeyReleaseTimingsResponse.LEN.MAX_DURATION // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_key_release_timings_response

    @staticmethod
    def test_config_emit_time():
        """
        Test ``ConfigEmitTime`` class instantiation
        """
        my_class = ConfigEmitTime(device_index=0, feature_index=0,
                                  emit_time_us=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = ConfigEmitTime(device_index=0xff, feature_index=0xff,
                                  emit_time_us=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_config_emit_time

    @staticmethod
    def test_config_emit_time_response():
        """
        Test ``ConfigEmitTimeResponse`` class instantiation
        """
        my_class = ConfigEmitTimeResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ConfigEmitTimeResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_config_emit_time_response

    @staticmethod
    def test_end_test():
        """
        Test ``EndTest`` class instantiation
        """
        my_class = EndTest(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = EndTest(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_end_test

    @staticmethod
    def test_end_test_response():
        """
        Test ``EndTestResponse`` class instantiation
        """
        my_class = EndTestResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = EndTestResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_end_test_response
# end class OpticalSwitchesInstantiationTestCase


class OpticalSwitchesTestCase(TestCase):
    """
    Test ``OpticalSwitches`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            OpticalSwitchesV0.VERSION: {
                "cls": OpticalSwitchesV0,
                "interfaces": {
                    "get_hardware_info_cls": GetHardwareInfo,
                    "get_hardware_info_response_cls": GetHardwareInfoResponse,
                    "generate_mask_table_cls": GenerateMaskTable,
                    "generate_mask_table_response_cls": GenerateMaskTableResponse,
                    "get_mask_table_cls": GetMaskTable,
                    "get_mask_table_response_cls": GetMaskTableResponse,
                    "init_test_cls": InitTest,
                    "init_test_response_cls": InitTestResponse,
                    "get_key_release_timings_cls": GetKeyReleaseTimings,
                    "get_key_release_timings_response_cls": GetKeyReleaseTimingsResponse,
                    "config_emit_time_cls": ConfigEmitTime,
                    "config_emit_time_response_cls": ConfigEmitTimeResponse,
                    "end_test_cls": EndTest,
                    "end_test_response_cls": EndTestResponse,
                },
                "max_function_index": 6
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Test ``OpticalSwitchesFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(OpticalSwitchesFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``OpticalSwitchesFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [1, 2]:
            with self.assertRaises(KeyError):
                OpticalSwitchesFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``OpticalSwitchesFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = OpticalSwitchesFactory.create(version)
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
            obj = OpticalSwitchesFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class OpticalSwitchesTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
