#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_00c3.testrunner
:brief: HID++ 2.0  Device Secure DFU control 0x00c3 testrunner implementation
:author: Stanislas Cottard <scottard@logitech.com>, Kevin Dayet <kdayet@logitech.com>
:date: 2020/09/04
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_00c3.business import DeviceSecureDfuControlBusinessTestCase
from pytestbox.device.hidpp20.common.feature_00c3.errorhandling import DeviceSecureDfuControlErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_00c3.functionality import DeviceSecureDfuControlFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_00c3.interface import DeviceSecureDfuControlInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_00c3.robustness import DeviceSecureDfuControlRobustnessTestCase
from pytestbox.device.hidpp20.common.feature_00c3.security import DeviceSecureDfuControlSecurityTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceHidpp20Feature00C3TestSuite(PyHarnessSuite):
    """
    Test runner class for HID++ 2.0 feature 0x00C3 tests.
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, DeviceSecureDfuControlInterfaceTestCase)
        self.runTest(result, context, DeviceSecureDfuControlBusinessTestCase)
        self.runTest(result, context, DeviceSecureDfuControlFunctionalityTestCase)
        self.runTest(result, context, DeviceSecureDfuControlErrorHandlingTestCase)
        self.runTest(result, context, DeviceSecureDfuControlRobustnessTestCase)
        self.runTest(result, context, DeviceSecureDfuControlSecurityTestCase)
    # end def runTests
# end class DeviceHidpp20Feature00C3TestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
