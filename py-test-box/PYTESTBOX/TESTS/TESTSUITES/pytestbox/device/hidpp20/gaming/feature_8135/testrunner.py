#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_8135.testrunner
:brief: HID++ 2.0 feature 0x8135 testrunner implementation
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/04/08
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.gaming.feature_8135.errorhandling import PedalStatusErrorHandlingTestCase
from pytestbox.device.hidpp20.gaming.feature_8135.interface import PedalStatusInterfaceTestCase
from pytestbox.device.hidpp20.gaming.feature_8135.robustness import PedalStatusRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature8135TestSuite(PyHarnessSuite):
    """
    Define test runner suite for gaming feature 0x8135 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, PedalStatusInterfaceTestCase)
        self.runTest(result, context, PedalStatusErrorHandlingTestCase)
        self.runTest(result, context, PedalStatusRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature8135TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
