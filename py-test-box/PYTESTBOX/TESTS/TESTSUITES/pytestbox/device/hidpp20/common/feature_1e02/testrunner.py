#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1e02.testrunner
:brief: Device HID++ 2.0 Common feature 0x1e02 testrunner implementation
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2021/06/08
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_1e02.business import DeviceManageDeactivatableFeaturesAuthBusinessTestCase
from pytestbox.device.hidpp20.common.feature_1e02.functionality import \
    DeviceManageDeactivatableFeaturesAuthFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_1e02.interface import \
    DeviceManageDeactivatableFeaturesAuthInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_1e02.robustness import \
    DeviceManageDeactivatableFeaturesAuthRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature1e02TestSuite(PyHarnessSuite):
    """
    Test runner class for HID++ 2.0 feature 0x1e02 tests
    """
    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        self.runTest(result, context, DeviceManageDeactivatableFeaturesAuthInterfaceTestCase)
        self.runTest(result, context, DeviceManageDeactivatableFeaturesAuthBusinessTestCase)
        self.runTest(result, context, DeviceManageDeactivatableFeaturesAuthFunctionalityTestCase)
        self.runTest(result, context, DeviceManageDeactivatableFeaturesAuthRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature1e02TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
