#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.keyboard.feature_4522.functionality
:brief: HID++ 2.0 DisableKeysByUsage functionality test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2021/09/14
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid.usbhidusagetable import STANDARD_KEYS
from pyhid.hidpp.features.keyboard.disablekeysbyusage import DisableKeys
from pylibrary.emulator.keyid import KEY_ID
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.disablekeysbyusageutils import DisableKeysByUsageTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4522.disablekeysbyusage import DisableKeysByUsageBaseTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DisableKeysByUsageFunctionalityTestCase(DisableKeysByUsageBaseTestCase):
    """
    x4522 - Disable keys by usage functionality test case
    """
    @features('Feature4522')
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.GAME_MODE_KEY, ))
    def test_disable_all_standard_keys(self):
        """
        Validates disableKeys/enableKeys for all standard keys (Feature 0x4522)
        [1]disableKeys(keysToDisable)
        [2]enableKeys(keysToEnable)
        """
        standard_keys_id = DisableKeysByUsageTestUtils.get_keyboard_standard_key_id(
                                            test_case=self,
                                            keyboard_layout=self.button_stimuli_emulator._keyboard_layout.KEYS.keys())
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable game mode')
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.enable_game_mode(test_case=self)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send disableKeys all of standard keys')
        # ---------------------------------------------------------------------------
        disable_keys_resp = DisableKeysByUsageTestUtils.disable_keys_by_key_id(test_case=self,
                                                                               keys=standard_keys_id)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check disableKeys response fields")
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.DisableKeysResponseChecker.check_disable_keys_responses(
            test_case=self,
            messages=disable_keys_resp,
            expected_cls=self.feature_4522.disable_keys_response_cls)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate key strokes on all of standard keys')
        # ---------------------------------------------------------------------------
        keys_reports = KeyMatrixTestUtils.stroke_keys_in_sequence(test_case=self,
                                                                  keys=standard_keys_id,
                                                                  collect_hid_report=True)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate host can not receive key report')
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.check_keys_disabled(test_case=self,
                                                        keys_reports=keys_reports)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send enableKeys all of standard keys')
        # ---------------------------------------------------------------------------
        enable_keys_resp = DisableKeysByUsageTestUtils.enable_keys_by_key_id(test_case=self,
                                                                             keys=standard_keys_id)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check enableKeys response fields")
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.EnableKeysResponseChecker.check_enable_keys_responses(
            test_case=self,
            messages=enable_keys_resp,
            expected_cls=self.feature_4522.enable_keys_response_cls)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate key strokes on these enabled keys')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.stroke_keys_in_sequence(test_case=self,
                                                   keys=standard_keys_id)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate host can receive key report")
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.check_all_standard_keys_enabled(
                                            test_case=self,
                                            keyboard_layout=self.button_stimuli_emulator._keyboard_layout.KEYS.keys())

        self.testCaseChecked("FUN_4522_0001")
    # end def test_disable_all_standard_keys

    @features('Feature4522')
    @level('Functionality')
    @services('RequiredKeys', tuple(list(STANDARD_KEYS.keys())[:DisableKeys.LEN.KEYS_TO_DISABLE // 8]
                                    + [KEY_ID.GAME_MODE_KEY]))
    def test_check_stop_byte_with_disable_keys(self):
        """
        Validate disableKeys to insert stop byte 0x00 in the middle if Inputs.keysToDisable to make sure
        the disable keys should take effect before the stop byte(Feature 0x4522)
        [1]disableKeys(keysToDisable)
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable game mode')
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.enable_game_mode(test_case=self)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Select 16 keys to disable")
        # ---------------------------------------------------------------------------
        max_key_hid_usages_per_request = DisableKeys.LEN.KEYS_TO_DISABLE // 8
        disable_keys = list(STANDARD_KEYS)[:max_key_hid_usages_per_request]

        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over stop byte with range index 0 to 15')
        # ---------------------------------------------------------------------------
        for i in range(max_key_hid_usages_per_request):
            # ---------------------------------------------------------------------------
            LogHelper.log_step(
                self, f'Send disableKeys and replace index {i} to a stop byte "0x00"')
            # ---------------------------------------------------------------------------
            disable_keys[i] = 0x00
            disable_keys_resp = DisableKeysByUsageTestUtils.disable_keys_by_key_id(test_case=self,
                                                                                   keys=disable_keys)
            disable_keys[i] = list(STANDARD_KEYS)[i]

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, "Check disableKeys response fields")
            # ---------------------------------------------------------------------------
            DisableKeysByUsageTestUtils.DisableKeysResponseChecker.check_disable_keys_responses(
                test_case=self,
                messages=disable_keys_resp,
                expected_cls=self.feature_4522.disable_keys_response_cls)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Emulate key strokes on these disabled keys')
            # ---------------------------------------------------------------------------
            KeyMatrixTestUtils.stroke_keys_in_sequence(test_case=self,
                                                       keys=disable_keys)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate only keys before index {i} are disabled')
            # ---------------------------------------------------------------------------
            DisableKeysByUsageTestUtils.check_keys_enabled(test_case=self,
                                                           keys=disable_keys[i:])

        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("FUN_4522_0002")
    # end def test_check_stop_byte_with_disable_keys

    @features('Feature4522')
    @level('Functionality')
    @services('RequiredKeys', tuple(list(STANDARD_KEYS.keys())[:DisableKeys.LEN.KEYS_TO_DISABLE // 8]
                                    + [KEY_ID.GAME_MODE_KEY]))
    def test_check_stop_byte_with_enable_keys(self):
        """
        Validate enableKeys to insert stop byte 0x00 in the middle if Inputs.keysToEnable to make sure
        the enable keys should take effect before the stop byte(Feature 0x4522)
        [1]disableKeys(keysToDisable)
        [2]enableKeys(keysToEnable)
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable game mode')
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.enable_game_mode(test_case=self)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Select 16 keys to disable")
        # ---------------------------------------------------------------------------
        max_key_hid_usages_per_request = DisableKeys.LEN.KEYS_TO_DISABLE // 8
        keys = list(STANDARD_KEYS)[:max_key_hid_usages_per_request]

        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over stop byte with range index 0 to 15')
        # ---------------------------------------------------------------------------
        for i in range(max_key_hid_usages_per_request):
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send disableKeys')
            # ---------------------------------------------------------------------------
            disable_keys_resp = DisableKeysByUsageTestUtils.disable_keys_by_key_id(test_case=self,
                                                                                   keys=keys)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, "Check disableKeys response fields")
            # ---------------------------------------------------------------------------
            DisableKeysByUsageTestUtils.DisableKeysResponseChecker.check_disable_keys_responses(
                test_case=self,
                messages=disable_keys_resp,
                expected_cls=self.feature_4522.disable_keys_response_cls)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Emulate key strokes on these disabled keys')
            # ---------------------------------------------------------------------------
            keys_reports = KeyMatrixTestUtils.stroke_keys_in_sequence(test_case=self,
                                                                      keys=keys,
                                                                      collect_hid_report=True)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate disabled keys are disabled')
            # ---------------------------------------------------------------------------
            DisableKeysByUsageTestUtils.check_keys_disabled(test_case=self,
                                                            keys_reports=keys_reports)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send enableKeys and replace index {i} to a stop byte "0x00"')
            # ---------------------------------------------------------------------------
            keys[i] = 0x00
            enable_keys_resp = DisableKeysByUsageTestUtils.enable_keys_by_key_id(test_case=self,
                                                                                 keys=keys)
            keys[i] = list(STANDARD_KEYS)[i]

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, "Check enableKeys response fields")
            # ---------------------------------------------------------------------------
            DisableKeysByUsageTestUtils.EnableKeysResponseChecker.check_enable_keys_responses(
                test_case=self,
                messages=enable_keys_resp,
                expected_cls=self.feature_4522.enable_keys_response_cls)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Emulate key strokes on these enabled')
            # ---------------------------------------------------------------------------
            KeyMatrixTestUtils.stroke_keys_in_sequence(test_case=self,
                                                       keys=keys)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate only keys before index {i} are enabled')
            # ---------------------------------------------------------------------------
            DisableKeysByUsageTestUtils.check_keys_enabled(test_case=self,
                                                           keys=keys[:i])
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked('FUN_4522_0003')
    # end def test_check_stop_byte_with_enable_keys

    @features('Feature4522')
    @features('Wireless')
    @level('Functionality')
    @services('PowerSupply')
    @services('RequiredKeys', (KEY_ID.GAME_MODE_KEY, KEY_ID.KEYBOARD_A))
    def test_disable_keys_reset_after_restart(self):
        """
        Verify disable keys will reset when DUT restart (Feature 0x4522)
        [1]disableKeys(keysToDisable)
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable game mode')
        # ----------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.enable_game_mode(test_case=self)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send disable key "A"')
        # ----------------------------------------------------------------------------
        disable_keys_resp = DisableKeysByUsageTestUtils.disable_keys_by_key_id(test_case=self,
                                                                               keys=[KEY_ID.KEYBOARD_A])

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check disableKeys response fields")
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.DisableKeysResponseChecker.check_disable_keys_responses(
            test_case=self,
            messages=disable_keys_resp,
            expected_cls=self.feature_4522.disable_keys_response_cls)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate key strokes on "A" key')
        # ----------------------------------------------------------------------------
        keys_reports = KeyMatrixTestUtils.stroke_keys_in_sequence(test_case=self,
                                                                  keys=[KEY_ID.KEYBOARD_A],
                                                                  collect_hid_report=True)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate "A" is disabled')
        # ----------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.check_keys_disabled(test_case=self,
                                                        keys_reports=keys_reports)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power OFF->ON DUT')
        # ----------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable game mode')
        # ----------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.enable_game_mode(test_case=self)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate key strokes on "A" key')
        # ----------------------------------------------------------------------------
        KeyMatrixTestUtils.stroke_keys_in_sequence(test_case=self,
                                                   keys=[KEY_ID.KEYBOARD_A])

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate "A" is enabled')
        # ----------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.check_keys_enabled(test_case=self,
                                                       keys=[KEY_ID.KEYBOARD_A])

        self.testCaseChecked('FUN_4522_0004')
    # end def test_disable_keys_reset_after_restart

    @features('Feature4522')
    @features('Wireless')
    @level('Functionality')
    @services('PowerSupply')
    @services('PowerSwitch')
    @services('RequiredKeys', (KEY_ID.GAME_MODE_KEY, KEY_ID.KEYBOARD_A))
    def test_disable_keys_reset_after_restart_by_power_switch(self):
        """
        Verify disable keys will reset when DUT restarted by power switch (Feature 0x4522)
        [1]disableKeys(keysToDisable)
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable game mode')
        # ----------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.enable_game_mode(test_case=self)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send disable key "A"')
        # ----------------------------------------------------------------------------
        disable_keys_resp = DisableKeysByUsageTestUtils.disable_keys_by_key_id(test_case=self,
                                                                               keys=[KEY_ID.KEYBOARD_A])

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check disableKeys response fields")
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.DisableKeysResponseChecker.check_disable_keys_responses(
            test_case=self,
            messages=disable_keys_resp,
            expected_cls=self.feature_4522.disable_keys_response_cls)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate key strokes on "A" key')
        # ----------------------------------------------------------------------------
        keys_reports = KeyMatrixTestUtils.stroke_keys_in_sequence(test_case=self,
                                                                  keys=[KEY_ID.KEYBOARD_A],
                                                                  collect_hid_report=True)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate "A" is disabled')
        # ----------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.check_keys_disabled(test_case=self,
                                                        keys_reports=keys_reports)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power OFF->ON DUT')
        # ----------------------------------------------------------------------------
        self.power_slider_emulator.reset()

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable game mode')
        # ----------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.enable_game_mode(test_case=self)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate key strokes on "A" key')
        # ----------------------------------------------------------------------------
        KeyMatrixTestUtils.stroke_keys_in_sequence(test_case=self,
                                                   keys=[KEY_ID.KEYBOARD_A])

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate "A" is enabled')
        # ----------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.check_keys_enabled(test_case=self,
                                                       keys=[KEY_ID.KEYBOARD_A])

        self.testCaseChecked('FUN_4522_0005')
    # end def test_disable_keys_reset_after_restart_by_power_switch
# end class DisableKeysByUsageFunctionalityTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
