#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.connection_parameters.interface
:brief: Validate BLE connection parameters Interface test cases
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2022/09/27
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pylibrary.mcu.nrf52.blenvschunks import BleNvsChunks
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleconnectionparametersutils import BleConnectionParametersTestUtils
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.ble.connection_parameters.connectionparameters import \
    ConnectionParametersBootloaderReconnectionTestCases
from pytestbox.device.ble.connection_parameters.connectionparameters import ConnectionParametersTestCases

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
_AUTHOR = "Stanislas Cottard"


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ConnectionParametersInterfaceApplicationTestCases(ConnectionParametersTestCases):
    """
    BLE connection parameters Interface Test Cases in application
    """


    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_correct_connection_parameters_any_os_not_ios_ipados(self):
        """
        Verify that a connection and a bonding do not trigger a Connection Parameters Update Request when the
        connection parameters are the right one from the start for any OS but iOS/iPadOS
        """
        self._generic_test_correct_connection_parameters(
            correct_parameters=True,
            connection_parameters=BleConnectionParametersTestUtils.get_default_os_connection_parameters(test_case=self))

        self.testCaseChecked("INT_BLE_CONN_PARAM_0001", _AUTHOR)
    # end def test_correct_connection_parameters_any_os_not_ios_ipados

    @features('BLESpacesSpecification')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_correct_connection_parameters_ios_ipados(self):
        """
        Verify that a connection and a bonding trigger only one Connection Parameters Update Request when the
        connection parameters are the right one from the start for any OS but iOS/iPadOS.

        A ticket is open on the fact that a change request is always receive even if the connection parameters are
        the right one: https://jira.logitech.io/browse/BT-430
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text="Change host OS emulation to IOS")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_os_emulation = True
        BleProtocolTestUtils.change_host_os_emulation(self, os_emulation_type=BleNvsChunks.OsDetectedType.IOS)

        self._generic_test_correct_connection_parameters(
            correct_parameters=True,
            connection_parameters=BleConnectionParametersTestUtils.get_ios_ipados_connection_parameters(test_case=self),
            one_request_present=True)

        self.testCaseChecked("INT_BLE_CONN_PARAM_0002", _AUTHOR)
    # end def test_correct_connection_parameters_ios_ipados

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_incorrect_connection_parameters(self):
        """
        Verify that a connection and a bonding trigger a Connection Parameters Update Request when the
        connection parameters are incorrect from the start for any OS
        """
        self._generic_test_correct_connection_parameters(
            correct_parameters=False,
            connection_parameters=BleConnectionParametersTestUtils.get_any_os_incorrect_connection_parameters(
                test_case=self))

        self.testCaseChecked("INT_BLE_CONN_PARAM_0003", _AUTHOR)
    # end def test_incorrect_connection_parameters
# end class ConnectionParametersInterfaceApplicationTestCases


@features.class_decorator("BootloaderBLESupport")
class ConnectionParametersInterfaceBootloaderTestCases(ConnectionParametersBootloaderReconnectionTestCases):
    """
    BLE connection parameters Interface Test Cases In bootloader mode
    """

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_correct_connection_parameters_bootloader(self):
        """
        Verify that a connection and a bonding do not trigger a Connection Parameters Update Request when the
        connection parameters are the right one from the start for any bootloader
        """
        parameters = BleConnectionParametersTestUtils.get_bootloader_connection_parameters(test_case=self)
        self._generic_test_correct_connection_parameters(
            correct_parameters=True,
            connection_parameters=parameters)

        self.testCaseChecked("INT_BLE_CONN_PARAM_0003", _AUTHOR)
    # end def test_correct_connection_parameters_bootloader

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_incorrect_connection_parameters(self):
        """
        Verify that a connection and a bonding trigger a Connection Parameters Update Request when the
        connection parameters are incorrect from the start for any OS
        """
        self._generic_test_correct_connection_parameters(
            correct_parameters=False,
            connection_parameters=BleConnectionParametersTestUtils.get_any_os_incorrect_connection_parameters(
                test_case=self))

        self.testCaseChecked("INT_BLE_CONN_PARAM_0003", _AUTHOR)
    # end def test_incorrect_connection_parameters
# end class ConnectionParametersInterfaceBootloaderTestCases

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
