#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.keyboard.feature_4522.testrunner
:brief: Device HID++ 2.0 Keyboard feature 0x4522 - DisableKeysByUsage testrunner implementation
:author: YY Liu <yliu5@logitech.com>
:date: 2021/09/14
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.keyboard.feature_4522.business import DisableKeysByUsageBusinessTestCase
from pytestbox.device.hidpp20.keyboard.feature_4522.errorhandling import DisableKeysByUsageErrorHandlingTestCase
from pytestbox.device.hidpp20.keyboard.feature_4522.functionality import DisableKeysByUsageFunctionalityTestCase
from pytestbox.device.hidpp20.keyboard.feature_4522.interface import DisableKeysByUsageInterfaceTestCase
from pytestbox.device.hidpp20.keyboard.feature_4522.robustness import DisableKeysByUsageRobustnessTestCase


# ----------------------------------------------------------------------------
#  implementation
# ----------------------------------------------------------------------------
class DeviceHidpp20Feature4522TestSuite(PyHarnessSuite):
    """
    Test runner class for HID++ 2.0 feature 0x4522 - DisableKeysByUsage tests.
    """
    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, DisableKeysByUsageInterfaceTestCase)
        self.runTest(result, context, DisableKeysByUsageBusinessTestCase)
        self.runTest(result, context, DisableKeysByUsageFunctionalityTestCase)
        self.runTest(result, context, DisableKeysByUsageErrorHandlingTestCase)
        self.runTest(result, context, DisableKeysByUsageRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature4522TestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
