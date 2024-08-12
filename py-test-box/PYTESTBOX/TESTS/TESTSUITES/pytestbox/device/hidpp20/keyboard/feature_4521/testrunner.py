#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.keyboard.feature_4521.testrunner
:brief: Device HID++ 2.0 Keyboard feature 0x4521 - DisableKeys testrunner implementation
:author: YY Liu <yliu5@logitech.com>
:date: 2021/12/07
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.keyboard.feature_4521.business import DisableKeysBusinessTestCase
from pytestbox.device.hidpp20.keyboard.feature_4521.errorhandling import DisableKeysErrorHandlingTestCase
from pytestbox.device.hidpp20.keyboard.feature_4521.functionality import DisableKeysFunctionalityTestCase
from pytestbox.device.hidpp20.keyboard.feature_4521.interface import DisableKeysInterfaceTestCase
from pytestbox.device.hidpp20.keyboard.feature_4521.robustness import DisableKeysRobustnessTestCase


# ----------------------------------------------------------------------------
#  implementation
# ----------------------------------------------------------------------------
class DeviceHidpp20Feature4521TestSuite(PyHarnessSuite):
    """
    Test runner class for HID++ 2.0 feature 0x4521 - DisableKeys testrunner implementation
    """
    def runTests(self, result, context):
        """
        Run all the test in the test suites
        """
        self.runTest(result, context, DisableKeysInterfaceTestCase)
        self.runTest(result, context, DisableKeysBusinessTestCase)
        self.runTest(result, context, DisableKeysFunctionalityTestCase)
        self.runTest(result, context, DisableKeysErrorHandlingTestCase)
        self.runTest(result, context, DisableKeysRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature4521TestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
