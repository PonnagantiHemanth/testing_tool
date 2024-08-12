#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.ghostkeys.testrunner
:brief: Device Hid keyboard ghost keys feature testrunner implementation
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/06/25
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hid.keyboard.ghostkeys.functionality import GhostKeysFunctionalityTestCase
from pytestbox.device.hid.keyboard.ghostkeys.robustness import GhostKeysRobustnessTestCase


# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class DeviceHidKeyboardGhostKeysTestSuite(PyHarnessSuite):
    """
    Test runner class for Hid Keyboard Ghost Keys tests.
    """
    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, GhostKeysFunctionalityTestCase)
        self.runTest(result, context, GhostKeysRobustnessTestCase)
    # end def runTests
# end class DeviceHidKeyboardGhostKeysTestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
