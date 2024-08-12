#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1f30.testrunner
:brief: HID++ 2.0 feature 0x1f30 testrunner implementation
:author: Sanjib Hazra <shazra@logitech.com>
:date: 2021/03/25
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_1f30.errorhandling import TemperatureMeasurementErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_1f30.functionality import TemperatureMeasurementFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_1f30.interface import TemperatureMeasurementInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_1f30.robustness import TemperatureMeasurementRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature1F30TestSuite(PyHarnessSuite):
    """
    Test runner class for common feature 0x1F30 tests
    """
    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        self.runTest(result, context, TemperatureMeasurementInterfaceTestCase)
        self.runTest(result, context, TemperatureMeasurementFunctionalityTestCase)
        self.runTest(result, context, TemperatureMeasurementErrorHandlingTestCase)
        self.runTest(result, context, TemperatureMeasurementRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature1F30TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
