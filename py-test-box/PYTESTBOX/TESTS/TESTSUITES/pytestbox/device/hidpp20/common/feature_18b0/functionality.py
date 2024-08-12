#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.common.feature_18b0.functionality
:brief: HID++ 2.0 ``StaticMonitorMode`` functionality test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/12/19
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import warnings

from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.staticmonitormode import EnhancedKeyboardModeEvent
from pyhid.hidpp.features.common.staticmonitormode import EnhancedKeyboardWithLargerMatrixModeEvent
from pyhid.hidpp.features.common.staticmonitormode import KeyboardModeEvent
from pyhid.hidpp.features.common.staticmonitormode import KeyboardWithLargerMatrixModeEvent
from pyhid.hidpp.features.common.staticmonitormode import MouseModeEvent
from pyhid.hidpp.features.common.staticmonitormode import StaticMonitorMode
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.base.staticmonitormodeutils import StaticMonitorModeTestUtils
from pytestbox.device.hidpp20.common.feature_18b0.staticmonitormode import StaticMonitorModeTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_CHECK_MONITOR_MODE_RESPONSE = "Check SetMonitorModeResponse fields"
_END_TEST_LOOP = "End Test Loop"
_KEY_PRESS = "UserAction: KeyPress"
_SET_MONITOR_MODE_0 = "Send SetMonitorMode request with mode: 0 (OFF)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
@bugtracker.class_decorator('MonitorMode_BadRowColValues')
class StaticMonitorModeFunctionalityTestCase(StaticMonitorModeTestCase):
    """
    Validate ``StaticMonitorMode`` functionality test cases
    """

    @features("Feature18B0")
    @features("KeyboardMode")
    @level("Functionality")
    def test_kbd_set_monitor_mode_validate_parameter_mode_0_1_0(self):
        """
        Validate parameter - mode (keyboard)

        Rationale: validate both transitions (OFF->ON->OFF)

        [0] setMonitorMode(mode)
        """
        key = KeyMatrixTestUtils.get_key_list(test_case=self, group_count=1, group_size=1, random=True)[0][0]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over mode valid range [0 - OFF, 1 - ON, 0 - OFF]")
        # --------------------------------------------------------------------------------------------------------------
        for mode in [StaticMonitorMode.OFF, StaticMonitorMode.KBD_ON, StaticMonitorMode.OFF]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetMonitorMode request with a mode: {mode}")
            # ----------------------------------------------------------------------------------------------------------
            response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
            # ----------------------------------------------------------------------------------------------------------
            checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
            checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check MonitorModeEvent if mode is ON, Else check HID Make report")
            # ----------------------------------------------------------------------------------------------------------
            if mode == StaticMonitorMode.OFF:
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key, MAKE))
            else:
                row_col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(self, key)
                event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self,
                                                                                            check_first_message=False)
                keyboard_mode_event = KeyboardModeEvent.fromHexList(HexList(event))
                checker = StaticMonitorModeTestUtils.KeyboardModeEventChecker
                check_map = checker.get_default_check_map(self)
                check_map.update(
                    {
                        "row_col_code": (checker.check_row_col_code, row_col_code),
                        "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.MAKE)
                    }
                )
                checker.check_fields(self, keyboard_mode_event, KeyboardModeEvent, check_map)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check MonitorModeEvent if mode is ON, Else check HID Break report")
            # ----------------------------------------------------------------------------------------------------------
            if mode == StaticMonitorMode.OFF:
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key, BREAK))
            else:
                row_col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(self, key)
                event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(
                    self, check_first_message=False)
                keyboard_mode_event = KeyboardModeEvent.fromHexList(HexList(event))
                checker = StaticMonitorModeTestUtils.KeyboardModeEventChecker
                check_map = checker.get_default_check_map(self)
                check_map.update(
                    {
                        "row_col_code": (checker.check_row_col_code, row_col_code),
                        "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.BREAK)
                    }
                )
                checker.check_fields(self, keyboard_mode_event, KeyboardModeEvent, check_map)
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_18B0_0001", _AUTHOR)
    # end def test_kbd_set_monitor_mode_validate_parameter_mode_0_1_0

    @features("Feature18B0")
    @features("Mice")
    @level("Functionality")
    @services("RequiredKeys", (KEY_ID.LEFT_BUTTON,))
    def test_mouse_set_monitor_mode_validate_parameter_mode_0_2_0(self):
        """
        Validate parameter - mode (mouse)

        Rationale: validate both transitions (OFF->ON->OFF)

        [0] setMonitorMode(mode)
        """
        button = KEY_ID.LEFT_BUTTON
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over mode valid range [0 - OFF, 2 - ON, 0 - OFF]")
        # --------------------------------------------------------------------------------------------------------------
        for mode in [StaticMonitorMode.OFF, StaticMonitorMode.MOUSE_ON, StaticMonitorMode.OFF]:
            switch = HexList("00" * (MouseModeEvent.LEN.SWITCHES // 8))
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetMonitorMode request with a mode: {mode}")
            # ----------------------------------------------------------------------------------------------------------
            response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
            # ----------------------------------------------------------------------------------------------------------
            checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
            checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {button.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(button)
            switch = StaticMonitorModeTestUtils.update_switch(switch, button, set_bit=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check MonitorModeEvent if mode is ON, Else check HID Make report")
            # ----------------------------------------------------------------------------------------------------------
            if mode == StaticMonitorMode.OFF:
                warnings.warn("To be implemented when spurious motion algo branch is merged")

            else:
                event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(
                    self, check_first_message=False)
                mouse_mode_event = MouseModeEvent.fromHexList(HexList(event))
                checker = StaticMonitorModeTestUtils.MouseModeEventChecker
                check_map = checker.get_default_check_map(self)
                check_map.update({"switches": (checker.check_switches, switch)})
                checker.check_fields(self, mouse_mode_event, MouseModeEvent, check_map)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {button.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(button)
            switch = StaticMonitorModeTestUtils.update_switch(switch, button, clear_bit=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check MonitorModeEvent if mode is ON, Else check HID Break report")
            # ----------------------------------------------------------------------------------------------------------
            if mode == StaticMonitorMode.OFF:
                warnings.warn("To be implemented when spurious motion algo branch is merged")
            else:
                event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(
                    self, check_first_message=False)
                mouse_mode_event = MouseModeEvent.fromHexList(HexList(event))
                checker = StaticMonitorModeTestUtils.MouseModeEventChecker
                check_map = checker.get_default_check_map(self)
                check_map.update({"switches": (checker.check_switches, switch)})
                checker.check_fields(self, mouse_mode_event, MouseModeEvent, check_map)
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_18B0_0002", _AUTHOR)
    # end def test_mouse_set_monitor_mode_validate_parameter_mode_0_2_0

    @features("Feature18B0")
    @features("EnhancedKeyboardMode")
    @level("Functionality")
    def test_kbd_set_monitor_mode_validate_parameter_mode_0_3_0(self):
        """
        Validate parameter - mode (enhanced keyboard)

        Rationale: validate both transitions (OFF->ON->OFF)

        [0] setMonitorMode(mode)
        """
        key = KeyMatrixTestUtils.get_key_list(test_case=self, group_count=1, group_size=1, random=True)[0][0]
        row_col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(self, key)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over mode valid range [0 - OFF, 3 - ON, 0 - OFF]")
        # --------------------------------------------------------------------------------------------------------------
        for mode in [StaticMonitorMode.OFF, StaticMonitorMode.ENHANCED_KBD_ON, StaticMonitorMode.OFF]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetMonitorMode request with a mode: {mode}")
            # ----------------------------------------------------------------------------------------------------------
            response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
            # ----------------------------------------------------------------------------------------------------------
            checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
            checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check MonitorModeEvent if mode is ON, Else check HID Make report")
            # ----------------------------------------------------------------------------------------------------------
            if mode == StaticMonitorMode.OFF:
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key, MAKE))
            else:
                event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(
                    self, check_first_message=False)
                enhanced_keyboard_mode_event = EnhancedKeyboardModeEvent.fromHexList(HexList(event))
                checker = StaticMonitorModeTestUtils.EnhancedKeyboardModeEventChecker
                check_map = checker.get_default_check_map(self)
                check_map.update(
                    {
                        "row_col_code_0": (checker.check_row_col_code_0, row_col_code)
                    }
                )
                checker.check_fields(self, enhanced_keyboard_mode_event, EnhancedKeyboardModeEvent, check_map)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check MonitorModeEvent if mode is ON, Else check HID Break report")
            # ----------------------------------------------------------------------------------------------------------
            if mode == StaticMonitorMode.OFF:
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key, BREAK))
            else:
                event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(
                    self, check_first_message=False)
                enhanced_keyboard_mode_event = EnhancedKeyboardModeEvent.fromHexList(HexList(event))
                checker = StaticMonitorModeTestUtils.EnhancedKeyboardModeEventChecker
                checker.check_fields(self, enhanced_keyboard_mode_event, EnhancedKeyboardModeEvent)
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_18B0_0003", _AUTHOR)
    # end def test_kbd_set_monitor_mode_validate_parameter_mode_0_3_0

    @features("Feature18B0v1")
    @features("KeyboardWithLargerMatrixMode")
    @level("Functionality")
    def test_kbd_set_monitor_mode_validate_parameter_mode_0_4_0(self):
        """
        Validate parameter - mode (keyboard with large matrix)

        Rationale: validate both transitions (OFF->ON->OFF)

        [0] setMonitorMode(mode)
        """
        key = KeyMatrixTestUtils.get_key_list(test_case=self, group_count=1, group_size=1, random=True)[0][0]
        row_code, col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(self, key, combined=False)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over mode valid range [0 - OFF, 4 - ON, 0 - OFF]")
        # --------------------------------------------------------------------------------------------------------------
        for mode in [StaticMonitorMode.OFF, StaticMonitorMode.KBD_LARGER_MATRIX, StaticMonitorMode.OFF]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetMonitorMode request with a mode: {mode}")
            # ----------------------------------------------------------------------------------------------------------
            response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
            # ----------------------------------------------------------------------------------------------------------
            checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
            checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check MonitorModeEvent if mode is ON, Else check HID Make report")
            # ----------------------------------------------------------------------------------------------------------
            if mode == StaticMonitorMode.OFF:
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key, MAKE))
            else:
                event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(
                    self, check_first_message=False)
                kbd_with_larger_matrix_mode_event = KeyboardWithLargerMatrixModeEvent.fromHexList(HexList(event))
                checker = StaticMonitorModeTestUtils.KeyboardWithLargerMatrixModeEventChecker
                check_map = checker.get_default_check_map(self)
                check_map.update(
                    {
                        "row_code": (checker.check_row_code, row_code),
                        "col_code": (checker.check_col_code, col_code),
                        "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.MAKE)
                    }
                )
                checker.check_fields(self, kbd_with_larger_matrix_mode_event, KeyboardWithLargerMatrixModeEvent,
                                     check_map)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check MonitorModeEvent if mode is ON, Else check HID Break report")
            # ----------------------------------------------------------------------------------------------------------
            if mode == StaticMonitorMode.OFF:
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key, BREAK))
            else:
                event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(
                    self, check_first_message=False)
                kbd_with_larger_matrix_mode_event = KeyboardWithLargerMatrixModeEvent.fromHexList(HexList(event))
                checker = StaticMonitorModeTestUtils.KeyboardWithLargerMatrixModeEventChecker
                check_map = checker.get_default_check_map(self)
                check_map.update(
                    {
                        "row_code": (checker.check_row_code, row_code),
                        "col_code": (checker.check_col_code, col_code),
                        "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.BREAK)
                    }
                )
                checker.check_fields(self, kbd_with_larger_matrix_mode_event, KeyboardWithLargerMatrixModeEvent,
                                     check_map)
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_18B0_0004", _AUTHOR)
    # end def test_kbd_set_monitor_mode_validate_parameter_mode_0_4_0

    @features("Feature18B0v1")
    @features("EnhancedKeyboardWithLargerMatrixMode")
    @level("Functionality")
    def test_kbd_set_monitor_mode_validate_parameter_mode_0_5_0(self):
        """
        Validate parameter - mode (enhanced keyboard with large matrix)

        Rationale: validate both transitions (0 <-> 5)

        [0] setMonitorMode(mode)
        """
        key = KeyMatrixTestUtils.get_key_list(test_case=self, group_count=1, group_size=1, random=True)[0][0]
        row_code, col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(self, key, combined=False)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over mode valid range [0 - OFF, 5 - ON, 0 - OFF]")
        # --------------------------------------------------------------------------------------------------------------
        for mode in [StaticMonitorMode.OFF, StaticMonitorMode.ENHANCED_KBD_LARGER_MATRIX, StaticMonitorMode.OFF]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetMonitorMode request with a mode: {mode}")
            # ----------------------------------------------------------------------------------------------------------
            response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
            # ----------------------------------------------------------------------------------------------------------
            checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
            checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check MonitorModeEvent if mode is ON, Else check HID Make report")
            # ----------------------------------------------------------------------------------------------------------
            if mode == StaticMonitorMode.OFF:
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key, MAKE))
            else:
                event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(
                    self, check_first_message=False)
                enhanced_kbd_with_larger_matrix_mode_event = EnhancedKeyboardWithLargerMatrixModeEvent.fromHexList(
                    HexList(event))
                checker = StaticMonitorModeTestUtils.EnhancedKeyboardWithLargerMatrixModeEventChecker
                check_map = checker.get_default_check_map(self)
                check_map.update(
                    {
                        "row_code_0": (checker.check_row_code_0, row_code),
                        "col_code_0": (checker.check_col_code_0, col_code)
                    }
                )
                checker.check_fields(self, enhanced_kbd_with_larger_matrix_mode_event,
                                     EnhancedKeyboardWithLargerMatrixModeEvent, check_map)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check MonitorModeEvent if mode is ON, Else check HID Break report")
            # ----------------------------------------------------------------------------------------------------------
            if mode == StaticMonitorMode.OFF:
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key, BREAK))
            else:
                event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(
                    self, check_first_message=False)
                enhanced_kbd_with_larger_matrix_mode_event = EnhancedKeyboardWithLargerMatrixModeEvent.fromHexList(
                    HexList(event))
                checker = StaticMonitorModeTestUtils.EnhancedKeyboardWithLargerMatrixModeEventChecker
                checker.check_fields(self, enhanced_kbd_with_larger_matrix_mode_event,
                                     EnhancedKeyboardWithLargerMatrixModeEvent)
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_18B0_0005", _AUTHOR)
    # end def test_kbd_set_monitor_mode_validate_parameter_mode_0_5_0

    @features("Feature18B0")
    @features("KeyboardMode")
    @level("Functionality")
    def test_kbd_set_monitor_mode_validate_parameter_mode_1_1(self):
        """
        Validate parameter - mode (keyboard)

        Rationale: validate same transitions (1 -> 1)

        [0] setMonitorMode(mode)
        """
        key = KeyMatrixTestUtils.get_key_list(test_case=self, group_count=1, group_size=1, random=True)[0][0]
        row_col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(self, key)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over mode valid range [1 - ON, 1 - ON]")
        # --------------------------------------------------------------------------------------------------------------
        for mode in [StaticMonitorMode.KBD_ON, StaticMonitorMode.KBD_ON]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetMonitorMode request with a mode: {mode}")
            # ----------------------------------------------------------------------------------------------------------
            response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
            # ----------------------------------------------------------------------------------------------------------
            checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
            checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check MonitorModeEvent")
            # ----------------------------------------------------------------------------------------------------------
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(
                self, check_first_message=False)
            keyboard_mode_event = KeyboardModeEvent.fromHexList(HexList(event))
            checker = StaticMonitorModeTestUtils.KeyboardModeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update(
                {
                    "row_col_code": (checker.check_row_col_code, row_col_code),
                    "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.MAKE)
                }
            )
            checker.check_fields(self, keyboard_mode_event, KeyboardModeEvent, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check MonitorModeEvent")
            # ----------------------------------------------------------------------------------------------------------
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(
                self, check_first_message=False)
            keyboard_mode_event = KeyboardModeEvent.fromHexList(HexList(event))
            checker = StaticMonitorModeTestUtils.KeyboardModeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update(
                {
                    "row_col_code": (checker.check_row_col_code, row_col_code),
                    "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.BREAK)
                }
            )
            checker.check_fields(self, keyboard_mode_event, KeyboardModeEvent, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_MONITOR_MODE_0)
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls, check_map)

        self.testCaseChecked("FUN_18B0_0006", _AUTHOR)
    # end def test_kbd_set_monitor_mode_validate_parameter_mode_1_1

    @features("Feature18B0")
    @features("Mice")
    @level("Functionality")
    @services("RequiredKeys", (KEY_ID.LEFT_BUTTON,))
    def test_mouse_set_monitor_mode_validate_parameter_mode_2_2(self):
        """
        Validate parameter - mode (mouse)

        Rationale: validate same transitions (2 -> 2)

        [0] setMonitorMode(mode)
        """
        button = KEY_ID.LEFT_BUTTON
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over mode valid range [2 - ON, 2 - ON]")
        # --------------------------------------------------------------------------------------------------------------
        for mode in [StaticMonitorMode.MOUSE_ON, StaticMonitorMode.MOUSE_ON]:
            switch = HexList("00" * (MouseModeEvent.LEN.SWITCHES // 8))
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetMonitorMode request with a mode: {mode}")
            # ----------------------------------------------------------------------------------------------------------
            response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
            # ----------------------------------------------------------------------------------------------------------
            checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
            checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {button.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(button)
            switch = StaticMonitorModeTestUtils.update_switch(switch, button, set_bit=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check MonitorModeEvent")
            # ----------------------------------------------------------------------------------------------------------
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
            mouse_mode_event = MouseModeEvent.fromHexList(HexList(event))
            checker = StaticMonitorModeTestUtils.MouseModeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({"switches": (checker.check_switches, switch)})
            checker.check_fields(self, mouse_mode_event, MouseModeEvent, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {button.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(button)
            switch = StaticMonitorModeTestUtils.update_switch(switch, button, clear_bit=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check MonitorModeEvent")
            # ----------------------------------------------------------------------------------------------------------
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
            mouse_mode_event = MouseModeEvent.fromHexList(HexList(event))
            checker = StaticMonitorModeTestUtils.MouseModeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({"switches": (checker.check_switches, switch)})
            checker.check_fields(self, mouse_mode_event, MouseModeEvent, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_MONITOR_MODE_0)
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        self.testCaseChecked("FUN_18B0_0007", _AUTHOR)
    # end def test_mouse_set_monitor_mode_validate_parameter_mode_2_2

    @features("Feature18B0")
    @features("EnhancedKeyboardMode")
    @level("Functionality")
    def test_kbd_set_monitor_mode_validate_parameter_mode_3_3(self):
        """
        Validate parameter - mode (enhanced keyboard)

        Rationale: validate same transitions (3 -> 3)

        [0] setMonitorMode(mode)
        """
        key = KeyMatrixTestUtils.get_key_list(test_case=self, group_count=1, group_size=1, random=True)[0][0]
        row_col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(self, key)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over mode valid range [3 - ON, 3 - ON]")
        # --------------------------------------------------------------------------------------------------------------
        for mode in [StaticMonitorMode.ENHANCED_KBD_ON, StaticMonitorMode.ENHANCED_KBD_ON]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetMonitorMode request with a mode: {mode}")
            # ----------------------------------------------------------------------------------------------------------
            response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
            # ----------------------------------------------------------------------------------------------------------
            checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
            checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check MonitorModeEvent")
            # ----------------------------------------------------------------------------------------------------------
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
            enhanced_keyboard_mode_event = EnhancedKeyboardModeEvent.fromHexList(HexList(event))
            checker = StaticMonitorModeTestUtils.EnhancedKeyboardModeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({"row_col_code_0": (checker.check_row_col_code_0, row_col_code)})
            checker.check_fields(self, enhanced_keyboard_mode_event, EnhancedKeyboardModeEvent, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check MonitorModeEvent")
            # ----------------------------------------------------------------------------------------------------------
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
            enhanced_keyboard_mode_event = EnhancedKeyboardModeEvent.fromHexList(HexList(event))
            checker = StaticMonitorModeTestUtils.EnhancedKeyboardModeEventChecker
            checker.check_fields(self, enhanced_keyboard_mode_event, EnhancedKeyboardModeEvent)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_MONITOR_MODE_0)
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        self.testCaseChecked("FUN_18B0_0008", _AUTHOR)
    # end def test_kbd_set_monitor_mode_validate_parameter_mode_3_3

    @features("Feature18B0v1")
    @features("KeyboardWithLargerMatrixMode")
    @level("Functionality")
    def test_kbd_set_monitor_mode_validate_parameter_mode_4_4(self):
        """
        Validate parameter - mode (keyboard with large matrix)

        Rationale: validate same transitions (4 -> 4)

        [0] setMonitorMode(mode)
        """
        key = KeyMatrixTestUtils.get_key_list(test_case=self, group_count=1, group_size=1, random=True)[0][0]
        row_code, col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(test_case=self, key_id=key, combined=False)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over mode valid range [4 - ON, 4 - ON]")
        # --------------------------------------------------------------------------------------------------------------
        for mode in [StaticMonitorMode.KBD_LARGER_MATRIX, StaticMonitorMode.KBD_LARGER_MATRIX]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetMonitorMode request with a mode: {mode}")
            # ----------------------------------------------------------------------------------------------------------
            response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
            # ----------------------------------------------------------------------------------------------------------
            checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
            checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check MonitorModeEvent")
            # ----------------------------------------------------------------------------------------------------------
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
            kbd_with_larger_matrix_mode_event = KeyboardWithLargerMatrixModeEvent.fromHexList(HexList(event))
            checker = StaticMonitorModeTestUtils.KeyboardWithLargerMatrixModeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update(
                {
                    "row_code": (checker.check_row_code, row_code),
                    "col_code": (checker.check_col_code, col_code),
                    "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.MAKE)
                }
            )
            checker.check_fields(self, kbd_with_larger_matrix_mode_event, KeyboardWithLargerMatrixModeEvent, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check MonitorModeEvent")
            # ----------------------------------------------------------------------------------------------------------
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
            kbd_with_larger_matrix_mode_event = KeyboardWithLargerMatrixModeEvent.fromHexList(HexList(event))
            checker = StaticMonitorModeTestUtils.KeyboardWithLargerMatrixModeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update(
                {
                    "row_code": (checker.check_row_code, row_code),
                    "col_code": (checker.check_col_code, col_code),
                    "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.BREAK)
                }
            )
            checker.check_fields(self, kbd_with_larger_matrix_mode_event, KeyboardWithLargerMatrixModeEvent, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_MONITOR_MODE_0)
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        self.testCaseChecked("FUN_18B0_0009", _AUTHOR)
    # end def test_kbd_set_monitor_mode_validate_parameter_mode_4_4

    @features("Feature18B0v1")
    @features("EnhancedKeyboardWithLargerMatrixMode")
    @level("Functionality")
    def test_kbd_set_monitor_mode_validate_parameter_mode_5_5(self):
        """
        Validate parameter - mode (enhanced keyboard with large matrix)

        Rationale: validate same transitions (5 -> 5)

        [0] setMonitorMode(mode)
        """
        key = KeyMatrixTestUtils.get_key_list(test_case=self, group_count=1, group_size=1, random=True)[0][0]
        row_code, col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(test_case=self, key_id=key, combined=False)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over mode valid range [5 - ON, 5 - ON]")
        # --------------------------------------------------------------------------------------------------------------
        for mode in [StaticMonitorMode.ENHANCED_KBD_LARGER_MATRIX, StaticMonitorMode.ENHANCED_KBD_LARGER_MATRIX]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetMonitorMode request with a mode: {mode}")
            # ----------------------------------------------------------------------------------------------------------
            response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
            # ----------------------------------------------------------------------------------------------------------
            checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
            checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check MonitorModeEvent")
            # ----------------------------------------------------------------------------------------------------------
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
            enhanced_kbd_with_larger_matrix_mode_event = EnhancedKeyboardWithLargerMatrixModeEvent.fromHexList(
                HexList(event))
            checker = StaticMonitorModeTestUtils.EnhancedKeyboardWithLargerMatrixModeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update(
                {
                    "row_code_0": (checker.check_row_code_0, row_code),
                    "col_code_0": (checker.check_col_code_0, col_code)
                }
            )
            checker.check_fields(self, enhanced_kbd_with_larger_matrix_mode_event,
                                 EnhancedKeyboardWithLargerMatrixModeEvent, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check MonitorModeEvent")
            # ----------------------------------------------------------------------------------------------------------
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
            enhanced_kbd_with_larger_matrix_mode_event = EnhancedKeyboardWithLargerMatrixModeEvent.fromHexList(HexList(
                event))
            checker = StaticMonitorModeTestUtils.EnhancedKeyboardWithLargerMatrixModeEventChecker
            checker.check_fields(self, enhanced_kbd_with_larger_matrix_mode_event,
                                 EnhancedKeyboardWithLargerMatrixModeEvent)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_MONITOR_MODE_0)
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        self.testCaseChecked("FUN_18B0_0010", _AUTHOR)
    # end def test_kbd_set_monitor_mode_validate_parameter_mode_5_5

    @features("Feature18B0")
    @features("EnhancedKeyboardMode")
    @features("KeyboardMode")
    @level("Functionality")
    def test_kbd_set_monitor_mode_validate_parameter_mode_1_3(self):
        """
        Validate parameter - mode (keyboard & enhanced keyboard)

        Rationale: validate different transitions (1 <-> 3)

        [0] setMonitorMode(mode)
        """
        key = KeyMatrixTestUtils.get_key_list(test_case=self, group_count=1, group_size=1, random=True)[0][0]
        row_col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(self, key)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over mode valid range [1 - ON, 3 - ON, 1 - ON]")
        # --------------------------------------------------------------------------------------------------------------
        for mode in [StaticMonitorMode.KBD_ON, StaticMonitorMode.ENHANCED_KBD_ON, StaticMonitorMode.KBD_ON]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetMonitorMode request with a mode: {mode}")
            # ----------------------------------------------------------------------------------------------------------
            response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
            # ----------------------------------------------------------------------------------------------------------
            checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
            checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check MonitorModeEvent")
            # ----------------------------------------------------------------------------------------------------------
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
            if mode == StaticMonitorMode.KBD_ON:
                keyboard_mode_event = KeyboardModeEvent.fromHexList(HexList(event))
                checker = StaticMonitorModeTestUtils.KeyboardModeEventChecker
                check_map = checker.get_default_check_map(self)
                check_map.update(
                    {
                        "row_col_code": (checker.check_row_col_code, row_col_code),
                        "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.MAKE)
                    }
                )
                checker.check_fields(self, keyboard_mode_event, KeyboardModeEvent, check_map)

            elif mode == StaticMonitorMode.ENHANCED_KBD_ON:
                enhanced_keyboard_mode_event = EnhancedKeyboardModeEvent.fromHexList(HexList(event))
                checker = StaticMonitorModeTestUtils.EnhancedKeyboardModeEventChecker
                check_map = checker.get_default_check_map(self)
                check_map.update(
                    {
                        "row_col_code_0": (checker.check_row_col_code_0, row_col_code)
                    }
                )
                checker.check_fields(self, enhanced_keyboard_mode_event, EnhancedKeyboardModeEvent, check_map)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check MonitorModeEvent")
            # ----------------------------------------------------------------------------------------------------------
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
            if mode == StaticMonitorMode.KBD_ON:
                keyboard_mode_event = KeyboardModeEvent.fromHexList(HexList(event))
                checker = StaticMonitorModeTestUtils.KeyboardModeEventChecker
                check_map = checker.get_default_check_map(self)
                check_map.update(
                    {
                        "row_col_code": (checker.check_row_col_code, row_col_code),
                        "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.BREAK)
                    }
                )
                checker.check_fields(self, keyboard_mode_event, KeyboardModeEvent, check_map)

            elif mode == StaticMonitorMode.ENHANCED_KBD_ON:
                enhanced_keyboard_mode_event = EnhancedKeyboardModeEvent.fromHexList(HexList(event))
                checker = StaticMonitorModeTestUtils.EnhancedKeyboardModeEventChecker
                checker.check_fields(self, enhanced_keyboard_mode_event, EnhancedKeyboardModeEvent)
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_MONITOR_MODE_0)
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "mode": (checker.check_mode, StaticMonitorMode.OFF),
            }
        )
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls, check_map)

        self.testCaseChecked("FUN_18B0_0011", _AUTHOR)
    # end def test_kbd_set_monitor_mode_validate_parameter_mode_1_3

    @features("Feature18B0v1")
    @features("EnhancedKeyboardWithLargerMatrixMode")
    @features("KeyboardWithLargerMatrixMode")
    @level("Functionality")
    def test_kbd_set_monitor_mode_validate_parameter_mode_4_5(self):
        """
        Validate parameter - mode (keyboard with large matrix & enhanced keyboard with large matrix)

        Rationale: validate different transitions (4 <-> 5)

        [0] setMonitorMode(mode)
        """
        key = KeyMatrixTestUtils.get_key_list(test_case=self, group_count=1, group_size=1, random=True)[0][0]
        row_code, col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(test_case=self, key_id=key, combined=False)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over mode valid range [4 - ON, 5 - ON, 4 - ON]")
        # --------------------------------------------------------------------------------------------------------------
        for mode in [StaticMonitorMode.KBD_LARGER_MATRIX, StaticMonitorMode.ENHANCED_KBD_LARGER_MATRIX,
                     StaticMonitorMode.KBD_LARGER_MATRIX]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetMonitorMode request with a mode: {mode}")
            # ----------------------------------------------------------------------------------------------------------
            response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
            # ----------------------------------------------------------------------------------------------------------
            checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
            checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check MonitorModeEvent")
            # ----------------------------------------------------------------------------------------------------------
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
            if mode == StaticMonitorMode.KBD_LARGER_MATRIX:
                kbd_with_larger_matrix_mode_event = KeyboardWithLargerMatrixModeEvent.fromHexList(HexList(event))
                checker = StaticMonitorModeTestUtils.KeyboardWithLargerMatrixModeEventChecker
                check_map = checker.get_default_check_map(self)
                check_map.update(
                    {
                        "row_code": (checker.check_row_code, row_code),
                        "col_code": (checker.check_col_code, col_code),
                        "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.MAKE)
                    }
                )
                checker.check_fields(self, kbd_with_larger_matrix_mode_event, KeyboardWithLargerMatrixModeEvent,
                                     check_map)

            elif mode == StaticMonitorMode.ENHANCED_KBD_LARGER_MATRIX:
                enhanced_kbd_with_larger_matrix_mode_event = EnhancedKeyboardWithLargerMatrixModeEvent.fromHexList(
                    HexList(event))
                checker = StaticMonitorModeTestUtils.EnhancedKeyboardWithLargerMatrixModeEventChecker
                check_map = checker.get_default_check_map(self)
                check_map.update(
                    {
                        "row_code_0": (checker.check_row_code_0, row_code),
                        "col_code_0": (checker.check_col_code_0, col_code)
                    }
                )
                checker.check_fields(self, enhanced_kbd_with_larger_matrix_mode_event,
                                     EnhancedKeyboardWithLargerMatrixModeEvent,
                                     check_map)
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check MonitorModeEvent")
            # ----------------------------------------------------------------------------------------------------------
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
            if mode == StaticMonitorMode.KBD_LARGER_MATRIX:
                kbd_with_larger_matrix_mode_event = KeyboardWithLargerMatrixModeEvent.fromHexList(HexList(event))
                checker = StaticMonitorModeTestUtils.KeyboardWithLargerMatrixModeEventChecker
                check_map = checker.get_default_check_map(self)
                check_map.update(
                    {
                        "row_code": (checker.check_row_code, row_code),
                        "col_code": (checker.check_col_code, col_code),
                        "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.BREAK)
                    }
                )
                checker.check_fields(self, kbd_with_larger_matrix_mode_event, KeyboardWithLargerMatrixModeEvent,
                                     check_map)

            elif mode == StaticMonitorMode.ENHANCED_KBD_LARGER_MATRIX:
                enhanced_kbd_with_larger_matrix_mode_event = EnhancedKeyboardWithLargerMatrixModeEvent.fromHexList(
                    HexList(event))
                checker = StaticMonitorModeTestUtils.EnhancedKeyboardWithLargerMatrixModeEventChecker
                checker.check_fields(
                    self, enhanced_kbd_with_larger_matrix_mode_event, EnhancedKeyboardWithLargerMatrixModeEvent)
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_MONITOR_MODE_0)
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        self.testCaseChecked("FUN_18B0_0012", _AUTHOR)
    # end def test_kbd_set_monitor_mode_validate_parameter_mode_4_5

    @features("Feature18B0")
    @features("Mice")
    @level("Functionality")
    @services("OpticalSensor")
    def test_mouse_set_monitor_mode_validate_multiple_stimuli(self):
        """
        Test multiple stimuli at once (motion + roller + Key Pressed)

        [0] setMonitorMode(mode)
        """
        raise NotImplementedError("To be implemented when @services('OpticalSensor') is available")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with a mode: 2")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "UserAction: Set (x,y) - mouse movement")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "UserAction: Roller.ScrollUp")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "UserAction: KeyPress (left click)")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check MonitorModeEvent")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "UserAction: Roller.ScrollDown")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "UserAction: KeyRelease (left click)")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check MonitorModeEvent")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_MONITOR_MODE_0)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_18B0_0013", _AUTHOR)
    # end def test_mouse_set_monitor_mode_validate_multiple_stimuli

    @features("Feature18B0v1")
    @features("EnhancedKeyboardWithLargerMatrixMode")
    @level("Functionality")
    @services('SimultaneousKeystrokes')
    @bugtracker("StickyKeysInMonitorModeEvent")
    def test_kbd_set_monitor_mode_5_validate_multi_keys(self):
        """
        Test increasing and decreasing number of key pressed (up to 8 keys) (Enhanced KBD with large matrix)

        [0] setMonitorMode(mode)
        """
        mode_5 = StaticMonitorMode.ENHANCED_KBD_LARGER_MATRIX
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with a mode: 5")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode_5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Loop over Key ID list")
        # --------------------------------------------------------------------------------------------------------------
        key_list = []
        for key in self.button_stimuli_emulator.get_key_id_list():
            key_list.append(key)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Press 8 keys in the DUT")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Loop over first 8 keys in DUT")
        # --------------------------------------------------------------------------------------------------------------
        for key in key_list[:8]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(test_case=self,
                                                                                        check_first_message=False)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Get row and col code for keys")
        # --------------------------------------------------------------------------------------------------------------
        [[_, _], [row_code_1, col_code_1], [row_code_2, col_code_2], [row_code_3, col_code_3],
         [row_code_4, col_code_4], [row_code_5, col_code_5], [row_code_6, col_code_6], [row_code_7, col_code_7]] = \
            list(StaticMonitorModeTestUtils.get_kbd_row_col_code(test_case=self, key_id=x, combined=False)
                 for x in key_list[:8])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop all remaning keys in the DUT")
        # --------------------------------------------------------------------------------------------------------------
        key_to_be_released = key_list[0]
        for key in key_list[8:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "UserAction: KeyRelease (release 1st item in the press list) if PressCount > 8")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key_to_be_released.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key_to_be_released)
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
            enhanced_kbd_with_larger_matrix_mode_event = EnhancedKeyboardWithLargerMatrixModeEvent.fromHexList(
                HexList(event))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check MonitorModeEvent for 7 keys excluding the released key")
            # ----------------------------------------------------------------------------------------------------------
            checker = StaticMonitorModeTestUtils.EnhancedKeyboardWithLargerMatrixModeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "row_code_0": (checker.check_row_code_0, HexList(0xFF)),
                "col_code_0": (checker.check_col_code_0, HexList(0xFF)),
                "row_code_1": (checker.check_row_code_1, row_code_1),
                "col_code_1": (checker.check_col_code_1, col_code_1),
                "row_code_2": (checker.check_row_code_2, row_code_2),
                "col_code_2": (checker.check_col_code_2, col_code_2),
                "row_code_3": (checker.check_row_code_3, row_code_3),
                "col_code_3": (checker.check_col_code_3, col_code_3),
                "row_code_4": (checker.check_row_code_4, row_code_4),
                "col_code_4": (checker.check_col_code_4, col_code_4),
                "row_code_5": (checker.check_row_code_5, row_code_5),
                "col_code_5": (checker.check_col_code_5, col_code_5),
                "row_code_6": (checker.check_row_code_6, row_code_6),
                "col_code_6": (checker.check_col_code_6, col_code_6),
                "row_code_7": (checker.check_row_code_7, row_code_7),
                "col_code_7": (checker.check_col_code_7, col_code_7)
            })
            checker.check_fields(self, enhanced_kbd_with_larger_matrix_mode_event,
                                 EnhancedKeyboardWithLargerMatrixModeEvent, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "UserAction: KeyPress (add the item in the press list & increase PressCount)")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)
            key_to_be_released = key
            row_code_key, col_code_key = StaticMonitorModeTestUtils.get_kbd_row_col_code(test_case=self, key_id=key,
                                                                                         combined=False)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check MonitorModeEvent for number of keys in the press list")
            # ----------------------------------------------------------------------------------------------------------
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
            enhanced_kbd_with_larger_matrix_mode_event = EnhancedKeyboardWithLargerMatrixModeEvent.fromHexList(
                HexList(event))
            checker = StaticMonitorModeTestUtils.EnhancedKeyboardWithLargerMatrixModeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update(
                {
                    "row_code_0": (checker.check_row_code_0, row_code_key),
                    "col_code_0": (checker.check_col_code_0, col_code_key),
                    "row_code_1": (checker.check_row_code_1, row_code_1),
                    "col_code_1": (checker.check_col_code_1, col_code_1),
                    "row_code_2": (checker.check_row_code_2, row_code_2),
                    "col_code_2": (checker.check_col_code_2, col_code_2),
                    "row_code_3": (checker.check_row_code_3, row_code_3),
                    "col_code_3": (checker.check_col_code_3, col_code_3),
                    "row_code_4": (checker.check_row_code_4, row_code_4),
                    "col_code_4": (checker.check_col_code_4, col_code_4),
                    "row_code_5": (checker.check_row_code_5, row_code_5),
                    "col_code_5": (checker.check_col_code_5, col_code_5),
                    "row_code_6": (checker.check_row_code_6, row_code_6),
                    "col_code_6": (checker.check_col_code_6, col_code_6),
                    "row_code_7": (checker.check_row_code_7, row_code_7),
                    "col_code_7": (checker.check_col_code_7, col_code_7)
                }
            )
            checker.check_fields(self, enhanced_kbd_with_larger_matrix_mode_event,
                                 EnhancedKeyboardWithLargerMatrixModeEvent, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "UserAction: KeyRelease (all other keys pending)")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop all pending keys")
        # --------------------------------------------------------------------------------------------------------------
        for key in [key_to_be_released] + key_list[1:8]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key.name}")
            # ---------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(test_case=self,
                                                                                        check_first_message=False)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check MonitorModeEvent")
        # --------------------------------------------------------------------------------------------------------------
        enhanced_kbd_with_larger_matrix_mode_event = EnhancedKeyboardWithLargerMatrixModeEvent.fromHexList(
            HexList(event))
        checker = StaticMonitorModeTestUtils.EnhancedKeyboardWithLargerMatrixModeEventChecker
        checker.check_fields(self, enhanced_kbd_with_larger_matrix_mode_event,
                             EnhancedKeyboardWithLargerMatrixModeEvent)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_MONITOR_MODE_0)
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        self.testCaseChecked("FUN_18B0_0014", _AUTHOR)
    # end def test_kbd_set_monitor_mode_5_validate_multi_keys

    @features("Feature18B0v1")
    @features("EnhancedKeyboardWithLargerMatrixMode")
    @level("Functionality")
    def test_kbd_set_monitor_mode_5_by_row(self):
        """
        Test a key on all available row (Enhanced KBD with large matrix)

        [0] setMonitorMode(mode)
        """
        mode_5 = StaticMonitorMode.ENHANCED_KBD_LARGER_MATRIX
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with a mode: 5")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode_5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop in all rows (1..NO_OF_ROWS)")
        # --------------------------------------------------------------------------------------------------------------
        seen_rows = []
        for key in self.button_stimuli_emulator.get_key_id_list():
            row_code, col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(test_case=self, key_id=key,
                                                                                 combined=False)
            if row_code not in seen_rows:
                seen_rows.append(row_code)
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Press {key.name} in row {row_code}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_press(key)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check MonitorModeEvent")
                # ------------------------------------------------------------------------------------------------------
                event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self,
                                                                                            check_first_message=False)
                enhanced_kbd_with_larger_matrix_mode_event = EnhancedKeyboardWithLargerMatrixModeEvent.fromHexList(
                    HexList(event))
                checker = StaticMonitorModeTestUtils.EnhancedKeyboardWithLargerMatrixModeEventChecker
                check_map = checker.get_default_check_map(self)
                check_map.update(
                    {
                        "row_code_0": (checker.check_row_code_0, row_code),
                        "col_code_0": (checker.check_col_code_0, col_code)
                    }
                )
                checker.check_fields(
                    self, enhanced_kbd_with_larger_matrix_mode_event, EnhancedKeyboardWithLargerMatrixModeEvent,
                    check_map)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Release {key.name} in row {row_code}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_release(key)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check MonitorModeEvent")
                # ------------------------------------------------------------------------------------------------------
                event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self,
                                                                                            check_first_message=False)
                enhanced_kbd_with_larger_matrix_mode_event = EnhancedKeyboardWithLargerMatrixModeEvent.fromHexList(
                    HexList(event))
                checker = StaticMonitorModeTestUtils.EnhancedKeyboardWithLargerMatrixModeEventChecker
                checker.check_fields(
                    self, enhanced_kbd_with_larger_matrix_mode_event, EnhancedKeyboardWithLargerMatrixModeEvent)
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_MONITOR_MODE_0)
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        self.testCaseChecked("FUN_18B0_0015", _AUTHOR)
    # end def test_kbd_set_monitor_mode_5_by_row

    @features("Feature18B0")
    @features("EnhancedKeyboardWithLargerMatrixMode")
    @level("Functionality")
    def test_kbd_set_monitor_mode_5_by_column(self):
        """
        Test a key on all available column (Enhanced KBD with large matrix)

        [0] setMonitorMode(mode)
        """
        mode_5 = StaticMonitorMode.ENHANCED_KBD_LARGER_MATRIX
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with a mode: 5")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode_5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop in all columns (1..NO_OF_COLUMNS)")
        # --------------------------------------------------------------------------------------------------------------
        for key in self.button_stimuli_emulator.get_key_id_list():
            seen_colums = []
            row_code, col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(test_case=self, key_id=key,
                                                                                 combined=False)
            if col_code not in seen_colums:
                seen_colums.append(col_code)
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Press {key.name} in column {col_code}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_press(key)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check MonitorModeEvent")
                # ------------------------------------------------------------------------------------------------------
                event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self,
                                                                                            check_first_message=False)
                enhanced_kbd_with_larger_matrix_mode_event = EnhancedKeyboardWithLargerMatrixModeEvent.fromHexList(
                    HexList(event))
                checker = StaticMonitorModeTestUtils.EnhancedKeyboardWithLargerMatrixModeEventChecker
                check_map = checker.get_default_check_map(self)
                check_map.update(
                    {
                        "row_code_0": (checker.check_row_code_0, row_code),
                        "col_code_0": (checker.check_col_code_0, col_code)
                    }
                )
                checker.check_fields(
                    self, enhanced_kbd_with_larger_matrix_mode_event, EnhancedKeyboardWithLargerMatrixModeEvent,
                    check_map)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Release {key.name} in column {col_code}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_release(key)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check MonitorModeEvent")
                # ------------------------------------------------------------------------------------------------------
                event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self,
                                                                                            check_first_message=False)
                enhanced_kbd_with_larger_matrix_mode_event = EnhancedKeyboardWithLargerMatrixModeEvent.fromHexList(
                    HexList(event))
                checker = StaticMonitorModeTestUtils.EnhancedKeyboardWithLargerMatrixModeEventChecker
                checker.check_fields(
                    self, enhanced_kbd_with_larger_matrix_mode_event, EnhancedKeyboardWithLargerMatrixModeEvent)
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_MONITOR_MODE_0)
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        self.testCaseChecked("FUN_18B0_0016", _AUTHOR)
    # end def test_kbd_set_monitor_mode_5_by_column

    @features("Feature18B0")
    @features("KeyboardMode")
    @level("Functionality")
    def test_kbd_set_monitor_mode_1_limit(self):
        """
        Test every event parameter limits - 0x1 (KBD)

        [0] setMonitorMode(mode)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with a mode: 1")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.KBD_ON)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Loop over Key ID list")
        # --------------------------------------------------------------------------------------------------------------
        key_list = []
        for key in self.button_stimuli_emulator.get_key_id_list():
            key_list.append(key)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Loop")
        # --------------------------------------------------------------------------------------------------------------
        key_first = key_list[0]
        key_last = key_list[-1]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key_first.name} (first row, first col)")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_first)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check MonitorModeEvent (make)")
        # --------------------------------------------------------------------------------------------------------------
        key_first_row_col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(self, key_first)
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        keyboard_mode_event = KeyboardModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.KeyboardModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "row_col_code": (checker.check_row_col_code, key_first_row_col_code),
                "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.MAKE)
            }
        )
        checker.check_fields(self, keyboard_mode_event, KeyboardModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key_first.name} (first row, first col)")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_first)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check MonitorModeEvent (break)")
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        keyboard_mode_event = KeyboardModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.KeyboardModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "row_col_code": (checker.check_row_col_code, key_first_row_col_code),
                "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.BREAK)
            }
        )
        checker.check_fields(self, keyboard_mode_event, KeyboardModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key_last.name} (last row, last col)")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_last)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check MonitorModeEvent (make)")
        # --------------------------------------------------------------------------------------------------------------
        key_last_row_col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(self, key_last)
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        keyboard_mode_event = KeyboardModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.KeyboardModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "row_col_code": (checker.check_row_col_code, key_last_row_col_code),
                "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.MAKE)
            }
        )
        checker.check_fields(self, keyboard_mode_event, KeyboardModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key_last.name} (last row, last col)")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_last)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check MonitorModeEvent (break)")
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        keyboard_mode_event = KeyboardModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.KeyboardModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "row_col_code": (checker.check_row_col_code, key_last_row_col_code),
                "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.BREAK)
            }
        )
        checker.check_fields(self, keyboard_mode_event, KeyboardModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_MONITOR_MODE_0)
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        self.testCaseChecked("FUN_18B0_0017", _AUTHOR)
    # end def test_kbd_set_monitor_mode_1_limit

    @features("Feature18B0")
    @features("Mice")
    @level("Functionality")
    @services("OpticalSensor")
    def test_mouse_set_monitor_mode_2_limit(self):
        """
        Test every event parameter limits - 0x2 (Mouse)

        [0] setMonitorMode(mode)
        """
        raise NotImplementedError("To be implemented when @services('OpticalSensor') is available")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with a mode: 2")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "UserAction: Set X Value minimum -> xy_motion(dx=0x8001)")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "UserAction: Set Y Value minimum -> xy_motion(dy=0x8001)")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "UserAction: Set TiltLeftAndRight Analog Value minimum")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "UserAction: Set BackAndForward Analog Value minimum")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "UserAction: Set Roller Value minimum")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "UserAction: Set Time between ratchets minimum")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "User Action: Set Switches minimum")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check event sent by the DUT (all minimum values)")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "UserAction: Set X Value maximum -> xy_motion(dx=0x7FFF)")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "UserAction: Set Y Value maximum -> xy_motion(dy=0x7FFF)")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "UserAction: Set TiltLeftAndRight Analog Value maximum")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "UserAction: Set BackAndForward Analog Value maximum")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "UserAction: Set Roller Value maximum")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "UserAction: Set Time between ratchets maximum")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "User Action: Set Switches maximum")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check event sent by the DUT (all maximum values)")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_MONITOR_MODE_0)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_18B0_0018", _AUTHOR)
    # end def test_mouse_set_monitor_mode_2_limit

    @features("Feature18B0")
    @features("EnhancedKeyboardMode")
    @level("Functionality")
    @services('SimultaneousKeystrokes')
    def test_kbd_set_monitor_mode_3_limit(self):
        """
        Test every event parameter limits - 0x3 (Enhanced KBD)

        [0] setMonitorMode(mode)
        """
        mode_3 = StaticMonitorMode.ENHANCED_KBD_ON
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with a mode: 3")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Loop over Key ID list")
        # --------------------------------------------------------------------------------------------------------------
        key_list = []
        for key in self.button_stimuli_emulator.get_key_id_list():
            key_list.append(key)
        # end for
        first_8_keys = key_list[:8]
        last_8_keys = key_list[-8:]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "UserAction: Press the (first row, first 8 col) keys")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over the first 8 keys in row 0")
        # --------------------------------------------------------------------------------------------------------------
        for key in first_8_keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Get row col code for first 8 keys in row 0")
        # --------------------------------------------------------------------------------------------------------------
        [row_col_code_0, row_col_code_1, row_col_code_2, row_col_code_3, row_col_code_4, row_col_code_5,
         row_col_code_6, row_col_code_7] = list(StaticMonitorModeTestUtils.get_kbd_row_col_code(self, x)
                                                for x in first_8_keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the MonitorMode event sent by the DUT (Row Col Code 0..7)")
        # --------------------------------------------------------------------------------------------------------------
        enhanced_keyboard_mode_event = EnhancedKeyboardModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.EnhancedKeyboardModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "row_col_code_0": (checker.check_row_col_code_0, row_col_code_0),
                "row_col_code_1": (checker.check_row_col_code_1, row_col_code_1),
                "row_col_code_2": (checker.check_row_col_code_2, row_col_code_2),
                "row_col_code_3": (checker.check_row_col_code_3, row_col_code_3),
                "row_col_code_4": (checker.check_row_col_code_4, row_col_code_4),
                "row_col_code_5": (checker.check_row_col_code_5, row_col_code_5),
                "row_col_code_6": (checker.check_row_col_code_6, row_col_code_6),
                "row_col_code_7": (checker.check_row_col_code_7, row_col_code_7),
            }
        )
        checker.check_fields(self, enhanced_keyboard_mode_event, EnhancedKeyboardModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "UserAction: release the keys")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Loop over the first 8 keys in row 0")
        # --------------------------------------------------------------------------------------------------------------
        for key in first_8_keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the MonitorMode event sent by the DUT (FF)")
        # --------------------------------------------------------------------------------------------------------------
        enhanced_keyboard_mode_event = EnhancedKeyboardModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.EnhancedKeyboardModeEventChecker
        checker.check_fields(self, enhanced_keyboard_mode_event, EnhancedKeyboardModeEvent)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "UserAction: Press the (last row, last 8 col) key")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over the last 8 keys in row 0")
        # --------------------------------------------------------------------------------------------------------------
        for key in last_8_keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Get row col code for last 8 keys in row 0")
        # --------------------------------------------------------------------------------------------------------------
        [row_col_code_0, row_col_code_1, row_col_code_2, row_col_code_3, row_col_code_4, row_col_code_5,
         row_col_code_6, row_col_code_7] = list(StaticMonitorModeTestUtils.get_kbd_row_col_code(self, x)
                                                for x in last_8_keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the MonitorMode event sent by the DUT (Row Col Code 0..7)")
        # --------------------------------------------------------------------------------------------------------------
        enhanced_keyboard_mode_event = EnhancedKeyboardModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.EnhancedKeyboardModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "row_col_code_0": (checker.check_row_col_code_0, row_col_code_0),
                "row_col_code_1": (checker.check_row_col_code_1, row_col_code_1),
                "row_col_code_2": (checker.check_row_col_code_2, row_col_code_2),
                "row_col_code_3": (checker.check_row_col_code_3, row_col_code_3),
                "row_col_code_4": (checker.check_row_col_code_4, row_col_code_4),
                "row_col_code_5": (checker.check_row_col_code_5, row_col_code_5),
                "row_col_code_6": (checker.check_row_col_code_6, row_col_code_6),
                "row_col_code_7": (checker.check_row_col_code_7, row_col_code_7),
            }
        )
        checker.check_fields(self, enhanced_keyboard_mode_event, EnhancedKeyboardModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "UserAction: release the key")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over the last 8 keys in row 0")
        # --------------------------------------------------------------------------------------------------------------
        for key in last_8_keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the MonitorMode event sent by the DUT (FF)")
        # --------------------------------------------------------------------------------------------------------------
        enhanced_keyboard_mode_event = EnhancedKeyboardModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.EnhancedKeyboardModeEventChecker
        checker.check_fields(self, enhanced_keyboard_mode_event, EnhancedKeyboardModeEvent)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_MONITOR_MODE_0)
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        self.testCaseChecked("FUN_18B0_0019", _AUTHOR)
    # end def test_kbd_set_monitor_mode_3_limit

    @features("Feature18B0v1")
    @features("KeyboardWithLargerMatrixMode")
    @level("Functionality")
    def test_kbd_set_monitor_mode_4_limit(self):
        """
        Test every event parameter limits - 0x4 (KBD with large matrix)

        [0] setMonitorMode(mode)
        """
        mode_4 = StaticMonitorMode.KBD_LARGER_MATRIX
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with a mode: 4")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode_4)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Get first and last Key IDs")
        # --------------------------------------------------------------------------------------------------------------
        key_list = []
        for key in self.button_stimuli_emulator.get_key_id_list():
            key_list.append(key)
        # end for
        key_first = key_list[0]
        key_last = key_list[-1]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key_first.name} (first row, first col)")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_first)
        row_code, col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(test_case=self, key_id=key_first,
                                                                             combined=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the MonitorMode event sent by the DUT (Row Code, Col Code, Make)")
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        kbd_with_larger_matrix_mode_event = KeyboardWithLargerMatrixModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.KeyboardWithLargerMatrixModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "row_code": (checker.check_row_code, row_code),
                "col_code": (checker.check_col_code, col_code),
                "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.MAKE)
            }
        )
        checker.check_fields(self, kbd_with_larger_matrix_mode_event, KeyboardWithLargerMatrixModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key_first.name} (first row, first col)")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_first)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the MonitorMode event sent by the DUT (Row Code, Col Code, Break)")
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        kbd_with_larger_matrix_mode_event = KeyboardWithLargerMatrixModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.KeyboardWithLargerMatrixModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "row_code": (checker.check_row_code, row_code),
                "col_code": (checker.check_col_code, col_code),
                "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.BREAK)
            }
        )
        checker.check_fields(self, kbd_with_larger_matrix_mode_event, KeyboardWithLargerMatrixModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key_last.name} (last row, last col)")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_last)
        row_code, col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(test_case=self, key_id=key_last,
                                                                             combined=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the MonitorMode event sent by the DUT (Row Code, Col Code, Make)")
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        kbd_with_larger_matrix_mode_event = KeyboardWithLargerMatrixModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.KeyboardWithLargerMatrixModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "row_code": (checker.check_row_code, row_code),
                "col_code": (checker.check_col_code, col_code),
                "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.MAKE)
            }
        )
        checker.check_fields(self, kbd_with_larger_matrix_mode_event, KeyboardWithLargerMatrixModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key_last.name} (last row, last col)")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_last)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the MonitorMode event sent by the DUT (Row Code, Col Code, Break)")
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        kbd_with_larger_matrix_mode_event = KeyboardWithLargerMatrixModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.KeyboardWithLargerMatrixModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "row_code": (checker.check_row_code, row_code),
                "col_code": (checker.check_col_code, col_code),
                "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.BREAK)
            }
        )
        checker.check_fields(self, kbd_with_larger_matrix_mode_event, KeyboardWithLargerMatrixModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_MONITOR_MODE_0)
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        self.testCaseChecked("FUN_18B0_0020", _AUTHOR)
    # end def test_kbd_set_monitor_mode_4_limit

    @features("Feature18B0v1")
    @features("EnhancedKeyboardWithLargerMatrixMode")
    @level("Functionality")
    @services('SimultaneousKeystrokes')
    @bugtracker("StickyKeysInMonitorModeEvent")
    def test_kbd_set_monitor_mode_5_limit(self):
        """
        Test every event parameter limits - 0x5 (Enhanced KBD with large matrix)

        [0] setMonitorMode(mode)
        """
        mode_5 = StaticMonitorMode.ENHANCED_KBD_LARGER_MATRIX
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with a mode: 5")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode_5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Get first 8 and last 8 keys")
        # --------------------------------------------------------------------------------------------------------------
        key_list = []
        for key in self.button_stimuli_emulator.get_key_id_list():
            key_list.append(key)
        # end for
        first_8_keys = key_list[:8]
        last_8_keys = key_list[-8:]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "UserAction: Press the (first row, first 8 col) keys")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over the first 8 keys in row 0")
        # --------------------------------------------------------------------------------------------------------------
        for key in first_8_keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Get row and col code for keys")
        # --------------------------------------------------------------------------------------------------------------
        [[row_code_0, col_code_0], [row_code_1, col_code_1], [row_code_2, col_code_2], [row_code_3, col_code_3],
         [row_code_4, col_code_4], [row_code_5, col_code_5], [row_code_6, col_code_6], [row_code_7, col_code_7]] = \
            list(StaticMonitorModeTestUtils.get_kbd_row_col_code(test_case=self,
                                                                 key_id=x, combined=False) for x in first_8_keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the MonitorMode event sent by the DUT (Row Code 0..7, Col Code 0..7)")
        # --------------------------------------------------------------------------------------------------------------
        enhanced_kbd_with_larger_matrix_mode_event = EnhancedKeyboardWithLargerMatrixModeEvent.fromHexList(
            HexList(event))
        checker = StaticMonitorModeTestUtils.EnhancedKeyboardWithLargerMatrixModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "row_code_0": (checker.check_row_code_0, row_code_0),
                "col_code_0": (checker.check_col_code_0, col_code_0),
                "row_code_1": (checker.check_row_code_1, row_code_1),
                "col_code_1": (checker.check_col_code_1, col_code_1),
                "row_code_2": (checker.check_row_code_2, row_code_2),
                "col_code_2": (checker.check_col_code_2, col_code_2),
                "row_code_3": (checker.check_row_code_3, row_code_3),
                "col_code_3": (checker.check_col_code_3, col_code_3),
                "row_code_4": (checker.check_row_code_4, row_code_4),
                "col_code_4": (checker.check_col_code_4, col_code_4),
                "row_code_5": (checker.check_row_code_5, row_code_5),
                "col_code_5": (checker.check_col_code_5, col_code_5),
                "row_code_6": (checker.check_row_code_6, row_code_6),
                "col_code_6": (checker.check_col_code_6, col_code_6),
                "row_code_7": (checker.check_row_code_7, row_code_7),
                "col_code_7": (checker.check_col_code_7, col_code_7)
            }
        )
        checker.check_fields(self, enhanced_kbd_with_larger_matrix_mode_event, EnhancedKeyboardWithLargerMatrixModeEvent
                             , check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "UserAction: release the keys")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over the first 8 keys in row 0")
        # --------------------------------------------------------------------------------------------------------------
        for key in first_8_keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the MonitorMode event sent by the DUT (FF)")
        # --------------------------------------------------------------------------------------------------------------
        enhanced_kbd_with_larger_matrix_mode_event = EnhancedKeyboardWithLargerMatrixModeEvent.fromHexList(
            HexList(event))
        checker = StaticMonitorModeTestUtils.EnhancedKeyboardWithLargerMatrixModeEventChecker
        checker.check_fields(self, enhanced_kbd_with_larger_matrix_mode_event,
                             EnhancedKeyboardWithLargerMatrixModeEvent)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "UserAction: Press the (last row, last 8 col) key")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over the last 8 keys in row 0")
        # --------------------------------------------------------------------------------------------------------------
        for key in last_8_keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name} key")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Get row and col code for keys")
        # --------------------------------------------------------------------------------------------------------------
        [[row_code_0, col_code_0], [row_code_1, col_code_1], [row_code_2, col_code_2], [row_code_3, col_code_3],
         [row_code_4, col_code_4], [row_code_5, col_code_5], [row_code_6, col_code_6], [row_code_7, col_code_7]] = \
            list(StaticMonitorModeTestUtils.get_kbd_row_col_code(test_case=self, key_id=x, combined=False)
                 for x in last_8_keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the MonitorMode event sent by the DUT (Row Code 0..7, Col Code 0..7)")
        # --------------------------------------------------------------------------------------------------------------
        enhanced_kbd_with_larger_matrix_mode_event = EnhancedKeyboardWithLargerMatrixModeEvent.fromHexList(
            HexList(event))
        checker = StaticMonitorModeTestUtils.EnhancedKeyboardWithLargerMatrixModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "row_code_0": (checker.check_row_code_0, row_code_0),
            "col_code_0": (checker.check_col_code_0, col_code_0),
            "row_code_1": (checker.check_row_code_1, row_code_1),
            "col_code_1": (checker.check_col_code_1, col_code_1),
            "row_code_2": (checker.check_row_code_2, row_code_2),
            "col_code_2": (checker.check_col_code_2, col_code_2),
            "row_code_3": (checker.check_row_code_3, row_code_3),
            "col_code_3": (checker.check_col_code_3, col_code_3),
            "row_code_4": (checker.check_row_code_4, row_code_4),
            "col_code_4": (checker.check_col_code_4, col_code_4),
            "row_code_5": (checker.check_row_code_5, row_code_5),
            "col_code_5": (checker.check_col_code_5, col_code_5),
            "row_code_6": (checker.check_row_code_6, row_code_6),
            "col_code_6": (checker.check_col_code_6, col_code_6),
            "row_code_7": (checker.check_row_code_7, row_code_7),
            "col_code_7": (checker.check_col_code_7, col_code_7)
        })
        checker.check_fields(self, enhanced_kbd_with_larger_matrix_mode_event, EnhancedKeyboardWithLargerMatrixModeEvent
                             , check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "UserAction: release the keys")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Loop over the last 8 keys in row 0")
        # --------------------------------------------------------------------------------------------------------------
        for key in last_8_keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key.name} key")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the MonitorMode event sent by the DUT (FF)")
        # --------------------------------------------------------------------------------------------------------------
        enhanced_kbd_with_larger_matrix_mode_event = EnhancedKeyboardWithLargerMatrixModeEvent.fromHexList(
            HexList(event))
        checker = StaticMonitorModeTestUtils.EnhancedKeyboardWithLargerMatrixModeEventChecker
        checker.check_fields(self, enhanced_kbd_with_larger_matrix_mode_event,
                             EnhancedKeyboardWithLargerMatrixModeEvent)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_MONITOR_MODE_0)
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        self.testCaseChecked("FUN_18B0_0021", _AUTHOR)
    # end def test_kbd_set_monitor_mode_5_limit
# end class StaticMonitorModeFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
