#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.keyboard.feature_4521.functionality
:brief: HID++ 2.0 DisableKeys functionality test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2021/12/13
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from random import choice
from random import choices

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid import HID_REPORTS
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.configchange import ConfigChange
from pyhid.hidpp.features.configchange import SetConfigurationComplete
from pyhid.hidpp.features.configchange import SetConfigurationCompleteResponse
from pylibrary.tools.hexlist import HexList
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.disablekeysutils import DisableKeysUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4521.disablekeys import DisableKeysBaseTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DisableKeysFunctionalityTestCase(DisableKeysBaseTestCase):
    """
    0x4521 DisableKeys functionality test case
    """
    @features('Feature4521')
    @level('Functionality')
    def test_get_disabled_keys(self):
        """
        Validate host can get disabled key by GetDisabledKeys

        disabledKeys [1]GetDisabledKeys
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
        LogHelper.log_step(self, 'Send GetDisabledKeys request')
        # ---------------------------------------------------------------------------
        get_disabled_keys_response = DisableKeysUtils.HIDppHelper.get_disabled_keys(test_case=self)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(
            self, f'Validate GetDisabledKeys.disabledKeys value is equal to {self.all_disableable_keys}')
        # ---------------------------------------------------------------------------
        DisableKeysUtils.DisabledKeysResponseChecker.check_fields(
                                                        test_case=self,
                                                        message=get_disabled_keys_response,
                                                        expected_cls=self.feature_4521.get_disabled_keys_response_cls,
                                                        check_map=check_map)

        self.testCaseChecked('FUN_4521_0001')
    # end def test_get_disabled_keys

    @features('Feature4521')
    @level('Functionality')
    @services('KeyMatrix')
    def test_disabled_keys_with_all_combination(self):
        """
        Validate disableable keys can be disabled with all combination

        disabledKeys [2]SetDisabledKeys
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over supported keys in [0x00..0x1F]')
        # ---------------------------------------------------------------------------
        for supported_keys in choices(range(0x1F), k=8):
            # Skip unsupported key in this test
            if not DisableKeysUtils.check_keys_disableable_capability(test_case=self, keys_to_disable=supported_keys):
                continue
            # end if
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send SetDisabledKeys with keyToDisable = {supported_keys}')
            # ---------------------------------------------------------------------------
            set_disabled_keys_response = DisableKeysUtils.HIDppHelper.set_disabled_keys(test_case=self,
                                                                                        keys_to_disable=supported_keys)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate SetDisabledKeys.disabledKeys value is equal to {supported_keys}')
            # ---------------------------------------------------------------------------
            check_map = DisableKeysUtils.update_disabled_keys_for_check_map(test_case=self,
                                                                            keys_to_disable=supported_keys)
            DisableKeysUtils.DisabledKeysResponseChecker.check_fields(
                                                          test_case=self,
                                                          message=set_disabled_keys_response,
                                                          expected_cls=self.feature_4521.set_disabled_keys_response_cls,
                                                          check_map=check_map)

            # ---------------------------------------------------------------------------
            LogHelper.log_info(self, f'Test Loop over key ids in {self.all_disableable_keys}')
            # ---------------------------------------------------------------------------
            supported_keys_id = DisableKeysUtils.get_disabled_key_ids(test_case=self, value=supported_keys)
            # Get the KEY_ID list of specific disabled keys

            for key_id_to_stroke in self.all_disableable_keys:
                # ---------------------------------------------------------------------------
                LogHelper.log_step(self, f'Emulate keystroke on "{key_id_to_stroke}"')
                # ---------------------------------------------------------------------------
                KeyMatrixTestUtils.stroke_key_with_fn(test_case=self, key_id=key_id_to_stroke)

                # ---------------------------------------------------------------------------
                LogHelper.log_check(
                    self, 'Validate host can receive keystroke reports from the DUT. But except the disabled one')
                # ---------------------------------------------------------------------------
                if key_id_to_stroke in supported_keys_id:
                    self.check_key_disabled(key_id=key_id_to_stroke)
                    # check host cannot receive keystroke reports from the disabled key
                else:
                    self.check_key_enabled(key_id=key_id_to_stroke)
                    # check host can receive keystroke reports from the enabled key
                # end if
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
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked('FUN_4521_0002')
    # end def test_disabled_keys_with_all_combination

    @features('Feature4521')
    @level('Functionality')
    @services('KeyMatrix')
    def test_enabled_keys_with_all_combination(self):
        """
        Validate disableable keys can be enabled with all combination

        disabledKeys [2]SetDisabledKeys
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over supported keys in [0x00..0x1F]')
        # ---------------------------------------------------------------------------
        for supported_keys in choices(range(0x1F), k=8):
            # Skip unsupported key in this test
            if not DisableKeysUtils.check_keys_disableable_capability(test_case=self, keys_to_disable=supported_keys):
                continue
            # end if
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send SetDisabledKeys with keysToDisable = {self.all_disableable_keys}')
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
                LogHelper.log_step(self, f'Emulate keystroke on {key_id_to_stroke}')
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

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send SetDisabledKeys with keysToDisable = {supported_keys}')
            # ---------------------------------------------------------------------------
            set_disabled_keys_response = DisableKeysUtils.HIDppHelper.set_disabled_keys(test_case=self,
                                                                                        keys_to_disable=supported_keys)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate SetDisabledKeys.disabledKeys value is equal to {supported_keys}')
            # ---------------------------------------------------------------------------
            check_map = DisableKeysUtils.update_disabled_keys_for_check_map(test_case=self,
                                                                            keys_to_disable=supported_keys)
            DisableKeysUtils.DisabledKeysResponseChecker.check_fields(
                                                          test_case=self,
                                                          message=set_disabled_keys_response,
                                                          expected_cls=self.feature_4521.set_disabled_keys_response_cls,
                                                          check_map=check_map)
            # Empty hid_message_queue
            # TODO: Temporary workaround to clear the report returned when releasing the Left Win key
            # cf https://jira.logitech.io/browse/NRF52-503
            ChannelUtils.clean_messages(
                test_case=self, channel=self.current_channel, queue_name=HIDDispatcher.QueueName.HID,
                class_type=HID_REPORTS)

            # ---------------------------------------------------------------------------
            LogHelper.log_info(self, f'Test Loop over key ids in {self.all_disableable_keys}')
            # ---------------------------------------------------------------------------
            supported_keys_id = DisableKeysUtils.get_disabled_key_ids(test_case=self, value=supported_keys)
            # Get the KEY_ID list of specific disabled keys

            for key_id_to_stroke in self.all_disableable_keys:
                # ---------------------------------------------------------------------------
                LogHelper.log_step(self, f'Emulate keystroke on {key_id_to_stroke}')
                # ---------------------------------------------------------------------------
                KeyMatrixTestUtils.stroke_key_with_fn(test_case=self, key_id=key_id_to_stroke)

                # ---------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the host receives keystroke reports only when the key is enabled')
                # ---------------------------------------------------------------------------
                if key_id_to_stroke in supported_keys_id:
                    self.check_key_disabled(key_id=key_id_to_stroke)
                else:
                    self.check_key_enabled(key_id=key_id_to_stroke)
                # end if
            # end for
            # ---------------------------------------------------------------------------
            LogHelper.log_info(self, 'End Test Loop')
            # ---------------------------------------------------------------------------
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked('FUN_4521_0003')
    # end def test_enabled_keys_with_all_combination

    @features('Feature4521')
    @features('Feature0020')
    @level('Functionality')
    @services('KeyMatrix')
    def test_disabled_keys_reset_after_set_config(self):
        """
        Validate disabled keys can be reset by 0x0020.SetConfigurationComplete

        disabledKeys        [1]GetDisabledKeys
        disabledKeys        [2]SetDisabledKeys
        ConfigurationCookie [1]SetConfigurationComplete
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x0020)')
        # ---------------------------------------------------------------------------
        self.feature_0020_index = ChannelUtils.update_feature_mapping(test_case=self,
                                                                      feature_id=ConfigChange.FEATURE_ID)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send SetDisabledKeys with keysToDisable = {self.all_disableable_keys}')
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
            LogHelper.log_step(self, f'Emulate keystroke on {key_id_to_stroke}')
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

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send SetConfigurationComplete with ConfigurationCookie = 0x0000')
        # ---------------------------------------------------------------------------
        set_config_complete = SetConfigurationComplete(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                                       featureId=self.feature_0020_index,
                                                       configurationCookie=0)
        set_config_complete_response = ChannelUtils.send(test_case=self,
                                                         report=set_config_complete,
                                                         response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                         response_class_type=SetConfigurationCompleteResponse)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate SetConfigurationComplete.ConfigurationCookie value is equal to 0x0000')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=HexList('0000'),
                         obtained=set_config_complete_response.configurationCookie,
                         msg='The deviceName parameter differs from the one expected')

        # Empty hid_message_queue
        # TODO: Temporary workaround to clear the report returned when releasing the Left Win key
        # cf https://jira.logitech.io/browse/NRF52-503
        ChannelUtils.clean_messages(
            test_case=self, channel=self.current_channel, queue_name=HIDDispatcher.QueueName.HID,
            class_type=HID_REPORTS)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetDisabledKeys request')
        # ---------------------------------------------------------------------------
        get_disabled_keys_response = DisableKeysUtils.HIDppHelper.get_disabled_keys(test_case=self)

        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'Validate GetDisabledKeys.disabledKeys value is equal to 0x00')
        # ---------------------------------------------------------------------------
        DisableKeysUtils.DisabledKeysResponseChecker.check_fields(
                                                          test_case=self,
                                                          message=get_disabled_keys_response,
                                                          expected_cls=self.feature_4521.get_disabled_keys_response_cls)

        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, f'Test Loop over key ids in {self.all_disableable_keys}')
        # ---------------------------------------------------------------------------
        for key_id_to_stroke in self.all_disableable_keys:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate keystroke on {key_id_to_stroke}')
            # ---------------------------------------------------------------------------
            KeyMatrixTestUtils.stroke_key_with_fn(self, key_id=key_id_to_stroke)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate host can receive keystroke reports from the DUT')
            # ---------------------------------------------------------------------------
            self.check_key_enabled(key_id=key_id_to_stroke)
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked('FUN_4521_0004')
    # end def test_reset_disabled_key_by_set_config

    @features('Feature4521')
    @features('Wireless')
    @level('Functionality')
    @services('PowerSupply')
    @services('KeyMatrix')
    def test_disabled_keys_reset_after_restart(self):
        """
        Verify disable keys will reset when DUT restart (Feature 0x4521)

        disabledKeys [1]GetDisabledKeys
        disabledKeys [2]SetDisabledKeys
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send SetDisabledKeys with keysToDisable = {self.all_disableable_keys}')
        # ----------------------------------------------------------------------------
        set_disabled_keys_response = DisableKeysUtils.set_disabled_keys_by_key_id(test_case=self,
                                                                                  key_ids=self.all_disableable_keys)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate SetDisabledKeys.disabledKeys value is equal to all_disableable_keys')
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
            LogHelper.log_step(self, f'Emulate keystroke on {key_id_to_stroke}')
            # ---------------------------------------------------------------------------
            KeyMatrixTestUtils.stroke_key_with_fn(self, key_id=key_id_to_stroke)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate host cannot receive keystroke reports from the DUT')
            # ---------------------------------------------------------------------------
            self.check_key_disabled(key_id=key_id_to_stroke)
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ---------------------------------------------------------------------------

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power OFF->ON DUT')
        # ----------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetDisabledKeys request')
        # ----------------------------------------------------------------------------
        get_disabled_keys_response = DisableKeysUtils.HIDppHelper.get_disabled_keys(test_case=self)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate GetDisabledKeys.disabledKeys value is equal to 0x00')
        # ----------------------------------------------------------------------------
        DisableKeysUtils.DisabledKeysResponseChecker.check_fields(
            test_case=self, message=get_disabled_keys_response,
            expected_cls=self.feature_4521.get_disabled_keys_response_cls)

        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, f'Test Loop over key ids in {self.all_disableable_keys}')
        # ---------------------------------------------------------------------------
        for key_id_to_stroke in self.all_disableable_keys:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate keystroke on {key_id_to_stroke}')
            # ---------------------------------------------------------------------------
            KeyMatrixTestUtils.stroke_key_with_fn(self, key_id=key_id_to_stroke)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate host can receive keystroke reports from the DUT')
            # ---------------------------------------------------------------------------
            self.check_key_enabled(key_id=key_id_to_stroke)
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked('FUN_4521_0005')
    # end def test_disabled_keys_reset_after_restart

    @features('Feature4521')
    @features('Wireless')
    @level('Functionality')
    @services('PowerSwitch')
    @services('KeyMatrix')
    def test_disabled_keys_reset_after_restart_by_power_switch(self):
        """
        Verify disable keys will reset when DUT restart (Feature 0x4521)

        disabledKeys [1]GetDisabledKeys
        disabledKeys [2]SetDisabledKeys
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send SetDisabledKeys with keysToDisable = {self.all_disableable_keys}')
        # ----------------------------------------------------------------------------
        set_disabled_keys_response = DisableKeysUtils.set_disabled_keys_by_key_id(test_case=self,
                                                                                  key_ids=self.all_disableable_keys,)

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
            LogHelper.log_step(self, f'Emulate keystroke on {key_id_to_stroke}')
            # ---------------------------------------------------------------------------
            KeyMatrixTestUtils.stroke_key_with_fn(self, key_id=key_id_to_stroke)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate host cannot receive keystroke reports from the DUT')
            # ---------------------------------------------------------------------------
            self.check_key_disabled(key_id=key_id_to_stroke)
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ---------------------------------------------------------------------------

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power OFF->ON DUT')
        # ----------------------------------------------------------------------------
        self.power_slider_emulator.reset()
        # Empty hid_message_queue
        # TODO: Temporary workaround to clear the report returned when releasing the Left Win key
        # cf https://jira.logitech.io/browse/NRF52-503
        ChannelUtils.clean_messages(
            test_case=self, channel=self.current_channel, queue_name=HIDDispatcher.QueueName.HID,
            class_type=HID_REPORTS)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetDisabledKeys request')
        # ----------------------------------------------------------------------------
        get_disabled_keys_response = DisableKeysUtils.HIDppHelper.get_disabled_keys(test_case=self)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate GetDisabledKeys.disabledKeys value is equal to 0x00')
        # ----------------------------------------------------------------------------
        DisableKeysUtils.DisabledKeysResponseChecker.check_fields(
            test_case=self, message=get_disabled_keys_response,
            expected_cls=self.feature_4521.get_disabled_keys_response_cls)

        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, f'Test Loop over key ids in {self.all_disableable_keys}')
        # ---------------------------------------------------------------------------
        for key_id_to_stroke in self.all_disableable_keys:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate keystroke on {key_id_to_stroke}')
            # ---------------------------------------------------------------------------
            KeyMatrixTestUtils.stroke_key_with_fn(self, key_id=key_id_to_stroke)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate host can receive keystroke reports from the DUT')
            # ---------------------------------------------------------------------------
            self.check_key_enabled(key_id=key_id_to_stroke)
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked('FUN_4521_0006')
    # end def test_disabled_keys_reset_after_restart_by_power_switch

    @features('Feature4521')
    @level('Functionality')
    @services('KeyMatrix')
    def test_enabling_disabling_diff_keys_in_the_same_request(self):
        """
        Validate enabling a key and disabling another key in the same request should work with no error

        disabledKeys [2]SetDisabledKey
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, f'Test Loop over {self.all_disableable_keys}')
        # ---------------------------------------------------------------------------
        for key in self.all_disableable_keys:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send SetDisabledKeys with keysToDisable = {key}')
            # ---------------------------------------------------------------------------
            set_disabled_keys_response = DisableKeysUtils.set_disabled_keys_by_key_id(test_case=self,
                                                                                      key_ids=[key])

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self,
                                'Validate SetDisabledKeys.disabledKeys is equal to'
                                f' {DisableKeysUtils.convert_keys_ids_to_int(self, [key])}')
            # ---------------------------------------------------------------------------
            check_map = DisableKeysUtils.update_disabled_keys_for_check_map(test_case=self,
                                                                            keys_to_disable=[key])
            DisableKeysUtils.DisabledKeysResponseChecker.check_fields(
                                                          test_case=self,
                                                          message=set_disabled_keys_response,
                                                          expected_cls=self.feature_4521.set_disabled_keys_response_cls,
                                                          check_map=check_map)

            # ---------------------------------------------------------------------------
            LogHelper.log_info(self, f'Test Loop over key_id_to_stroke in {self.all_disableable_keys}')
            # ---------------------------------------------------------------------------
            for key_id_to_stroke in self.all_disableable_keys:
                # ---------------------------------------------------------------------------
                LogHelper.log_step(self, f'Emulate keystroke on {key_id_to_stroke}')
                # ---------------------------------------------------------------------------
                KeyMatrixTestUtils.stroke_key_with_fn(test_case=self, key_id=key_id_to_stroke)

                # ---------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate host can receive corresponding keystroke reports from the DUT')
                # ---------------------------------------------------------------------------
                if key_id_to_stroke == key:
                    self.check_key_disabled(key_id=key_id_to_stroke)
                else:
                    self.check_key_enabled(key_id=key_id_to_stroke)
                # end if
            # end for
            # ---------------------------------------------------------------------------
            LogHelper.log_info(self, f'End Test Loop')
            # ---------------------------------------------------------------------------
            # Empty hid_message_queue
            # TODO: Temporary workaround to clear the report returned when releasing the Left Win key
            # cf https://jira.logitech.io/browse/NRF52-503
            ChannelUtils.clean_messages(
                test_case=self, channel=self.current_channel, queue_name=HIDDispatcher.QueueName.HID,
                class_type=HID_REPORTS)

            other_key = choice([value for value in self.all_disableable_keys if value != key])
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send SetDisabledKeys with keysToDisable = {other_key}')
            # ---------------------------------------------------------------------------
            set_disabled_keys_response = DisableKeysUtils.set_disabled_keys_by_key_id(test_case=self,
                                                                                      key_ids=[other_key])

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self,
                                'Validate SetDisabledKeys.disabledKeys is equal to'
                                f' {DisableKeysUtils.convert_keys_ids_to_int(self, [other_key])}')
            # ---------------------------------------------------------------------------
            check_map = DisableKeysUtils.update_disabled_keys_for_check_map(test_case=self,
                                                                            keys_to_disable=[other_key])
            DisableKeysUtils.DisabledKeysResponseChecker.check_fields(
                                                      test_case=self,
                                                      message=set_disabled_keys_response,
                                                      expected_cls=self.feature_4521.set_disabled_keys_response_cls,
                                                      check_map=check_map)

            # ---------------------------------------------------------------------------
            LogHelper.log_info(self, f'Test Loop over key_id_to_stroke in {self.all_disableable_keys}')
            # ---------------------------------------------------------------------------
            for key_id_to_stroke in self.all_disableable_keys:
                # ---------------------------------------------------------------------------
                LogHelper.log_step(self, f'Emulate keystroke on {key_id_to_stroke}')
                # ---------------------------------------------------------------------------
                KeyMatrixTestUtils.stroke_key_with_fn(test_case=self, key_id=key_id_to_stroke)

                # ---------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate host can receive corresponding keystroke reports from the DUT')
                # ---------------------------------------------------------------------------
                if key_id_to_stroke == other_key:
                    self.check_key_disabled(key_id=key_id_to_stroke)
                else:
                    self.check_key_enabled(key_id=key_id_to_stroke)
                # end if
            # end for
            # ---------------------------------------------------------------------------
            LogHelper.log_info(self, f'End Test Loop')
            # ---------------------------------------------------------------------------

            # Empty hid_message_queue
            # TODO: Temporary workaround to clear the report returned when releasing the Left Win key
            # cf https://jira.logitech.io/browse/NRF52-503
            ChannelUtils.clean_messages(
                test_case=self, channel=self.current_channel, queue_name=HIDDispatcher.QueueName.HID,
                class_type=HID_REPORTS)
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, f'End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked('FUN_4521_0007')
    # end def test_enabling_disabling_diff_keys_in_the_same_request
# end class DisableKeysFunctionalityTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
