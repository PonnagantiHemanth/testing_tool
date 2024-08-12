#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.gaming.feature_8101.testrunner
:brief: HID++ 2.0 feature 0x8101 testrunner implementation
:author: YY Liu <yliu5@logitech.com>
:date: 2023/04/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.gaming.feature_8101.business import ProfileManagementBusinessTestCase
from pytestbox.device.hidpp20.gaming.feature_8101.errorhandling import ProfileManagementErrorHandlingTestCase
from pytestbox.device.hidpp20.gaming.feature_8101.functionality import ProfileManagementFunctionalityTestCase
from pytestbox.device.hidpp20.gaming.feature_8101.interface import ProfileManagementInterfaceTestCase
from pytestbox.device.hidpp20.gaming.feature_8101.robustness import ProfileManagementRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature8101TestSuite(PyHarnessSuite):
    """
    Define test runner suite for gaming feature 0x8101 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, ProfileManagementInterfaceTestCase)
        self.runTest(result, context, ProfileManagementBusinessTestCase)
        self.runTest(result, context, ProfileManagementFunctionalityTestCase)
        self.runTest(result, context, ProfileManagementErrorHandlingTestCase)
        self.runTest(result, context, ProfileManagementRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature8101TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
