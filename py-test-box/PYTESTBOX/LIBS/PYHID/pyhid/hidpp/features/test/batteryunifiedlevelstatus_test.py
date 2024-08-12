#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
""" @package pyhid.hidpp.feature.test.batteryunifiedlevelstatus_test

@brief  HID++ 2.0 Battery Unified Level Status test module

@author Andy Su

@date   2019/04/08
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList
from pyhid.hidpp.features.batteryunifiedlevelstatus import BatteryUnifiedLevelStatus
from pyhid.hidpp.features.batteryunifiedlevelstatus import GetBatteryLevelStatus
from pyhid.hidpp.features.batteryunifiedlevelstatus import GetBatteryLevelStatusResponse
from pyhid.hidpp.features.batteryunifiedlevelstatus import GetBatteryCapability
from pyhid.hidpp.features.batteryunifiedlevelstatus import GetBatteryCapabilityResponse
from pyhid.hidpp.features.batteryunifiedlevelstatus import ShowBatteryStatus
from pyhid.hidpp.features.batteryunifiedlevelstatus import ShowBatteryStatusResponse
from pyhid.hidpp.features.batteryunifiedlevelstatus import BatteryLevelStatusBroadcastEvent
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.features.test.root_test import RootTestCase
from unittest import TestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class BatteryUnifiedLevelStatusTestCase(TestCase):
    """
    BatteryUnifiedLevelStatus testing class
    """

    def test_batteryunifiedlevelstatus(self):
        """
        Tests Battery Unified Level Status class instantiation
        """
        my_class = BatteryUnifiedLevelStatus(deviceIndex=0,
                                             featureIndex=0x10)

        RootTestCase._top_level_class_checker(my_class)

    # end def test_batteryunifiedlevelstatus

    def test_get_battery_level_status(self):
        """
        Tests GetBatteryLevelStatus class instantiation
        """
        my_class = GetBatteryLevelStatus(deviceIndex=0,
                                         featureId=0x10)

        RootTestCase._short_function_class_checker(my_class)

    # end def test_get_battery_level_status

    def test_get_battery_level_status_response(self):
        """
        Tests GetBatteryLevelStatusResponse class instantiation
        """
        my_class = GetBatteryLevelStatusResponse(deviceIndex=0,
                                                 featureId=0x10,
                                                 batteryDischargeLevel=0,
                                                 batteryDischargeNextLevel=0,
                                                 batteryStatus=0)

        RootTestCase._long_function_class_checker(my_class)

    # end def test_test_get_battery_level_status_response

    def test_get_battery_capability(self):
        """
        Tests GetBatteryCapability class instantiation
        """
        my_class = GetBatteryCapability(deviceIndex=0,
                                        featureId=0x10)

        RootTestCase._short_function_class_checker(my_class)

    # end def test_get_battery_capability

    def test_get_battery_capability_response(self):
        """
        Tests GetBatteryCapabilityResponse class instantiation
        """
        my_class = GetBatteryCapabilityResponse(deviceIndex=0,
                                                featureId=0x10,
                                                numberOfLevels=0,
                                                flags=0,
                                                nominalBatteryLife=0,
                                                batteryCriticalLevel=0)

        RootTestCase._long_function_class_checker(my_class)

    # end def test_get_battery_capability_response

    def test_show_battery_status(self):
        """
        Tests ShowBatteryStatus class instantiation
        """
        my_class = ShowBatteryStatus(deviceIndex=0,
                                     featureId=0x10)

        RootTestCase._short_function_class_checker(my_class)

    # end def test_show_battery_status

    def test_show_battery_status_response(self):
        """
        Tests ShowBatteryStatusResponse class instantiation
        """
        my_class = ShowBatteryStatusResponse(deviceIndex=0,
                                             featureId=0x10)

        RootTestCase._long_function_class_checker(my_class)

    # end def test_show_battery_status_response

    def test_battery_level_status_broadcast_event(self):
        """
        Tests BatteryLevelStatusBroadcastEvent class instantiation
        """
        my_class = BatteryLevelStatusBroadcastEvent(deviceIndex=0,
                                                    featureId=0x10,
                                                    batteryDischargeLevel=0,
                                                    batteryDischargeNextLevel=0,
                                                    batteryStatus=0)

        RootTestCase._long_function_class_checker(my_class)

    # end def test_battery_level_status_broadcast_event

# end class BatteryUnifiedLevelStatusTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
