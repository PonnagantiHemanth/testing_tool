#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.keyboard.feature_4610.testrunner
:brief: HID++ 2.0 feature 0x4610 testrunner implementation
:author: YY Liu <yliu5@logitech.com>
:date: 2023/10/03
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.keyboard.feature_4610.business import MultiRollerBusinessTestCase
from pytestbox.device.hidpp20.keyboard.feature_4610.errorhandling import MultiRollerErrorHandlingTestCase
from pytestbox.device.hidpp20.keyboard.feature_4610.functionality import MultiRollerFunctionalityTestCase
from pytestbox.device.hidpp20.keyboard.feature_4610.interface import MultiRollerInterfaceTestCase
from pytestbox.device.hidpp20.keyboard.feature_4610.robustness import MultiRollerRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature4610TestSuite(PyHarnessSuite):
    """
    Define test runner suite for keyboard feature 0x4610 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, MultiRollerInterfaceTestCase)
        self.runTest(result, context, MultiRollerBusinessTestCase)
        self.runTest(result, context, MultiRollerFunctionalityTestCase)
        self.runTest(result, context, MultiRollerErrorHandlingTestCase)
        self.runTest(result, context, MultiRollerRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature4610TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
