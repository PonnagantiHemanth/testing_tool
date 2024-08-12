#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.common.feature_1e30.testrunner
:brief: HID++ 2.0 feature 0x1e30 testrunner implementation
:author: YY Liu <yliu5@logitech.com>
:date: 2022/12/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_1e30.errorhandling import I2CDirectAccessErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_1e30.functionality import I2CDirectAccessFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_1e30.interface import I2CDirectAccessInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_1e30.robustness import I2CDirectAccessRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature1E30TestSuite(PyHarnessSuite):
    """
    Define test runner suite for common feature 0x1E30 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, I2CDirectAccessInterfaceTestCase)
        self.runTest(result, context, I2CDirectAccessFunctionalityTestCase)
        self.runTest(result, context, I2CDirectAccessErrorHandlingTestCase)
        self.runTest(result, context, I2CDirectAccessRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature1E30TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
