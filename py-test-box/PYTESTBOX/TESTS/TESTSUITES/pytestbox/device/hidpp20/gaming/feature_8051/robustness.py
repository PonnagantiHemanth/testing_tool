#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.gaming.feature_8051.robustness
:brief: HID++ 2.0 ``LogiModifiers`` robustness test suite
:author: Zane Lu <zlu@logitech.com>
:date: 2023/05/04
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.gaming.logimodifiers import LogiModifiers
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.logimodifiersutils import LogiModifiersTestUtils
from pytestbox.device.hidpp20.gaming.feature_8051.logimodifiers import LogiModifiersTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Zane Lu"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class LogiModifiersRobustnessTestCase(LogiModifiersTestCase):
    """
    Validate ``LogiModifiers`` robustness test cases
    """

    @features("Feature8051")
    @level("Robustness")
    def test_get_capabilities_software_id(self):
        """
        Validate ``GetCapabilities`` software id field is ignored by the firmware

        [0] getCapabilities() -> gettableModifiers, forceableModifiers

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(LogiModifiers.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = LogiModifiersTestUtils.HIDppHelper.get_capabilities(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = LogiModifiersTestUtils.GetCapabilitiesResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_8051.get_capabilities_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8051_0001#1", _AUTHOR)
    # end def test_get_capabilities_software_id

    @features("Feature8051")
    @level("Robustness")
    def test_get_locally_pressed_state_software_id(self):
        """
        Validate ``GetLocallyPressedState`` software id field is ignored by the firmware

        [1] getLocallyPressedState() -> locallyPressedState

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(LogiModifiers.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetLocallyPressedState request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = LogiModifiersTestUtils.HIDppHelper.get_locally_pressed_state(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetLocallyPressedStateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = LogiModifiersTestUtils.GetLocallyPressedStateResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_8051.get_locally_pressed_state_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8051_0001#2", _AUTHOR)
    # end def test_get_locally_pressed_state_software_id

    @features("Feature8051")
    @level("Robustness")
    def test_set_forced_pressed_state_software_id(self):
        """
        Validate ``SetForcedPressedState`` software id field is ignored by the firmware

        [2] setForcedPressedState(forcedPressedState) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.ForcedPressedState.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        g_shift = 0
        fn = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(LogiModifiers.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetForcedPressedState request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = LogiModifiersTestUtils.HIDppHelper.set_forced_pressed_state(
                test_case=self,
                g_shift=g_shift,
                fn=fn,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetForcedPressedStateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            LogiModifiersTestUtils.MessageChecker.check_fields(
                self, response, self.feature_8051.set_forced_pressed_state_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8051_0001#3", _AUTHOR)
    # end def test_set_forced_pressed_state_software_id

    @features("Feature8051")
    @level("Robustness")
    def test_set_press_events_software_id(self):
        """
        Validate ``SetPressEvents`` software id field is ignored by the firmware

        [3] setPressEvents(reportedModifiers) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.ReportedModifiers.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        g_shift = 0
        fn = 0
        right_gui = 0
        right_alt = 0
        right_shift = 0
        right_ctrl = 0
        left_gui = 0
        left_alt = 0
        left_shift = 0
        left_ctrl = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(LogiModifiers.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetPressEvents request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = LogiModifiersTestUtils.HIDppHelper.set_press_events(
                test_case=self,
                g_shift=g_shift,
                fn=fn,
                right_gui=right_gui,
                right_alt=right_alt,
                right_shift=right_shift,
                right_ctrl=right_ctrl,
                left_gui=left_gui,
                left_alt=left_alt,
                left_shift=left_shift,
                left_ctrl=left_ctrl,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetPressEventsResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            LogiModifiersTestUtils.MessageChecker.check_fields(
                self, response, self.feature_8051.set_press_events_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8051_0001#4", _AUTHOR)
    # end def test_set_press_events_software_id

    @features("Feature8051")
    @level("Robustness")
    def test_get_forced_pressed_state_software_id(self):
        """
        Validate ``GetForcedPressedState`` software id field is ignored by the firmware

        [4] getForcedPressedState() -> forcedPressedStateRsp

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        g_shift = 0
        fn = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(LogiModifiers.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetForcedPressedState request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = LogiModifiersTestUtils.HIDppHelper.get_forced_pressed_state(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetForcedPressedStateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = LogiModifiersTestUtils.ForcedPressedStateResponseChecker
            forced_pressed_state_rsp = {
                "g_shift": (checker.check_g_shift, g_shift),
                "fn": (checker.check_fn, fn)
            }
            checker = LogiModifiersTestUtils.GetForcedPressedStateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "forced_pressed_state_rsp": (checker.check_forced_pressed_state_rsp, forced_pressed_state_rsp)
            })
            checker.check_fields(self, response, self.feature_8051.get_forced_pressed_state_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8051_0001#5", _AUTHOR)
    # end def test_get_forced_pressed_state_software_id

    @features("Feature8051")
    @level("Robustness")
    def test_get_press_events_software_id(self):
        """
        Validate ``GetPressEvents`` software id field is ignored by the firmware

        [5] getPressEvents() -> reportedModifiersRsp

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        g_shift = 0
        fn = 0
        right_gui = 0
        right_alt = 0
        right_shift = 0
        right_ctrl = 0
        left_gui = 0
        left_alt = 0
        left_shift = 0
        left_ctrl = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(LogiModifiers.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetPressEvents request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = LogiModifiersTestUtils.HIDppHelper.get_press_events(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetPressEventsResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = LogiModifiersTestUtils.ReportedModifiersRspChecker
            reported_modifiers_rsp = {
                "g_shift": (checker.check_g_shift, g_shift),
                "fn": (checker.check_fn, fn),
                "right_gui": (checker.check_right_gui, right_gui),
                "right_alt": (checker.check_right_alt, right_alt),
                "right_shift": (checker.check_right_shift, right_shift),
                "right_ctrl": (checker.check_right_ctrl, right_ctrl),
                "left_gui": (checker.check_left_gui, left_gui),
                "left_alt": (checker.check_left_alt, left_alt),
                "left_shift": (checker.check_left_shift, left_shift),
                "left_ctrl": (checker.check_left_ctrl, left_ctrl)
            }
            checker = LogiModifiersTestUtils.GetPressEventsResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "reported_modifiers_rsp": (checker.check_reported_modifiers_rsp, reported_modifiers_rsp)
            })
            checker.check_fields(self, response, self.feature_8051.get_press_events_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8051_0001#6", _AUTHOR)
    # end def test_get_press_events_software_id

    @features("Feature8051")
    @level("Robustness")
    def test_get_capabilities_padding(self):
        """
        Validate ``GetCapabilities`` padding bytes are ignored by the firmware

        [0] getCapabilities() -> gettableModifiers, forceableModifiers

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8051.get_capabilities_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = LogiModifiersTestUtils.HIDppHelper.get_capabilities(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = LogiModifiersTestUtils.GetCapabilitiesResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_8051.get_capabilities_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8051_0002#1", _AUTHOR)
    # end def test_get_capabilities_padding

    @features("Feature8051")
    @level("Robustness")
    def test_get_locally_pressed_state_padding(self):
        """
        Validate ``GetLocallyPressedState`` padding bytes are ignored by the firmware

        [1] getLocallyPressedState() -> locallyPressedState

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8051.get_locally_pressed_state_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetLocallyPressedState request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = LogiModifiersTestUtils.HIDppHelper.get_locally_pressed_state(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetLocallyPressedStateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = LogiModifiersTestUtils.GetLocallyPressedStateResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_8051.get_locally_pressed_state_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8051_0002#2", _AUTHOR)
    # end def test_get_locally_pressed_state_padding

    @features("Feature8051")
    @level("Robustness")
    def test_set_forced_pressed_state_padding(self):
        """
        Validate ``SetForcedPressedState`` padding bytes are ignored by the firmware

        [2] setForcedPressedState(forcedPressedState) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.ForcedPressedState.0xPP

        Padding (PP) boundary values [00..FF]
        """
        g_shift = 0
        fn = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8051.set_forced_pressed_state_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetForcedPressedState request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = LogiModifiersTestUtils.HIDppHelper.set_forced_pressed_state(
                test_case=self,
                g_shift=g_shift,
                fn=fn,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetForcedPressedStateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            LogiModifiersTestUtils.MessageChecker.check_fields(
                self, response, self.feature_8051.set_forced_pressed_state_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8051_0002#3", _AUTHOR)
    # end def test_set_forced_pressed_state_padding

    @features("Feature8051")
    @level("Robustness")
    def test_set_press_events_padding(self):
        """
        Validate ``SetPressEvents`` padding bytes are ignored by the firmware

        [3] setPressEvents(reportedModifiers) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.ReportedModifiers.0xPP

        Padding (PP) boundary values [00..FF]
        """
        g_shift = 0
        fn = 0
        right_gui = 0
        right_alt = 0
        right_shift = 0
        right_ctrl = 0
        left_gui = 0
        left_alt = 0
        left_shift = 0
        left_ctrl = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8051.set_press_events_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetPressEvents request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = LogiModifiersTestUtils.HIDppHelper.set_press_events(
                test_case=self,
                g_shift=g_shift,
                fn=fn,
                right_gui=right_gui,
                right_alt=right_alt,
                right_shift=right_shift,
                right_ctrl=right_ctrl,
                left_gui=left_gui,
                left_alt=left_alt,
                left_shift=left_shift,
                left_ctrl=left_ctrl,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetPressEventsResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            LogiModifiersTestUtils.MessageChecker.check_fields(
                self, response, self.feature_8051.set_press_events_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8051_0002#4", _AUTHOR)
    # end def test_set_press_events_padding

    @features("Feature8051")
    @level("Robustness")
    def test_get_forced_pressed_state_padding(self):
        """
        Validate ``GetForcedPressedState`` padding bytes are ignored by the firmware

        [4] getForcedPressedState() -> forcedPressedStateRsp

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        g_shift = 0
        fn = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8051.get_forced_pressed_state_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetForcedPressedState request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = LogiModifiersTestUtils.HIDppHelper.get_forced_pressed_state(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetForcedPressedStateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = LogiModifiersTestUtils.ForcedPressedStateResponseChecker
            forced_pressed_state_rsp = {
                "g_shift": (checker.check_g_shift, g_shift),
                "fn": (checker.check_fn, fn)
            }
            checker = LogiModifiersTestUtils.GetForcedPressedStateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "forced_pressed_state_rsp": (checker.check_forced_pressed_state_rsp, forced_pressed_state_rsp)
            })
            checker.check_fields(self, response, self.feature_8051.get_forced_pressed_state_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8051_0002#5", _AUTHOR)

    # end def test_get_forced_pressed_state_padding

    @features("Feature8051")
    @level("Robustness")
    def test_get_press_events_padding(self):
        """
        Validate ``GetPressEvents`` padding bytes are ignored by the firmware

        [5] getPressEvents() -> reportedModifiersRsp

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        g_shift = 0
        fn = 0
        right_gui = 0
        right_alt = 0
        right_shift = 0
        right_ctrl = 0
        left_gui = 0
        left_alt = 0
        left_shift = 0
        left_ctrl = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8051.get_press_events_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetPressEvents request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = LogiModifiersTestUtils.HIDppHelper.get_press_events(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetPressEventsResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = LogiModifiersTestUtils.ReportedModifiersRspChecker
            reported_modifiers_rsp = {
                "g_shift": (checker.check_g_shift, g_shift),
                "fn": (checker.check_fn, fn),
                "right_gui": (checker.check_right_gui, right_gui),
                "right_alt": (checker.check_right_alt, right_alt),
                "right_shift": (checker.check_right_shift, right_shift),
                "right_ctrl": (checker.check_right_ctrl, right_ctrl),
                "left_gui": (checker.check_left_gui, left_gui),
                "left_alt": (checker.check_left_alt, left_alt),
                "left_shift": (checker.check_left_shift, left_shift),
                "left_ctrl": (checker.check_left_ctrl, left_ctrl)
            }
            checker = LogiModifiersTestUtils.GetPressEventsResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "reported_modifiers_rsp": (checker.check_reported_modifiers_rsp, reported_modifiers_rsp)
            })
            checker.check_fields(self, response, self.feature_8051.get_press_events_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8051_0002#6", _AUTHOR)
    # end def test_get_press_events_padding
# end class LogiModifiersRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
