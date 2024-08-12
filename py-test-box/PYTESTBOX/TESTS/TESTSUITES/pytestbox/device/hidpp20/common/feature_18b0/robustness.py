#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.common.feature_18b0.robustness
:brief: HID++ 2.0 ``StaticMonitorMode`` robustness test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/12/19
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import warnings

from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddata import HidData
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.staticmonitormode import EnhancedKeyboardModeEvent
from pyhid.hidpp.features.common.staticmonitormode import EnhancedKeyboardWithLargerMatrixModeEvent
from pyhid.hidpp.features.common.staticmonitormode import KeyboardModeEvent
from pyhid.hidpp.features.common.staticmonitormode import KeyboardWithLargerMatrixModeEvent
from pyhid.hidpp.features.common.staticmonitormode import MouseModeEvent
from pyhid.hidpp.features.common.staticmonitormode import StaticMonitorMode
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pyraspi.services.kosmos.config.buttonlayout import BUTTON_LAYOUT_BY_ID
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.base.staticmonitormodeutils import StaticMonitorModeTestUtils
from pytestbox.device.hid.keyboard.keycode.keycode import KeyCodeTestCase
from pytestbox.device.hidpp20.common.feature_18b0.staticmonitormode import StaticMonitorModeTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"
_CHECK_MONITORMODE_RESPONSE = "Check Monitor Mode response fields"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class StaticMonitorModeRobustnessTestCase(StaticMonitorModeTestCase):
    """
    Validate ``StaticMonitorMode`` robustness test cases
    """

    @features("Feature18B0")
    @level("Robustness")
    def test_set_monitor_mode_software_id(self):
        """
        Validate ``SetMonitorMode`` software id field is ignored by the firmware

        [0] setMonitorMode(mode) -> mode

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.Mode.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        mode = StaticMonitorMode.OFF
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(StaticMonitorMode.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetMonitorMode request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(test_case=self, mode=mode,
                                                                               software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetMonitorModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
            checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_18B0_0001#1", _AUTHOR)
    # end def test_set_monitor_mode_software_id

    @features("Feature18B0")
    @level("Robustness")
    def test_set_monitor_mode_padding(self):
        """
        Validate ``SetMonitorMode`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.Mode.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        mode = StaticMonitorMode.OFF
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_18b0.set_monitor_mode_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetMonitorMode request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(test_case=self, mode=mode,
                                                                               padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetMonitorModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
            checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_18B0_0002#1", _AUTHOR)
    # end def test_set_monitor_mode_padding

    @features("Feature18B0")
    @features("KeyboardMode")
    @level("Robustness")
    @services('SimultaneousKeystrokes')
    @bugtracker('MonitorMode_BadRowColValues')
    def test_kbd_set_monitor_mode_1(self):
        """
        Validate pressing 2 keys at once and release one

        [0] setMonitorMode(mode)
        """
        event = None
        mode_1 = StaticMonitorMode.KBD_ON
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with mode: 1")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetMonitorModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "UserAction: Press 2 keys at once")
        # --------------------------------------------------------------------------------------------------------------
        keys = KeyMatrixTestUtils.get_key_list(test_case=self, group_count=1, group_size=2, random=True)[0]
        row_col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(self, keys[1])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Loop over keys")
        # --------------------------------------------------------------------------------------------------------------
        for key in keys:
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
        LogHelper.log_check(self, "Check key pressed second is reported in MonitorModeBroadcastEvent")
        # --------------------------------------------------------------------------------------------------------------
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

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release the second pressed key {keys[1].name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(keys[1])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check key released reported in MonitorModeBroadcastEvent")
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
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

        self.testCaseChecked("ROB_18B0_0003", _AUTHOR)
    # end def test_kbd_set_monitor_mode_1

    @features("Feature18B0")
    @features("EnhancedKeyboardMode")
    @level("Robustness")
    @services('SimultaneousKeystrokes')
    @bugtracker('MonitorMode_BadRowColValues')
    def test_kbd_set_monitor_mode_3(self):
        """
        Validate pressing more than 8 keys at once and release one then press another (Enhanced KBD)

        [0] setMonitorMode(mode)
        """
        event = None
        mode_3 = StaticMonitorMode.ENHANCED_KBD_ON
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with mode: 3")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetMonitorModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "UserAction: Press 9 keys at once")
        # --------------------------------------------------------------------------------------------------------------
        test_key_list = []
        if self.f.PRODUCT.DEVICE.F_KeyboardType == "membrane":
            test_key_list = StaticMonitorModeTestUtils.get_non_ghosted_keys(self, 9)
        else:
            for key in self.button_stimuli_emulator.get_key_id_list():
                test_key_list.append(key)
                if len(test_key_list) == 9:
                    break
                # end if
            # end for
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Loop over key list")
        # --------------------------------------------------------------------------------------------------------------
        for key in test_key_list:
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
        LogHelper.log_info(self, "Get row col code for test keys")
        # --------------------------------------------------------------------------------------------------------------
        [row_col_code_0, row_col_code_1, row_col_code_2, row_col_code_3, row_col_code_4, row_col_code_5,
         row_col_code_6, row_col_code_7, row_col_code_8] = \
            list(StaticMonitorModeTestUtils.get_kbd_row_col_code(self, x) for x in test_key_list)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check 8 keys are reported in the event, 9'th key is filtered")
        # --------------------------------------------------------------------------------------------------------------
        enhanced_kbd_mode_event = EnhancedKeyboardModeEvent.fromHexList(HexList(event))
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
        checker.check_fields(self, enhanced_kbd_mode_event, EnhancedKeyboardModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"UserAction: Release the first reported key {test_key_list[0].name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(test_key_list[0])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check event is triggered without the first key {test_key_list[0].name}")
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        enhanced_kbd_mode_event = EnhancedKeyboardModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.EnhancedKeyboardModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "row_col_code_0": (checker.check_row_col_code_0, HexList(0xFF)),
                "row_col_code_1": (checker.check_row_col_code_1, row_col_code_1),
                "row_col_code_2": (checker.check_row_col_code_2, row_col_code_2),
                "row_col_code_3": (checker.check_row_col_code_3, row_col_code_3),
                "row_col_code_4": (checker.check_row_col_code_4, row_col_code_4),
                "row_col_code_5": (checker.check_row_col_code_5, row_col_code_5),
                "row_col_code_6": (checker.check_row_col_code_6, row_col_code_6),
                "row_col_code_7": (checker.check_row_col_code_7, row_col_code_7),
            }
        )
        checker.check_fields(self, enhanced_kbd_mode_event, EnhancedKeyboardModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Re-Press the 9'th key {test_key_list[8].name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(test_key_list[8])
        _ = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        self.button_stimuli_emulator.key_press(test_key_list[8])
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        enhanced_kbd_mode_event = EnhancedKeyboardModeEvent.fromHexList(HexList(event))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the missing key {test_key_list[8].name} is now included in the report, "
                                  f"{test_key_list[0].name} is released")
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.EnhancedKeyboardModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "row_col_code_0": (checker.check_row_col_code_0, row_col_code_8),
                "row_col_code_1": (checker.check_row_col_code_1, row_col_code_1),
                "row_col_code_2": (checker.check_row_col_code_2, row_col_code_2),
                "row_col_code_3": (checker.check_row_col_code_3, row_col_code_3),
                "row_col_code_4": (checker.check_row_col_code_4, row_col_code_4),
                "row_col_code_5": (checker.check_row_col_code_5, row_col_code_5),
                "row_col_code_6": (checker.check_row_col_code_6, row_col_code_6),
                "row_col_code_7": (checker.check_row_col_code_7, row_col_code_7),
            }
        )
        checker.check_fields(self, enhanced_kbd_mode_event, EnhancedKeyboardModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Re-press the released key {test_key_list[0].name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(test_key_list[0])
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check event is triggered without key {test_key_list[0].name} "
                                  f"but includes all other 8 keys")
        # --------------------------------------------------------------------------------------------------------------
        enhanced_kbd_mode_event = EnhancedKeyboardModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.EnhancedKeyboardModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "row_col_code_0": (checker.check_row_col_code_0, row_col_code_8),
                "row_col_code_1": (checker.check_row_col_code_1, row_col_code_1),
                "row_col_code_2": (checker.check_row_col_code_2, row_col_code_2),
                "row_col_code_3": (checker.check_row_col_code_3, row_col_code_3),
                "row_col_code_4": (checker.check_row_col_code_4, row_col_code_4),
                "row_col_code_5": (checker.check_row_col_code_5, row_col_code_5),
                "row_col_code_6": (checker.check_row_col_code_6, row_col_code_6),
                "row_col_code_7": (checker.check_row_col_code_7, row_col_code_7),
            }
        )
        checker.check_fields(self, enhanced_kbd_mode_event, EnhancedKeyboardModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "UserAction: Release all keys")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Loop over keys")
        # --------------------------------------------------------------------------------------------------------------
        for key in test_key_list:
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
        LogHelper.log_check(self, "Check event has FF for all keys released")
        # --------------------------------------------------------------------------------------------------------------
        enhanced_kbd_mode_event = EnhancedKeyboardModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.EnhancedKeyboardModeEventChecker
        checker.check_fields(self, enhanced_kbd_mode_event, EnhancedKeyboardModeEvent)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with mode: 0 (OFF)")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetMonitorModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        self.testCaseChecked("ROB_18B0_0004", _AUTHOR)
    # end def test_kbd_set_monitor_mode_3

    @features("Feature18B0v1")
    @features("KeyboardWithLargerMatrixMode")
    @level("Robustness")
    @services('SimultaneousKeystrokes')
    @bugtracker('MonitorMode_BadRowColValues')
    def test_kbd_set_monitor_mode_4(self):
        """
        Validate pressing 2 keys at once and release one

        [0] setMonitorMode(mode)
        """
        event = None
        mode_4 = StaticMonitorMode.KBD_LARGER_MATRIX
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with mode: 4")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode_4)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetMonitorModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press 2 keys at once")
        # --------------------------------------------------------------------------------------------------------------
        keys = KeyMatrixTestUtils.get_key_list(test_case=self, group_count=1, group_size=2, random=True)[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Loop over keys")
        # --------------------------------------------------------------------------------------------------------------
        for key in keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Loop")
        # --------------------------------------------------------------------------------------------------------------
        row_code, col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(test_case=self, key_id=keys[1],
                                                                             combined=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check key pressed second is reported in the event")
        # --------------------------------------------------------------------------------------------------------------
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
        LogHelper.log_step(self, f"Release the second pressed key {keys[1].name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=keys[1])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check key released second is reported in the event")
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

        self.testCaseChecked("ROB_18B0_0005", _AUTHOR)
    # end def test_kbd_set_monitor_mode_4

    @features("Feature18B0v1")
    @features("EnhancedKeyboardWithLargerMatrixMode")
    @level("Robustness")
    @services('SimultaneousKeystrokes')
    @bugtracker('MonitorMode_BadRowColValues')
    def test_kbd_set_monitor_mode_5(self):
        """
        Validate pressing more than 8 keys at once and release one then press another (Enhanced KBD with large matrix)

        [0] setMonitorMode(mode)
        """
        event = None
        mode_5 = StaticMonitorMode.ENHANCED_KBD_LARGER_MATRIX
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Get Test Keys list with 9 keys")
        # --------------------------------------------------------------------------------------------------------------
        test_key_list = []
        if self.f.PRODUCT.DEVICE.F_KeyboardType == "membrane":
            test_key_list = StaticMonitorModeTestUtils.get_non_ghosted_keys(self, 9)
        else:
            for key in self.button_stimuli_emulator.get_key_id_list():
                test_key_list.append(key)
                if len(test_key_list) == 9:
                    break
                # end if
            # end for
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with mode: 5")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode_5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetMonitorModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "UserAction: Press 9 keys at once")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Loop over keys")
        # --------------------------------------------------------------------------------------------------------------
        for key in test_key_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(test_case=self,
                                                                                        check_first_message=False,
                                                                                        allow_no_message=True)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Get row and col code for keys")
        # --------------------------------------------------------------------------------------------------------------
        [[row_code_0, col_code_0], [row_code_1, col_code_1], [row_code_2, col_code_2], [row_code_3, col_code_3],
         [row_code_4, col_code_4], [row_code_5, col_code_5], [row_code_6, col_code_6], [row_code_7, col_code_7],
         [row_code_8, col_code_8]] = list(StaticMonitorModeTestUtils.get_kbd_row_col_code(
            test_case=self, combined=False, key_id=x) for x in test_key_list)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check 8 keys are reported in the event")
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
        checker.check_fields(
            self, enhanced_kbd_with_larger_matrix_mode_event, EnhancedKeyboardWithLargerMatrixModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Release the first reported key {test_key_list[0].name} "
                                 f"and 9'th pressed key {test_key_list[8].name}")
        # --------------------------------------------------------------------------------------------------------------
        for key in [test_key_list[0], test_key_list[8]]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key.name} key")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key_id=key)
            _ = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False,
                                                                                    allow_no_message=True)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Re-press 9'th key {test_key_list[8].name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(test_key_list[8])
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        enhanced_kbd_with_larger_matrix_mode_event = EnhancedKeyboardWithLargerMatrixModeEvent.fromHexList(
            HexList(event))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the missing key {test_key_list[8].name} is now included in the report")
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.EnhancedKeyboardWithLargerMatrixModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "row_code_0": (checker.check_row_code_0, row_code_8),
                "col_code_0": (checker.check_col_code_0, col_code_8),
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
        checker.check_fields(
            self, enhanced_kbd_with_larger_matrix_mode_event, EnhancedKeyboardWithLargerMatrixModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Re-press the released key {test_key_list[0].name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(test_key_list[0])
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False,
                                                                                    allow_no_message=True)
        enhanced_kbd_with_larger_matrix_mode_event = EnhancedKeyboardWithLargerMatrixModeEvent.fromHexList(HexList(
            event))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check event is triggered without key{test_key_list[0].name} "
                                  f"but includes all other 8 keys")
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.EnhancedKeyboardWithLargerMatrixModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "row_code_0": (checker.check_row_code_0, row_code_8),
                "col_code_0": (checker.check_col_code_0, col_code_8),
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
        checker.check_fields(
            self, enhanced_kbd_with_larger_matrix_mode_event, EnhancedKeyboardWithLargerMatrixModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "UserAction: Release all keys")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Loop over keys")
        # --------------------------------------------------------------------------------------------------------------
        for key in test_key_list[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(test_case=self,
                                                                                        check_first_message=False)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check event has FF for all keys released")
        # --------------------------------------------------------------------------------------------------------------
        enhanced_kbd_with_larger_matrix_mode_event = EnhancedKeyboardWithLargerMatrixModeEvent.fromHexList(
            HexList(event))
        checker = StaticMonitorModeTestUtils.EnhancedKeyboardWithLargerMatrixModeEventChecker
        checker.check_fields(self, enhanced_kbd_with_larger_matrix_mode_event,
                             EnhancedKeyboardWithLargerMatrixModeEvent)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with mode: 0 (OFF)")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetMonitorModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        self.testCaseChecked("ROB_18B0_0006", _AUTHOR)
    # end def test_kbd_set_monitor_mode_5

    @features("Feature18B0")
    @features("KeyboardMode")
    @level("Robustness")
    @bugtracker('MonitorMode_BadRowColValues')
    def test_kbd_set_monitor_mode_1_in_between_press_and_release(self):
        """
        Validate SetMonitorMode in between press and release (KBD)

        [0] setMonitorMode(mode)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over 5 randomly selected keys")
        # --------------------------------------------------------------------------------------------------------------
        keys = KeyMatrixTestUtils.get_key_list(self, group_count=KeyCodeTestCase.NUMBER_OF_KEYS, random=True)
        for (key,) in keys:
            ChannelUtils.empty_queues(self)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID Report is ON")
            # ----------------------------------------------------------------------------------------------------------
            if key in HidData.KEY_ID_TO_HID_MAP:
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key, MAKE))
            else:
                warnings.warn(f"{key.name} not in KEY_ID_TO_HID_MAP, skipped checking HID report")
                ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Event is OFF")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self,
                                           timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                           class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                           queue_name=HIDDispatcher.QueueName.EVENT)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set Monitor Mode = 0x1")
            # ----------------------------------------------------------------------------------------------------------
            StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.KBD_ON)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID Report is OFF")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self,
                                           timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                           queue_name=HIDDispatcher.QueueName.HID)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Event is ON")
            # ----------------------------------------------------------------------------------------------------------
            row_col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(self, key)
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
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

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID Report is OFF")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self,
                                           timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                           queue_name=HIDDispatcher.QueueName.HID)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Event is ON")
            # ----------------------------------------------------------------------------------------------------------
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
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
            LogHelper.log_step(self, "Set Monitor Mode = 0x0")
            # ----------------------------------------------------------------------------------------------------------
            StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.OFF)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID Report is ON")
            # ----------------------------------------------------------------------------------------------------------
            if key in HidData.KEY_ID_TO_HID_MAP:
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key, BREAK))
            else:
                warnings.warn(f"{key.name} not in KEY_ID_TO_HID_MAP, skipped checking HID report")
                ChannelUtils.empty_queue(self, HIDDispatcher.QueueName.HID)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Event is OFF")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self,
                                           timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                           class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                           queue_name=HIDDispatcher.QueueName.EVENT)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End test loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_18B0_0007", _AUTHOR)
    # end def test_kbd_set_monitor_mode_1_in_between_press_and_release

    @features("Feature18B0")
    @features("Mice")
    @level("Robustness")
    def test_mouse_set_monitor_mode_2_in_between_press_and_release(self):
        """
        Validate SetMonitorMode in between press and release (Mouse)

        [0] setMonitorMode(mode)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over all the keys in the DUT")
        # --------------------------------------------------------------------------------------------------------------
        for button in BUTTON_LAYOUT_BY_ID[self.f.PRODUCT.F_ProductReference].KEYS.keys():
            ChannelUtils.empty_queues(self)
            switch = HexList("00" * MouseModeEvent.LEN.SWITCHES // 8)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {button.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(button)
            switch = StaticMonitorModeTestUtils.update_switch(switch, button, set_bit=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID Report is ON")
            # ----------------------------------------------------------------------------------------------------------
            warnings.warn("To be implemented when spurious motion algo branch is merged")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Event is OFF")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self,
                                           timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                           class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                           queue_name=HIDDispatcher.QueueName.EVENT)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set Monitor Mode = 0x2")
            # ----------------------------------------------------------------------------------------------------------
            StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.MOUSE_ON)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {button.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(button)
            switch = StaticMonitorModeTestUtils.update_switch(switch, button, clear_bit=False)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID Report is OFF")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self,
                                           timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                           queue_name=HIDDispatcher.QueueName.HID)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Event is ON")
            # ----------------------------------------------------------------------------------------------------------
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
            mouse_mode_event = MouseModeEvent.fromHexList(HexList(event))
            checker = StaticMonitorModeTestUtils.MouseModeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({"switches": (checker.check_switches, switch)})
            checker.check_fields(self, mouse_mode_event, MouseModeEvent, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {button.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(button)
            switch = StaticMonitorModeTestUtils.update_switch(switch, button, set_bit=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID Report is OFF")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self,
                                           timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                           queue_name=HIDDispatcher.QueueName.HID)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Event is ON")
            # ----------------------------------------------------------------------------------------------------------
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
            mouse_mode_event = MouseModeEvent.fromHexList(HexList(event))
            checker = StaticMonitorModeTestUtils.MouseModeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({"switches": (checker.check_switches, switch)})
            checker.check_fields(self, mouse_mode_event, MouseModeEvent, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set Monitor Mode = 0x0")
            # ----------------------------------------------------------------------------------------------------------
            StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.OFF)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {button.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(button)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID Report is ON")
            # ----------------------------------------------------------------------------------------------------------
            warnings.warn("To be implemented when spurious motion algo branch is merged")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Event is OFF")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self,
                                           timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                           class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                           queue_name=HIDDispatcher.QueueName.EVENT)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End test loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_18B0_0008", _AUTHOR)
    # end def test_mouse_set_monitor_mode_2_in_between_press_and_release

    @features("Feature18B0")
    @features("EnhancedKeyboardMode")
    @level("Robustness")
    @bugtracker('MonitorMode_BadRowColValues')
    def test_kbd_set_monitor_mode_3_in_between_press_and_release(self):
        """
        Validate SetMonitorMode in between press and release (Enhanced KBD)

        [0] setMonitorMode(mode)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over 5 randomly selected keys")
        # --------------------------------------------------------------------------------------------------------------
        keys = KeyMatrixTestUtils.get_key_list(self, group_count=KeyCodeTestCase.NUMBER_OF_KEYS, random=True)
        for (key,) in keys:
            ChannelUtils.empty_queues(self)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID Report is ON")
            # ----------------------------------------------------------------------------------------------------------
            if key in HidData.KEY_ID_TO_HID_MAP:
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key, MAKE))
            else:
                warnings.warn(f"{key.name} not in KEY_ID_TO_HID_MAP, skipped checking HID report")
                ChannelUtils.empty_queue(self, HIDDispatcher.QueueName.HID)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Event is OFF")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self,
                                           timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                           class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                           queue_name=HIDDispatcher.QueueName.EVENT)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set Monitor Mode = 0x3")
            # ----------------------------------------------------------------------------------------------------------
            StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.ENHANCED_KBD_ON)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID Report is OFF")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self,
                                           timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                           queue_name=HIDDispatcher.QueueName.HID)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Event is ON")
            # ----------------------------------------------------------------------------------------------------------
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
            enhanced_keyboard_mode_event = EnhancedKeyboardModeEvent.fromHexList(HexList(event))
            checker = StaticMonitorModeTestUtils.EnhancedKeyboardModeEventChecker
            checker.check_fields(self, enhanced_keyboard_mode_event, EnhancedKeyboardModeEvent)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID Report is OFF")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self,
                                           timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                           queue_name=HIDDispatcher.QueueName.HID)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Event is ON")
            # ----------------------------------------------------------------------------------------------------------
            row_col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(self, key)
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
            enhanced_keyboard_mode_event = EnhancedKeyboardModeEvent.fromHexList(HexList(event))
            checker = StaticMonitorModeTestUtils.EnhancedKeyboardModeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({"row_col_code_0": (checker.check_row_col_code_0, row_col_code)})
            checker.check_fields(self, enhanced_keyboard_mode_event, EnhancedKeyboardModeEvent, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set Monitor Mode = 0x0")
            # ----------------------------------------------------------------------------------------------------------
            StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.OFF)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID Report is ON")
            # ----------------------------------------------------------------------------------------------------------
            if key in HidData.KEY_ID_TO_HID_MAP:
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key, BREAK))
            else:
                warnings.warn(f"{key.name} not in KEY_ID_TO_HID_MAP, skipped checking HID report")
                ChannelUtils.empty_queue(self, HIDDispatcher.QueueName.HID)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Event is OFF")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self,
                                           timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                           class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                           queue_name=HIDDispatcher.QueueName.EVENT)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End test loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_18B0_0009", _AUTHOR)
    # end def test_kbd_set_monitor_mode_3_in_between_press_and_release

    @features("Feature18B0v1")
    @features("KeyboardWithLargerMatrixMode")
    @level("Robustness")
    @bugtracker('MonitorMode_BadRowColValues')
    def test_kbd_set_monitor_mode_4_in_between_press_and_release(self):
        """
        Validate SetMonitorMode in between press and release (KBD with large matrix)

        [0] setMonitorMode(mode)
        """
        mode_4 = StaticMonitorMode.KBD_LARGER_MATRIX
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over 5 randomly selected keys")
        # --------------------------------------------------------------------------------------------------------------
        keys = KeyMatrixTestUtils.get_key_list(self, group_count=KeyCodeTestCase.NUMBER_OF_KEYS, random=True)
        for (key,) in keys:
            ChannelUtils.empty_queues(self)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID Report is ON")
            # ----------------------------------------------------------------------------------------------------------
            if key in HidData.KEY_ID_TO_HID_MAP:
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key, MAKE))
            else:
                warnings.warn(f"{key.name} not in KEY_ID_TO_HID_MAP, skipped checking HID report")
                ChannelUtils.empty_queue(self, HIDDispatcher.QueueName.HID)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Event is OFF")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self,
                                           timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                           class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                           queue_name=HIDDispatcher.QueueName.EVENT)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set Monitor Mode = 0x4")
            # ----------------------------------------------------------------------------------------------------------
            response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode_4)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _CHECK_MONITORMODE_RESPONSE)
            # ----------------------------------------------------------------------------------------------------------
            checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
            checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID Report is OFF")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self,
                                           timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                           queue_name=HIDDispatcher.QueueName.HID)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Event is ON")
            # ----------------------------------------------------------------------------------------------------------
            row_code, col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(test_case=self, key_id=key,
                                                                                 combined=False)
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

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID Report is OFF")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self,
                                           timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                           queue_name=HIDDispatcher.QueueName.HID)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Event is ON")
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
            LogHelper.log_step(self, "Set Monitor Mode = 0x0")
            # ----------------------------------------------------------------------------------------------------------
            response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.OFF)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _CHECK_MONITORMODE_RESPONSE)
            # ----------------------------------------------------------------------------------------------------------
            checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
            checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID Report is ON")
            # ----------------------------------------------------------------------------------------------------------
            if key in HidData.KEY_ID_TO_HID_MAP:
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key, BREAK))
            else:
                warnings.warn(f"{key.name} not in KEY_ID_TO_HID_MAP, skipped checking HID report")
                ChannelUtils.empty_queue(self, HIDDispatcher.QueueName.HID)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Event is OFF")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self,
                                           timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                           class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                           queue_name=HIDDispatcher.QueueName.EVENT)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End test loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_18B0_0010", _AUTHOR)
    # end def test_kbd_set_monitor_mode_4_in_between_press_and_release

    @features("Feature18B0v1")
    @features("EnhancedKeyboardWithLargerMatrixMode")
    @level("Robustness")
    @bugtracker('MonitorMode_BadRowColValues')
    def test_kbd_set_monitor_mode_5_in_between_press_and_release(self):
        """
        Validate SetMonitorMode in between press and release (Enhanced KBD with large matrix)

        [0] setMonitorMode(mode)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over 5 randomly selected keys")
        # --------------------------------------------------------------------------------------------------------------
        keys = KeyMatrixTestUtils.get_key_list(self, group_count=KeyCodeTestCase.NUMBER_OF_KEYS, random=True)
        for (key,) in keys:
            ChannelUtils.empty_queues(self)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID Report is ON")
            # ----------------------------------------------------------------------------------------------------------
            if key in HidData.KEY_ID_TO_HID_MAP:
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key, MAKE))
            else:
                warnings.warn(f"{key.name} not in KEY_ID_TO_HID_MAP, skipped checking HID report")
                ChannelUtils.empty_queue(self, HIDDispatcher.QueueName.HID)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Event is OFF")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self,
                                           timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                           class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                           queue_name=HIDDispatcher.QueueName.EVENT)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set Monitor Mode = 0x5")
            # ----------------------------------------------------------------------------------------------------------
            response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(
                self, StaticMonitorMode.ENHANCED_KBD_LARGER_MATRIX)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _CHECK_MONITORMODE_RESPONSE)
            # ----------------------------------------------------------------------------------------------------------
            checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
            checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID Report is OFF")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self,
                                           timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                           queue_name=HIDDispatcher.QueueName.HID)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Event is ON")
            # ----------------------------------------------------------------------------------------------------------
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
            enhanced_kbd_with_larger_matrix_mode_event = EnhancedKeyboardWithLargerMatrixModeEvent.fromHexList(
                HexList(event))
            checker = StaticMonitorModeTestUtils.EnhancedKeyboardWithLargerMatrixModeEventChecker
            checker.check_fields(self, enhanced_kbd_with_larger_matrix_mode_event,
                                 EnhancedKeyboardWithLargerMatrixModeEvent)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID Report is OFF")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self,
                                           timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                           queue_name=HIDDispatcher.QueueName.HID)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Event is ON")
            # ----------------------------------------------------------------------------------------------------------
            row_code, col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(test_case=self, key_id=key,
                                                                                 combined=False)
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
            LogHelper.log_step(self, "Set Monitor Mode = 0x0")
            # ----------------------------------------------------------------------------------------------------------
            response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.OFF)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _CHECK_MONITORMODE_RESPONSE)
            # ----------------------------------------------------------------------------------------------------------
            checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
            checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID Report is ON")
            # ----------------------------------------------------------------------------------------------------------
            if key in HidData.KEY_ID_TO_HID_MAP:
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key, BREAK))
            else:
                warnings.warn(f"{key.name} not in KEY_ID_TO_HID_MAP, skipped checking HID report")
                ChannelUtils.empty_queue(self, HIDDispatcher.QueueName.HID)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Event is OFF")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self,
                                           timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                           class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                           queue_name=HIDDispatcher.QueueName.EVENT)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End test loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_18B0_0011", _AUTHOR)
    # end def test_kbd_set_monitor_mode_5_in_between_press_and_release
# end class StaticMonitorModeRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
