#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.testrunner
:brief: Device tests runner
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2020/03/09
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.ble.testrunner import BleProtocolTestSuite
from pytestbox.device.codechecklist.testrunner import DeviceCodeChecklistTestSuite
from pytestbox.device.connectionscheme.testrunner import ConnectionSchemeTestSuite
from pytestbox.device.dualbank.testrunner import DeviceDualBankTestSuite
from pytestbox.device.hid.testrunner import DeviceHidTestSuite
from pytestbox.device.hidpp20.testrunner import DeviceHidpp20TestSuite
from pytestbox.device.led.testrunner import DeviceLedTestSuite
from pytestbox.device.ls2connectionscheme.testrunner import Ls2ConnectionSchemeTestSuite
from pytestbox.device.recovery.testrunner import DeviceRecoveryFeatureTestSuite
from pytestbox.device.usb.testrunner import DeviceUsbProtocolTestSuite
from pytestbox.device.vlp.testrunner import DeviceVlpTestSuite


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class DeviceTestSuite(PyHarnessSuite):
    """
    Test runner class for Device tests
    """
    def canRun(self, unusedresult, context):
        """
        Tests whether the test is allowed to run.
        """
        f = context.getFeatures()
        return f.PRODUCT.F_Enabled
    # end def canRun

    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        self.runTest(result, context, Ls2ConnectionSchemeTestSuite)
        self.runTest(result, context, ConnectionSchemeTestSuite)
        self.runTest(result, context, BleProtocolTestSuite)
        self.runTest(result, context, DeviceHidTestSuite)
        self.runTest(result, context, DeviceHidpp20TestSuite)
        self.runTest(result, context, DeviceUsbProtocolTestSuite)
        self.runTest(result, context, DeviceCodeChecklistTestSuite)
        self.runTest(result, context, DeviceDualBankTestSuite)
        self.runTest(result, context, DeviceVlpTestSuite)
        self.runTest(result, context, DeviceRecoveryFeatureTestSuite)
        self.runTest(result, context, DeviceLedTestSuite)
    # end def runTests
# end class DeviceTestSuite

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
