#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.connectionscheme.pairing_functionality
:brief: Validate device pairing feature
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2020/04/07
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC
from random import choice
from time import sleep

from pychannel.throughreceiverchannel import ThroughReceiverChannel
from pychannel.usbchannel import UsbReceiverChannel
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.hidpp1model import Hidpp1Model
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.notifications.devicedisconnection import DeviceDisconnection
from pyhid.hidpp.hidpp1.notifications.devicediscovery import DeviceDiscovery
from pyhid.hidpp.hidpp1.notifications.discoverystatus import DiscoveryStatus
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetBLEProDevicePairingInfoRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetBLEProDevicePairingInfoResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import NonVolatilePairingInformation
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionRequest
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.threadutils import QueueEmpty
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.unifiedbatteryutils import UnifiedBatteryTestUtils
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.connectionscheme.pairing import SharedCommonPairingTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SharedPairingFunctionalityTestCase(SharedCommonPairingTestCase, ABC):
    """
    Shared Pairing Functional TestCases
    """
    MID_SEQUENCE_INDEX = 3

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
    @level('Functionality')
    def test_no_change(self):
        """
        Send a device connection request with 'Connect Devices' parameter equal to 0 = Reserved (previously 'No change')
        """
        auth_method = DevicePairingTestUtils.get_authentication_method(self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform device connection request with Connect Devices = 0")
        # --------------------------------------------------------------------------------------------------------------
        write_device_connect = SetPerformDeviceConnectionRequest(
            connect_devices=SetPerformDeviceConnectionRequest.ConnectState.RESERVED_0,
            bluetooth_address=self.device_bluetooth_address,
            emu_2buttons_auth_method=(auth_method == SetPerformDeviceConnectionRequest.MASK.EMU_2BUTTONS_AUTH_METHOD),
            passkey_auth_method=(auth_method == SetPerformDeviceConnectionRequest.MASK.PASSKEY_AUTH_METHOD))
        err_resp = ChannelUtils.send(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self), report=write_device_connect,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
            response_class_type=Hidpp1ErrorCodes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check error response')
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
            self,
            err_resp,
            Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
            Hidpp1Data.Hidpp1RegisterAddress.PERFORM_DEVICE_CONNECTION_DISCONNECTION,
            [Hidpp1ErrorCodes.ERR_INVALID_PARAM_VALUE])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Perform Device Discovery to Cancel discovery')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.cancel_discovery(self)
        ChannelUtils.clean_messages(
            test_case=self,
            channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
            class_type=(DeviceDiscovery, DiscoveryStatus))

        self.testCaseChecked("FNT_DEV_PAIR_0003")
    # end def test_no_change

    @features('BLEDevicePairing')
    @level('Functionality')
    def test_connect(self):
        """
        Send a device connection request with 'Connect Devices' parameter equal to 1 = Pairing
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform device connection request with Connect Devices = 1 i.e. Pairing")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.start_pairing_sequence(self, self.device_bluetooth_address, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a start pairing status notification')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.check_start_pairing_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a display passkey notification')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.get_passkey_digits(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a Digit Start passkey notification')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.get_display_passkey_start(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform device connection request with Connect Devices = Cancel Pairing")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.cancel_pairing(self, log_check=True)

        self.testCaseChecked("FNT_DEV_PAIR_0004")
    # end def test_connect

    @features('BLEDevicePairing')
    @level('Functionality')
    def test_connect_while_connection_ongoing(self):
        """
        Send a device connection request with 'Connect Devices' parameter equal to '1 = Pairing'
        while a connection request has already been sent to the receiver.

        Check the new Perform Device Connection will be rejected (ERR_BUSY).
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform device connection request with Connect Devices = 1 i.e. Pairing")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.start_pairing_sequence(self, self.device_bluetooth_address, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a start pairing status notification')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.check_start_pairing_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a display passkey notification')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.get_passkey_digits(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a Digit Start passkey notification')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.get_display_passkey_start(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Resend 'Perform device connection' request with Connect Devices = 1")
        # --------------------------------------------------------------------------------------------------------------
        auth_method = DevicePairingTestUtils.get_authentication_method(self)
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
        LogHelper.log_check(self, 'Check HID++ 1.0 ERR_BUSY (7) Error Code returned by the device')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=Hidpp1ErrorCodes.ERR_BUSY,
                         obtained=int(Numeral(write_device_connect_response.errorCode)),
                         msg='The errorCode parameter differs from the one expected')

        self.testCaseChecked("FNT_DEV_PAIR_0005")
    # end def test_connect_while_connection_ongoing

    @features('BLEDevicePairing')
    @level('Functionality')
    def test_connect_while_connection_established(self):
        """
        Send a device connection request with 'Connect Devices' parameter equal to '1 = Pairing'
        while a connection is already established with the targeted device
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "The 'Device Pairing' sequence successfully returns a stop pairing "
                                         "notification")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.pair_device(self, self.device_bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform device connection request with Connect Devices = 1 i.e. Pairing")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.start_pairing_sequence(self, self.device_bluetooth_address, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a start pairing status notification')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.check_start_pairing_status(self)

        sleep(self.START_PAIRING_TIMEOUT)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a timeout pairing status notification')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.check_timeout_pairing_status(self)

        self.testCaseChecked("FNT_DEV_PAIR_0006")
    # end def test_connect_while_connection_established

    @features('BLEDevicePairing')
    @level('Functionality')
    def test_connect_unmatching_bluetooth_address(self):
        """
        Send a device connection request with an unmatching bluetooth address.
        """
        for wrong_bluetooth_address in compute_wrong_range(self.device_bluetooth_address, range_size=5):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send Perform device connection request with bluetooth address != device BT '
                                     'address')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.start_pairing_sequence(self, wrong_bluetooth_address, log_check=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a start pairing status notification')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.check_start_pairing_status(self)

            sleep(self.START_PAIRING_TIMEOUT)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a timeout pairing status notification')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.check_timeout_pairing_status(self)
        # end for

        self.testCaseChecked("FNT_DEV_PAIR_0007")
    # end def test_connect_unmatching_bluetooth_address

    @features('BLEDevicePairing')
    @level('Functionality')
    def test_connect_unsupported_authentication_method(self):
        """
        Send a device connection request with 'Connect Devices' parameter equal to 1 = Pairing but
        an unsupported authentication method
        """
        if not self.config_manager.get_feature(ConfigurationManager.ID.IS_PLATFORM):
            auth_method = DevicePairingTestUtils.get_authentication_method(self)
        else:
            auth_method = SetPerformDeviceConnectionRequest.MASK.BOTH_AUTH_METHOD
        # end if
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform device connection' request with authentication method != device supported "
                                 "authentication method")
        # --------------------------------------------------------------------------------------------------------------
        write_device_connect = SetPerformDeviceConnectionRequest(
            connect_devices=SetPerformDeviceConnectionRequest.ConnectState.PAIRING,
            bluetooth_address=self.device_bluetooth_address,
            # Notice that below the mask fields are inverted to enable the unsupported method
            emu_2buttons_auth_method=(auth_method == SetPerformDeviceConnectionRequest.MASK.PASSKEY_AUTH_METHOD),
            passkey_auth_method=(auth_method == SetPerformDeviceConnectionRequest.MASK.EMU_2BUTTONS_AUTH_METHOD))
        write_device_connect_response = ChannelUtils.send(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self), report=write_device_connect,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=SetPerformDeviceConnectionResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the response to the Write command is success')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PerformDeviceConnectionResponseChecker.check_fields(self, write_device_connect_response,
                                                                                   SetPerformDeviceConnectionResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a start pairing status notification')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.check_start_pairing_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a failed pairing status notification')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.check_failed_pairing_status(self)

        self.testCaseChecked("FNT_DEV_PAIR_0008")
    # end def test_connect_unsupported_authentication_method

    @features('BLEDevicePairing')
    @level('Functionality')
    def test_connect_bad_entropy(self):
        """
        Send a device connection request with 'Connect Devices' parameter equal to 1 = Connect but
        an unsupported authentication entropy length
        """
        auth_method = DevicePairingTestUtils.get_authentication_method(self)
        entropy_range = list(range(SetPerformDeviceConnectionRequest.DEFAULT.ENTROPY_LENGTH_MIN,
                                   SetPerformDeviceConnectionRequest.DEFAULT.ENTROPY_LENGTH_MAX+1))
        for wrong_entropy in compute_wrong_range(entropy_range):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send Perform device connection request with bluetooth address != device BT '
                                     'address')
            # ----------------------------------------------------------------------------------------------------------
            write_device_connect = SetPerformDeviceConnectionRequest(
                connect_devices=SetPerformDeviceConnectionRequest.ConnectState.PAIRING,
                bluetooth_address=self.device_bluetooth_address,
                emu_2buttons_auth_method=auth_method == SetPerformDeviceConnectionRequest.MASK.EMU_2BUTTONS_AUTH_METHOD,
                passkey_auth_method=(auth_method == SetPerformDeviceConnectionRequest.MASK.PASSKEY_AUTH_METHOD),
                auth_entropy=wrong_entropy)
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

        self.testCaseChecked("FNT_DEV_PAIR_0009")
    # end def test_connect_bad_entropy

    @features('BLEDevicePairing')
    @level('Functionality')
    def test_cancel(self):
        """
        Send a device connection request with 'Connect Devices' parameter equal to '2 = Cancel Pairing' connect
        while a connection is ongoing
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform device connection request with Connect Devices = 1 i.e. Pairing")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.start_pairing_sequence(self, self.device_bluetooth_address, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a start pairing status notification')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.check_start_pairing_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a display passkey notification')
        # --------------------------------------------------------------------------------------------------------------
        passkey_digits = DevicePairingTestUtils.PairingChecker.get_passkey_digits(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a Digit Start passkey notification')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.get_display_passkey_start(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Loop over part of the passkey inputs list provided by the receiver')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.generate_keystrokes(self, passkey_digits, end=self.MID_SEQUENCE_INDEX, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "'Perform device connection' request with Connect Devices = Cancel Pairing")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.cancel_pairing(self, log_check=True)

        self.testCaseChecked("FNT_DEV_PAIR_0010")
    # end def test_cancel

    @features('BLEDevicePairing')
    @level('Functionality')
    def test_cancel_no_connection(self):
        """
        Send a device connection request with 'Connect Devices' parameter equal to '2 = Cancel Pairing'
        while no connection on going
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform device connection request with Connect Devices = Cancel Pairing")
        # --------------------------------------------------------------------------------------------------------------
        write_device_connect = SetPerformDeviceConnectionRequest(
            connect_devices=SetPerformDeviceConnectionRequest.ConnectState.CANCEL_PAIRING)
        write_device_connect_response = ChannelUtils.send(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self), report=write_device_connect,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=SetPerformDeviceConnectionResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the response to the Write command is success')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PerformDeviceConnectionResponseChecker.check_fields(
            self, write_device_connect_response, SetPerformDeviceConnectionResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a cancel pairing status notification')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.check_cancel_pairing_status(self, bypass_address_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Perform Device Discovery to Cancel discovery')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.cancel_discovery(self)
        ChannelUtils.clean_messages(
            test_case=self,
            channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
            class_type=(DeviceDiscovery, DiscoveryStatus))

        self.testCaseChecked("FNT_DEV_PAIR_0011")
    # end def test_cancel_no_connection

    @features('BLEDevicePairing')
    @level('Functionality')
    def test_cancel_unmatching_bt_address(self):
        """
        Send a device connection request with 'Connect Devices' parameter equal to '2 = Cancel Pairing'
        while a connection is ongoing
        Check this parameter is ignored in Cancel mode.
        """
        for wrong_bluetooth_address in compute_wrong_range(self.device_bluetooth_address, range_size=5):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Perform device connection request with Connect Devices = 1 i.e. Pairing")
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.start_pairing_sequence(self, self.device_bluetooth_address, log_check=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a start pairing status notification')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.check_start_pairing_status(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a display passkey notification')
            # ----------------------------------------------------------------------------------------------------------
            passkey_digits = DevicePairingTestUtils.PairingChecker.get_passkey_digits(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a Digit Start passkey notification')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.get_display_passkey_start(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Loop over part of the passkey inputs list provided by the receiver')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.generate_keystrokes(
                self, passkey_digits, end=self.MID_SEQUENCE_INDEX, log_check=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Perform device connection request with Connect Devices = 2 and bluetooth "
                                     "address != device BT address")
            # ----------------------------------------------------------------------------------------------------------
            write_device_connect = SetPerformDeviceConnectionRequest(
                connect_devices=SetPerformDeviceConnectionRequest.ConnectState.CANCEL_PAIRING,
                bluetooth_address=wrong_bluetooth_address)
            write_device_connect_response = ChannelUtils.send(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self), report=write_device_connect,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=SetPerformDeviceConnectionResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the response to the Write command is success')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PerformDeviceConnectionResponseChecker.check_fields(
                self, write_device_connect_response, SetPerformDeviceConnectionResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a cancel pairing status notification')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.check_cancel_pairing_status(self)
        # end for

        self.testCaseChecked("FNT_DEV_PAIR_0012")
    # end def test_cancel_unmatching_bt_address

    @features('BLEDevicePairing')
    @level('Functionality')
    def test_cancel_unmatching_authentication_method(self):
        """
        Send a device connection request with 'Connect Devices' parameter equal to '2 = Cancel' connect,
        a connection ongoing but an unsupported authentication method.
        Check this parameter is ignored in Cancel mode.
        """
        for reserved_bits in compute_wrong_range(
                SetPerformDeviceConnectionRequest.DEFAULT.RESERVED, range_size=3,
                max_value=pow(2, SetPerformDeviceConnectionRequest.LEN.RESERVED_AUTH_METHOD) - 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Perform device connection request with Connect Devices = 1 i.e. Pairing")
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.start_pairing_sequence(self, self.device_bluetooth_address, log_check=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a start pairing status notification')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.check_start_pairing_status(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a display passkey notification')
            # ----------------------------------------------------------------------------------------------------------
            passkey_digits = DevicePairingTestUtils.PairingChecker.get_passkey_digits(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a Digit Start passkey notification')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.get_display_passkey_start(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Loop over part of the passkey inputs list provided by the receiver')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.generate_keystrokes(
                self, passkey_digits, end=self.MID_SEQUENCE_INDEX, log_check=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Perform device connection request with Connect Devices = 2 and "
                                     "authentication method != device supported authentication method")
            # ----------------------------------------------------------------------------------------------------------
            write_device_connect = SetPerformDeviceConnectionRequest(
                connect_devices=SetPerformDeviceConnectionRequest.ConnectState.CANCEL_PAIRING,
                bluetooth_address=self.device_bluetooth_address)
            write_device_connect.reserved_auth_method = reserved_bits
            write_device_connect_response = ChannelUtils.send(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self), report=write_device_connect,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=SetPerformDeviceConnectionResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the response to the Write command is success')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PerformDeviceConnectionResponseChecker.check_fields(
                                    self, write_device_connect_response, SetPerformDeviceConnectionResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a cancel pairing status notification')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.check_cancel_pairing_status(self)
        # end for

        self.testCaseChecked("FNT_DEV_PAIR_0013")
    # end def test_cancel_unmatching_authentication_method

    @features('BLEDevicePairing')
    @level('Functionality')
    def test_cancel_bad_entropy(self):
        """
        Send a device connection request with 'Connect Devices' parameter equal to '2 = Cancel Pairing' while
        a connection is ongoing but an unsupported authentication entropy length.
        Check this parameter is ignored in Cancel mode.
        """
        entropy_range = list(range(SetPerformDeviceConnectionRequest.DEFAULT.ENTROPY_LENGTH_MIN,
                                   SetPerformDeviceConnectionRequest.DEFAULT.ENTROPY_LENGTH_MAX + 1))
        for wrong_entropy in compute_wrong_range(entropy_range):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Perform device connection request with Connect Devices = 1 i.e. Pairing")
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.start_pairing_sequence(self, self.device_bluetooth_address, log_check=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a start pairing status notification')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.check_start_pairing_status(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a display passkey notification')
            # ----------------------------------------------------------------------------------------------------------
            passkey_digits = DevicePairingTestUtils.PairingChecker.get_passkey_digits(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a Digit Start passkey notification')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.get_display_passkey_start(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Loop over part of the passkey inputs list provided by the receiver')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.generate_keystrokes(
                self, passkey_digits, end=self.MID_SEQUENCE_INDEX, log_check=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Perform device connection request with Connect Devices = 2 and "
                                     "authentication method != device supported authentication method")
            # ----------------------------------------------------------------------------------------------------------
            write_device_connect = SetPerformDeviceConnectionRequest(
                connect_devices=SetPerformDeviceConnectionRequest.ConnectState.CANCEL_PAIRING,
                auth_entropy=wrong_entropy)
            write_device_connect_response = ChannelUtils.send(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self), report=write_device_connect,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=SetPerformDeviceConnectionResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the response to the Write command is success')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PerformDeviceConnectionResponseChecker.check_fields(
                                    self, write_device_connect_response, SetPerformDeviceConnectionResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a cancel pairing status notification')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.check_cancel_pairing_status(self)
        # end for

        self.testCaseChecked("FNT_DEV_PAIR_0014")
    # end def test_cancel_bad_entropy

    @features('BLEDevicePairing')
    @level('Functionality')
    def test_restart_after_cancel(self):
        """
        Start Pairing, then Cancel Pairing while a connection is ongoing. Then repeat in a loop to check Pairing can
        always be restarted after cancel.
        """
        loop_count = 100  # ~3 minutes for 100 loops
        failure_count = 0
        for loop_index in range(loop_count):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Loop {loop_index}: Start Pairing')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.start_pairing_sequence(self, self.device_bluetooth_address)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Loop {loop_index}: Wait for a start pairing status notification')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.check_start_pairing_status(self)

            try:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f'Loop {loop_index}: Wait for a display passkey notification')
                # ------------------------------------------------------------------------------------------------------
                DevicePairingTestUtils.PairingChecker.get_passkey_digits(self)
            except (AssertionError, QueueEmpty):
                failure_count += 1
                self.log_traceback_as_warning(supplementary_message=f'Failure {failure_count}: ',
                                              force_console_print=self.f.LOGGING.F_LogHelperVerbose)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Loop {loop_index}: Send Cancel Pairing request')
                # ------------------------------------------------------------------------------------------------------
                write_device_connect = SetPerformDeviceConnectionRequest(
                    connect_devices=SetPerformDeviceConnectionRequest.ConnectState.CANCEL_PAIRING)
                write_device_connect_response = ChannelUtils.send(
                    test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                    report=write_device_connect,
                    response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                    response_class_type=SetPerformDeviceConnectionResponse)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f'Loop {loop_index}: Check successful response')
                # ------------------------------------------------------------------------------------------------------
                DevicePairingTestUtils.PerformDeviceConnectionResponseChecker.check_fields(
                    self, write_device_connect_response, SetPerformDeviceConnectionResponse)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f'Loop {loop_index}: Wait for a cancel pairing status notification')
                # ------------------------------------------------------------------------------------------------------
                DevicePairingTestUtils.PairingChecker.check_cancel_pairing_status(self)

                continue
            # end try

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Loop {loop_index}: Wait for a "Digit Start" passkey notification')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.get_display_passkey_start(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Loop {loop_index}: Send Cancel Pairing request')
            # ----------------------------------------------------------------------------------------------------------
            write_device_connect = SetPerformDeviceConnectionRequest(
                connect_devices=SetPerformDeviceConnectionRequest.ConnectState.CANCEL_PAIRING)
            write_device_connect_response = ChannelUtils.send(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self), report=write_device_connect,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=SetPerformDeviceConnectionResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Loop {loop_index}: Check successful response')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PerformDeviceConnectionResponseChecker.check_fields(
                self, write_device_connect_response, SetPerformDeviceConnectionResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Loop {loop_index}: Wait for a cancel pairing status notification')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.check_cancel_pairing_status(self)
        # end for

        self.assertEqual(obtained=failure_count, expected=0,
                         msg=f'{failure_count} failures on pairing start ({failure_count * 100 / loop_count}%)')

        self.testCaseChecked("FNT_DEV_PAIR_0048")
    # end def test_restart_after_cancel

    @features('BLEDevicePairing')
    @level('Functionality')
    def test_unpair_no_connection(self):
        """
        Unpair use case:
        Send a device connection request with 'Connect Devices' parameter equal to 3 = Disconnect (unpair)
        while no connection exists
        """
        for slot_to_unplug in range(2, DevicePairingTestUtils.NvsManager.RECEIVER_PAIRING_SLOT_COUNT+1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send 'Perform device connection' request with Connect Devices = 3 and "
                                     f"index=0xFF")
            # ----------------------------------------------------------------------------------------------------------
            write_device_disconnect = SetPerformDeviceConnectionRequest(
                pairing_slot_to_be_unpaired=slot_to_unplug,
                connect_devices=SetPerformDeviceConnectionRequest.ConnectState.UNPAIRING)
            write_device_disconnect_response = ChannelUtils.send(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                report=write_device_disconnect,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                response_class_type=Hidpp1ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check HID++ 1.0 ERR_UNKNOWN_DEVICE (8) Error Code returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=Hidpp1ErrorCodes.ERR_UNKNOWN_DEVICE,
                             obtained=int(Numeral(write_device_disconnect_response.errorCode)),
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

        self.testCaseChecked("FNT_DEV_PAIR_0018")
    # end def test_unpair_no_connection

    @features('BLEDevicePairing')
    @level('Functionality')
    def _test_unplug_no_connection(self):
        """
        Unplug use case:
        Send a device connection request with 'Connect Devices' parameter equal to 3 = Disconnect (unplug)
        while no connection exists
        """
        for slot_to_unplug in range(2, DevicePairingTestUtils.NvsManager.RECEIVER_PAIRING_SLOT_COUNT+1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send 'Perform device connection' request with Connect Devices = 3 and index=0x0n")
            # ----------------------------------------------------------------------------------------------------------
            write_device_disconnect = SetPerformDeviceConnectionRequest(
                device_index=slot_to_unplug, connect_devices=SetPerformDeviceConnectionRequest.ConnectState.UNPAIRING)
            write_device_disconnect_response = ChannelUtils.send(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self), report=write_device_disconnect,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=SetPerformDeviceConnectionResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check HID++ 1.0 ERR_UNKNOWN_DEVICE (8) Error Code returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=Hidpp1ErrorCodes.ERR_UNKNOWN_DEVICE,
                             obtained=int(Numeral(write_device_disconnect_response.errorCode)),
                             msg='The errorCode parameter differs from the one expected')
        # end for

        self.testCaseChecked("FNT_DEV_PAIR_0019")
    # end def test_unplug_no_connection

    @features('BLEDevicePairing')
    @level('Functionality')
    def test_second_connection(self):
        """
        Multiple connections: Pair a second device to the receiver
        (add a mice device on top of a keyboard and vice versa)
        """
        # Retrieve current device BT address
        self.device_bluetooth_address = DiscoveryTestUtils.discover_device(self)

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
            LogHelper.log_step(self, "Send 'Perform device connection' request with Connect Devices = 1 i.e. Pairing")
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.start_pairing_sequence(self, self.device_bluetooth_address, log_check=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a start pairing status notification')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.check_start_pairing_status(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a display passkey notification')
            # ----------------------------------------------------------------------------------------------------------
            passkey_digits = DevicePairingTestUtils.PairingChecker.get_passkey_digits(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a Digit Start passkey notification')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.get_display_passkey_start(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Loop over passkey inputs list provided by the receiver')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.generate_keystrokes(self, passkey_digits, log_check=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "User enters the last passkey input")
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.generate_end_of_sequence(self, log_check=True)

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
            assert (int(Numeral(device_info.device_info_link_status)) == DeviceConnection.LinkStatus.LINK_ESTABLISHED)
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

        self.testCaseChecked("FNT_DEV_PAIR_0023")
    # end def test_second_connection

    @features('BLEDevicePairing')
    @level('Functionality')
    def test_max_connections(self):
        """
        Multiple connections: Pair the maximum allowed number of device to the receiver
        """
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

            # Add DeviceConnection notification to the event queue to enable notification sequence verification
            if isinstance(self.current_channel, UsbReceiverChannel):
                current_receiver_channel = self.current_channel
            elif isinstance(self.current_channel, ThroughReceiverChannel):
                current_receiver_channel = self.current_channel.receiver_channel
            else:
                assert False, \
                    "Cannot use this method on a channel other than UsbReceiverChannel or ThroughReceiverChannel"
            # end if

            current_receiver_channel.hid_dispatcher.receiver_event_queue.update_accepted_messages(
                Hidpp1Model.get_available_events_classes() + Hidpp1Model.get_connection_events_classes())

            try:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send 'Perform device connection' request with Connect Devices = 1 i.e. "
                                         "Pairing")
                # ------------------------------------------------------------------------------------------------------
                DevicePairingTestUtils.start_pairing_sequence(self, self.device_bluetooth_address, log_check=True)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Wait for a start pairing status notification')
                # ------------------------------------------------------------------------------------------------------
                DevicePairingTestUtils.PairingChecker.check_start_pairing_status(self)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Wait for a display passkey notification')
                # ------------------------------------------------------------------------------------------------------
                passkey_digits = DevicePairingTestUtils.PairingChecker.get_passkey_digits(self)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Wait for a Digit Start passkey notification')
                # ------------------------------------------------------------------------------------------------------
                DevicePairingTestUtils.PairingChecker.get_display_passkey_start(self)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Loop over passkey inputs list provided by the receiver")
                # ------------------------------------------------------------------------------------------------------
                DevicePairingTestUtils.generate_keystrokes(self, passkey_digits, log_check=True)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "User enters the last passkey input")
                # ------------------------------------------------------------------------------------------------------
                DevicePairingTestUtils.generate_end_of_sequence(self, log_check=True)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Wait for a stop pairing status notification')
                # ------------------------------------------------------------------------------------------------------
                DevicePairingTestUtils.PairingChecker.check_stop_pairing_status(self)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Wait for a device connection notification')
                # ------------------------------------------------------------------------------------------------------
                device_connection = ChannelUtils.get_only(
                    test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                    queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceConnection)

                device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
                device_info = device_info_class.fromHexList(HexList(device_connection.information))
                assert (int(Numeral(device_info.device_info_link_status)) ==
                        DeviceConnection.LinkStatus.LINK_ESTABLISHED)
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

            if int(Numeral(device_connection.pairing_slot)) == \
                    DevicePairingTestUtils.NvsManager.RECEIVER_PAIRING_SLOT_COUNT:
                break
            else:
                current_pairing_slot = int(Numeral(device_connection.pairing_slot))
            # end if
        # end for

        self.testCaseChecked("FNT_DEV_PAIR_0023")
    # end def test_max_connections

    @features('BLEDevicePairing')
    @features('PasskeyLowEntropy')
    @level('Functionality')
    def test_entropy_length(self):
        """
        Send a device connection request with 'Connect Devices' parameter equal to 1 = Pairing and entropy length
        within its valid range
        """
        # create the list of entropy length valid values but remove the 0x20 default one already tested elsewhere
        entropy_range_except_default = list(range(
            SetPerformDeviceConnectionRequest.DEFAULT.TWO_BUTTONS_EMULATION_ENTROPY_LENGTH_MIN,
            SetPerformDeviceConnectionRequest.DEFAULT.ENTROPY_LENGTH_MAX))
        for valid_entropy_value in entropy_range_except_default:
            # Retrieve current device BT address
            self.device_bluetooth_address = DiscoveryTestUtils.discover_device(self)

            # Add DeviceConnection notification to the event queue to enable notification sequence verification
            if isinstance(self.current_channel, UsbReceiverChannel):
                current_receiver_channel = self.current_channel
            elif isinstance(self.current_channel, ThroughReceiverChannel):
                current_receiver_channel = self.current_channel.receiver_channel
            else:
                assert False, \
                    "Cannot use this method on a channel other than UsbReceiverChannel or ThroughReceiverChannel"
            # end if

            current_receiver_channel.hid_dispatcher.receiver_event_queue.update_accepted_messages(
                Hidpp1Model.get_available_events_classes() + Hidpp1Model.get_connection_events_classes())

            try:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send 'Perform device connection' request with Connect Devices = 1")
                # ------------------------------------------------------------------------------------------------------
                auth_method = DevicePairingTestUtils.get_authentication_method(self)
                write_device_connect = SetPerformDeviceConnectionRequest(
                    connect_devices=SetPerformDeviceConnectionRequest.ConnectState.PAIRING,
                    bluetooth_address=self.device_bluetooth_address,
                    emu_2buttons_auth_method=(auth_method ==
                                              SetPerformDeviceConnectionRequest.MASK.EMU_2BUTTONS_AUTH_METHOD),
                    passkey_auth_method=(auth_method == SetPerformDeviceConnectionRequest.MASK.PASSKEY_AUTH_METHOD),
                    auth_entropy=valid_entropy_value)
                write_device_connect_response = ChannelUtils.send(
                    test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                    report=write_device_connect,
                    response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                    response_class_type=SetPerformDeviceConnectionResponse)
                DevicePairingTestUtils.set_remaining_entropy(self, auth_entropy=valid_entropy_value)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check the response to the Write command is success')
                # ------------------------------------------------------------------------------------------------------
                DevicePairingTestUtils.PerformDeviceConnectionResponseChecker.check_fields(
                                        self, write_device_connect_response, SetPerformDeviceConnectionResponse)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Wait for a start pairing status notification')
                # ------------------------------------------------------------------------------------------------------
                DevicePairingTestUtils.PairingChecker.check_start_pairing_status(self)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Wait for a display passkey notification')
                # ------------------------------------------------------------------------------------------------------
                passkey_digits = DevicePairingTestUtils.PairingChecker.get_passkey_digits(self)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Wait for a Digit Start passkey notification')
                # ------------------------------------------------------------------------------------------------------
                DevicePairingTestUtils.PairingChecker.get_display_passkey_start(self)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Loop over passkey inputs list provided by the receiver")
                # ------------------------------------------------------------------------------------------------------
                DevicePairingTestUtils.generate_keystrokes(
                    self, passkey_digits, start=valid_entropy_value-1, log_check=True)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "User enters the last passkey input")
                # ------------------------------------------------------------------------------------------------------
                DevicePairingTestUtils.generate_end_of_sequence(self, log_check=True)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Wait for a stop pairing status notification')
                # ------------------------------------------------------------------------------------------------------
                DevicePairingTestUtils.PairingChecker.check_stop_pairing_status(self)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Wait for a device connection notification')
                # ------------------------------------------------------------------------------------------------------
                device_connection = ChannelUtils.get_only(
                    test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                    queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DeviceConnection)

                device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
                device_info = device_info_class.fromHexList(HexList(device_connection.information))
                assert (int(Numeral(device_info.device_info_link_status)) ==
                        DeviceConnection.LinkStatus.LINK_ESTABLISHED)
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

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send Read BLE Pro device pairing information request')
            LogHelper.log_check(self, 'Validate BLE PRo device pairing information response is received')
            # ----------------------------------------------------------------------------------------------------------
            r0 = (NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_PAIRING_INFO_MIN & 0xF0) + int(Numeral(
                device_connection.pairing_slot))
            device_name_req = GetBLEProDevicePairingInfoRequest(r0)

            device_name_resp = ChannelUtils.send(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self), report=device_name_req,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=GetBLEProDevicePairingInfoResponse)
            self.assertTrue(int(Numeral(device_name_resp.auth_entropy)) ==
                            valid_entropy_value,
                            msg='Wrong auth_entropy parameter received in Get BLE Pro Device PairingInfo Response')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send 'Perform device connection' request with Connect Devices = 3 (Unpair)")
            # ----------------------------------------------------------------------------------------------------------
            slot_to_unpair = int(Numeral(device_connection.pairing_slot))
            write_device_connect = SetPerformDeviceConnectionRequest(
                connect_devices=SetPerformDeviceConnectionRequest.ConnectState.UNPAIRING,
                bluetooth_address=self.device_bluetooth_address,
                pairing_slot_to_be_unpaired=slot_to_unpair)
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
            LogHelper.log_check(self, 'Check Device disconnection notification received')
            # ----------------------------------------------------------------------------------------------------------
            device_disconnection = ChannelUtils.get_only(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceDisconnection,
                check_first_message=False)
            self.assertTrue(int(Numeral(device_disconnection.disconnection_type)) ==
                            DeviceDisconnection.PERMANENT_DISCONNECTION,
                            msg='Wrong disconnection_type parameter received in device disconnection notification')
            self.assertTrue(int(Numeral(device_disconnection.pairing_slot)) == slot_to_unpair,
                            msg='Wrong pairing_slot parameter received in device disconnection notification')
        # end for

        self.testCaseChecked("FNT_DEV_PAIR_0033")
    # end def test_entropy_length

    @features('BLEDevicePairing')
    @features('NoPasskeyLowEntropy')
    @level('Functionality')
    def test_blocked_entropy_length(self):
        """
        Send a device connection request with 'Connect Devices' parameter equal to 1 = Pairing and entropy length
        within its valid range for the device but blocked on the receiver side
        """
        # create the list of entropy length blocked values
        entropy_range_except_default = list(range(SetPerformDeviceConnectionRequest.DEFAULT.ENTROPY_LENGTH_MIN,
                                                  SetPerformDeviceConnectionRequest.DEFAULT.PASSKEY_ENTROPY_LENGTH_MIN))
        for valid_entropy_value in entropy_range_except_default:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send 'Perform device connection' request with Connect Devices = 1")
            # ----------------------------------------------------------------------------------------------------------
            write_device_connect = SetPerformDeviceConnectionRequest(
                connect_devices=SetPerformDeviceConnectionRequest.ConnectState.PAIRING,
                bluetooth_address=self.device_bluetooth_address, passkey_auth_method=True,
                auth_entropy=valid_entropy_value)
            write_device_connect_response = ChannelUtils.send(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                report=write_device_connect,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                response_class_type=Hidpp1ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check HID++ 1.0 ERR_INVALID_PARAM_VALUE (11) Error Code returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=Hidpp1ErrorCodes.ERR_INVALID_PARAM_VALUE,
                             obtained=int(Numeral(write_device_connect_response.errorCode)),
                             msg='The errorCode parameter differs from the one expected')
        # end for

        self.testCaseChecked("FNT_DEV_PAIR_0033")
    # end def test_blocked_entropy_length

    @features('BLEDevicePairing')
    @level('Time-consuming')
    def test_pairing_near_device_discovery_timeout(self):
        """
        Check Device Discovery Timeout has no impact. Start the pairing sequence in the last 10 seconds of the 3-min
        device discoverable period and complete it after the Discovery timeout occurs.
        Check Connectivity LED status while in 'Discoverable' and 'Acknowledge Pairing' modes.
        Check an HID Mouse report is received on the new pairing slot
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for entering the last 10 seconds of the 3 min device discoverable period')
        # --------------------------------------------------------------------------------------------------------------
        sleep(DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT - 10)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Move ahead with the Pairing sequence and check the successfully stop pairing '
                                 'notification')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.pair_device(self, self.device_bluetooth_address)

        self.testCaseChecked("FNT_DEV_PAIR_0033")
    # end def test_pairing_near_device_discovery_timeout

    @features('BLEDevicePairing')
    @level('Functionality')
    def test_cancel_near_device_discovery_timeout(self):
        """
        Check Device Discovery Timeout has no impact. Start the pairing sequence in the last 10 seconds of the 3-min
        device discoverable period then cancel it after the Discovery timeout occurs.
        Check Connectivity LED status while in 'Discoverable' and 'No Pairing' modes.
        Check No HID Mouse report is received on the pairing slot
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for entering the last 10 seconds of the 3 min device discoverable period')
        # --------------------------------------------------------------------------------------------------------------
        sleep(DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT - 10)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform device connection request with Connect Devices = 1 i.e. Pairing")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.start_pairing_sequence(self, self.device_bluetooth_address, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a start pairing status notification')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.check_start_pairing_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a display passkey notification')
        # --------------------------------------------------------------------------------------------------------------
        passkey_digits = DevicePairingTestUtils.PairingChecker.get_passkey_digits(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a Digit Start passkey notification')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.get_display_passkey_start(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Loop over part of the passkey inputs list provided by the receiver')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.generate_keystrokes(self, passkey_digits, end=self.MID_SEQUENCE_INDEX, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform device connection request with Connect Devices = 2 i.e Cancel Pairing")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.cancel_pairing(self, log_check=True)

        self.testCaseChecked("FNT_DEV_PAIR_0034")
    # end def test_cancel_near_device_discovery_timeout

    @features('BLEDevicePairing')
    @level('Functionality')
    @services('PowerSupply')
    def test_battery_level(self):
        """
        Battery level impact: Complete a pairing sequence whatever the voltage level
        (mainly in Critical level, close to cut-off).
        """
        f = self.getFeatures()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over battery_level in range [FULL..CRITICAL]')
        # --------------------------------------------------------------------------------------------------------------
        for i in range(len(f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_SupportedLevels)):
            state_of_charge = int(f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_SupportedLevels[i])
            battery_value = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, state_of_charge)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set battery level to {battery_value}V')
            # ----------------------------------------------------------------------------------------------------------
            self.power_supply_emulator.set_voltage(battery_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'start the discovery sequence')
            # ----------------------------------------------------------------------------------------------------------
            bluetooth_address = DiscoveryTestUtils.discover_device(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'start the pairing sequence')
            # ----------------------------------------------------------------------------------------------------------
            pairing_slot = DevicePairingTestUtils.pair_device(self, bluetooth_address)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Unpair the device')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.unpair_slot(self, pairing_slot)

        self.testCaseChecked("FNT_DEV_PAIR_0037")
    # end def test_battery_level
# end class SharedPairingFunctionalityTestCase


class SharedUnpairingFunctionalityTestCase(SharedCommonPairingTestCase, ABC):
    """
    Shared Unpairing Functional TestCases
    """
    def setUp(self):
        """
        Handles test prerequisites.
        """
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "The 'Device Pairing' sequence had been completed successfully")
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
    # end def setUp

    def tearDown(self):
        """
        Handles test post-requisites.
        """
        try:
            # Empty event queue
            self.clean_device_discovery_notifications()
        except AttributeError:
            self.log_traceback_as_warning(supplementary_message="Exception in tearDown:")
        # end try

        super().tearDown()
    # end def tearDown

    @features('BLEDevicePairing')
    @level('Functionality')
    def test_unpair(self):
        """
        Unpair use case:
        Send a device connection request with 'Connect Devices' parameter equal to 3 = Unpairing
        while a device connection is established
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform device connection request with Connect Devices = 3 i.e. Unpairing "
                                 "and index=0xFF")
        # --------------------------------------------------------------------------------------------------------------
        slot_to_unpair = choice(self.pairing_slot_list[:-1])
        write_device_connect = SetPerformDeviceConnectionRequest(
            connect_devices=SetPerformDeviceConnectionRequest.ConnectState.UNPAIRING,
            pairing_slot_to_be_unpaired=slot_to_unpair)
        write_device_connect_response = ChannelUtils.send(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            report=write_device_connect,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=SetPerformDeviceConnectionResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the response to the Write command is success')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PerformDeviceConnectionResponseChecker.check_fields(self, write_device_connect_response,
                                                                                   SetPerformDeviceConnectionResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device disconnection notification received')
        # --------------------------------------------------------------------------------------------------------------
        device_disconnection = ChannelUtils.get_only(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceDisconnection)
        self.assertTrue(int(Numeral(device_disconnection.disconnection_type)) ==
                        DeviceDisconnection.PERMANENT_DISCONNECTION,
                        msg='Wrong disconnection_type parameter received in device disconnection notification')
        self.assertTrue(int(Numeral(device_disconnection.pairing_slot)) == slot_to_unpair,
                        msg='Wrong pairing_slot parameter received in device disconnection notification')

        self.testCaseChecked("FNT_DEV_PAIR_0015")
    # end def test_unpair

    @features('BLEDevicePairing')
    @level('Functionality')
    def test_unpair_unmatching_bt_address(self):
        """
        Unpair use case:
        Send a device connection request with 'Connect Devices' parameter equal to 3 = Unpairing
        while a device connection is established
        Check this parameter is ignored in Disconnect mode.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform device connection request with Connect Devices = 3 and index=0xFF")
        # --------------------------------------------------------------------------------------------------------------
        slot_to_unpair = choice(self.pairing_slot_list[:-1])
        wrong_bluetooth_address = HexList(self.device_bluetooth_address)
        wrong_bluetooth_address.invertBit(0)
        write_device_connect = SetPerformDeviceConnectionRequest(
            connect_devices=SetPerformDeviceConnectionRequest.ConnectState.UNPAIRING,
            bluetooth_address=wrong_bluetooth_address,
            pairing_slot_to_be_unpaired=slot_to_unpair)
        write_device_connect_response = ChannelUtils.send(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            report=write_device_connect,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=SetPerformDeviceConnectionResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the response to the Write command is success')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PerformDeviceConnectionResponseChecker.check_fields(self, write_device_connect_response,
                                                                                   SetPerformDeviceConnectionResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device disconnection notification received')
        # --------------------------------------------------------------------------------------------------------------
        device_disconnection = ChannelUtils.get_only(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceDisconnection)
        self.assertTrue(int(Numeral(device_disconnection.disconnection_type)) ==
                        DeviceDisconnection.PERMANENT_DISCONNECTION,
                        msg='Wrong disconnection_type parameter received in device disconnection notification')
        self.assertTrue(int(Numeral(device_disconnection.pairing_slot)) == slot_to_unpair,
                        msg='Wrong pairing_slot parameter received in device disconnection notification')

        self.testCaseChecked("FNT_DEV_PAIR_0020")
    # end def test_unpair_unmatching_bt_address
# end class SharedUnpairingFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
