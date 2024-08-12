#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------
""" @package pytestbox.hid.emulator.testrunner

@brief  HID common features testrunner implementation

@author Stanislas Cottard

@date   2019/07/03
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.emulator.buttonstimuliemulator import ButtonStimuliEmulatorTestCase
from pytestbox.device.hidpp20.emulator.opticalxydisplacementemulator import OpticalXyDisplacementEmulatorTestCase

# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------


class EmulatorTestSuite(PyHarnessSuite):
    '''
    Test runner class for Emulator tests
    '''
    def runTests(self, result, context):
        '''
        @copydoc pyharness.extensions.PyHarnessSuite.runTests
        '''
        self.runTest(result, context, ButtonStimuliEmulatorTestCase)
        self.runTest(result, context, OpticalXyDisplacementEmulatorTestCase)
    # end def runTests
# end class EmulatorHidTestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
