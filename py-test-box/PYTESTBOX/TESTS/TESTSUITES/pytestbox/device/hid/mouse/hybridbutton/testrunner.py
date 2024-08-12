#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.mouse.hybridbutton.testrunner
:brief: Device Hid mouse hybrid button feature testrunner implementation
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2024/02/15
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hid.mouse.hybridbutton.functionality import HybridButtonFunctionalityTestCase


# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class DeviceHidMouseHybridButtonTestSuite(PyHarnessSuite):
    """
    Test runner class for Hid Mouse Hybrid Button tests.
    """
    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, HybridButtonFunctionalityTestCase)
    # end def runTests
# end class DeviceHidMouseHybridButtonTestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
