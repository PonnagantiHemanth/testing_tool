#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.mouse.testrunner
:brief: Device Hid mouse features testrunner implementation
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2023/01/19
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hid.mouse.button.testrunner import DeviceHidMouseButtonTestSuite
from pytestbox.device.hid.mouse.displacement.testrunner import DeviceHidMouseDisplacementTestSuite
from pytestbox.device.hid.mouse.hybridbutton.testrunner import DeviceHidMouseHybridButtonTestSuite
from pytestbox.device.hid.mouse.spuriousmotion.testrunner import DeviceHidMouseSpuriousMotionTestSuite
from pytestbox.device.hid.mouse.smoothingalgo.testrunner import DeviceHidMouseSmoothingAlgoTestSuite


# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class DeviceHidMouseTestSuite(PyHarnessSuite):
    """
    Test runner class for Hid Mouse tests.
    """
    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        # Hid Mouse button feature
        self.runTest(result, context, DeviceHidMouseButtonTestSuite)
        # Hid Mouse hybrid button feature
        self.runTest(result, context, DeviceHidMouseHybridButtonTestSuite)
        # Hid Mouse XY displacement feature
        self.runTest(result, context, DeviceHidMouseDisplacementTestSuite)
        # HID Mouse Spurious motion detection algorithm feature
        self.runTest(result, context, DeviceHidMouseSpuriousMotionTestSuite)
        # HID Mouse Smoothing algorithm feature
        self.runTest(result, context, DeviceHidMouseSmoothingAlgoTestSuite)
    # end def runTests
# end class DeviceHidMouseTestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
