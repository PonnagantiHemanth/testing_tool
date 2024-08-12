#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.gaming.feature_8040.interface
:brief: HID++ 2.0 ``BrightnessControl`` interface test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2023/11/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.gaming.brightnesscontrol import CapabilitiesV1
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.brightnesscontrolutils import BrightnessControlTestUtils
from pytestbox.device.hidpp20.gaming.feature_8040.brightnesscontrol import BrightnessControlTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BrightnessControlInterfaceTestCase(BrightnessControlTestCase):
    """
    Validate ``BrightnessControl`` interface test cases
    """

    @features("Feature8040")
    @level("Interface")
    def test_get_info(self):
        """
        Validate ``GetInfo`` normal processing

        [0] getInfo() -> maxBrightness, capabilities
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetInfo request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_info(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetInfoResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = BrightnessControlTestUtils.GetInfoResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8040_index)),
        })
        checker.check_fields(self, response, self.feature_8040.get_info_response_cls, check_map)

        self.testCaseChecked("INT_8040_0001", _AUTHOR)
    # end def test_get_info

    @features("Feature8040")
    @level("Interface")
    def test_get_brightness(self):
        """
        Validate ``GetBrightness`` normal processing

        [1] getBrightness() -> brightness
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetBrightness request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_brightness(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetBrightnessResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = BrightnessControlTestUtils.GetBrightnessResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8040_index)),
        })
        checker.check_fields(self, response, self.feature_8040.get_brightness_response_cls, check_map)

        self.testCaseChecked("INT_8040_0002", _AUTHOR)
    # end def test_get_brightness

    @features("Feature8040")
    @level("Interface")
    def test_set_brightness(self):
        """
        Validate ``SetBrightness`` normal processing

        [2] setBrightness(brightness) -> None
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetBrightness request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.set_brightness(
            test_case=self,
            brightness=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetBrightnessResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = BrightnessControlTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8040_index))
        }
        checker.check_fields(self, response, self.feature_8040.set_brightness_response_cls, check_map)

        self.testCaseChecked("INT_8040_0003", _AUTHOR)
    # end def test_set_brightness

    @features("Feature8040v1")
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.ILLUMINATION)
    @level("Interface")
    def test_get_illumination(self):
        """
        Validate ``GetIllumination`` normal processing

        [3] getIllumination() -> state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetIllumination request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_illumination(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetIlluminationResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = BrightnessControlTestUtils.GetIlluminationResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8040_index)),
        })
        checker.check_fields(self, response, self.feature_8040.get_illumination_response_cls, check_map)

        self.testCaseChecked("INT_8040_0004", _AUTHOR)
    # end def test_get_illumination

    @features("Feature8040v1")
    @features("RequiredBrightnessCapability", CapabilitiesV1.POS.ILLUMINATION)
    @level("Interface")
    def test_set_illumination(self):
        """
        Validate ``SetIllumination`` normal processing

        [4] setIllumination(state) -> None
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetIllumination request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.set_illumination(
            test_case=self,
            state=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetIlluminationResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = BrightnessControlTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8040_index))
        }
        checker.check_fields(self, response, self.feature_8040.set_illumination_response_cls, check_map)

        self.testCaseChecked("INT_8040_0005", _AUTHOR)
    # end def test_set_illumination
# end class BrightnessControlInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
