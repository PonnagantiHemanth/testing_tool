#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.receiver.hidpp20.common.testrunner
    :brief: Receiver HID++ 2.0 Common features testrunner implementation
    :author: Christophe Roquebert
    :date: 2020/03/25
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.receiver.hidpp20.common.feature_0003 import DeviceInformationTestCase
from pytestbox.receiver.hidpp20.common.feature_0005 import DeviceTypeAndNameTestCase
from pytestbox.receiver.hidpp20.common.feature_00D0_interface import DfuTestCaseInterface
from pytestbox.receiver.hidpp20.common.feature_00D0_business import DfuTestCaseBusiness
from pytestbox.receiver.hidpp20.common.feature_00D0_functionality import DfuTestCaseFunctionality
from pytestbox.receiver.hidpp20.common.feature_00D0_change_flag import DfuTestCaseChangeFlag
from pytestbox.receiver.hidpp20.common.feature_00D0_robustness import DfuTestCaseRobustness
from pytestbox.receiver.hidpp20.common.feature_00D0_errorhandling import DfuTestCaseErrorHandling
from pytestbox.receiver.hidpp20.common.feature_00D0_security import DfuTestCaseSecurity
from pytestbox.receiver.hidpp20.common.feature_00D0_change_security_level import DfuTestCaseChangeSecurityLevel


# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class ReceiverCommonHidpp20TestSuite(PyHarnessSuite):
    """
    Test runner class for HID++ 2.0 common tests
    """
    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        self.runTest(result, context, DeviceInformationTestCase)
        self.runTest(result, context, DeviceTypeAndNameTestCase)
        self.runTest(result, context, DfuTestCaseInterface)
        self.runTest(result, context, DfuTestCaseBusiness)
        self.runTest(result, context, DfuTestCaseFunctionality)
        self.runTest(result, context, DfuTestCaseChangeFlag)
        self.runTest(result, context, DfuTestCaseRobustness)
        self.runTest(result, context, DfuTestCaseErrorHandling)
        self.runTest(result, context, DfuTestCaseSecurity)
        self.runTest(result, context, DfuTestCaseChangeSecurityLevel)
    # end def runTests
# end class ReceiverCommonHidpp20TestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
