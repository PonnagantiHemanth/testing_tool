#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.doublepress.testrunner
:brief: Device Hid keyboard double press feature testrunner implementation
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2023/05/12
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hid.keyboard.doublepress.business import DoublePressBusinessTestCase
from pytestbox.device.hid.keyboard.doublepress.functionality import DoublePressFunctionalityTestCase
from pytestbox.device.hid.keyboard.doublepress.timings import DoublePressTimingsTestCase


# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class DeviceHidKeyboardDoublePressTestSuite(PyHarnessSuite):
    """
    Test runner class for Hid Keyboard Double Press translation tests.
    """
    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, DoublePressBusinessTestCase)
        self.runTest(result, context, DoublePressFunctionalityTestCase)
        self.runTest(result, context, DoublePressTimingsTestCase)
    # end def runTests
# end class DeviceHidKeyboardDoublePressTestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
