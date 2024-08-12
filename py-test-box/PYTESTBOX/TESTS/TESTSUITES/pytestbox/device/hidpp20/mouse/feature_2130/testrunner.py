#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.mouse.feature_2130.testrunner
:brief: HID++ 2.0 feature 0x2130 testrunner implementation
:author: Gautham S B <gsb@logitech.com>
:date: 2022/11/30
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.mouse.feature_2130.business import RatchetWheelBusinessTestCase
from pytestbox.device.hidpp20.mouse.feature_2130.errorhandling import RatchetWheelErrorHandlingTestCase
from pytestbox.device.hidpp20.mouse.feature_2130.functionality import RatchetWheelFunctionalityTestCase
from pytestbox.device.hidpp20.mouse.feature_2130.interface import RatchetWheelInterfaceTestCase
from pytestbox.device.hidpp20.mouse.feature_2130.robustness import RatchetWheelRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature2130TestSuite(PyHarnessSuite):
    """
    Define test runner suite for mouse feature 0x2130 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, RatchetWheelInterfaceTestCase)
        self.runTest(result, context, RatchetWheelBusinessTestCase)
        self.runTest(result, context, RatchetWheelFunctionalityTestCase)
        self.runTest(result, context, RatchetWheelErrorHandlingTestCase)
        self.runTest(result, context, RatchetWheelRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature2130TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
