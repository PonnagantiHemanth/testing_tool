#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.gaming.feature_8061.testrunner
:brief: HID++ 2.0 feature 0x8061 testrunner implementation
:author: YY Liu <yliu5@logitech.com>
:date: 2022/05/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.gaming.feature_8061.business import ExtendedAdjustableReportRateBusinessTestCase
from pytestbox.device.hidpp20.gaming.feature_8061.errorhandling import ExtendedAdjustableReportRateErrorHandlingTestCase
from pytestbox.device.hidpp20.gaming.feature_8061.functionality import ExtendedAdjustableReportRateFunctionalityTestCase
from pytestbox.device.hidpp20.gaming.feature_8061.interface import ExtendedAdjustableReportRateInterfaceTestCase
from pytestbox.device.hidpp20.gaming.feature_8061.robustness import ExtendedAdjustableReportRateRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature8061TestSuite(PyHarnessSuite):
    """
    Define test runner suite for gaming feature 0x8061 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, ExtendedAdjustableReportRateInterfaceTestCase)
        self.runTest(result, context, ExtendedAdjustableReportRateBusinessTestCase)
        self.runTest(result, context, ExtendedAdjustableReportRateFunctionalityTestCase)
        self.runTest(result, context, ExtendedAdjustableReportRateErrorHandlingTestCase)
        self.runTest(result, context, ExtendedAdjustableReportRateRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature8061TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
