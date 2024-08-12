#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1861.testrunner
:brief: Device HID++ 2.0 Common feature 0x1861 testrunner implementation
:author: Christophe Roquebert
:date: 2021/04/06
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_1861.business import BatteryLevelsCalibrationBusinessTestCase
from pytestbox.device.hidpp20.common.feature_1861.errorhandling import BatteryLevelsCalibrationErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_1861.functionality import BatteryLevelsCalibrationFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_1861.interface import BatteryLevelsCalibrationInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_1861.robustness import BatteryLevelsCalibrationRobustnessTestCase


# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class DeviceHidpp20Feature1861TestSuite(PyHarnessSuite):
    """
    Test runner class for HID++ 2.0 feature 0x1861 tests
    """
    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        self.runTest(result, context, BatteryLevelsCalibrationBusinessTestCase)
        self.runTest(result, context, BatteryLevelsCalibrationErrorHandlingTestCase)
        self.runTest(result, context, BatteryLevelsCalibrationFunctionalityTestCase)
        self.runTest(result, context, BatteryLevelsCalibrationInterfaceTestCase)
        self.runTest(result, context, BatteryLevelsCalibrationRobustnessTestCase)

    # end def runTests
# end class DeviceHidpp20Feature1861TestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
