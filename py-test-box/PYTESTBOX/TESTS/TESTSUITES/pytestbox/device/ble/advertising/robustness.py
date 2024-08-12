#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.advertising.robustness
:brief: Validates BLE advertising Robustness test cases
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2021/06/23
"""

# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pychannel.logiconstants import BleAdvertisingSeries
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.bleprotocolutils import EXTRA_SCAN_TIME
from pytestbox.device.ble.advertising.advertising import AdvertisingApplicationReconnectionModeTestCase
from pytestbox.device.ble.advertising.advertising import AdvertisingBootloaderReconnectionModeTestCase
from pytestbox.device.ble.advertising.advertising import AdvertisingPairingModeTestCase
from pytestbox.device.ble.advertising.advertising import AdvertisingPairingModeUnusedPrepairingDataTestCase
from pytestbox.device.ble.advertising.advertising import AdvertisingPairingModeUsedPrepairingDataTestCase


# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
_AUTHOR = "Stanislas Cottard"


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class AdvertisingPairingModeNoPrepairingDataRobustnessTestCases(AdvertisingPairingModeTestCase):
    """
    BLE advertising in pairing mode with no prepairing data Robustness Test Cases
    """

    @features('BLEProtocol')
    @level('ReleaseCandidate')
    @services('BleContext')
    @services('Debugger')
    def test_advertising_interval_robustness_pairing_mode_application_no_prepairing_data(self):
        """
        Verify all advertising intervals for the entire duration of the advertising window when the device is in
        application mode, unpaired and have no prepairing data.
        """
        # An extra time is added to the second window to be sure to get all the advertising packets
        self._test_advertising_interval(
            expected_series=BleProtocolTestUtils.get_expected_series_application_pairing(self), check_all=True)

        self.testCaseChecked("ROB_BLE_ADVERTISING_0001", _AUTHOR)
    # end def test_advertising_interval_robustness_pairing_mode_application_no_prepairing_data

    @features('BLEProtocol')
    @level('Robustness')
    @services('BleContext')
    @services('Debugger')
    @bugtracker('AdvertisingShortLocalName')
    def test_advertising_sequence_pairing_mode_application_no_prepairing_data(self):
        """
        Verify advertising match the expected sequence defined by the series
        """
        expected_series = BleProtocolTestUtils.get_expected_series_application_pairing(self)
        duration = BleProtocolTestUtils.get_scan_time(expected_series)
        self._test_advertising_sequence(expected_series, duration, pairing=True, prepairing=False)

        self.testCaseChecked("ROB_BLE_ADVERTISING_0006", _AUTHOR)
    # end def test_advertising_sequence_pairing_mode_application_no_prepairing_data

# end class AdvertisingPairingModeNoPrepairingDataRobustnessTestCases


class AdvertisingPairingModeUnusedPrepairingDataRobustnessTestCase(
        AdvertisingPairingModeUnusedPrepairingDataTestCase):
    """
    BLE advertising in pairing mode with unused prepairing data Robustness Test Cases
    """

    @features('BLEProtocol')
    @level('ReleaseCandidate')
    @services('BleContext')
    @services('Debugger')
    def test_advertising_interval_robustness_pairing_mode_application_unused_prepairing_data(self):
        """
        Verify all advertising interval when the device is in application mode and unpaired but with unused
        prepairing information
        """
        expected_series = BleProtocolTestUtils.get_expected_series_application_pairing(self, prepairing=True)

        address_current_device = BleProtocolTestUtils.increment_address(self)
        self._test_advertising_interval(expected_series=expected_series,
                                        ble_addresses=[self.device_prepairing_ble_address, address_current_device],
                                        check_all=True)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check that the device is back on the first known host")
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(test_case=self)

        self.testCaseChecked("ROB_BLE_ADVERTISING_0002", _AUTHOR)
    # end def test_advertising_interval_robustness_pairing_mode_application_unused_prepairing_data

    @features('BLEProtocol')
    @level('ReleaseCandidate')
    @services('BleContext')
    @services('Debugger')
    def test_advertising_sequence_pairing_mode_application_unused_prepairing_data(self):
        """
        Verify advertising for prepairing appear in the whole advertising procedure when the device is in application
        mode and unpaired but with unused prepairing information.
        """
        prepairing = True
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, f"Scan for the entire advertising window plus {EXTRA_SCAN_TIME}s")
        # ---------------------------------------------------------------------------
        expected_series = BleProtocolTestUtils.get_expected_series_application_pairing(self, prepairing=prepairing)
        entire_window = BleProtocolTestUtils.get_scan_time(expected_series)

        self._test_advertising_sequence(expected_series, entire_window, True, prepairing)

        self.testCaseChecked("ROB_BLE_ADVERTISING_0003", _AUTHOR)
    # end def test_advertising_sequence_pairing_mode_application_unused_prepairing_data
# end class AdvertisingPairingModeUnusedPrepairingDataRobustnessTestCase

class AdvertisingPairingModeUsedPrepairingDataRobustnessTestCase(
    AdvertisingPairingModeUsedPrepairingDataTestCase):
    """
    BLE advertising in pairing mode with used prepairing data Robustness Test Cases
    """

    @features('BLEProtocol')
    @level('ReleaseCandidate')
    @services('BleContext')
    @services('Debugger')
    def test_advertising_sequence_pairing_mode_application_used_prepairing_data(self):
        """
        Verify advertising match the expected sequence defined by the series
        """
        expected_series = BleProtocolTestUtils.get_expected_series_application_pairing(self)
        entire_window = BleProtocolTestUtils.get_scan_time(expected_series)

        self._test_advertising_sequence(expected_series, entire_window, True)

        self.testCaseChecked("ROB_BLE_ADVERTISING_0007", _AUTHOR)
    # end def test_advertising_sequence_pairing_mode_application_used_prepairing_data
# end class AdvertisingPairingModeUsedPrepairingDataRobustnessTestCase


class AdvertisingApplicationReconnectionModeRobustnessTestCase(AdvertisingApplicationReconnectionModeTestCase):
    """
    BLE advertising in reconnection mode when the device is on the application Robustness Test Cases
    """

    @features('BLEProtocol')
    @level('ReleaseCandidate')
    @services('BleContext')
    @services('Debugger')
    def test_advertising_interval_during_reconnection_application_mode(self):
        """
        Verify all advertising intervals for the entire duration of the advertising window when the device is in
        paired application mode.
        """
        # An extra time is added to the second window to be sure to get all the advertising packets
        self._test_advertising_interval(expected_series=[BleAdvertisingSeries.G],
                                        ble_addresses=[self.current_channel.get_device_ble_address()], check_all=True)

        self.testCaseChecked("ROB_BLE_ADVERTISING_0004", _AUTHOR)
    # end def test_advertising_interval_during_reconnection_application_mode
# end class AdvertisingApplicationReconnectionModeRobustnessTestCase


class AdvertisingBootloaderReconnectionModeRobustnessTestCase(AdvertisingBootloaderReconnectionModeTestCase):
    """
    BLE advertising in reconnection mode when the device is on the bootloader Robustness Test Cases
    """

    @features('BLEProtocol')
    @features('BootloaderAvailable')
    @level('ReleaseCandidate')
    @services('BleContext')
    @services('Debugger')
    def test_advertising_interval_during_reconnection_bootloader_mode(self):
        """
        Verify all advertising intervals for the entire duration of the advertising window when the device is in
        paired bootloader mode.
        """
        expected_series = [BleAdvertisingSeries.I, BleAdvertisingSeries.J, BleAdvertisingSeries.K]

        self._test_advertising_interval(expected_series=expected_series,
                                        ble_addresses=[self.current_channel.get_device_ble_address()], check_all=True,
                                        max_scan_time=40)

        self.testCaseChecked("ROB_BLE_ADVERTISING_0005", _AUTHOR)
    # end def test_advertising_interval_during_reconnection_bootloader_mode
# end class AdvertisingBootloaderReconnectionModeRobustnessTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
