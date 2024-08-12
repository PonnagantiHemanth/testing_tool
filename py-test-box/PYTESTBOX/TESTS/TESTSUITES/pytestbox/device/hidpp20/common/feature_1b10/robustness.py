#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1b10.robustness
:brief: HID++ 2.0 ``ControlList`` robustness test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2023/06/09
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.common.controllist import ControlList
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.controllistutils import ControlListTestUtils
from pytestbox.device.hidpp20.common.feature_1b10.controllist import ControlListTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ControlListRobustnessTestCase(ControlListTestCase):
    """
    Validate ``ControlList`` robustness test cases
    """

    @features("Feature1B10")
    @level("Robustness")
    def test_get_count_software_id(self):
        """
        Validate ``GetCount`` software id field is ignored by the firmware

        [0] getCount() -> count

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ControlList.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCount request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ControlListTestUtils.HIDppHelper.get_count(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCountResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ControlListTestUtils.GetCountResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_1b10.get_count_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1B10_0001#1", _AUTHOR)
    # end def test_get_count_software_id

    @features("Feature1B10")
    @level("Robustness")
    def test_get_control_list_software_id(self):
        """
        Validate ``GetControlList`` software id field is ignored by the firmware

        [1] getControlList(offset) -> cid0, cid1, cid2, cid3, cid4, cid5, cid6, cid7

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.Offset.0xPP.0xPP

        SwID boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ControlList.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetControlList request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ControlListTestUtils.HIDppHelper.get_control_list(
                test_case=self,
                offset=0,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetControlListResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ControlListTestUtils.GetControlListResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_1b10.get_control_list_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1B10_0001#2", _AUTHOR)
    # end def test_get_control_list_software_id

    @features("Feature1B10")
    @level("Robustness")
    def test_get_count_padding(self):
        """
        Validate ``GetCount`` padding bytes are ignored by the firmware

        [0] getCount() -> count

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1b10.get_count_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCount request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = ControlListTestUtils.HIDppHelper.get_count(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCountResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ControlListTestUtils.GetCountResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_1b10.get_count_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1B10_0002#1", _AUTHOR)
    # end def test_get_count_padding

    @features("Feature1B10")
    @level("Robustness")
    def test_get_control_list_padding(self):
        """
        Validate ``GetControlList`` padding bytes are ignored by the firmware

        [1] getControlList(offset) -> cid0, cid1, cid2, cid3, cid4, cid5, cid6, cid7

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.Offset.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1b10.get_control_list_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetControlList request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = ControlListTestUtils.HIDppHelper.get_control_list(
                test_case=self,
                offset=0,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetControlListResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ControlListTestUtils.GetControlListResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_1b10.get_control_list_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1B10_0002#2", _AUTHOR)
    # end def test_get_control_list_padding
# end class ControlListRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
