#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.recovery.functionality
:brief: Receiver for device recovery functionality test suite
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
from pyhid.hidpp.hidpp1.notifications.devicediscovery import DeviceDiscovery
from pyhid.hidpp.hidpp1.notifications.devicerecovery import DeviceRecovery
from pyhid.hidpp.hidpp1.notifications.discoverystatus import DiscoveryStatus
from pyhid.hidpp.hidpp1.notifications.pairingstatus import PairingStatus
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionRequest
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
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
class ReceiverForDeviceRecoveryFunctionalityTestCase(ReceiverForDeviceRecoveryTestCase):
    """
    Validate ``ReceiverForDeviceRecovery`` functionality test cases
    """

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('Functionality')
    @services('Debugger')
    def test_device_recovery_connection_connect_functionality(self):
        """
        Sending PerformDevicePairingAndUnpairing with ConnectDevices = Pairing (0x01) when the recovery device is not
        connected should start a connection
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

        self.testCaseChecked("FUN_DEV_RECVONR_0001")
    # end def test_device_recovery_connection_connect_functionality

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('Functionality')
    @services('Debugger')
    def test_device_recovery_connection_cancel_connect_functionality(self):
        """
        Sending PerformDevicePairingAndUnpairing with ConnectDevices = CancelPairing (0x02) when the recovery device is
        connecting should stop the connection
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
            LogHelper.log_step(self, 'Send PerformDevicePairingAndUnpairing with connect_devices = '
                                     f'{SetPerformDeviceConnectionRequest.ConnectState.CANCEL_PAIRING} '
                                     '(Cancel Pairing)')
            # ----------------------------------------------------------------------------------------------------------
            request = SetPerformDeviceConnectionRequest(
                connect_devices=SetPerformDeviceConnectionRequest.ConnectState.CANCEL_PAIRING,
                bluetooth_address=bluetooth_address)

            self.send_report_wait_response(report=request,
                                           response_queue=self.hidDispatcher.receiver_response_queue,
                                           response_class_type=SetPerformDeviceConnectionResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Received PairingStatus with device_pairing_status = '
                                      f'{PairingStatus.STATUS.PAIRING_START} (Pairing Start)')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.check_start_pairing_status(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Received PairingStatus with device_pairing_status = '
                                      f'{PairingStatus.STATUS.PAIRING_CANCEL}')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.check_cancel_pairing_status(test_case=self, bypass_address_check=True)
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
        self.testCaseChecked("FUN_DEV_RECVONR_0002")
    # end def test_device_recovery_connection_cancel_connect_functionality

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('Functionality')
    @services('Debugger')
    def test_no_bonding_in_recovery(self):
        """
        Sending PerformDevicePairingAndUnpairing with ConnectDevices = Pairing (0x01) will not create BLE bonding
        between the device and the receiver
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Save current NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        ble_bond_ids = self.memory_manager.get_ble_bond_id_chunks()

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
                                      f'{DeviceConnection.LinkStatus.LINK_ESTABLISHED}')
            # ----------------------------------------------------------------------------------------------------------
            device_index = 0
            while device_index != self.recovery_device_index:
                device_connection = self.getMessage(queue=self.hidDispatcher.receiver_event_queue,
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
        LogHelper.log_check(self, 'No credential added to the receiver NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        new_ble_bond_ids = self.memory_manager.get_ble_bond_id_chunks()
        for i in range(len(new_ble_bond_ids)):
            self.assertEquals(expected=ble_bond_ids[i],
                              obtained=new_ble_bond_ids[i],
                              msg=f"New bonding credential created when it should not on slot {i}")
        # end for

        self.testCaseChecked("FUN_DEV_RECVONR_0003")
    # end def test_no_bonding_in_recovery

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('Functionality')
    @services('Debugger')
    def test_disconnect_using_dfu_restart(self):
        """
        Sending feature 0x00D0 (DFU) Restart function should trigger a disconnection in the receiver and it should send
        DeviceConnection (0x41) with link not established and then DeviceDisconnection (0x40) with Permanent
        disconnection (unpaired)
        """
        self._complete_business(disconnect_method=DisconnectMethod.DFU_RESTART)

        self.testCaseChecked("FUN_DEV_RECVONR_0004")
    # end def test_disconnect_using_dfu_restart

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('Functionality')
    @services('Debugger')
    def test_connect_cancel_on_going_discovery_functionality(self):
        """
        Connecting to a recovery device should cancel any on-going discovery
        """
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
            LogHelper.log_check(self,
                                'Received DeviceDiscoveryStatus with device_discovery_status = '
                                f'{DiscoveryStatus.DeviceDiscoveryStatus.STOP} (Discovery Stop) and error_type = '
                                f'{DiscoveryStatus.ErrorType.NO_ERROR} (No Error)')
            # ----------------------------------------------------------------------------------------------------------
            self.clean_message_type_in_queue(self.hidDispatcher.receiver_event_queue, (DeviceDiscovery, DeviceRecovery))
            DiscoveryTestUtils.check_status_notification(test_case=self,
                                                         expected_status=DiscoveryStatus.DeviceDiscoveryStatus.STOP,
                                                         expected_error_type=DiscoveryStatus.ErrorType.NO_ERROR)

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
                device_connection = self.getMessage(queue=self.hidDispatcher.receiver_event_queue,
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

        self.testCaseChecked("FUN_DEV_RECVONR_0005")
    # end def test_connect_cancel_on_going_discovery_functionality
# end class ReceiverForDeviceRecoveryFunctionalityTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
