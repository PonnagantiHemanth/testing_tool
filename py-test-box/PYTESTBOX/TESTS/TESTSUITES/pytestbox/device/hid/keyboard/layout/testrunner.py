#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.layout.testrunner
:brief: Device Hid keyboard layout feature testrunner implementation
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/07/26
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hid.keyboard.layout.business import LayoutBusinessTestCase
from pytestbox.device.hid.keyboard.layout.functionality import LayoutFunctionalityTestCase


# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class DeviceHidKeyboardLayoutTestSuite(PyHarnessSuite):
    """
    Test runner class for Hid Keyboard Layout tests.
    """
    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, LayoutBusinessTestCase)
        self.runTest(result, context, LayoutFunctionalityTestCase)
    # end def runTests
# end class DeviceHidKeyboardLayoutTestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
