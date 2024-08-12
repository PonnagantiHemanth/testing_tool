#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.keyboard.feature_4610.interface
:brief: HID++ 2.0 ``MultiRoller`` interface test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2023/10/03
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.multirollerutils import MultiRollerTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4610.multiroller import MultiRollerTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MultiRollerInterfaceTestCase(MultiRollerTestCase):
    """
    Validate ``MultiRoller`` interface test cases
    """

    @features("Feature4610")
    @level("Interface")
    def test_get_capabilities(self):
        """
        Validate ``GetCapabilities`` normal processing

        [0] getCapabilities() -> numRollers
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetCapabilities request")
        # --------------------------------------------------------------------------------------------------------------
        response = MultiRollerTestUtils.HIDppHelper.get_capabilities(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MultiRollerTestUtils.GetCapabilitiesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_4610_index))
        })
        checker.check_fields(self, response, self.feature_4610.get_capabilities_response_cls, check_map)

        self.testCaseChecked("INT_4610_0001", _AUTHOR)
    # end def test_get_capabilities

    @features("Feature4610")
    @level("Interface")
    def test_get_roller_capabilities(self):
        """
        Validate ``GetRollerCapabilities`` normal processing

        [1] getRollerCapabilities(roller_id) -> incrementsPerRotation, incrementsPerRatchet, capabilities
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetRollerCapabilities request")
        # --------------------------------------------------------------------------------------------------------------
        response = MultiRollerTestUtils.HIDppHelper.get_roller_capabilities(
            test_case=self,
            roller_id=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetRollerCapabilitiesResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MultiRollerTestUtils.GetRollerCapabilitiesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_4610_index)),
        })
        checker.check_fields(self, response, self.feature_4610.get_roller_capabilities_response_cls, check_map)

        self.testCaseChecked("INT_4610_0002", _AUTHOR)
    # end def test_get_roller_capabilities

    @features("Feature4610")
    @level("Interface")
    def test_get_mode(self):
        """
        Validate ``GetMode`` normal processing

        [2] getMode(roller_id) -> roller_mode
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetMode request")
        # --------------------------------------------------------------------------------------------------------------
        response = MultiRollerTestUtils.HIDppHelper.get_mode(
            test_case=self,
            roller_id=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MultiRollerTestUtils.GetModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_4610_index)),
        })
        checker.check_fields(self, response, self.feature_4610.get_mode_response_cls, check_map)

        self.testCaseChecked("INT_4610_0003", _AUTHOR)
    # end def test_get_mode

    @features("Feature4610")
    @level("Interface")
    def test_set_mode(self):
        """
        Validate ``SetMode`` normal processing

        [3] setMode(roller_id, roller_mode) -> None
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMode request")
        # --------------------------------------------------------------------------------------------------------------
        response = MultiRollerTestUtils.HIDppHelper.set_mode(
            test_case=self,
            roller_id=0,
            divert=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MultiRollerTestUtils.SetModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_4610_index))
        })
        checker.check_fields(self, response, self.feature_4610.set_mode_response_cls, check_map)

        self.testCaseChecked("INT_4610_0004", _AUTHOR)
    # end def test_set_mode
# end class MultiRollerInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
