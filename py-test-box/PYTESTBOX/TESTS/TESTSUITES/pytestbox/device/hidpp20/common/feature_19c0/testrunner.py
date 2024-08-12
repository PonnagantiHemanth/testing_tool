#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_19c0.testrunner
:brief: HID++ 2.0 feature 0x19c0 testrunner implementation
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2024/08/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_19c0.interface import ForceSensingButtonInterfaceTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature19C0TestSuite(PyHarnessSuite):
    """
    Define test runner suite for common feature 0x19C0 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.

        :param result: The test result that will collect the results.
        :type result: ``TestResult``
        :param context: The context in which the tests are run.
        :type context: ``Context``
        """
        self.runTest(result, context, ForceSensingButtonInterfaceTestCase)
    # end def runTests
# end class DeviceHidpp20Feature19C0TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
