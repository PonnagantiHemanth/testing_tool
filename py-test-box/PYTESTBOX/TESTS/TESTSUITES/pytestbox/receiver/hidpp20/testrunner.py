#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.receiver.hidpp20.testrunner
    :brief: Receiver HID++ 2.0 tests runner
    :author: Christophe Roquebert
    :date: 2020/02/19
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.receiver.hidpp20.common.testrunner import ReceiverCommonHidpp20TestSuite
from pytestbox.receiver.hidpp20.important.testrunner import ReceiverImportantHidpp20TestSuite


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ReceiverHidpp20TestSuite(PyHarnessSuite):
    """
    Test runner class for Receiver HID++ 2.0 tests
    """

    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        self.runTest(result, context, ReceiverImportantHidpp20TestSuite)
        self.runTest(result, context, ReceiverCommonHidpp20TestSuite)
    # end def runTests
# end class ReceiverHidpp20TestSuite


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
