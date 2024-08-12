#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.peripheral.feature_9001.testrunner
:brief: HID++ 2.0 feature 0x9001 testrunner implementation
:author: Gautham S B <gsb@logitech.com>
:date: 2023/01/09
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.peripheral.feature_9001.business import PMW3816andPMW3826BusinessTestCase
from pytestbox.device.hidpp20.peripheral.feature_9001.errorhandling import PMW3816andPMW3826ErrorHandlingTestCase
from pytestbox.device.hidpp20.peripheral.feature_9001.functionality import PMW3816andPMW3826FunctionalityTestCase
from pytestbox.device.hidpp20.peripheral.feature_9001.interface import PMW3816andPMW3826InterfaceTestCase
from pytestbox.device.hidpp20.peripheral.feature_9001.robustness import PMW3816andPMW3826RobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature9001TestSuite(PyHarnessSuite):
    """
    Define test runner suite for peripheral feature 0x9001 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, PMW3816andPMW3826InterfaceTestCase)
        self.runTest(result, context, PMW3816andPMW3826BusinessTestCase)
        self.runTest(result, context, PMW3816andPMW3826FunctionalityTestCase)
        self.runTest(result, context, PMW3816andPMW3826ErrorHandlingTestCase)
        self.runTest(result, context, PMW3816andPMW3826RobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature9001TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
