#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.keyboard.feature_4220.functionality
:brief: HID++ 2.0 ``LockKeyState`` functionality test suite
:author: Anil Gadad <agadad@logitech.com>
:date: 2022/04/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.emulator.ledid import LOCK_KEYS_LEDS
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.connectionschemeutils import BleProConnectionSchemeTestUtils
from pytestbox.device.base.unifiedbatteryutils import UnifiedBatteryTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4220.lockkeystate import LockKeyStateTestCase


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Anil Gadad"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LockKeyStateFunctionalityTestCase(LockKeyStateTestCase):
    """
    Validate ``LockKeyState`` functionality test cases
    """

    @features("Feature4220")
    @level("Functionality")
    @services('RequiredKeys', (KEY_ID.KEYBOARD_CAPS_LOCK,))
    def test_lock_key_change_event_caps_lock(self):
        """
        Validate LockKeyState value in LockKeyChange event matches the LED indicator state sent by the host
        """
        for delay in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
            keys = dict(CapsLock=True)
            self.set_keys(keys)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Wait for delay: {delay}")
            # ----------------------------------------------------------------------------------------------------------
            sleep(delay)

            self.check_lock_key_change_event(keys)

            keys = dict()
            self.set_keys(keys)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Wait for delay: {delay}")
            # ----------------------------------------------------------------------------------------------------------
            sleep(delay)

            self.check_lock_key_change_event(keys)
        # end for

        self.testCaseChecked("FUN_4220_0001", _AUTHOR)
    # end def test_lock_key_change_event_caps_lock

    @features("Feature4220")
    @level("Functionality")
    @services('RequiredKeys', (KEY_ID.KEYBOARD_CAPS_LOCK,))
    def test_caps_lock_led_indicator_without_backlight(self):
        """
        Validate Caps Lock LED indicator matches the LED indicator state sent by the host on keyboard without backlight
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Start LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        keys = dict(CapsLock=True)
        self.set_keys(keys)
        self.check_lock_key_change_event(keys)
        self.check_led_state_on(keys)

        keys = dict()
        self.set_keys(keys)
        self.check_lock_key_change_event(keys)
        self.check_led_state_off()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        self.testCaseChecked("FUN_4220_0002", _AUTHOR)
    # end def test_caps_lock_led_indicator_without_backlight

    @features("Feature4220")
    @level("Functionality")
    @services('RequiredKeys', (KEY_ID.KEYBOARD_CAPS_LOCK,))
    def test_caps_lock_led_indicator_with_backlight(self):
        """
        Validate Caps Lock LED indicator matches the LED indicator state sent by the host on keyboard with backlight
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Start LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        keys = dict(CapsLock=True)
        self.set_keys(keys)
        self.check_lock_key_change_event(keys)
        self.check_led_state_blink(keys)

        keys = dict()
        self.set_keys(keys)
        self.check_lock_key_change_event(keys)
        self.check_led_state_off()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        self.testCaseChecked("FUN_4220_0003", _AUTHOR)
    # end def test_caps_lock_led_indicator_with_backlight

    @features("Feature4220")
    @level("Functionality")
    @services('RequiredKeys', (KEY_ID.KEYBOARD_CAPS_LOCK,))
    @services('MultiHost')
    def test_caps_lock_led_indicator(self):
        """
        Validate Caps lock LED indicator stays active for 5 minutes after the last user activity
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Start LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        keys = dict(CapsLock=True)
        self.set_keys(keys)
        self.check_lock_key_change_event(keys)
        self.check_led_state_blink(keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power off receiver")
        # --------------------------------------------------------------------------------------------------------------
        port_index = ChannelUtils.get_port_index(test_case=self)
        self.channel_disable(usb_port_index=port_index)

        self.check_led_state_blink(keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wait for 5 minutes")
        # --------------------------------------------------------------------------------------------------------------
        sleep(300)

        self.check_led_state_off()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Power on receiver")
        # --------------------------------------------------------------------------------------------------------------
        self.channel_enable(usb_port_index=port_index, wait_device_notification=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)
        self.testCaseChecked("FUN_4220_0004", _AUTHOR)
    # end def test_caps_lock_led_indicator

    @features("Feature4220")
    @level("Functionality")
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LOCKING_NUM_LOCK,))
    def test_num_lock_led_event(self):
        """
        Validate Num Lock LED indicator matches the LED indicator state sent by the host
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Start LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        keys = dict(NumLock=True)
        self.set_keys(keys)
        self.check_lock_key_change_event(keys)
        self.check_led_state_on(keys)

        keys = dict()
        self.set_keys(keys)
        self.check_lock_key_change_event(keys)
        self.check_led_state_off()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        self.testCaseChecked("FUN_4220_0005", _AUTHOR)
    # end def test_num_lock_led_event

    @features("Feature4220")
    @level("Functionality")
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LOCKING_NUM_LOCK,))
    def test_num_lock_led_indicator(self):
        """
        Validate Num lock LED indicator stays active for 5 minutes after the last user activity
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Start LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        keys = dict(NumLock=True)
        self.set_keys(keys)
        self.check_lock_key_change_event(keys)
        self.check_led_state_on(keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power off receiver")
        # --------------------------------------------------------------------------------------------------------------
        port_index = ChannelUtils.get_port_index(test_case=self)
        self.channel_disable(usb_port_index=port_index)

        self.check_led_state_on(keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wait for 5 minutes")
        # --------------------------------------------------------------------------------------------------------------
        sleep(300)

        self.check_led_state_off()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Power on receiver")
        # --------------------------------------------------------------------------------------------------------------
        self.channel_enable(usb_port_index=port_index, wait_device_notification=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        self.testCaseChecked("FUN_4220_0006", _AUTHOR)
    # end def test_num_lock_led_indicator

    @features("Feature4220")
    @level("Functionality")
    @services('RequiredKeys', (KEY_ID.KEYBOARD_SCROLL_LOCK,))
    def test_scroll_lock_led_event(self):
        """
        Validate Scroll Lock LED indicator matches the LED indicator state sent by the host
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Start LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        keys = dict(ScrollLock=True)
        self.set_keys(keys)
        self.check_lock_key_change_event(keys)
        self.check_led_state_on(keys)

        keys = dict()
        self.set_keys(keys)
        self.check_lock_key_change_event(keys)
        self.check_led_state_off()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        self.testCaseChecked("FUN_4220_0007", _AUTHOR)
    # end def test_scroll_lock_led_event

    @features("Feature4220")
    @level("Functionality")
    @services('RequiredKeys', (KEY_ID.KEYBOARD_SCROLL_LOCK,))
    def test_scroll_lock_led_indicator(self):
        """
        Validate Scroll lock LED indicator stays active for 5 minutes after the last user activity
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Start LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        keys = dict(ScrollLock=True)
        self.set_keys(keys)
        self.check_lock_key_change_event(keys)
        self.check_led_state_on(keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power off receiver")
        # --------------------------------------------------------------------------------------------------------------
        port_index = ChannelUtils.get_port_index(test_case=self)
        self.channel_disable(usb_port_index=port_index)

        self.check_led_state_on(keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wait for 5 minutes")
        # --------------------------------------------------------------------------------------------------------------
        sleep(300)

        self.check_led_state_off()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Power on receiver")
        # --------------------------------------------------------------------------------------------------------------
        self.channel_enable(usb_port_index=port_index, wait_device_notification=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        self.testCaseChecked("FUN_4220_0008", _AUTHOR)
    # end def test_scroll_lock_led_indicator

    @features("Feature4220")
    @level("Functionality")
    @services('RequiredKeys', (KEY_ID.KEYBOARD_COMPOSE,))
    def test_compose_led_event(self):
        """
        Validate Compose LED indicator matches the LED indicator state sent by the host
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Start LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        keys = dict(Compose=True)
        self.set_keys(keys)
        self.check_lock_key_change_event(keys)
        self.check_led_state_on(keys)

        keys = dict()
        self.set_keys(keys)
        self.check_lock_key_change_event(keys)
        self.check_led_state_off(compose_key=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        self.testCaseChecked("FUN_4220_0009", _AUTHOR)
    # end def test_compose_led_event

    @features("Feature4220")
    @level("Functionality")
    @services('RequiredKeys', (KEY_ID.KEYBOARD_COMPOSE,))
    def test_compose_key_led_indicator(self):
        """
        Validate Compose key LED indicator stays active for 5 minutes after the last user activity
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Start LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        keys = dict(Compose=True)
        self.set_keys(keys)
        self.check_lock_key_change_event(keys)
        self.check_led_state_on(keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power off receiver")
        # --------------------------------------------------------------------------------------------------------------
        port_index = ChannelUtils.get_port_index(test_case=self)
        self.channel_disable(usb_port_index=port_index)

        self.check_led_state_on(keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wait for 5 minutes")
        # --------------------------------------------------------------------------------------------------------------
        sleep(300)

        self.check_led_state_off(compose_key=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Power on receiver")
        # --------------------------------------------------------------------------------------------------------------
        self.channel_enable(usb_port_index=port_index, wait_device_notification=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        self.testCaseChecked("FUN_4220_0010", _AUTHOR)
    # end def test_compose_key_led_indicator

    @features("Feature4220")
    @level("Functionality")
    @services('RequiredKeys', (KEY_ID.KEYBOARD_KANA,))
    def test_kana_led_event(self):
        """
        Validate Kana LED indicator matches the LED indicator state sent by the host
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Start LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        keys = dict(Kana=True)
        self.set_keys(keys)
        self.check_lock_key_change_event(keys)
        self.check_led_state_on(keys)

        keys = dict()
        self.set_keys(keys)
        self.check_lock_key_change_event(keys)
        self.check_led_state_off(kana_key=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        self.testCaseChecked("FUN_4220_0011", _AUTHOR)
    # end def test_kana_led_event

    @features("Feature4220")
    @level("Functionality")
    @services('RequiredKeys', (KEY_ID.KEYBOARD_KANA,))
    def test_kana_key_led_indicator(self):
        """
        Validate Kana key LED indicator stays active for 5 minutes after the last user activity
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Start LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        keys = dict(Kana=True)
        self.set_keys(keys)
        self.check_lock_key_change_event(keys)
        self.check_led_state_on(keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power off receiver")
        # --------------------------------------------------------------------------------------------------------------
        port_index = ChannelUtils.get_port_index(test_case=self)
        self.channel_disable(usb_port_index=port_index)

        self.check_led_state_on(keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wait for 5 minutes")
        # --------------------------------------------------------------------------------------------------------------
        sleep(300)

        self.check_led_state_off(kana_key=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Power on receiver")
        # --------------------------------------------------------------------------------------------------------------
        self.channel_enable(usb_port_index=port_index, wait_device_notification=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        self.testCaseChecked("FUN_4220_0012", _AUTHOR)
    # end def test_scroll_lock_led_indicator

    @features("Feature4220")
    @level("Functionality")
    def test_pressing_lock_keys(self):
        """
        Validate pressing the lock keys don't switch on the LED indicators
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Start LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        keyboard = self.button_stimuli_emulator.keyboard_layout
        if KEY_ID.KEYBOARD_LOCKING_NUM_LOCK in keyboard.KEYS:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Num lock key stroke through emulator")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(KEY_ID.KEYBOARD_LOCKING_NUM_LOCK)

            self.check_led_state_off()
        # end if

        if KEY_ID.KEYBOARD_CAPS_LOCK in keyboard.KEYS:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Caps lock key stroke through emulator")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(KEY_ID.KEYBOARD_CAPS_LOCK)

            self.check_led_state_off()
        # end if

        if KEY_ID.KEYBOARD_SCROLL_LOCK in keyboard.KEYS:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Scroll lock key stroke through emulator")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(KEY_ID.KEYBOARD_SCROLL_LOCK)

            self.check_led_state_off()
        # end if

        if KEY_ID.KEYBOARD_COMPOSE in keyboard.KEYS:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Compose key stroke through emulator")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(KEY_ID.KEYBOARD_COMPOSE)

            self.check_led_state_off(compose_key=True)
        # end if

        if KEY_ID.KEYBOARD_KANA in keyboard.KEYS:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Kana key stroke through emulator")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(KEY_ID.KEYBOARD_KANA)

            self.check_led_state_off(kana_key=True)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        self.testCaseChecked("FUN_4220_0013", _AUTHOR)
    # end def test_pressing_lock_keys

    @features("Feature4220")
    @level("Functionality")
    @services('RequiredKeys', (KEY_ID.KEYBOARD_CAPS_LOCK,))
    def test_led_indicator_state_range_with_caps_lock_on(self):
        """
        Validate LED indicator state in all key combination with Caps Lock On.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Start LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        for keys in self.get_lock_key_state_combination(include_caps_lock=True):
            self.set_keys(keys)
            self.check_lock_key_change_event(keys)
            self.check_get_lock_key_state(keys)
            self.check_led_state_on(keys)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        self.testCaseChecked("FUN_4220_0014", _AUTHOR)
    # end def test_led_indicator_state_range_with_caps_lock_on

    @features("Feature4220")
    @level("Functionality")
    @services('RequiredKeys', (KEY_ID.KEYBOARD_CAPS_LOCK,))
    def test_led_indicator_state_range_with_caps_lock_off(self):
        """
        Validate LED indicator state in all key combination with Caps Lock Off.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Start LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        for keys in self.get_lock_key_state_combination(include_caps_lock=False):
            self.set_keys(keys)
            self.check_lock_key_change_event(keys)
            self.check_get_lock_key_state(keys)
            self.check_led_state_on(keys)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        self.testCaseChecked("FUN_4220_0015", _AUTHOR)
    # end def test_led_indicator_state_range_with_caps_lock_off

    @features("Feature4220")
    @level("Functionality")
    @services('PowerSupply')
    def test_battery_level(self):
        """
        Validate LED indicator state in its valid range [0x00, 0x01, 0x05, 0x0D, 0x1D] with Caps Lock bit = 0
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Test Loop over battery_level in range [FULL..CRITICAL]")
        # --------------------------------------------------------------------------------------------------------------
        battery = self.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY
        for index in range(len(battery.F_SupportedLevels)):
            if int(battery.F_SupportedLevels[index]) == -1:
                continue
            # end if
            state_of_charge = int(battery.F_SupportedLevels[index])
            battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, state_of_charge)
            self.power_supply_emulator.set_voltage(battery_value)
        # end for

        self.testCaseChecked("FUN_4220_0016", _AUTHOR)
    # end def test_battery_level
# end class LockKeyStateFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
