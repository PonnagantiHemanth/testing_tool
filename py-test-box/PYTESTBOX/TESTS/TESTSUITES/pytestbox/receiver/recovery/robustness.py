#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.recovery.robustness
:brief: Receiver for device recovery robustness test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2024/02/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pychannel.throughreceiverchannel import ThroughBleProReceiverChannel
from pychannel.throughreceiverchannel import ThroughReceiverChannel
from pychannel.usbchannel import UsbReceiverChannel
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.hidpp1.hidpp1model import Hidpp1Model
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.notifications.pairingstatus import PairingStatus
from pyhid.hidpp.hidpp1.registers.connectionstate import SetConnectionStateRequest
from pyhid.hidpp.hidpp1.registers.connectionstate import SetConnectionStateResponse
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
from pytestbox.shared.base.recoveryutils import DisconnectMethod
from pytestbox.shared.base.recoveryutils import RecoveryTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ReceiverForDeviceRecoveryRobustnessTestCase(ReceiverForDeviceRecoveryTestCase):
    """
    Validate ``ReceiverForDeviceRecovery`` robustness test cases
    """

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('Robustness')
    @services('Debugger')
    def test_device_recovery_no_permanent_connection_information(self):
        """
        As the recovery pairing is only temporary (nothing is stored permanently), when the receiver is reset/power
        cycled the recovery pairing is lost. Checking for the existing pairings via fake device arrival will not show
        any previously 'paired' recovery devices.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start discovery')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.start_discovery(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify all Device Recovery Notification parts are received')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = RecoveryTestUtils.get_discovered_recovery_device(test_case=self)
        self.assertNotNone(obtained=bluetooth_address,
                           msg="Recovery device wanted not found")

        # Add DeviceConnection notification to the event queue to enable notification sequence verification
        self.hidDispatcher.receiver_event_queue.update_accepted_messages(
            Hidpp1Model.get_available_events_classes() + Hidpp1Model.get_connection_events_classes())

        try:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send PerformDevicePairingAndUnpairing with connect_devices = '
                                     f'{SetPerformDeviceConnectionRequest.ConnectState.PAIRING} (Pairing) and '
                                     f'bluetooth_address = {bluetooth_address}')
            # ----------------------------------------------------------------------------------------------------------
            RecoveryTestUtils.connect_to_recovery_device(test_case=self, bluetooth_address=bluetooth_address)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Received PairingStatus with device_pairing_status = '
                                      f'{PairingStatus.STATUS.PAIRING_START} (Pairing Start)')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.check_start_pairing_status(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Received PairingStatus with device_pairing_status = '
                                      f'{PairingStatus.STATUS.PAIRING_STOP} (Pairing Stop)')
            # ----------------------------------------------------------------------------------------------------------
            self.recovery_device_index = \
                int(Numeral(DevicePairingTestUtils.PairingChecker.check_stop_pairing_status(test_case=self)))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Received DeviceConnection with device_info_link_status = '
                                      f'{DeviceConnection.LinkStatus.LINK_ESTABLISHED} (Link Established')
            # ----------------------------------------------------------------------------------------------------------
            device_index = 0
            while device_index != self.recovery_device_index:
                device_connection = ChannelUtils.get_only(test_case=self,
                                                          channel=ChannelUtils.get_receiver_channel(test_case=self),
                                                          queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                                                          class_type=DeviceConnection)
                device_index = int(Numeral(device_connection.device_index))
                if device_index == self.recovery_device_index:
                    device_info_class = \
                        self.get_device_info_bit_field_structure_in_device_connection(device_connection)
                    device_info = device_info_class.fromHexList(HexList(device_connection.information))
                    self.assertEquals(int(Numeral(device_info.device_info_link_status)),
                                      DeviceConnection.LinkStatus.LINK_ESTABLISHED,
                                      msg=f'The device do not connect on the receiver, {device_info}')
                # end if
            # end while

            if isinstance(self.current_channel, UsbReceiverChannel):
                current_receiver_channel = self.current_channel
            elif isinstance(self.current_channel, ThroughReceiverChannel):
                current_receiver_channel = self.current_channel.receiver_channel
            else:
                assert False, \
                    "Cannot use this method on a channel other than UsbReceiverChannel or ThroughReceiverChannel"
            # end if

            channel = ThroughBleProReceiverChannel(
                receiver_channel=current_receiver_channel, device_index=self.recovery_device_index)
            channel.get_transport_id()
            channel.is_device_connected()
            DeviceManagerUtils.add_channel_to_cache(test_case=self, channel=channel)
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

        self.config_manager.current_mode = self.config_manager.MODE.BOOTLOADER

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reset receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)
        ChannelUtils.set_hidpp_reporting(
            test_case=self, channel=self.current_channel, enable=True, force_send_unknown_channel_type=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send a fake arrival')
        # --------------------------------------------------------------------------------------------------------------
        set_register = SetConnectionStateRequest(write_action_on_connection_fake_device_arrival=1)
        ChannelUtils.send(test_case=self, report=set_register,
                          channel=ChannelUtils.get_receiver_channel(test_case=self),
                          response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                          response_class_type=SetConnectionStateResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the recovery device is not connected anymore')
        # --------------------------------------------------------------------------------------------------------------
        while not self.is_current_hid_dispatcher_queue_empty(queue=self.hidDispatcher.receiver_connection_event_queue):
            device_connection = ChannelUtils.get_only(test_case=self,
                                                      channel=ChannelUtils.get_receiver_channel(test_case=self),
                                                      queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                                      class_type=DeviceConnection)
            device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
            device_info = device_info_class.fromHexList(HexList(device_connection.information))

            self.assertFalse(
                expr=self.recovery_device_index == int(Numeral(device_connection.device_index)) and
                int(Numeral(device_info.device_info_link_status)) == DeviceConnection.LinkStatus.LINK_ESTABLISHED,
                msg="Recovery device still connected")
        # end while

        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel)

        self.testCaseChecked("ROB_DEV_RECVONR_0001")
    # end def test_device_recovery_no_permanent_connection_information

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('Robustness')
    @services('Debugger')
    def test_device_recovery_connection_cancel_connect_when_disconnected(self):
        """
        Sending PerformDevicePairingAndUnpairing with ConnectDevices = CancelPairing (0x02) when recovery device is
        disconnected should still return a notification 0x54 cancel pairing and not triggering any error
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send PerformDevicePairingAndUnpairing with connect_devices = '
                                 f'{SetPerformDeviceConnectionRequest.ConnectState.CANCEL_PAIRING} (Cancel Pairing)')
        # --------------------------------------------------------------------------------------------------------------
        request = SetPerformDeviceConnectionRequest(
            connect_devices=SetPerformDeviceConnectionRequest.ConnectState.CANCEL_PAIRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify response is received')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.send(test_case=self,
                          report=request,
                          response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                          response_class_type=SetPerformDeviceConnectionResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Received PairingStatus with device_pairing_status = '
                                  f'{PairingStatus.STATUS.PAIRING_CANCEL} (Pairing Cancel)')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.check_cancel_pairing_status(test_case=self, bypass_address_check=True)

        self.testCaseChecked("ROB_DEV_RECVONR_0002")
    # end def test_device_recovery_connection_cancel_connect_when_disconnected

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('Robustness')
    @services('Debugger')
    def test_device_recovery_connection_cancel_connect_when_connected(self):
        """
        Sending PerformDevicePairingAndUnpairing with ConnectDevices = CancelPairing (0x02) when recovery device is
        completely connected should still return a notification 0x54 cancel pairing and not triggering any error
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start discovery')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.start_discovery(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify all Device Recovery Notification parts are received')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = RecoveryTestUtils.get_discovered_recovery_device(test_case=self)
        self.assertNotNone(obtained=bluetooth_address,
                           msg="Recovery device wanted not found")

        # Add DeviceConnection notification to the event queue to enable notification sequence verification
        self.hidDispatcher.receiver_event_queue.update_accepted_messages(
            Hidpp1Model.get_available_events_classes() + Hidpp1Model.get_connection_events_classes())

        try:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self,
                               'Send PerformDevicePairingAndUnpairing with connect_devices = '
                               f'{SetPerformDeviceConnectionRequest.ConnectState.PAIRING} (Pairing) and '
                               f'bluetooth_address = {bluetooth_address}')
            # ----------------------------------------------------------------------------------------------------------
            RecoveryTestUtils.connect_to_recovery_device(test_case=self, bluetooth_address=bluetooth_address)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Received PairingStatus with device_pairing_status = '
                                      f'{PairingStatus.STATUS.PAIRING_START} (Pairing Start)')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.check_start_pairing_status(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Received PairingStatus with device_pairing_status = '
                                      f'{PairingStatus.STATUS.PAIRING_STOP} (Pairing Stop)')
            # ----------------------------------------------------------------------------------------------------------
            self.recovery_device_index = \
                int(Numeral(DevicePairingTestUtils.PairingChecker.check_stop_pairing_status(test_case=self)))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Received DeviceConnection with device_info_link_status = '
                                      f'{DeviceConnection.LinkStatus.LINK_ESTABLISHED} (Link Established)')
            # ----------------------------------------------------------------------------------------------------------
            device_index = 0
            while device_index != self.recovery_device_index:
                device_connection = ChannelUtils.get_only(test_case=self,
                                                          channel=ChannelUtils.get_receiver_channel(test_case=self),
                                                          queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                                                          class_type=DeviceConnection)
                device_index = int(Numeral(device_connection.device_index))
                if device_index == self.recovery_device_index:
                    device_info_class = \
                        self.get_device_info_bit_field_structure_in_device_connection(device_connection)
                    device_info = device_info_class.fromHexList(HexList(device_connection.information))
                    self.assertEquals(int(Numeral(device_info.device_info_link_status)),
                                      DeviceConnection.LinkStatus.LINK_ESTABLISHED,
                                      msg=f'The device do not connect on the receiver, {device_info}')
                # end if
            # end while

            if isinstance(self.current_channel, UsbReceiverChannel):
                current_receiver_channel = self.current_channel
            elif isinstance(self.current_channel, ThroughReceiverChannel):
                current_receiver_channel = self.current_channel.receiver_channel
            else:
                assert False, \
                    "Cannot use this method on a channel other than UsbReceiverChannel or ThroughReceiverChannel"
            # end if

            channel = ThroughBleProReceiverChannel(
                receiver_channel=current_receiver_channel, device_index=self.recovery_device_index)
            channel.get_transport_id()
            channel.is_device_connected()
            DeviceManagerUtils.add_channel_to_cache(test_case=self, channel=channel)

            DeviceManagerUtils.set_channel(test_case=self, new_channel=channel)
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

        self.config_manager.current_mode = self.config_manager.MODE.BOOTLOADER

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send PerformDevicePairingAndUnpairing with connect_devices = '
                                 f'{SetPerformDeviceConnectionRequest.ConnectState.CANCEL_PAIRING} (Cancel Pairing)')
        # --------------------------------------------------------------------------------------------------------------
        request = SetPerformDeviceConnectionRequest(
            connect_devices=SetPerformDeviceConnectionRequest.ConnectState.CANCEL_PAIRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Verify response is received')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.send(test_case=self,
                          channel=self.current_channel.receiver_channel,
                          report=request,
                          response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                          response_class_type=SetPerformDeviceConnectionResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Received PairingStatus with device_pairing_status = '
                                  f'{PairingStatus.STATUS.PAIRING_CANCEL} (Pairing Cancel)')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.check_cancel_pairing_status(test_case=self, bypass_address_check=True)

        self.testCaseChecked("ROB_DEV_RECVONR_0003")
    # end def test_device_recovery_connection_cancel_connect_when_connected

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('Robustness')
    @services('Debugger')
    def test_device_recovery_connection_connect_ignore_entropy_length(self):
        """
        PerformDevicePairingAndUnpairing.AuthenticationEntropyLength should be ignored when sending
        PerformDevicePairingAndUnpairing with ConnectDevices = Pairing (0x01)
        """
        jump_to_recovery_bootloader = False
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self,
                           'Test Loop over the entropy_length parameter of PerformDevicePairingAndUnpairing in the '
                           'valid and invalid range')
        # --------------------------------------------------------------------------------------------------------------
        for entropy_length in compute_wrong_range(SetPerformDeviceConnectionRequest.DEFAULT.ENTROPY_LENGTH_MAX,
                                                  min_value=0, max_value=0xFF):
            if jump_to_recovery_bootloader:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Jump on recovery bootloader for tests after the first entropy_length value')
                # ------------------------------------------------------------------------------------------------------
                self._device_jump_on_recovery_bootloader(discover_and_connect=False)
            else:
                jump_to_recovery_bootloader = True
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
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Send PerformDevicePairingAndUnpairing with connect_devices = '
                                         f'{SetPerformDeviceConnectionRequest.ConnectState.PAIRING} (Pairing) and '
                                         f'bluetooth_address = {bluetooth_address} and auth_entropy = {entropy_length}')
                # ------------------------------------------------------------------------------------------------------
                write_device_connect = SetPerformDeviceConnectionRequest(
                    connect_devices=SetPerformDeviceConnectionRequest.ConnectState.PAIRING,
                    bluetooth_address=bluetooth_address,
                    auth_entropy=entropy_length)
                ChannelUtils.send(test_case=self,
                                  channel=ChannelUtils.get_receiver_channel(test_case=self),
                                  report=write_device_connect,
                                  response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                                  response_class_type=SetPerformDeviceConnectionResponse)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Received PairingStatus with device_pairing_status = '
                                          f'{PairingStatus.STATUS.PAIRING_START} (Pairing Start)')
                # ------------------------------------------------------------------------------------------------------
                DevicePairingTestUtils.PairingChecker.check_start_pairing_status(test_case=self)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Received PairingStatus with device_pairing_status = '
                                          f'{PairingStatus.STATUS.PAIRING_STOP} (Pairing Stop)')
                # ------------------------------------------------------------------------------------------------------
                self.recovery_device_index = int(Numeral(
                    DevicePairingTestUtils.PairingChecker.check_stop_pairing_status(test_case=self)))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Received DeviceConnection with device_info_link_status = '
                                          f'{DeviceConnection.LinkStatus.LINK_ESTABLISHED} (Link Established)')
                # ------------------------------------------------------------------------------------------------------
                device_index = 0
                while device_index != self.recovery_device_index:
                    device_connection = ChannelUtils.get_only(test_case=self,
                                                              channel=ChannelUtils.get_receiver_channel(test_case=self),
                                                              queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                                                              class_type=DeviceConnection)
                    device_index = int(Numeral(device_connection.device_index))
                    if device_index == self.recovery_device_index:
                        device_info_class = \
                            self.get_device_info_bit_field_structure_in_device_connection(device_connection)
                        device_info = device_info_class.fromHexList(HexList(device_connection.information))
                        self.assertEquals(int(Numeral(device_info.device_info_link_status)),
                                          DeviceConnection.LinkStatus.LINK_ESTABLISHED,
                                          msg=f'The device do not connect on the receiver, {device_info}')
                    # end if
                # end while

                if isinstance(self.current_channel, UsbReceiverChannel):
                    current_receiver_channel = self.current_channel
                elif isinstance(self.current_channel, ThroughReceiverChannel):
                    current_receiver_channel = self.current_channel.receiver_channel
                else:
                    assert False, \
                        "Cannot use this method on a channel other than UsbReceiverChannel or ThroughReceiverChannel"
                # end if

                channel = ThroughBleProReceiverChannel(
                    receiver_channel=current_receiver_channel, device_index=self.recovery_device_index)
                try:
                    channel.get_transport_id()
                    channel.is_device_connected()
                    DeviceManagerUtils.add_channel_to_cache(test_case=self, channel=channel)
                except Exception:
                    # Delete the object ThroughReceiverChannel to prevent having multiple channel with the
                    # same device index in the receiver multi-queue created in the retry loop
                    del channel
                    raise
                # end try

                DeviceManagerUtils.set_channel(test_case=self, new_channel=channel)
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

            self.config_manager.current_mode = self.config_manager.MODE.BOOTLOADER

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Disconnect using unpairing command')
            # ----------------------------------------------------------------------------------------------------------
            # Clean DeviceConnection to avoid errors in next call to verify_recovery_disconnection due to
            # previous events
            ChannelUtils.clean_messages(
                test_case=self,
                queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                class_type=DeviceConnection,
                channel=self.current_channel.receiver_channel)
            self._disconnect_device(disconnect_method=DisconnectMethod.PERFORM_DEVICE_PAIRING_AND_UNPAIRING,
                                    pairing_slot=self.recovery_device_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Verify recovery device disconnects')
            # ----------------------------------------------------------------------------------------------------------
            RecoveryTestUtils.verify_recovery_disconnection(
                test_case=self,
                recovery_device_index=self.recovery_device_index,
                application_device_index=self.backup_through_receiver_channel.device_index,
                disconnection_method_used=DisconnectMethod.PERFORM_DEVICE_PAIRING_AND_UNPAIRING)
            DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_DEV_RECVONR_0004")
    # end def test_device_recovery_connection_connect_ignore_entropy_length
# end class ReceiverForDeviceRecoveryRobustnessTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
