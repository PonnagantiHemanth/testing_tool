#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.peripheral.testrunner
:brief: Device HID++ 2.0 peripheral features testrunner implementation
:author: Ganesh Thiraviam <gthiraviam@logitech.com>
:date: 2021/03/10
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.peripheral.feature_9001.testrunner import DeviceHidpp20Feature9001TestSuite
from pytestbox.device.hidpp20.peripheral.feature_9205.testrunner import DeviceHidpp20Feature9205TestSuite
from pytestbox.device.hidpp20.peripheral.feature_9209.testrunner import DeviceHidpp20Feature9209TestSuite
from pytestbox.device.hidpp20.peripheral.feature_9215.testrunner import DeviceHidpp20Feature9215TestSuite
from pytestbox.device.hidpp20.peripheral.feature_92e2.testrunner import DeviceHidpp20Feature92E2TestSuite


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20PeripheralTestSuite(PyHarnessSuite):
    """
    Test runner class for peripheral tests
    """
    def runTests(self, result, context):
        # See ``PyHarnessSuite.runTests``
        self.runTest(result, context, DeviceHidpp20Feature9001TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature9205TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature9209TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature9215TestSuite)
        self.runTest(result, context, DeviceHidpp20Feature92E2TestSuite)
    # end def runTests
# end class DeviceHidpp20PeripheralTestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
