#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1801.interface
:brief: HID++ 2.0 ``ManufacturingMode`` interface test suite
:author: Masan Xu <mxu11@logitech.com>
:date: 2023/06/14
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.manufacturingmodeutils import ManufacturingModeTestUtils
from pytestbox.device.hidpp20.common.feature_1801.manufacturingmode import ManufacturingModeTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Masan Xu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class ManufacturingModeInterfaceTestCase(ManufacturingModeTestCase):
    """
    Validate ``ManufacturingMode`` interface test cases
    """

    @features("Feature1801")
    @level("Interface")
    def test_set_manufacturing_mode(self):
        """
        Validate ``SetManufacturingMode`` normal processing

        [0] setManufacturingMode(manufacturingMode) -> None
        """
        manufacturing_mode = False
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetManufacturingMode request")
        # --------------------------------------------------------------------------------------------------------------
        response = ManufacturingModeTestUtils.HIDppHelper.set_manufacturing_mode(
            test_case=self,
            manufacturing_mode=manufacturing_mode)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetManufacturingModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ManufacturingModeTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_1801_index))
        }
        checker.check_fields(self, response, self.feature_1801.set_manufacturing_mode_response_cls, check_map)

        self.testCaseChecked("INT_1801_0001", _AUTHOR)
    # end def test_set_manufacturing_mode

    @features("Feature1801")
    @level("Interface")
    def test_get_manufacturing_mode(self):
        """
        Validate ``GetManufacturingMode`` normal processing

        [1] getManufacturingMode() -> manufacturingMode
        """
        manufacturing_mode = False
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetManufacturingMode request")
        # --------------------------------------------------------------------------------------------------------------
        response = ManufacturingModeTestUtils.HIDppHelper.get_manufacturing_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetManufacturingModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ManufacturingModeTestUtils.GetManufacturingModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_1801_index)),
            "manufacturing_mode": (checker.check_manufacturing_mode, manufacturing_mode)
        })
        checker.check_fields(self, response, self.feature_1801.get_manufacturing_mode_response_cls, check_map)

        self.testCaseChecked("INT_1801_0002", _AUTHOR)
    # end def test_get_manufacturing_mode
# end class ManufacturingModeInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
