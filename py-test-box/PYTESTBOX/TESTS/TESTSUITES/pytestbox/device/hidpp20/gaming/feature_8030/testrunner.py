#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.gaming.feature_8030.testrunner
:brief: HID++ 2.0 feature 0x8030 testrunner implementation
:author: Zane Lu <zlu@logitech.com>
:date: 2023/11/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.gaming.feature_8030.business import MacroRecordkeyBusinessTestCase
from pytestbox.device.hidpp20.gaming.feature_8030.errorhandling import MacroRecordkeyErrorHandlingTestCase
from pytestbox.device.hidpp20.gaming.feature_8030.functionality import MacroRecordkeyFunctionalityTestCase
from pytestbox.device.hidpp20.gaming.feature_8030.interface import MacroRecordkeyInterfaceTestCase
from pytestbox.device.hidpp20.gaming.feature_8030.robustness import MacroRecordkeyRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature8030TestSuite(PyHarnessSuite):
    """
    Define test runner suite for gaming feature 0x8030 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, MacroRecordkeyInterfaceTestCase)
        self.runTest(result, context, MacroRecordkeyBusinessTestCase)
        self.runTest(result, context, MacroRecordkeyFunctionalityTestCase)
        self.runTest(result, context, MacroRecordkeyErrorHandlingTestCase)
        self.runTest(result, context, MacroRecordkeyRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature8030TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
