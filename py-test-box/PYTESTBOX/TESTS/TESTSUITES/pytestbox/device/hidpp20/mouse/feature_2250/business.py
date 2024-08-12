#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.mouse.feature_2250.business
:brief: HID++ 2.0 ``AnalysisMode`` business test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2023/08/28
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import randint

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.mouse.analysismode import AnalysisMode
from pylibrary.tools.hexlist import HexList
from pytestbox.base.channelutils import ChannelUtils
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
class AnalysisModeBusinessTestCase(AnalysisModeTestCase):
    """
    Validate ``AnalysisMode`` business test cases
    """

    @features('Feature2250')
    @level('Business', 'SmokeTests')
    @services('OpticalSensor')
    def test_analysis_data(self):
        """
        Validate GetAnalysisData Business case sequence
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Empty Analysis Data buffers')
        # --------------------------------------------------------------------------------------------------------------
        AnalysisModeTestUtils.HIDppHelper.get_analysis_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Clear the pending HID Mouse messages')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send SetAnalysisMode request with mode parameter as ON')
        # --------------------------------------------------------------------------------------------------------------
        AnalysisModeTestUtils.HIDppHelper.set_analysis_mode(self, AnalysisMode.MODE.ON)

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
                "mode": (checker.check_mode, AnalysisMode.MODE.ON)
            }
        )
        checker.check_fields(self, response, self.feature_2250.get_analysis_mode_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Provide stimuli to generate a displacement on X and Y')
        # --------------------------------------------------------------------------------------------------------------
        x, y = randint(1, 16), randint(1, 16)
        self.emulate_continuous_motion(self, x, y)
        self.emulate_continuous_motion(self, -x, -y)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetAnalysisData request')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.get_analysis_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check GetAnalysisDataResponse fields')
        # --------------------------------------------------------------------------------------------------------------
        # Retrieve X and Y displacement from the HID mouse interface
        expected_counters = HexList(self.compute_cumulative_displacement(self))

        checker = AnalysisModeTestUtils.GetAnalysisDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "data": (checker.check_data, expected_counters)
            }
        )
        checker.check_fields(self, response, self.feature_2250.get_analysis_data_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send SetAnalysisMode request with mode parameter as OFF')
        # --------------------------------------------------------------------------------------------------------------
        AnalysisModeTestUtils.HIDppHelper.set_analysis_mode(self, AnalysisMode.MODE.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetAnalysisMode request')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.get_analysis_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check GetAnalysisModeResponse fields')
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalysisModeTestUtils.GetAnalysisModeResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_2250.get_analysis_mode_response_cls, check_map)

        self.testCaseChecked("BUS_2250_0001")
    # end def test_analysis_data
# end class AnalysisModeBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
