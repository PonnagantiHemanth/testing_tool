#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.advertising.business
:brief: Validates BLE advertising Business test cases
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2021/06/23
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.ble.advertising.advertising import AdvertisingApplicationReconnectionModeTestCase
from pytestbox.device.ble.advertising.advertising import AdvertisingBootloaderReconnectionModeTestCase
from pytestbox.device.ble.advertising.advertising import AdvertisingPairingModeTestCase
from pytestbox.device.ble.advertising.advertising import AdvertisingPairingModeUnusedPrepairingDataTestCase
from pytestbox.device.ble.advertising.advertising import AdvertisingPairingModeUsedPrepairingDataTestCase
from pytransport.ble.bleconstants import BleAdvertisingPduType


# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
_AUTHOR = "Stanislas Cottard"


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class AdvertisingPairingModeNoPrepairingDataBusinessTestCase(AdvertisingPairingModeTestCase):
    """
    BLE advertising in pairing mode with no prepairing data Business Test Cases
    """

    @features('BLEProtocol')
    @level('Business')
    @services('BleContext')
    @services('Debugger')
    @bugtracker('AdvertisingShortLocalName')
    def test_business_pairing_mode_application_no_prepairing_data(self):
        """
        Business case for when the device is in application mode, unpaired and with no prepairing data.
        """
        self.common_business_pairing_mode_application()

        self.testCaseChecked("BUS_BLE_ADVERTISING_0001", _AUTHOR)
    # end def test_business_pairing_mode_application_no_prepairing_data
# end class AdvertisingPairingModeNoPrepairingDataBusinessTestCase


class AdvertisingPairingModeUsedPrepairingDataBusinessTestCase(AdvertisingPairingModeUsedPrepairingDataTestCase):
    """
    BLE advertising in pairing mode with used prepairing data Business Test Cases
    """

    @features('BLEProtocol')
    @level('Business')
    @services('BleContext')
    @services('Debugger')
    def test_business_pairing_mode_application_used_prepairing_data(self):
        """
        Business case for when the device is in application mode, unpaired and with used prepairing data.
        """
        self.common_business_pairing_mode_application()

        self.testCaseChecked("BUS_BLE_ADVERTISING_0002", _AUTHOR)
    # end def test_business_pairing_mode_application_used_prepairing_data
# end class AdvertisingPairingModeUsedPrepairingDataBusinessTestCase


class AdvertisingPairingModeUnusedPrepairingDataBusinessTestCase(AdvertisingPairingModeUnusedPrepairingDataTestCase):
    """
    BLE advertising in pairing mode with unused prepairing data Business Test Cases
    """

    @features('BLEProtocol')
    @level('Business')
    @services('BleContext')
    @services('Debugger')
    def test_business_pairing_mode_application_unused_prepairing_data(self):
        """
        Business case for when the device is in application mode, unpaired and with unused prepairing data.
        """
        timeout_scanning = 2 * (
                self.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_UnusedPrepairingInfoRegularAdvertisingSubWindowS +
                self.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_UnusedPrepairingInfoPrepairingAdvertisingSubWindowS
        )
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, f"Enter pairing mode and Scan until current device is found (max {timeout_scanning}s)")
        # ---------------------------------------------------------------------------
        current_device = BleProtocolTestUtils.scan_for_devices_with_entering_pairing_mode_during_scan(test_case=self,
                                                                                                      ble_addresses=[
                                                                                                          self.device_prepairing_ble_address],
                                                                                                      scan_timeout=timeout_scanning,
                                                                                                      send_scan_request=False)[0]

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that the advertising is connectable directed")
        # ---------------------------------------------------------------------------
        self.assertEqual(obtained=current_device.advertising_type,
                         expected=BleAdvertisingPduType.CONNECTABLE_DIRECTED,
                         msg="Advertising should be connectable undirected")

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Connect and bond to the device")
        # ---------------------------------------------------------------------------
        BleProtocolTestUtils.connect_device(test_case=self, ble_context_device=current_device, confirm_connect=True)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self,
                           f"Scan for a duration wide enough to get 2 cycles of regular and prepairing advertising")
        # ---------------------------------------------------------------------------
        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that the device is not advertising anymore")
        # ---------------------------------------------------------------------------
        self.check_device_not_advertising(scan_duration=timeout_scanning)

        self.testCaseChecked("BUS_BLE_ADVERTISING_0003", _AUTHOR)
    # end def test_business_pairing_mode_application_unused_prepairing_data
# end class AdvertisingPairingModeUnusedPrepairingDataBusinessTestCase


class AdvertisingApplicationReconnectionBusinessTestCases(AdvertisingApplicationReconnectionModeTestCase):
    """
    BLE advertising in reconnection mode when the device is on the application Business Test Cases
    """

    @features('BLEProtocol')
    @level('Business', 'SmokeTests')
    @services('BleContext')
    @services('Debugger')
    def test_business_reconnection_application_mode(self):
        """
        Business case for when the device is in paired application mode.
        """
        self.common_business_paired_mode()

        self.testCaseChecked("BUS_BLE_ADVERTISING_0004", _AUTHOR)
    # end def test_business_reconnection_application_mode
# end class AdvertisingApplicationReconnectionBusinessTestCases


@features.class_decorator("BootloaderBLESupport")
class AdvertisingBootloaderReconnectionBusinessTestCases(AdvertisingBootloaderReconnectionModeTestCase):
    """
    BLE advertising in reconnection mode when the device is on the bootloader Business Test Cases
    """

    @features('BLEProtocol')
    @features('BootloaderAvailable')
    @level('Business')
    @services('BleContext')
    @services('Debugger')
    def test_business_reconnection_bootloader_mode(self):
        """
        Business case for when the device is in paired bootloader mode.
        """
        self.common_business_paired_mode()

        self.testCaseChecked("BUS_BLE_ADVERTISING_0005", _AUTHOR)
    # end def test_business_reconnection_bootloader_mode
# end class AdvertisingBootloaderReconnectionBusinessTestCases

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
