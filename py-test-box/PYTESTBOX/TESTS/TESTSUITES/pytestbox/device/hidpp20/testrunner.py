#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.device.hidpp20.testrunner
    :brief: Device HID++ 2.0 features testrunner implementation
    :author: Christophe Roquebert
    :date: 2020/03/26
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.testrunner import DeviceCommonHidpp20TestSuite
from pytestbox.device.hidpp20.emulator.testrunner import EmulatorTestSuite
from pytestbox.device.hidpp20.gaming.testrunner import GamingHidTestSuite
from pytestbox.device.hidpp20.important.testrunner import DeviceImportantHidpp20TestSuite
from pytestbox.device.hidpp20.keyboard.testrunner import KeyboardHidTestSuite
from pytestbox.device.hidpp20.mouse.testrunner import MouseHidTestSuite
from pytestbox.device.hidpp20.peripheral.testrunner import DeviceHidpp20PeripheralTestSuite
from pytestbox.device.hidpp20.touchpad.testrunner import TouchpadHidpp20TestSuite


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceHidpp20TestSuite(PyHarnessSuite):
    """
    Test runner class for HID++ 2.0 common tests
    """
    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        # Important HID++ features
        self.runTest(result, context, DeviceImportantHidpp20TestSuite)

        # Common HID++ features
        self.runTest(result, context, DeviceCommonHidpp20TestSuite)

        # Mouse HID++ features
        self.runTest(result, context, MouseHidTestSuite)

        # Keyboard HID++ features
        self.runTest(result, context, KeyboardHidTestSuite)

        # Touchpad HID++ features
        self.runTest(result, context, TouchpadHidpp20TestSuite)

        # Gaming Devices HID++ features
        self.runTest(result, context, GamingHidTestSuite)

        # Peripheral Devices HID++ features
        self.runTest(result, context, DeviceHidpp20PeripheralTestSuite)

        # --------------
        # Emulator
        # --------------
        self.runTest(result, context, EmulatorTestSuite)
    # end def runTests
# end class DeviceHidpp20TestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
