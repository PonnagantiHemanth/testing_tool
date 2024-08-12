#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.recovery.testrunner
:brief: Receiver for device recovery testrunner implementation
:author: YY Liu <yliu5@logitech.com>
:date: 2023/02/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.receiver.recovery.business import ReceiverForDeviceRecoveryBusinessTestCase
from pytestbox.receiver.recovery.errorhandling import ReceiverForDeviceRecoveryErrorHandlingTestCase
from pytestbox.receiver.recovery.functionality import ReceiverForDeviceRecoveryFunctionalityTestCase
from pytestbox.receiver.recovery.interface import ReceiverForDeviceRecoveryInterfaceTestCase
from pytestbox.receiver.recovery.robustness import ReceiverForDeviceRecoveryRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ReceiverForDeviceRecoveryFeatureTestSuite(PyHarnessSuite):
    """
    Define test runner class for receiver for device recovery feature tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, ReceiverForDeviceRecoveryInterfaceTestCase)
        self.runTest(result, context, ReceiverForDeviceRecoveryBusinessTestCase)
        self.runTest(result, context, ReceiverForDeviceRecoveryFunctionalityTestCase)
        self.runTest(result, context, ReceiverForDeviceRecoveryRobustnessTestCase)
        self.runTest(result, context, ReceiverForDeviceRecoveryErrorHandlingTestCase)
    # end def runTests
# end class ReceiverForDeviceRecoveryFeatureTestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
