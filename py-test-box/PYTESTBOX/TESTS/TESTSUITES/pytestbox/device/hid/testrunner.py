#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.testrunner
:brief: Device HID features testrunner implementation
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/04/15
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hid.debouncing.testrunner import DeviceHidDebouncingTestSuite
from pytestbox.device.hid.keyboard.testrunner import DeviceHidKeyboardTestSuite
from pytestbox.device.hid.latency.testrunner import DeviceHidLatencyTestSuite
from pytestbox.device.hid.mouse.testrunner import DeviceHidMouseTestSuite


# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class DeviceHidTestSuite(PyHarnessSuite):
    """
    Test runner class for HID tests
    """
    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        # Debouncing features
        self.runTest(result, context, DeviceHidDebouncingTestSuite)
        self.runTest(result, context, DeviceHidLatencyTestSuite)
        # Keyboard features
        self.runTest(result, context, DeviceHidKeyboardTestSuite)
        # Mouse features
        self.runTest(result, context, DeviceHidMouseTestSuite)
    # end def runTests
# end class DeviceHidTestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
