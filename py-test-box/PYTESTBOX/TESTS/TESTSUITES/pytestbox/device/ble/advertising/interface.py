#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.advertising.interface
:brief: Validates BLE advertising Interface test cases
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
from pytestbox.device.base.bleprotocolutils import ADVERTISING_DURATION_TOLERANCE
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.bleprotocolutils import EXTRA_SCAN_TIME
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

N_INTERVAL_FOR_AVERAGE = 100

BOOTLOADER_RECONNECTION_DURATION_ERROR_OFFSET = 8  # Observed offset, reported in https://jira.logitech.io/browse/BT-573

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class AdvertisingPairingModeNoPrepairingDataInterfaceTestCase(AdvertisingPairingModeTestCase):
    """
    BLE advertising in pairing mode with no prepairing data Interface Test Cases
    """

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_advertising_type_pairing_mode_application_no_prepairing_data(self):
        """
        Verify the advertising type when the device is in application mode, unpaired and have no prepairing data.
        """
        self._test_advertising_type(expected_type=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
                                    scanning_timeout=EXTRA_SCAN_TIME)

        self.testCaseChecked("INT_BLE_ADVERTISING_0001", _AUTHOR)
    # end def test_advertising_type_pairing_mode_application_no_prepairing_data

    @features('BLEProtocol')
    @level('Time-consuming')
    @services('BleContext')
    @services('Debugger')
    def test_advertising_duration_pairing_mode_application_no_prepairing_data(self):
        """
        Verify the advertising duration when the device is in application mode, unpaired and have no prepairing data.
        """
        duration = BleProtocolTestUtils.get_scan_time(
            BleProtocolTestUtils.get_expected_series_application_pairing(self, prepairing=False))
        self._test_advertising_duration(expected_duration=duration,
                                        accepted_error=duration * ADVERTISING_DURATION_TOLERANCE / 100,
                                        verify_reconnection=False)

        self.testCaseChecked("INT_BLE_ADVERTISING_0002", _AUTHOR)
    # end def test_advertising_duration_pairing_mode_application_no_prepairing_data

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_advertising_interval_pairing_mode_application_no_prepairing_data(self):
        """
        Verify the advertising interval when the device is in application mode, unpaired and have no prepairing data.
        """
        expected_series = BleProtocolTestUtils.get_expected_series_application_pairing(self, prepairing=False)
        duration = BleProtocolTestUtils.get_scan_time_number_of_interval_for_each_series(
            expected_series, N_INTERVAL_FOR_AVERAGE)
        self._test_advertising_interval(expected_series=expected_series, max_scan_time=duration)

        self.testCaseChecked("INT_BLE_ADVERTISING_0003", _AUTHOR)
    # end def test_advertising_interval_pairing_mode_application_no_prepairing_data

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    @bugtracker('AdvertisingShortLocalName')
    def test_advertising_packet_content_pairing_mode_application_no_prepairing_data(self):
        """
        Verify the advertising packet content when the device is in application mode, unpaired and have no prepairing
        data.
        """
        self.common_advertising_packet_content_pairing_mode_application()

        self.testCaseChecked("INT_BLE_ADVERTISING_0004", _AUTHOR)
    # end def test_advertising_packet_content_pairing_mode_application_no_prepairing_data

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_scan_response_content_pairing_mode_application_no_prepairing_data(self):
        """
        Verify the scan response content when the device is in application mode, unpaired and have no prepairing
        data.
        """
        expected_series = BleProtocolTestUtils.get_expected_series_application_pairing(self)
        self.common_scan_response_content_pairing_mode_application(expected_series)

        self.testCaseChecked("INT_BLE_ADVERTISING_0005", _AUTHOR)
    # end def test_scan_response_content_pairing_mode_application_no_prepairing_data
# end class AdvertisingPairingModeNoPrepairingDataInterfaceTestCase


