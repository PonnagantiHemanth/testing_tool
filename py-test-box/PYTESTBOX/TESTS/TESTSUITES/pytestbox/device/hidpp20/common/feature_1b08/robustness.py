#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1b08.robustness
:brief: HID++ 2.0 ``AnalogKeys`` robustness test suite
:author: Fred Chen <fchen7@logitech.com>
:date: 2024/03/13
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.analogkeys import AnalogKeys
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.analogkeysutils import AnalogKeysTestUtils
from pytestbox.device.hidpp20.common.feature_1b08.analogkeys import AnalogKeysTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Fred Chen"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_RESERVED = "Test loop over reserved range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AnalogKeysRobustnessTestCase(AnalogKeysTestCase):
    """
    Validate ``AnalogKeys`` robustness test cases
    """

    @features("Feature1B08")
    @level("Robustness")
    def test_get_capabilities_software_id(self):
        """
        Validate ``GetCapabilities`` software id field is ignored by the firmware

        [0] getCapabilities() -> analogKeyConfigFileVer, analogKeyConfigFileMaxsize, analogKeyLevelResolution

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(AnalogKeys.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = AnalogKeysTestUtils.HIDppHelper.get_capabilities(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AnalogKeysTestUtils.GetCapabilitiesResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_1b08.get_capabilities_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1B08_0001#1", _AUTHOR)
    # end def test_get_capabilities_software_id

    @features("Feature1B08")
    @level("Robustness")
    def test_get_rapid_trigger_state_software_id(self):
        """
        Validate ``GetRapidTriggerState`` software id field is ignored by the firmware

        [1] getRapidTriggerState() -> rtSettings

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        rapid_trigger_state = False
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(AnalogKeys.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetRapidTriggerState request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = AnalogKeysTestUtils.HIDppHelper.get_rapid_trigger_state(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetRapidTriggerStateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AnalogKeysTestUtils.RapidTriggerSettingsChecker
            rapid_trigger_settings = {
                "reserved": (checker.check_reserved, 0),
                "rapid_trigger_state": (checker.check_rapid_trigger_state, rapid_trigger_state)
            }
            checker = AnalogKeysTestUtils.GetRapidTriggerStateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rapid_trigger_settings": (checker.check_rapid_trigger_settings, rapid_trigger_settings)
            })
            checker.check_fields(self, response, self.feature_1b08.get_rapid_trigger_state_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1B08_0001#2", _AUTHOR)
    # end def test_get_rapid_trigger_state_software_id

    @features("Feature1B08")
    @level("Robustness")
    def test_set_rapid_trigger_state_software_id(self):
        """
        Validate ``SetRapidTriggerState`` software id field is ignored by the firmware

        [2] setRapidTriggerState(rtSettings) -> rtSettings

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RTSettings

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        rapid_trigger_state = False
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(AnalogKeys.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetRapidTriggerState request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = AnalogKeysTestUtils.HIDppHelper.set_rapid_trigger_state(
                test_case=self,
                rapid_trigger_state=rapid_trigger_state,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetRapidTriggerStateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AnalogKeysTestUtils.RapidTriggerSettingsChecker
            rapid_trigger_settings = {
                "reserved": (checker.check_reserved, 0),
                "rapid_trigger_state": (checker.check_rapid_trigger_state, rapid_trigger_state)
            }
            checker = AnalogKeysTestUtils.SetRapidTriggerStateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rapid_trigger_settings": (checker.check_rapid_trigger_settings, rapid_trigger_settings)
            })
            checker.check_fields(self, response, self.feature_1b08.set_rapid_trigger_state_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1B08_0001#3", _AUTHOR)
    # end def test_set_rapid_trigger_state_software_id

    @features("Feature1B08")
    @level("Robustness")
    def test_set_key_travel_event_state_software_id(self):
        """
        Validate ``SetKeyTravelEventState`` software id field is ignored by the firmware

        [3] setKeyTravelEventState(ktSettings) -> ktSettings

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.KTSettings

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        key_travel_event_state = False
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(AnalogKeys.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetKeyTravelEventState request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = AnalogKeysTestUtils.HIDppHelper.set_key_travel_event_state(
                test_case=self,
                key_travel_event_state=key_travel_event_state,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetKeyTravelEventStateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AnalogKeysTestUtils.KeyTravelSettingsChecker
            key_travel_settings = {
                "reserved": (checker.check_reserved, 0),
                "key_travel_event_state": (checker.check_key_travel_event_state, key_travel_event_state)
            }
            checker = AnalogKeysTestUtils.SetKeyTravelEventStateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "key_travel_settings": (checker.check_key_travel_settings, key_travel_settings)
            })
            checker.check_fields(self, response, self.feature_1b08.set_key_travel_event_state_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1B08_0001#4", _AUTHOR)
    # end def test_set_key_travel_event_state_software_id

    @features("Feature1B08")
    @level("Robustness")
    def test_get_capabilities_padding(self):
        """
        Validate ``GetCapabilities`` padding bytes are ignored by the firmware

        [0] getCapabilities() -> analogKeyConfigFileVer, analogKeyConfigFileMaxsize, analogKeyLevelResolution

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1b08.get_capabilities_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = AnalogKeysTestUtils.HIDppHelper.get_capabilities(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AnalogKeysTestUtils.GetCapabilitiesResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_1b08.get_capabilities_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1B08_0002#1", _AUTHOR)
    # end def test_get_capabilities_padding

    @features("Feature1B08")
    @level("Robustness")
    def test_get_rapid_trigger_state_padding(self):
        """
        Validate ``GetRapidTriggerState`` padding bytes are ignored by the firmware

        [1] getRapidTriggerState() -> rtSettings

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        rapid_trigger_state = False
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1b08.get_rapid_trigger_state_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetRapidTriggerState request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = AnalogKeysTestUtils.HIDppHelper.get_rapid_trigger_state(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetRapidTriggerStateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AnalogKeysTestUtils.RapidTriggerSettingsChecker
            rapid_trigger_settings = {
                "reserved": (checker.check_reserved, 0),
                "rapid_trigger_state": (checker.check_rapid_trigger_state, rapid_trigger_state)
            }
            checker = AnalogKeysTestUtils.GetRapidTriggerStateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rapid_trigger_settings": (checker.check_rapid_trigger_settings, rapid_trigger_settings)
            })
            checker.check_fields(self, response, self.feature_1b08.get_rapid_trigger_state_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1B08_0002#2", _AUTHOR)
    # end def test_get_rapid_trigger_state_padding

    @features("Feature1B08")
    @level("Robustness")
    def test_set_rapid_trigger_state_reserved(self):
        """
        Validate ``SetRapidTriggerState`` reserved bytes are ignored by the firmware

        [2] setRapidTriggerState(rtSettings) -> rtSettings
        """
        rapid_trigger_state = False
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_RESERVED)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1b08.set_rapid_trigger_state_cls
        for reserved in compute_wrong_range(0, max_value=(1 << request_cls.LEN.RESERVED) - 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetRapidTriggerState request with reserved: {reserved}")
            # ----------------------------------------------------------------------------------------------------------
            response = AnalogKeysTestUtils.HIDppHelper.set_rapid_trigger_state(
                test_case=self,
                rapid_trigger_state=rapid_trigger_state,
                reserved=reserved)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetRapidTriggerStateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AnalogKeysTestUtils.RapidTriggerSettingsChecker
            rapid_trigger_settings = {
                "reserved": (checker.check_reserved, 0),
                "rapid_trigger_state": (checker.check_rapid_trigger_state, rapid_trigger_state)
            }
            checker = AnalogKeysTestUtils.SetRapidTriggerStateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rapid_trigger_settings": (checker.check_rapid_trigger_settings, rapid_trigger_settings)
            })
            checker.check_fields(self, response, self.feature_1b08.set_rapid_trigger_state_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1B08_0002#3", _AUTHOR)
    # end def test_set_rapid_trigger_state_reserved

    @features("Feature1B08")
    @level("Robustness")
    def test_set_key_travel_event_state_reserved(self):
        """
        Validate ``SetKeyTravelEventState`` reserved bytes are ignored by the firmware

        [3] setKeyTravelEventState(ktSettings) -> ktSettings
        """
        key_travel_event_state = False
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_RESERVED)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1b08.set_key_travel_event_state_cls
        for reserved in compute_wrong_range(0, max_value=(1 << request_cls.LEN.RESERVED) - 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetKeyTravelEventState request with reserved: {reserved}")
            # ----------------------------------------------------------------------------------------------------------
            response = AnalogKeysTestUtils.HIDppHelper.set_key_travel_event_state(
                test_case=self,
                key_travel_event_state=key_travel_event_state,
                reserved=reserved)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetKeyTravelEventStateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AnalogKeysTestUtils.KeyTravelSettingsChecker
            key_travel_settings = {
                "reserved": (checker.check_reserved, 0),
                "key_travel_event_state": (checker.check_key_travel_event_state, key_travel_event_state)
            }
            checker = AnalogKeysTestUtils.SetKeyTravelEventStateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "kt_settings": (checker.check_key_travel_settings, key_travel_settings)
            })
            checker.check_fields(self, response, self.feature_1b08.set_key_travel_event_state_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1B08_0002#4", _AUTHOR)
    # end def test_set_key_travel_event_state_reserved
# end class AnalogKeysRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
