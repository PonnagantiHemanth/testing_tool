#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
""" @package pyhid.hidpp.feature.common.test.unifiedbattery_test

@brief  HID++ 2.0 UnifiedBattery test module

@author Stanislas Cottard

@date   2019/10/23
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from unittest import TestCase
from pyhid.hidpp.features.common.unifiedbattery import BatteryStatusEventV0ToV3
from pyhid.hidpp.features.common.unifiedbattery import BatteryStatusEventV4
from pyhid.hidpp.features.common.unifiedbattery import BatteryStatusEventV5
from pyhid.hidpp.features.common.unifiedbattery import GetCapabilitiesResponseV0ToV1
from pyhid.hidpp.features.common.unifiedbattery import GetCapabilitiesResponseV2
from pyhid.hidpp.features.common.unifiedbattery import GetCapabilitiesResponseV3
from pyhid.hidpp.features.common.unifiedbattery import GetCapabilitiesResponseV4
from pyhid.hidpp.features.common.unifiedbattery import GetCapabilitiesResponseV5
from pyhid.hidpp.features.common.unifiedbattery import GetCapabilitiesV0ToV5
from pyhid.hidpp.features.common.unifiedbattery import GetStatusResponseV0ToV3
from pyhid.hidpp.features.common.unifiedbattery import GetStatusResponseV4
from pyhid.hidpp.features.common.unifiedbattery import GetStatusResponseV5
from pyhid.hidpp.features.common.unifiedbattery import GetStatusV0ToV5
from pyhid.hidpp.features.common.unifiedbattery import ShowBatteryStatusResponseV1ToV5
from pyhid.hidpp.features.common.unifiedbattery import ShowBatteryStatusV1ToV5
from pyhid.hidpp.features.common.unifiedbattery import UnifiedBattery
from pyhid.hidpp.features.common.unifiedbattery import UnifiedBatteryFactory
from pyhid.hidpp.features.common.unifiedbattery import UnifiedBatteryV0
from pyhid.hidpp.features.common.unifiedbattery import UnifiedBatteryV1
from pyhid.hidpp.features.common.unifiedbattery import UnifiedBatteryV2
from pyhid.hidpp.features.common.unifiedbattery import UnifiedBatteryV3
from pyhid.hidpp.features.common.unifiedbattery import UnifiedBatteryV4
from pyhid.hidpp.features.common.unifiedbattery import UnifiedBatteryV5
from pyhid.hidpp.features.test.root_test import RootTestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class UnifiedBatteryInstantiationTestCase(TestCase):
    """
    ``UnifiedBattery`` testing class
    """

    @staticmethod
    def test_unified_battery():
        """
        Tests ``UnifiedBattery`` class instantiation
        """
        my_class = UnifiedBattery(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = UnifiedBattery(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_unified_battery

    @staticmethod
    def test_get_capabilities():
        """
        Tests ``GetCapabilities`` class instantiation
        """
        my_class = GetCapabilitiesV0ToV5(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetCapabilitiesV0ToV5(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_capabilities

    @staticmethod
    def test_get_status():
        """
        Tests ``GetStatus`` class instantiation
        """
        my_class = GetStatusV0ToV5(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetStatusV0ToV5(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_status

    @staticmethod
    def test_get_capabilities_response():
        """
        Tests ``GetCapabilitiesResponseV0ToV1`` class instantiation
        """
        my_class = GetCapabilitiesResponseV0ToV1(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCapabilitiesResponseV0ToV1(device_index=0xFF, feature_index=0xFF, supported_level_full=True,
                                                 supported_level_good=True, supported_level_low=True,
                                                 supported_level_critical=True, soc_capability_flag=True,
                                                 rchg_capability_flag=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_capabilities_response

    @staticmethod
    def test_get_capabilities_response_v2():
        """
        Tests ``GetCapabilitiesResponseV2`` class instantiation
        """
        my_class = GetCapabilitiesResponseV2(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCapabilitiesResponseV2(device_index=0xFF, feature_index=0xFF, supported_level_full=True,
                                             supported_level_good=True, supported_level_low=True,
                                             supported_level_critical=True, show_capability_flag=True,
                                             soc_capability_flag=True, rchg_capability_flag=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_capabilities_response_v2

    @staticmethod
    def test_get_capabilities_response_v3():
        """
        Tests ``GetCapabilitiesResponseV3`` class instantiation
        """
        my_class = GetCapabilitiesResponseV3(device_index=0xFF, feature_index=0xFF, supported_level_full=False,
                                             supported_level_good=False, supported_level_low=False,
                                             supported_level_critical=False,
                                             battery_src_idx_capability_flag=False, show_capability_flag=False,
                                             soc_capability_flag=False, rchg_capability_flag=False,
                                             battery_source_index=0x00)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCapabilitiesResponseV3(device_index=0xFF, feature_index=0xFF, supported_level_full=True,
                                             supported_level_good=True, supported_level_low=True,
                                             supported_level_critical=True,
                                             battery_src_idx_capability_flag=True, show_capability_flag=True,
                                             soc_capability_flag=True, rchg_capability_flag=True,
                                             battery_source_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_capabilities_response_v3

    @staticmethod
    def test_get_capabilities_response_v4():
        """
        Tests ``GetCapabilitiesResponseV4`` class instantiation
        """
        my_class = GetCapabilitiesResponseV4(device_index=0, feature_index=0, supported_level_full=False,
                                             supported_level_good=False, supported_level_low=False,
                                             supported_level_critical=False, fast_charging_capability_flag=False,
                                             battery_src_idx_capability_flag=False, show_capability_flag=False,
                                             soc_capability_flag=False, rchg_capability_flag=False,
                                             battery_source_index=0x00)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCapabilitiesResponseV4(device_index=0xFF, feature_index=0xFF, supported_level_full=True,
                                             supported_level_good=True, supported_level_low=True,
                                             supported_level_critical=True, fast_charging_capability_flag=True,
                                             battery_src_idx_capability_flag=True, show_capability_flag=True,
                                             soc_capability_flag=True, rchg_capability_flag=True,
                                             battery_source_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_capabilities_response_v4

    @staticmethod
    def test_get_capabilities_response_v5():
        """
        Tests ``GetCapabilitiesResponseV5`` class instantiation
        """
        my_class = GetCapabilitiesResponseV5(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCapabilitiesResponseV5(device_index=0, feature_index=0, supported_level_full=False,
                                             supported_level_good=False, supported_level_low=False,
                                             supported_level_critical=False, removable_battery_capability_flag=False,
                                             fast_charging_capability_flag=True,
                                             battery_src_idx_capability_flag=False, show_capability_flag=False,
                                             soc_capability_flag=False, rchg_capability_flag=False,
                                             battery_source_index=0x00)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCapabilitiesResponseV5(device_index=0xFF, feature_index=0xFF, supported_level_full=True,
                                             supported_level_good=True, supported_level_low=True,
                                             supported_level_critical=True, removable_battery_capability_flag=True,
                                             fast_charging_capability_flag=True,
                                             battery_src_idx_capability_flag=True, show_capability_flag=True,
                                             soc_capability_flag=True, rchg_capability_flag=True,
                                             battery_source_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_capabilities_response_v5

    @staticmethod
    def test_get_status_response():
        """
        Tests ``GetStatusResponseV0ToV3`` class instantiation
        """

        my_class = GetStatusResponseV0ToV3(device_index=0, feature_index=0, state_of_charge=0,
                                           battery_level_full=False, battery_level_good=False, battery_level_low=False,
                                           battery_level_critical=False,
                                           charging_status=0,
                                           external_power_status=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetStatusResponseV0ToV3(device_index=0xFF, feature_index=0xFF, state_of_charge=0xFF,
                                           battery_level_full=True, battery_level_good=True, battery_level_low=True,
                                           battery_level_critical=True,
                                           charging_status=0xFF,
                                           external_power_status=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_status_response

    @staticmethod
    def test_get_status_response_v4():
        """
        Tests ``GetStatusResponseV4`` class instantiation
        """
        my_class = GetStatusResponseV4(device_index=0, feature_index=0, state_of_charge=0,
                                       battery_level_full=False, battery_level_good=False, battery_level_low=False,
                                       battery_level_critical=False,
                                       charging_status=0,
                                       external_power_status=0,
                                       fast_charging_status=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetStatusResponseV4(device_index=0xFF, feature_index=0xFF, state_of_charge=0xFF,
                                       battery_level_full=True, battery_level_good=True, battery_level_low=True,
                                       battery_level_critical=True,
                                       charging_status=0xFF,
                                       external_power_status=0xFF,
                                       fast_charging_status=False)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_status_response_v4

    @staticmethod
    def test_get_status_response_v5():
        """
        Tests ``GetStatusResponseV5`` class instantiation
        """
        my_class = GetStatusResponseV5(device_index=0, feature_index=0, state_of_charge=0,
                                       battery_level_full=False, battery_level_good=False, battery_level_low=False,
                                       battery_level_critical=False,
                                       charging_status=0,
                                       external_power_status=0,
                                       fast_charging_status=False,
                                       removable_battery_status=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetStatusResponseV5(device_index=0xFF, feature_index=0xFF, state_of_charge=0xFF,
                                       battery_level_full=True, battery_level_good=True, battery_level_low=True,
                                       battery_level_critical=True,
                                       charging_status=0xFF,
                                       external_power_status=0xFF,
                                       fast_charging_status=True,
                                       removable_battery_status=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_status_response_v5

    @staticmethod
    def test_show_battery_status():
        """
        Tests ``ShowBatteryStatusV1ToV5`` class instantiation
        """
        my_class = ShowBatteryStatusV1ToV5(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = ShowBatteryStatusV1ToV5(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_show_battery_status

    @staticmethod
    def test_show_battery_status_response():
        """
        Tests ``ShowBatteryStatusResponseV1ToV5`` class instantiation
        """
        my_class = ShowBatteryStatusResponseV1ToV5(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ShowBatteryStatusResponseV1ToV5(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_show_battery_status_response

    @staticmethod
    def test_battery_status_event():
        """
        Tests ``BatteryStatusEventV0ToV3`` class instantiation
        """
        my_class = BatteryStatusEventV0ToV3(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = BatteryStatusEventV0ToV3(device_index=0xFF, feature_index=0xFF, state_of_charge=0xFF,
                                            battery_level_full=True, battery_level_good=True, battery_level_low=True,
                                            battery_level_critical=True,
                                            charging_status=0xFF,
                                            external_power_status=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_battery_status_event

    @staticmethod
    def test_battery_status_event_v4():
        """
        Tests ``BatteryStatusEventV4`` class instantiation
        """
        my_class = BatteryStatusEventV4(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = BatteryStatusEventV4(device_index=0xFF, feature_index=0xFF, state_of_charge=0xFF,
                                        battery_level_full=True, battery_level_good=True, battery_level_low=True,
                                        battery_level_critical=True,
                                        charging_status=0xFF,
                                        external_power_status=0xFF,
                                        fast_charging_status=False)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_battery_status_event_v4

    @staticmethod
    def test_battery_status_event_v5():
        """
        Tests ``BatteryStatusEventV5`` class instantiation
        """
        my_class = BatteryStatusEventV5(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = BatteryStatusEventV5(device_index=0xFF, feature_index=0xFF, state_of_charge=0xFF,
                                        battery_level_full=True, battery_level_good=True, battery_level_low=True,
                                        battery_level_critical=True,
                                        charging_status=0xFF,
                                        external_power_status=0xFF,
                                        fast_charging_status=True,
                                        removable_battery_status=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_battery_status_event_v5
# end class UnifiedBatteryInstantiationTestCase


class UnifiedBatteryTestCase(TestCase):
    """
    ``UnifiedBattery`` factory model testing class
    """

    @classmethod
    def setUpClass(cls):
        cls.expected = {
            UnifiedBatteryV0.VERSION: {
                "cls": UnifiedBatteryV0,
                "interfaces": {
                    "get_capabilities_cls": GetCapabilitiesV0ToV5,
                    "get_status_cls": GetStatusV0ToV5,
                    "get_capabilities_response_cls": GetCapabilitiesResponseV0ToV1,
                    "get_status_response_cls": GetStatusResponseV0ToV3,
                },
                "max_function_index": 1
            },
            UnifiedBatteryV1.VERSION: {
                "cls": UnifiedBatteryV1,
                "interfaces": {
                    "get_capabilities_cls": GetCapabilitiesV0ToV5,
                    "get_status_cls": GetStatusV0ToV5,
                    "show_battery_status_cls": ShowBatteryStatusV1ToV5,
                    "get_capabilities_response_cls": GetCapabilitiesResponseV0ToV1,
                    "get_status_response_cls": GetStatusResponseV0ToV3,
                    "show_battery_status_response_cls": ShowBatteryStatusResponseV1ToV5,
                },
                "max_function_index": 2
            },
            UnifiedBatteryV2.VERSION: {
                "cls": UnifiedBatteryV2,
                "interfaces": {
                    "get_capabilities_cls": GetCapabilitiesV0ToV5,
                    "get_status_cls": GetStatusV0ToV5,
                    "show_battery_status_cls": ShowBatteryStatusV1ToV5,
                    "get_capabilities_response_cls": GetCapabilitiesResponseV2,
                    "get_status_response_cls": GetStatusResponseV0ToV3,
                    "show_battery_status_response_cls": ShowBatteryStatusResponseV1ToV5,
                },
                "max_function_index": 2
            },
            UnifiedBatteryV3.VERSION: {
                "cls": UnifiedBatteryV3,
                "interfaces": {
                    "get_capabilities_cls": GetCapabilitiesV0ToV5,
                    "get_status_cls": GetStatusV0ToV5,
                    "show_battery_status_cls": ShowBatteryStatusV1ToV5,
                    "get_capabilities_response_cls": GetCapabilitiesResponseV3,
                    "get_status_response_cls": GetStatusResponseV0ToV3,
                    "show_battery_status_response_cls": ShowBatteryStatusResponseV1ToV5,
                },
                "max_function_index": 2
            },
            UnifiedBatteryV4.VERSION: {
                "cls": UnifiedBatteryV4,
                "interfaces": {
                    "get_capabilities_cls": GetCapabilitiesV0ToV5,
                    "get_status_cls": GetStatusV0ToV5,
                    "show_battery_status_cls": ShowBatteryStatusV1ToV5,
                    "get_capabilities_response_cls": GetCapabilitiesResponseV4,
                    "get_status_response_cls": GetStatusResponseV4,
                    "show_battery_status_response_cls": ShowBatteryStatusResponseV1ToV5,
                },
                "max_function_index": 2
            },
            UnifiedBatteryV5.VERSION: {
                "cls": UnifiedBatteryV5,
                "interfaces": {
                    "get_capabilities_cls": GetCapabilitiesV0ToV5,
                    "get_status_cls": GetStatusV0ToV5,
                    "show_battery_status_cls": ShowBatteryStatusV1ToV5,
                    "get_capabilities_response_cls": GetCapabilitiesResponseV5,
                    "get_status_response_cls": GetStatusResponseV5,
                    "show_battery_status_response_cls": ShowBatteryStatusResponseV1ToV5,
                },
                "max_function_index": 2
            },
        }
    # end def setUpClass

    def test_unified_battery_factory(self):
        """
        Tests ``UnifiedBatteryFactory``
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(UnifiedBatteryFactory.create(version)), expected["cls"])
        # end for loop
    # end def test_unified_battery_factory

    def test_unified_battery_factory_version_out_of_range(self):
        """
        Tests ``UnifiedBatteryFactory`` with out of range versions
        """
        for version in [6, 7]:
            with self.assertRaises(KeyError):
                UnifiedBatteryFactory.create(version)
            # end with
        # end for
    # end def test_unified_battery_factory_version_out_of_range

    def test_unified_battery_factory_interfaces(self):
        """
        Check the ``UnifiedBatteryFactory`` returns its expected interfaces
        """
        for version, cls_map in self.expected.items():
            unified_battery = UnifiedBatteryFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(unified_battery, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(unified_battery, interface)
                # end if
            # end for loop
        # end for loop
    # end def test_unified_battery_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check get_max_function_index returns correct value at each version
        """
        for version, expected in self.expected.items():
            unified_battery = UnifiedBatteryFactory.create(version)
            self.assertEqual(unified_battery.get_max_function_index(), expected["max_function_index"])
        # end for loop
    # end def test_get_max_function_index
# end class UnifiedBatteryTestCase


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
