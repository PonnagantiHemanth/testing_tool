#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.receiver.hidpp.f9_fa.testrunner
:brief: Receiver HID++ tests runner for F9 & FA registers
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2021/06/08
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.receiver.hidpp.f9_fa.business import \
    ReceiverManageDeactivatableFeaturesAuthBusinessTestCase
from pytestbox.receiver.hidpp.f9_fa.functionality import \
    ReceiverManageDeactivatableFeaturesAuthFunctionalityTestCase
from pytestbox.receiver.hidpp.f9_fa.interface import \
    ReceiverManageDeactivatableFeaturesAuthInterfaceTestCase
from pytestbox.receiver.hidpp.f9_fa.robustness import \
    ReceiverManageDeactivatableFeaturesAuthRobustnessTestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ReceiverHidppF9FATestSuite(PyHarnessSuite):
    """
    Receiver HID++ tests launcher for FA & F9 registers
    """
    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        self.runTest(result, context, ReceiverManageDeactivatableFeaturesAuthInterfaceTestCase)
        self.runTest(result, context, ReceiverManageDeactivatableFeaturesAuthBusinessTestCase)
        self.runTest(result, context, ReceiverManageDeactivatableFeaturesAuthFunctionalityTestCase)
        self.runTest(result, context, ReceiverManageDeactivatableFeaturesAuthRobustnessTestCase)
    # end def runTests
# end class ReceiverHidppF9FATestSuite

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
