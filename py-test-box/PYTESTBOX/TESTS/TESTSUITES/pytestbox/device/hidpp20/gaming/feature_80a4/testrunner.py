#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_80a4.testrunner
:brief: HID++ 2.0 feature 0x80a4 testrunner implementation
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/06/04
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.gaming.feature_80a4.business import AxisResponseCurveBusinessTestCase
from pytestbox.device.hidpp20.gaming.feature_80a4.errorhandling import AxisResponseCurveErrorHandlingTestCase
from pytestbox.device.hidpp20.gaming.feature_80a4.functionality import AxisResponseCurveFunctionalityTestCase
from pytestbox.device.hidpp20.gaming.feature_80a4.interface import AxisResponseCurveInterfaceTestCase
from pytestbox.device.hidpp20.gaming.feature_80a4.robustness import AxisResponseCurveRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature80A4TestSuite(PyHarnessSuite):
    """
    Define test runner suite for gaming feature 0x80A4 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, AxisResponseCurveInterfaceTestCase)
        self.runTest(result, context, AxisResponseCurveBusinessTestCase)
        self.runTest(result, context, AxisResponseCurveFunctionalityTestCase)
        self.runTest(result, context, AxisResponseCurveErrorHandlingTestCase)
        self.runTest(result, context, AxisResponseCurveRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature80A4TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
