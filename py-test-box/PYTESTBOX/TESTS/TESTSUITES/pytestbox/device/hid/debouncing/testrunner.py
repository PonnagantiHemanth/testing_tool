#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.debouncing.testrunner
:brief: Device Hid debouncing feature testrunner implementation
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/04/29
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hid.debouncing.business import DebouncingBusinessTestCase
from pytestbox.device.hid.debouncing.functionality import DebouncingFunctionalityTestCase
from pytestbox.device.hid.debouncing.performance import DebouncePerformanceBLEProTestCase
from pytestbox.device.hid.debouncing.performance import DebouncePerformanceBLETestCase
from pytestbox.device.hid.debouncing.performance import DebouncePerformanceCrushTestCase
from pytestbox.device.hid.debouncing.performance import DebouncePerformanceLS2TestCase
from pytestbox.device.hid.debouncing.performance import DebouncePerformanceUSBTestCase


# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class DeviceHidDebouncingTestSuite(PyHarnessSuite):
    """
    Test runner class for Hid Debouncing tests
    """
    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        self.runTest(result, context, DebouncingBusinessTestCase)
        self.runTest(result, context, DebouncingFunctionalityTestCase)
        self.runTest(result, context, DebouncePerformanceLS2TestCase)
        self.runTest(result, context, DebouncePerformanceBLEProTestCase)
        self.runTest(result, context, DebouncePerformanceBLETestCase)
        self.runTest(result, context, DebouncePerformanceCrushTestCase)
        self.runTest(result, context, DebouncePerformanceUSBTestCase)
    # end def runTests
# end class DeviceHidDebouncingTestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
