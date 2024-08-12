#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1eb0.testrunner
:brief: HID++ 2.0 feature 0x1eb0 testrunner implementation
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/03/22
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_1eb0.errorhandling import TdeAccessToNvmErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_1eb0.functionality import TdeAccessToNvmFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_1eb0.interface import TdeAccessToNvmInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_1eb0.robustness import TdeAccessToNvmRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature1EB0TestSuite(PyHarnessSuite):
    """
    Define test runner suite for common feature 0x1EB0 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, TdeAccessToNvmInterfaceTestCase)
        self.runTest(result, context, TdeAccessToNvmFunctionalityTestCase)
        self.runTest(result, context, TdeAccessToNvmErrorHandlingTestCase)
        self.runTest(result, context, TdeAccessToNvmRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature1EB0TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
