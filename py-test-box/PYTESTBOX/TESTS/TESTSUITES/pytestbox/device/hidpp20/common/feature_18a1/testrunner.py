#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_18a1.testrunner
:brief: HID++ 2.0 feature 0x18a1 testrunner implementation
:author: Gautham S B <gsb@logitech.com>
:date: 2023/06/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_18a1.business import LEDTestBusinessTestCase
from pytestbox.device.hidpp20.common.feature_18a1.errorhandling import LEDTestErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_18a1.functionality import LEDTestFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_18a1.interface import LEDTestInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_18a1.robustness import LEDTestRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature18A1TestSuite(PyHarnessSuite):
    """
    Define test runner suite for common feature 0x18A1 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, LEDTestInterfaceTestCase)
        self.runTest(result, context, LEDTestBusinessTestCase)
        self.runTest(result, context, LEDTestFunctionalityTestCase)
        self.runTest(result, context, LEDTestErrorHandlingTestCase)
        self.runTest(result, context, LEDTestRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature18A1TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
