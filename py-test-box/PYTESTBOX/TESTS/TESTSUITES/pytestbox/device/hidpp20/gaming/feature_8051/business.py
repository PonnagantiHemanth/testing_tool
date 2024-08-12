#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_8051.business
:brief: HID++ 2.0 ``LogiModifiers`` business test suite
:author: Zane Lu <zlu@logitech.com>
:date: 2023/05/09
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import MAKE
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.base.logimodifiersutils import LogiModifiersTestUtils
from pytestbox.device.hidpp20.gaming.feature_8051.logimodifiers import LogiModifiersTestCase


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Zane Lu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LogiModifiersBusinessTestCase(LogiModifiersTestCase):
    """
    Validate ``LogiModifiers`` business test cases
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create a FKC profile")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        self.remapping_keys_info = self.init_fkc_profile()
    # end def setUp

    def verify_get_locally_state_of_a_modifier_key(self, key_id, key_name, check_state):
        """
        Verify the result of the function GetLocallyPressedState for a specific modifier key

        :param key_id: the key id of the modifier for check
        :type key_id: ``KEY_ID``
        :param key_name: the key name of the modifier for check
        :type key_name: ``str``
        :param check_state: true to check press state, false to check release state
        :type check_state: ``bool``
        """
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[key_id], delay=.1)

        if check_state:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send getLocallyPressedState request")
            # ----------------------------------------------------------------------------------------------------------
            response = LogiModifiersTestUtils.HIDppHelper.get_locally_pressed_state(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check {key_name} is pressed")
            # ----------------------------------------------------------------------------------------------------------
            checker = LogiModifiersTestUtils.GetLocallyPressedStateResponseChecker
            lps_check_map = LogiModifiersTestUtils.LocallyPressedStateChecker.get_default_check_map(self)
            lps_check_map.update({
                key_name: (lps_check_map[key_name][0], True)
            })
            check_map = {
                "locally_pressed_state": (
                    LogiModifiersTestUtils.GetLocallyPressedStateResponseChecker.check_locally_pressed_state,
                    lps_check_map)
            }
            checker.check_fields(self, response, self.feature_8051.get_locally_pressed_state_response_cls, check_map)
        # end if

        self.button_stimuli_emulator.multiple_keys_release(key_ids=[key_id], delay=.1)

        if not check_state:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send getLocallyPressedState request")
            # ----------------------------------------------------------------------------------------------------------
            response = LogiModifiersTestUtils.HIDppHelper.get_locally_pressed_state(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check {key_name} is released")
            # ----------------------------------------------------------------------------------------------------------
            checker = LogiModifiersTestUtils.GetLocallyPressedStateResponseChecker
            lps_check_map = LogiModifiersTestUtils.LocallyPressedStateChecker.get_default_check_map(self)
            lps_check_map.update({
                key_name: (lps_check_map[key_name][0], False)
            })
            check_map = {
                "locally_pressed_state": (
                    LogiModifiersTestUtils.GetLocallyPressedStateResponseChecker.check_locally_pressed_state,
                    lps_check_map)
            }
            checker.check_fields(self, response, self.feature_8051.get_locally_pressed_state_response_cls, check_map)
        # end if
    # end def verify_get_locally_state_of_a_modifier_key

    def verify_get_locally_states_of_modifier_keys(self, modifier_keys, press_state):
        """
        Verify the result of the function GetLocallyPressedState for all available modifier keys

        :param modifier_keys: the list of the modifier keys for check
        :type modifier_keys: ``dict``
        :param press_state: true to check press state, false to check release state
        :type press_state: ``bool``
        """
        for key_name, supported in self.locally_pressed_support.items():
            if supported:
                self.verify_get_locally_state_of_a_modifier_key(modifier_keys[key_name]["key_id"],
                                                                key_name, press_state)
            # end if
        # end for
    # end def verify_get_locally_states_of_modifier_keys

    def verify_press_event_for_a_modifier_key(self, key_id, key_name, enabled):
        """
        Verify the result of the press event for a specific modifier key

        :param key_id: the key id of the modifier for check
        :type key_id: ``KEY_ID``
        :param key_name: the key name of the modifier for check
        :type key_name: ``str``
        :param enabled: true to enable press event, false to disable press event
        :type enabled: ``bool``
        """
        params = {"g_shift": 0, "fn": 0, "right_gui": 0, "right_alt": 0, "right_shift": 0, "right_ctrl": 0,
                  "left_gui": 0, "left_alt": 0, "left_shift": 0, "left_ctrl": 0, key_name: enabled}
        ChannelUtils.empty_queues(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setPressEvents request")
        # --------------------------------------------------------------------------------------------------------------
        LogiModifiersTestUtils.HIDppHelper.set_press_events(
            test_case=self,
            **params)

        self.button_stimuli_emulator.keystroke(key_id=key_id)

        response = LogiModifiersTestUtils.HIDppHelper.press_event(
            test_case=self,
            check_first_message=False,
            allow_no_message=(not enabled))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the key event of {key_name}")
        # --------------------------------------------------------------------------------------------------------------
        if enabled:
            checker = LogiModifiersTestUtils.PressEventChecker
            lps_check_map = LogiModifiersTestUtils.LocallyPressedStateChecker.get_default_check_map(self)
            lps_check_map.update({
                key_name: (lps_check_map[key_name][0], enabled)
            })
            check_map = {
                "locally_pressed_state": (
                    LogiModifiersTestUtils.PressEventChecker.check_locally_pressed_state,
                    lps_check_map)
            }
            checker.check_fields(self, response, self.feature_8051.press_event_cls, check_map)
        else:
            self.assertNone(obtained=response, msg="Shall not get the key press event")
        # end if
    # end def verify_press_event_for_a_modifier_key

    def verify_press_event_for_modifier_keys(self, modifier_keys, enabled):
        """
        Verify the result of the press event for all available modifier keys

        :param modifier_keys: the list of the modifier keys for check
        :type modifier_keys: ``dict``
        :param enabled: true to enable press event, false to disable press event
        :type enabled: ``bool``
        """
        for key_name, supported in self.locally_pressed_support.items():
            if supported:
                self.verify_press_event_for_a_modifier_key(modifier_keys[key_name]["key_id"],
                                                           key_name, enabled)
            # end if
        # end for
    # end def verify_press_event_for_modifier_keys

    def verify_set_force_press_a_modifier(self, key_name, remapped_key_enabled, remapped_key_disabled):
        """
        Verify the result of the function SetForcedPressedState for a specific modifier key

        :param key_name: the key name of the modifier for check
        :type key_name: ``str``
        :param remapped_key_enabled: the key event for 'set_force_press' enabled
        :type remapped_key_enabled: ``RemappedKey``
        :param remapped_key_disabled: the key event for 'set_force_press' disabled
        :type remapped_key_disabled: ``RemappedKey | None``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setForcedPressedState request")
        # --------------------------------------------------------------------------------------------------------------
        params = {"g_shift": 0, "fn": 0, key_name: 1}
        LogiModifiersTestUtils.HIDppHelper.set_forced_pressed_state(
            test_case=self,
            **params)

        test_disabled = remapped_key_disabled is not None
        if test_disabled:
            params[key_name] = 0
            LogiModifiersTestUtils.HIDppHelper.set_forced_pressed_state(
                test_case=self,
                **params)
        # end if

        self.kosmos.sequencer.offline_mode = True
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press the trigger key")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=remapped_key_enabled.trigger_key)

        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence(block=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the action key")
        # --------------------------------------------------------------------------------------------------------------
        if not test_disabled:
            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id=remapped_key_enabled.action_key, state=MAKE))
            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id=remapped_key_enabled.action_key, state=BREAK))
            KeyMatrixTestUtils.KeyExpectedActions.reset()
        else:
            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id=remapped_key_disabled.action_key, state=MAKE))
            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id=remapped_key_disabled.action_key, state=BREAK))
            KeyMatrixTestUtils.KeyExpectedActions.reset()
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        params[key_name] = 0
        LogiModifiersTestUtils.HIDppHelper.set_forced_pressed_state(
            test_case=self,
            **params)
    # end def verify_set_force_press_a_modifier

    @features("Feature8051")
    @features('FullKeyCustomization')
    @level('Business', 'SmokeTests')
    def test_get_locally_pressed_states_of_modifier_keys(self):
        """
        Get the locally pressed states of modifier keys on the device which are available reported from getCapabilities
        """
        self.verify_get_locally_states_of_modifier_keys(
            modifier_keys=self.remapping_keys_info["modifier_keys"], press_state=True)
        self.testCaseChecked("BUS_8051_0001", _AUTHOR)
    # end def test_get_locally_pressed_states_of_modifier_keys

    @features("Feature8051")
    @features('FullKeyCustomization')
    @level("Business")
    def test_get_locally_released_states_of_modifier_keys(self):
        """
        Get the locally released states of modifier keys on the device which are available reported from getCapabilities
        """
        self.verify_get_locally_states_of_modifier_keys(
            modifier_keys=self.remapping_keys_info["modifier_keys"], press_state=False)
        self.testCaseChecked("BUS_8051_0002", _AUTHOR)
    # end def test_get_locally_released_states_of_modifier_keys

    @features("Feature8051")
    @features('FullKeyCustomization')
    @level("Business")
    def test_enable_event_reportings_for_modifiers(self):
        """
        Enable event reporting for modifiers which are available
        """
        self.verify_press_event_for_modifier_keys(
            modifier_keys=self.remapping_keys_info["modifier_keys"], enabled=True)
        self.testCaseChecked("BUS_8051_0003", _AUTHOR)
    # end def test_enable_event_reportings_for_modifiers

    @features("Feature8051")
    @features('FullKeyCustomization')
    @level("Business")
    def test_disable_event_reportings_for_modifiers(self):
        """
        Disable event reporting for modifiers which are available
        """
        self.verify_press_event_for_modifier_keys(
            modifier_keys=self.remapping_keys_info["modifier_keys"], enabled=False)
        self.testCaseChecked("BUS_8051_0004", _AUTHOR)
    # end def test_disable_event_reportings_for_modifiers

    @features("Feature8051")
    @features('FullKeyCustomization')
    @level("Business")
    def test_force_press_modifiers(self):
        """
        Force press modifiers
        """
        remapping_keys_info = self.remapping_keys_info
        test_enabled_key_index = 10
        enabled_key = remapping_keys_info["remapped_keys"][test_enabled_key_index]

        for key_name, supported in self.forceable_modifiers_support.items():
            if supported:
                self.verify_set_force_press_a_modifier(key_name=key_name,
                                                       remapped_key_enabled=enabled_key,
                                                       remapped_key_disabled=None)
            # end if
        # end for
        self.testCaseChecked("BUS_8051_0005", _AUTHOR)
    # end def test_force_press_modifiers

    @features("Feature8051")
    @features('FullKeyCustomization')
    @level("Business")
    def test_disable_force_press_modifiers(self):
        """
        Disable force press modifiers
        """
        remapping_keys_info = self.remapping_keys_info
        test_enabled_key_index = 10
        test_disabled_key_index = 12
        enabled_key = remapping_keys_info["remapped_keys"][test_enabled_key_index]
        disabled_key = remapping_keys_info["remapped_keys"][test_disabled_key_index]

        for key_name, supported in self.forceable_modifiers_support.items():
            if supported:
                self.verify_set_force_press_a_modifier(key_name=key_name,
                                                       remapped_key_enabled=enabled_key,
                                                       remapped_key_disabled=disabled_key)
            # end if
        # end for
        self.testCaseChecked("BUS_8051_0006", _AUTHOR)
    # end def test_disable_force_press_modifiers
# end class LogiModifiersBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
