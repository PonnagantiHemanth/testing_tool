#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1b10.testrunner
:brief: HID++ 2.0 feature 0x1b10 testrunner implementation
:author: YY Liu <yliu5@logitech.com>
:date: 2023/06/09
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_1b10.business import ControlListBusinessTestCase
from pytestbox.device.hidpp20.common.feature_1b10.errorhandling import ControlListErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_1b10.functionality import ControlListFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_1b10.interface import ControlListInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_1b10.robustness import ControlListRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature1B10TestSuite(PyHarnessSuite):
    """
    Define test runner suite for common feature 0x1B10 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, ControlListInterfaceTestCase)
        self.runTest(result, context, ControlListBusinessTestCase)
        self.runTest(result, context, ControlListFunctionalityTestCase)
        self.runTest(result, context, ControlListErrorHandlingTestCase)
        self.runTest(result, context, ControlListRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature1B10TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
