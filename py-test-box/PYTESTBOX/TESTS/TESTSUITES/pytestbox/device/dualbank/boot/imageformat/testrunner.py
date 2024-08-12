#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.dualbank.boot.imageformat.testrunner
:brief: Device Dual Bank Boot Image Format tests runner
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2022/11/21
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.dualbank.boot.imageformat.business import ImageFormatBusinessTestCase
from pytestbox.device.dualbank.boot.imageformat.functionality import ImageFormatFunctionalityTestCase
from pytestbox.device.dualbank.boot.imageformat.interface import ImageFormatInterfaceTestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ImageFormatTestSuite(PyHarnessSuite):
    """
    Dual Bank Image Format tests launcher
    """

    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        self.runTest(result, context, ImageFormatInterfaceTestCase)
        self.runTest(result, context, ImageFormatBusinessTestCase)
        self.runTest(result, context, ImageFormatFunctionalityTestCase)
    # end def runTests
# end class ImageFormatTestSuite

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
