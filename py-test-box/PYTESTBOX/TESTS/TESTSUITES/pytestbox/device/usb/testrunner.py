#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.usb.testrunner
:brief: Device USB Protocol tests runner
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/01/11
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.usb.descriptors import DescriptorsTestCases


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class DeviceUsbProtocolTestSuite(PyHarnessSuite):
    """
    Device Usb Protocol tests launcher
    """

    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        self.runTest(result, context, DescriptorsTestCases)
    # end def runTests
# end class DeviceUsbProtocolTestSuite

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
