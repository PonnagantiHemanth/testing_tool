#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_8051.functionality
:brief: HID++ 2.0 ``LogiModifiers`` functionality test suite
:author: Zane Lu <zlu@logitech.com>
:date: 2023/05/12
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.logimodifiersutils import LogiModifiersTestUtils
from pytestbox.device.hidpp20.gaming.feature_8051.logimodifiers import LogiModifiersTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Zane Lu"
_LOOP_END = "End Test Loop"
_LOOP_START_TEST_KEYS = "Test loop over test keys"
_LOOP_START_MODIFIER_KEYS = "Test loop over modifier keys"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LogiModifiersFunctionalityTestCase(LogiModifiersTestCase):
    """
    Validate ``LogiModifiers`` functionality test cases
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

    @features("Feature8051")
    @features('FullKeyCustomization')
    @level("Functionality")
    def test_check_pressing_not_modifier_keys_no_raised_bits(self):
        """
        Check that pressing any other keys than modifiers does not raise bits
        in the getLocallyPressedState.locally_pressed_state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_TEST_KEYS)
        # --------------------------------------------------------------------------------------------------------------
        for key in self.remapping_keys_info["test_keys"]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Press a key which is not a modifier key")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key_id=key["key_id"])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send getLocallyPressedState request")
            # ----------------------------------------------------------------------------------------------------------
            response = LogiModifiersTestUtils.HIDppHelper.get_locally_pressed_state(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check locally pressed state")
            # ----------------------------------------------------------------------------------------------------------
            for field in self.locally_pressed_support.keys():
                if self.locally_pressed_support[field]:
                    fid = response.locally_pressed_state.getFidFromName(field)
                    self.assertEqual(expected=0, obtained=response.locally_pressed_state.getValue(fid, False),
                                     msg=f"Key '{field}' shall be in the RELEASE state")
                # end if
            # end for
            self.button_stimuli_emulator.key_release(key_id=key["key_id"])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8051_0001", _AUTHOR)
    # end def test_check_pressing_not_modifier_keys_no_raised_bits

    @features("Feature8051")
    @features('FullKeyCustomization')
    @level("Functionality")
    @services('SimultaneousKeystrokes')
    def test_check_pressing_standard_key_with_modifier_key_shall_raise_bit(self):
        """
        Check that pressing a combinaison of one modifier and another standard key will raise the correct bit
        in the getLocallyPressedState.locally_pressed_state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_TEST_KEYS)
        # --------------------------------------------------------------------------------------------------------------
        for test_key in self.remapping_keys_info["test_keys"]:
            for modifier_name, modifier_key in self.remapping_keys_info["modifier_keys"].items():
                if self.locally_pressed_support[modifier_name]:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, "Press a modifier key + a non-modifier key")
                    # --------------------------------------------------------------------------------------------------
                    combination_keys = [modifier_key["key_id"], test_key["key_id"]]
                    self.button_stimuli_emulator.multiple_keys_press(key_ids=combination_keys, delay=0.05)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, "Send getLocallyPressedState request")
                    # --------------------------------------------------------------------------------------------------
                    response = LogiModifiersTestUtils.HIDppHelper.get_locally_pressed_state(test_case=self)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, "Check locally pressed state")
                    # --------------------------------------------------------------------------------------------------
                    checker = LogiModifiersTestUtils.GetLocallyPressedStateResponseChecker
                    lps_check_map = LogiModifiersTestUtils.LocallyPressedStateChecker.get_default_check_map(self)
                    lps_check_map.update({
                        modifier_name: (lps_check_map[modifier_name][0], True)
                    })
                    check_map = {
                        "locally_pressed_state": (
                            LogiModifiersTestUtils.GetLocallyPressedStateResponseChecker.check_locally_pressed_state,
                            lps_check_map)
                    }
                    checker.check_fields(self, response, self.feature_8051.get_locally_pressed_state_response_cls,
                                         check_map)

                    self.button_stimuli_emulator.multiple_keys_release(key_ids=list(reversed(combination_keys)),
                                                                       delay=0.05)
                # end if
            # end for
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8051_0002", _AUTHOR)
    # end def test_check_pressing_standard_key_with_modifier_key_shall_raise_bit

    def verify_pressing_all_modifiers_simultaneously(self, virtual_key=None):
        """
        Press simultaneously and check the modifiers for the given layer (i.e. base, fn or g_shift)

        :param virtual_key: the name of the virtual key corresponding to the layer - OPTIONAL
        :type virtual_key: ``string``
        """
        self.assertIn(member=virtual_key, container=[None, "g_shift", "fn"])
        combination_keys = list()
        if virtual_key:
            combination_keys.append(self.remapping_keys_info["modifier_keys"][virtual_key]["key_id"])
        # end if
        for modifier_name, modifier_key in self.remapping_keys_info["modifier_keys"].items():
            if modifier_name not in ["g_shift", "fn"] and self.locally_pressed_support[modifier_name]:
                combination_keys.append(modifier_key["key_id"])
            # end if
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press all combination keys")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=combination_keys)
        sleep(0.5)

        response = LogiModifiersTestUtils.HIDppHelper.get_locally_pressed_state(test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check locally pressed state")
        # --------------------------------------------------------------------------------------------------------------
        checker = LogiModifiersTestUtils.GetLocallyPressedStateResponseChecker
        lps_check_map = LogiModifiersTestUtils.LocallyPressedStateChecker.get_default_check_map(self)

        for modifier_name, modifier_key in self.remapping_keys_info["modifier_keys"].items():
            if modifier_name not in ["g_shift", "fn"] and self.locally_pressed_support[modifier_name]:
                lps_check_map.update({
                    modifier_name: (lps_check_map[modifier_name][0], True)
                })
            # end if
        # end for

        if virtual_key:
            lps_check_map.update({
                virtual_key: (lps_check_map[virtual_key][0], True)
            })
        # end if

        check_map = {
            "locally_pressed_state": (
                LogiModifiersTestUtils.GetLocallyPressedStateResponseChecker.check_locally_pressed_state,
                lps_check_map)
        }
        checker.check_fields(self, response, self.feature_8051.get_locally_pressed_state_response_cls,
                             check_map)

        self.button_stimuli_emulator.multiple_keys_release(key_ids=list(reversed(combination_keys)))
    # end def verify_pressing_all_modifiers_simultaneously

    @features("Feature8051")
    @features('FullKeyCustomization')
    @level("Functionality")
    @services('SimultaneousKeystrokes')
    def test_check_pressing_all_modifiers_simultaneously(self):
        """
        Check that pressing all modifiers simultaneously will raise all supported bits
        in the getLocallyPressedState.locally_pressed_state
        """
        self.verify_pressing_all_modifiers_simultaneously()
        self.testCaseChecked("FUN_8051_0003#0001", _AUTHOR)
    # end def test_check_pressing_all_modifiers_simultaneously

    @features("Feature8051")
    @features('FullKeyCustomization')
    @features("Feature8051GShiftGettable")
    @level("Functionality")
    @services('SimultaneousKeystrokes')
    def test_check_pressing_all_modifiers_simultaneously_with_gshift(self):
        """
        Check that pressing all modifiers simultaneously will raise all supported bits
        in the getLocallyPressedState.locally_pressed_state
        """
        self.verify_pressing_all_modifiers_simultaneously(virtual_key="g_shift")
        self.testCaseChecked("FUN_8051_0003#0002", _AUTHOR)
    # end def test_check_pressing_all_modifiers_simultaneously_with_gshift

    @features("Feature8051")
    @features('FullKeyCustomization')
    @features("Feature8051FnGettable")
    @level("Functionality")
    @services('SimultaneousKeystrokes')
    def test_check_pressing_all_modifiers_simultaneously_with_fn(self):
        """
        Check that pressing all modifiers simultaneously will raise all supported bits
        in the getLocallyPressedState.locally_pressed_state
        """
        self.verify_pressing_all_modifiers_simultaneously(virtual_key="fn")
        self.testCaseChecked("FUN_8051_0003#0003", _AUTHOR)

    # end def test_check_pressing_all_modifiers_simultaneously_with_fn

    @features("Feature8051")
    @features('FullKeyCustomization')
    @level("Functionality")
    @services('KeyMatrix')
    def test_check_pressing_modifiers_incrementally(self):
        """
        Check that pressing all modifiers incrementally will raise the correct set of bits
        in the getLocallyPressedState.locally_pressed_state
        """
        pressed_key_names = list()
        combination_keys = list()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_MODIFIER_KEYS)
        # --------------------------------------------------------------------------------------------------------------
        for modifier_name, modifier_key in self.remapping_keys_info["modifier_keys"].items():
            if self.locally_pressed_support[modifier_name] and modifier_name != "g_shift" and modifier_name != "fn":
                combination_keys.append(modifier_key["key_id"])
                pressed_key_names.append(modifier_name)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Press the key '{modifier_name}'")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_press(key_id=modifier_key["key_id"])
                sleep(0.5)

                response = LogiModifiersTestUtils.HIDppHelper.get_locally_pressed_state(test_case=self)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check locally pressed state")
                # ------------------------------------------------------------------------------------------------------
                # noinspection DuplicatedCode
                for name in self.locally_pressed_support.keys():
                    fid = response.locally_pressed_state.getFidFromName(name)
                    if name in pressed_key_names:
                        self.assertEqual(expected=1, obtained=response.locally_pressed_state.getValue(fid, False),
                                         msg=f"Key '{name}' shall be in the MAKE state")
                    else:
                        self.assertEqual(expected=0, obtained=response.locally_pressed_state.getValue(fid, False),
                                         msg=f"Key '{name}' shall be in the RELEASE state")
                    # end if
                # end for
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_release(key_ids=list(reversed(combination_keys)),
                                                           delay=0.05)
        self.testCaseChecked("FUN_8051_0004", _AUTHOR)
    # end def test_check_pressing_modifiers_incrementally

    @features("Feature8051")
    @features('FullKeyCustomization')
    @level("Functionality")
    @services('SimultaneousKeystrokes')
    def test_check_press_events_for_pressing_modifiers_simultaneously(self):
        """
        Check that pressing all modifiers simultaneously when event reporting is enabled shall
        generate a single HID++ event with the correct set of bits.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable the press event")
        # --------------------------------------------------------------------------------------------------------------
        LogiModifiersTestUtils.HIDppHelper.set_press_events(
            test_case=self,
            **self.locally_pressed_support)

        combination_keys = list()
        for modifier_name, modifier_key in self.remapping_keys_info["modifier_keys"].items():
            if self.locally_pressed_support[modifier_name]:
                combination_keys.append(modifier_key["key_id"])
            # end if
        # end for

        ChannelUtils.empty_queues(test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press all combination keys")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=combination_keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check PressEvent")
        # --------------------------------------------------------------------------------------------------------------
        response = LogiModifiersTestUtils.HIDppHelper.press_event(
            test_case=self,
            check_first_message=False)
        self.assertNotNone(obtained=response, msg="Shall get the Press event")

        response = LogiModifiersTestUtils.HIDppHelper.press_event(
            test_case=self,
            check_first_message=False,
            allow_no_message=True)
        self.assertNone(obtained=response, msg="Shall be no Press event")

        self.testCaseChecked("FUN_8051_0005", _AUTHOR)
    # end def test_check_press_events_for_pressing_modifiers_simultaneously

    @features("Feature8051")
    @features('FullKeyCustomization')
    @level("Functionality")
    @services('KeyMatrix')
    def test_check_press_events_for_pressing_modifiers_incrementally(self):
        """
        Check that pressing all modifiers incrementally when the event reporting is enabled
        shall generate multiple events with an incremental set of bits
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable press events")
        # --------------------------------------------------------------------------------------------------------------
        LogiModifiersTestUtils.HIDppHelper.set_press_events(
            test_case=self,
            **self.locally_pressed_support)

        pressed_key_names = list()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_MODIFIER_KEYS)
        # --------------------------------------------------------------------------------------------------------------
        for modifier_name, modifier_key in self.remapping_keys_info["modifier_keys"].items():
            if self.locally_pressed_support[modifier_name] and modifier_name != "g_shift" and modifier_name != "fn":
                pressed_key_names.append(modifier_name)

                ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Press the modifier key: {modifier_name}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_press(key_id=modifier_key["key_id"])

                response = LogiModifiersTestUtils.HIDppHelper.press_event(
                    test_case=self,
                    check_first_message=False)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check PressEvent fields")
                # ------------------------------------------------------------------------------------------------------
                # noinspection DuplicatedCode
                for name in self.locally_pressed_support.keys():
                    fid = response.locally_pressed_state.getFidFromName(name)
                    if name in pressed_key_names:
                        self.assertEqual(expected=1, obtained=response.locally_pressed_state.getValue(fid, False),
                                         msg=f"Key '{name}' shall be in the MAKE state")
                    else:
                        self.assertEqual(expected=0, obtained=response.locally_pressed_state.getValue(fid, False),
                                         msg=f"Key '{name}' shall be in the RELEASE state")
                    # end if
                # end for
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8051_0006", _AUTHOR)
    # end def test_check_press_events_for_pressing_modifiers_incrementally

    @features("Feature8051")
    @features('FullKeyCustomization')
    @level("Functionality")
    def test_check_releasing_a_modifier_key_for_press_events(self):
        """
        Check releasing a modifier key shall get the event when the reporting has been enabled
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable press events")
        # --------------------------------------------------------------------------------------------------------------
        LogiModifiersTestUtils.HIDppHelper.set_press_events(
            test_case=self,
            **self.locally_pressed_support)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_MODIFIER_KEYS)
        # --------------------------------------------------------------------------------------------------------------
        for modifier_name, modifier_key in self.remapping_keys_info["modifier_keys"].items():
            if self.locally_pressed_support[modifier_name]:
                ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Press the modifier key: {modifier_name}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_press(key_id=modifier_key["key_id"])

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check PressEvent fields")
                # ------------------------------------------------------------------------------------------------------
                response = LogiModifiersTestUtils.HIDppHelper.press_event(
                    test_case=self,
                    check_first_message=False)
                fid = response.locally_pressed_state.getFidFromName(modifier_name)
                self.assertEqual(expected=1, obtained=response.locally_pressed_state.getValue(fid, False),
                                 msg=f"Key '{modifier_name}' shall be in the MAKE state")

                ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Release the modifier key: {modifier_name}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_release(key_id=modifier_key["key_id"])

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check PressEvent fields")
                # ------------------------------------------------------------------------------------------------------
                response = LogiModifiersTestUtils.HIDppHelper.press_event(
                    test_case=self,
                    check_first_message=False
                )
                self.assertEqual(expected=0, obtained=response.locally_pressed_state.getValue(fid, False),
                                 msg=f"Key '{modifier_name}' shall be in the RELEASE state")
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8051_0007", _AUTHOR)
    # end def test_check_releasing_a_modifier_key_for_press_events

    @features("Feature8051")
    @features('FullKeyCustomization')
    @level("Functionality")
    def test_check_release_event_for_enable_event_reporting_of_a_modifier_which_is_already_pressed(self):
        """
        Enable the event reporting of a modifier which is already pressed.
        We shall receive the event for the release.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_MODIFIER_KEYS)
        # --------------------------------------------------------------------------------------------------------------
        for key_name, supported in self.locally_pressed_support.items():
            if not supported:
                continue
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Disable press events")
            # ----------------------------------------------------------------------------------------------------------
            params = {"g_shift": 0, "fn": 0,
                      "right_gui": 0, "right_alt": 0, "right_shift": 0, "right_ctrl": 0,
                      "left_gui": 0, "left_alt": 0, "left_shift": 0, "left_ctrl": 0}
            LogiModifiersTestUtils.HIDppHelper.set_press_events(test_case=self, **params)

            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)

            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press the modifier key: {key_name}")
            # ------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key_id=self.remapping_keys_info["modifier_keys"][key_name]["key_id"])

            response = LogiModifiersTestUtils.HIDppHelper.press_event(
                test_case=self,
                check_first_message=False,
                allow_no_message=True)
            self.assertNone(obtained=response, msg="Shall not receiver the event!!!")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Enable press events")
            # ----------------------------------------------------------------------------------------------------------
            params[key_name] = 1
            LogiModifiersTestUtils.HIDppHelper.set_press_events(test_case=self, **params)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release the modifier key: {key_name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(
                key_id=self.remapping_keys_info["modifier_keys"][key_name]["key_id"])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check PressEvent fields")
            # ----------------------------------------------------------------------------------------------------------
            response = LogiModifiersTestUtils.HIDppHelper.press_event(
                test_case=self,
                check_first_message=False)

            fid = response.locally_pressed_state.getFidFromName(key_name)
            self.assertEqual(expected=0,
                             obtained=response.locally_pressed_state.getValue(fid, False),
                             msg="Shall receive key release event!!!")
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8051_0008", _AUTHOR)
    # end def test_check_release_event_for_enable_event_reporting_of_a_modifier_which_is_already_pressed

    @features("Feature8051")
    @features('FullKeyCustomization')
    @level("Functionality")
    def test_check_no_release_event_after_disable_the_event_reporting_of_a_modifier_which_is_already_pressed(self):
        """
        Disable the event reporting of a modifier which is already pressed.
        We shall not receive the event for the release.
        """
        ChannelUtils.empty_queues(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_MODIFIER_KEYS)
        # --------------------------------------------------------------------------------------------------------------
        for key_name, supported in self.locally_pressed_support.items():
            if not supported:
                continue
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Enable the press event for '{key_name}'")
            # ----------------------------------------------------------------------------------------------------------
            params = {"g_shift": 0, "fn": 0, "right_gui": 0, "right_alt": 0, "right_shift": 0, "right_ctrl": 0,
                      "left_gui": 0, "left_alt": 0, "left_shift": 0, "left_ctrl": 0, key_name: 1}
            LogiModifiersTestUtils.HIDppHelper.set_press_events(test_case=self, **params)
            self.button_stimuli_emulator.key_press(key_id=self.remapping_keys_info["modifier_keys"][key_name]["key_id"])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check PressEvent fields")
            # ----------------------------------------------------------------------------------------------------------
            response = LogiModifiersTestUtils.HIDppHelper.press_event(
                test_case=self,
                check_first_message=False)
            fid = response.locally_pressed_state.getFidFromName(key_name)
            self.assertEqual(expected=1,
                             obtained=response.locally_pressed_state.getValue(fid, False),
                             msg="Shall receive key press event!!!")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Disable the press event for '{key_name}'")
            # ----------------------------------------------------------------------------------------------------------
            params[key_name] = 0
            LogiModifiersTestUtils.HIDppHelper.set_press_events(test_case=self, **params)
            self.button_stimuli_emulator.key_release(
                key_id=self.remapping_keys_info["modifier_keys"][key_name]["key_id"])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check PressEvent fields")
            # ----------------------------------------------------------------------------------------------------------
            response = LogiModifiersTestUtils.HIDppHelper.press_event(
                test_case=self,
                check_first_message=False,
                allow_no_message=True)
            self.assertNone(obtained=response, msg="Shall not receive the key release event!!!")
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8051_0009", _AUTHOR)
    # end def test_check_no_release_event_after_disable_the_event_reporting_of_a_modifier_which_is_already_pressed

    @features("Feature8051")
    @features('FullKeyCustomization')
    @level("Functionality")
    def test_check_release_event_for_force_press_a_modifier_which_is_already_manually_pressed_by_the_user(self):
        """
        Force press a modifier which is already manually pressed by the user.
        We shall receive the event when the user manually releases it.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_MODIFIER_KEYS)
        # --------------------------------------------------------------------------------------------------------------
        for key_name, supported in self.forceable_modifiers_support.items():
            if not supported:
                continue
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Enable the press event for '{key_name}'")
            # ----------------------------------------------------------------------------------------------------------
            set_pressed_event_params = {"g_shift": 0, "fn": 0,
                                        "right_gui": 0, "right_alt": 0, "right_shift": 0, "right_ctrl": 0,
                                        "left_gui": 0, "left_alt": 0, "left_shift": 0, "left_ctrl": 0,
                                        key_name: 1}
            LogiModifiersTestUtils.HIDppHelper.set_press_events(test_case=self, **set_pressed_event_params)

            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press the key '{key_name}'")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key_id=self.remapping_keys_info["modifier_keys"][key_name]["key_id"])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check locally press state")
            # ----------------------------------------------------------------------------------------------------------
            response = LogiModifiersTestUtils.HIDppHelper.press_event(
                test_case=self,
                check_first_message=False)
            fid = response.locally_pressed_state.getFidFromName(key_name)
            self.assertEqual(expected=1,
                             obtained=response.locally_pressed_state.getValue(fid, False),
                             msg="Shall receive key press event!!!")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Force press the key '{key_name}'")
            # ----------------------------------------------------------------------------------------------------------
            forced_press_params = {"g_shift": 0, "fn": 0, key_name: 1}
            LogiModifiersTestUtils.HIDppHelper.set_forced_pressed_state(
                test_case=self,
                **forced_press_params)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release the key '{key_name}'")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(
                key_id=self.remapping_keys_info["modifier_keys"][key_name]["key_id"])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check locally press state")
            # ----------------------------------------------------------------------------------------------------------
            response = LogiModifiersTestUtils.HIDppHelper.press_event(
                test_case=self,
                check_first_message=False)
            fid = response.locally_pressed_state.getFidFromName(key_name)
            self.assertEqual(expected=0,
                             obtained=response.locally_pressed_state.getValue(fid, False),
                             msg="Shall receive key release event!!!")

            forced_press_params[key_name] = 0
            LogiModifiersTestUtils.HIDppHelper.set_forced_pressed_state(
                test_case=self,
                **forced_press_params)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8051_0010", _AUTHOR)
    # end def test_check_release_event_for_force_press_a_modifier_which_is_already_manually_pressed_by_the_user

    @features("Feature8051")
    @features('FullKeyCustomization')
    @level("Functionality")
    def test_get_locally_press_state_not_affected_by_force_state(self):
        """
        Check getLocallyPressedState functions not affected by calls of forceState()
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_MODIFIER_KEYS)
        # --------------------------------------------------------------------------------------------------------------
        for key_name, supported in self.forceable_modifiers_support.items():
            if not supported:
                continue
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Force press the key '{key_name}'")
            # ----------------------------------------------------------------------------------------------------------
            params = {"g_shift": 0, "fn": 0, key_name: 1}
            LogiModifiersTestUtils.HIDppHelper.set_forced_pressed_state(test_case=self, **params)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check locally press state")
            # ----------------------------------------------------------------------------------------------------------
            response = LogiModifiersTestUtils.HIDppHelper.get_locally_pressed_state(test_case=self)
            fid = response.locally_pressed_state.getFidFromName(key_name)
            self.assertEqual(expected=0,
                             obtained=response.locally_pressed_state.getValue(fid, False),
                             msg=f"Locally pressed state of '{key_name}' shall not be affected by "
                                 f"set_forced_pressed_state")

            params[key_name] = 0
            LogiModifiersTestUtils.HIDppHelper.set_forced_pressed_state(test_case=self, **params)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8051_0011", _AUTHOR)
    # end def test_get_locally_press_state_not_affected_by_force_state

    @features("Feature8051")
    @features('FullKeyCustomization')
    @level("Functionality")
    def test_the_event_shall_not_be_affected_by_set_forced_press_state(self):
        """
        Check the event shall not be affected by calls of setForcedPressedState()
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Enable the press events")
        # --------------------------------------------------------------------------------------------------------------
        LogiModifiersTestUtils.HIDppHelper.set_press_events(
            test_case=self,
            **self.locally_pressed_support)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_MODIFIER_KEYS)
        # --------------------------------------------------------------------------------------------------------------
        for key_name, supported in self.forceable_modifiers_support.items():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Force press the key '{key_name}'")
            # ----------------------------------------------------------------------------------------------------------
            params = {"g_shift": 0, "fn": 0, key_name: 1}
            LogiModifiersTestUtils.HIDppHelper.set_forced_pressed_state(test_case=self, **params)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "No PressEvent received")
            # ----------------------------------------------------------------------------------------------------------
            response = LogiModifiersTestUtils.HIDppHelper.press_event(
                test_case=self,
                check_first_message=False,
                allow_no_message=True)
            self.assertNone(obtained=response, msg="shall be no event received!!!")

            params[key_name] = 0
            LogiModifiersTestUtils.HIDppHelper.set_forced_pressed_state(test_case=self, **params)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_8051_0012", _AUTHOR)
    # end def test_the_event_shall_not_be_affected_by_set_forced_press_state

# end class LogiModifiersFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
