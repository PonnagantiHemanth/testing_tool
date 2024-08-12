#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.connection_parameters.business
:brief: Validate BLE connection parameters Business test cases
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2023/05/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import skip

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pylibrary.mcu.nrf52.blenvschunks import BleNvsChunks
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleconnectionparametersutils import BleConnectionParametersTestUtils
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.ble.connection_parameters.connectionparameters import ConnectionParametersTestCases

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Sylvana Ieri"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ConnectionParametersBusinessTestCases(ConnectionParametersTestCases):
    @features('BLEProtocol')
    @level('Business', 'SmokeTests')
    @services('BleContext')
    @services('Debugger')
    def test_correct_connection_parameters_windows(self):
        """
        Verify that a connection and a bonding do not trigger a Connection Parameters Update Request when the
        connection parameters are the right one from the start for any OS but iOS/iPadOS
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text="Change host OS emulation to windows")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_os_emulation = True
        BleProtocolTestUtils.change_host_os_emulation(self, os_emulation_type=BleNvsChunks.OsDetectedType.UNDETERMINED)

        self._generic_test_correct_connection_parameters(
            correct_parameters=True,
            connection_parameters=BleConnectionParametersTestUtils.get_default_os_connection_parameters(test_case=self))

        self.testCaseChecked("BUS_BLE_CONN_PARAM_0001", _AUTHOR)
    # end def test_correct_connection_parameters_windows

    @features('BLEProtocol')
    @level('Business')
    @services('BleContext')
    @services('Debugger')
    def test_correct_connection_parameters_osx(self):
        """
        Verify that a connection and a bonding do not trigger a Connection Parameters Update Request when the
        connection parameters are the right one from the start for any OS but iOS/iPadOS
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text="Change host OS emulation to OsX")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_os_emulation = True
        BleProtocolTestUtils.change_host_os_emulation(self, os_emulation_type=BleNvsChunks.OsDetectedType.OSX)

        self._generic_test_correct_connection_parameters(
            correct_parameters=True,
            connection_parameters=BleConnectionParametersTestUtils.get_default_os_connection_parameters(test_case=self))

        self.testCaseChecked("BUS_BLE_CONN_PARAM_0002", _AUTHOR)
    # end def test_correct_connection_parameters_osx

    @features('BLEProtocol')
    @level('Business')
    @services('BleContext')
    @services('Debugger')
    @skip("enable when os emulation Android is implemented")
    def test_correct_connection_parameters_android(self):
        """
        Verify that a connection and a bonding do not trigger a Connection Parameters Update Request when the
        connection parameters are the right one from the start for any OS but iOS/iPadOS

        note: disabled TODO: enable when os emulation Android is implemented
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text="Change host OS emulation to Android")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_os_emulation = True
        BleProtocolTestUtils.change_host_os_emulation(self, os_emulation_type=BleNvsChunks.OsDetectedType.ANDROID)

        self._generic_test_correct_connection_parameters(
            correct_parameters=True,
            connection_parameters=BleConnectionParametersTestUtils.get_default_os_connection_parameters(test_case=self))

        self.testCaseChecked("BUS_BLE_CONN_PARAM_0003", _AUTHOR)
    # end def test_correct_connection_parameters_android

    @features('BLEProtocol')
    @level('Business')
    @services('BleContext')
    @services('Debugger')
    def test_correct_connection_parameters_chrome(self):
        """
        Verify that a connection and a bonding do not trigger a Connection Parameters Update Request when the
        connection parameters are the right one from the start for any OS but iOS/iPadOS
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text="Change host OS emulation to Chrome OS")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_os_emulation = True
        BleProtocolTestUtils.change_host_os_emulation(self, os_emulation_type=BleNvsChunks.OsDetectedType.CHROME)

        self._generic_test_correct_connection_parameters(
            correct_parameters=True,
            connection_parameters=BleConnectionParametersTestUtils.get_default_os_connection_parameters(test_case=self))

        self.testCaseChecked("BUS_BLE_CONN_PARAM_0004", _AUTHOR)
    # end def test_correct_connection_parameters_chrome
# end class ConnectionParametersBusinessTestCases

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
