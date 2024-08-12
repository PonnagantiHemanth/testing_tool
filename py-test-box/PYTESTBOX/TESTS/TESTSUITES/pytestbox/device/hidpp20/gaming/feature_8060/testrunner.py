#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.1'
:package: pytestbox.device.hidpp20.gaming.feature_8060.testrunner
:brief: HID++ 2.0 feature 0x8060 testrunner implementation
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2022/08/12
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.gaming.feature_8060.business import ReportRateBusinessTestCase
from pytestbox.device.hidpp20.gaming.feature_8060.errorhandling import ReportRateErrorHandlingTestCase
from pytestbox.device.hidpp20.gaming.feature_8060.functionality import ReportRateFunctionalityTestCase
from pytestbox.device.hidpp20.gaming.feature_8060.interface import ReportRateInterfaceTestCase
from pytestbox.device.hidpp20.gaming.feature_8060.robustness import ReportRateRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature8060TestSuite(PyHarnessSuite):
    """
    Define test runner suite for gaming feature 0x8060 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, ReportRateInterfaceTestCase)
        self.runTest(result, context, ReportRateBusinessTestCase)
        self.runTest(result, context, ReportRateFunctionalityTestCase)
        self.runTest(result, context, ReportRateErrorHandlingTestCase)
        self.runTest(result, context, ReportRateRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature8060TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
