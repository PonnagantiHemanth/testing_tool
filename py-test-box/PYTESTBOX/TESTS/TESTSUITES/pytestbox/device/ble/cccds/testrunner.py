#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.testrunner
:brief: BLE++ service CCCD toggling tests runner
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/09/06
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.ble.cccds.business import BleppCccdToggledBusinessTestCases


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class BleppCccdToggledTestSuite(PyHarnessSuite):
    """
    Device BLE++ service CCCD toggling tests launcher
    """

    def runTests(self, result, context):
        # See ``PyHarnessSuite.runTests``
        self.runTest(result, context, BleppCccdToggledBusinessTestCases)
    # end def runTests
# end class BleppCccdToggledTestSuite


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
