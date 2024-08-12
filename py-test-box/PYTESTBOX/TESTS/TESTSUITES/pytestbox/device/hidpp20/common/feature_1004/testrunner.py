#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1004.testrunner
:brief: Device HID++ 2.0 Common feature 0x1004 testrunner implementation
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/05/11
"""
from pychannel.channelinterfaceclasses import LogitechProtocol
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.device.hidpp20.common.feature_1004.business import UnifiedBatteryBusinessGamingTestCase
from pytestbox.device.hidpp20.common.feature_1004.business import UnifiedBatteryBusinessTestCase
from pytestbox.device.hidpp20.common.feature_1004.errorhandling import UnifiedBatteryErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_1004.functionality import UnifiedBatteryFunctionalityGamingTestCase
from pytestbox.device.hidpp20.common.feature_1004.functionality import UnifiedBatteryFunctionalityMultiHostTestCase
from pytestbox.device.hidpp20.common.feature_1004.functionality import UnifiedBatteryFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_1004.functionality import UnifiedBatteryRepeatedBleFunctionalityTestCases
from pytestbox.device.hidpp20.common.feature_1004.interface import UnifiedBatteryInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_1004.robustness import UnifiedBatteryRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature1004TestSuite(PyHarnessSuite):
    """
    Test runner class for HID++ 2.0 feature 0x1004 tests.
    """
    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        config_manager = ConfigurationManager(context.getFeatures())

        self.runTest(result, context, UnifiedBatteryBusinessTestCase)
        self.runTest(result, context, UnifiedBatteryBusinessGamingTestCase)
        self.runTest(result, context, UnifiedBatteryErrorHandlingTestCase)
        self.runTest(result, context, UnifiedBatteryFunctionalityTestCase)
        self.runTest(result, context, UnifiedBatteryFunctionalityMultiHostTestCase)
        self.runTest(result, context, UnifiedBatteryFunctionalityGamingTestCase)
        self.runTest(result, context, UnifiedBatteryInterfaceTestCase)
        self.runTest(result, context, UnifiedBatteryRobustnessTestCase)

        if config_manager.current_protocol != LogitechProtocol.BLE:
            self.runTest(result, context, UnifiedBatteryRepeatedBleFunctionalityTestCases)
        # end if
    # end def runTests
# end class DeviceHidpp20Feature1004TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
