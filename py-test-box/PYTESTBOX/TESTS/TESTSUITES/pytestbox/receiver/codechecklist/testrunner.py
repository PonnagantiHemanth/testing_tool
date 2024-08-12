#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.receiver.codechecklist.testrunner
:brief: Receiver Code Checklist tests runner
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/06/21
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.receiver.codechecklist.ram import ReceiverRamTestCase
from pytestbox.receiver.codechecklist.stack import ReceiverStackTestCase
from pytestbox.receiver.codechecklist.uicr import ReceiverUICRTestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ReceiverCodeChecklistTestSuite(PyHarnessSuite):
    """
    Receiver Code Checklist tests launcher
    """

    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        self.runTest(result, context, ReceiverRamTestCase)
        self.runTest(result, context, ReceiverUICRTestCase)
        if context.getFeatures().PRODUCT.CODE_CHECKLIST.F_StackVerification:
            self.runTest(result, context, ReceiverStackTestCase)
        # end if
    # end def runTests
# end class ReceiverMemoryTestSuite

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
