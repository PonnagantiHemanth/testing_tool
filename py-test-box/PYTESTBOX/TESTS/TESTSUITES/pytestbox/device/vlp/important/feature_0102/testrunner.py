#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.vlp.important.feature_0102.testrunner
:brief: VLP 1.0 feature 0x0102 testrunner implementation
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/09/10
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.vlp.important.feature_0102.interface import VLPRootInterfaceTestCase
from pytestbox.device.vlp.important.feature_0102.business import VLPRootBusinessTestCase
from pytestbox.device.vlp.important.feature_0102.functionality import VLPRootFunctionalityTestCase
from pytestbox.device.vlp.important.feature_0102.robustness import VLPRootRobustnessTestCase
from pytestbox.device.vlp.important.feature_0102.errorhandling import VLPRootErrorHandlingTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceVlpFeature0102TestSuite(PyHarnessSuite):
    """
    Define test runner suite for Vlp important feature 0x0102 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, VLPRootInterfaceTestCase)
        self.runTest(result, context, VLPRootBusinessTestCase)
        self.runTest(result, context, VLPRootFunctionalityTestCase)
        self.runTest(result, context, VLPRootRobustnessTestCase)
        self.runTest(result, context, VLPRootErrorHandlingTestCase)
    # end def runTests
# end class DeviceVlpFeature0102TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
