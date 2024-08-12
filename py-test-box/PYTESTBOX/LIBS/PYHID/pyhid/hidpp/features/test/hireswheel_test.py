#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
""" @package pyhid.hidpp.feature.test.hireswheel_test

@brief  HID++ 2.0 HiRes Wheel test module

@author Andy Su

@date   2019/04/08
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList
from pyhid.hidpp.features.hireswheel import HiResWheel
from pyhid.hidpp.features.hireswheel import HiResWheelModel
from pyhid.hidpp.features.hireswheel import HiResWheelInterface
from pyhid.hidpp.features.hireswheel import HiResWheelFactory
from pyhid.hidpp.features.hireswheel import HiResWheelV0
from pyhid.hidpp.features.hireswheel import HiResWheelV1
from pyhid.hidpp.features.hireswheel import GetWheelCapability
from pyhid.hidpp.features.hireswheel import GetWheelCapabilityResponse
from pyhid.hidpp.features.hireswheel import GetWheelMode
from pyhid.hidpp.features.hireswheel import GetWheelModeResponse
from pyhid.hidpp.features.hireswheel import SetWheelModev0
from pyhid.hidpp.features.hireswheel import SetWheelModev0Response
from pyhid.hidpp.features.hireswheel import GetWheelCapabilityv1Response
from pyhid.hidpp.features.hireswheel import GetWheelModev1Response
from pyhid.hidpp.features.hireswheel import SetWheelModev1
from pyhid.hidpp.features.hireswheel import SetWheelModev1Response
from pyhid.hidpp.features.hireswheel import GetRatchetSwitchState
from pyhid.hidpp.features.hireswheel import GetRatchetSwitchStateResponse
from pyhid.hidpp.features.hireswheel import GetAnalyticsData
from pyhid.hidpp.features.hireswheel import GetAnalyticsDataResponse
from pyhid.hidpp.features.hireswheel import GetAnalyticsDataHERZOGResponse
from pyhid.hidpp.features.hireswheel import WheelMovementEvent
from pyhid.hidpp.features.hireswheel import RatchetSwitchEvent
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.features.test.root_test import RootTestCase
from unittest import TestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class HiResWheelTestCase(TestCase):
    """
    HiResWheel testing class
    """

    def test_hireswheel(self):
        """
        Tests HiRes Wheel class instantiation
        """
        my_class = HiResWheel(deviceIndex=0,
                              featureIndex=0x22)

        RootTestCase._top_level_class_checker(my_class)

    # end def test_hireswheel

    def test_get_wheel_capability_v0(self):
        """
        Tests GetWheelCapability v0 class instantiation
        """
        my_class = GetWheelCapability(deviceIndex=0,
                                      featureId=0x22)

        RootTestCase._short_function_class_checker(my_class)

    # end def test_get_wheel_capability_v0

    def test_get_wheel_capability_response_v0(self):
        """
        Tests GetWheelCapabilityResponse v0 class instantiation
        """
        my_class = GetWheelCapabilityResponse(deviceIndex=0,
                                              featureId=0x22,
                                              multiplier=0,
                                              reserved1=0,
                                              hasInvert=0,
                                              hasSwitch=0,
                                              reserved2=0)

        RootTestCase._long_function_class_checker(my_class)

    # end def test_get_wheel_capability_response_v0

    def test_get_wheel_capability_response_v1(self):
        """
        Tests GetWheelCapabilityResponse v1 class instantiation
        """
        my_class = GetWheelCapabilityv1Response(deviceIndex=0,
                                                featureId=0x22,
                                                multiplier=0,
                                                reserved1=0,
                                                hasAnalyticsData=0,
                                                hasInvert=0,
                                                hasSwitch=0,
                                                reserved2=0,
                                                ratchetsPerRotation=0,
                                                wheelDiameter=0)

        RootTestCase._long_function_class_checker(my_class)

    # end def test_get_wheel_capability_response_v1

    def test_get_wheel_mode_v0(self):
        """
        Tests GetWheelMode v0 class instantiation
        """
        my_class = GetWheelMode(deviceIndex=0,
                                featureId=0x22)

        RootTestCase._short_function_class_checker(my_class)

    # end def test_get_wheel_mode_v0

    def test_get_wheel_mode_response_v0(self):
        """
        Tests GetWheelModeResponse v0 class instantiation
        """
        my_class = GetWheelModeResponse(deviceIndex=0,
                                        featureId=0x22,
                                        reserved=0,
                                        invert=0,
                                        resolution=0,
                                        target=0)

        RootTestCase._long_function_class_checker(my_class)

    # end def test_get_wheel_mode_response_v0

    def test_get_wheel_mode_response_v1(self):
        """
        Tests GetWheelModeResponse v1 class instantiation
        """
        my_class = GetWheelModev1Response(deviceIndex=0,
                                          featureId=0x22,
                                          reserved=0,
                                          analytics=0,
                                          invert=0,
                                          resolution=0,
                                          target=0)

        RootTestCase._long_function_class_checker(my_class)

    # end def test_get_wheel_mode_response_v1

    def test_set_wheel_mode_v0(self):
        """
        Tests SetWheelMode v0 class instantiation
        """
        my_class = SetWheelModev0(deviceIndex=0,
                                  featureId=0x22,
                                  reserved=0,
                                  invert=0,
                                  resolution=0,
                                  target=0)

        RootTestCase._short_function_class_checker(my_class)

    # end def test_set_wheel_mode_v0

    def test_set_wheel_mode_response_v0(self):
        """
        Tests SetWheelModeResponse v0 class instantiation
        """
        my_class = SetWheelModev0Response(deviceIndex=0,
                                          featureId=0x22,
                                          reserved=0,
                                          invert=0,
                                          resolution=0,
                                          target=0)

        RootTestCase._long_function_class_checker(my_class)

    # end def test_set_wheel_mode_response_v0

    def test_set_wheel_mode_v1(self):
        """
        Tests SetWheelMode v1 class instantiation
        """
        my_class = SetWheelModev1(deviceIndex=0,
                                  featureId=0x22,
                                  reserved=0,
                                  analytics=0,
                                  invert=0,
                                  resolution=0,
                                  target=0)

        RootTestCase._short_function_class_checker(my_class)

    # end def test_set_wheel_mode_v1

    def test_set_wheel_mode_response_v1(self):
        """
        Tests SetWheelModeResponse v1 class instantiation
        """
        my_class = SetWheelModev1Response(deviceIndex=0,
                                          featureId=0x22,
                                          reserved=0,
                                          analytics=0,
                                          invert=0,
                                          resolution=0,
                                          target=0)

        RootTestCase._long_function_class_checker(my_class)

    # end def test_set_wheel_mode_response_v1

    def test_get_ratchet_switch_state(self):
        """
        Tests GetRatchetSwitchState class instantiation
        """
        my_class = GetRatchetSwitchState(deviceIndex=0,
                                         featureId=0x22)

        RootTestCase._short_function_class_checker(my_class)

    # end def test_get_ratchet_switch_state

    def test_get_ratchet_switch_state_response(self):
        """
        Tests GetRatchetSwitchStateResponse class instantiation
        """
        my_class = GetRatchetSwitchStateResponse(deviceIndex=0,
                                                 featureId=0x22,
                                                 reserved=0,
                                                 state=0)

        RootTestCase._long_function_class_checker(my_class)

    # end def test_get_ratchet_switch_state_response

    def test_get_analytics_data(self):
        """
        Tests GetAnalyticsData class instantiation
        """
        my_class = GetAnalyticsData(deviceIndex=0,
                                    featureId=0x22)

        RootTestCase._short_function_class_checker(my_class)

    # end def test_get_analytics_data

    def test_get_analytics_data_response(self):
        """
        Tests GetAnalyticsDataResponse class instantiation
        """
        my_class = GetAnalyticsDataResponse(deviceIndex=0,
                                            featureId=0x22,
                                            analyticsData=0)

        RootTestCase._long_function_class_checker(my_class)

    # end def test_get_analytics_data_response

    def test_get_analytics_data_response(self):
        """
        Tests GetAnalyticsDataHERZOGResponse class instantiation
        """
        my_class = GetAnalyticsDataHERZOGResponse(deviceIndex=0,
                                                  featureId=0x22,
                                                  initEpmChargeAdcBattLevel=0,
                                                  epmChargingTime=0,
                                                  endEpmChargeAdcBattLevel=0,
                                                  temperature=0)

        RootTestCase._long_function_class_checker(my_class)

    # end def test_get_analytics_data_response

    def test_wheel_movement(self):
        """
        Tests WheelMovement class instantiation
        """
        my_class = WheelMovementEvent(deviceIndex=0,
                                      featureId=0x22,
                                      reserved=0,
                                      resolution=0,
                                      periods=0,
                                      deltaV=0)

        RootTestCase._long_function_class_checker(my_class)

    # end def test_wheel_movement

    def test_ratchet_switch(self):
        """
        Tests RatchetSwitch class instantiation
        """
        my_class = RatchetSwitchEvent(deviceIndex=0,
                                      featureId=0x22,
                                      reserved=0,
                                      state=0)

        RootTestCase._long_function_class_checker(my_class)

    # end def test_ratchet_switch

# end class HiResWheelTestCase


class HiResWheelTestCase(TestCase):
    """
    Dfu Control factory testing
    """

    @classmethod
    def setUpClass(cls):
        cls.expected = {
            0: {
                "cls": HiResWheelV0,
                "interfaces": {
                    "get_wheel_capability_cls": GetWheelCapability,
                    "get_wheel_mode_cls": GetWheelMode,
                    "set_wheel_mode_cls": SetWheelModev0,
                    "get_ratchet_switch_state_cls": GetRatchetSwitchState,
                    "get_wheel_capability_response_cls": GetWheelCapabilityResponse,
                    "get_wheel_mode_response_cls": GetWheelModeResponse,
                    "set_wheel_mode_response_cls": SetWheelModev0Response,
                    "get_ratchet_switch_state_response_cls": GetRatchetSwitchStateResponse,
                },
                "max_function_index": 3
            },
            1: {
                "cls": HiResWheelV1,
                "interfaces": {
                    "get_wheel_capability_cls": GetWheelCapability,
                    "get_wheel_mode_cls": GetWheelMode,
                    "set_wheel_mode_cls": SetWheelModev1,
                    "get_ratchet_switch_state_cls": GetRatchetSwitchState,
                    "get_analytics_data_cls": GetAnalyticsData,
                    "get_wheel_capability_response_cls": GetWheelCapabilityv1Response,
                    "get_wheel_mode_response_cls": GetWheelModev1Response,
                    "set_wheel_mode_response_cls": SetWheelModev1Response,
                    "get_ratchet_switch_state_response_cls": GetRatchetSwitchStateResponse,
                    "get_analytics_data_response_cls": GetAnalyticsDataResponse,
                },
                "max_function_index": 4
            },
        }
    # end def setUpClass

    def test_high_resolution_wheel_factory(self):
        """
        Tests High Resolution Wheel Factory
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(HiResWheelFactory.create(version)), expected["cls"])
        # end for loop

    # end def test_high_resolution_wheel_factory

    def test_high_resolution_wheel_factory_version_out_of_range(self):
        """
        Tests High Resolution Wheel Factory with out of range versions
        """
        for version in [2, 3]:
            with self.assertRaises(KeyError):
                HiResWheelFactory.create(version)
            # end with
        # end for
    # end def test_high_resolution_wheel_factory_version_out_of_range

    def test_high_resolution_wheel_factory_interfaces(self):
        """
        Check High Resolution Wheel Factory returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            high_resolution_wheel = HiResWheelFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(high_resolution_wheel, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(high_resolution_wheel, interface)
                # end if
            # end for loop
        # end for loop
    # end def test_high_resolution_wheel_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check get_max_function_index returns correct value at each version
        """
        for version, expected in self.expected.items():
            high_resolution_wheel = HiResWheelFactory.create(version)
            self.assertEqual(high_resolution_wheel.get_max_function_index(), expected["max_function_index"])
        # end for loop
    # end def test_get_max_function_index
# end class HiResWheelTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
