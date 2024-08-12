#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.touchpad.testrunner
:brief: Device HID++ 2.0 Touchpad features testrunner implementation
:author: Masan Xu <mxu11@logitech.com>
:date: 2022/04/15
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.touchpad.feature_6100.testrunner import DeviceHidpp20Feature6100TestSuite


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class TouchpadHidpp20TestSuite(PyHarnessSuite):
    """
    Test runner class for HID++ 2.0 touchpad tests
    """
    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        self.runTest(result, context, DeviceHidpp20Feature6100TestSuite)

    # end def runTests
# end class TouchpadHidpp20TestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
