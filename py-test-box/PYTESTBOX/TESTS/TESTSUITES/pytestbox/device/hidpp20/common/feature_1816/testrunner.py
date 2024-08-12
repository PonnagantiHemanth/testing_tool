#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1816.testrunner
:brief: Device HID++ 2.0 Common feature 0x1816 testrunner implementation
:author: Alexandre Lafaye <alafaye@logitech.com>
:date: 2022/06/22
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_1816.business import BleProPrePairingBusinessTestCase
from pytestbox.device.hidpp20.common.feature_1816.errorhandling import BleProPrePairingErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_1816.functionality import BleProPrePairingFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_1816.interface import BleProPrePairingInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_1816.robustness import BleProPrePairingRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Alexandre Lafaye"


# ----------------------------------------------------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature1816TestSuite(PyHarnessSuite):
    """
    Test runner class for HID++ 2.0 feature 0x1816 tests
    """
    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        self.runTest(result, context, BleProPrePairingInterfaceTestCase)
        self.runTest(result, context, BleProPrePairingBusinessTestCase)
        self.runTest(result, context, BleProPrePairingFunctionalityTestCase)
        self.runTest(result, context, BleProPrePairingErrorHandlingTestCase)
        self.runTest(result, context, BleProPrePairingRobustnessTestCase)

    # end def runTests
# end class DeviceHidpp20Feature1816TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
