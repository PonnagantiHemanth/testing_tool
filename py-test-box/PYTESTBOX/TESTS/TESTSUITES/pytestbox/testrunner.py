#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
""" @package   pytestbox.testrunner

@brief  demo tests runner

@author christophe.roquebert

@date   2018/11/17
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class DemoTestSuite(PyHarnessSuite):
    """
    Demo tests launcher
    """

    def runTests(self, result, context):
        """
        @copydoc pyharness.extensions.PyHarnessSuite.runTests
        """
        from pytestbox.device.testrunner import DeviceTestSuite
        self.runTest(result, context, DeviceTestSuite)

        from pytestbox.emulator.testrunner import EmulatorTestSuite
        self.runTest(result, context, EmulatorTestSuite)

        from pytestbox.timings.testrunner import TimingsTestSuite
        self.runTest(result, context, TimingsTestSuite)

        from pytestbox.receiver.testrunner import ReceiverTestSuite
        self.runTest(result, context, ReceiverTestSuite)

        from pytestbox.tools.testrunner import ToolsTestSuite
        self.runTest(result, context, ToolsTestSuite)
    # end def runTests

# end class ScTestRunner

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
