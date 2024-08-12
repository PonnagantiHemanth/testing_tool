#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.mouse.spuriousmotion.testrunner
:brief: Device Hid mouse spurious motion filtering algorithm feature
        testrunner implementation
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2023/04/04
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hid.mouse.spuriousmotion.business import SpuriousMotionBusinessTestCase
from pytestbox.device.hid.mouse.spuriousmotion.functionality import SpuriousMotionFunctionalityTestCase


# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class DeviceHidMouseSpuriousMotionTestSuite(PyHarnessSuite):
    """
    Test runner class for Hid Mouse spurious motion filtering algorithm tests.
    """
    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, SpuriousMotionBusinessTestCase)
        self.runTest(result, context, SpuriousMotionFunctionalityTestCase)
    # end def runTests
# end class DeviceHidMouseSpuriousMotionTestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
