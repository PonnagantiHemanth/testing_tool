#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.keyboard.feature_4521.business
:brief: HID++ 2.0 DisableKeys business test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2021/12/10
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid import HID_REPORTS
from pyhid.hiddispatcher import HIDDispatcher
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.disablekeysutils import DisableKeysUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4521.disablekeys import DisableKeysBaseTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DisableKeysBusinessTestCase(DisableKeysBaseTestCase):
    """
    0x4521 DisableKeys business test case
    """
    @features('Feature4521')
    @level('Business', 'SmokeTests')
    @services('KeyMatrix')
    def test_disable_then_enable_disableable_keys(self):
        """
        Validate Disable/Enable keys by SetDisabledKeys API

        disabledKeys [2]SetDisabledKeys
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send SetDisabledKeys with keyToDisable = {self.all_disableable_keys}')
        # ---------------------------------------------------------------------------
        set_disabled_keys_response = DisableKeysUtils.set_disabled_keys_by_key_id(test_case=self,
                                                                                  key_ids=self.all_disableable_keys)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(
            self, f'Validate SetDisabledKeys.disabledKeys value is equal to {self.all_disableable_keys}')
        # ---------------------------------------------------------------------------
        check_map = DisableKeysUtils.update_disabled_keys_for_check_map(test_case=self,
                                                                        keys_to_disable=self.all_disableable_keys)
        DisableKeysUtils.DisabledKeysResponseChecker.check_fields(
                                                        test_case=self,
                                                        message=set_disabled_keys_response,
                                                        expected_cls=self.feature_4521.set_disabled_keys_response_cls,
                                                        check_map=check_map)

        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, f'Test Loop over key ids in {self.all_disableable_keys}')
        # ---------------------------------------------------------------------------
        for key_id_to_stroke in self.all_disableable_keys:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate keystroke on "{key_id_to_stroke}"')
            # ---------------------------------------------------------------------------
            KeyMatrixTestUtils.stroke_key_with_fn(test_case=self, key_id=key_id_to_stroke)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate host cannot receive keystroke reports from the DUT')
            # ---------------------------------------------------------------------------
            self.check_key_disabled(key_id=key_id_to_stroke)
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ---------------------------------------------------------------------------

        # Empty hid_message_queue
        # TODO: Temporary workaround to clear the report returned when releasing the Left Win key
        # cf https://jira.logitech.io/browse/NRF52-503
        ChannelUtils.clean_messages(
            test_case=self, channel=self.current_channel, queue_name=HIDDispatcher.QueueName.HID,
            class_type=HID_REPORTS)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send SetDisabledKeys with keysToDisable = 0x00')
        # ---------------------------------------------------------------------------
        set_disabled_keys_response = DisableKeysUtils.HIDppHelper.set_disabled_keys(test_case=self,
                                                                                    keys_to_disable=0x00)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate SetDisabledKeys.disabledKeys value is equal to 0x00')
        # ---------------------------------------------------------------------------
        check_map = DisableKeysUtils.update_disabled_keys_for_check_map(test_case=self,
                                                                        keys_to_disable=0x00)
        DisableKeysUtils.DisabledKeysResponseChecker.check_fields(
                                                        test_case=self,
                                                        message=set_disabled_keys_response,
                                                        expected_cls=self.feature_4521.set_disabled_keys_response_cls,
                                                        check_map=check_map)

        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, f'Test Loop over key ids in {self.all_disableable_keys}')
        # ---------------------------------------------------------------------------
        for key_id_to_stroke in self.all_disableable_keys:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate keystroke on "{key_id_to_stroke}"')
            # ---------------------------------------------------------------------------
            KeyMatrixTestUtils.stroke_key_with_fn(test_case=self, key_id=key_id_to_stroke)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate host can receive keystroke reports from the DUT')
            # ---------------------------------------------------------------------------
            self.check_key_enabled(key_id=key_id_to_stroke)
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked('BUS_4521_0001')
    # end def test_disable_then_enable_disableable_keys
# end class DisableKeysBusinessTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
