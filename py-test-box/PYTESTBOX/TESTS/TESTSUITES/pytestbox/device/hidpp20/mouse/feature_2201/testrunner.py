#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.mouse.feature_2201.testrunner
:brief: Device HID++ 2.0 Mouse feature 0x2201 testrunner implementation
:author: Fred Chen <fchen7@logitech.com>
:date: 2021/06/16
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.mouse.feature_2201.business import AdjustableDpiBusinessTestCase
from pytestbox.device.hidpp20.mouse.feature_2201.errorhandling import AdjustableDpiErrorHandlingTestCase
from pytestbox.device.hidpp20.mouse.feature_2201.functionality import AdjustableDpiFunctionalityTestCase
from pytestbox.device.hidpp20.mouse.feature_2201.interface import AdjustableDpiInterfaceTestCase
from pytestbox.device.hidpp20.mouse.feature_2201.robustness import AdjustableDpiRobustnessTestCase


# ----------------------------------------------------------------------------
#  implementation
# ----------------------------------------------------------------------------
class DeviceHidpp20Feature2201TestSuite(PyHarnessSuite):
    """
    Test runner class for HID++ 2.0 feature 0x2201 tests.
    """
    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, AdjustableDpiInterfaceTestCase)
        self.runTest(result, context, AdjustableDpiBusinessTestCase)
        self.runTest(result, context, AdjustableDpiFunctionalityTestCase)
        self.runTest(result, context, AdjustableDpiErrorHandlingTestCase)
        self.runTest(result, context, AdjustableDpiRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature2201TestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
