#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1004.interface
:brief: HID++ 2.0 Unified Battery interface test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/05/11
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.unifiedbatteryutils import UnifiedBatteryTestUtils
from pytestbox.device.hidpp20.common.feature_1004.unifiedbattery import UnifiedBatteryGenericTest


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class UnifiedBatteryInterfaceTestCase(UnifiedBatteryGenericTest):
    """
    Validates Unified Battery interface TestCases
    """
    @features('Feature1004')
    @level('Interface')
    def test_get_capabilities(self):
        """
        Test the get_capabilities request API.

        [0] get_capabilities() -> supported_levels, flags
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send get_capabilities request')
        # --------------------------------------------------------------------------------------------------------------
        get_capabilities_response = UnifiedBatteryTestUtils.HIDppHelper.get_capabilities(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for get_capabilities response and check product-specific constants')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.GetCapabilitiesResponseChecker.check_fields(
            test_case=self, message=get_capabilities_response,
            expected_cls=self.feature_1004.get_capabilities_response_cls)

        self.testCaseChecked("INT_1004_0001")
    # end def test_get_capabilities

    @features('Feature1004')
    @level('Interface')
    @services('PowerSupply')
    def test_get_status(self):
        """
        Test the get_status request API.

        [1] get_status() -> state_of_charge, battery_level, charging_status
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device with input voltage to its maximum value')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.power_reset_device_wait_wireless_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send get_status request')
        # --------------------------------------------------------------------------------------------------------------
        get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, 'Wait for get_status response and check battery_level is FULL and state_of_charge is 100%')
        # --------------------------------------------------------------------------------------------------------------
        checker = UnifiedBatteryTestUtils.GetStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge, 100),
            "battery_level_full": (checker.check_full_battery_level, 1)
        })
        UnifiedBatteryTestUtils.GetStatusResponseChecker.check_fields(
            test_case=self, message=get_status_response,
            expected_cls=self.feature_1004.get_status_response_cls, check_map=check_map)

        self.testCaseChecked("INT_1004_0002")
    # end def test_get_status

    @features('Feature1004v1+')
    @features('Feature1004ShowBatteryStatusCapability')
    @level('Interface')
    @services('PowerSupply')
    def test_show_battery_status(self):
        """
        Test the show_battery_status request API.

        [2] showBatteryStatus()
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device with input voltage to its maximum value')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.power_reset_device_wait_wireless_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send show_battery_status request')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.HIDppHelper.show_battery_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Battery Status LED behavior matches LED Guidelines')
        # --------------------------------------------------------------------------------------------------------------
        self.check_led_behaviour(battery_value=self.f.PRODUCT.DEVICE.BATTERY.F_MaximumVoltage)

        self.testCaseChecked("INT_1004_0004")
    # end def test_show_battery_status

    @features('Feature1004')
    @level('Interface')
    @services('PowerSupply')
    def test_battery_status_event(self):
        """
        Test the battery_status_event request API.

        [event0] battery_status_event() -> state_of_charge, battery_level, charging_status
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force battery level to its maximum value')
        # --------------------------------------------------------------------------------------------------------------
        UnifiedBatteryTestUtils.power_reset_device_wait_wireless_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, 'Wait for battery_status_event response and check battery_level is FULL and state_of_charge is 100%')
        # --------------------------------------------------------------------------------------------------------------
        battery_status_event = UnifiedBatteryTestUtils.wait_for_battery_status_event(
                                                    self, timeout=UnifiedBatteryTestUtils.BATTERY_MEASURE_BLIND_WINDOW)
        checker = UnifiedBatteryTestUtils.BatteryStatusEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "state_of_charge": (checker.check_state_of_charge, 100),
            "battery_level_full": (checker.check_full_battery_level, 1)
        })
        UnifiedBatteryTestUtils.BatteryStatusEventChecker.check_fields(
            test_case=self, message=battery_status_event,
            expected_cls=self.feature_1004.battery_status_event_cls, check_map=check_map)

        self.testCaseChecked("INT_1004_0003")
    # end def test_battery_status_event
# end class UnifiedBatteryInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
