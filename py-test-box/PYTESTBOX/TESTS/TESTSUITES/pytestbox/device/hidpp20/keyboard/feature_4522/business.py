#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.keyboard.feature_4522.business
:brief: HID++ 2.0 DisableKeysByUsage business test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2021/09/13
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid.usbhidusagetable import STANDARD_KEYS
from pylibrary.emulator.keyid import KEY_ID
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.disablekeysbyusageutils import DisableKeysByUsageTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4522.disablekeysbyusage import DisableKeysByUsageBaseTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DisableKeysByUsageBusinessTestCase(DisableKeysByUsageBaseTestCase):
    """
    x4522 - Disable keys by usage business test case
    """
    @features('Feature4522')
    @level('Business', 'SmokeTests')
    @services('RequiredKeys', (KEY_ID.GAME_MODE_KEY, KEY_ID.KEYBOARD_MENU))
    def test_enable_menu_key_by_enable_keys(self):
        """
        Validate "Menu" key cannot be enabled by enableKeys in game mode.
        [2]enableKeys(keysToEnable)
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable game mode')
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.enable_game_mode(test_case=self)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send enableKeys "Menu"')
        # ---------------------------------------------------------------------------
        enable_keys_resp = DisableKeysByUsageTestUtils.enable_keys_by_key_id(test_case=self,
                                                                             keys=[KEY_ID.KEYBOARD_MENU])

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check enableKeys response fields")
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.EnableKeysResponseChecker.check_enable_keys_responses(
                                                        test_case=self,
                                                        messages=enable_keys_resp,
                                                        expected_cls=self.feature_4522.enable_keys_response_cls)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate key strokes on "Menu" key')
        # ---------------------------------------------------------------------------
        keys_reports = KeyMatrixTestUtils.stroke_keys_in_sequence(test_case=self,
                                                                  keys=[KEY_ID.KEYBOARD_MENU],
                                                                  collect_hid_report=True)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate host cannot receive key report')
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.check_keys_disabled(test_case=self,
                                                        keys_reports=keys_reports)

        self.testCaseChecked('BUS_4522_0001')
    # end def test_enable_menu_key_by_enable_keys

    @features('Feature4522')
    @level('Business')
    @services('RequiredKeys', (KEY_ID.GAME_MODE_KEY, KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION))
    def test_enable_win_key_by_enable_keys(self):
        """
        Validate "Win" key cannot be enabled by enableKeys in game mode.
        [2]enableKeys(keysToEnable)
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable game mode')
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.enable_game_mode(test_case=self)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send enableKeys "Win"')
        # ---------------------------------------------------------------------------
        enable_keys_resp = DisableKeysByUsageTestUtils.enable_keys_by_key_id(test_case=self,
                                                                             keys=[KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION])

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check enableKeys response fields")
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.EnableKeysResponseChecker.check_enable_keys_responses(
            test_case=self,
            messages=enable_keys_resp,
            expected_cls=self.feature_4522.enable_keys_response_cls)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate key strokes on "Win" key')
        # ---------------------------------------------------------------------------
        keys_reports = KeyMatrixTestUtils.stroke_keys_in_sequence(test_case=self,
                                                                  keys=[KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION],
                                                                  collect_hid_report=True)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate host cannot receive key report')
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.check_keys_disabled(test_case=self,
                                                        keys_reports=keys_reports)

        self.testCaseChecked('BUS_4522_0002')
    # end def test_enable_win_key_by_enable_keys

    @features('Feature4522')
    @level('Business')
    @services('RequiredKeys', (KEY_ID.GAME_MODE_KEY, KEY_ID.KEYBOARD_MENU))
    def test_enable_menu_key_by_enable_all_keys(self):
        """
        Validate "Menu" key cannot be enabled by enableAllKeys in game mode.
        [3]enableAllKeys()
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable game mode')
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.enable_game_mode(test_case=self)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send enableAllKeys')
        # ---------------------------------------------------------------------------
        enable_all_keys_resp = DisableKeysByUsageTestUtils.HIDppHelper.enable_all_keys(test_case=self)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check enableAllKeys response fields")
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.EnableAllKeysResponseChecker.check_fields(
                                                        test_case=self,
                                                        message=enable_all_keys_resp,
                                                        expected_cls=self.feature_4522.enable_all_keys_response_cls)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate key strokes on "Menu" key')
        # ---------------------------------------------------------------------------
        keys_reports = KeyMatrixTestUtils.stroke_keys_in_sequence(test_case=self,
                                                                  keys=[KEY_ID.KEYBOARD_MENU],
                                                                  collect_hid_report=True)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate host cannot receive key report')
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.check_keys_disabled(test_case=self,
                                                        keys_reports=keys_reports)

        self.testCaseChecked('BUS_4522_0003')
    # end def test_enable_menu_key_by_enable_all_keys

    @features('Feature4522')
    @level('Business')
    @services('RequiredKeys', (KEY_ID.GAME_MODE_KEY, KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION))
    def test_enable_win_key_by_enable_all_keys(self):
        """
        Validate "Win" key cannot be enabled by enableAllKeys in game mode.
        [3]enableAllKeys()
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable game mode')
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.enable_game_mode(test_case=self)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send enableAllKeys')
        # ---------------------------------------------------------------------------
        enable_all_keys_resp = DisableKeysByUsageTestUtils.HIDppHelper.enable_all_keys(test_case=self)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check enableAllKeys response fields")
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.EnableAllKeysResponseChecker.check_fields(
            test_case=self,
            message=enable_all_keys_resp,
            expected_cls=self.feature_4522.enable_all_keys_response_cls)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate key strokes on "Win" key')
        # ---------------------------------------------------------------------------
        keys_reports = KeyMatrixTestUtils.stroke_keys_in_sequence(test_case=self,
                                                                  keys=[KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION],
                                                                  collect_hid_report=True)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate host cannot receive key report')
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.check_keys_disabled(test_case=self,
                                                        keys_reports=keys_reports)

        self.testCaseChecked('BUS_4522_0004')
    # end def test_enable_win_key_by_enable_all_keys

    @features('Feature4522')
    @level('Business')
    @services('RequiredKeys', (KEY_ID.GAME_MODE_KEY, KEY_ID.KEYBOARD_MENU))
    def test_game_mode_and_menu_key(self):
        """
        Validate "Menu" key is disabled by default in game mode.
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable game mode')
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.enable_game_mode(test_case=self)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate key strokes on "Menu" key')
        # ---------------------------------------------------------------------------
        keys_reports = KeyMatrixTestUtils.stroke_keys_in_sequence(test_case=self,
                                                                  keys=[KEY_ID.KEYBOARD_MENU],
                                                                  collect_hid_report=True)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate host cannot receive key report')
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.check_keys_disabled(test_case=self,
                                                        keys_reports=keys_reports)

        self.testCaseChecked('BUS_4522_0005')
    # end def test_game_mode_and_menu_key

    @features('Feature4522')
    @level('Business')
    @services('RequiredKeys', (KEY_ID.GAME_MODE_KEY, KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION))
    def test_game_mode_and_win_key(self):
        """
        Validate "Win" key is disabled by default in game mode.
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable game mode')
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.enable_game_mode(test_case=self)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate key strokes on "Win" key')
        # ---------------------------------------------------------------------------
        keys_reports = KeyMatrixTestUtils.stroke_keys_in_sequence(test_case=self,
                                                                  keys=[KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION],
                                                                  collect_hid_report=True)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate host cannot receive key report')
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.check_keys_disabled(test_case=self,
                                                        keys_reports=keys_reports)

        self.testCaseChecked('BUS_4522_0006')
    # end def test_game_mode_and_win_key

    @features('Feature4522')
    @level('Business')
    @services('RequiredKeys', tuple(STANDARD_KEYS.keys()))
    def test_disable_keys(self):
        """
        Check disabled keys generate HID reports while the game lock is off.
        [1]disableKeys(keysToDisable)
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Randomly select 10 keys to disable")
        # ---------------------------------------------------------------------------
        disable_keys = DisableKeysByUsageTestUtils.get_key_list_from_standard_keys(test_case=self,
                                                                                   group_count=1,
                                                                                   group_size=10)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Send disableKeys 10 keys by randomly selection from standard keys")
        # ---------------------------------------------------------------------------
        disable_keys_resp = DisableKeysByUsageTestUtils.disable_keys_by_key_id(test_case=self,
                                                                               keys=disable_keys)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check disableKeys response fields")
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.DisableKeysResponseChecker.check_disable_keys_responses(
            test_case=self,
            messages=disable_keys_resp,
            expected_cls=self.feature_4522.disable_keys_response_cls)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Emulate key strokes on these disabled keys")
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.stroke_keys_in_sequence(test_case=self,
                                                   keys=disable_keys)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate host can receive key report")
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.check_keys_enabled(test_case=self,
                                                       keys=disable_keys)

        self.testCaseChecked("BUS_4522_0007")
    # end def test_disable_keys
# end class DisableKeysByUsageBusinessTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
