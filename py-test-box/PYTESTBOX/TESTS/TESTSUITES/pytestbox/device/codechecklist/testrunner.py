#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.codechecklist.testrunner
:brief: Device Code Checklist tests runner
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/06/21
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.codechecklist.ram import DeviceRamTestCase
from pytestbox.device.codechecklist.stack import DeviceStackTestCase
from pytestbox.device.codechecklist.uicr import DeviceUICRTestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class DeviceCodeChecklistTestSuite(PyHarnessSuite):
    """
    Device Code Checklist tests launcher
    """

    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        self.runTest(result, context, DeviceRamTestCase)
        self.runTest(result, context, DeviceUICRTestCase)
        if context.getFeatures().PRODUCT.CODE_CHECKLIST.F_StackVerification:
            self.runTest(result, context, DeviceStackTestCase)
        # end if
    # end def runTests
# end class DeviceMemoryTestSuite

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
