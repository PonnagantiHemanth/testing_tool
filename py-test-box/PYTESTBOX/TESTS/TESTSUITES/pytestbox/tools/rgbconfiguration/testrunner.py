#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.tools.rgbconfiguration.testrunner
:brief: RGB configuration tools tests runner
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2023/07/20
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.tools.rgbconfiguration.rgbeffectsrecorder import RgbEffectsRecorder


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class RgbConfigurationTools(PyHarnessSuite):
    """
    Test runner class for RGB configuration tools.
    """
    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, RgbEffectsRecorder)
    # end def runTests
# end class RgbConfigurationTestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
