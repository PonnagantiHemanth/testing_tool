#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.dualbank.boot.testrunner
:brief: Device Dual Bank Boot tests runner
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2022/11/21
"""

# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.dualbank.boot.bootloaderimagecommunication.testrunner import BootloaderImageCommunicationTestSuite
from pytestbox.device.dualbank.boot.imageformat.testrunner import ImageFormatTestSuite


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DualBankBootTestSuite(PyHarnessSuite):
    """
    Dual Bank Boot tests launcher
    """

    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        self.runTest(result, context, ImageFormatTestSuite)
        self.runTest(result, context, BootloaderImageCommunicationTestSuite)
    # end def runTests
# end class DualBankBootTestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
