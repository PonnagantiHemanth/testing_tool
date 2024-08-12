#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.testrunner
:brief: Device Hid keyboard features testrunner implementation
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/04/15
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hid.keyboard.analogkeys.testrunner import DeviceKeyboardAnalogKeysTestSuite
from pytestbox.device.hid.keyboard.doublepress.testrunner import DeviceHidKeyboardDoublePressTestSuite
from pytestbox.device.hid.keyboard.fkc.testrunner import DeviceHidKeyboardFKCTestSuite
from pytestbox.device.hid.keyboard.ghostkeys.testrunner import DeviceHidKeyboardGhostKeysTestSuite
from pytestbox.device.hid.keyboard.keycode.testrunner import DeviceHidKeyboardKeyCodeTestSuite
from pytestbox.device.hid.keyboard.layout.testrunner import DeviceHidKeyboardLayoutTestSuite
from pytestbox.device.hid.keyboard.sholo.testrunner import DeviceHidKeyboardSholoTestSuite
from pytestbox.device.hid.keyboard.typing.testrunner import DeviceHidKeyboardTypingTestSuite


# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class DeviceHidKeyboardTestSuite(PyHarnessSuite):
    """
    Test runner class for Hid Keyboard tests.
    """
    def runTests(self, result, context):
        """
        Run all the tests in the test suite.

        :param result: The test result that will collect the results.
        :type result: ``TestResult``
        :param context: The context in which the tests are run.
        :type context: ``Context``
        """
        # Hid Keyboard features
        self.runTest(result, context, DeviceHidKeyboardDoublePressTestSuite)
        self.runTest(result, context, DeviceHidKeyboardFKCTestSuite)
        self.runTest(result, context, DeviceKeyboardAnalogKeysTestSuite)
        self.runTest(result, context, DeviceHidKeyboardGhostKeysTestSuite)
        self.runTest(result, context, DeviceHidKeyboardKeyCodeTestSuite)
        self.runTest(result, context, DeviceHidKeyboardLayoutTestSuite)
        self.runTest(result, context, DeviceHidKeyboardSholoTestSuite)
        self.runTest(result, context, DeviceHidKeyboardTypingTestSuite)
    # end def runTests
# end class DeviceHidKeyboardTestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
