#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.mouse.displacement.testrunner
:brief: Device Hid mouse XY displacement feature testrunner implementation
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2023/01/19
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hid.mouse.displacement.business import XYDisplacementBusinessTestCase
from pytestbox.device.hid.mouse.displacement.functionality import XYDisplacementFunctionalityTestCase
from pytestbox.device.hid.mouse.displacement.performance import XYDisplacementReportRatePerformanceLSXTestCase
from pytestbox.device.hid.mouse.displacement.performance import XYDisplacementReportRatePerformanceTestCase
from pytestbox.device.hid.mouse.displacement.performance import XYDisplacementReportRatePerformanceUSBTestCase


# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class DeviceHidMouseDisplacementTestSuite(PyHarnessSuite):
    """
    Test runner class for Hid Mouse XY Displacement tests.
    """
    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, XYDisplacementBusinessTestCase)
        self.runTest(result, context, XYDisplacementFunctionalityTestCase)
        self.runTest(result, context, XYDisplacementReportRatePerformanceTestCase)
        self.runTest(result, context, XYDisplacementReportRatePerformanceLSXTestCase)
        self.runTest(result, context, XYDisplacementReportRatePerformanceUSBTestCase)
    # end def runTests
# end class DeviceHidMouseDisplacementTestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
