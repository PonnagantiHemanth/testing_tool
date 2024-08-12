#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.mouse.feature_2250.testrunner
:brief: HID++ 2.0 feature 0x2250 testrunner implementation
:author: Gautham S B <gsb@logitech.com>
:date: 2023/08/28
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.mouse.feature_2250.business import AnalysisModeBusinessTestCase
from pytestbox.device.hidpp20.mouse.feature_2250.errorhandling import AnalysisModeErrorHandlingTestCase
from pytestbox.device.hidpp20.mouse.feature_2250.functionality import AnalysisModeFunctionalityTestCase
from pytestbox.device.hidpp20.mouse.feature_2250.interface import AnalysisModeInterfaceTestCase
from pytestbox.device.hidpp20.mouse.feature_2250.robustness import AnalysisModeRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature2250TestSuite(PyHarnessSuite):
    """
    Define test runner suite for mouse feature 0x2250 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, AnalysisModeInterfaceTestCase)
        self.runTest(result, context, AnalysisModeBusinessTestCase)
        self.runTest(result, context, AnalysisModeFunctionalityTestCase)
        self.runTest(result, context, AnalysisModeErrorHandlingTestCase)
        self.runTest(result, context, AnalysisModeRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature2250TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
