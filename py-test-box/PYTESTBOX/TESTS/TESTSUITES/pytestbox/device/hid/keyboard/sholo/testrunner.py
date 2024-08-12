#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.sholo.testrunner
:brief: Device Hid keyboard sholo feature testrunner implementation
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/07/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hid.keyboard.sholo.business import SholoBusinessTestCase
from pytestbox.device.hid.keyboard.sholo.functionality import SholoFunctionalityTestCase
from pytestbox.device.hid.keyboard.sholo.robustness import SholoRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidKeyboardSholoTestSuite(PyHarnessSuite):
    """
    Test runner class for Hid Keyboard short/long key press detection tests.
    """
    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, SholoBusinessTestCase)
        self.runTest(result, context, SholoFunctionalityTestCase)
        self.runTest(result, context, SholoRobustnessTestCase)
    # end def runTests
# end class DeviceHidKeyboardSholoTestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
