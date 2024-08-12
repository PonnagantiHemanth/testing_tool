#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.keyboard.feature_40a3.testrunner
:brief: HID++ 2.0 feature 0x40a3 testrunner implementation
:author: Masan Xu <mxu11@logitech.com>
:date: 2022/9/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.keyboard.feature_40a3.business import FnInversionForMultiHostDevicesBusinessTestCase
from pytestbox.device.hidpp20.keyboard.feature_40a3.errorhandling \
    import FnInversionForMultiHostDevicesErrorHandlingTestCase
from pytestbox.device.hidpp20.keyboard.feature_40a3.functionality \
    import FnInversionForMultiHostDevicesFunctionalityTestCase
from pytestbox.device.hidpp20.keyboard.feature_40a3.interface import FnInversionForMultiHostDevicesInterfaceTestCase
from pytestbox.device.hidpp20.keyboard.feature_40a3.robustness import FnInversionForMultiHostDevicesRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature40A3TestSuite(PyHarnessSuite):
    """
    Define test runner suite for keyboard feature 0x40A3 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, FnInversionForMultiHostDevicesInterfaceTestCase)
        self.runTest(result, context, FnInversionForMultiHostDevicesBusinessTestCase)
        self.runTest(result, context, FnInversionForMultiHostDevicesFunctionalityTestCase)
        self.runTest(result, context, FnInversionForMultiHostDevicesRobustnessTestCase)
        self.runTest(result, context, FnInversionForMultiHostDevicesErrorHandlingTestCase)
    # end def runTests
# end class DeviceHidpp20Feature40A3TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
