#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.common.feature_1807.testrunner
:brief: HID++ 2.0 feature 0x1807 testrunner implementation
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/09/14
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_1807.business import ConfigurablePropertiesBLEBusinessTestCase
from pytestbox.device.hidpp20.common.feature_1807.business import ConfigurablePropertiesBLEProBusinessTestCase
from pytestbox.device.hidpp20.common.feature_1807.business import ConfigurablePropertiesBusinessTestCase
from pytestbox.device.hidpp20.common.feature_1807.business import ConfigurablePropertiesEQuadBusinessTestCase
from pytestbox.device.hidpp20.common.feature_1807.business import ConfigurablePropertiesUSBBusinessTestCase
from pytestbox.device.hidpp20.common.feature_1807.errorhandling import ConfigurablePropertiesErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_1807.functionality import ConfigurablePropertiesFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_1807.interface import ConfigurablePropertiesInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_1807.robustness import ConfigurablePropertiesRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature1807TestSuite(PyHarnessSuite):
    """
    Define test runner suite for common feature 0x1807 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, ConfigurablePropertiesInterfaceTestCase)
        self.runTest(result, context, ConfigurablePropertiesBusinessTestCase)
        self.runTest(result, context, ConfigurablePropertiesBLEProBusinessTestCase)
        self.runTest(result, context, ConfigurablePropertiesBLEBusinessTestCase)
        self.runTest(result, context, ConfigurablePropertiesEQuadBusinessTestCase)
        self.runTest(result, context, ConfigurablePropertiesUSBBusinessTestCase)
        self.runTest(result, context, ConfigurablePropertiesFunctionalityTestCase)
        self.runTest(result, context, ConfigurablePropertiesErrorHandlingTestCase)
        self.runTest(result, context, ConfigurablePropertiesRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature1807TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
