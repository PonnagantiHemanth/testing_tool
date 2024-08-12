#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1801.robustness
:brief: HID++ 2.0 ``ManufacturingMode`` robustness test suite
:author: Masan Xu <mxu11@logitech.com>
:date: 2023/06/14
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.common.manufacturingmode import ManufacturingMode
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.manufacturingmodeutils import ManufacturingModeTestUtils
from pytestbox.device.hidpp20.common.feature_1801.manufacturingmode import ManufacturingModeTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Masan Xu"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class ManufacturingModeRobustnessTestCase(ManufacturingModeTestCase):
    """
    Validate ``ManufacturingMode`` robustness test cases
    """

    @features("Feature1801")
    @level("Robustness")
    def test_set_manufacturing_mode_software_id(self):
        """
        Validate ``SetManufacturingMode`` software id field is ignored by the firmware

        [0] setManufacturingMode(manufacturingMode) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.ManufacturingMode.0xPP.0xPP

        SwID boundary values [0..F]
        """
        manufacturing_mode = False
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ManufacturingMode.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetManufacturingMode request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ManufacturingModeTestUtils.HIDppHelper.set_manufacturing_mode(
                test_case=self,
                manufacturing_mode=manufacturing_mode,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetManufacturingModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ManufacturingModeTestUtils.MessageChecker.check_fields(
                self, response, self.feature_1801.set_manufacturing_mode_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1801_0001#1", _AUTHOR)
    # end def test_set_manufacturing_mode_software_id

    @features("Feature1801")
    @level("Robustness")
    def test_get_manufacturing_mode_software_id(self):
        """
        Validate ``GetManufacturingMode`` software id field is ignored by the firmware

        [1] getManufacturingMode() -> manufacturingMode

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        manufacturing_mode = False
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ManufacturingMode.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetManufacturingMode request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ManufacturingModeTestUtils.HIDppHelper.get_manufacturing_mode(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetManufacturingModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ManufacturingModeTestUtils.GetManufacturingModeResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "manufacturing_mode": (checker.check_manufacturing_mode, manufacturing_mode)
            })
            checker.check_fields(self, response, self.feature_1801.get_manufacturing_mode_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1801_0001#2", _AUTHOR)
    # end def test_get_manufacturing_mode_software_id

    @features("Feature1801")
    @level("Robustness")
    def test_set_manufacturing_mode_padding(self):
        """
        Validate ``SetManufacturingMode`` padding bytes are ignored by the firmware

        [0] setManufacturingMode(manufacturingMode) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.ManufacturingMode.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        manufacturing_mode = False
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1801.set_manufacturing_mode_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetManufacturingMode request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = ManufacturingModeTestUtils.HIDppHelper.set_manufacturing_mode(
                test_case=self,
                manufacturing_mode=manufacturing_mode,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetManufacturingModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ManufacturingModeTestUtils.MessageChecker.check_fields(
                self, response, self.feature_1801.set_manufacturing_mode_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1801_0002#1", _AUTHOR)
    # end def test_set_manufacturing_mode_padding

    @features("Feature1801")
    @level("Robustness")
    def test_get_manufacturing_mode_padding(self):
        """
        Validate ``GetManufacturingMode`` padding bytes are ignored by the firmware

        [1] getManufacturingMode() -> manufacturingMode

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        manufacturing_mode = False
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1801.get_manufacturing_mode_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetManufacturingMode request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = ManufacturingModeTestUtils.HIDppHelper.get_manufacturing_mode(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetManufacturingModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ManufacturingModeTestUtils.GetManufacturingModeResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "manufacturing_mode": (checker.check_manufacturing_mode, manufacturing_mode)
            })
            checker.check_fields(self, response, self.feature_1801.get_manufacturing_mode_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1801_0002#2", _AUTHOR)
    # end def test_get_manufacturing_mode_padding
# end class ManufacturingModeRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
