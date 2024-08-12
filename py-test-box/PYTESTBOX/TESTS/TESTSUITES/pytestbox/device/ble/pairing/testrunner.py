#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.pairing.testrunner
:brief: BLE pairing tests runner
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2022/09/27
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.ble.pairing.security import PairingSecurityTestCases


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class PairingTestSuite(PyHarnessSuite):
    """
    Device BLE pairing tests launcher
    """

    def runTests(self, result, context):
        # See ``PyHarnessSuite.runTests``
        self.runTest(result, context, PairingSecurityTestCases)
    # end def runTests
# end class PairingTestSuite

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
