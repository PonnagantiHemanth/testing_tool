#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_0007.testrunner
:brief: Device HID++ 2.0 Common feature 0x0007 testrunner implementation
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/03/19
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_0007.business import DeviceFriendlyNameBusinessTestCase
from pytestbox.device.hidpp20.common.feature_0007.errorhandling import DeviceFriendlyNameErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_0007.functionality import DeviceFriendlyNameFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_0007.interface import DeviceFriendlyNameInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_0007.robustness import DeviceFriendlyNameRobustnessTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceHidpp20Feature0007TestSuite(PyHarnessSuite):
    """
    Test runner class for HID++ 2.0 feature 0x0007 tests
    """
    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        self.runTest(result, context, DeviceFriendlyNameInterfaceTestCase)
        self.runTest(result, context, DeviceFriendlyNameBusinessTestCase)
        self.runTest(result, context, DeviceFriendlyNameFunctionalityTestCase)
        self.runTest(result, context, DeviceFriendlyNameErrorHandlingTestCase)
        self.runTest(result, context, DeviceFriendlyNameRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature0007TestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
