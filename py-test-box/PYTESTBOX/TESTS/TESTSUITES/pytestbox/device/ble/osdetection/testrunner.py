#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.osdetection.testrunner
:brief: Device BLE Protocol OS Detection tests runner
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2022/07/14
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.ble.osdetection.business import OsDetectionBusinessTestCases
from pytestbox.device.ble.osdetection.errorhandling import OsDetectionErrorHandlingTestCases
from pytestbox.device.ble.osdetection.functionality import OsDetectionFunctionalityTestCases
from pytestbox.device.ble.osdetection.interface import OsDetectionInterfaceTestCases
from pytestbox.device.ble.osdetection.robusteness import OsDetectionRobustnessTestCases


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class BleOsDetectionTestSuite(PyHarnessSuite):
    """
    Device BLE Protocol OS detection tests launcher
    """

    def runTests(self, result, context):
        # See ``PyHarnessSuite.runTests``
        self.runTest(result, context, OsDetectionInterfaceTestCases)
        self.runTest(result, context, OsDetectionErrorHandlingTestCases)
        self.runTest(result, context, OsDetectionFunctionalityTestCases)
        self.runTest(result, context, OsDetectionBusinessTestCases)
        self.runTest(result, context, OsDetectionRobustnessTestCases)
    # end def runTests
# end class BleOsDetectionTestSuite

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
