#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.1'
:package: pytestbox.device.hidpp20.common.feature_0011.testrunner
:brief: HID++ 2.0 feature 0x0011 testrunner implementation
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2022/06/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_0011.business import PropertyAccessBLEBusinessTestCase
from pytestbox.device.hidpp20.common.feature_0011.business import PropertyAccessBLEProBusinessTestCase
from pytestbox.device.hidpp20.common.feature_0011.business import PropertyAccessBusinessTestCase
from pytestbox.device.hidpp20.common.feature_0011.business import PropertyAccessEQuadBusinessTestCase
from pytestbox.device.hidpp20.common.feature_0011.business import PropertyAccessUSBBusinessTestCase
from pytestbox.device.hidpp20.common.feature_0011.errorhandling import PropertyAccessErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_0011.functionality import PropertyAccessFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_0011.interface import PropertyAccessInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_0011.robustness import PropertyAccessRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature0011TestSuite(PyHarnessSuite):
    """
    Define test runner suite for common feature 0x0011 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, PropertyAccessInterfaceTestCase)
        self.runTest(result, context, PropertyAccessBusinessTestCase)
        self.runTest(result, context, PropertyAccessBLEProBusinessTestCase)
        self.runTest(result, context, PropertyAccessBLEBusinessTestCase)
        self.runTest(result, context, PropertyAccessEQuadBusinessTestCase)
        self.runTest(result, context, PropertyAccessUSBBusinessTestCase)
        self.runTest(result, context, PropertyAccessFunctionalityTestCase)
        self.runTest(result, context, PropertyAccessErrorHandlingTestCase)
        self.runTest(result, context, PropertyAccessRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature0011TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
