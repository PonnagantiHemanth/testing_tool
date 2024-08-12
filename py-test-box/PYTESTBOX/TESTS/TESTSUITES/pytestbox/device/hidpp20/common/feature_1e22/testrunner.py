#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.common.feature_1e22.testrunner
:brief: HID++ 2.0 feature 0x1e22 testrunner implementation
:author: YY Liu <yliu5@logitech.com>
:date: 2022/11/21
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_1e22.errorhandling import SPIDirectAccessErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_1e22.functionality import SPIDirectAccessFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_1e22.interface import SPIDirectAccessInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_1e22.robustness import SPIDirectAccessRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature1E22TestSuite(PyHarnessSuite):
    """
    Define test runner suite for common feature 0x1E22 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, SPIDirectAccessInterfaceTestCase)
        self.runTest(result, context, SPIDirectAccessFunctionalityTestCase)
        self.runTest(result, context, SPIDirectAccessErrorHandlingTestCase)
        self.runTest(result, context, SPIDirectAccessRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature1E22TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
