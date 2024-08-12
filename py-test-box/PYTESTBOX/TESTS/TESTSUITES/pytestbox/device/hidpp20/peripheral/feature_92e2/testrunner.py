#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.peripheral.feature_92e2.testrunner
:brief: HID++ 2.0 feature 0x92e2 testrunner implementation
:author: Gautham S B <gsb@logitech.com>
:date: 2024/04/02
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.peripheral.feature_92e2.business import TestKeysDisplayBusinessTestCase
from pytestbox.device.hidpp20.peripheral.feature_92e2.errorhandling import TestKeysDisplayErrorHandlingTestCase
from pytestbox.device.hidpp20.peripheral.feature_92e2.functionality import TestKeysDisplayFunctionalityTestCase
from pytestbox.device.hidpp20.peripheral.feature_92e2.interface import TestKeysDisplayInterfaceTestCase
from pytestbox.device.hidpp20.peripheral.feature_92e2.robustness import TestKeysDisplayRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature92E2TestSuite(PyHarnessSuite):
    """
    Define test runner suite for peripheral feature 0x92E2 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, TestKeysDisplayInterfaceTestCase)
        self.runTest(result, context, TestKeysDisplayBusinessTestCase)
        self.runTest(result, context, TestKeysDisplayFunctionalityTestCase)
        self.runTest(result, context, TestKeysDisplayErrorHandlingTestCase)
        self.runTest(result, context, TestKeysDisplayRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature92E2TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
