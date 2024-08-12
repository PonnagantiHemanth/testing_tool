#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.mouse.feature_2250.robustness
:brief: HID++ 2.0 ``AnalysisMode`` robustness test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2023/08/28
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.mouse.analysismode import AnalysisMode
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.analysismodeutils import AnalysisModeTestUtils
from pytestbox.device.hidpp20.mouse.feature_2250.analysismode import AnalysisModeTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AnalysisModeRobustnessTestCase(AnalysisModeTestCase):
    """
    Validate ``AnalysisMode`` robustness test cases
    """

    @features("Feature2250")
    @level("Robustness")
    def test_get_analysis_mode_software_id(self):
        """
        Validate ``GetAnalysisMode`` software id field is ignored by the firmware

        [0] getAnalysisMode() -> mode

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(AnalysisMode.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetAnalysisMode request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = AnalysisModeTestUtils.HIDppHelper.get_analysis_mode(test_case=self,
                                                                           software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetAnalysisModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AnalysisModeTestUtils.GetAnalysisModeResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_2250.get_analysis_mode_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2250_0001#1")
    # end def test_get_analysis_mode_software_id

    @features("Feature2250")
    @level("Robustness")
    def test_set_analysis_mode_software_id(self):
        """
        Validate ``SetAnalysisMode`` software id field is ignored by the firmware

        [1] setAnalysisMode(mode) -> mode

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.mode.0xPP.0xPP

        SwID boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(AnalysisMode.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetAnalysisMode request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = AnalysisModeTestUtils.HIDppHelper.set_analysis_mode(test_case=self, mode=AnalysisMode.MODE.OFF,
                                                                           software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetAnalysisModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AnalysisModeTestUtils.SetAnalysisModeResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_2250.set_analysis_mode_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2250_0001#2")
    # end def test_set_analysis_mode_software_id

    @features("Feature2250")
    @level("Robustness")
    def test_get_analysis_data_software_id(self):
        """
        Validate ``GetAnalysisData`` software id field is ignored by the firmware

        [2] getAnalysisData() -> data

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(AnalysisMode.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetAnalysisData request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = AnalysisModeTestUtils.HIDppHelper.get_analysis_data(self, software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetAnalysisDataResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AnalysisModeTestUtils.GetAnalysisDataResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_2250.get_analysis_data_response_cls, check_map)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2250_0001#3")
    # end def test_get_analysis_data_software_id

    @features("Feature2250")
    @level("Robustness")
    def test_get_analysis_mode_padding(self):
        """
        Validate ``GetAnalysisMode`` padding bytes are ignored by the firmware

        [0] getAnalysisMode() -> mode

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_2250.get_analysis_mode_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetAnalysisMode request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = AnalysisModeTestUtils.HIDppHelper.get_analysis_mode(self, padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetAnalysisModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AnalysisModeTestUtils.GetAnalysisModeResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_2250.get_analysis_mode_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2250_0002#1")
    # end def test_get_analysis_mode_padding

    @features("Feature2250")
    @level("Robustness")
    def test_set_analysis_mode_padding(self):
        """
        Validate ``SetAnalysisMode`` padding bytes are ignored by the firmware

        [1] setAnalysisMode(mode) -> mode

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.mode.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_2250.set_analysis_mode_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetAnalysisMode request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = AnalysisModeTestUtils.HIDppHelper.set_analysis_mode(
                self, mode=AnalysisMode.MODE.OFF, padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetAnalysisModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AnalysisModeTestUtils.SetAnalysisModeResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_2250.set_analysis_mode_response_cls, check_map)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2250_0002#2")
    # end def test_set_analysis_mode_padding

    @features("Feature2250")
    @level("Robustness")
    def test_get_analysis_data_padding(self):
        """
        Validate ``GetAnalysisData`` padding bytes are ignored by the firmware

        [2] getAnalysisData() -> data

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_2250.get_analysis_data_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetAnalysisData request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = AnalysisModeTestUtils.HIDppHelper.get_analysis_data(self, padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetAnalysisDataResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AnalysisModeTestUtils.GetAnalysisDataResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_2250.get_analysis_data_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2250_0002#3")
    # end def test_get_analysis_data_padding
# end class AnalysisModeRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
