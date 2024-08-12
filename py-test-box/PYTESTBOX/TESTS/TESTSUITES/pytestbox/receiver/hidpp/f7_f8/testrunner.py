#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.hidpp.f7_f8.testrunner
:brief: Receiver HID++ 1.0 feature 0x1602 testrunner implementation
:author: Gautham S B <gsb@logitech.com>
:date: 2022/10/17
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.receiver.hidpp.f7_f8.business import ReceiverPasswordAuthenticationBusinessTestCase
from pytestbox.receiver.hidpp.f7_f8.errorhandling import ReceiverPasswordAuthenticationErrorHandlingTestCase
from pytestbox.receiver.hidpp.f7_f8.functionality import ReceiverPasswordAuthenticationFunctionalityTestCase
from pytestbox.receiver.hidpp.f7_f8.interface import ReceiverPasswordAuthenticationInterfaceTestCase
from pytestbox.receiver.hidpp.f7_f8.robustness import ReceiverPasswordAuthenticationRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ReceiverHidppF7F8TestSuite(PyHarnessSuite):
    """
    Receiver HID++ tests launcher for F7 & F8 registers
    """
    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        self.runTest(result, context, ReceiverPasswordAuthenticationInterfaceTestCase)
        self.runTest(result, context, ReceiverPasswordAuthenticationBusinessTestCase)
        self.runTest(result, context, ReceiverPasswordAuthenticationFunctionalityTestCase)
        self.runTest(result, context, ReceiverPasswordAuthenticationErrorHandlingTestCase)
        self.runTest(result, context, ReceiverPasswordAuthenticationRobustnessTestCase)
    # end def runTests
# end class ReceiverHidppF7F8TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
