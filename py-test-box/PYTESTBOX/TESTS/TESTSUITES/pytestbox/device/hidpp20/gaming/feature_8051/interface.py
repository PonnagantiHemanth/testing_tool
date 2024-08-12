#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.gaming.feature_8051.interface
:brief: HID++ 2.0 ``LogiModifiers`` interface test suite
:author: Zane Lu <zlu@logitech.com>
:date: 2023/05/04
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.hexlist import HexList
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.logimodifiersutils import LogiModifiersTestUtils
from pytestbox.device.hidpp20.gaming.feature_8051.logimodifiers import LogiModifiersTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Zane Lu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LogiModifiersInterfaceTestCase(LogiModifiersTestCase):
    """
    Validate ``LogiModifiers`` interface test cases
    """

    @features("Feature8051")
    @level("Interface")
    def test_get_capabilities(self):
        """
        Validate ``GetCapabilities`` normal processing

        [0] getCapabilities() -> gettableModifiers, forceableModifiers
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetCapabilities request")
        # --------------------------------------------------------------------------------------------------------------
        response = LogiModifiersTestUtils.HIDppHelper.get_capabilities(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = LogiModifiersTestUtils.GetCapabilitiesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8051_index)),
        })
        checker.check_fields(self, response, self.feature_8051.get_capabilities_response_cls, check_map)

        self.testCaseChecked("INT_8051_0001", _AUTHOR)
    # end def test_get_capabilities

    @features("Feature8051")
    @level("Interface")
    def test_get_locally_pressed_state(self):
        """
        Validate ``GetLocallyPressedState`` normal processing

        [1] getLocallyPressedState() -> locallyPressedState
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetLocallyPressedState request")
        # --------------------------------------------------------------------------------------------------------------
        response = LogiModifiersTestUtils.HIDppHelper.get_locally_pressed_state(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetLocallyPressedStateResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = LogiModifiersTestUtils.GetLocallyPressedStateResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8051_index)),
        })
        checker.check_fields(self, response, self.feature_8051.get_locally_pressed_state_response_cls, check_map)

        self.testCaseChecked("INT_8051_0002", _AUTHOR)
    # end def test_get_locally_pressed_state

    @features("Feature8051")
    @level("Interface")
    def test_set_forced_pressed_state(self):
        """
        Validate ``SetForcedPressedState`` normal processing

        [2] setForcedPressedState(forcedPressedState) -> None
        """
        g_shift = 0
        fn = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetForcedPressedState request")
        # --------------------------------------------------------------------------------------------------------------
        response = LogiModifiersTestUtils.HIDppHelper.set_forced_pressed_state(
            test_case=self,
            g_shift=g_shift,
            fn=fn)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetForcedPressedStateResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = LogiModifiersTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8051_index))
        }
        checker.check_fields(self, response, self.feature_8051.set_forced_pressed_state_response_cls, check_map)

        self.testCaseChecked("INT_8051_0003", _AUTHOR)
    # end def test_set_forced_pressed_state

    @features("Feature8051")
    @level("Interface")
    def test_set_press_events(self):
        """
        Validate ``SetPressEvents`` normal processing

        [3] setPressEvents(reportedModifiers) -> None
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetPressEvents request with all parameters equal to their default value")
        # --------------------------------------------------------------------------------------------------------------
        response = LogiModifiersTestUtils.HIDppHelper.set_press_events(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetPressEventsResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = LogiModifiersTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8051_index))
        }
        checker.check_fields(self, response, self.feature_8051.set_press_events_response_cls, check_map)

        self.testCaseChecked("INT_8051_0004", _AUTHOR)
    # end def test_set_press_events

    @features("Feature8051")
    @level("Interface")
    def test_get_forced_pressed_state(self):
        """
        Validate ``GetForcedPressedState`` normal processing

        [4] getForcedPressedState() -> forcedPressedStateRsp
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetForcedPressedState request")
        # --------------------------------------------------------------------------------------------------------------
        response = LogiModifiersTestUtils.HIDppHelper.get_forced_pressed_state(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetForcedPressedStateResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        # noinspection DuplicatedCode
        checker = LogiModifiersTestUtils.GetForcedPressedStateResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8051_index)),
        })
        checker.check_fields(self, response, self.feature_8051.get_forced_pressed_state_response_cls, check_map)

        self.testCaseChecked("INT_8051_0005", _AUTHOR)
    # end def test_get_forced_pressed_state

    @features("Feature8051")
    @level("Interface")
    def test_get_press_events(self):
        """
        Validate ``GetPressEvents`` normal processing

        [5] getPressEvents() -> reportedModifiersRsp
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetPressEvents request")
        # --------------------------------------------------------------------------------------------------------------
        response = LogiModifiersTestUtils.HIDppHelper.get_press_events(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetPressEventsResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        # noinspection DuplicatedCode
        checker = LogiModifiersTestUtils.GetPressEventsResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8051_index)),
        })
        checker.check_fields(self, response, self.feature_8051.get_press_events_response_cls, check_map)

        self.testCaseChecked("INT_8051_0006", _AUTHOR)
    # end def test_get_press_events
# end class LogiModifiersInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
