#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1b05.testrunner
:brief: HID++ 2.0 feature 0x1b05 testrunner implementation
:author: Masan Xu <mxu11@logitech.com>
:date: 2023/05/04
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_1b05.business import FullKeyCustomizationBusinessTestCase
from pytestbox.device.hidpp20.common.feature_1b05.errorhandling import FullKeyCustomizationErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_1b05.functionality import FullKeyCustomizationFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_1b05.interface import FullKeyCustomizationInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_1b05.robustness import FullKeyCustomizationRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature1B05TestSuite(PyHarnessSuite):
    """
    Define test runner suite for common feature 0x1B05 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, FullKeyCustomizationInterfaceTestCase)
        self.runTest(result, context, FullKeyCustomizationBusinessTestCase)
        self.runTest(result, context, FullKeyCustomizationFunctionalityTestCase)
        self.runTest(result, context, FullKeyCustomizationErrorHandlingTestCase)
        self.runTest(result, context, FullKeyCustomizationRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature1B05TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
