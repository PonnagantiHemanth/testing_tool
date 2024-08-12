#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.keyboard.feature_4220.lockkeystate
:brief: Validate HID++ 2.0 ``LockKeyState`` feature
:author: Anil Gadad <agadad@logitech.com>
:date: 2022/04/04
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.keyboard.lockkeystate import LockKeyState
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.emulator.ledid import LED_ID
from pylibrary.emulator.ledid import LOCK_KEYS_LEDS
from pylibrary.tools.hexlist import HexList
from pyraspi.services.kosmos.leds.leddataparser import SchemeType
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.connectionschemeutils import BleProConnectionSchemeTestUtils
from pytestbox.device.base.lockkeystateutils import LockKeyStateTestUtils
from pytransport.usb.usbconstants import HidClassSpecificRequest
from pytransport.usb.usbmessage import UsbMessage


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LockKeyStateTestCase(DeviceBaseTestCase):
    """
    Validate ``LockKeyState`` TestCases in Application mode
    """
    # time required to capture 2 cycles of the caps lock blinking scheme
    # 2 * (1.5s off + 1.5s on) + 1s margin
    CAPS_LOCK_BLINK_DETECTION_TIME = 7

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x4220 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_4220_index, self.feature_4220, _, _ = LockKeyStateTestUtils.HIDppHelper.get_parameters(self)
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, 'Stop LEDs monitoring')
            # ----------------------------------------------------------------------------------------------------------
            BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(
                self, led_identifiers=LOCK_KEYS_LEDS, build_timeline=False)
        # end with
        super().tearDown()
    # end def tearDown

    def check_get_lock_key_state(self, keys):
        """
        Check GetLockKeyState request & response

        :param keys: key types with dictionary keys in Reserved, CapsLock, NumLock, ScrollLock, Compose & Kana
        :type keys: ``dict``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetLockKeyState request")
        # --------------------------------------------------------------------------------------------------------------
        response = LockKeyStateTestUtils.HIDppHelper.get_lock_key_state(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetLockKeyState response fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = LockKeyStateTestUtils.GetLockKeyStateResponseChecker
        check_map = checker.get_default_check_map(self)
        self.update_check_map(check_map, keys)
        LockKeyStateTestUtils.GetLockKeyStateResponseChecker.check_fields(
            self, response, self.feature_4220.get_lock_key_state_response_cls, check_map=check_map)
    # end def check_get_lock_key_state

    @staticmethod
    def update_check_map(check_map, keys):
        """
        Update check map dictionary

        :param check_map: source check_map
        :type check_map: ``dict``
        :param keys: keys lookup dictionary with Reserved, CapsLock, NumLock, ScrollLock, Compose and Kana
        :type keys: ``dict`` or ``None``
        """
        if keys is None:
            return
        # end if
        inner_item = check_map["lock_key_state_mask_bit_map"][1]

        kana = keys.get("Kana")
        if kana:
            inner_item.update({
                "kana": (LockKeyStateTestUtils.LockKeyStateMaskBitMapChecker.check_kana, 1)
            })
        # end if
        compose = keys.get("Compose")
        if compose:
            inner_item.update({
                "compose": (LockKeyStateTestUtils.LockKeyStateMaskBitMapChecker.check_compose, 1)
            })
        # end if
        scroll_lock = keys.get("ScrollLock")
        if scroll_lock:
            inner_item.update({
                "scroll_lock": (LockKeyStateTestUtils.LockKeyStateMaskBitMapChecker.check_scroll_lock, 1)
            })
        # end if
        caps_lock = keys.get("CapsLock")
        if caps_lock:
            inner_item.update({
                "caps_lock": (LockKeyStateTestUtils.LockKeyStateMaskBitMapChecker.check_caps_lock, 1)
            })
        # end if
        num_lock = keys.get("NumLock")
        if num_lock:
            inner_item.update({
                "num_lock": (LockKeyStateTestUtils.LockKeyStateMaskBitMapChecker.check_num_lock, 1)
            })
        # end if
    # end def update_check_map

    def check_lock_key_change_event(self, keys):
        """
        Check LockKeyChange event

        :param keys: key types with dictionary keys in Reserved, CapsLock, NumLock, ScrollLock, Compose & Kana
        :type keys: ``dict``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get LockKeyChange event")
        # --------------------------------------------------------------------------------------------------------------
        report = LockKeyStateTestUtils.HIDppHelper.lock_key_change_event(self,
                                                                         check_first_message=False,
                                                                         allow_no_message=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check LockKeyChange event fields")
        # --------------------------------------------------------------------------------------------------------------
        if report is not None:
            checker = LockKeyStateTestUtils.LockKeyChangeEventChecker
            check_map = checker.get_default_check_map(self)
            self.update_check_map(check_map, keys)
            LockKeyStateTestUtils.LockKeyChangeEventChecker.check_fields(
                self, report, self.feature_4220.lock_key_change_event_cls, check_map=check_map)
        # end if
    # end def check_lock_key_change_event

    def set_keys(self, keys):
        """
        Set the given keys

        :param keys: key types with dictionary keys in Reserved, CapsLock, NumLock, ScrollLock, Compose & Kana
        :type keys: ``dict``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Clear any previous events in the queue")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(
            test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
            class_type=self.feature_4220.lock_key_change_event_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send setReport.LedIndicatorState {self.get_label(keys)}")
        # --------------------------------------------------------------------------------------------------------------
        self.current_channel.receiver_channel.hid_class_specific_request(
            b_request=HidClassSpecificRequest.SET_REPORT,
            # index is ignored in this context
            interface_id=0,
            data=UsbMessage(data=HexList(self.get_lock_state_value(keys))),
            w_value=0x0200)
    # end def set_keys

    @staticmethod
    def get_label(keys):
        """
        Get label

        :param keys: key types with dictionary keys in Reserved, CapsLock, NumLock, ScrollLock, Compose & Kana
        :type keys: ``dict``

        :return: Label
        :rtype: ``str``
        """
        label = []
        reserved_3 = keys.get("Reserved3")
        reserved_2 = keys.get("Reserved2")
        reserved_1 = keys.get("Reserved1")
        if reserved_3 or reserved_2 or reserved_1:
            label.append("[Reserved]")
        # end if
        kana = keys.get("Kana")
        if kana:
            label.append("[Kana]")
        # end if
        compose = keys.get("Compose")
        if compose:
            label.append("[Compose]")
        # end if
        scroll_lock = keys.get("ScrollLock")
        if scroll_lock:
            label.append("[Scroll Lock]")
        # end if
        caps_lock = keys.get("CapsLock")
        if caps_lock:
            label.append("[Caps Lock]")
        # end if
        num_lock = keys.get("NumLock")
        if num_lock:
            label.append("[Num Lock]")
        # end if
        return ', '.join(label)
    # end def get_label

    @staticmethod
    def get_lock_state_value(keys):
        """
        Get value from LockKeyStateMaskBitMap

        :param keys: key types with dictionary keys in Reserved, CapsLock, NumLock, ScrollLock, Compose & Kana
        :type keys: ``dict``

        :return: BitMap value
        :rtype: ``LockKeyState.LockKeyStateMaskBitMap``
        """
        reserved_value = 0x0
        reserved_3 = keys.get("Reserved3")
        reserved_2 = keys.get("Reserved2")
        reserved_1 = keys.get("Reserved1")
        if reserved_3:
            reserved_value += 0x4
        # end if
        if reserved_2:
            reserved_value += 0x2
        # end if
        if reserved_1:
            reserved_value += 0x1
        # end if
        kana = 1 if keys.get("Kana") else 0
        compose = 1 if keys.get("Compose") else 0
        scroll_lock = 1 if keys.get("ScrollLock") else 0
        caps_lock = 1 if keys.get("CapsLock") else 0
        num_lock = 1 if keys.get("NumLock") else 0

        return LockKeyState.LockKeyStateMaskBitMap(reserved=reserved_value,
                                                   compose=compose,
                                                   kana=kana,
                                                   caps_lock=caps_lock,
                                                   num_lock=num_lock,
                                                   scroll_lock=scroll_lock)
    # end def get_lock_state_value

    def check_led_state_off(self, compose_key=False, kana_key=False):
        """
        Check LED state off

        :param compose_key: Compose Key - OPTIONAL
        :type compose_key: ``bool``
        :param kana_key: Kana Key - OPTIONAL
        :type kana_key: ``bool``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check all LED's are in off state")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.CAPS_LOCK, state=SchemeType.OFF)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.NUM_LOCK, state=SchemeType.OFF)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.SCROLL_LOCK, state=SchemeType.OFF)
        if compose_key:
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                self, led_id=LED_ID.COMPOSE, state=SchemeType.OFF)
        # end if
        if kana_key:
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                self, led_id=LED_ID.KANA, state=SchemeType.OFF)
        # end if
    # end def check_led_state_off

    def check_led_state_on(self, keys):
        """
        Check LED state on for given key(s)

        :param keys: key types with dictionary keys in Reserved, CapsLock, NumLock, ScrollLock, Compose & Kana
        :type keys: ``dict``
        """
        label = self.get_label(keys)
        verb = "are" if label.find(",") > 0 else "is"
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check {label} LED {verb} in active(steady) and other LEDs are in off state")
        # --------------------------------------------------------------------------------------------------------------
        state = SchemeType.STEADY if keys.get("CapsLock") else SchemeType.OFF
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.CAPS_LOCK, state=state)

        state = SchemeType.STEADY if keys.get("NumLock") else SchemeType.OFF
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.NUM_LOCK, state=state)

        state = SchemeType.STEADY if keys.get("ScrollLock") else SchemeType.OFF
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.SCROLL_LOCK, state=state)

        if keys.get("Compose"):
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                self, led_id=LED_ID.COMPOSE, state=SchemeType.STEADY)
        # end if
        if keys.get("Kana"):
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                self, led_id=LED_ID.KANA, state=SchemeType.STEADY)
        # end if
    # end def check_led_state_on

    def check_led_state_blink(self, keys):
        """
        Check LED state blink for given key(s)

        :param keys: key types with dictionary keys in Reserved, CapsLock, NumLock, ScrollLock, Compose & Kana
        :type keys: ``dict``
        """
        label = self.get_label(keys)
        verb = "are" if label.find(",") > 0 else "is"
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check {label} LED {verb} in active(blink) and other LEDs are in off state")
        # --------------------------------------------------------------------------------------------------------------
        state = SchemeType.CAPS_LOCK_BLINK if keys.get("CapsLock") else SchemeType.OFF
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.CAPS_LOCK, state=state)

        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.NUM_LOCK, state=SchemeType.OFF)

        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.SCROLL_LOCK, state=SchemeType.OFF)

        if keys.get("Compose"):
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                self, led_id=LED_ID.COMPOSE, state=SchemeType.OFF)
        # end if
        if keys.get("Kana"):
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                self, led_id=LED_ID.KANA, state=SchemeType.OFF)
        # end if
    # end def check_led_state_blink

    def get_lock_key_state_combination(self, include_caps_lock):
        """
        | Compute the incremental combination of supported lock keys states starting with caps lock if included.
        |
        | Example output:
        | [{'CapsLock': True},
        |  {'CapsLock': True, 'NumLock': True},
        |  {'CapsLock': True, 'NumLock': True, 'ScrollLock': True},
        |  {'CapsLock': True, 'NumLock': True, 'ScrollLock': True, 'Compose': True},
        |  {'CapsLock': True, 'NumLock': True, 'ScrollLock': True, 'Compose': True, 'Kana': True}]

        :param include_caps_lock: Flag indicating to include the CapsLock
        :type include_caps_lock: ``bool``

        :return: key types with dictionary keys in Reserved, CapsLock, NumLock, ScrollLock, Compose & Kana
        :rtype: ``list[dict]``
        """
        dictionary = dict()
        values = []
        if include_caps_lock:
            dictionary["CapsLock"] = True
            values.append(dictionary.copy())
        # end if
        keyboard = self.button_stimuli_emulator.keyboard_layout
        if KEY_ID.KEYBOARD_LOCKING_NUM_LOCK in keyboard.KEYS or KEY_ID.KEYBOARD_LOCKING_NUM_LOCK in keyboard.FN_KEYS:
            dictionary["NumLock"] = True
            # CapsLock/NumLock
            values.append(dictionary.copy())
        # end if
        if KEY_ID.KEYBOARD_SCROLL_LOCK in keyboard.KEYS or KEY_ID.KEYBOARD_SCROLL_LOCK in keyboard.FN_KEYS:
            dictionary["ScrollLock"] = True
            # CapsLock/NumLock/ScrollLock
            values.append(dictionary.copy())
        # end if
        if KEY_ID.KEYBOARD_COMPOSE in keyboard.KEYS or KEY_ID.KEYBOARD_COMPOSE in keyboard.FN_KEYS:
            dictionary["Compose"] = True
            # CapsLock/NumLock/ScrollLock/Compose
            values.append(dictionary.copy())
        # end if
        if KEY_ID.KEYBOARD_KANA in keyboard.KEYS or KEY_ID.KEYBOARD_KANA in keyboard.FN_KEYS:
            dictionary["Kana"] = True
            # CapsLock/NumLock/ScrollLock/Compose/Kana
            values.append(dictionary.copy())
        # end if
        return values
    # end def get_lock_key_state_combination

    def get_lock_key_state_combination_with_reserved_bits(self):
        """
        | Compute the incremental combination of reserved bits states with other supported lock keys enabled
        |
        | Example output:
        | [{'CapsLock': True, 'Reserved1':True},
        |  {'CapsLock': True, 'Reserved2':True},
        |  {'CapsLock': True, 'Reserved3':True},
        |  {'CapsLock': True, 'Reserved1':True, 'Reserved2':True},
        |  {'CapsLock': True, 'Reserved1':True, 'Reserved3':True},
        |  {'CapsLock': True, 'Reserved2':True, 'Reserved3':True},
        |  {'CapsLock': True, 'Reserved1':True, 'Reserved2':True, 'Reserved3':True}]
        |  NumLock, ScrollLock, Compose and Kana can be True in the above list based on their presence.

        :return: key types with dictionary keys in Reserved, CapsLock, NumLock, ScrollLock, Compose & Kana
        :rtype: ``list[dict]``
        """
        dictionary = dict(CapsLock=True)
        values = []
        keyboard = self.button_stimuli_emulator.keyboard_layout
        if KEY_ID.KEYBOARD_LOCKING_NUM_LOCK in keyboard.KEYS or KEY_ID.KEYBOARD_LOCKING_NUM_LOCK in keyboard.FN_KEYS:
            dictionary["NumLock"] = True
        # end if
        if KEY_ID.KEYBOARD_SCROLL_LOCK in keyboard.KEYS or KEY_ID.KEYBOARD_SCROLL_LOCK in keyboard.FN_KEYS:
            dictionary["ScrollLock"] = True
        # end if
        if KEY_ID.KEYBOARD_COMPOSE in keyboard.KEYS or KEY_ID.KEYBOARD_COMPOSE in keyboard.FN_KEYS:
            dictionary["Compose"] = True
        # end if
        if KEY_ID.KEYBOARD_KANA in keyboard.KEYS or KEY_ID.KEYBOARD_KANA in keyboard.FN_KEYS:
            dictionary["Kana"] = True
        # end if

        # Only reserved 1 bit
        reserved_1 = dictionary.copy()
        reserved_1["Reserved1"] = True
        values.append(reserved_1)

        # Only reserved 2 bit
        reserved_2 = dictionary.copy()
        reserved_2["Reserved2"] = True
        values.append(reserved_2)

        # Only reserved 3 bit
        reserved_3 = dictionary.copy()
        reserved_3["Reserved3"] = True
        values.append(reserved_3)

        # Reserved bits 1 & 2
        reserved_1_2 = dictionary.copy()
        reserved_1_2["Reserved1"] = True
        reserved_1_2["Reserved2"] = True
        values.append(reserved_1_2)

        # Reserved bits 1 & 3
        reserved_1_3 = dictionary.copy()
        reserved_1_3["Reserved1"] = True
        reserved_1_3["Reserved3"] = True
        values.append(reserved_1_3)

        # Reserved bits 2 & 3
        reserved_2_3 = dictionary.copy()
        reserved_2_3["Reserved2"] = True
        reserved_2_3["Reserved3"] = True
        values.append(reserved_2_3)

        # Reserved bits 1, 2 & 3.
        dictionary["Reserved1"] = True
        dictionary["Reserved2"] = True
        dictionary["Reserved3"] = True
        values.append(dictionary)

        return values
    # end def get_lock_key_state_combination_with_reserved_bits
# end class LockKeyStateTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
