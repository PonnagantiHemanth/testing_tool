#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.connectionscheme.pairing
:brief: Validate device pairing feature
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2020/03/09
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC
from time import sleep

from pychannel.throughreceiverchannel import ThroughReceiverChannel
from pychannel.usbchannel import UsbReceiverChannel
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.hidpp1.hidpp1model import Hidpp1Model
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.notifications.devicedisconnection import DeviceDisconnection
from pyhid.hidpp.hidpp1.notifications.devicediscovery import DeviceDiscovery
from pyhid.hidpp.hidpp1.notifications.discoverystatus import DiscoveryStatus
from pyhid.hidpp.hidpp1.notifications.pairingstatus import PairingStatus
from pyhid.hidpp.hidpp1.registers.performdevicediscovery import GetPerformDeviceDiscoveryRequest
from pyhid.hidpp.hidpp1.registers.performdevicediscovery import GetPerformDeviceDiscoveryResponse
from pyhid.hidpp.hidpp1.registers.performdevicediscovery import PerformDeviceDiscovery
from pyhid.hidpp.hidpp1.registers.performdevicediscovery import SetPerformDeviceDiscoveryResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.enumerationutils import EnumerationTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SharedCommonPairingTestCase(CommonBaseTestCase, ABC):
    """
    Shared Common Pairing TestCase class
    """
    # Timeout to connect to the device with the requested bluetooth address
    START_PAIRING_TIMEOUT = DevicePairingTestUtils.START_PAIRING_TIMEOUT
    # Timeout to complete the whole pairing sequence
    PAIRING_TIMEOUT = DevicePairingTestUtils.PAIRING_TIMEOUT
    # delay between 2 consecutive keystrokes in second
    KEYSTROKE_INTERVAL = DevicePairingTestUtils.KEYSTROKE_INTERVAL

    def setUp(self):
        """
        Handle test prerequisites.
        """
        # Attribute to ensure device stays connected after each test
        self.post_requisite_device_connected = False

        super().setUp()

        if self.device_memory_manager is not None:
            self.device_memory_manager.read_nvs(backup=True)
        # end if

        # Cleanup all pairing slots except the first one
        DevicePairingTestUtils.NvsManager.clean_pairing_data(self)
        # Initialize Bluetooth address test parameter
        self.bluetooth_address = HexList("00"*6)
        # Initialize the authentication method parameter
        DevicePairingTestUtils.set_authentication_method(self, self.config_manager)
        # Enable HID notification
        ChannelUtils.set_hidpp_reporting(test_case=self)
        # Attribute to ensure device stays connected after each test
        self.post_requisite_device_connected = True
        # Double-click on the easy switch button to switch to host 2 or 3
        DevicePairingTestUtils.change_host_by_link_state(
            self, link_state=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED)
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            try:
                response = True
                while response is not None:
                    response = ChannelUtils.get_only(
                        test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                        queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, allow_no_message=True)
                    if isinstance(response, DeviceConnection):
                        device_pairing_slot = int(Numeral(response.pairing_slot))
                        device_info_class = self.get_device_info_bit_field_structure_in_device_connection(
                            response)
                        device_info = device_info_class.fromHexList(HexList(response.information))
                        if (int(Numeral(device_info.device_info_link_status)) ==
                                DeviceConnection.LinkStatus.LINK_ESTABLISHED and device_pairing_slot == 1):
                            self.post_requisite_device_connected = False
                        else:
                            self.post_requisite_device_connected = True
                        # end if
                    elif isinstance(response, DeviceDisconnection):
                        self.post_requisite_device_connected = True
                    # end if
                # end while
                if self.post_requisite_device_connected:
                    if self.f.PRODUCT.DEVICE.F_NbHosts > 1:
                        DevicePairingTestUtils.change_host_by_link_state(
                            self, DeviceConnection.LinkStatus.LINK_ESTABLISHED)
                        self.cleanup_battery_event_from_queue()
                    else:
                        CommonBaseTestUtils.load_nvs(self, backup=True, no_reset=True)
                    # end if
                # end if
                ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
            except Exception:
                if self.device_memory_manager is not None:
                    self.device_memory_manager.load_nvs(self, backup=True)
                    # Add a delay to make sure that the device is connected again
                    sleep(1)
                # end if
                raise
            # end try
        # end with
        super().tearDown()
    # end def tearDown

    def clean_device_discovery_notifications(self):
        """
        Remove DeviceDiscovery notifications from receiver event queue
        """
        # Empty queue from DeviceDiscovery and DiscoveryStatus notifications
        ChannelUtils.clean_messages(
            test_case=self,
            channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
            class_type=(DeviceDiscovery, DiscoveryStatus))
    # end def clean_device_discovery_notifications
