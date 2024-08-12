#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.dualbank.boot.bootloaderimagecommunication.testrunner
:brief: Device Dual Bank Boot Bootloader Image Communication tests runner
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2022/11/21
"""

# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.dualbank.boot.bootloaderimagecommunication.business import \
    BootloaderImageCommunicationBusinessTestCase
from pytestbox.device.dualbank.boot.bootloaderimagecommunication.functionality import \
    BootloaderImageCommunicationFunctionalityTestCase
from pytestbox.device.dualbank.boot.bootloaderimagecommunication.interface import \
    BootloaderImageCommunicationInterfaceTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BootloaderImageCommunicationTestSuite(PyHarnessSuite):
    """
    Dual Bank Bootloader Image Communication tests launcher
    """

    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        self.runTest(result, context, BootloaderImageCommunicationInterfaceTestCase)
        self.runTest(result, context, BootloaderImageCommunicationBusinessTestCase)
        self.runTest(result, context, BootloaderImageCommunicationFunctionalityTestCase)
    # end def runTests
# end class BootloaderImageCommunicationTestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
