#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1982.testrunner
:brief: HID++ 2.0 feature 0x1982 testrunner implementation
:author: Anil Gadad <agadad@logitech.com>
:date: 2021/09/09
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_1982.business import BacklightBusinessTestCase
from pytestbox.device.hidpp20.common.feature_1982.errorhandling import BacklightErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_1982.functionality import BacklightFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_1982.interface import BacklightInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_1982.robustness import BacklightRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature1982TestSuite(PyHarnessSuite):
    """
    Define test runner suite for common feature 0x1982 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, BacklightInterfaceTestCase)
        self.runTest(result, context, BacklightBusinessTestCase)
        self.runTest(result, context, BacklightFunctionalityTestCase)
        self.runTest(result, context, BacklightErrorHandlingTestCase)
        self.runTest(result, context, BacklightRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature1982TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
