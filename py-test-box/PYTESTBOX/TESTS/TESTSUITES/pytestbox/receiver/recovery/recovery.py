#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.recovery.recovery
:brief: Validate device Recovery feature from the receiver point of view
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2020/07/09
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pychannel.throughreceiverchannel import ThroughBleProReceiverChannel
from pychannel.throughreceiverchannel import ThroughReceiverChannel
from pychannel.usbchannel import UsbReceiverChannel
from pyhid.hiddispatcher import HIDDispatcher
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetest import ReceiverBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.recovery.recovery import SharedCommonRecoveryTestCase
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionRequest
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.recoveryutils import DisconnectMethod
from pytestbox.shared.base.recoveryutils import RecoveryTestUtils
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.notifications.devicedisconnection import DeviceDisconnection
from pyhid.hidpp.hidpp1.hidpp1model import Hidpp1Model
from pyhid.hidpp.hidpp1.notifications.pairingstatus import PairingStatus
from pyhid.hidpp.features.root import Root


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ReceiverForDeviceRecoveryTestCase(SharedCommonRecoveryTestCase, ReceiverBaseTestCase):
    """
    Receiver for a recovery device TestCase class
    """

    def setUp(self):
        """
        Handles test prerequisites
        """
        self.clean_pairing_data = False

        super().setUp()

        self.assertNotNone(
            obtained=self.backup_through_receiver_channel,
            msg="Cannot do recovery tests without a device connected to the receiver")
        root_version = self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.IMPORTANT.ROOT)
        self.backup_through_receiver_channel.hid_dispatcher.add_feature_entry(
            Root.FEATURE_INDEX, Root.FEATURE_ID, root_version)

        # Enable HID notification
        ChannelUtils.set_hidpp_reporting(
            test_case=self, channel=self.current_channel, enable=True, force_send_unknown_channel_type=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Perform user actions to make the device in recovery bootloader')
        # --------------------------------------------------------------------------------------------------------------
        self._device_jump_on_recovery_bootloader(discover_and_connect=False)
    # end def setUp

    def tearDown(self):
        """
        Handles test post-requisites.
        """
        try:
            if self.clean_pairing_data:
                CommonBaseTestUtils.NvsHelper.clean_pairing_data(self)
            # end if
        except Exception:
            self.log_traceback_as_warning(supplementary_message=f"Error in {self.__class__.__name__}.tearDown:")
        # end try

        super().tearDown()
    # end def tearDown

    def _complete_business(self, disconnect_method, perform_dfu=False):
        """
        Validates the business case

        :param disconnect_method: Disconnect method to use
        :type disconnect_method: ``DisconnectMethod``
        :param perform_dfu: Perform a DFU or not, by default it will not, this will only be used for
                            disconnect_method = DISCONNECT_METHOD.DFU_RESTART, optional
        :type perform_dfu: ``bool``
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

        if disconnect_method == DisconnectMethod.DFU_RESTART and perform_dfu:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Perform DFU')
            # ----------------------------------------------------------------------------------------------------------
            self._perform_dfu(skip_restart=True)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Simulate disconnect using the method {disconnect_method.name}')
        # --------------------------------------------------------------------------------------------------------------
        # Clean DeviceConnection to avoid errors in next call to verify_recovery_disconnection due to
        # previous events
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=DeviceConnection,
            channel=self.current_channel.receiver_channel)
        self._disconnect_device(disconnect_method=disconnect_method, pairing_slot=self.recovery_device_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self,
                            'Receive DeviceConnection with device_info_link_status = '
                            f'{DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED} (Link Not Established) and then '
                            'DeviceDisconnection with disconnection_type = '
                            f'{DeviceDisconnection.PERMANENT_DISCONNECTION} (Permanent Disconnection)')
        # --------------------------------------------------------------------------------------------------------------
        RecoveryTestUtils.verify_recovery_disconnection(
            test_case=self,
            disconnection_method_used=disconnect_method,
            recovery_device_index=self.recovery_device_index,
            application_device_index=self.backup_through_receiver_channel.device_index,
            check_application_connection=False)

        self.device_memory_manager.load_nvs(backup=True)

        ChannelUtils.wait_through_receiver_channel_link_status(
            test_case=self,
            channel=self.backup_through_receiver_channel,
            link_status=DeviceConnection.LinkStatus.LINK_ESTABLISHED,
            timeout=3)

        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_through_receiver_channel)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Device shall be in Main Application mode')
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(expr=self._check_device_on_application(), msg="Target not on Application")
    # end def _complete_business
# end class ReceiverForDeviceRecoveryTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
