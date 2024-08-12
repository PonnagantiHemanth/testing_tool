#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.recovery.errorhandling
:brief: Receiver for device recovery error handling test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2024/02/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import skip

from pychannel.throughreceiverchannel import ThroughReceiverChannel
from pychannel.usbchannel import UsbReceiverChannel
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.hidpp1.hidpp1model import Hidpp1Model
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.notifications.pairingstatus import PairingStatus
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionRequest
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.receiver.recovery.recovery import ReceiverForDeviceRecoveryTestCase
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.recoveryutils import RecoveryTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ReceiverForDeviceRecoveryErrorHandlingTestCase(ReceiverForDeviceRecoveryTestCase):
    """
    Validate ``ReceiverForDeviceRecovery`` error handling test cases
    """

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('ErrorHandling')
    @services('Debugger')
    @skip("Current framework do not handle multiple devices")
    def test_connect_more_than_one_recovery_device_error(self):
        """
        Sending PerformDevicePairingAndUnpairing with ConnectDevices = Pairing (0x01) when a recovery device is
        already connected should return the error 0x05 (ERR_TOO_MANY_DEVICES)
        """
        # TODO Need to have two devices in recovery mode

        self.testCaseChecked("ERR_DEV_RECVONR_0001")
    # end def test_connect_more_than_one_recovery_device_error

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('ErrorHandling')
    @services('Debugger')
    def test_disconnect_on_an_empty_slot_error(self):
        """
        Sending PerformDevicePairingAndUnpairing with ConnectDevices = Unpairing (0x03) on an empty slot
        (no device connected) should return the error 0x08 (ERR_UNKNOWN_DEVICE)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over the pairing slot in range [2, .., RECEIVER_PAIRING_SLOT_COUNT]')
        # --------------------------------------------------------------------------------------------------------------
        for i in range(2, DevicePairingTestUtils.NvsManager.RECEIVER_PAIRING_SLOT_COUNT + 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send PerformDevicePairingAndUnpairing with connect_devices = '
                                     f'{SetPerformDeviceConnectionRequest.ConnectState.UNPAIRING} and '
                                     f'pairing_slot_to_be_disconnected = {i}')
            # ----------------------------------------------------------------------------------------------------------
            request = SetPerformDeviceConnectionRequest(
                connect_devices=SetPerformDeviceConnectionRequest.ConnectState.UNPAIRING,
                pairing_slot_to_be_unpaired=i)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Verify receive error code 0x08 (ERR_UNKNOWN_DEVICE)')
            # ----------------------------------------------------------------------------------------------------------
            response = ChannelUtils.send(test_case=self,
                                         channel=ChannelUtils.get_receiver_channel(test_case=self),
                                         report=request,
                                         response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                                         response_class_type=Hidpp1ErrorCodes)
            self.assertEquals(expected=Hidpp1ErrorCodes.ERR_UNKNOWN_DEVICE,
                              obtained=int(Numeral(response.error_code)),
                              msg="Wrong error code")
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_DEV_RECVONR_0002")
    # end def test_disconnect_on_an_empty_slot_error

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('ErrorHandling')
    @services('Debugger')
    def test_device_recovery_connection_connect_devices_reserved_error(self):
        """
        Sending PerformDevicePairingAndUnpairing with ConnectDevices = Reserved value (0 or > 3) should return the
        error 0x0B (ERR_INVALID_PARAM_VALUE)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over the connected_devices parameter of PerformDevicePairingAndUnpairing '
                                 'in the invalid range')
        # --------------------------------------------------------------------------------------------------------------
        for invalid_connected_devices in compute_wrong_range(
                list(range(SetPerformDeviceConnectionRequest.ConnectState.PAIRING,
                           SetPerformDeviceConnectionRequest.ConnectState.RESERVED - 1)),
                min_value=SetPerformDeviceConnectionRequest.ConnectState.RESERVED_0,
                max_value=pow(2, SetPerformDeviceConnectionRequest.LEN.CONNECT_DEVICES) - 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send PerformDevicePairingAndUnpairing with connect_devices = '
                                     f'{invalid_connected_devices}')
            # ----------------------------------------------------------------------------------------------------------
            request = SetPerformDeviceConnectionRequest(connect_devices=invalid_connected_devices)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Verify receive error code 0x0B (ERR_INVALID_PARAM_VALUE)')
            # ----------------------------------------------------------------------------------------------------------
            response = ChannelUtils.send(test_case=self,
                                         report=request,
                                         response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                                         response_class_type=Hidpp1ErrorCodes)
            self.assertEquals(expected=Hidpp1ErrorCodes.ERR_INVALID_PARAM_VALUE,
                              obtained=int(Numeral(response.error_code)),
                              msg="Wrong error code")
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_DEV_RECVONR_0003")
    # end def test_device_recovery_connection_connect_devices_reserved_error

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('ErrorHandling')
    @services('Debugger')
    @skip("In development")
    def test_device_recovery_connection_not_slot_available_error(self):
        """
        Sending PerformDevicePairingAndUnpairing with ConnectDevices = Pairing (0x01) on a recovery device when all
        pairing slots are taken should return the error= 0x05 (ERR_TOO_MANY_DEVICES)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Add necessary NVS chunks to have all pairing slots taken in the receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.clean_pairing_data = True
        # TODO
        # # Dump receiver NVS
        # self.memory_manager.read_nvs()
        # # Extract the latest BLE pairing chunk
        # receiver_data_list = self.memory_manager.get_chunks_by_name('NVS_BLE_BOND_ID_0')
        # for i in range(1, self.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots):
        #     # Increment address to avoid problems
        #     receiver_data_list[-1].bluetooth_low_energy_address.device_bluetooth_address[-1] += 1
        #     self.memory_manager.nvs_parser.add_new_chunk(f'NVS_BLE_BOND_ID_{i}', HexList(receiver_data_list[-1]),
        #                                                  is_encrypted=True,
        #                                                  iv=receiver_data_list[-1].ref.iv)
        # CommonBaseTestUtils.load_nvs(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start discovery')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.start_discovery(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify all Device Recovery Notification parts are received')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = RecoveryTestUtils.get_discovered_recovery_device(
            test_case=self, cancel_discovery_when_found=False)
        self.assertNotNone(obtained=bluetooth_address,
                           msg="Recovery device wanted not found")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send PerformDevicePairingAndUnpairing with connect_devices = '
                                 f'{SetPerformDeviceConnectionRequest.ConnectState.PAIRING} (Pairing) and '
                                 f'bluetooth_address = {bluetooth_address}')
        # --------------------------------------------------------------------------------------------------------------
        request = SetPerformDeviceConnectionRequest(
            connect_devices=SetPerformDeviceConnectionRequest.ConnectState.PAIRING,
            bluetooth_address=bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify receive error code 0x0B (ERR_INVALID_PARAM_VALUE)')
        # --------------------------------------------------------------------------------------------------------------
        response = ChannelUtils.send(test_case=self,
                                     channel=self.current_channel.receiver_channel,
                                     report=request,
                                     response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                                     response_class_type=Hidpp1ErrorCodes)
        self.assertEquals(expected=Hidpp1ErrorCodes.ERR_TOO_MANY_DEVICES,
                          obtained=int(Numeral(response.error_code)),
                          msg="Wrong error code")

        self.testCaseChecked("ERR_DEV_RECVONR_0004")
    # end def test_device_recovery_connection_not_slot_available_error

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('ErrorHandling')
    @services('Debugger')
    def test_device_recovery_wrong_authentication_method(self):
        """
        Sending PerformDevicePairingAndUnpairing with ConnectDevices = Pairing (0x01) and a wrong value of
        PerformDevicePairingAndUnpairing.AuthenticationMethodRequested should have the pairing process fail
        """
        for i in range(2):
            if i > 0:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Jump on recovery bootloader')
                # ------------------------------------------------------------------------------------------------------
                self._device_jump_on_recovery_bootloader(discover_and_connect=False)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start discovery')
            # ----------------------------------------------------------------------------------------------------------
            DiscoveryTestUtils.start_discovery(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Verify all Device Recovery Notification parts are received')
            # ----------------------------------------------------------------------------------------------------------
            bluetooth_address = RecoveryTestUtils.get_discovered_recovery_device(test_case=self)
            self.assertNotNone(obtained=bluetooth_address,
                               msg="Recovery device wanted not found")

            # Add DeviceConnection notification to the event queue to enable notification sequence verification
            self.hidDispatcher.receiver_event_queue.update_accepted_messages(
                Hidpp1Model.get_available_events_classes() + Hidpp1Model.get_connection_events_classes())

            try:
                if i == 0:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self,
                                       'Send PerformDevicePairingAndUnpairing with connect_devices = '
                                       f'{SetPerformDeviceConnectionRequest.ConnectState.PAIRING} (Pairing) and '
                                       f'bluetooth_address = {bluetooth_address} and passkey_auth_method = True')
                    # --------------------------------------------------------------------------------------------------
                    write_device_connect = SetPerformDeviceConnectionRequest(
                        connect_devices=SetPerformDeviceConnectionRequest.ConnectState.PAIRING,
                        bluetooth_address=bluetooth_address,
                        passkey_auth_method=True)
                    ChannelUtils.send(test_case=self,
                                      report=write_device_connect,
                                      response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                                      response_class_type=SetPerformDeviceConnectionResponse)
                elif i == 1:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self,
                                       'Send PerformDevicePairingAndUnpairing with connect_devices = '
                                       f'{SetPerformDeviceConnectionRequest.ConnectState.PAIRING} (Pairing) and '
                                       f'bluetooth_address = {bluetooth_address} and emu_2buttons_auth_method = True')
                    # --------------------------------------------------------------------------------------------------
                    write_device_connect = SetPerformDeviceConnectionRequest(
                        connect_devices=SetPerformDeviceConnectionRequest.ConnectState.PAIRING,
                        bluetooth_address=bluetooth_address,
                        emu_2buttons_auth_method=True)
                    ChannelUtils.send(test_case=self,
                                      channel=ChannelUtils.get_receiver_channel(test_case=self),
                                      report=write_device_connect,
                                      response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                                      response_class_type=SetPerformDeviceConnectionResponse)
                else:
                    assert False, "Unknown authentication method"
                # end if

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Received PairingStatus with device_pairing_status = '
                                          f'{PairingStatus.STATUS.PAIRING_START} (Pairing Start)')
                # ------------------------------------------------------------------------------------------------------
                DevicePairingTestUtils.PairingChecker.check_start_pairing_status(test_case=self)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Received PairingStatus with device_pairing_status = '
                                          f'{PairingStatus.STATUS.PAIRING_STOP} (Pairing Stop) and error_type = '
                                          f'{PairingStatus.ERROR_TYPE.FAILED} (Failed)')
                # ------------------------------------------------------------------------------------------------------
                DevicePairingTestUtils.PairingChecker.check_failed_pairing_status(test_case=self)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Verify device has jumped on application')
                # ------------------------------------------------------------------------------------------------------
                # Check received link established notification
                device_index = 0
                while device_index != self.backup_through_receiver_channel.device_index:
                    device_connection = ChannelUtils.get_only(test_case=self,
                                                              channel=ChannelUtils.get_receiver_channel(test_case=self),
                                                              queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                                                              class_type=DeviceConnection)
                    device_index = int(Numeral(device_connection.device_index))
                    if device_index == self.backup_through_receiver_channel.device_index:
                        device_info_class = \
                            self.get_device_info_bit_field_structure_in_device_connection(device_connection)
                        device_info = device_info_class.fromHexList(HexList(device_connection.information))
                        self.assertEquals(
                            int(Numeral(device_info.device_info_link_status)),
                            DeviceConnection.LinkStatus.LINK_ESTABLISHED,
                            msg=f'The receiver did not connect to the device in application, {device_info}')
                    # end if
                # end while
                DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel)
            finally:
                if isinstance(self.current_channel, UsbReceiverChannel):
                    current_receiver_channel = self.current_channel
                elif isinstance(self.current_channel, ThroughReceiverChannel):
                    current_receiver_channel = self.current_channel.receiver_channel
                else:
                    assert False, \
                        "Cannot use this method on a channel other than UsbReceiverChannel or ThroughReceiverChannel"
                # end if

                current_receiver_channel.hid_dispatcher.receiver_event_queue.update_accepted_messages(
                    Hidpp1Model.get_available_events_classes())
            # end try

        self.testCaseChecked("ERR_DEV_RECVONR_0005")
    # end def test_device_recovery_wrong_authentication_method
# end class ReceiverForDeviceRecoveryErrorHandlingTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
