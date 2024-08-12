#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------
"""
:package: pytestbox.hid.mouse.testrunner
:brief: HID mouse testrunner implementation
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/01/25
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.mouse.feature_2100 import VerticalScrollingTestCase
from pytestbox.device.hidpp20.mouse.feature_2110_functionality import SmartShiftFunctionalityDeviceResetTestCase
from pytestbox.device.hidpp20.mouse.feature_2110_functionality import SmartShiftFunctionalityTestCase
from pytestbox.device.hidpp20.mouse.feature_2110_interface import SmartShiftInterfaceTestCase
from pytestbox.device.hidpp20.mouse.feature_2110_robustness import SmartShiftRobustnessTestCase
from pytestbox.device.hidpp20.mouse.feature_2111.testrunner import DeviceHidpp20Feature2111TestSuite
from pytestbox.device.hidpp20.mouse.feature_2121 import HiResWheelTestCase
from pytestbox.device.hidpp20.mouse.feature_2130.testrunner import DeviceHidpp20Feature2130TestSuite
from pytestbox.device.hidpp20.mouse.feature_2150.testrunner import DeviceHidpp20Feature2150TestSuite
from pytestbox.device.hidpp20.mouse.feature_2201.testrunner import DeviceHidpp20Feature2201TestSuite
from pytestbox.device.hidpp20.mouse.feature_2202.testrunner import DeviceHidpp20Feature2202TestSuite
from pytestbox.device.hidpp20.mouse.feature_2250.testrunner import DeviceHidpp20Feature2250TestSuite
from pytestbox.device.hidpp20.mouse.feature_2251.testrunner import DeviceHidpp20Feature2251TestSuite
from pytestbox.device.hidpp20.mouse.move import XYMoveTestCase


# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class MouseHidTestSuite(PyHarnessSuite):
    """
    Test runner class for HID common tests
    """
    def runTests(self, result, context):
        # See ``pyharness.extensions.PyHarnessSuite.runTests``
        self.runTest(result, context, HiResWheelTestCase)
        self.runTest(result, context, SmartShiftInterfaceTestCase)
        self.runTest(result, context, SmartShiftFunctionalityDeviceResetTestCase)
        self.runTest(result, context, SmartShiftFunctionalityTestCase)
        self.runTest(result, context, SmartShiftRobustnessTestCase)
        self.runTest(result, context, VerticalScrollingTestCase)
        self.runTest(result, context, XYMoveTestCase)

        self.runTest(result, context, DeviceHidpp20Feature2111TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature2130TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature2150TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature2201TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature2202TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature2250TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature2251TestSuite)
    # end def runTests
# end class MouseHidTestSuite
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
