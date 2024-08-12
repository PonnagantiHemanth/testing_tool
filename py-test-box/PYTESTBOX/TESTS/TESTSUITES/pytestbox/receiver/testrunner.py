#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.receiver.testrunner
:brief: Receiver tests runner
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2020/02/19
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.receiver.connectionscheme.testrunner import ConnectionSchemeTestSuite
from pytestbox.receiver.hidpp.testrunner import ReceiverHidppTestSuite
from pytestbox.receiver.hidpp20.testrunner import ReceiverHidpp20TestSuite
from pytestbox.receiver.codechecklist.testrunner import ReceiverCodeChecklistTestSuite
from pytestbox.receiver.recovery.testrunner import ReceiverForDeviceRecoveryFeatureTestSuite
from pytestbox.receiver.setup.testrunner import SetupTestSuite
from pytestbox.receiver.tde.testrunner import ReceiverTDETestSuite
from pytestbox.receiver.usb.testrunner import ReceiverUsbProtocolTestSuite


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ReceiverTestSuite(PyHarnessSuite):
    """
    Test runner class for Receiver tests
    """
    def canRun(self, unusedresult, context):
        """
        Tests whether the test is allowed to run.
        """
        f = context.getFeatures()
        return f.RECEIVER.F_Enabled
    # end def canRun

    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        self.runTest(result, context, ConnectionSchemeTestSuite)
        self.runTest(result, context, ReceiverHidpp20TestSuite)
        self.runTest(result, context, ReceiverHidppTestSuite)
        self.runTest(result, context, ReceiverTDETestSuite)
        self.runTest(result, context, SetupTestSuite)
        self.runTest(result, context, ReceiverUsbProtocolTestSuite)
        self.runTest(result, context, ReceiverCodeChecklistTestSuite)
        self.runTest(result, context, ReceiverForDeviceRecoveryFeatureTestSuite)
    # end def runTests
# end class ReceiverTestSuite

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
