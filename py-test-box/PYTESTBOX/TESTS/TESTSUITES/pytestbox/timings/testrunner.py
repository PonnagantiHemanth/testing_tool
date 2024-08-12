#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
@package   pytestbox.testrunner

@brief  timings tests runner

@author christophe.roquebert

@date   2019/11/27
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.timings.main_loop import MainLoopTestCase
from pytestbox.timings.main_loop import MainLoop2kHzTestCase
from pytestbox.timings.main_loop import MainLoop2kHzRFTestTestCase
from pytestbox.timings.main_loop import MainLoop2kHzUSBTestCase
from pytestbox.timings.hid_report_latency import HidLatencyTestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class TimingsTestSuite(PyHarnessSuite):
    """
    Demo tests launcher
    """

    def runTests(self, result, context):
        """
        @copydoc pyharness.extensions.PyHarnessSuite.runTests
        """
        self.runTest(result, context, MainLoopTestCase)
        self.runTest(result, context, MainLoop2kHzTestCase)
        self.runTest(result, context, MainLoop2kHzRFTestTestCase)
        self.runTest(result, context, MainLoop2kHzUSBTestCase)
        self.runTest(result, context, HidLatencyTestCase)
    # end def runTests

# end class TimingsTestSuite

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
