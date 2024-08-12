#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.gaming.feature_8100.testrunner
:brief: HID++ 2.0 feature 0x8100 testrunner implementation
:author: Fred Chen <fchen7@logitech.com>
:date: 2022/01/04
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.gaming.feature_8100.business import OnboardProfilesBusinessTestCase
from pytestbox.device.hidpp20.gaming.feature_8100.errorhandling import OnboardProfilesErrorHandlingTestCase
from pytestbox.device.hidpp20.gaming.feature_8100.functionality import OnboardProfilesFunctionalityTestCase
from pytestbox.device.hidpp20.gaming.feature_8100.interface import OnboardProfilesInterfaceTestCase
from pytestbox.device.hidpp20.gaming.feature_8100.robustness import OnboardProfilesRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature8100TestSuite(PyHarnessSuite):
    """
    Define test runner suite for gaming feature 0x8100 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, OnboardProfilesInterfaceTestCase)
        self.runTest(result, context, OnboardProfilesBusinessTestCase)
        self.runTest(result, context, OnboardProfilesFunctionalityTestCase)
        self.runTest(result, context, OnboardProfilesErrorHandlingTestCase)
        self.runTest(result, context, OnboardProfilesRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature8100TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
