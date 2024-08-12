#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_80d0.testrunner
:brief: HID++ 2.0 feature 0x80d0 testrunner implementation
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/04/01
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.gaming.feature_80d0.business import CombinedPedalsBusinessTestCase
from pytestbox.device.hidpp20.gaming.feature_80d0.errorhandling import CombinedPedalsErrorHandlingTestCase
from pytestbox.device.hidpp20.gaming.feature_80d0.functionality import CombinedPedalsFunctionalityTestCase
from pytestbox.device.hidpp20.gaming.feature_80d0.interface import CombinedPedalsInterfaceTestCase
from pytestbox.device.hidpp20.gaming.feature_80d0.robustness import CombinedPedalsRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature80D0TestSuite(PyHarnessSuite):
    """
    Test runner class for gaming feature 0x80D0 tests
    """
    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        self.runTest(result, context, CombinedPedalsInterfaceTestCase)
        self.runTest(result, context, CombinedPedalsBusinessTestCase)
        self.runTest(result, context, CombinedPedalsFunctionalityTestCase)
        self.runTest(result, context, CombinedPedalsErrorHandlingTestCase)
        self.runTest(result, context, CombinedPedalsRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature80D0TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
