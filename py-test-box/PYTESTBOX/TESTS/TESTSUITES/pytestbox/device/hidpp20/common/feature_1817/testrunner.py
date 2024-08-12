#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.common.feature_1817.testrunner
:brief: HID++ 2.0 feature 0x1817 testrunner implementation
:author: Zane Lu <zlu@logitech.com>
:date: 2022/06/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_1817.business import LightspeedPrepairingBusinessTestCase
from pytestbox.device.hidpp20.common.feature_1817.errorhandling import LightspeedPrepairingErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_1817.functionality import LightspeedPrepairingFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_1817.interface import LightspeedPrepairingInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_1817.robustness import LightspeedPrepairingRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature1817TestSuite(PyHarnessSuite):
    """
    Define test runner suite for common feature 0x1817 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, LightspeedPrepairingInterfaceTestCase)
        self.runTest(result, context, LightspeedPrepairingBusinessTestCase)
        self.runTest(result, context, LightspeedPrepairingFunctionalityTestCase)
        self.runTest(result, context, LightspeedPrepairingErrorHandlingTestCase)
        self.runTest(result, context, LightspeedPrepairingRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature1817TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
