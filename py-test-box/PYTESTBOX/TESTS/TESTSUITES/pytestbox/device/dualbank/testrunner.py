#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.dualbank.testrunner
:brief: Device Dual Bank tests runner
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2022/11/21
"""

# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.dualbank.boot.testrunner import DualBankBootTestSuite


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceDualBankTestSuite(PyHarnessSuite):
    """
    Device Dual Bank tests launcher
    """

    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        self.runTest(result, context, DualBankBootTestSuite)
    # end def runTests
# end class DeviceDualBankTestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
