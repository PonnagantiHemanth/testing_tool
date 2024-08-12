#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.recovery.testrunner
:brief: Device recovery testrunner implementation
:author: YY Liu <yliu5@logitech.com>
:date: 2023/01/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.recovery.business import DeviceRecoveryBusinessTestCase
from pytestbox.device.recovery.functionality import DeviceRecoveryFunctionalityTestCase
from pytestbox.device.recovery.robustness import DeviceRecoveryRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceRecoveryFeatureTestSuite(PyHarnessSuite):
    """
    Define test runner class for device recovery feature tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, DeviceRecoveryBusinessTestCase)
        self.runTest(result, context, DeviceRecoveryFunctionalityTestCase)
        self.runTest(result, context, DeviceRecoveryRobustnessTestCase)
    # end def runTests
# end class DeviceRecoveryFeatureTestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
