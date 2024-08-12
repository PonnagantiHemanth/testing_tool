#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
""" @package pytestbox.subsystem.test.testrunner
@brief  HID keyboard features testrunner implementation
@author Max Tu
@date   2019/09/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.keyboard.feature_40a3.testrunner import DeviceHidpp20Feature40A3TestSuite
from pytestbox.device.hidpp20.keyboard.feature_4220.testrunner import DeviceHidpp20Feature4220TestSuite
from pytestbox.device.hidpp20.keyboard.feature_4521.testrunner import DeviceHidpp20Feature4521TestSuite
from pytestbox.device.hidpp20.keyboard.feature_4522.testrunner import DeviceHidpp20Feature4522TestSuite
from pytestbox.device.hidpp20.keyboard.feature_4523.testrunner import DeviceHidpp20Feature4523TestSuite
from pytestbox.device.hidpp20.keyboard.feature_4531.testrunner import DeviceHidpp20Feature4531TestSuite
from pytestbox.device.hidpp20.keyboard.feature_4540.testrunner import DeviceHidpp20Feature4540TestSuite
from pytestbox.device.hidpp20.keyboard.feature_4610.testrunner import DeviceHidpp20Feature4610TestSuite


# ----------------------------------------------------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------------------------------------------------
class KeyboardHidTestSuite(PyHarnessSuite):
    """
    Test runner class for HID important tests
    """
    def runTests(self, result, context):
        """
        @copydoc pyharness.extensions.PyHarnessSuite.runTests
        """
        self.runTest(result, context, DeviceHidpp20Feature40A3TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature4220TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature4521TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature4522TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature4523TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature4531TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature4540TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature4610TestSuite)
    # end def runTests
# end class KeyboardHidTestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
