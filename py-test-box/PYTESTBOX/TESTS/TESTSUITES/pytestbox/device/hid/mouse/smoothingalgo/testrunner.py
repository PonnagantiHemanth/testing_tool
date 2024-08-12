#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.mouse.smoothingalgo.testrunner
:brief: Device Hid mouse smoothing algorithm feature testrunner implementation
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2024/07/04
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hid.mouse.smoothingalgo.business import SmoothingAlgoBusinessTestCase
from pytestbox.device.hid.mouse.smoothingalgo.functionality import SmoothingAlgoFunctionalityTestCase


# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class DeviceHidMouseSmoothingAlgoTestSuite(PyHarnessSuite):
    """
    Test runner class for Hid Mouse spurious motion filtering algorithm tests.
    """
    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, SmoothingAlgoBusinessTestCase)
        self.runTest(result, context, SmoothingAlgoFunctionalityTestCase)
    # end def runTests
# end class DeviceHidMouseSmoothingAlgoTestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
