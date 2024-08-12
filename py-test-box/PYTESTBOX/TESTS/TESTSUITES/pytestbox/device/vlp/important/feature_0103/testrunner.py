#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.vlp.important.feature_0103.testrunner
:brief: VLP 1.0 feature 0x0103 testrunner implementation
:author: Gautham S B <gsb@logitech.com>
:date: 2024/04/23
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.vlp.important.feature_0103.business import VLPFeatureSetBusinessTestCase
from pytestbox.device.vlp.important.feature_0103.errorhandling import VLPFeatureSetErrorHandlingTestCase
from pytestbox.device.vlp.important.feature_0103.functionality import VLPFeatureSetFunctionalityTestCase
from pytestbox.device.vlp.important.feature_0103.interface import VLPFeatureSetInterfaceTestCase
from pytestbox.device.vlp.important.feature_0103.robustness import VLPFeatureSetRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------

class DeviceVlpFeature0103TestSuite(PyHarnessSuite):
    """
    Define test runner suite for vlp.important feature 0x0103 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, VLPFeatureSetInterfaceTestCase)
        self.runTest(result, context, VLPFeatureSetBusinessTestCase)
        self.runTest(result, context, VLPFeatureSetFunctionalityTestCase)
        self.runTest(result, context, VLPFeatureSetErrorHandlingTestCase)
        self.runTest(result, context, VLPFeatureSetRobustnessTestCase)
    # end def runTests
# end class DeviceVlpFeature0103TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
