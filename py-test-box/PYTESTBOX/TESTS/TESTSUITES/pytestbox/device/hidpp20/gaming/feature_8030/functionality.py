#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_8030.functionality
:brief: HID++ 2.0 ``MacroRecordkey`` functionality test suite
:author: Zane Lu <zlu@logitech.com>
:date: 2023/11/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.gaming.macrorecordkey import MacroRecordkey
from pylibrary.emulator.keyid import KEY_ID
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.macrorecordkeyutils import MacroRecordkeyTestUtils
from pytestbox.device.base.unifiedbatteryutils import UnifiedBatteryTestUtils
from pytestbox.device.hidpp20.gaming.feature_8030.macrorecordkey import MacroRecordkeyTestCase


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Zane Lu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MacroRecordkeyFunctionalityTestCase(MacroRecordkeyTestCase):
    """
    Validate ``MacroRecordkey`` functionality test cases
    """

    def _verify_mr_button_status_change_notification(self):
        """
        Verify receiving MR button status change notification when MR button is pressed.
        """
        ChannelUtils.empty_queues(test_case=self)
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press MR key")
        # ----------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.MR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check button report")
        # --------------------------------------------------------------------------------------------------------------
        response = MacroRecordkeyTestUtils.HIDppHelper.button_report_event(
            test_case=self,
            check_first_message=False)
        self.assertNotNone(obtained=response, msg="Shall get the button status event")
    # end def _verify_mr_button_status_change_notification

    @features("Feature8030")
    @level("Functionality")
    def test_to_check_receiving_the_button_status_change_notification(self):
        """
        Check that receiving the button status change notification
        """
        self._verify_mr_button_status_change_notification()
        self.testCaseChecked("FUN_8030_0001", _AUTHOR)
    # end def test_to_check_receiving_the_button_status_change_notification

    @features("Feature8030")
    @features('Feature1004')
    @level("Functionality")
    @services('PowerSupply')
    def test_to_check_receiving_the_button_status_change_notification_for_different_battery_levels(self):
        """
        Check that receiving the button status change notification for different battery levels
        """
        f = self.getFeatures()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over battery_level in range [FULL..CRITICAL]')
        # --------------------------------------------------------------------------------------------------------------
        for i in range(len(f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_SupportedLevels)):
            state_of_charge = int(f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_SupportedLevels[i])
            battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, state_of_charge)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set battery level to {battery_value}V')
            # ----------------------------------------------------------------------------------------------------------
            self.power_supply_emulator.set_voltage(battery_value)

            self._verify_mr_button_status_change_notification()
        # end for
        self.testCaseChecked("FUN_8030_0002", _AUTHOR)
    # end def test_to_check_receiving_the_button_status_change_notification_for_different_battery_levels

    @features("Feature8030")
    @features('Feature1004')
    @features('Rechargeable')
    @features('USBCharging')
    @level("Functionality")
    @services('PowerSupply')
    @services('Rechargeable')
    def test_to_check_receiving_the_button_status_change_notification_when_dut_is_charging(self):
        """
        Check that receiving the button status change notification when DUT is charging
        """
        DeviceTestUtils.ChargingHelper.enter_charging_mode(test_case=self)
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=MacroRecordkey.FEATURE_ID)
        self._verify_mr_button_status_change_notification()
        self.testCaseChecked("FUN_8030_0003", _AUTHOR)
    # end def test_to_check_receiving_the_button_status_change_notification_when_dut_is_charging

    @features("Feature8030")
    @level("Functionality")
    def test_to_check_a_single_button_report_when_mr_button_pressed_for_2_seconds(self):
        """
        Check a single ButtonReport when MR button pressed for 2 seconds
        """
        ChannelUtils.empty_queues(test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press MR key for 2 seconds")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=KEY_ID.MR)
        sleep(2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check button report")
        # --------------------------------------------------------------------------------------------------------------
        response = MacroRecordkeyTestUtils.HIDppHelper.button_report_event(
            test_case=self,
            check_first_message=False)
        self.assertNotNone(obtained=response, msg="Shall get the button status event")

        response = MacroRecordkeyTestUtils.HIDppHelper.button_report_event(
            test_case=self,
            check_first_message=False,
            allow_no_message=True)
        self.assertNone(obtained=response, msg="Shall be no button status event")

        self.testCaseChecked("FUN_8030_0004", _AUTHOR)
    # end def test_to_check_a_single_button_report_when_mr_button_pressed_for_2_seconds

    @features("Feature8030")
    @level("Functionality")
    def test_to_check_a_single_button_report_for_mr_button_while_other_keys_are_already_pressed(self):
        """
        Check a single ButtonReport for MR button pressed while other keys are already pressed
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press 'a' key")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=KEY_ID.KEYBOARD_A)

        ChannelUtils.empty_queues(test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press MR key")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=KEY_ID.MR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check button report")
        # --------------------------------------------------------------------------------------------------------------
        response = MacroRecordkeyTestUtils.HIDppHelper.button_report_event(
            test_case=self,
            check_first_message=False)
        self.assertNotNone(obtained=response, msg="Shall get the button status event")

        response = MacroRecordkeyTestUtils.HIDppHelper.button_report_event(
            test_case=self,
            check_first_message=False,
            allow_no_message=True)
        self.assertNone(obtained=response, msg="Shall be no button status event")

        self.testCaseChecked("FUN_8030_0005", _AUTHOR)
    # end def test_to_check_a_single_button_report_for_mr_button_while_other_keys_are_already_pressed
# end class MacroRecordkeyFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
