#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.1'
:package: pytestbox.device.hidpp20.gaming.feature_8090.testrunner
:brief: HID++ 2.0 feature 0x8090 testrunner implementation
:author: YY Liu <yliu5@logitech.com>
:date: 2022/08/23
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.gaming.feature_8090.business import ModeStatusBusinessTestCase
from pytestbox.device.hidpp20.gaming.feature_8090.errorhandling import ModeStatusErrorHandlingTestCase
from pytestbox.device.hidpp20.gaming.feature_8090.functionality import ModeStatusFunctionalityTestCase
from pytestbox.device.hidpp20.gaming.feature_8090.interface import ModeStatusInterfaceTestCase
from pytestbox.device.hidpp20.gaming.feature_8090.robustness import ModeStatusRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature8090TestSuite(PyHarnessSuite):
    """
    Define test runner suite for gaming feature 0x8090 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, ModeStatusInterfaceTestCase)
        self.runTest(result, context, ModeStatusBusinessTestCase)
        self.runTest(result, context, ModeStatusFunctionalityTestCase)
        self.runTest(result, context, ModeStatusErrorHandlingTestCase)
        self.runTest(result, context, ModeStatusRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature8090TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
