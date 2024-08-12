#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.feature.mouse.test.adjustabledpi_test
    :brief: HID++ 2.0 Adjustable DPI test module
    :author: Christophe Roquebert
    :date:   2020/05/20
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidpp.features.mouse.adjustabledpi import AdjustableDpiFactory
from pyhid.hidpp.features.mouse.adjustabledpi import AdjustableDpiV0
from pyhid.hidpp.features.mouse.adjustabledpi import AdjustableDpiV1
from pyhid.hidpp.features.mouse.adjustabledpi import AdjustableDpiV2
from pyhid.hidpp.features.mouse.adjustabledpi import AdjustableDpi
from pyhid.hidpp.features.mouse.adjustabledpi import GetSensorCount
from pyhid.hidpp.features.mouse.adjustabledpi import GetSensorCountResponse
from pyhid.hidpp.features.mouse.adjustabledpi import GetSensorDpiList
from pyhid.hidpp.features.mouse.adjustabledpi import GetSensorDpiListResponse
from pyhid.hidpp.features.mouse.adjustabledpi import GetSensorDpi
from pyhid.hidpp.features.mouse.adjustabledpi import GetSensorDpiResponseV0
from pyhid.hidpp.features.mouse.adjustabledpi import GetSensorDpiResponseV1ToV2
from pyhid.hidpp.features.mouse.adjustabledpi import SetSensorDpiV0ToV1
from pyhid.hidpp.features.mouse.adjustabledpi import SetSensorDpiV2
from pyhid.hidpp.features.mouse.adjustabledpi import SetSensorDpiResponseV0
from pyhid.hidpp.features.mouse.adjustabledpi import SetSensorDpiResponseV1
from pyhid.hidpp.features.mouse.adjustabledpi import SetSensorDpiResponseV2
from pyhid.hidpp.features.mouse.adjustabledpi import GetNumberOfDpiLevelsV2
from pyhid.hidpp.features.mouse.adjustabledpi import GetNumberOfDpiLevelsResponseV2
from pyhid.hidpp.features.test.root_test import RootTestCase
from unittest import TestCase
from pylibrary.tools.hexlist import HexList


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class AdjustableDpiInstantiationTestCase(TestCase):
    """
    Adjustable Dpi Instantiation testing class
    """

    @staticmethod
    def test_adjustable_dpi():
        """
        Tests AdjustableDPi class instantiation
        """
        my_class = AdjustableDpi(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = AdjustableDpi(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_adjustable_dpi

    @staticmethod
    def test_get_sensor_count():
        """
        Tests GetSensorCount class instantiation
        """
        my_class = GetSensorCount(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetSensorCount(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_sensor_count

    @staticmethod
    def test_get_sensor_dpi_list():
        """
        Tests GetSensorDpiList class instantiation
        """
        my_class = GetSensorDpiList(device_index=0, feature_index=0, sensor_idx=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetSensorDpiList(device_index=0xFF, feature_index=0xFF, sensor_idx=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_sensor_dpi_list

    @staticmethod
    def test_get_sensor_dpi():
        """
        Tests GetSensorDpi class instantiation
        """
        my_class = GetSensorDpi(device_index=0, feature_index=0, sensor_idx=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetSensorDpi(device_index=0xFF, feature_index=0xFF, sensor_idx=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_sensor_dpi

    @staticmethod
    def test_set_sensor_dpi_v0_to_v1():
        """
        Tests SetSensorDpiV0ToV1 class instantiation
        """
        my_class = SetSensorDpiV0ToV1(device_index=0, feature_index=0, sensor_idx=0, dpi=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetSensorDpiV0ToV1(device_index=0xFF, feature_index=0xFF, sensor_idx=0xFF, dpi=0xFFFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_sensor_dpi_v0_to_v1

    @staticmethod
    def test_set_sensor_dpi_v2():
        """
        Tests SetSensorDpiV2 class instantiation
        """
        my_class = SetSensorDpiV2(device_index=0, feature_index=0, sensor_idx=0, dpi=0, dpi_level=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetSensorDpiV2(device_index=0xFF, feature_index=0xFF, sensor_idx=0xFF, dpi=0xFFFF, dpi_level=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_sensor_dpi_v2

    @staticmethod
    def test_get_number_of_dpi_levels_v2():
        """
        Tests GetNumberOfDpiLevelsV2 class instantiation
        """
        my_class = GetNumberOfDpiLevelsV2(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetNumberOfDpiLevelsV2(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_number_of_dpi_levels_v2

    @staticmethod
    def test_get_sensor_count_response():
        """
        Tests GetSensorCountResponse class instantiation
        """
        my_class = GetSensorCountResponse(device_index=0, feature_index=0, sensor_count=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetSensorCountResponse(device_index=0xFF, feature_index=0xFF, sensor_count=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_sensor_count_response

    @staticmethod
    def test_get_sensor_dpi_list_response():
        """
        Tests GetSensorDpiListResponse class instantiation
        """
        my_class = GetSensorDpiListResponse(device_index=0, feature_index=0, sensor_idx=0,
                                            dpi_list=HexList('00' * (GetSensorDpiListResponse.LEN.DPI_LIST // 8)))

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetSensorDpiListResponse(device_index=0xFF, feature_index=0xFF, sensor_idx=0xFF,
                                            dpi_list=HexList('FF' * (GetSensorDpiListResponse.LEN.DPI_LIST // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_sensor_dpi_list_response

    @staticmethod
    def test_get_sensor_dpi_response_v0():
        """
        Tests GetSensorDpiResponseV0 class instantiation
        """
        my_class = GetSensorDpiResponseV0(device_index=0, feature_index=0, sensor_idx=0, dpi=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetSensorDpiResponseV0(device_index=0xFF, feature_index=0xFF, sensor_idx=0xFF, dpi=0xFFFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_sensor_dpi_response_v0

    @staticmethod
    def test_get_sensor_dpi_response_v1_to_v2():
        """
        Tests GetSensorDpiResponseV1ToV2 class instantiation
        """
        my_class = GetSensorDpiResponseV1ToV2(device_index=0, feature_index=0, sensor_idx=0, dpi=0, default_dpi=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetSensorDpiResponseV1ToV2(device_index=0xFF, feature_index=0xFF, sensor_idx=0xFF, dpi=0xFFFF,
                                              default_dpi=0xFFFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_sensor_dpi_response_v1_to_V2

    @staticmethod
    def test_set_sensor_dpi_response_v0():
        """
        Tests SetSensorDpiResponseV0 class instantiation
        """
        my_class = SetSensorDpiResponseV0(device_index=0, feature_index=0, sensor_idx=0, dpi=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetSensorDpiResponseV0(device_index=0xFF, feature_index=0xFF, sensor_idx=0xFF, dpi=0xFFFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_sensor_dpi_response_v0

    @staticmethod
    def test_set_sensor_dpi_response_v1():
        """
        Tests SetSensorDpiResponseV1 class instantiation
        """
        my_class = SetSensorDpiResponseV1(device_index=0, feature_index=0, sensor_idx=0, dpi=0, default_dpi=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetSensorDpiResponseV1(device_index=0xFF, feature_index=0xFF, sensor_idx=0xFF, dpi=0xFFFF,
                                          default_dpi=0xFFFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_sensor_dpi_response_v1

    @staticmethod
    def test_set_sensor_dpi_response_v2():
        """
        Tests SetSensorDpiResponseV2 class instantiation
        """
        my_class = SetSensorDpiResponseV2(device_index=0, feature_index=0, sensor_idx=0, dpi=0, dpi_level=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = SetSensorDpiResponseV2(device_index=0xFF, feature_index=0xFF, sensor_idx=0xFF, dpi=0xFFFF,
                                          dpi_level=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_set_sensor_dpi_response_v2

    @staticmethod
    def test_get_number_of_dpi_levels_response_v2():
        """
        Tests GetNumberOfDpiLevelsResponseV2 class instantiation
        """
        my_class = GetNumberOfDpiLevelsResponseV2(device_index=0, feature_index=0, dpi_levels=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetNumberOfDpiLevelsResponseV2(device_index=0xFF, feature_index=0xFF, dpi_levels=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_number_of_dpi_levels_response_v2

# end class AdjustableDpiInstantiationTestCase


class AdjustableDpiTestCase(TestCase):
    """
    Adjustable Dpi factory testing
    """

    @classmethod
    def setUpClass(cls):
        cls.expected = {
            AdjustableDpiV0.VERSION: {
                "cls": AdjustableDpiV0,
                "interfaces": {
                    "get_sensor_count_cls": GetSensorCount,
                    "get_sensor_dpi_list_cls": GetSensorDpiList,
                    "get_sensor_dpi_cls": GetSensorDpi,
                    "set_sensor_dpi_cls": SetSensorDpiV0ToV1,
                    "get_sensor_count_response_cls": GetSensorCountResponse,
                    "get_sensor_dpi_list_response_cls": GetSensorDpiListResponse,
                    "get_sensor_dpi_response_cls": GetSensorDpiResponseV0,
                    "set_sensor_dpi_response_cls": SetSensorDpiResponseV0,
                },
                "max_function_index": AdjustableDpi.MAX_FUNCTION_INDEX_V0_TO_V1
            },
            AdjustableDpiV1.VERSION: {
                "cls": AdjustableDpiV1,
                "interfaces": {
                    "get_sensor_count_cls": GetSensorCount,
                    "get_sensor_dpi_list_cls": GetSensorDpiList,
                    "get_sensor_dpi_cls": GetSensorDpi,
                    "set_sensor_dpi_cls": SetSensorDpiV0ToV1,
                    "get_sensor_count_response_cls": GetSensorCountResponse,
                    "get_sensor_dpi_list_response_cls": GetSensorDpiListResponse,
                    "get_sensor_dpi_response_cls": GetSensorDpiResponseV1ToV2,
                    "set_sensor_dpi_response_cls": SetSensorDpiResponseV1,
                },
                "max_function_index": AdjustableDpi.MAX_FUNCTION_INDEX_V0_TO_V1
            },
            AdjustableDpiV2.VERSION: {
                "cls": AdjustableDpiV2,
                "interfaces": {
                    "get_sensor_count_cls": GetSensorCount,
                    "get_sensor_dpi_list_cls": GetSensorDpiList,
                    "get_sensor_dpi_cls": GetSensorDpi,
                    "set_sensor_dpi_cls": SetSensorDpiV2,
                    "get_sensor_count_response_cls": GetSensorCountResponse,
                    "get_sensor_dpi_list_response_cls": GetSensorDpiListResponse,
                    "get_sensor_dpi_response_cls": GetSensorDpiResponseV1ToV2,
                    "set_sensor_dpi_response_cls": SetSensorDpiResponseV2,
                    "get_number_of_dpi_levels_cls": GetNumberOfDpiLevelsV2,
                    "get_number_of_dpi_levels_response_cls": GetNumberOfDpiLevelsResponseV2,
                },
                "max_function_index": AdjustableDpi.MAX_FUNCTION_INDEX_V2
            },
        }
    # end def setUpClass

    def test_adjustable_dpi_factory(self):
        """
        Tests Adjustable Dpi Factory
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(AdjustableDpiFactory.create(version)), expected["cls"])
        # end for loop
    # end def test_adjustable_dpi_factory

    def test_adjustable_dpi_factory_version_out_of_range(self):
        """
        Tests Adjustable Dpi Factory with out of range versions
        """
        for version in [3, 4]:
            with self.assertRaises(KeyError):
                AdjustableDpiFactory.create(version)
            # end with
        # end for
    # end def test_adjustable_dpi_factory_version_out_of_range

    def test_adjustable_dpi_factory_interfaces(self):
        """
        Check Adjustable Dpi Factory returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            adjustable_dpi = AdjustableDpiFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(adjustable_dpi, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(adjustable_dpi, interface)
                # end if
            # end for loop
        # end for loop
    # end def test_adjustable_dpi_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check get_max_function_index returns correct value at each version
        """
        for version, expected in self.expected.items():
            adjustable_dpi = AdjustableDpiFactory.create(version)
            self.assertEqual(adjustable_dpi.get_max_function_index(), expected["max_function_index"])
        # end for loop
    # end def test_get_max_function_index
# end class AdjustableDpiTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
