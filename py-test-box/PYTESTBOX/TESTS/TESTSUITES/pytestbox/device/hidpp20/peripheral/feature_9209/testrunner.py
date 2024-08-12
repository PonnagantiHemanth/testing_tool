#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_9209.testrunner
:brief: Device HID++ 2.0 Common feature 0x9209 testrunner implementation
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/03/25
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.peripheral.feature_9209.business import Mlx90393MultiSensorBusinessTestCase
from pytestbox.device.hidpp20.peripheral.feature_9209.errorhandling import Mlx90393MultiSensorErrorHandlingTestCase
from pytestbox.device.hidpp20.peripheral.feature_9209.interface import Mlx90393MultiSensorInterfaceTestCase
from pytestbox.device.hidpp20.peripheral.feature_9209.robustness import Mlx90393MultiSensorRobustnessTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceHidpp20Feature9209TestSuite(PyHarnessSuite):
    """
    Test runner class for HID++ 2.0 feature 0x9209 tests
    """
    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        self.runTest(result, context, Mlx90393MultiSensorInterfaceTestCase)
        self.runTest(result, context, Mlx90393MultiSensorBusinessTestCase)
        self.runTest(result, context, Mlx90393MultiSensorErrorHandlingTestCase)
        self.runTest(result, context, Mlx90393MultiSensorRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature0007TestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
