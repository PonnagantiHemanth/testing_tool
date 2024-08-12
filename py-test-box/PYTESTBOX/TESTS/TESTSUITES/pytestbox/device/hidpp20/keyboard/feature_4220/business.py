#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.keyboard.feature_4220.business
:brief: HID++ 2.0 ``LockKeyState`` business test suite
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
from pylibrary.emulator.ledid import LED_ID
from pylibrary.emulator.ledid import LOCK_KEYS_LEDS
from pyraspi.services.kosmos.leds.leddataparser import SchemeType
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.backlightutils import BacklightTestUtils
from pytestbox.device.base.connectionschemeutils import BleProConnectionSchemeTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4220.lockkeystate import LockKeyStateTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Anil Gadad"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LockKeyStateBusinessTestCase(LockKeyStateTestCase):
    """
    Validate ``LockKeyState`` business test cases
    """

    @features("Feature4220")
    @level('Business', 'SmokeTests')
    def test_device_declares_supported_leds(self):
        """
        Validate ``LockStateChange`` has the default value equals to 0
        """
        keys = dict()
        self.set_keys(keys)
        self.check_get_lock_key_state(keys)
        self.check_led_state_off()

        self.testCaseChecked("BUS_4220_0001", _AUTHOR)
    # end def test_device_declares_supported_leds

    @features("Feature4220")
    @level("Business")
    @services('MultiHost')
    def test_device_reconnection(self):
        """
        Validate ``LockStateChange`` could be initialized to 0
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power-off receiver for 2 seconds and power-on")
        # --------------------------------------------------------------------------------------------------------------
        port_index = ChannelUtils.get_port_index(test_case=self)
        self.channel_disable(usb_port_index=port_index)
        sleep(2)
        self.channel_enable(usb_port_index=port_index, wait_device_notification=False)

        self.button_stimuli_emulator.user_action()
        sleep(.3)

        # Add delay to wait for previous commands to process and prevent them from generating events after clearing
        # queue
        sleep(5)

        keys = dict()
        self.check_lock_key_change_event(keys)
        self.check_get_lock_key_state(keys)
        self.check_led_state_off()

        self.testCaseChecked("BUS_4220_0002", _AUTHOR)
    # end def test_device_reconnection

    @features("Feature4220")
    @level("Business")
    @services('RequiredKeys', (KEY_ID.KEYBOARD_CAPS_LOCK,))
    def test_caps_lock_active_with_led(self):
        """
        Validate CapsLock LED is active and matches the expected effect for keyboard with backlight with a dedicated
        CapsLock LED
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Start LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        keys = dict(CapsLock=True)
        self.set_keys(keys)
        self.check_lock_key_change_event(keys)
        self.check_get_lock_key_state(keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check CapsLock LED is active (steady) and other LED's are off")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1, state=SchemeType.STEADY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        self.testCaseChecked("BUS_4220_0003", _AUTHOR)
    # end def test_caps_lock_active_with_led

    @features("Feature4220")
    @level("Business")
    @services('RequiredKeys', (KEY_ID.KEYBOARD_CAPS_LOCK,))
    def test_caps_lock_active_without_led(self):
        """
        Validate CapsLock LED is active and matches the expected effect for keyboard with backlight
        """
        BacklightTestUtils.HIDppHelper.disable_backlight_wow_effect(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Start LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        keys = dict(CapsLock=True)
        self.set_keys(keys)
        self.check_lock_key_change_event(keys)
        self.check_get_lock_key_state(keys)
        sleep(LockKeyStateTestCase.CAPS_LOCK_BLINK_DETECTION_TIME)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check CapsLock LED is active (steady) and other LED's are off")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.CAPS_LOCK, state=SchemeType.CAPS_LOCK_BLINK)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.NUM_LOCK, state=SchemeType.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        self.testCaseChecked("BUS_4220_0004", _AUTHOR)
    # end def test_caps_lock_active_without_led

    @features("Feature4220")
    @level("Business")
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LOCKING_NUM_LOCK,))
    def test_num_lock_led_active(self):
        """
        Validate NumLock LED is active and matches the expected effect
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Start LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        keys = dict(NumLock=True)
        self.set_keys(keys)
        self.check_lock_key_change_event(keys)
        self.check_get_lock_key_state(keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check NumLock LED is active (steady) and other LED's are off")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1, state=SchemeType.STEADY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        self.testCaseChecked("BUS_4220_0005", _AUTHOR)
    # end def test_num_lock_led_active

    @features("Feature4220")
    @level("Business")
    @services('RequiredKeys', (KEY_ID.KEYBOARD_SCROLL_LOCK,))
    def test_scroll_lock_led_active(self):
        """
        Validate Scroll Lock LED is active and matches the expected effect
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Start LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        keys = dict(ScrollLock=True)
        self.set_keys(keys)
        self.check_lock_key_change_event(keys)
        self.check_get_lock_key_state(keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ScrLock key LED is active (steady) and other LED's are off")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.SCROLL_LOCK, state=SchemeType.STEADY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        self.testCaseChecked("BUS_4220_0006", _AUTHOR)
    # end def test_scroll_lock_led_active

    @features("Feature4220")
    @level("Business")
    @services('RequiredKeys', (KEY_ID.KEYBOARD_COMPOSE,))
    def test_compose_key_led_active(self):
        """
        Validate Compose key LED is active and matches the expected effect
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Start LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        keys = dict(Compose=True)
        self.set_keys(keys)
        self.check_lock_key_change_event(keys)
        self.check_get_lock_key_state(keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Compose key LED is active (steady) and other LED's are off")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.COMPOSE, state=SchemeType.STEADY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        self.testCaseChecked("BUS_4220_0007", _AUTHOR)
    # end def test_compose_key_led_active

    @features("Feature4220")
    @level("Business")
    @services('RequiredKeys', (KEY_ID.KEYBOARD_KANA,))
    def test_kana_key_led_active(self):
        """
        Validate Kana key LED is active and matches the expected effect
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Start LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        keys = dict(Kana=True)
        self.set_keys(keys)
        self.check_lock_key_change_event(keys)
        self.check_get_lock_key_state(keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Kana key LED is active (steady) and other LED's are off")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.KANA, state=SchemeType.STEADY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        self.testCaseChecked("BUS_4220_0008", _AUTHOR)
    # end def test_kana_key_led_active
# end class LockKeyStateBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
