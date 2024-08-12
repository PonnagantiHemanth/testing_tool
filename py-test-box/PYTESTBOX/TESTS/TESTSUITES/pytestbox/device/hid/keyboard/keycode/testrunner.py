#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.keycode.testrunner
:brief: Device Hid keyboard keycode feature testrunner implementation
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/04/22
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hid.keyboard.keycode.business import KeyCodeBusinessTestCase
from pytestbox.device.hid.keyboard.keycode.functionality import KeyCodeFunctionalityTestCase
from pytestbox.device.hid.keyboard.keycode.robustness import KeyCodeRobustnessTestCase
from pytestbox.device.hid.keyboard.keycode.timing import KeyCodeTimingTestCase


# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class DeviceHidKeyboardKeyCodeTestSuite(PyHarnessSuite):
    """
    Test runner class for Hid Keyboard KeyCode translation tests.
    """
    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, KeyCodeBusinessTestCase)
        self.runTest(result, context, KeyCodeFunctionalityTestCase)
        self.runTest(result, context, KeyCodeRobustnessTestCase)
        self.runTest(result, context, KeyCodeTimingTestCase)
    # end def runTests
# end class DeviceHidKeyboardKeyCodeTestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
