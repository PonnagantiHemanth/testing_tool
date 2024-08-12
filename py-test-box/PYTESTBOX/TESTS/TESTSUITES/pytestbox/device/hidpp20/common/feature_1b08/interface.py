#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1b08.interface
:brief: HID++ 2.0 ``AnalogKeys`` interface test suite
:author: Fred Chen <fchen7@logitech.com>
:date: 2024/03/13
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.analogkeysutils import AnalogKeysTestUtils
from pytestbox.device.hidpp20.common.feature_1b08.analogkeys import AnalogKeysTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Fred Chen"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AnalogKeysInterfaceTestCase(AnalogKeysTestCase):
    """
    Validate ``AnalogKeys`` interface test cases
    """

    @features("Feature1B08")
    @level("Interface")
    def test_get_capabilities(self):
        """
        Validate ``GetCapabilities`` normal processing

        [0] getCapabilities() -> analogKeyConfigFileVer, analogKeyConfigFileMaxsize, analogKeyLevelResolution
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetCapabilities request")
        # --------------------------------------------------------------------------------------------------------------
        response = AnalogKeysTestUtils.HIDppHelper.get_capabilities(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalogKeysTestUtils.GetCapabilitiesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_1b08_index))
        })
        checker.check_fields(self, response, self.feature_1b08.get_capabilities_response_cls, check_map)

        self.testCaseChecked("INT_1B08_0001", _AUTHOR)
    # end def test_get_capabilities

    @features("Feature1B08")
    @level("Interface")
    def test_get_rapid_trigger_state(self):
        """
        Validate ``GetRapidTriggerState`` normal processing

        [1] getRapidTriggerState() -> rtSettings
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetRapidTriggerState request")
        # --------------------------------------------------------------------------------------------------------------
        response = AnalogKeysTestUtils.HIDppHelper.get_rapid_trigger_state(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetRapidTriggerStateResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalogKeysTestUtils.GetRapidTriggerStateResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_1b08_index)),
        })
        checker.check_fields(self, response, self.feature_1b08.get_rapid_trigger_state_response_cls, check_map)

        self.testCaseChecked("INT_1B08_0002", _AUTHOR)
    # end def test_get_rapid_trigger_state

    @features("Feature1B08")
    @level("Interface")
    def test_set_rapid_trigger_state(self):
        """
        Validate ``SetRapidTriggerState`` normal processing

        [2] setRapidTriggerState(rtSettings) -> rtSettings
        """
        rapid_trigger_state = False
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetRapidTriggerState request")
        # --------------------------------------------------------------------------------------------------------------
        response = AnalogKeysTestUtils.HIDppHelper.set_rapid_trigger_state(
            test_case=self,
            rapid_trigger_state=rapid_trigger_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetRapidTriggerStateResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalogKeysTestUtils.RapidTriggerSettingsChecker
        rapid_trigger_settings = {
            "reserved": (checker.check_reserved, 0),
            "rapid_trigger_state": (checker.check_rapid_trigger_state, rapid_trigger_state)
        }
        checker = AnalogKeysTestUtils.SetRapidTriggerStateResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_1b08_index)),
            "rapid_trigger_settings": (checker.check_rapid_trigger_settings, rapid_trigger_settings)
        })
        checker.check_fields(self, response, self.feature_1b08.set_rapid_trigger_state_response_cls, check_map)

        self.testCaseChecked("INT_1B08_0003", _AUTHOR)
    # end def test_set_rapid_trigger_state

    @features("Feature1B08")
    @level("Interface")
    def test_set_key_travel_event_state(self):
        """
        Validate ``SetKeyTravelEventState`` normal processing

        [3] setKeyTravelEventState(ktSettings) -> ktSettings
        """
        key_travel_event_state = False
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetKeyTravelEventState request")
        # --------------------------------------------------------------------------------------------------------------
        response = AnalogKeysTestUtils.HIDppHelper.set_key_travel_event_state(
            test_case=self,
            key_travel_event_state=key_travel_event_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetKeyTravelEventStateResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalogKeysTestUtils.KeyTravelSettingsChecker
        key_travel_settings = {
            "reserved": (checker.check_reserved, 0),
            "key_travel_event_state": (checker.check_key_travel_event_state, key_travel_event_state)
        }
        checker = AnalogKeysTestUtils.SetKeyTravelEventStateResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_1b08_index)),
            "key_travel_settings": (checker.check_key_travel_settings, key_travel_settings)
        })
        checker.check_fields(self, response, self.feature_1b08.set_key_travel_event_state_response_cls, check_map)

        self.testCaseChecked("INT_1B08_0004", _AUTHOR)
    # end def test_set_key_travel_event_state
# end class AnalogKeysInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
