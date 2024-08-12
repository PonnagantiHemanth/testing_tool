#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hid.keyboard.analogkeys.testrunner
:brief: ``AnalogKeys`` testrunner implementation
:author: YY Liu <yliu5@logitech.com>
:date: 2024/03/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hid.keyboard.analogkeys.business import AnalogKeysBusinessTestCase
from pytestbox.device.hid.keyboard.analogkeys.functionality import AnalogKeysFunctionalityTestCase
from pytestbox.device.hid.keyboard.analogkeys.robustness import AnalogKeysRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceKeyboardAnalogKeysTestSuite(PyHarnessSuite):
    """
    Define test runner suite for device keyboard analog keys tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.

        :param result: The test result that will collect the results.
        :type result: ``TestResult``
        :param context: The context in which the tests are run.
        :type context: ``Context``
        """
        self.runTest(result, context, AnalogKeysBusinessTestCase)
        self.runTest(result, context, AnalogKeysFunctionalityTestCase)
        self.runTest(result, context, AnalogKeysRobustnessTestCase)
    # end def runTests
# end class DeviceKeyboardAnalogKeysTestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
