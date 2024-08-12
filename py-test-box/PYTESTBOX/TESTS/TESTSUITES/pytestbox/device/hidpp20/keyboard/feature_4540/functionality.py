#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.keyboard.feature_4540.functionality
:brief: HID++ 2.0 ``KeyboardInternationalLayouts`` functionality test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/12/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.keyboard.keyboardinternationallayouts import KeyboardInternationalLayouts
from pyhid.hidpp.features.keyboard.keyboardinternationallayouts import KeyboardInternationalLayouts as KBDLayout
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.configurablepropertiesutils import ConfigurablePropertiesTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.keyboardinternationallayoutsutils import KeyboardInternationalLayoutsTestUtils as KBDUtils
from pytestbox.device.base.unifiedbatteryutils import UnifiedBatteryTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4540.keyboardinternationallayouts \
    import KeyboardInternationalLayoutsTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class KeyboardInternationalLayoutsFunctionalityTestCase(KeyboardInternationalLayoutsTestCase):
    """
    Validate ``KeyboardInternationalLayouts`` functionality test cases
    """

    @features("Feature4540")
    @features("Feature1802")
    @features("Feature1807")
    @level("Functionality")
    @services("Debugger")
    def test_set_all_supported_layout_id(self):
        """
        Check the firmware returned the correct keyboard international layout value for every supported keyboard
        layout configured in DUT NVS
         - write keyboard layout property with data in range [2 to max]
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over multiple values of keyboard layout in [2..Max]")
        # --------------------------------------------------------------------------------------------------------------
        for layout_id in range(KBDLayout.LAYOUT.US_INTERNATIONAL_105_KEYS, self.feature_4540.get_max_layout_id() + 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Select keyboard_layout Property")
            # ----------------------------------------------------------------------------------------------------------
            ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id=KBDLayout.PROPERTY_ID)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Set keyboard_layout data with the selected layout id = {layout_id}")
            # ----------------------------------------------------------------------------------------------------------
            ConfigurablePropertiesTestUtils.HIDppHelper.write_data(self, data=HexList(layout_id))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Reset the device")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.ResetHelper.hidpp_reset(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "After reset once again enable manufacturing feature")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetKeyboardLayout")
            # ----------------------------------------------------------------------------------------------------------
            response = KBDUtils.HIDppHelper.get_keyboard_layout(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Validate the keyboard layout matches with selected layout id = {layout_id}")
            # ----------------------------------------------------------------------------------------------------------
            checker = KBDUtils.GetKeyboardLayoutResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({"keyboard_layout": (checker.check_keyboard_layout, HexList(layout_id))})
            checker.check_fields(self, response, self.feature_4540.get_keyboard_layout_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_4540_0001", _AUTHOR)
    # end def test_set_all_supported_layout_id

    @features("Feature4540")
    @features("Feature1802")
    @features("Feature1807")
    @level("Functionality")
    @services("Debugger")
    def test_set_unknown_layout(self):
        """
        Check the firmware reports keyboard layout to 'Unknown' 
        
         - write keyboard layout property with data = 0
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Select keyboard_layout Property")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id=KBDLayout.PROPERTY_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set keyboard_layout data with the layout id as 0 (unknown)")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.write_data(self, KBDLayout.LAYOUT.UNKNOWN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset the device")
        # --------------------------------------------------------------------------------------------------------------
        KBDUtils.ResetHelper.hidpp_reset(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetKeyboardLayout")
        # --------------------------------------------------------------------------------------------------------------
        response = KBDUtils.HIDppHelper.get_keyboard_layout(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the keyboard layout returned as unknown(0)")
        # --------------------------------------------------------------------------------------------------------------
        checker = KBDUtils.GetKeyboardLayoutResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({"keyboard_layout": (checker.check_keyboard_layout, KBDLayout.LAYOUT.UNKNOWN)})
        checker.check_fields(self, response, self.feature_4540.get_keyboard_layout_response_cls, check_map)

        self.testCaseChecked("FUN_4540_0002", _AUTHOR)
    # end def test_set_unknown_layout

    @features("Feature4540")
    @features("Feature1802")
    @features("Feature1807")
    @level("Functionality")
    @services("Debugger")
    def test_set_unsupported_layout_id(self):
        """
        Check the firmware behavior when the keyboard layout value is greater than the max defined value
         - write keyboard layout property with data in range [max+1 to 255]
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over multiple values of keyboard layout in [Max+1..255]")
        # --------------------------------------------------------------------------------------------------------------
        for layout_id in compute_sup_values(self.feature_4540.get_max_layout_id()):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Select keyboard_layout Property")
            # ----------------------------------------------------------------------------------------------------------
            ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id=KBDLayout.PROPERTY_ID)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Set keyboard_layout data with the selected layout id = {layout_id}")
            # ----------------------------------------------------------------------------------------------------------
            ConfigurablePropertiesTestUtils.HIDppHelper.write_data(self, layout_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Reset the device")
            # ----------------------------------------------------------------------------------------------------------
            KBDUtils.ResetHelper.hidpp_reset(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "After reset once again enable manufacturing feature")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetKeyboardLayout")
            # ----------------------------------------------------------------------------------------------------------
            response = KBDUtils.HIDppHelper.get_keyboard_layout(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Validate the keyboard layout matches with selected layout id = {layout_id}")
            # ----------------------------------------------------------------------------------------------------------
            checker = KBDUtils.GetKeyboardLayoutResponseChecker
            check_map = checker.get_default_check_map(self)
            # Set unsupported layout id, gaming keyboard will change it to United States (US).
            # Note: Gaming keyboards applied the patch at 2024/05/08
            # https://goldenpass.logitech.com:8443/plugins/gitiles/ccp_fw/mpk25_cinderella_tkl/+/e592acff88024b5689fd1942d0ae6242cb20fe8f
            check_map.update({"keyboard_layout": (checker.check_keyboard_layout,
                                                  layout_id if not self.f.PRODUCT.F_IsGaming else
                                                  KeyboardInternationalLayouts.LAYOUT.US)})
            checker.check_fields(self, response, self.feature_4540.get_keyboard_layout_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_4540_0003", _AUTHOR)
    # end def test_set_unsupported_layout_id

    @features("Feature4540")
    @features("Feature1004")
    @level("Functionality")
    @services("Debugger")
    @services("PowerSupply")
    def test_check_kbd_layout_critical_battery(self):
        """
        Check the keyboard layout value is not impacted by a critical battery level
         - set voltage to a critical level
        
        Require power supply
        """
        self.post_requisite_set_nominal_voltage = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get current keyboard layout value from GetKeyboardLayout")
        # --------------------------------------------------------------------------------------------------------------
        initial_kbd_layout = KBDUtils.HIDppHelper.get_keyboard_layout(self).keyboard_layout

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set Power to critical voltage using power supply")
        # --------------------------------------------------------------------------------------------------------------
        critical_voltage = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(
            self, UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'critical'))
        self.power_supply_emulator.set_voltage(critical_voltage)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetKeyboardLayout request")
        # --------------------------------------------------------------------------------------------------------------
        kbd_layout_at_critical_voltage = KBDUtils.HIDppHelper.get_keyboard_layout(self).keyboard_layout

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate keyboard layout value is unchanged whatever the voltage")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=to_int(initial_kbd_layout),
            obtained=to_int(kbd_layout_at_critical_voltage),
            msg="The keyboard_layout parameter differs before and after critical voltage"
                f"(expected:{initial_kbd_layout}, obtained:{kbd_layout_at_critical_voltage})")

        self.testCaseChecked("FUN_4540_0004", _AUTHOR)
    # end def test_check_kbd_layout_critical_battery

    @features("Feature4540")
    @features("Rechargeable")
    @level("Functionality")
    @services("Debugger")
    @services("PowerSupply")
    @services("Rechargeable")
    def test_check_kbd_layout_usb_charging_impact(self):
        """
        Check the keyboard layout value is not impacted by USB charging
        
         - plug in the USB cable
        """
        self.post_requisite_unplug_usb_cable = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get current keyboard layout value from GetKeyboardLayout")
        # --------------------------------------------------------------------------------------------------------------
        initial_kbd_layout = KBDUtils.HIDppHelper.get_keyboard_layout(self).keyboard_layout

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Turn on USB Charging Cable")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.ChargingHelper.enter_charging_mode(test_case=self)
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=KeyboardInternationalLayouts.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetKeyboardLayout request")
        # --------------------------------------------------------------------------------------------------------------
        kbd_layout_during_usb_charging = KBDUtils.HIDppHelper.get_keyboard_layout(self).keyboard_layout

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate keyboard layout value is unchanged whatever the charging state")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=to_int(initial_kbd_layout),
                         obtained=to_int(kbd_layout_during_usb_charging),
                         msg="The keyboard_layout parameter differs before and after USB charging"
                             f"(expected:{initial_kbd_layout}, obtained:"
                             f"{kbd_layout_during_usb_charging})")

        self.testCaseChecked("FUN_4540_0005", _AUTHOR)
    # end def test_check_kbd_layout_usb_charging_impact
# end class KeyboardInternationalLayoutsFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
