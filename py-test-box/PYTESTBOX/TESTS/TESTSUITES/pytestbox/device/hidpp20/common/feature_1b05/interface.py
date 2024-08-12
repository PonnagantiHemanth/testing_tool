#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1b05.interface
:brief: HID++ 2.0 ``FullKeyCustomization`` interface test suite
:author: Masan Xu <mxu11@logitech.com>
:date: 2023/05/04
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import time

from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.common.fullkeycustomization import FullKeyCustomization
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.fullkeycustomizationutils import FullKeyCustomizationTestUtils
from pytestbox.device.hidpp20.common.feature_1b05.fullkeycustomization import FullKeyCustomizationTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Masan Xu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class FullKeyCustomizationInterfaceTestCase(FullKeyCustomizationTestCase):
    """
    Validate ``FullKeyCustomization`` interface test cases
    """

    @features('Keyboard')
    @features("Feature1B05")
    @level("Interface")
    def test_get_capabilities(self):
        """
        Validate ``GetCapabilities`` normal processing

        [0] getCapabilities() -> fkcConfigFileVer, macroDefFileVer, fkcConfigFileMaxsize,
        macroDefFileMaxsize, fkcConfigMaxTriggers, SwConfigCapabilities
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetCapabilities request")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_capabilities(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = FullKeyCustomizationTestUtils.GetCapabilitiesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_1b05_index))
        })
        checker.check_fields(self, response, self.feature_1b05.get_capabilities_response_cls, check_map)

        self.testCaseChecked("INT_1B05_0001", _AUTHOR)
    # end def test_get_capabilities

    @features('Keyboard')
    @features("Feature1B05")
    @level("Interface")
    def test_get_set_power_on_params(self):
        """
        Validate ``GetSetPowerOnParams`` normal processing

        [1] getSetPowerOnParams(setPowerOnFkcState, powerOnFkcState) -> powerOnFkcState
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetSetPowerOnParams request")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_power_on_params(
            test_case=self,
            set_power_on_fkc_enable=FullKeyCustomization.PowerOnFKCRequest.GET)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetSetPowerOnParamsResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = FullKeyCustomizationTestUtils.GetSetPowerOnParamsResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_1b05_index)),
        })
        checker.check_fields(self, response, self.feature_1b05.get_set_power_on_params_response_cls, check_map)

        self.testCaseChecked("INT_1B05_0002", _AUTHOR)
    # end def test_get_set_power_on_params

    @features('Keyboard')
    @features("Feature1B05")
    @level("Interface")
    def test_get_toggle_key_list(self):
        """
        Validate ``GetToggleKeyList`` normal processing

        [2] getToggleKeyList() -> toggleKey0, toggleKey1, toggleKey2, toggleKey3, toggleKey4, toggleKey5,
        toggleKey6, toggleKey7
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetToggleKeyList request")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_toggle_key_list(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetToggleKeyListResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = FullKeyCustomizationTestUtils.GetToggleKeyListResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_1b05_index)),
        })
        checker.check_fields(self, response, self.feature_1b05.get_toggle_key_list_response_cls, check_map)

        self.testCaseChecked("INT_1B05_0003", _AUTHOR)
    # end def test_get_toggle_key_list

    @features('Keyboard')
    @features("Feature1B05")
    @level("Interface")
    def test_get_set_enabled(self):
        """
        Validate ``GetSetEnabled`` normal processing

        [3] getSetEnabled(setGetFkcState, fkcState, toggleKeysState) -> fkcState, toggleKeysState
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetSetEnabled request")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            test_case=self,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.GET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET,
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetSetEnabledResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = FullKeyCustomizationTestUtils.GetSetEnabledResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_1b05_index)),
        })
        checker.check_fields(self, response, self.feature_1b05.get_set_enabled_response_cls, check_map)

        self.testCaseChecked("INT_1B05_0004", _AUTHOR)
    # end def test_get_set_enabled

    @features("Feature1B05V1+")
    @level("Interface")
    def test_get_set_sw_configuration_cookie(self):
        """
        Validate the API function 'getSetSWConfigurationCookie'
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getSetSWConfigurationCookie request")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_sw_configuration_cookie(
            test_case=self,
            set_sw_configuration_cookie=FullKeyCustomization.SWConfigurationCookieRequest.GET,
            sw_configuration_cookie=0,
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait for getSetSWConfigurationCookie response and validate response is success")
        # --------------------------------------------------------------------------------------------------------------
        checker = FullKeyCustomizationTestUtils.GetSetSWConfigurationCookieResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_1b05_index)),
        })
        checker.check_fields(self, response, self.feature_1b05.get_set_sw_configuration_cookie_response_cls, check_map)

        self.testCaseChecked("INT_1B05_0005", _AUTHOR)
    # end def test_get_set_sw_configuration_cookie
# end class FullKeyCustomizationInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
