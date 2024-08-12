#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.latency.testrunner
:brief: Device Hid latency feature testrunner implementation
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/07/23
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hid.latency.performance import LatencyPerformance1kHzLS2TestCase
from pytestbox.device.hid.latency.performance import LatencyPerformance1kHzUSBTestCase
from pytestbox.device.hid.latency.performance import LatencyPerformance2kHzLS2TestCase
from pytestbox.device.hid.latency.performance import LatencyPerformance2kHzUSBTestCase
from pytestbox.device.hid.latency.performance import LatencyPerformance4kHzLS2TestCase
from pytestbox.device.hid.latency.performance import LatencyPerformance4kHzUSBTestCase
from pytestbox.device.hid.latency.performance import LatencyPerformance8kHzLS2TestCase
from pytestbox.device.hid.latency.performance import LatencyPerformance8kHzUSBTestCase
from pytestbox.device.hid.latency.performance import LatencyPerformanceBLEProTestCase
from pytestbox.device.hid.latency.performance import LatencyPerformanceBLETestCase
from pytestbox.device.hid.latency.performance import LatencyPerformanceCrushTestCase
from pytestbox.device.hid.latency.performance import LatencyPerformanceLS2TestCase


# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class DeviceHidLatencyTestSuite(PyHarnessSuite):
    """
    Test runner class for Hid Latency tests.
    """
    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, LatencyPerformanceLS2TestCase)
        self.runTest(result, context, LatencyPerformance1kHzLS2TestCase)
        self.runTest(result, context, LatencyPerformance2kHzLS2TestCase)
        self.runTest(result, context, LatencyPerformance4kHzLS2TestCase)
        self.runTest(result, context, LatencyPerformance8kHzLS2TestCase)
        self.runTest(result, context, LatencyPerformance1kHzUSBTestCase)
        self.runTest(result, context, LatencyPerformance2kHzUSBTestCase)
        self.runTest(result, context, LatencyPerformance4kHzUSBTestCase)
        self.runTest(result, context, LatencyPerformance8kHzUSBTestCase)
        self.runTest(result, context, LatencyPerformanceBLETestCase)
        self.runTest(result, context, LatencyPerformanceBLEProTestCase)
        self.runTest(result, context, LatencyPerformanceCrushTestCase)
    # end def runTests
# end class DeviceHidLatencyTestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
