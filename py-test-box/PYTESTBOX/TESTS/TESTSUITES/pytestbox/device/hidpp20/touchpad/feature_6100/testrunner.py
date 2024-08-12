#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.touchpad.feature_6100.testrunner
:brief: HID++ 2.0 feature 0x6100 testrunner implementation
:author: Masan Xu <mxu11@logitech.com>
:date: 2022/05/11
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.touchpad.feature_6100.interface import TouchpadRawXYInterfaceTestCase


# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class DeviceHidpp20Feature6100TestSuite(PyHarnessSuite):
    """
    Define test runner suite for touchpad feature 0x6100 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, TouchpadRawXYInterfaceTestCase)

    # end def runTests
# end class DeviceHidpp20Feature6100TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
