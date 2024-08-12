#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.connectionscheme.pairing_robustness
:brief: Validate device pairing feature
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2020/04/21
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.notifications.devicediscovery import DeviceDiscovery
from pyhid.hidpp.hidpp1.notifications.discoverystatus import DiscoveryStatus
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionRequest
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionResponse
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.connectionscheme.pairing import SharedCommonPairingTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SharedPairingRobustnessTestCase(SharedCommonPairingTestCase, ABC):
    """
    Shared Pairing Robustness TestCases
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "The Device Discovery sequence successfully returns a discovery notification")
        # --------------------------------------------------------------------------------------------------------------
        # Retrieve current device BT address
        self.device_bluetooth_address = DiscoveryTestUtils.discover_device(self)

    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            # Empty event queue
            self.clean_device_discovery_notifications()
        # end with
        super().tearDown()
    # end def tearDown

    @features('BLEDevicePairing')
    @level('Robustness')
    def test_bad_sub_id(self):
        """
        Invalid Device Index shall raise an error message with SUB ID=0x8F
        """
        auth_method = DevicePairingTestUtils.get_authentication_method(self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over sub_id invalid range [0x80, 0x83, 0x84]')
        # --------------------------------------------------------------------------------------------------------------
        for wrong_sub_id in [0x80, 0x83, 0x84]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send Perform device connection request with Connect Devices = 0 and '
                                     f'index={wrong_sub_id}')
            # ----------------------------------------------------------------------------------------------------------
            write_device_connect = SetPerformDeviceConnectionRequest(
                connect_devices=SetPerformDeviceConnectionRequest.ConnectState.PAIRING,
                bluetooth_address=self.device_bluetooth_address, 
                emu_2buttons_auth_method=auth_method == SetPerformDeviceConnectionRequest.MASK.EMU_2BUTTONS_AUTH_METHOD,
                passkey_auth_method=(auth_method == SetPerformDeviceConnectionRequest.MASK.PASSKEY_AUTH_METHOD))
            write_device_connect.sub_id = wrong_sub_id
            write_device_connect_response = ChannelUtils.send(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self), report=write_device_connect,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                response_class_type=Hidpp1ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check HID++ 1.0 ERR_INVALID_SUBID (1) Error Code returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=Hidpp1ErrorCodes.ERR_INVALID_SUBID,
                             obtained=int(Numeral(write_device_connect_response.errorCode)),
                             msg='The errorCode parameter differs from the one expected')

        self.testCaseChecked("ROT_DEV_PAIR_0002")
    # end def test_bad_sub_id

    @features('BLEDevicePairing')
    @level('Robustness')
    def test_Padding(self):
        """
        Padding bytes (p9 to pF) shall be ignored by the firmware
        """
        auth_method = DevicePairingTestUtils.get_authentication_method(self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over padding range (several interesting values)')
        # --------------------------------------------------------------------------------------------------------------
        for padding_byte in compute_wrong_range(
                HexList(Numeral(SetPerformDeviceConnectionRequest.DEFAULT.PADDING, 
                                SetPerformDeviceConnectionRequest.LEN.PADDING // 8)), range_size=5):
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'''Send 'Perform device connection' request with padding = {padding_byte}''')
            # ----------------------------------------------------------------------------------------------------------
            write_device_connect = SetPerformDeviceConnectionRequest(
                connect_devices=SetPerformDeviceConnectionRequest.ConnectState.PAIRING,
                bluetooth_address=self.device_bluetooth_address, 
                emu_2buttons_auth_method=auth_method == SetPerformDeviceConnectionRequest.MASK.EMU_2BUTTONS_AUTH_METHOD,
                passkey_auth_method=(auth_method == SetPerformDeviceConnectionRequest.MASK.PASSKEY_AUTH_METHOD))
            write_device_connect.padding = padding_byte
            write_device_connect_response = ChannelUtils.send(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                report=write_device_connect,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=SetPerformDeviceConnectionResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the response to the Write command is success')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PerformDeviceConnectionResponseChecker.check_fields(
                self, write_device_connect_response, SetPerformDeviceConnectionResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a start pairing status notification')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.check_start_pairing_status(self)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2("""Test Step 2: Send 'Perform device connection' request with Connect Devices = 2 i.e 
            Cancel Pairing""")
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.cancel_pairing(self, log_check=True)

        self.testCaseChecked("ROT_DEV_PAIR_0003")
    # end def test_Padding

    @features('BLEDevicePairing')
    @level('Robustness')
    def test_bad_connect_devices(self):
        """
        Send a device connection request with 'Connect Devices' value > 3
        """
        auth_method = DevicePairingTestUtils.get_authentication_method(self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over connect_devices invalid range')
        # --------------------------------------------------------------------------------------------------------------
        for wrong_connect_devices in compute_sup_values(SetPerformDeviceConnectionRequest.ConnectState.RESERVED, 
                                                        is_equal=True):
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'''Test Step 1: Send 'Perform device connection' request with Connect Devices = 
            {wrong_connect_devices}''')
            # ----------------------------------------------------------------------------------------------------------
            write_device_connect = SetPerformDeviceConnectionRequest(
                connect_devices=wrong_connect_devices,
                bluetooth_address=self.device_bluetooth_address, 
                emu_2buttons_auth_method=auth_method == SetPerformDeviceConnectionRequest.MASK.EMU_2BUTTONS_AUTH_METHOD,
                passkey_auth_method=(auth_method == SetPerformDeviceConnectionRequest.MASK.PASSKEY_AUTH_METHOD))
            write_device_connect_response = ChannelUtils.send(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self), report=write_device_connect,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                response_class_type=Hidpp1ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check HID++ 1.0 ERR_INVALID_PARAM_VALUE (11) Error Code returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=Hidpp1ErrorCodes.ERR_INVALID_PARAM_VALUE,
                             obtained=int(Numeral(write_device_connect_response.errorCode)),
                             msg='The errorCode parameter differs from the one expected')
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Perform Device Discovery to Cancel discovery')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.cancel_discovery(self)
        ChannelUtils.clean_messages(
            test_case=self,
            channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
            class_type=(DeviceDiscovery, DiscoveryStatus))

        self.testCaseChecked("ROT_DEV_PAIR_0004")
    # end def test_bad_connect_devices

    @features('BLEDevicePairing')
    @level('Robustness')
    def test_ignore_reserved(self):
        """
        The 'Requested Authentication method' reserved bits shall be ignored by the firmware
        """
        auth_method = DevicePairingTestUtils.get_authentication_method(self)
        current_pairing_slot = None
        for reserved_bits in compute_wrong_range(
                                    SetPerformDeviceConnectionRequest.DEFAULT.RESERVED, range_size=3,
                                    max_value=pow(2, SetPerformDeviceConnectionRequest.LEN.RESERVED_AUTH_METHOD) - 1):
            # Retrieve a new device BT address
            self.device_bluetooth_address = DiscoveryTestUtils.discover_device(self)

            if current_pairing_slot is not None:
                # Previous connection is lost when starting the new sequence
                device_connection = ChannelUtils.get_only(
                    test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                    queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection)

                device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
                device_info = device_info_class.fromHexList(HexList(device_connection.information))
                assert (int(Numeral(device_info.device_info_link_status)) ==
                        DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'''Test Step 1: Send 'Perform device connection' request with auth_method_reserved=
            {reserved_bits}''')
            # ----------------------------------------------------------------------------------------------------------
            write_device_connect = SetPerformDeviceConnectionRequest(
                connect_devices=SetPerformDeviceConnectionRequest.ConnectState.PAIRING,
                bluetooth_address=self.device_bluetooth_address,
                emu_2buttons_auth_method=(auth_method ==
                                          SetPerformDeviceConnectionRequest.MASK.EMU_2BUTTONS_AUTH_METHOD),
                passkey_auth_method=(auth_method == SetPerformDeviceConnectionRequest.MASK.PASSKEY_AUTH_METHOD))
            write_device_connect.reserved_auth_method = reserved_bits
            write_device_connect_response = ChannelUtils.send(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                report=write_device_connect,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=SetPerformDeviceConnectionResponse)
            DevicePairingTestUtils.set_remaining_entropy(
                self, auth_entropy=SetPerformDeviceConnectionRequest.DEFAULT.ENTROPY_LENGTH_MAX)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the response to the Write command is success')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PerformDeviceConnectionResponseChecker.check_fields(
                self, write_device_connect_response, SetPerformDeviceConnectionResponse)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a start pairing status notification')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.check_start_pairing_status(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a display passkey notification')
            # ----------------------------------------------------------------------------------------------------------
            passkey_digits = DevicePairingTestUtils.PairingChecker.get_passkey_digits(self)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('''Test Check 4: Wait for a 'Digit Start' passkey notification''')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.get_display_passkey_start(self)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2("Test Step 2: Loop over passkey inputs list provided by the receiver")
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.generate_keystrokes(self, passkey_digits, log_check=True)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2("Test Step 3: User enters the last passkey input")
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.generate_end_of_sequence(self, log_check=True)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('''Test Check 6: Wait for a stop pairing status notification''')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.check_stop_pairing_status(self)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('''Test Check 7: Wait for a device connection notification''')
            # ----------------------------------------------------------------------------------------------------------
            device_connection = ChannelUtils.get_only(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection)

            device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
            device_info = device_info_class.fromHexList(HexList(device_connection.information))
            assert (int(Numeral(device_info.device_info_link_status)) == DeviceConnection.LinkStatus.LINK_ESTABLISHED)
            current_pairing_slot = int(Numeral(device_connection.pairing_slot))
        # end for

        self.testCaseChecked("ROT_DEV_PAIR_0005")
    # end def test_ignore_reserved

    @features('BLEDevicePairing')
    @level('Robustness')
    def test_more_than_max_connections(self):
        """
        Multiple connections: Pair the maximum allowed number of device to the receiver
        """
        auth_method = DevicePairingTestUtils.get_authentication_method(self)
        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2(
            "Pre-requisite#1: The 'Device Pairing' sequence had been completed successfully"
            "notification")
        # --------------------------------------------------------------------------------------------------------------
        self.pairing_slot_list = []
        current_pairing_slot = None
        for i in range(DevicePairingTestUtils.NvsManager.RECEIVER_PAIRING_SLOT_COUNT):
            # Retrieve current device BT address
            self.device_bluetooth_address = DiscoveryTestUtils.discover_device(self)

            if current_pairing_slot is not None:
                # Previous connection is lost when starting the new sequence
                device_connection = ChannelUtils.get_only(
                    test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                    queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection)

                device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
                device_info = device_info_class.fromHexList(HexList(device_connection.information))
                assert (int(Numeral(device_info.device_info_link_status)) ==
                        DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED)
            # end if
            # Pair the discovered device
            current_pairing_slot = DevicePairingTestUtils.pair_device(self, self.device_bluetooth_address)
            self.pairing_slot_list.append(current_pairing_slot)
            if current_pairing_slot == DevicePairingTestUtils.NvsManager.RECEIVER_PAIRING_SLOT_COUNT:
                break
            # end if
        # end for

        # Retrieve current device BT address
        self.device_bluetooth_address = DiscoveryTestUtils.discover_device(self)
        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2("Test Step 1: Send 'Perform device connection' request with Connect Devices = 1")
        # --------------------------------------------------------------------------------------------------------------
        write_device_connect = SetPerformDeviceConnectionRequest(
            connect_devices=SetPerformDeviceConnectionRequest.ConnectState.PAIRING,
            bluetooth_address=self.device_bluetooth_address, 
            emu_2buttons_auth_method=(auth_method == SetPerformDeviceConnectionRequest.MASK.EMU_2BUTTONS_AUTH_METHOD),
            passkey_auth_method=(auth_method == SetPerformDeviceConnectionRequest.MASK.PASSKEY_AUTH_METHOD))
        write_device_connect_response = ChannelUtils.send(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self), report=write_device_connect,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
            response_class_type=Hidpp1ErrorCodes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check HID++ 1.0 ERR_TOO_MANY_DEVICES (5) Error Code returned by the device')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=Hidpp1ErrorCodes.ERR_TOO_MANY_DEVICES,
                         obtained=int(Numeral(write_device_connect_response.errorCode)),
                         msg='The errorCode parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Perform Device Discovery to Cancel discovery')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.cancel_discovery(self)
        ChannelUtils.clean_messages(
            test_case=self,
            channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
            class_type=(DeviceDiscovery, DiscoveryStatus))

        self.testCaseChecked("ROT_DEV_PAIR_0006")
    # end def test_more_than_max_connections

    @features('BLEDevicePairing')
    @level('Robustness')
    def test_notifications_disabled(self):
        """
        All Discovery & Pairing Notifications shall be enabled by 'Enable HID++ reporting' request
        """
        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2(f'''Test Step 1: Send 'Enable HID++ Reporting' request with wireless flag reset''')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.set_hidpp_reporting(test_case=self, enable=False)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2("Test Step 2: Send 'Perform device connection' request with Connect Devices = 1 i.e. Pairing")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.start_pairing_sequence(self, self.device_bluetooth_address, log_check=True)

        # Wait a short delay
        sleep(3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'No pairing notifications shall be issued')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.check_notifications_absence(self)

        # Re-enable HID++ reporting
        ChannelUtils.set_hidpp_reporting(test_case=self, enable=True)

        self.testCaseChecked("ROT_DEV_PAIR_0007")
    # end def test_notifications_disabled

    @features('BLEDevicePairing')
    @level('Robustness')
    def test_connect_both_authentication_method(self):
        """
        Ask several authentification method at the same time: parameters p8 = 0x03
        """
        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2("Test Step 1: Send 'Perform device connection' request with both authentication method enabled")
        # --------------------------------------------------------------------------------------------------------------
        write_device_connect = SetPerformDeviceConnectionRequest(
            connect_devices=SetPerformDeviceConnectionRequest.ConnectState.PAIRING,
            bluetooth_address=self.device_bluetooth_address,
            emu_2buttons_auth_method=True, passkey_auth_method=True)
        write_device_connect_response = ChannelUtils.send(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self), report=write_device_connect,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
            response_class_type=Hidpp1ErrorCodes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check HID++ 1.0 ERR_INVALID_PARAM_VALUE (11) Error Code returned by the device')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=Hidpp1ErrorCodes.ERR_INVALID_PARAM_VALUE,
                         obtained=int(Numeral(write_device_connect_response.errorCode)),
                         msg='The errorCode parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Perform Device Discovery to Cancel discovery')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.cancel_discovery(self)
        ChannelUtils.clean_messages(
            test_case=self,
            channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
            class_type=(DeviceDiscovery, DiscoveryStatus))

        self.testCaseChecked("ROT_DEV_PAIR_0008")
    # end def test_connect_both_authentication_method

    @features('BLEDevicePairing')
    @features('PasskeyAuthenticationMethod')
    @level('Robustness')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_DELETE_FORWARD,))
    def test_ignore_del_key(self):
        """
        Verify the "Del key" is ignored by the firmware in standard passkey emulation authentication method.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'start the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('''Test Step 2: Send 'Perform device connection' request with Connect Devices = 1 (i.e 
            Pairing)''')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.start_pairing_sequence(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a start pairing status notification')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.check_start_pairing_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a display passkey notification')
        # --------------------------------------------------------------------------------------------------------------
        passkey_digits = DevicePairingTestUtils.PairingChecker.get_passkey_digits(self)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('''Test Check 3: Wait for a 'Digit Start' passkey notification''')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.get_display_passkey_start(self)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2("Test Step 3: Loop over passkey inputs list provided by the receiver except the last one")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.generate_keystrokes(self, passkey_digits, end=0, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2("Test Step 4: Delete the previous key press")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.press_delete_key(self, key_name='del', ignore_erased_notification=True)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2("Test Step 5: Enter the last key")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.generate_keystrokes(self, passkey_digits, start=0, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 6: User enters the end of sequence input')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.generate_end_of_sequence(self)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 7: Wait for a stop pairing status notification')
        # --------------------------------------------------------------------------------------------------------------
        pairing_slot = DevicePairingTestUtils.PairingChecker.check_stop_pairing_status(self)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 8: Wait for a device connection notification')
        # --------------------------------------------------------------------------------------------------------------
        message_count = 0
        while message_count < 5:
            device_connection = ChannelUtils.get_only(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection)
            device_info_class = self.get_device_info_bit_field_structure_in_device_connection(
                device_connection)
            device_info = device_info_class.fromHexList(HexList(device_connection.information))
            if pairing_slot == device_connection.pairing_slot:
                assert (int(Numeral(device_info.device_info_link_status)) ==
                        DeviceConnection.LinkStatus.LINK_ESTABLISHED)
                break
            # end if
            message_count += 1
        # end for

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 7: Unpair the device')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.unpair_slot(self, int(Numeral(pairing_slot)))

        self.testCaseChecked("ROT_DEV_PAIR_0009")
    # end def test_ignore_del_key
# end class SharedPairingRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
