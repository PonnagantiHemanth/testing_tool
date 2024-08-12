#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_8134.testrunner
:brief: HID++ 2.0 feature 0x8134 testrunner implementation
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/04/01
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.gaming.feature_8134.business import BrakeForceBusinessTestCase
from pytestbox.device.hidpp20.gaming.feature_8134.errorhandling import BrakeForceErrorHandlingTestCase
from pytestbox.device.hidpp20.gaming.feature_8134.functionality import BrakeForceFunctionalityTestCase
from pytestbox.device.hidpp20.gaming.feature_8134.interface import BrakeForceInterfaceTestCase
from pytestbox.device.hidpp20.gaming.feature_8134.robustness import BrakeForceRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature8134TestSuite(PyHarnessSuite):
    """
    Define test runner suite for gaming feature 0x8134 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, BrakeForceInterfaceTestCase)
        self.runTest(result, context, BrakeForceBusinessTestCase)
        self.runTest(result, context, BrakeForceFunctionalityTestCase)
        self.runTest(result, context, BrakeForceErrorHandlingTestCase)
        self.runTest(result, context, BrakeForceRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature8134TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
