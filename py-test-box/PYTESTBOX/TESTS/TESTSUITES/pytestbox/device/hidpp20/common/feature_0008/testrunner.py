#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_0008.testrunner
:brief: HID++ 2.0 feature 0x0008 testrunner implementation
:author: Harish Kumar D <hd@logitech.com>
:date: 2024/01/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_0008.business import KeepAliveBusinessTestCase
from pytestbox.device.hidpp20.common.feature_0008.errorhandling import KeepAliveErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_0008.functionality import KeepAliveFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_0008.interface import KeepAliveInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_0008.robustness import KeepAliveRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature0008TestSuite(PyHarnessSuite):
    """
    Define test runner suite for common feature 0x0008 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, KeepAliveInterfaceTestCase)
        self.runTest(result, context, KeepAliveBusinessTestCase)
        self.runTest(result, context, KeepAliveFunctionalityTestCase)
        self.runTest(result, context, KeepAliveErrorHandlingTestCase)
        self.runTest(result, context, KeepAliveRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature0008TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
