#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.receiver.usb.testrunner
:brief: Receiver USB Protocol tests runner
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/01/11
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.receiver.usb.bootprotocol import BootProtocolTestCases
from pytestbox.receiver.usb.descriptors import DescriptorsTestCases


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ReceiverUsbProtocolTestSuite(PyHarnessSuite):
    """
    Receiver Usb Protocol tests launcher
    """

    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        self.runTest(result, context, BootProtocolTestCases)
        self.runTest(result, context, DescriptorsTestCases)
    # end def runTests
# end class ReceiverUsbProtocolTestSuite

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
