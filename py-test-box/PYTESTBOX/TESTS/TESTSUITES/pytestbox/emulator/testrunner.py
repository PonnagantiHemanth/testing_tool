#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------
""" @package pytestbox.emulator.testrunner

@brief  Emulator testrunner implementation

@author christophe roquebert

@date   2019/07/08
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.emulator.powersupply import DemoPowerSupplyTestCase

# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------


class EmulatorTestSuite(PyHarnessSuite):
    """
    Test runner class for Emulator tests
    """
    def canRun(self, unusedresult,                                                                                      #pylint:disable=R0201,W8012
                     context):
        """
        @copydoc pyharness.extensions.PyHarnessSuite.canRun
        """
        f = context.getFeatures()
        return f.EMULATOR.F_Enabled
    # end def canRun
    
    def runTests(self, result, context):
        """
        @copydoc pyharness.extensions.PyHarnessSuite.runTests
        """
        self.runTest(result, context, DemoPowerSupplyTestCase)
    # end def runTests
# end class EmulatorTestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
