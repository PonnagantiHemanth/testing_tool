#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1805.testrunner
:brief: HID++ 2.0 feature 0x1805 testrunner implementation
:author: Sanjib Hazra <shazra@logitech.com>
:date: 2022/03/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_1805.business import OobStateBusinessTestCase
from pytestbox.device.hidpp20.common.feature_1805.errorhandling import OobStateErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_1805.functionality import OobStateEQuadFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_1805.functionality import OobStateFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_1805.functionality import OobStateUSBFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_1805.interface import OobStateInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_1805.robustness import OobStateRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature1805TestSuite(PyHarnessSuite):
    """
    Define test runner suite for common feature 0x1805 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, OobStateInterfaceTestCase)
        self.runTest(result, context, OobStateBusinessTestCase)
        self.runTest(result, context, OobStateFunctionalityTestCase)
        self.runTest(result, context, OobStateEQuadFunctionalityTestCase)
        self.runTest(result, context, OobStateUSBFunctionalityTestCase)
        self.runTest(result, context, OobStateErrorHandlingTestCase)
        self.runTest(result, context, OobStateRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature1805TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
