#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.typing.testrunner
:brief: Device Hid keyboard typing feature testrunner implementation
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/04/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hid.keyboard.typing.business import TypingBusinessTestCase
from pytestbox.device.hid.keyboard.typing.functionality import TypingFunctionalityTestCase


# ----------------------------------------------------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidKeyboardTypingTestSuite(PyHarnessSuite):
    """
    Test runner class for Hid Keyboard typing tests.
    """
    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, TypingBusinessTestCase)
        self.runTest(result, context, TypingFunctionalityTestCase)
    # end def runTests
# end class DeviceHidKeyboardTypingTestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
