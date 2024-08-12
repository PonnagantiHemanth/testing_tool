#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.keyboard.feature_4522.robustness
:brief: HID++ 2.0 DisableKeysByUsage robustness test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2021/09/14
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.keyboard.disablekeysbyusage import GetCapabilities
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.disablekeysbyusageutils import DisableKeysByUsageTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4522.disablekeysbyusage import DisableKeysByUsageBaseTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DisableKeysByUsageRobustnessTestCase(DisableKeysByUsageBaseTestCase):
    """
    x4522 - Disable keys by usage robustness test case
    """
    @features('Feature4522')
    @level('Robustness')
    @services('RequiredKeys', (KEY_ID.GAME_MODE_KEY, KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_B))
    def test_check_duplicate_keys_with_disable_keys(self):
        """
        Validate disableKeys to fills up Inputs.keysToDisable by a single key "A" should work properly(Feature 0x4522)
        [1]disableKeys(keysToDisable)
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable game mode')
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.enable_game_mode(self)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send disableKeys "A" and fill up all 16 bytes by "A"')
        # ---------------------------------------------------------------------------
        disable_key_list = [KEY_ID.KEYBOARD_A] * 16
        disable_keys_resp = DisableKeysByUsageTestUtils.disable_keys_by_key_id(test_case=self,
                                                                               keys=disable_key_list)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check disableKeys response fields")
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.DisableKeysResponseChecker.check_disable_keys_responses(
            test_case=self,
            messages=disable_keys_resp,
            expected_cls=self.feature_4522.disable_keys_response_cls)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate key stokes on "A" and "B" keys')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.stroke_keys_in_sequence(test_case=self,
                                                   keys=[KEY_ID.KEYBOARD_A,
                                                         KEY_ID.KEYBOARD_B])

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate only "A" is disabled')
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.check_keys_enabled(test_case=self,
                                                       keys=[KEY_ID.KEYBOARD_B])

        self.testCaseChecked("ROB_4522_0001")
    # end def test_check_duplicate_keys_with_disable_keys

    @features('Feature4522')
    @level('Robustness')
    @services('RequiredKeys', (KEY_ID.GAME_MODE_KEY, KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_B))
    def test_check_duplicate_keys_with_enable_keys(self):
        """
        Validate keys could be disabled then enabled by functions disableKeys and enableKeys (Feature 0x4522)
        [1]disableKeys(keysToDisable)`
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable game mode')
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.enable_game_mode(self)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send disableKeys "A" and "B"')
        # ---------------------------------------------------------------------------
        disable_keys_resp = DisableKeysByUsageTestUtils.disable_keys_by_key_id(test_case=self,
                                                                               keys=[KEY_ID.KEYBOARD_A,
                                                                                     KEY_ID.KEYBOARD_B])

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check disableKeys response fields")
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.DisableKeysResponseChecker.check_disable_keys_responses(
            test_case=self,
            messages=disable_keys_resp,
            expected_cls=self.feature_4522.disable_keys_response_cls)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate key strokes on "A" and "B" keys')
        # ---------------------------------------------------------------------------
        keys_reports = KeyMatrixTestUtils.stroke_keys_in_sequence(test_case=self,
                                                                  keys=[KEY_ID.KEYBOARD_A,
                                                                        KEY_ID.KEYBOARD_B],
                                                                  collect_hid_report=True)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate "A" and "B" is disabled')
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.check_keys_disabled(test_case=self,
                                                        keys_reports=keys_reports)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send enableKeys "A" and fill up all 16 bytes by "A"')
        # ---------------------------------------------------------------------------
        enable_key_list = [KEY_ID.KEYBOARD_A] * 16
        enable_keys_resp = DisableKeysByUsageTestUtils.enable_keys_by_key_id(test_case=self,
                                                                             keys=enable_key_list)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check enableKeys response fields")
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.EnableKeysResponseChecker.check_enable_keys_responses(
            test_case=self,
            messages=enable_keys_resp,
            expected_cls=self.feature_4522.enable_keys_response_cls)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate key strokes on "A" key')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.stroke_keys_in_sequence(test_case=self,
                                                   keys=[KEY_ID.KEYBOARD_A])

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate "A" is enabled')
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.check_keys_enabled(test_case=self,
                                                       keys=[KEY_ID.KEYBOARD_A])

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate key strokes on "B" key')
        # ---------------------------------------------------------------------------
        keys_reports = KeyMatrixTestUtils.stroke_keys_in_sequence(test_case=self,
                                                                  keys=[KEY_ID.KEYBOARD_B],
                                                                  collect_hid_report=True)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate "B" is still disabled')
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.check_keys_disabled(test_case=self,
                                                        keys_reports=keys_reports)

        self.testCaseChecked("ROB_4522_0002")
    # end def test_check_duplicate_keys_with_enable_keys

    @features('Feature4522')
    @level('Robustness')
    def test_disable_inexistent_key(self):
        """
        Disable inexistent key, host shall not receive error message from DUT
        [1]disableKeys(keysToDisable)
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send disableKeys with keysToDisable = "0xFF"')
        # ---------------------------------------------------------------------------
        disable_keys_resp = DisableKeysByUsageTestUtils.disable_keys_by_key_id(test_case=self,
                                                                               keys=[0xFF])

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check disableKeys response fields")
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.DisableKeysResponseChecker.check_disable_keys_responses(
                                                        test_case=self,
                                                        messages=disable_keys_resp,
                                                        expected_cls=self.feature_4522.disable_keys_response_cls)

        self.testCaseChecked("ROB_4522_0003")
    # end def test_disable_inexistent_key

    @features('Feature4522')
    @level('Robustness')
    def test_ignore_padding(self):
        """
        Padding bytes shall be ignored by the firmware (Feature 0x4522)
        maxDisabledUsages [0]getCapabilities
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over getCapabilities padding range (several interesting values)')
        # ---------------------------------------------------------------------------
        for padding_byte in compute_sup_values(HexList(Numeral(GetCapabilities.DEFAULT.PADDING,
                                                               GetCapabilities.LEN.PADDING//8))):
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getCapabilities with several value for padding')
            # ---------------------------------------------------------------------------
            response = DisableKeysByUsageTestUtils.get_capabilities_with_specific_padding(test_case=self,
                                                                                          padding_byte=padding_byte)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate maxDisableUsages value')
            # ---------------------------------------------------------------------------
            DisableKeysByUsageTestUtils.GetCapabilitiesResponseChecker.check_fields(
                                                        self, response, self.feature_4522.get_capabilities_response_cls)
        # end for
        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ----------------------------------------------------------------------------

        self.testCaseChecked("ROB_4522_0004")
    # end def test_ignore_padding

    @features('Feature4522')
    @level('Robustness')
    @services('RequiredKeys', (KEY_ID.GAME_MODE_KEY, KEY_ID.KEYBOARD_MENU))
    def test_disable_menu_key(self):
        """
        Disable the game mode default disabled key "Menu". And validate the key is still disabled while game mode is on.
        [1]disableKeys(keysToDisable)
        [2]enableKeys(keysToEnable)
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable game mode')
        # ----------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.enable_game_mode(test_case=self)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send disableKeys with keysToDisable = "Menu"')
        # ----------------------------------------------------------------------------
        disable_keys_resp = DisableKeysByUsageTestUtils.disable_keys_by_key_id(test_case=self,
                                                                               keys=[KEY_ID.KEYBOARD_MENU])

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check disableKeys response fields")
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.DisableKeysResponseChecker.check_disable_keys_responses(
                                                        test_case=self,
                                                        messages=disable_keys_resp,
                                                        expected_cls=self.feature_4522.disable_keys_response_cls)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate key strokes on "Menu" key')
        # ----------------------------------------------------------------------------
        keys_reports = KeyMatrixTestUtils.stroke_keys_in_sequence(test_case=self,
                                                                  keys=[KEY_ID.KEYBOARD_MENU],
                                                                  collect_hid_report=True)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate host can not receive key report')
        # ----------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.check_keys_disabled(test_case=self,
                                                        keys_reports=keys_reports)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send enableKeys with keysToEnable = "Menu"')
        # ----------------------------------------------------------------------------
        enable_keys_resp = DisableKeysByUsageTestUtils.enable_keys_by_key_id(test_case=self,
                                                                             keys=[KEY_ID.KEYBOARD_MENU])

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check enableKeys response fields")
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.EnableKeysResponseChecker.check_enable_keys_responses(
                                                        test_case=self,
                                                        messages=enable_keys_resp,
                                                        expected_cls=self.feature_4522.enable_keys_response_cls)

        self.testCaseChecked("ROB_4522_0005")
    # end def test_disable_menu_key

    @features('Feature4522')
    @level('Robustness')
    @services('RequiredKeys', (KEY_ID.GAME_MODE_KEY, KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION))
    def test_disable_win_key(self):
        """
        Disable the game mode default disabled key "Win". And validate the key is still disabled while game mode is on.
        [1]disableKeys(keysToDisable)
        [2]enableKeys(keysToEnable)
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable game mode')
        # ----------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.enable_game_mode(test_case=self)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send disableKeys with keysToDisable = "Win"')
        # ----------------------------------------------------------------------------
        disable_keys_resp = DisableKeysByUsageTestUtils.disable_keys_by_key_id(
                                test_case=self, keys=[KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION])

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check disableKeys response fields")
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.DisableKeysResponseChecker.check_disable_keys_responses(
            test_case=self,
            messages=disable_keys_resp,
            expected_cls=self.feature_4522.disable_keys_response_cls)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate key strokes on "Win" keys')
        # ----------------------------------------------------------------------------
        keys_reports = KeyMatrixTestUtils.stroke_keys_in_sequence(test_case=self,
                                                                  keys=[KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION],
                                                                  collect_hid_report=True)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate host can not receive key report')
        # ----------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.check_keys_disabled(test_case=self,
                                                        keys_reports=keys_reports)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send enableKeys with keysToEnable = "Win"')
        # ----------------------------------------------------------------------------
        enable_keys_resp = DisableKeysByUsageTestUtils.enable_keys_by_key_id(test_case=self,
                                                                             keys=[KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION])

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check enableKeys response fields")
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.EnableKeysResponseChecker.check_enable_keys_responses(
            test_case=self,
            messages=enable_keys_resp,
            expected_cls=self.feature_4522.enable_keys_response_cls)

        self.testCaseChecked("ROB_4522_0006")
    # end def test_disable_win_key
# end class DisableKeysByUsageRobustnessTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
