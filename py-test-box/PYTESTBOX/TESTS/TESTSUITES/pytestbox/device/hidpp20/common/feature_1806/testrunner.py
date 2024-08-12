#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1806.testrunner
:brief: Device HID++ 2.0 Common feature 0x1806 testrunner implementation
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/04/28
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_1806.business import ConfigurableDevicePropertiesBusinessTestCase
from pytestbox.device.hidpp20.common.feature_1806.errorhandling import ConfigurableDevicePropertiesErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_1806.functionality import ConfigurableDevicePropertiesFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_1806.interface import ConfigurableDevicePropertiesInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_1806.robustness import ConfigurableDevicePropertiesRobustnessTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceHidpp20Feature1806TestSuite(PyHarnessSuite):
    """
    Test runner class for HID++ 2.0 feature 0x1806 tests
    """
    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        self.runTest(result, context, ConfigurableDevicePropertiesInterfaceTestCase)
        self.runTest(result, context, ConfigurableDevicePropertiesBusinessTestCase)
        self.runTest(result, context, ConfigurableDevicePropertiesFunctionalityTestCase)
        self.runTest(result, context, ConfigurableDevicePropertiesErrorHandlingTestCase)
        self.runTest(result, context, ConfigurableDevicePropertiesRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature1806TestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