# end class SharedCommonPairingTestCase(CommonBaseTestCase):


class SharedPairingTestCase(SharedCommonPairingTestCase, ABC):
    """
    Shared Pairing TestCases
    """

    @features('BLEDevicePairing')
    @level('Business', 'SmokeTests')
    def test_discover_and_pair(self):
        """
        Validates the device discovery and pairing business case using the 2 buttons authentication method
        """
        # Event: discovery launches
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send 'Perform device discovery' request")
        # --------------------------------------------------------------------------------------------------------------
        start_discovery_resp = DiscoveryTestUtils.start_discovery(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate device discovery response')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.MessageChecker.check_fields(
            self, start_discovery_resp, SetPerformDeviceDiscoveryResponse, {})

        # Event: User performs action on the device to put it in pairing mode
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the Easy switch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Perform Device Discovery read request')
        # --------------------------------------------------------------------------------------------------------------
        perform_device_discovery = GetPerformDeviceDiscoveryRequest()
        perform_device_discovery_resp = ChannelUtils.send(
            test_case=self,
            report=perform_device_discovery,
            channel=ChannelUtils.get_receiver_channel(test_case=self),
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=GetPerformDeviceDiscoveryResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Read Perform Device Discovery response')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.GetPerformDeviceDiscoveryResponseChecker.check_fields(
            self,
            perform_device_discovery_resp,
            GetPerformDeviceDiscoveryResponse,
            DiscoveryTestUtils.GetPerformDeviceDiscoveryResponseChecker.get_check_map(
                PerformDeviceDiscovery.DeviceDiscoveryStatus.DISCOVER_HID_DEVICES_ONGOING)
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check discovery status notification returned no error')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.check_status_notification(
            self, DiscoveryStatus.DeviceDiscoveryStatus.START, DiscoveryStatus.ErrorType.NO_ERROR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a device discovery notification')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self, PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE)

        self.assertNotNone(device_discovery,
                           "Device discovery notifications should be received")
        self.assertNotNone(device_discovery[DeviceDiscovery.PART.CONFIGURATION],
                           "Part 0 (configuration) should always be received")
        self.assertNotNone(device_discovery[DeviceDiscovery.PART.NAME_1],
                           "Part 1 (Device name first part) should always be received")

        self.assertTrue(int(Numeral(device_discovery[DeviceDiscovery.PART.CONFIGURATION].data.protocol_type)) ==
                        DeviceDiscovery.DeviceDiscoveryPart0.BLE_PRO_PROTOCOL_TYPE,
                        msg='Wrong protocol_type parameter received in device discovery notification')
        # Empty event queue
        ChannelUtils.empty_queue(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT)

        ChannelUtils.set_hidpp_reporting(test_case=self)

        # Add DeviceConnection notification to the event queue to enable notification sequence verification
        if isinstance(self.current_channel, UsbReceiverChannel):
            current_receiver_channel = self.current_channel
        elif isinstance(self.current_channel, ThroughReceiverChannel):
            current_receiver_channel = self.current_channel.receiver_channel
        else:
            assert False, "Cannot use this method on a channel other than UsbReceiverChannel or ThroughReceiverChannel"
        # end if

        current_receiver_channel.hid_dispatcher.receiver_event_queue.update_accepted_messages(
            Hidpp1Model.get_available_events_classes() + Hidpp1Model.get_connection_events_classes())

        try:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send 'Perform device connection' request")
            # ----------------------------------------------------------------------------------------------------------
            bluetooth_address = device_discovery[DeviceDiscovery.PART.CONFIGURATION].data.bluetooth_address

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate 'Perform device pairing and unpairing' response")
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.start_pairing_sequence(self, bluetooth_address)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check discovery status notification')
            # ----------------------------------------------------------------------------------------------------------
            DiscoveryTestUtils.check_status_notification(
                self, DiscoveryStatus.DeviceDiscoveryStatus.STOP, DiscoveryStatus.ErrorType.NO_ERROR)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a start pairing status notification')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.check_start_pairing_status(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a display passkey notification')
            # ----------------------------------------------------------------------------------------------------------
            passkey_digits = DevicePairingTestUtils.PairingChecker.get_passkey_digits(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait for a 'Digit Start' passkey notification")
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.get_display_passkey_start(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Loop over passkey inputs list provided by the receiver')
            LogHelper.log_check(self, "Wait for a 'Digit In' passkey notification")
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.generate_keystrokes(self, passkey_digits)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Emulate an 'End of sequence' user action")
            LogHelper.log_check(self, "Wait for a 'Digit End' passkey notification")
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.generate_end_of_sequence(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a stop pairing status notification')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.check_stop_pairing_status(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a device connection notification')
            # ----------------------------------------------------------------------------------------------------------
            device_connection = ChannelUtils.get_only(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceConnection)

            device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
            device_info = device_info_class.fromHexList(HexList(device_connection.information))
            self.assertTrue(int(Numeral(device_info.device_info_link_status)) ==
                            DeviceConnection.LinkStatus.LINK_ESTABLISHED, msg='The device do not connect on the receiver')
        finally:
            # Remove DeviceConnection notification to the event queue
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

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Read BLE Pro device pairing information request')
        # --------------------------------------------------------------------------------------------------------------
        f = self.getFeatures()
        device_name_resp = EnumerationTestUtils.get_device_pairing_information(self, pairing_slot=int(Numeral(
            device_connection.pairing_slot)))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate BLE PRo device pairing information response is received')
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(
            expr=str(HexList(device_name_resp.device_unit_id)) in f.SHARED.DEVICES.F_UnitIds_1,
            msg=f'Wrong device_unit_id parameter ({HexList(device_name_resp.device_unit_id)}) received in Get BLE Pro '
                f'Device PairingInfo Response')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.testCaseChecked("FNT_DEV_PAIR_0001")
    # end def test_discover_and_pair

    @features('BLEDevicePairing')
    @level('Time-consuming')
    def test_get_pass_keycode(self):
        """
        Validates the get pass keycode exchange failure rate is negligible.
        """
        loop_count = 25
        failure_counter = 0

        for _ in range(loop_count):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send 'Perform device discovery' request")
            # ----------------------------------------------------------------------------------------------------------
            start_discovery_resp = DiscoveryTestUtils.start_discovery(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate device discovery response')
            # ----------------------------------------------------------------------------------------------------------
            DiscoveryTestUtils.MessageChecker.check_fields(
                self, start_discovery_resp, SetPerformDeviceDiscoveryResponse, {})

            # Event: User performs action on the device to put it in pairing mode
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the Easy switch button')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.enter_pairing_mode()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check discovery status notification')
            # ----------------------------------------------------------------------------------------------------------
            DiscoveryTestUtils.check_status_notification(
                self, DiscoveryStatus.DeviceDiscoveryStatus.START, DiscoveryStatus.ErrorType.NO_ERROR)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a device discovery notification')
            # ----------------------------------------------------------------------------------------------------------
            device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
                self, PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE)
            ChannelUtils.clean_messages(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=(PairingStatus, DeviceDiscovery))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send 'Cancel device discovery' request")
            # ----------------------------------------------------------------------------------------------------------
            DiscoveryTestUtils.cancel_discovery(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send 'Perform device connection' request")
            # ----------------------------------------------------------------------------------------------------------
            from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionRequest
            bluetooth_address = device_discovery[DeviceDiscovery.PART.CONFIGURATION].data.bluetooth_address
            DevicePairingTestUtils.start_pairing_sequence(
                self, bluetooth_address, auth_entropy=SetPerformDeviceConnectionRequest.DEFAULT.ENTROPY_LENGTH_MAX)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check discovery status notification')
            # ----------------------------------------------------------------------------------------------------------
            DiscoveryTestUtils.check_status_notification(
                self, DiscoveryStatus.DeviceDiscoveryStatus.CANCEL, DiscoveryStatus.ErrorType.NO_ERROR)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a start pairing status notification')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.check_start_pairing_status(self)

            # noinspection PyBroadException
            try:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Wait for a display passkey notification')
                # ------------------------------------------------------------------------------------------------------
                DevicePairingTestUtils.PairingChecker.get_passkey_digits(self)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Wait for a 'Digit Start' passkey notification")
                # ------------------------------------------------------------------------------------------------------
                DevicePairingTestUtils.PairingChecker.get_display_passkey_start(self)
            except Exception:
                failure_counter += 1
                LogHelper.log_info(self, 'passkey notifications not received !')
            # end try

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Pairing Passkey step failure rate is null")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(failure_counter, 0, msg='Pairing get_passkey_digits step shall not fail')

        self.testCaseChecked("FNT_DEV_PAIR_0002")
    # end def test_get_pass_keycode
# end class SharedPairingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
