#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.common.feature_1814.testrunner
:brief: HID++ 2.0 feature 0x1814 testrunner implementation
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2021/12/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_1814.business import ChangeHostBusinessTestCase
from pytestbox.device.hidpp20.common.feature_1814.business import ChangeHostMultiReceiverBusinessTestCase
from pytestbox.device.hidpp20.common.feature_1814.errorhandling import ChangeHostErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_1814.functionality import ChangeHostFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_1814.functionality import ChangeHostMultiReceiverFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_1814.interface import ChangeHostInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_1814.robustness import ChangeHostRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature1814TestSuite(PyHarnessSuite):
    """
    Define test runner suite for common feature 0x1814 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, ChangeHostInterfaceTestCase)
        self.runTest(result, context, ChangeHostBusinessTestCase)
        self.runTest(result, context, ChangeHostMultiReceiverBusinessTestCase)
        self.runTest(result, context, ChangeHostFunctionalityTestCase)
        self.runTest(result, context, ChangeHostMultiReceiverFunctionalityTestCase)
        self.runTest(result, context, ChangeHostErrorHandlingTestCase)
        self.runTest(result, context, ChangeHostRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature1814TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
