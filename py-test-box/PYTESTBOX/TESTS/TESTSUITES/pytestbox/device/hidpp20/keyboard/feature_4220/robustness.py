#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.keyboard.feature_4220.robustness
:brief: HID++ 2.0 ``LockKeyState`` robustness test suite
:author: Anil Gadad <agadad@logitech.com>
:date: 2022/04/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.keyboard.lockkeystate import LockKeyState
from pylibrary.emulator.ledid import LOCK_KEYS_LEDS
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.connectionschemeutils import BleProConnectionSchemeTestUtils
from pytestbox.device.base.lockkeystateutils import LockKeyStateTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4220.lockkeystate import LockKeyStateTestCase


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Anil Gadad"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LockKeyStateRobustnessTestCase(LockKeyStateTestCase):
    """
    Validate ``LockKeyState`` robustness test cases
    """

    @features("Feature4220")
    @level("Robustness")
    def test_get_lock_key_state_software_id(self):
        """
        Validate ``GetLockKeyState`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        self.set_keys(dict())
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(LockKeyState.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetLockKeyState request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_4220.get_lock_key_state_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_4220_index)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=self.feature_4220.get_lock_key_state_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetLockKeyStateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            LockKeyStateTestUtils.GetLockKeyStateResponseChecker.check_fields(
                self, response, self.feature_4220.get_lock_key_state_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4220_0001", _AUTHOR)
    # end def test_get_lock_key_state_software_id

    @features("Feature4220")
    @level("Robustness")
    def test_get_lock_key_state_padding(self):
        """
        Validate ``GetLockKeyState`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        self.set_keys(dict())
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_4220.get_lock_key_state_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetLockKeyState request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_4220_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=self.feature_4220.get_lock_key_state_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetLockKeyStateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            LockKeyStateTestUtils.GetLockKeyStateResponseChecker.check_fields(
                self, response, self.feature_4220.get_lock_key_state_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4220_0002", _AUTHOR)
    # end def test_get_lock_key_state_padding

    @features("Feature4220")
    @level("Robustness")
    @bugtracker('LockKeyState_ReservedBitsHandling')
    def test_lock_key_state_api(self):
        """
        Validate LED indicator state bit6, 7 & 8 are filtered out when building the GetLockKeyState API response
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Start LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        for keys in self.get_lock_key_state_combination_with_reserved_bits():
            self.set_keys(keys)
            self.check_get_lock_key_state(keys)
            compose_key = True if keys.get("Compose") else False
            kana_key = True if keys.get("Kana") else False
            self.check_led_state_off(compose_key=compose_key, kana_key=kana_key)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)
        self.testCaseChecked("ROB_4220_0003", _AUTHOR)
    # end def test_get_lock_key_state_api

    @features("Feature4220")
    @level("Robustness")
    @bugtracker('LockKeyState_ReservedBitsHandling')
    def test_get_lock_key_state_event(self):
        """
        Validate LED indicator state bit 6, 7 & 8 are filtered out when building the GetLockKeyState event response
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Start LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        for keys in self.get_lock_key_state_combination_with_reserved_bits():
            self.set_keys(keys)
            self.check_lock_key_change_event(keys)
            compose_key = True if keys.get("Compose") else False
            kana_key = True if keys.get("Kana") else False
            self.check_led_state_off(compose_key=compose_key, kana_key=kana_key)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop LEDs monitoring")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=LOCK_KEYS_LEDS)

        self.testCaseChecked("ROB_4220_0004", _AUTHOR)
    # end def test_get_lock_key_state_event
# end class LockKeyStateRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
