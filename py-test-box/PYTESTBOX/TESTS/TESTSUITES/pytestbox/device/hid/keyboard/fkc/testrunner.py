#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.fkc.testrunner
:brief: Device Hid keyboard FKC feature testrunner implementation
:author: Fred Chen <fchen7@logitech.com>
:date: 2023/03/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hid.keyboard.fkc.business import FKCBusinessTestCase
from pytestbox.device.hid.keyboard.fkc.functionality import FKCFunctionalityTestCase
from pytestbox.device.hid.keyboard.fkc.robustness import FKCRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidKeyboardFKCTestSuite(PyHarnessSuite):
    """
    Test runner class for Hid Keyboard Full Key Customization tests.
    """
    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, FKCBusinessTestCase)
        self.runTest(result, context, FKCFunctionalityTestCase)
        self.runTest(result, context, FKCRobustnessTestCase)
    # end def runTests
# end class DeviceHidKeyboardFKCTestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
