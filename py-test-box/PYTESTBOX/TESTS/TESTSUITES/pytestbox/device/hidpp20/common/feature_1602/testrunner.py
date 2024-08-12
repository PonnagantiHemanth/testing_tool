#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1602.testrunner
:brief: Device HID++ 2.0 feature 0x1602 testrunner implementation
:author: Anil Gadad <agadad@logitech.com>
:date: 2021/10/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_1602.business import DevicePasswordAuthenticationBusinessTestCase
from pytestbox.device.hidpp20.common.feature_1602.errorhandling import DevicePasswordAuthenticationErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_1602.functionality import DevicePasswordAuthenticationFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_1602.interface import DevicePasswordAuthenticationInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_1602.robustness import DevicePasswordAuthenticationRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature1602TestSuite(PyHarnessSuite):
    """
    Define test runner suite for common feature 0x1602 tests
    """
    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, DevicePasswordAuthenticationInterfaceTestCase)
        self.runTest(result, context, DevicePasswordAuthenticationBusinessTestCase)
        self.runTest(result, context, DevicePasswordAuthenticationFunctionalityTestCase)
        self.runTest(result, context, DevicePasswordAuthenticationErrorHandlingTestCase)
        self.runTest(result, context, DevicePasswordAuthenticationRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature1602TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
