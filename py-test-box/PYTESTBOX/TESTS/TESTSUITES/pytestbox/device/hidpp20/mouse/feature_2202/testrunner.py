#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.mouse.feature_2202.testrunner
:brief: HID++ 2.0 feature 0x2202 testrunner implementation
:author: Fred Chen <fchen7@logitech.com>
:date: 2022/06/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.mouse.feature_2202.business import ExtendedAdjustableDpiBusinessTestCase
from pytestbox.device.hidpp20.mouse.feature_2202.errorhandling import ExtendedAdjustableDpiErrorHandlingTestCase
from pytestbox.device.hidpp20.mouse.feature_2202.functionality import ExtendedAdjustableDpiFunctionalityTestCase
from pytestbox.device.hidpp20.mouse.feature_2202.interface import ExtendedAdjustableDpiInterfaceTestCase
from pytestbox.device.hidpp20.mouse.feature_2202.robustness import ExtendedAdjustableDpiRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature2202TestSuite(PyHarnessSuite):
    """
    Define test runner suite for mouse feature 0x2202 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, ExtendedAdjustableDpiInterfaceTestCase)
        self.runTest(result, context, ExtendedAdjustableDpiBusinessTestCase)
        self.runTest(result, context, ExtendedAdjustableDpiFunctionalityTestCase)
        self.runTest(result, context, ExtendedAdjustableDpiErrorHandlingTestCase)
        self.runTest(result, context, ExtendedAdjustableDpiRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature2202TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
