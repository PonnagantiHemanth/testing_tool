#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.hidpp.testrunner
:brief: Receiver HID++ tests runner
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/02/19
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.receiver.hidpp.f7_f8.testrunner import ReceiverHidppF7F8TestSuite
from pytestbox.receiver.hidpp.f9_fa.testrunner import ReceiverHidppF9FATestSuite
from pytestbox.receiver.hidpp.get_rssi_B4 import GetRssiTestCase
from pytestbox.receiver.hidpp.quaddeviceconnection_B2 import QuadDeviceConnectionTestCase
from pytestbox.receiver.hidpp.receiverupgrade_F0 import ReceiverUpgradeTestCase
from pytestbox.receiver.hidpp.securedfucontrol_F5 import ReceiverSecureDfuControlTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ReceiverHidppTestSuite(PyHarnessSuite):
    """
    Receiver HID++ tests launcher
    """

    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        # Register 0xB0 QUAD or eQUAD Device Connection tests
        self.runTest(result, context, QuadDeviceConnectionTestCase)
        # Register 0xB4 Get RSSI tests
        self.runTest(result, context, GetRssiTestCase)
        # Register 0xF0 Receiver Upgrade
        self.runTest(result, context, ReceiverUpgradeTestCase)
        # Register 0xF5 DFU Control
        self.runTest(result, context, ReceiverSecureDfuControlTestCase)
        # Registers 0xF7 AND 0xF8 Password Authentication
        self.runTest(result, context, ReceiverHidppF7F8TestSuite)
        # Registers 0xF9 and 0xFA Manage Deactivatable Features
        self.runTest(result, context, ReceiverHidppF9FATestSuite)
    # end def runTests
# end class ReceiverHidppTestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
