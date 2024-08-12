#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1801.functionality
:brief: HID++ 2.0 ``ManufacturingMode`` functionality test suite
:author: Masan Xu <mxu11@logitech.com>
:date: 2023/12/28
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
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
class ManufacturingModeFunctionalityTestCase(ManufacturingModeTestCase):
    """
    Validate ``ManufacturingMode`` functionality test cases
    """

    @features("Feature1801")
    @level("Functionality")
    def test_en_dis_manufacturing_mode(self):
        """
        SetManufacturingMode is able to enable/disable manufacturing mode
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable manufacturingMode by SetManufacturingMode request with manufacturingMode=1")
        # --------------------------------------------------------------------------------------------------------------
        ManufacturingModeTestUtils.HIDppHelper.set_manufacturing_mode(test_case=self, manufacturing_mode=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get manufacturingMode by GetManufacturingMode request")
        # --------------------------------------------------------------------------------------------------------------
        response = ManufacturingModeTestUtils.HIDppHelper.get_manufacturing_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check manufacturingMode is enable from GetManufacturingMode response with"
                                  "manufacturingMode=1")
        # --------------------------------------------------------------------------------------------------------------
        checker = ManufacturingModeTestUtils.GetManufacturingModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "manufacturing_mode": (checker.check_manufacturing_mode, True)
        })
        checker.check_fields(self, response, self.feature_1801.get_manufacturing_mode_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Disable manufacturingMode by SetManufacturingMode request with manufacturingMode=0")
        # --------------------------------------------------------------------------------------------------------------
        ManufacturingModeTestUtils.HIDppHelper.set_manufacturing_mode(test_case=self, manufacturing_mode=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get manufacturingMode by GetManufacturingMode request")
        # --------------------------------------------------------------------------------------------------------------
        response = ManufacturingModeTestUtils.HIDppHelper.get_manufacturing_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check manufacturingMode is disable from GetManufacturingMode response with"
                                  "manufacturingMode=0")
        # --------------------------------------------------------------------------------------------------------------
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "manufacturing_mode": (checker.check_manufacturing_mode, False)
        })
        checker.check_fields(self, response, self.feature_1801.get_manufacturing_mode_response_cls, check_map)

        self.testCaseChecked("FUN_1801_0001", _AUTHOR)
    # end def test_en_dis_manufacturing_mode
# end class ManufacturingModeFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
