#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.advertising.functionality
:brief: Validates BLE advertising Functionality test cases
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2021/06/23
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.bleprotocolutils import MAX_ADVERTISING_INTERVAL_DIRECTED_HDC
from pytestbox.device.ble.advertising.advertising import AdvertisingApplicationReconnectionModeTestCase
from pytestbox.device.ble.advertising.advertising import AdvertisingBootloaderReconnectionModeTestCase
from pytestbox.device.ble.advertising.advertising import AdvertisingPairingModeTestCase

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
_AUTHOR = "Stanislas Cottard"


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class AdvertisingPairingModeNoPrepairingDataFunctionalityTestCases(AdvertisingPairingModeTestCase):
    """
    BLE advertising in pairing mode with no prepairing data Functionality Test Cases
    """

    @features('BLEProtocol')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_advertising_stops_after_connect_pairing_mode_application(self):
        """
        Verify that the advertising stops after connection when the device is in application mode and unpaired.
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Enter Pairing mode and scan until current device is found (max 2s) with scan request")
        # ---------------------------------------------------------------------------
        current_device = BleProtocolTestUtils.scan_for_current_device_with_entering_pairing_mode_during_scan(
            test_case=self, scan_timeout=2, send_scan_request=True)

        advertising_interval = max(self.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_SecondAdvertisingIntervalMs,
                                   self.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_SecondAdvertisingIntervalMs)
        self._connect_and_check_no_advertising(current_device=current_device, advertising_interval=advertising_interval)

        self.testCaseChecked("FUN_BLE_ADVERTISING_0001", _AUTHOR)
    # end def test_advertising_stops_after_connect_pairing_mode_application
# end class AdvertisingPairingModeNoPrepairingDataFunctionalityTestCases


class AdvertisingApplicationReconnectionFunctionalityTestCases(AdvertisingApplicationReconnectionModeTestCase):
    """
    BLE advertising in reconnection mode when the device is on the application Functionality Test Cases
    """

    @features('BLEProtocol')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_advertising_stops_at_reconnection_application(self):
        """
        Verify that the advertising stops after connection when the device is in paired application mode.
        """
        self.trigger()
        self._connect_and_check_no_advertising(current_device=self.current_channel.get_ble_context_device(),
                                               advertising_interval=MAX_ADVERTISING_INTERVAL_DIRECTED_HDC)

        self.testCaseChecked("FUN_BLE_ADVERTISING_0002", _AUTHOR)
    # end def test_advertising_stops_at_reconnection_application
# end class AdvertisingApplicationReconnectionFunctionalityTestCases


@features.class_decorator("BootloaderBLESupport")
class AdvertisingBootloaderReconnectionFunctionalityTestCases(AdvertisingBootloaderReconnectionModeTestCase):
    """
    BLE advertising in reconnection mode when the device is on the bootloader Functionality Test Cases
    """

    @features('BLEProtocol')
    @features('BootloaderAvailable')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_advertising_stops_at_reconnection_bootloader(self):
        """
        Verify that the advertising stops after connection when the device is in paired bootloader mode.
        """
        self.trigger()
        self._connect_and_check_no_advertising(current_device=self.current_channel.get_ble_context_device(),
                                               advertising_interval=MAX_ADVERTISING_INTERVAL_DIRECTED_HDC)

        self.testCaseChecked("FUN_BLE_ADVERTISING_0003", _AUTHOR)
    # end def test_advertising_stops_at_reconnection_bootloader
# end class AdvertisingBootloaderReconnectionFunctionalityTestCases

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
