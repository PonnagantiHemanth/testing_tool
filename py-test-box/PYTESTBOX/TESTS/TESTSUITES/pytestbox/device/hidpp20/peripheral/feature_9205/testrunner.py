#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.peripheral.feature_9205.testrunner
:brief: HID++ 2.0 feature 0x9205 testrunner implementation
:author: Gautham S B <gsb@logitech.com>
:date: 2023/03/02
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.peripheral.feature_9205.business import MLX903xxBusinessTestCase
from pytestbox.device.hidpp20.peripheral.feature_9205.errorhandling import MLX903xxErrorHandlingTestCase
from pytestbox.device.hidpp20.peripheral.feature_9205.functionality import MLX903xxFunctionalityTestCase
from pytestbox.device.hidpp20.peripheral.feature_9205.interface import MLX903xxInterfaceTestCase
from pytestbox.device.hidpp20.peripheral.feature_9205.robustness import MLX903xxRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature9205TestSuite(PyHarnessSuite):
    """
    Define test runner suite for peripheral feature 0x9205 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, MLX903xxInterfaceTestCase)
        self.runTest(result, context, MLX903xxBusinessTestCase)
        self.runTest(result, context, MLX903xxFunctionalityTestCase)
        self.runTest(result, context, MLX903xxErrorHandlingTestCase)
        self.runTest(result, context, MLX903xxRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature9205TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
