#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
""" @package pyhid.hidpp.feature.common.test.wirelessdevicestatus_test

@brief  HID++ 2.0 PowerModes test module

@author Stanislas Cottard

@date   2019/04/04
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatus
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.features.test.root_test import RootTestCase
from unittest import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class WirelessDeviceStatusCase(TestCase):
    """
    WirelessDeviceStatus testing class
    """

    @staticmethod
    def test_wireless_device_status():
        """
        Tests WirelessDeviceStatus class instantiation
        """
        my_class = WirelessDeviceStatus(device_index=0,
                                        feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = WirelessDeviceStatus(device_index=0xFF,
                                        feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_wireless_device_status

    @staticmethod
    def test_wireless_device_status_broadcast_event ():
        """
        Tests WirelessDeviceStatusBroadcastEvent class instantiation
        """
        my_class = WirelessDeviceStatusBroadcastEvent(device_index=0,
                                                      feature_id=0,
                                                      status=0,
                                                      request=0,
                                                      reason=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = WirelessDeviceStatusBroadcastEvent(device_index=0xFF,
                                                      feature_id=0xFF,
                                                      status=0xFF,
                                                      request=0xFF,
                                                      reason=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_wireless_device_status_broadcast_event
# end class WirelessDeviceStatusCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
