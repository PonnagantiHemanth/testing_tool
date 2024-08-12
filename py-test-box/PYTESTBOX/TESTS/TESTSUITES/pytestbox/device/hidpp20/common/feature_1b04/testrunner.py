#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1b04.testrunner
:brief: Device HID++ 2.0 Common feature 0x1b04 testrunner implementation
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/05/11
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_1b04.business import SpecialKeysMSEButtonsBusinessTestCase
from pytestbox.device.hidpp20.common.feature_1b04.business import SpecialKeysMSEButtonsBusinessEmuTestCase
from pytestbox.device.hidpp20.common.feature_1b04.errorhandling import SpecialKeysMSEButtonsErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_1b04.functionality import SpecialKeysMSEButtonsFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_1b04.functionality import SpecialKeysMSEButtonsFunctionalityEmuTestCase
from pytestbox.device.hidpp20.common.feature_1b04.interface import SpecialKeysMSEButtonsInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_1b04.robustness import SpecialKeysMSEButtonsRobustnessTestCase
from pytestbox.device.hidpp20.common.feature_1b04.robustness import SpecialKeysMSEButtonsRobustnessEmuTestCase


# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class DeviceHidpp20Feature1B04TestSuite(PyHarnessSuite):
    """
    Test runner class for HID++ 2.0 feature 0x1B04 tests.
    """
    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, SpecialKeysMSEButtonsInterfaceTestCase)
        self.runTest(result, context, SpecialKeysMSEButtonsBusinessTestCase)
        self.runTest(result, context, SpecialKeysMSEButtonsBusinessEmuTestCase)
        self.runTest(result, context, SpecialKeysMSEButtonsFunctionalityTestCase)
        self.runTest(result, context, SpecialKeysMSEButtonsFunctionalityEmuTestCase)
        self.runTest(result, context, SpecialKeysMSEButtonsErrorHandlingTestCase)
        self.runTest(result, context, SpecialKeysMSEButtonsRobustnessTestCase)
        self.runTest(result, context, SpecialKeysMSEButtonsRobustnessEmuTestCase)
    # end def runTests
# end class DeviceHidpp20Feature1B04TestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
