#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.mouse.feature_2111.testrunner
:brief: Device HID++ 2.0 Mouse feature 0x2111 - SmartShiftTunable testrunner implementation
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2021/08/10
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.mouse.feature_2111.business import SmartShiftTunableBusinessTestCase
from pytestbox.device.hidpp20.mouse.feature_2111.functionality import SmartShiftTunableFunctionalityResetTestCase
from pytestbox.device.hidpp20.mouse.feature_2111.functionality import SmartShiftTunableFunctionalityTestCase
from pytestbox.device.hidpp20.mouse.feature_2111.interface import SmartShiftTunableInterfaceTestCase
from pytestbox.device.hidpp20.mouse.feature_2111.robustness import SmartShiftTunableRobustnessTestCase


# ----------------------------------------------------------------------------
#  implementation
# ----------------------------------------------------------------------------
class DeviceHidpp20Feature2111TestSuite(PyHarnessSuite):
    """
    Test runner class for HID++ 2.0 feature 0x2111 - SmartShifTunable tests.
    """
    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, SmartShiftTunableInterfaceTestCase)
        self.runTest(result, context, SmartShiftTunableBusinessTestCase)
        self.runTest(result, context, SmartShiftTunableFunctionalityTestCase)
        self.runTest(result, context, SmartShiftTunableFunctionalityResetTestCase)
        self.runTest(result, context, SmartShiftTunableRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature2111TestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