class AdvertisingPairingModeUsedPrepairingDataInterfaceTestCase(AdvertisingPairingModeUsedPrepairingDataTestCase):
    """
    BLE advertising in pairing mode with used prepairing data Interface Test Cases
    """

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_advertising_type_pairing_mode_application_used_prepairing_data(self):
        """
        Verify the advertising type when the device is in application mode, unpaired and have used prepairing data.
        """
        self._test_advertising_type(expected_type=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
                                    scanning_timeout=EXTRA_SCAN_TIME)

        self.testCaseChecked("INT_BLE_ADVERTISING_0006", _AUTHOR)
    # end def test_advertising_type_pairing_mode_application_used_prepairing_data

    @features('BLEProtocol')
    @level('Time-consuming')
    @services('BleContext')
    @services('Debugger')
    def test_advertising_duration_pairing_mode_application_used_prepairing_data(self):
        """
        Verify the advertising duration when the device is in application mode, unpaired and have used prepairing data.
        """
        duration = BleProtocolTestUtils.get_scan_time(BleProtocolTestUtils.get_expected_series_application_pairing(self))
        self._test_advertising_duration(expected_duration=duration,
                                        accepted_error=duration * ADVERTISING_DURATION_TOLERANCE / 100)

        self.testCaseChecked("INT_BLE_ADVERTISING_0007", _AUTHOR)
    # end def test_advertising_duration_pairing_mode_application_used_prepairing_data

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_advertising_interval_pairing_mode_application_used_prepairing_data(self):
        """
        Verify the advertising interval when the device is in application mode, unpaired and have used prepairing data.
        """
        expected_series = BleProtocolTestUtils.get_expected_series_application_pairing(self, prepairing=False)
        duration = BleProtocolTestUtils.get_scan_time_number_of_interval_for_each_series(expected_series,
                                                                                         N_INTERVAL_FOR_AVERAGE)
        self._test_advertising_interval(expected_series=expected_series, max_scan_time=duration)

        self.testCaseChecked("INT_BLE_ADVERTISING_0008", _AUTHOR)
    # end def test_advertising_interval_pairing_mode_application_used_prepairing_data

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_advertising_packet_content_pairing_mode_application_used_prepairing_data(self):
        """
        Verify the advertising packet content when the device is in application mode, unpaired and have used prepairing
        data.
        """
        self.common_advertising_packet_content_pairing_mode_application()

        self.testCaseChecked("INT_BLE_ADVERTISING_0009", _AUTHOR)
    # end def test_advertising_packet_content_pairing_mode_application_used_prepairing_data

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_scan_response_content_pairing_mode_application_used_prepairing_data(self):
        """
        Verify the scan response content when the device is in application mode, unpaired and have used prepairing data.
        """
        expected_series = BleProtocolTestUtils.get_expected_series_application_pairing(self)
        self.common_scan_response_content_pairing_mode_application(expected_series)

        self.testCaseChecked("INT_BLE_ADVERTISING_0010", _AUTHOR)
    # end def test_scan_response_content_pairing_mode_application_used_prepairing_data
# end class AdvertisingPairingModeUsedPrepairingDataInterfaceTestCase


class AdvertisingPairingModeUnusedPrepairingDataInterfaceTestCase(AdvertisingPairingModeUnusedPrepairingDataTestCase):
    """
    BLE advertising in pairing mode with unused prepairing data Interface Test Cases
    """

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_advertising_type_pairing_mode_application_unused_prepairing_data(self):
        """
        Verify the advertising type when the device is in application mode, unpaired and have unused prepairing data.
        """
        expected_series = [BleAdvertisingSeries.D]
        timeout_scanning = BleProtocolTestUtils.get_scan_time_one_window_each_series(expected_series)
        self._test_advertising_type(expected_type=BleAdvertisingPduType.CONNECTABLE_DIRECTED,
                                    scanning_timeout=timeout_scanning,
                                    ble_addresses=[self.device_prepairing_ble_address])

        self.testCaseChecked("INT_BLE_ADVERTISING_0011", _AUTHOR)
    # end def test_advertising_type_pairing_mode_application_unused_prepairing_data

    @features('BLEProtocol')
    @level('Time-consuming')
    @services('BleContext')
    @services('Debugger')
    def test_advertising_duration_pairing_mode_application_unused_prepairing_data(self):
        """
        Verify the advertising duration when the device is in application mode, unpaired and have unused prepairing
        data.
        """
        expected_series = BleProtocolTestUtils.get_expected_series_application_pairing(self, prepairing=True)
        current_address = BleProtocolTestUtils.increment_address(test_case=self)
        duration = BleProtocolTestUtils.get_scan_time(expected_series)
        accepted_error = duration*ADVERTISING_DURATION_TOLERANCE/100
        self._test_advertising_duration(expected_duration=duration, accepted_error=accepted_error,
                                        ble_addresses=[self.device_prepairing_ble_address, current_address])

        self.testCaseChecked("INT_BLE_ADVERTISING_0012", _AUTHOR)
    # end def test_advertising_duration_pairing_mode_application_unused_prepairing_data

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_advertising_interval_pairing_mode_application_unused_prepairing_data(self):
        """
        Verify the advertising interval when the device is in application mode, unpaired and have unused prepairing
        data.
        """

        expected_series = BleProtocolTestUtils.get_expected_series_application_pairing(self, prepairing=True)
        current_addr = BleProtocolTestUtils.increment_address(test_case=self)
        duration = BleProtocolTestUtils.get_scan_time_number_of_interval_for_each_series(expected_series,
                                                                                         N_INTERVAL_FOR_AVERAGE)
        self._test_advertising_interval(expected_series=expected_series, ble_addresses=[
            current_addr, self.device_prepairing_ble_address], max_scan_time=duration)

        self.testCaseChecked("INT_BLE_ADVERTISING_0013", _AUTHOR)
    # end def test_advertising_interval_pairing_mode_application_unused_prepairing_data
