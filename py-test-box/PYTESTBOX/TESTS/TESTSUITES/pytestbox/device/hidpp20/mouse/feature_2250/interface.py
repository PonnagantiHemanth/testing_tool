#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.mouse.feature_2250.interface
:brief: HID++ 2.0 ``AnalysisMode`` interface test suite
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
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.analysismodeutils import AnalysisModeTestUtils
from pytestbox.device.hidpp20.mouse.feature_2250.analysismode import AnalysisModeTestCase


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AnalysisModeInterfaceTestCase(AnalysisModeTestCase):
    """
    Validate ``AnalysisMode`` interface test cases
    """

    @features('Feature2250')
    @level('Interface')
    def test_get_analysis_mode(self):
        """
        Validate GetAnalysisMode normal processing (Feature 0x2250)

        [0] getAnalysisMode() -> mode (version 0)
        [0] getAnalysisMode() -> mode, capabilities (version 1)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetAnalysisMode request')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.get_analysis_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check GetAnalysisModeResponse fields')
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalysisModeTestUtils.GetAnalysisModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "device_index": (checker.check_device_index, HexList(self.original_device_index)),
                "feature_index": (checker.check_feature_index, HexList(self.feature_2250_index)),
            }
        )
        checker.check_fields(self, response, self.feature_2250.get_analysis_mode_response_cls, check_map)

        self.testCaseChecked("INT_2250_0001")
    # end def test_get_analysis_mode

    @features('Feature2250')
    @level('Interface')
    def test_set_analysis_mode(self):
        """
        Validate ``SetAnalysisMode`` normal processing

        [1] setAnalysisMode(mode) -> mode
        """
        off = AnalysisMode.MODE.OFF
        on = AnalysisMode.MODE.ON
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send SetAnalysisMode request with mode parameter as ON')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.set_analysis_mode(self, on)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check SetAnalysisModeResponse fields')
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalysisModeTestUtils.SetAnalysisModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "device_index": (checker.check_device_index, HexList(self.original_device_index)),
                "feature_index": (checker.check_feature_index, HexList(self.feature_2250_index)),
                "mode": (checker.check_mode, on)
            }
        )
        checker.check_fields(self, response, self.feature_2250.set_analysis_mode_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send SetAnalysisMode request with mode parameter as OFF')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.set_analysis_mode(self, off)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check SetAnalysisModeResponse fields')
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalysisModeTestUtils.SetAnalysisModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "device_index": (checker.check_device_index, HexList(self.original_device_index)),
                "feature_index": (checker.check_feature_index, HexList(self.feature_2250_index)),
                "mode": (checker.check_mode, off)
            }
        )
        checker.check_fields(self, response, self.feature_2250.set_analysis_mode_response_cls, check_map)

        self.testCaseChecked("INT_2250_0002")
    # end def test_set_analysis_mode

    @features('Feature2250')
    @level('Interface')
    def test_get_analysis_data(self):
        """
        Validate ``GetAnalysisData`` normal processing

        [2] getAnalysisData() -> data
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetAnalysisData request')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.get_analysis_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check GetAnalysisDataResponse fields')
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalysisModeTestUtils.GetAnalysisDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "device_index": (checker.check_device_index, HexList(self.original_device_index)),
                "feature_index": (checker.check_feature_index, HexList(self.feature_2250_index)),
            }
        )
        checker.check_fields(self, response, self.feature_2250.get_analysis_data_response_cls, check_map)

        self.testCaseChecked("INT_2250_0003")
    # end def test_get_analysis_data
# end class AnalysisModeInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
