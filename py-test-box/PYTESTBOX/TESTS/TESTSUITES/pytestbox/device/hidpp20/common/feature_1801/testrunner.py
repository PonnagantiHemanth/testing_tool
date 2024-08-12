#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1801.testrunner
:brief: HID++ 2.0 feature 0x1801 testrunner implementation
:author: Masan Xu <mxu11@logitech.com>
:date: 2023/06/14
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_1801.errorhandling import ManufacturingModeErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_1801.functionality import ManufacturingModeFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_1801.interface import ManufacturingModeInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_1801.robustness import ManufacturingModeRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature1801TestSuite(PyHarnessSuite):
    """
    Define test runner suite for common feature 0x1801 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, ManufacturingModeInterfaceTestCase)
        self.runTest(result, context, ManufacturingModeErrorHandlingTestCase)
        self.runTest(result, context, ManufacturingModeFunctionalityTestCase)
        self.runTest(result, context, ManufacturingModeRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature1801TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
