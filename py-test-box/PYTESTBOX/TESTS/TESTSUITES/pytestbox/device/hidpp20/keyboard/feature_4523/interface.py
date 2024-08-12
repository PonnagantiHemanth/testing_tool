#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.keyboard.feature_4523.interface
:brief: HID++ 2.0 ``DisableControlsByCIDX`` interface test suite
:author: Zane Lu <zlu@logitech.com>
:date: 2023/05/25
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.disablecontrolsbycidxutils import DisableControlsByCIDXTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4523.disablecontrolsbycidx import DisableControlsByCIDXTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Zane Lu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DisableControlsByCIDXInterfaceTestCase(DisableControlsByCIDXTestCase):
    """
    Validate ``DisableControlsByCIDX`` interface test cases
    """

    @features("Feature4523")
    @level("Interface")
    def test_set_disabled_controls(self):
        """
        Validate ``SetDisabledControls`` normal processing

        [0] setDisabledControls(cidxBitmap) -> None
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetDisabledControls request")
        # --------------------------------------------------------------------------------------------------------------
        response = DisableControlsByCIDXTestUtils.HIDppHelper.set_disabled_controls(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetDisabledControlsResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DisableControlsByCIDXTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_4523_index))
        }
        checker.check_fields(self, response, self.feature_4523.set_disabled_controls_response_cls, check_map)

        self.testCaseChecked("INT_4523_0001", _AUTHOR)
    # end def test_set_disabled_controls

    @features("Feature4523")
    @level("Interface")
    def test_get_game_mode(self):
        """
        Validate ``GetGameMode`` normal processing

        [1] getGameMode() -> gameModeFullState
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetGameMode request")
        # --------------------------------------------------------------------------------------------------------------
        response = DisableControlsByCIDXTestUtils.HIDppHelper.get_game_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetGameModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DisableControlsByCIDXTestUtils.GetGameModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_4523_index)),
        })
        checker.check_fields(self, response, self.feature_4523.get_game_mode_response_cls, check_map)

        self.testCaseChecked("INT_4523_0002", _AUTHOR)
    # end def test_get_game_mode

    @features("Feature4523v1")
    @level("Interface")
    def test_get_set_power_on_params(self):
        """
        Validate ``GetSetPowerOnParams`` normal processing

        [2] getSetPowerOnParams(setMask, setValue) -> getValue
        """
        poweron_game_mode_lock_valid = False
        poweron_game_mode_valid = False
        poweron_game_mode_lock = False
        poweron_game_mode = False
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetSetPowerOnParams request")
        # --------------------------------------------------------------------------------------------------------------
        response = DisableControlsByCIDXTestUtils.HIDppHelper.get_set_power_on_params(
            test_case=self,
            poweron_game_mode_lock_valid=poweron_game_mode_lock_valid,
            poweron_game_mode_valid=poweron_game_mode_valid,
            poweron_game_mode_lock=poweron_game_mode_lock,
            poweron_game_mode=poweron_game_mode)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetSetPowerOnParamsResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DisableControlsByCIDXTestUtils.GetSetPowerOnParamsResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_4523_index)),
        })
        checker.check_fields(self, response, self.feature_4523.get_set_power_on_params_response_cls, check_map)

        self.testCaseChecked("INT_4523_0003", _AUTHOR)
    # end def test_get_set_power_on_params

    @features("Feature4523v1")
    @level("Interface")
    def test_get_capabilities(self):
        """
        Validate ``GetCapabilities`` normal processing

        [3] getCapabilities() -> supportedPowerOnParams
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetCapabilities request")
        # --------------------------------------------------------------------------------------------------------------
        response = DisableControlsByCIDXTestUtils.HIDppHelper.get_capabilities(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DisableControlsByCIDXTestUtils.GetCapabilitiesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_4523_index)),
        })
        checker.check_fields(self, response, self.feature_4523.get_capabilities_response_cls, check_map)

        self.testCaseChecked("INT_4523_0004", _AUTHOR)
    # end def test_get_capabilities
# end class DisableControlsByCIDXInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