# end class AdvertisingPairingModeUnusedPrepairingDataInterfaceTestCase


class AdvertisingApplicationReconnectionInterfaceTestCase(AdvertisingApplicationReconnectionModeTestCase):
    """
    BLE advertising in reconnection mode when the device is on the application Interface Test Cases
    """

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_advertising_type_reconnection_mode_application(self):
        """
        Verify the advertising type when the device is in paired application mode.
        """
        self._test_advertising_type(expected_type=BleAdvertisingPduType.CONNECTABLE_DIRECTED,
                                    scanning_timeout=EXTRA_SCAN_TIME,
                                    ble_addresses=[self.current_channel.get_device_ble_address()])

        self.testCaseChecked("INT_BLE_ADVERTISING_0014", _AUTHOR)
    # end def test_advertising_type_reconnection_mode_application

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_advertising_duration_reconnection_mode_application(self):
        """
        Verify the advertising duration when the device is in paired application mode.
        """
        entire_window = self.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_ApplicationReconnectionAdvertisingWindowS - \
            self.time_lost_user_action
        self._test_advertising_duration(expected_duration=entire_window,
                                        accepted_error=entire_window * ADVERTISING_DURATION_TOLERANCE / 100,
                                        ble_addresses=[self.current_channel.get_device_ble_address()],
                                        verify_reconnection=False)

        self.testCaseChecked("INT_BLE_ADVERTISING_0015", _AUTHOR)
    # end def test_advertising_duration_reconnection_mode_application

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_advertising_interval_reconnection_mode_application(self):
        """
        Verify the advertising interval when the device is in paired application mode.
        """
        expected_series = [BleAdvertisingSeries.G]
        duration = BleProtocolTestUtils.get_scan_time_number_of_interval_for_each_series(expected_series,
                                                                                         N_INTERVAL_FOR_AVERAGE)
        self._test_advertising_interval(expected_series=expected_series,
                                        ble_addresses=[self.current_channel.get_device_ble_address()],
                                        max_scan_time=duration)

        self.testCaseChecked("INT_BLE_ADVERTISING_0016", _AUTHOR)
    # end def test_advertising_interval_reconnection_mode_application
# end class AdvertisingApplicationReconnectionInterfaceTestCase


@features.class_decorator("BootloaderBLESupport")
class AdvertisingBootloaderReconnectionInterfaceTestCase(AdvertisingBootloaderReconnectionModeTestCase):
    """
    BLE advertising in reconnection mode when the device is on the bootloader Interface Test Cases
    """

    @features('BLEProtocol')
    @features('BootloaderAvailable')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_advertising_type_reconnection_mode_bootloader(self):
        """
        Verify the advertising type when the device is in paired bootloader mode.
        """
        self._test_advertising_type(expected_type=BleAdvertisingPduType.CONNECTABLE_DIRECTED,
                                    scanning_timeout=EXTRA_SCAN_TIME,
                                    ble_addresses=[self.current_channel.get_device_ble_address()])

        self.testCaseChecked("INT_BLE_ADVERTISING_0017", _AUTHOR)
    # end def test_advertising_type_reconnection_mode_bootloader

    @features('BLEProtocol')
    @features('BootloaderAvailable')
    @level('Time-consuming')
    @services('BleContext')
    @services('Debugger')
    def test_advertising_duration_reconnection_mode_bootloader(self):
        """
        Verify the advertising duration when the device is in paired bootloader mode.
        """
        entire_window = self.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_BootloaderReconnectionAdvertisingCompleteWindowS

        accepted_error = entire_window * ADVERTISING_DURATION_TOLERANCE / 100
        accepted_error += BOOTLOADER_RECONNECTION_DURATION_ERROR_OFFSET
        self._test_advertising_duration(expected_duration=entire_window, accepted_error=accepted_error,
                                        ble_addresses=[self.current_channel.get_device_ble_address()],
                                        verify_reconnection=False)

        self.testCaseChecked("INT_BLE_ADVERTISING_0018", _AUTHOR)
    # end def test_advertising_duration_reconnection_mode_bootloader

    @features('BLEProtocol')
    @features('BootloaderAvailable')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_advertising_interval_reconnection_mode_bootloader(self):
        """
        Verify the advertising interval when the device is in paired bootloader mode.
        """
        expected_series = [BleAdvertisingSeries.I, BleAdvertisingSeries.J, BleAdvertisingSeries.K]
        duration = BleProtocolTestUtils.get_scan_time_number_of_interval_for_each_series(
            expected_series, N_INTERVAL_FOR_AVERAGE)

        self._test_advertising_interval(expected_series=expected_series,
                                        ble_addresses=[self.current_channel.get_device_ble_address()],
                                        max_scan_time=duration)

        self.testCaseChecked("INT_BLE_ADVERTISING_0019", _AUTHOR)
    # end def test_advertising_interval_reconnection_mode_bootloader
# end class AdvertisingBootloaderReconnectionInterfaceTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
