#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.connection_parameters.testrunner
:brief: BLE connection parameters tests runner
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2022/09/27
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.device.ble.connection_parameters.business import ConnectionParametersBusinessTestCases
from pytestbox.device.ble.connection_parameters.functionality import \
    ConnectionParametersFunctionalityApplicationReconnectionTestCases
from pytestbox.device.ble.connection_parameters.functionality import \
    ConnectionParametersFunctionalityBootloaderReconnectionTestCases
from pytestbox.device.ble.connection_parameters.functionality import \
    ConnectionParametersFunctionalityFirstConnectionTestCases
from pytestbox.device.ble.connection_parameters.interface import ConnectionParametersInterfaceBootloaderTestCases
from pytestbox.device.ble.connection_parameters.interface import ConnectionParametersInterfaceApplicationTestCases
from pytestbox.device.ble.connection_parameters.robustness import \
    ConnectionParametersRobustnessApplicationFirstConnectionTestCases
from pytestbox.device.ble.connection_parameters.robustness import \
    ConnectionParametersRobustnessApplicationReconnectionTestCases
from pytestbox.device.ble.connection_parameters.robustness import \
    ConnectionParametersRobustnessBootloaderReconnectionTestCases


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ConnectionParametersTestSuite(PyHarnessSuite):
    """
    Device BLE connection parameters tests launcher
    """

    def runTests(self, result, context):
        # See ``PyHarnessSuite.runTests``
        self.runTest(result, context, ConnectionParametersInterfaceApplicationTestCases)
        self.runTest(result, context, ConnectionParametersBusinessTestCases)
        self.runTest(result, context, ConnectionParametersFunctionalityFirstConnectionTestCases)
        self.runTest(result, context, ConnectionParametersFunctionalityApplicationReconnectionTestCases)
        self.runTest(result, context, ConnectionParametersRobustnessApplicationFirstConnectionTestCases)
        self.runTest(result, context, ConnectionParametersRobustnessApplicationReconnectionTestCases)

        config_manager = ConfigurationManager(context.getFeatures())
        if config_manager.feature_value_map[config_manager.ID.TRANSPORT_BTLE][config_manager.MODE.BOOTLOADER]:
            self.runTest(result, context, ConnectionParametersInterfaceBootloaderTestCases)
            self.runTest(result, context, ConnectionParametersFunctionalityBootloaderReconnectionTestCases)
            self.runTest(result, context, ConnectionParametersRobustnessBootloaderReconnectionTestCases)
        # end if
    # end def runTests
# end class ConnectionParametersTestSuite

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
