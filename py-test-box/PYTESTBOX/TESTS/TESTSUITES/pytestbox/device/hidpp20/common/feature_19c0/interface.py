#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_19c0.interface
:brief: HID++ 2.0 ``ForceSensingButton`` interface test suite
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2024/08/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.forcesensingbuttonutils import ForceSensingButtonTestUtils
from pytestbox.device.hidpp20.common.feature_19c0.forcesensingbutton import ForceSensingButtonTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vinodh Selvaraj"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class ForceSensingButtonInterfaceTestCase(ForceSensingButtonTestCase):
    """
    Validate ``ForceSensingButton`` interface test cases
    """

    @features("Feature19C0")
    @level("Interface")
    def test_get_capabilities(self):
        """
        Validate ``GetCapabilities`` normal processing

        [0] getCapabilities() -> numberOfButtons
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetCapabilities request")
        # --------------------------------------------------------------------------------------------------------------
        response = ForceSensingButtonTestUtils.HIDppHelper.get_capabilities(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ForceSensingButtonTestUtils.GetCapabilitiesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_19c0_index))
        })
        checker.check_fields(self, response, self.feature_19c0.get_capabilities_response_cls, check_map)

        self.testCaseChecked("INT_19C0_0001", _AUTHOR)
    # end def test_get_capabilities

    @features("Feature19C0")
    @level("Interface")
    def test_get_button_capabilities(self):
        """
        Validate ``GetButtonCapabilities`` normal processing

        [1] getButtonCapabilities(buttonId) -> customizableForce, defaultForce, maxForce, minForce
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetButtonCapabilities request")
        # --------------------------------------------------------------------------------------------------------------
        response = ForceSensingButtonTestUtils.HIDppHelper.get_button_capabilities(
            test_case=self,
            button_id=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetButtonCapabilitiesResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ForceSensingButtonTestUtils.ButtonCapabilitiesChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response.button_capabilities,
                             self.feature_19c0.get_button_capabilities_response_cls, check_map)

        self.testCaseChecked("INT_19C0_0002", _AUTHOR)
    # end def test_get_button_capabilities

    @features("Feature19C0")
    @level("Interface")
    def test_get_button_config(self):
        """
        Validate ``GetButtonConfig`` normal processing

        [2] getButtonConfig(buttonId) -> currentForce
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetButtonConfig request")
        # --------------------------------------------------------------------------------------------------------------
        response = ForceSensingButtonTestUtils.HIDppHelper.get_button_config(
            test_case=self,
            button_id=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetButtonConfigResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ForceSensingButtonTestUtils.GetButtonConfigResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_19c0_index)),
        })
        checker.check_fields(self, response, self.feature_19c0.get_button_config_response_cls, check_map)

        self.testCaseChecked("INT_19C0_0003", _AUTHOR)
    # end def test_get_button_config

    @features("Feature19C0")
    @level("Interface")
    def test_set_button_config(self):
        """
        Validate ``SetButtonConfig`` normal processing

        [3] setButtonConfig(buttonId, newForce) -> buttonId, currentForce
        """
        self.post_requisite_reload_nvs = True
        new_force = HexList(self.f.PRODUCT.FEATURES.COMMON.FORCE_SENSING_BUTTON.config.F_DefaultForce)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetButtonConfig request")
        # --------------------------------------------------------------------------------------------------------------
        response = ForceSensingButtonTestUtils.HIDppHelper.set_button_config(
            test_case=self,
            button_id=0,
            new_force=new_force)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetButtonConfigResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ForceSensingButtonTestUtils.SetButtonConfigResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_19c0_index)),
            "current_force": (checker.check_current_force, new_force)
        })
        checker.check_fields(self, response, self.feature_19c0.set_button_config_response_cls, check_map)

        self.testCaseChecked("INT_19C0_0004", _AUTHOR)
    # end def test_set_button_config
# end class ForceSensingButtonInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
