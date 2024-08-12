#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.gaming.feature_8051.testrunner
:brief: HID++ 2.0 feature 0x8051 testrunner implementation
:author: Zane Lu <zlu@logitech.com>
:date: 2023/05/04
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.gaming.feature_8051.business import LogiModifiersBusinessTestCase
from pytestbox.device.hidpp20.gaming.feature_8051.errorhandling import LogiModifiersErrorHandlingTestCase
from pytestbox.device.hidpp20.gaming.feature_8051.functionality import LogiModifiersFunctionalityTestCase
from pytestbox.device.hidpp20.gaming.feature_8051.interface import LogiModifiersInterfaceTestCase
from pytestbox.device.hidpp20.gaming.feature_8051.robustness import LogiModifiersRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature8051TestSuite(PyHarnessSuite):
    """
    Define test runner suite for gaming feature 0x8051 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, LogiModifiersInterfaceTestCase)
        self.runTest(result, context, LogiModifiersBusinessTestCase)
        self.runTest(result, context, LogiModifiersFunctionalityTestCase)
        self.runTest(result, context, LogiModifiersErrorHandlingTestCase)
        self.runTest(result, context, LogiModifiersRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature8051TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
