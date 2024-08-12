#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.tools.nrfblelib
:brief: Validates nrf-ble-lib BLE context test cases
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2023/08/17
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from sys import stdout

from pychannel.blechannel import BleChannel
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pylibrary.tools.hexlist import HexList
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.ble.advertising.advertising import AdvertisingPairingModeTestCase
from pytransport.ble.nrfblelibblecontext.nrfblelibblecontext import NrfBleLibBleContext

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
_AUTHOR = "Stanislas Cottard"


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class NrfBleLibTestCase(AdvertisingPairingModeTestCase):
    """
    Nrf-ble-lib BLE context Test Cases
    """

    @features('BLEProtocol')
    @level('Tools')
    @services('Debugger')
    def test_nrf_ble_lib(self):
        """
        Test the nrf-ble-lib by doing an open context, scan, connect, service discovery, bonf, send message, receive
        message, disconnect and close context sequence.
        """
        address_current_device = BleProtocolTestUtils.get_current_device_ble_gap_address(test_case=self)
        nrf_ble_lib_context = NrfBleLibBleContext()

        nrf_ble_lib_context.open()

        try:
            central_address = nrf_ble_lib_context.get_central_address()
            stdout.write(f"Central address: {central_address}\n")

            nrf_ble_lib_device = nrf_ble_lib_context.scan_for_first_device_found(
                ble_addresses=[address_current_device])
            stdout.write(f"Scanning done: {nrf_ble_lib_device}\n")

            self.assertTrue(expr=nrf_ble_lib_context.connect(ble_context_device=nrf_ble_lib_device,
                                                             service_discovery=False, confirm_connect=True),
                            msg="Connection failed")
            stdout.write("Connection done\n")

            try:
                stdout.write(f"Connection parameters: {nrf_ble_lib_device.connection_parameters}\n")
                nrf_ble_lib_context.perform_service_discovery(ble_context_device=nrf_ble_lib_device)
                stdout.write("Service discovery done\n")
                nrf_ble_lib_context.authenticate_just_works(ble_context_device=nrf_ble_lib_device, lesc=True)
                stdout.write("Authentication just work done\n")
                stdout.write(f"Connection security parameters before calling get_connection_security_parameters: "
                             f"{nrf_ble_lib_device.connection_security_parameters}\n")
                nrf_ble_lib_context.get_connection_security_parameters(ble_context_device=nrf_ble_lib_device)
                stdout.write(f"Connection security parameters after calling get_connection_security_parameters: "
                             f"{nrf_ble_lib_device.connection_security_parameters}\n")
                current_channel = BleChannel(ble_context=nrf_ble_lib_context, ble_context_device=nrf_ble_lib_device)
                stdout.write("BleChannel created\n")
                current_channel.open()
                current_channel.get_message()
                stdout.write("BleChannel opened\n")
                descriptors = current_channel.get_descriptors()
                stdout.write(f"Descriptor gotten: {descriptors}\n")
                current_channel.send_data(data=HexList("10FF021F000001"))
                stdout.write("Data sent: 10FF021F000001\n")
                message = current_channel.get_message()
                stdout.write(f"Data received: {message}\n")
            finally:
                self.assertTrue(expr=nrf_ble_lib_context.disconnect(ble_context_device=nrf_ble_lib_device),
                                msg="Disconnection failed")
                stdout.write("Disconnection done\n")
                nrf_ble_lib_context.delete_bond(ble_context_device=nrf_ble_lib_device)
                stdout.write("Deleting bond done\n")
            # end try
        finally:
            nrf_ble_lib_context.close()
        # end try

        self.testCaseChecked("NRF_BLE_LIB_TEST_0001", _AUTHOR)
    # end def test_nrf_ble_lib

    @features('BLEProtocol')
    @level('Tools')
    @services('Debugger')
    def test_nrf_ble_lib_stress(self):
        """
        Stress the nrf-ble-lib context by doing an open/close context loop with a sequence (scan, connect, service
        discovery, disconnect) loop for each open/close iteration.
        """
        address_current_device = BleProtocolTestUtils.get_current_device_ble_gap_address(test_case=self)
        nrf_ble_lib_context = NrfBleLibBleContext()

        open_close_count = 25
        device_sequence_count = 40
        number_of_scan_failed = 0
        number_of_connect_failed = 0
        number_of_service_discovery_failed = 0
        number_of_disconnect_failed = 0
        stdout.write(f"\nDevice address: {address_current_device}\n")
        for i in range(open_close_count):
            stdout.write(f"Outer loop number: {i + 1}\n")
            nrf_ble_lib_context.open()

            try:
                for j in range(device_sequence_count):
                    stdout.write(f"\tInner loop number: {j + 1}\n")

                    try:
                        nrf_ble_lib_device = nrf_ble_lib_context.scan_for_first_device_found(
                            ble_addresses=[address_current_device])
                        stdout.write("\t\tScanning done\n")
                    except Exception as e:
                        stdout.write(f"\t\tScanning failed: {type(e)} {e}\n")
                        number_of_scan_failed += 1
                        continue
                    # end try

                    try:
                        if nrf_ble_lib_context.connect(ble_context_device=nrf_ble_lib_device, service_discovery=False):
                            stdout.write("\t\tConnection done\n")
                        else:
                            stdout.write("\t\tConnection failed\n")
                            number_of_connect_failed += 1
                            continue
                        # end if
                    except Exception as e:
                        stdout.write(f"\t\tConnection failed: {type(e)} {e}\n")
                        number_of_connect_failed += 1
                        continue
                    # end try

                    try:
                        nrf_ble_lib_context.perform_service_discovery(ble_context_device=nrf_ble_lib_device)
                        stdout.write("\t\tService discovery done\n")
                    except Exception as e:
                        stdout.write(f"\t\tservice discovery failed: {type(e)} {e}\n")
                        number_of_service_discovery_failed += 1
                    finally:
                        try:
                            if nrf_ble_lib_context.disconnect(ble_context_device=nrf_ble_lib_device):
                                stdout.write("\t\tDisconnection done\n")
                            else:
                                stdout.write("\t\tDisconnection failed\n")
                                number_of_disconnect_failed += 1
                            # end if
                        except Exception as e:
                            stdout.write(f"\t\tDisconnection failed: {type(e)} {e}\n")
                            number_of_disconnect_failed += 1
                        # end try
                    # end try
                # end for
            finally:
                nrf_ble_lib_context.close()
            # end try
        # end for
        stdout.write(f"\nOpen/close count = {open_close_count}, Device sequence count (per open/close iteration) = "
                     f"{device_sequence_count}, Total sequence performed = "
                     f"{open_close_count * device_sequence_count}\n")
        stdout.write(f"Number of scan failed = {number_of_scan_failed}\n")
        stdout.write(f"Number of connect failed = {number_of_connect_failed}\n")
        stdout.write(f"Number of service discovery failed = {number_of_service_discovery_failed}\n")
        stdout.write(f"Number of disconnect failed = {number_of_disconnect_failed}\n")

        self.testCaseChecked("NRF_BLE_LIB_TEST_0002", _AUTHOR)
    # end def test_nrf_ble_lib_stress
# end class NrfBleLibTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
