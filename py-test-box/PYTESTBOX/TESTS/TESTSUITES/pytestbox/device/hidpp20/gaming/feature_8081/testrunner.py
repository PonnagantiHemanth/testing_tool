#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.gaming.feature_8081.testrunner
:brief: HID++ 2.0 feature 0x8081 testrunner implementation
:author: Gautham S B <gsb@logitech.com>
:date: 2022/10/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.gaming.feature_8081.business import PerKeyLightingBusinessTestCase
from pytestbox.device.hidpp20.gaming.feature_8081.errorhandling import PerKeyLightingErrorHandlingTestCase
from pytestbox.device.hidpp20.gaming.feature_8081.functionality import PerKeyLightingFunctionalityTestCase
from pytestbox.device.hidpp20.gaming.feature_8081.interface import PerKeyLightingInterfaceTestCase
from pytestbox.device.hidpp20.gaming.feature_8081.robustness import PerKeyLightingRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature8081TestSuite(PyHarnessSuite):
    """
    Define test runner suite for gaming feature 0x8081 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, PerKeyLightingInterfaceTestCase)
        self.runTest(result, context, PerKeyLightingBusinessTestCase)
        self.runTest(result, context, PerKeyLightingFunctionalityTestCase)
        self.runTest(result, context, PerKeyLightingErrorHandlingTestCase)
        self.runTest(result, context, PerKeyLightingRobustnessTestCase)

    # end def runTests
# end class DeviceHidpp20Feature8081TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
