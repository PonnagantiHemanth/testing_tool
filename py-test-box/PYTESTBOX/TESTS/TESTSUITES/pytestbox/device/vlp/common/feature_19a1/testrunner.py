#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.vlp.common.feature_19a1.testrunner
:brief: VLP 1.0 feature 0x19a1 testrunner implementation
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/11/03
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.vlp.common.feature_19a1.business import ContextualDisplayBusinessTestCase
from pytestbox.device.vlp.common.feature_19a1.errorhandling import ContextualDisplayErrorHandlingTestCase
from pytestbox.device.vlp.common.feature_19a1.functionality import ContextualDisplayFunctionalityTestCase
from pytestbox.device.vlp.common.feature_19a1.interface import ContextualDisplayInterfaceTestCase
from pytestbox.device.vlp.common.feature_19a1.robustness import ContextualDisplayRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceVlpFeature19A1TestSuite(PyHarnessSuite):
    """
    Define test runner suite for common feature 0x19A1 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, ContextualDisplayInterfaceTestCase)
        self.runTest(result, context, ContextualDisplayBusinessTestCase)
        self.runTest(result, context, ContextualDisplayFunctionalityTestCase)
        self.runTest(result, context, ContextualDisplayRobustnessTestCase)
        self.runTest(result, context, ContextualDisplayErrorHandlingTestCase)
    # end def runTests
# end class DeviceVlpFeature19A1TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
