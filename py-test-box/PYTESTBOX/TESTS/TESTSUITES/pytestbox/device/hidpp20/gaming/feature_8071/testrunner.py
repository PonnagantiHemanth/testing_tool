#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.gaming.feature_8071.testrunner
:brief: HID++ 2.0 feature 0x8071 testrunner implementation
:author: Fred Chen <fchen7@logitech.com>
:date: 2022/06/09
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.gaming.feature_8071.functionality import RGBEffectsFunctionalityTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature8071TestSuite(PyHarnessSuite):
    """
    Define test runner suite for gaming feature 0x8071 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, RGBEffectsFunctionalityTestCase)
    # end def runTests
# end class DeviceHidpp20Feature8071TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
