#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.shared.base.devicepairingutils
:brief:  Helpers for device pairing feature
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2020/04/14
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
import sys
from time import perf_counter_ns
from time import sleep
from time import time

from pychannel.throughreceiverchannel import ThroughBleProReceiverChannel
from pyharness.extensions import WarningLevel
from pyhid.hid.hidconsumer import HidConsumer
from pyhid.hid.hidkeyboard import HidKeyboard
from pyhid.hid.hidkeyboardbitmap import HidKeyboardBitmap
from pyhid.hid.hidmouse import HidMouse
from pyhid.hid.usbhidusagetable import KEYBOARD_HID_USAGE
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.deviceinformation import ascii_converter
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.features.root import Root
from pyhid.hidpp.hidpp1.hidpp1message import Hidpp1Message
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.notifications.devicedisconnection import DeviceDisconnection
from pyhid.hidpp.hidpp1.notifications.devicediscovery import DeviceDiscovery
from pyhid.hidpp.hidpp1.notifications.devicerecovery import DeviceRecovery
from pyhid.hidpp.hidpp1.notifications.discoverystatus import DiscoveryStatus
from pyhid.hidpp.hidpp1.notifications.displaypasskeykey import DisplayPassKeyKey
from pyhid.hidpp.hidpp1.notifications.pairingstatus import PairingStatus
from pyhid.hidpp.hidpp1.notifications.requestdisplaypasskey import RequestDisplayPassKey
from pyhid.hidpp.hidpp1.registers.connectionstate import SetConnectionStateRequest
from pyhid.hidpp.hidpp1.registers.connectionstate import SetConnectionStateResponse
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionRequest
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionResponse
from pyhid.hidpp.hidpp1.registers.performdevicediscovery import PerformDeviceDiscovery
from pylibrary.emulator.emulatorinterfaces import HOST
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.connectchunks import ConnectIdChunkData
from pylibrary.mcu.nrf52.blenvschunks import BleNvsChunks
from pylibrary.mcu.nrf52.blenvschunks import DeviceBleBondIdV1
from pylibrary.mcu.nrf52.blenvschunks import ReceiverBleBondId
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pylibrary.tools.nvsparser import NvsChunk
from pylibrary.tools.threadutils import QueueEmpty
from pyraspi.services.keyboardemulator import NUMBER_TO_KEYBOARD_KEY_ID_MAP
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pyusb.libusbdriver import ChannelIdentifier

# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------
LINK_NOT_ESTABLISHED = DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED
LINK_ESTABLISHED = DeviceConnection.LinkStatus.LINK_ESTABLISHED
ENTROPY_PER_MSE_USER_ACTION = 1
ENTROPY_PER_KBD_USER_ACTION = 4
ENTROPY_FULFILLED = 0


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DevicePairingTestUtils(CommonBaseTestUtils):
    """
    This class provides helpers for common checks on device pairing feature
    """
    # Timeout to connect to the device with the requested bluetooth address
    START_PAIRING_TIMEOUT = 5
    # Timeout to complete the whole pairing sequence
    PAIRING_TIMEOUT = 30
    # Timeout to reconnect to the paired receiver
    RECONNECTION_TIMEOUT = 5
    # Time margin
    TIMEOUT_MARGIN = 1
    # delay between 2 consecutive keystrokes in second
    KEYSTROKE_INTERVAL = 0.5
    # Host index providing the stable communication channel
    DEFAULT_HOST_INDEX = 1
    PAIRING_RETRY_NUMBER = 3
    # Maximum number of un-matching DeviceConnection message accepted after the successful pairing sequence
    MAX_WRONG_MESSAGE = 3

    @classmethod
    def set_authentication_method(cls, test_case, config_manager):
        """
        Set the requested authentication method

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param config_manager: Configuration Manager
        :type config_manager: ``ConfigurationManager``
        """
        if test_case.config_manager.get_feature(ConfigurationManager.ID.IS_PLATFORM):
            test_case.auth_method = SetPerformDeviceConnectionRequest.MASK.EMU_2BUTTONS_AUTH_METHOD
        elif config_manager.current_device_type == ConfigurationManager.DEVICE_TYPE.MOUSE:
            test_case.auth_method = SetPerformDeviceConnectionRequest.MASK.EMU_2BUTTONS_AUTH_METHOD
        else:
            test_case.auth_method = SetPerformDeviceConnectionRequest.MASK.PASSKEY_AUTH_METHOD
        # end if
    # end def set_authentication_method

    @classmethod
    def get_authentication_method(cls, test_case):
        """
        Retrieve the requested authentication method

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: Authentication method
        :rtype: ``int`` or ``None``
        """
        return test_case.auth_method if hasattr(test_case, 'auth_method') else None
    # end def get_authentication_method

    @classmethod
    def set_remaining_entropy(cls, test_case, auth_entropy):
        """
        Set the remaining authentication entropy in bits

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param auth_entropy: Authentication entropy value
        :type auth_entropy: ``int``
        """
        test_case.remaining_entropy = auth_entropy
    # end def set_remaining_entropy

    @classmethod
    def get_remaining_entropy(cls, test_case):
        """
        Retrieve the remaining authentication entropy in bits

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: Remaining authentication entropy value
        :rtype: ``int`` or ``None``
        """
        return test_case.remaining_entropy if hasattr(test_case, 'remaining_entropy') else None
    # end def get_remaining_entropy

    @classmethod
    def pair_device(cls, test_case, bluetooth_address, hid_dispatcher_to_dump=None, enable_retry=True):
        """
        Pair a device using its bluetooth address

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param bluetooth_address: The discovered device 6 bytes bluetooth address
        :type bluetooth_address: ``HexList``
        :param hid_dispatcher_to_dump: Current HID dispatcher to use to dump in the new channel HID
                                       dispatcher - OPTIONAL
        :type hid_dispatcher_to_dump: ``HIDDispatcher``
        :param enable_retry: Flag enabling the retry mechanism - OPTIONAL
        :type enable_retry: ``bool``

        :return: the pairing slot allocated by the receiver
        :rtype: ``int``
        """
        channel_receiver = ChannelUtils.get_receiver_channel(test_case=test_case)

        with ChannelUtils.channel_open_state(test_case=test_case):
            LogHelper.log_info(test_case=test_case, msg="Pair device")
            pairing_slot = None
            retry_count = cls.PAIRING_RETRY_NUMBER if enable_retry else 1
            while retry_count > 0:
                try:
                    # Empty connection event queue
                    ChannelUtils.clean_messages(
                        test_case=test_case, channel=channel_receiver,
                        queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection)
                    # Empty pairing status message queue
                    ChannelUtils.clean_messages(
                        test_case=test_case, channel=channel_receiver,
                        queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=PairingStatus)

                    LogHelper.log_info(
                        test_case=test_case,
                        msg="Send 'Perform device connection' request with Connect Devices = 1 (i.e. Pairing)")
                    cls.start_pairing_sequence(test_case, bluetooth_address)

                    LogHelper.log_info(test_case=test_case,msg="Wait for a start pairing status notification")
                    cls.PairingChecker.check_start_pairing_status(test_case)

                    LogHelper.log_info(test_case=test_case, msg="Wait for a display passkey notification")
                    passkey_digits = cls.PairingChecker.get_passkey_digits(test_case)

                    LogHelper.log_info(test_case=test_case, msg="Wait for a 'Digit Start' passkey notification")
                    cls.PairingChecker.get_display_passkey_start(test_case)

                    LogHelper.log_info(test_case=test_case,
                                       msg="Loop over passkey inputs list provided by the receiver")
                    cls.generate_keystrokes(test_case, passkey_digits)

                    LogHelper.log_info(test_case=test_case, msg="User enters the last passkey input")
                    cls.generate_end_of_sequence(test_case)

                    LogHelper.log_info(test_case=test_case, msg="Wait for a stop pairing status notification")
                    pairing_slot = cls.PairingChecker.check_stop_pairing_status(test_case)

                    LogHelper.log_info(test_case=test_case, msg="Wait for a device connection notification")
                    link_status = -1
                    # TODO: add device type in the settings to be able to check it
                    ble_pid = ''
                    expected_ble_pids = test_case.config_manager.get_feature(
                                ConfigurationManager.ID.DEVICES_BLUETOOTH_PIDS)
                    un_matching_connection_notification = -1
                    while (link_status != DeviceConnection.LinkStatus.LINK_ESTABLISHED or
                           ble_pid not in expected_ble_pids) and \
                            un_matching_connection_notification < cls.MAX_WRONG_MESSAGE:
                        device_connection = ChannelUtils.get_only(
                            test_case=test_case, channel=channel_receiver,
                            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection)

                        device_info_class = \
                            test_case.get_device_info_bit_field_structure_in_device_connection(device_connection)
                        device_info = device_info_class.fromHexList(HexList(device_connection.information))

                        if pairing_slot == device_connection.pairing_slot:
                            link_status = int(Numeral(device_info.device_info_link_status))
                            ble_pid = str(HexList(device_info.bluetooth_pid_msb) +
                                          HexList(device_info.bluetooth_pid_lsb))

                            test_case.assertEqual(
                                expected=DeviceConnection.LinkStatus.LINK_ESTABLISHED, obtained=link_status,
                                msg="The receiver should have sent a link established when the pairing sequence "
                                    "has passed")
                            test_case.assertIn(
                                member=ble_pid,
                                container=expected_ble_pids,
                                msg="The receiver should have sent the right BLE PID when the pairing sequence "
                                    "has passed")
                        # end if

                        un_matching_connection_notification += 1
                    # end while

                    assert (link_status == DeviceConnection.LinkStatus.LINK_ESTABLISHED and
                            ble_pid in expected_ble_pids), f"""Received too many wrong DeviceConnection messages 
                            {un_matching_connection_notification} after the pairing sequence has passed"""

                    pairing_slot = to_int(pairing_slot)

                    if DeviceManagerUtils.get_channel(
                            test_case=test_case,
                            channel_id=ChannelIdentifier(
                                port_index=ChannelUtils.get_port_index(test_case=test_case),
                                device_index=pairing_slot)) is None:
                        LogHelper.log_info(test_case=test_case, msg="Add new channel to cache")

                        channel = ThroughBleProReceiverChannel(
                            receiver_channel=channel_receiver, device_index=pairing_slot)

                        try:
                            channel.get_transport_id()
                            channel.is_device_connected()

                            if hid_dispatcher_to_dump is not None:
                                hid_dispatcher_to_dump.dump_mapping_in_other_dispatcher(
                                    other_dispatcher=channel.hid_dispatcher)
                            else:
                                root_version = test_case.config_manager.get_feature_version(
                                    test_case.f.PRODUCT.FEATURES.IMPORTANT.ROOT)
                                channel.hid_dispatcher.add_feature_entry(Root.FEATURE_INDEX, Root.FEATURE_ID,
                                                                         root_version)
                            # end if

                            DeviceManagerUtils.add_channel_to_cache(test_case=test_case, channel=channel)
                        except Exception:
                            # Delete the object ThroughReceiverChannel to prevent having multiple channel with the
                            # same device index in the receiver multiqueue created in the retry loop
                            del channel
                            raise
                        # end try
                    # end if

                    retry_count = 0
                except (AssertionError, AttributeError, QueueEmpty) as e:
                    if retry_count > 1:
                        retry_count -= 1
                        test_case.log_traceback_as_warning(
                            supplementary_message=f"Pairing failed: (counter = {retry_count})")

                        # noinspection PyBroadException
                        try:
                            LogHelper.log_info(
                                test_case=test_case, msg="Try to cancel pairing but do not block if it fails")
                            write_device_connect = SetPerformDeviceConnectionRequest(
                                connect_devices=SetPerformDeviceConnectionRequest.ConnectState.CANCEL_PAIRING)
                            write_device_connect_response = ChannelUtils.send(
                                test_case=test_case, channel=channel_receiver, report=write_device_connect,
                                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                                response_class_type=SetPerformDeviceConnectionResponse)

                            DevicePairingTestUtils.PerformDeviceConnectionResponseChecker.check_fields(
                                test_case=test_case, message=write_device_connect_response,
                                expected_cls=SetPerformDeviceConnectionResponse)
                            DevicePairingTestUtils.PairingChecker.check_cancel_pairing_status(test_case=test_case)
                        except Exception:
                            test_case.log_traceback_as_warning(
                                supplementary_message="Cancel pairing in exception failed")
                        # end try
                    else:
                        raise Exception(f"Pairing fails after {cls.PAIRING_RETRY_NUMBER} "
                                        f"try(ies): {e}").with_traceback(sys.exc_info()[2]) from None
                    # end if
                # end try
            # end while
        # end with

        assert pairing_slot is not None, "Could not pair but did not raise exception, this should not happen !"

        return pairing_slot
    # end def pair_device

    @classmethod
    def start_pairing_sequence(cls, test_case, bluetooth_address, log_check=False,
                               auth_entropy=SetPerformDeviceConnectionRequest.DEFAULT.ENTROPY_LENGTH_MAX):
        """
        Send a SetPerformDeviceConnectionRequest for pairing and check the acknowledgment.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param bluetooth_address: The discovered device 6 bytes bluetooth address
        :type bluetooth_address: ``HexList`` or ``int``
        :param log_check: Flag indicating if a log for the check should be added - OPTIONAL
        :type log_check: ``bool``
        :param auth_entropy: Authentication entropy length in bits - OPTIONAL
        :type auth_entropy: ``int``
        """
        channel_receiver = ChannelUtils.get_receiver_channel(test_case=test_case)

        with ChannelUtils.channel_open_state(test_case=test_case, channel=channel_receiver):
            LogHelper.log_info(test_case=test_case, msg="Start pairing sequence")
            auth_method = cls.get_authentication_method(test_case)
            LogHelper.log_info(
                test_case=test_case,
                msg="Send 'Perform device connection' request with Connect Devices = 1 (i.e. Pairing)")
            write_device_connect = SetPerformDeviceConnectionRequest(
                connect_devices=SetPerformDeviceConnectionRequest.ConnectState.PAIRING,
                bluetooth_address=bluetooth_address,
                emu_2buttons_auth_method=(auth_method ==
                                          SetPerformDeviceConnectionRequest.MASK.EMU_2BUTTONS_AUTH_METHOD),
                passkey_auth_method=(auth_method == SetPerformDeviceConnectionRequest.MASK.PASSKEY_AUTH_METHOD),
                auth_entropy=auth_entropy)
            write_device_connect_response = ChannelUtils.send(
                test_case=test_case, channel=channel_receiver, report=write_device_connect,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=SetPerformDeviceConnectionResponse)

            # Check the response to the Write command is success
            if log_check:
                # ---------------------------------------------------------------------------
                LogHelper.log_check(
                    test_case=test_case, text="Validate 'Perform device pairing and unpairing' response")
                # ---------------------------------------------------------------------------
            # end if
            cls.PerformDeviceConnectionResponseChecker.check_fields(
                test_case, write_device_connect_response, SetPerformDeviceConnectionResponse)
            DevicePairingTestUtils.set_remaining_entropy(test_case, auth_entropy)
        # end with
    # end def start_pairing_sequence

    @classmethod
    def generate_keystrokes(cls, test_case, passkey_digits, start=None, end=-1, log_check=False,
                            digit_to_ignore_display_key_check=None):
        """
        Emulate a series of keystrokes depending on a provided passkey digits

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param passkey_digits: sequence of 20 bits
        :type passkey_digits: ``int``
        :param start: first bit to consider in the keystroke sequence in [19..0] (default is 19) - OPTIONAL
        :type start: ``int``
        :param end: last bit to consider in the keystroke sequence in [18..-1] (default is -1) - OPTIONAL
        :type end: ``int``
        :param log_check: Flag indicating if a log for the check should be added - OPTIONAL
        :type log_check: ``bool``
        :param digit_to_ignore_display_key_check: The digit starts to ignore DisplayKey Key notification
                                                  checking - OPTIONAL
        :type digit_to_ignore_display_key_check: ``int``
        """
        auth_method = cls.get_authentication_method(test_case=test_case)
        assert auth_method is not None, "Cannot use this method if auth_method has not been set"

        LogHelper.log_info(test_case=test_case, msg="Generate keystrokes")
        start_max = None
        if auth_method == SetPerformDeviceConnectionRequest.MASK.EMU_2BUTTONS_AUTH_METHOD:
            start_max = RequestDisplayPassKey.BINARY_PASSKEY_IN_BITS - 1
        elif auth_method == SetPerformDeviceConnectionRequest.MASK.PASSKEY_AUTH_METHOD:
            start_max = RequestDisplayPassKey.PASSKEY_IN_DIGITS - 1
        # end if
        if start is None:
            start = start_max
        # end if
        assert (0 <= start <= start_max)
        assert (-1 <= end < start_max)
        assert (end < start)

        for index in range(start, end, -1):
            if auth_method == SetPerformDeviceConnectionRequest.MASK.EMU_2BUTTONS_AUTH_METHOD:
                bit_value = (passkey_digits >> index) & 0x01
                # User enters the next passkey input
                if bit_value == 1:
                    test_case.button_stimuli_emulator.keystroke(KEY_ID.RIGHT_BUTTON)
                else:
                    test_case.button_stimuli_emulator.keystroke(KEY_ID.LEFT_BUTTON)
                # end if
            elif auth_method == SetPerformDeviceConnectionRequest.MASK.PASSKEY_AUTH_METHOD:
                digit_value = (passkey_digits // (10**index)) % 10
                test_case.button_stimuli_emulator.keystroke(
                    key_id=NUMBER_TO_KEYBOARD_KEY_ID_MAP[digit_value])
            # end if

            if log_check:
                # ---------------------------------------------------------------------------
                LogHelper.log_check(test_case=test_case, text="Wait for a 'Digit In' passkey notification")
                # ---------------------------------------------------------------------------
            # end if
            if digit_to_ignore_display_key_check is None or index > digit_to_ignore_display_key_check:
                cls.PairingChecker.get_display_passkey_entry(test_case)
            # end if
            # Add a delay between 2 keystrokes
            sleep(cls.KEYSTROKE_INTERVAL)
        # end for
    # end def generate_keystrokes

    @classmethod
    def generate_end_of_sequence(cls, test_case, log_check=False, keypad_key=False):
        """
        Emulate the 'end of sequence' key combination.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param log_check: Flag indicating if a log for the check should be added - OPTIONAL
        :type log_check: ``bool``
        :param keypad_key: Flag to switch from keypad enter to keyboard return key - OPTIONAL
        :type keypad_key: ``bool``
        """
        auth_method = cls.get_authentication_method(test_case=test_case)
        assert auth_method is not None, "Cannot use this method if auth_method has not been set"

        LogHelper.log_info(test_case=test_case, msg="Generate end of sequence")
        # User enters the last passkey input
        if auth_method == SetPerformDeviceConnectionRequest.MASK.EMU_2BUTTONS_AUTH_METHOD:
            test_case.button_stimuli_emulator.simultaneous_keystroke([KEY_ID.RIGHT_BUTTON,
                                                                      KEY_ID.LEFT_BUTTON])
        elif auth_method == SetPerformDeviceConnectionRequest.MASK.PASSKEY_AUTH_METHOD:
            if keypad_key:
                test_case.button_stimuli_emulator.keystroke(KEY_ID.KEYPAD_ENTER)
            else:
                test_case.button_stimuli_emulator.keystroke(KEY_ID.KEYBOARD_RETURN_ENTER)
            # end if
        # end if

        if log_check > 0:
            # ---------------------------------------------------------------------------
            LogHelper.log_check(test_case=test_case, text="Wait for a 'Digit End' passkey notification")
            # ---------------------------------------------------------------------------
        # end if
        cls.PairingChecker.get_display_passkey_end(test_case)
    # end def generate_end_of_sequence

    @classmethod
    def press_delete_key(cls, test_case, key_name=None, ignore_erased_notification=False):
        """
        Emulate a keystroke on the 'del' or the 'backspace' key.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param key_name: The delete keys - OPTIONAL
        :type key_name: ``str``
        :param ignore_erased_notification: Flag indicating to skip the key erased notification check - OPTIONAL
        :type ignore_erased_notification: ``bool``
        """
        auth_method = cls.get_authentication_method(test_case=test_case)
        assert auth_method is not None, "Cannot use this method if auth_method has not been set"

        if not auth_method == SetPerformDeviceConnectionRequest.MASK.PASSKEY_AUTH_METHOD:
            return
        # end if

        LogHelper.log_info(test_case=test_case, msg="Press delete key")
        # User enters the last passkey input
        if key_name == 'del':
            test_case.button_stimuli_emulator.keystroke(
                key_id=KEY_ID.KEYBOARD_DELETE_FORWARD)
        elif key_name == 'backspace':
            test_case.button_stimuli_emulator.keystroke(
                key_id=KEY_ID.KEYBOARD_BACKSPACE)
        # end if

        if not ignore_erased_notification:
            # ---------------------------------------------------------------------------
            LogHelper.log_check(test_case=test_case, text="Wait for a 'Digit erased' passkey notification")
            # ---------------------------------------------------------------------------
            cls.PairingChecker.get_display_passkey_erased(test_case)
        # end if
    # end def press_delete_key

    @classmethod
    def generate_user_action(cls, test_case, key_id=None, is_hid_report_expected=False):
        """
        Emulate a user action on a key matching its key_id

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param key_id: Unique identifier of the key to emulate - OPTIONAL
        :type key_id: ``KEY_ID`` or ``int``
        :param is_hid_report_expected: Flag enabling the verification that we have successfully received an HID
                                       report - OPTIONAL
        :type is_hid_report_expected: ``bool``
        """
        auth_method = cls.get_authentication_method(test_case=test_case)
        assert auth_method is not None, "Cannot use this method if auth_method has not been set"
        channel_receiver = ChannelUtils.get_receiver_channel(test_case=test_case)

        with ChannelUtils.channel_open_state(test_case=test_case, channel=channel_receiver):
            LogHelper.log_info(test_case=test_case, msg="Generate user action")
            sleep(.5)  # wait awhile to make sure button break packet has been collected in queue.
            ChannelUtils.clean_messages(
                test_case=test_case, channel=channel_receiver, queue_name=HIDDispatcher.QueueName.HID,
                class_type=(HidMouse, HidKeyboard, HidKeyboardBitmap, HidConsumer))
            if key_id is not None:
                test_case.button_stimuli_emulator.keystroke(key_id=key_id)
            else:
                test_case.button_stimuli_emulator.user_action()
            # end if

            if is_hid_report_expected:
                if auth_method == SetPerformDeviceConnectionRequest.MASK.EMU_2BUTTONS_AUTH_METHOD:
                    hid_mouse = ChannelUtils.get_only(test_case=test_case, channel=channel_receiver,
                                                      queue_name=HIDDispatcher.QueueName.HID, class_type=HidMouse)
                    test_case.assertNotNone(obtained=hid_mouse, msg='HID mouse message should be received')
                    if int(Numeral(hid_mouse.Button1)) == 0:
                        # Fetch next HID report
                        hid_mouse = ChannelUtils.get_only(test_case=test_case, channel=channel_receiver,
                                                          queue_name=HIDDispatcher.QueueName.HID, class_type=HidMouse)
                        test_case.assertNotNone(obtained=hid_mouse, msg='HID mouse message should be received')
                    # end if
                    test_case.assertEqual(obtained=int(Numeral(hid_mouse.Button1)), expected=1,
                                          msg='Button 1 should be set')

                    hid_mouse = ChannelUtils.get_only(test_case=test_case, channel=channel_receiver,
                                                      queue_name=HIDDispatcher.QueueName.HID, class_type=HidMouse)
                    test_case.assertNotNone(obtained=hid_mouse, msg='HID mouse message should be received')
                    test_case.assertEqual(obtained=int(Numeral(hid_mouse.Button1)), expected=0,
                                          msg='Button 1 should be released')
                elif auth_method == SetPerformDeviceConnectionRequest.MASK.PASSKEY_AUTH_METHOD:
                    hid_keyboard = ChannelUtils.get_only(test_case=test_case, channel=channel_receiver,
                                                         queue_name=HIDDispatcher.QueueName.HID)
                    test_case.assertNotNone(obtained=hid_keyboard, msg='HID Keyboard message should have been received')
                    if isinstance(hid_keyboard, HidKeyboard):
                        test_case.assertEqual(obtained=int(Numeral(hid_keyboard.KEY_CODE1)),
                                              expected=KEYBOARD_HID_USAGE.KEYPAD_ENTER, msg='KEY_CODE1 should be set')

                        hid_keyboard = ChannelUtils.get_only(test_case=test_case, channel=channel_receiver,
                                                             queue_name=HIDDispatcher.QueueName.HID,
                                                             class_type=HidKeyboard)
                        test_case.assertNotNone(obtained=hid_keyboard,
                                                msg='HID Keyboard message should have been received')
                        test_case.assertEqual(obtained=int(Numeral(hid_keyboard.KEY_CODE1)), expected=0,
                                              msg='KEY_CODE1 should be released')
                    elif isinstance(hid_keyboard, HidKeyboardBitmap):
                        test_case.assertEqual(obtained=hid_keyboard.keypad_enter,
                                              expected=1, msg='KP_ENTER should be set')

                        hid_keyboard = ChannelUtils.get_only(
                            test_case=test_case, channel=channel_receiver,
                            queue_name=HIDDispatcher.QueueName.HID, class_type=HidKeyboardBitmap)
                        test_case.assertNotNone(obtained=hid_keyboard,
                                                msg='HID Keyboard Bitmap message should have been received')
                        test_case.assertEqual(obtained=hid_keyboard.keypad_enter, expected=0,
                                              msg='KP_ENTER should be released')
                    # end if
                # end if
            # end if
        # end with
    # end def generate_user_action

    @classmethod
    def multiple_pairing(cls, test_case, number_of_pairing=None):
        """
        Pair device on multiple pairing slots

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param number_of_pairing: Number of pairing to perform, if ``None`` it will pair all possible slots - OPTIONAL
        :type number_of_pairing: ``int`` or ``None``
        """
        channel_receiver = ChannelUtils.get_receiver_channel(test_case=test_case)

        with ChannelUtils.channel_open_state(test_case=test_case, channel=channel_receiver):
            if number_of_pairing is None:
                number_of_pairing = test_case.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots
            elif number_of_pairing > test_case.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots:
                raise ValueError(
                    f'Too many pairing requested: {test_case.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots} pairing '
                    f'slots available')
            # end if

            LogHelper.log_info(test_case=test_case, msg="Multiple pairing")

            current_pairing_slot = None
            for _ in range(number_of_pairing):
                bluetooth_address = DiscoveryTestUtils.discover_device(test_case)

                if current_pairing_slot is not None:
                    # Previous connection is lost when starting the new sequence
                    device_connection = ChannelUtils.get_only(
                        test_case=test_case, channel=channel_receiver,
                        queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection)

                    device_info_class = test_case.get_device_info_bit_field_structure_in_device_connection(
                        device_connection)
                    device_info = device_info_class.fromHexList(HexList(device_connection.information))
                    assert (int(Numeral(device_info.device_info_link_status)) ==
                            DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED)
                # end if

                pairing_slot = cls.pair_device(test_case, bluetooth_address)
                if pairing_slot == number_of_pairing:
                    break
                else:
                    current_pairing_slot = pairing_slot
                # end if
            # end for
        # end with
    # end def multiple_pairing

    @classmethod
    def pair_all_slots(cls, test_case):
        """
        Pair device until all slots are used

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        """
        channel_receiver = ChannelUtils.get_receiver_channel(test_case=test_case)

        with ChannelUtils.channel_open_state(test_case=test_case, channel=channel_receiver):
            LogHelper.log_info(test_case=test_case, msg="Pair all slots")
            try:
                cls.multiple_pairing(test_case)
            except (AssertionError, QueueEmpty):
                error_message = ChannelUtils.get_only(
                    test_case=test_case, channel=channel_receiver,
                    queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR, class_type=Hidpp1ErrorCodes)
                test_case.assertEqual(obtained=int(Numeral(error_message.errorCode)),
                                      expected=Hidpp1ErrorCodes.ERR_TOO_MANY_DEVICES,
                                      msg="When all pairing slots are used, the PerformDevicePairing.Pairing is "
                                          "rejected (ERR_TOO_MANY_DEVICES)")
                test_case.button_stimuli_emulator.change_host()
            finally:
                ChannelUtils.clean_messages(
                    test_case=test_case, channel=channel_receiver,
                    queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=(DiscoveryStatus, DeviceDiscovery))
            # end try
        # end with
    # end def pair_all_slots

    @classmethod
    def pair_all_available_hosts(cls, test_case, number_of_host=None):
        """
        Perform BLE Pro discovery and pairing sequences with all available hosts, except the host 1.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param number_of_host: number of hosts on which to perform a pairing - OPTIONAL
        :type number_of_host: ``int | None``
        """
        if number_of_host is None:
            number_of_host = test_case.f.PRODUCT.DEVICE.F_NbHosts
            assert number_of_host > 0, "The number of host shall not be null. Check F_NbHosts value in settings file"
        # end if
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case, "Clean-up receiver pairing slots")
        # --------------------------------------------------------------------------------------------------------------
        cls.unpair_all(test_case)

        if test_case.last_ble_address is None and test_case.device_debugger is not None:
            # Retrieve the last BLE address in the DUT NVS to correctly filter Device Discovery notifications
            test_case.device_memory_manager.read_nvs()
            test_case.last_ble_address = DeviceBaseTestUtils.NvsHelper.get_last_gap_address(
                test_case=test_case, memory_manager=test_case.device_memory_manager)
        # end if

        # Initialize the authentication method parameter
        DevicePairingTestUtils.set_authentication_method(test_case, test_case.config_manager)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case, "Test Loop over host in all available hosts")
        # --------------------------------------------------------------------------------------------------------------
        for host_index in range(number_of_host - 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, f'Force the device in pairing mode with a long press on '
                                          f'the Host{host_index + 2} Easy switch button')
            # ----------------------------------------------------------------------------------------------------------
            if test_case.f.PRODUCT.DEVICE.CONNECTION_SCHEME.F_MultipleEasySwitchButtons:
                test_case.button_stimuli_emulator.enter_pairing_mode(host_index=host_index + 2)
            else:
                test_case.button_stimuli_emulator.change_host(host_index=host_index + 2)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, 'Start the discovery sequence')
            # ----------------------------------------------------------------------------------------------------------
            bluetooth_address = DiscoveryTestUtils.discover_device(test_case, trigger_user_action=False)
            ChannelUtils.clean_messages(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                class_type=DeviceConnection,
                channel=test_case.current_channel)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, "Start the pairing sequence")
            # ----------------------------------------------------------------------------------------------------------
            pairing_slot = cls.pair_device(test_case, bluetooth_address)
            test_case.current_channel = \
                DeviceManagerUtils.get_channel(test_case=test_case,
                                               channel_id=ChannelIdentifier(
                                                   port_index=ChannelUtils.get_port_index(test_case=test_case),
                                                   device_index=pairing_slot))
            ChannelUtils.open_channel(test_case=test_case)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(test_case, "Verify an HID report can be received")
            # ----------------------------------------------------------------------------------------------------------
            DeviceBaseTestUtils.ButtonHelper.check_user_action(test_case)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
    # end def pair_all_available_hosts

    @staticmethod
    def pair_device_slot_to_other_receiver(
            test_case, device_slot, other_receiver_port_index, hid_dispatcher_to_dump=None):
        """
        pair a device slot to a receiver

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param device_slot: Host index to activate
        :type device_slot: ``int``
        :param other_receiver_port_index: Port index of the receiver to use
        :type other_receiver_port_index: ``int``
        :param hid_dispatcher_to_dump: Current HID dispatcher to use to dump in the new channel HID
                                       dispatcher - OPTIONAL
        :type hid_dispatcher_to_dump: ``HIDDispatcher``
        """
        DeviceBaseTestUtils.NvsHelper.change_host(test_case, test_case.memory_manager, device_slot,
                                                  ConnectIdChunkData.PairingSrc.NONE)
        if test_case.last_ble_address is None:
            # Retrieve the last BLE address in the DUT NVS to correctly filter Device Discovery notifications
            test_case.last_ble_address = DeviceBaseTestUtils.NvsHelper.get_last_gap_address(
                test_case=test_case, memory_manager=test_case.device_memory_manager)
        # end if

        # ---------------------------------------------------------------------------
        LogHelper.log_step(test_case, 'Start Discovery on spy receiver')
        # ---------------------------------------------------------------------------
        ReceiverTestUtils.switch_to_receiver(test_case, other_receiver_port_index)
        test_case.enable_hidpp_reporting()

        # ---------------------------------------------------------------------------
        LogHelper.log_step(test_case, 'Unpair all the slots')
        # ---------------------------------------------------------------------------
        DevicePairingTestUtils.unpair_all(test_case, first_slot=1)

        DiscoveryTestUtils.start_discovery(test_case, PerformDeviceDiscovery.DiscoveryTimeout.USE_DEFAULT)

        test_case.clean_message_type_in_queue(test_case.hidDispatcher.receiver_connection_event_queue, DeviceConnection)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(test_case, 'Check Device Discovery notifications are received while DUT is discoverable')
        # ---------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            test_case, PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE)
        test_case.assertNotNone(
            device_discovery, 'Device Discovery Notifications should be received while DUT is discoverable')

        DiscoveryTestUtils.cancel_discovery(test_case)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(test_case, 'Pair device with second receiver')
        # ---------------------------------------------------------------------------
        # noinspection PyUnresolvedReferences
        # bluetooth_address is part of the data in device discovery notification part 0
        device_index = DevicePairingTestUtils.pair_device(
            test_case=test_case,
            bluetooth_address=device_discovery[DeviceDiscovery.PART.CONFIGURATION].data.bluetooth_address,
            hid_dispatcher_to_dump=hid_dispatcher_to_dump)

        DevicePairingTestUtils.check_connection_status(
            test_case, device_index, DeviceConnection.LinkStatus.LINK_ESTABLISHED)

        # Fetch Device USB Descriptors matching the spy receiver interfaces configuration
        ChannelUtils.get_descriptors(test_case=test_case)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(test_case, 'Check User action -> Button')
        # ---------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(test_case)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(test_case, 'Check Connect Id chunk in NVS')
        # ---------------------------------------------------------------------------
        test_case.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            test_case, test_case.memory_manager, device_slot, ConnectIdChunkData.PairingSrc.USR)
    # end def pair_device_slot_to_other_receiver

    @classmethod
    def pair_all_hosts_to_receivers(cls, test_case):
        """
        Pair all hosts on DUT to the receivers one by one except the current host and back to the original host in
        the end

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case, 'Pair all hosts on DUT to the receivers one by one')
        # --------------------------------------------------------------------------------------------------------------
        test_case.post_requisite_clean_pairing_info_on_receivers = True

        # Cleanup all pairing slots except the first one
        CommonBaseTestUtils.NvsHelper.clean_pairing_data(test_case)

        # Initialize the authentication method parameter
        DevicePairingTestUtils.set_authentication_method(test_case, test_case.config_manager)

        ble_pro_receiver_port_indexes = ReceiverTestUtils.get_receiver_port_indexes(
            test_case,
            ReceiverTestUtils.USB_PID_MEZZY_BLE_PRO,
            skip=[ChannelUtils.get_port_index(test_case)])
        assert len(ble_pro_receiver_port_indexes) > 0, \
            "Cannot perform multi receiver tests if not enough receivers"

        device_slot = 1
        dispatcher_to_dump = test_case.current_channel.hid_dispatcher
        for index in ble_pro_receiver_port_indexes:
            DevicePairingTestUtils.pair_device_slot_to_other_receiver(
                test_case,
                device_slot=device_slot,
                other_receiver_port_index=index,
                hid_dispatcher_to_dump=dispatcher_to_dump)
            device_slot += 1
        # end for

        # Reconnect with the first receiver
        ReceiverTestUtils.switch_to_receiver(
            test_case, receiver_port_index=ChannelUtils.get_port_index(test_case, channel=test_case.backup_dut_channel))

        # Change host on Device
        DevicePairingTestUtils.change_host_by_link_state(
            test_case, link_state=DeviceConnection.LinkStatus.LINK_ESTABLISHED)

        DeviceManagerUtils.set_channel(test_case, new_channel=test_case.backup_dut_channel)
    # end def pair_all_hosts_to_receivers

    @classmethod
    def unpair_all(cls, test_case, first_slot=2):
        """
        Unpair all pairing slots except the first one which is preserved

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param first_slot: First pairing slot to unpair (default is 2 to preserve the first to connect to the
                           DUT) - OPTIONAL
        :type first_slot: ``int``
        """
        channel_receiver = ChannelUtils.get_receiver_channel(test_case=test_case)

        with ChannelUtils.channel_open_state(test_case=test_case, channel=channel_receiver):
            LogHelper.log_info(test_case=test_case, msg="Unpair all")
            for pairing_slot in range(first_slot, test_case.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots + 1):
                cls.unpair_slot(test_case, pairing_slot, ignore_notification=True)
            # end for
            ChannelUtils.empty_queue(test_case=test_case, channel=channel_receiver,
                                     queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT)
        # end with
    # end def unpair_all

    @classmethod
    def unpair_slot(cls, test_case, pairing_slot, ignore_notification=False):
        """
        Unpair a pairing slot

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param pairing_slot: Slot to unpair
        :type pairing_slot: ``int``
        :param ignore_notification: Skip DeviceDisconnection verification from queue - OPTIONAL
        :type ignore_notification: ``bool``
        """
        assert pairing_slot in range(1, test_case.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots + 1), \
            f"{pairing_slot} is not a valid pairing slot. It should be in the range " \
            f"[1 .. {test_case.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots}]"
        channel_receiver = ChannelUtils.get_receiver_channel(test_case=test_case)

        with ChannelUtils.channel_open_state(test_case=test_case, channel=channel_receiver):
            LogHelper.log_info(test_case=test_case, msg="Unpair slot")
            write_device_connect = SetPerformDeviceConnectionRequest(
                connect_devices=SetPerformDeviceConnectionRequest.ConnectState.UNPAIRING,
                pairing_slot_to_be_unpaired=pairing_slot)

            ChannelUtils.send_only(
                test_case=test_case, channel=channel_receiver, report=write_device_connect, timeout=1)
            message = None
            # Loop for 4 seconds
            remaining_time = 4
            end_time = time() + remaining_time
            while remaining_time > 0 and message is None:
                message = ChannelUtils.get_only(
                    test_case=test_case, channel=channel_receiver, queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                    class_type=SetPerformDeviceConnectionResponse, timeout=.1, check_first_message=False,
                    allow_no_message=True, skip_error_message=True)
                if message is None:
                    # When the pairing slot to be unpaired is empty,
                    # the PerformDevicePairing.Unpairing is rejected (ERR_UNKNOWN_DEVICE)
                    message = ChannelUtils.get_only(
                        test_case=test_case, channel=channel_receiver,
                        queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR, timeout=.1, allow_no_message=True)
                # end if
                remaining_time = end_time - time()
            # end while

            # TODO, Is it normal that we do not do anything if no message was received ?

            if not ignore_notification and message is not None and not isinstance(message, Hidpp1ErrorCodes):
                # Process optional link not established notification
                cls.check_link_not_established_notification(test_case, pairing_slot)
                # Previous connection is lost when unpairing
                cls.check_device_disconnection_notification(
                    test_case, pairing_slot, DeviceDisconnection.PERMANENT_DISCONNECTION)
            # end if

            if test_case.device is not None:
                DeviceManagerUtils.remove_channel_from_cache(
                    test_case=test_case,
                    port_index=ChannelUtils.get_port_index(test_case=test_case),
                    device_index=pairing_slot)
            # end if
        # end with
    # end def unpair_slot

    @classmethod
    def cancel_pairing(cls, test_case, log_check=False):
        """
        Cancel an ongoing pairing sequence

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param log_check: Flag indicating if a log for the check should be added - OPTIONAL
        :type log_check: ``bool``
        """
        channel_receiver = ChannelUtils.get_receiver_channel(test_case=test_case)

        with ChannelUtils.channel_open_state(test_case=test_case, channel=channel_receiver):
            LogHelper.log_info(test_case=test_case, msg="Cancel pairing")
            # Send 'Perform device connection' request with Connect Devices = Cancel Pairing
            write_device_connect = SetPerformDeviceConnectionRequest(
                connect_devices=SetPerformDeviceConnectionRequest.ConnectState.CANCEL_PAIRING)
            write_device_connect_response = ChannelUtils.send(
                test_case=test_case, channel=channel_receiver, report=write_device_connect,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=SetPerformDeviceConnectionResponse)

            if log_check:
                # ---------------------------------------------------------------------------
                LogHelper.log_check(test_case=test_case, text="Check the response to the Write command is success")
                # ---------------------------------------------------------------------------
            # end if
            cls.PerformDeviceConnectionResponseChecker.check_fields(
                test_case, write_device_connect_response, SetPerformDeviceConnectionResponse)

            if log_check:
                # ---------------------------------------------------------------------------
                LogHelper.log_check(test_case=test_case, text="Wait for a cancel pairing status notification")
                # ---------------------------------------------------------------------------
            # end if
            cls.PairingChecker.check_cancel_pairing_status(test_case)
        # end with
    # end def cancel_pairing

    @staticmethod
    def check_connection_status(test_case, pairing_slot, expected_connection_status, log_step=False, log_check=False):
        """
        Check the connection status for a pairing slot

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param pairing_slot: Pairing slot to check
        :type pairing_slot: ``int``
        :param expected_connection_status: The expected connection status
        :type expected_connection_status: ``DeviceConnection.LinkStatus``
        :param log_step: Flag indicating if a log for the step should be added - OPTIONAL
        :type log_step: ``bool``
        :param log_check: Flag indicating if a log for the check should be added - OPTIONAL
        :type log_check: ``bool``
        """
        channel_receiver = ChannelUtils.get_receiver_channel(test_case=test_case)

        with ChannelUtils.channel_open_state(test_case=test_case, channel=channel_receiver):
            LogHelper.log_info(test_case=test_case, msg="Check connection status")

            if log_step:
                # ---------------------------------------------------------------------------
                LogHelper.log_step(test_case=test_case, text="Send Connection State")
                # ---------------------------------------------------------------------------
            # end if

            ChannelUtils.clean_messages(test_case=test_case, channel=channel_receiver,
                                        queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                        class_type=DeviceConnection)

            connection_state_req = SetConnectionStateRequest(write_action_on_connection_fake_device_arrival=1)
            ChannelUtils.send(test_case=test_case, channel=channel_receiver, report=connection_state_req,
                              response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                              response_class_type=SetConnectionStateResponse)
            device_connections = ChannelUtils.clean_messages(
                test_case=test_case, channel=channel_receiver,
                queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection)

            if log_check:
                extra_str = " not " if expected_connection_status == DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED \
                    else " "
                # ---------------------------------------------------------------------------
                LogHelper.log_check(
                    test_case=test_case, text=f"Check link is{extra_str}established on pairing slot {pairing_slot}")
                # ---------------------------------------------------------------------------
            # end if

            pairing_slot_found = False
            expected_status_found = False
            status = None
            for device_connection in device_connections:
                if to_int(device_connection.pairing_slot) == pairing_slot:
                    pairing_slot_found = True
                    device_info_class = test_case.get_device_info_bit_field_structure_in_device_connection(
                        device_connection)
                    status = to_int(device_info_class.fromHexList(HexList(
                        device_connection.information)).device_info_link_status)
                    if expected_connection_status == status:
                        expected_status_found = True
                    else:
                        expected_status_found = False
                    # end if
                # end if
            # end for

            if pairing_slot_found:
                through_receiver_channel = DeviceManagerUtils.get_channel(
                    test_case=test_case, channel_id=ChannelIdentifier(
                        port_index=ChannelUtils.get_port_index(test_case=test_case), device_index=pairing_slot))
                if through_receiver_channel is not None:
                    # Update the associated channel's connection state
                    through_receiver_channel.connected = (status == DeviceConnection.LinkStatus.LINK_ESTABLISHED)
                # end if
            # end if

            test_case.assertTrue(
                expr=expected_status_found,
                msg=f'Device Connection with link status = {expected_connection_status} should be received '
                    f'for pairing slot {pairing_slot}')
        # end with
    # end def check_connection_status

    @staticmethod
    def check_link_not_established_notification(test_case, expected_pairing_slot):
        """
        Check optional link not established notification

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param expected_pairing_slot: Expected pairing slot
        :type expected_pairing_slot: ``int``
        """
        channel_receiver = ChannelUtils.get_receiver_channel(test_case=test_case)

        with ChannelUtils.channel_open_state(test_case=test_case, channel=channel_receiver):
            LogHelper.log_info(test_case=test_case, msg="Get optional link not estabished notification")
            device_connection = ChannelUtils.get_only(test_case=test_case, channel=channel_receiver,
                                                      queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                                      class_type=DeviceConnection, check_first_message=False,
                                                      allow_no_message=True)
            if device_connection is not None:
                test_case.assertEqual(obtained=int(Numeral(device_connection.pairing_slot)),
                                      expected=expected_pairing_slot,
                                      msg="Wrong pairing_slot parameter received in device disconnection notification")
                device_info_class = test_case.get_device_info_bit_field_structure_in_device_connection(
                    device_connection)
                device_info = device_info_class.fromHexList(HexList(device_connection.information))
                assert (int(Numeral(device_info.device_info_link_status)) ==
                        DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED)
            # end if
        # end with
    # end def check_link_not_established_notification

    @staticmethod
    def check_device_disconnection_notification(test_case, expected_pairing_slot, expected_disconnection_type):
        """
        Check pairing slot and disconnection type in device disconnection notification

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param expected_pairing_slot: Expected pairing slot
        :type expected_pairing_slot: ``int``
        :param expected_disconnection_type: Expected disconnection type
        :type expected_disconnection_type: ``int``
        """
        channel_receiver = ChannelUtils.get_receiver_channel(test_case=test_case)

        with ChannelUtils.channel_open_state(test_case=test_case, channel=channel_receiver):
            LogHelper.log_info(test_case=test_case, msg="Check device disconnection notification")
            device_disconnection = ChannelUtils.get_only(test_case=test_case, channel=channel_receiver,
                                                         queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                                         class_type=DeviceDisconnection, check_first_message=False)
            test_case.assertEqual(
                obtained=int(Numeral(device_disconnection.disconnection_type)), expected=expected_disconnection_type,
                msg="Wrong disconnection_type parameter received in device disconnection notification")
            test_case.assertEqual(obtained=int(Numeral(device_disconnection.pairing_slot)),
                                  expected=expected_pairing_slot,
                                  msg="Wrong pairing_slot parameter received in device disconnection notification")
        # end with
    # end def check_device_disconnection_notification

    @staticmethod
    def change_host_by_link_state(test_case, link_state=LINK_ESTABLISHED, clean_device_connection_event=True):
        """
        Using the easy switch button, change host until the requested link state is achieved.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param link_state: targeted link state (Established or not) - OPTIONAL
        :type link_state: ``int``
        :param clean_device_connection_event: Flag indicating to clean device connection event - OPTIONAL
        :type clean_device_connection_event: ``bool``
        """
        if ((test_case.config_manager.get_feature(ConfigurationManager.ID.IS_PLATFORM) or
             test_case.config_manager.current_device_type == ConfigurationManager.DEVICE_TYPE.MOUSE) and
                test_case.f.PRODUCT.DEVICE.F_NbHosts > 1):
            DevicePairingTestUtils._mouse_change_host_by_link_state(test_case, link_state)
        elif (test_case.config_manager.current_device_type == ConfigurationManager.DEVICE_TYPE.KEYBOARD or
              test_case.f.PRODUCT.DEVICE.F_NbHosts == 1):
            DevicePairingTestUtils._kbd_change_host_by_link_state(test_case, link_state, clean_device_connection_event)
        else:
            raise ValueError(f'unknown current device type! {test_case.config_manager.current_device_type}')
        # end if
    # end def change_host_by_link_state

    @staticmethod
    def _kbd_change_host_by_link_state(test_case, link_state=LINK_ESTABLISHED, clean_device_connection_event=True):
        """
        Mimic EasySwitch behavior on keyboard to have the same control interface with mouse

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param link_state: targeted link state (Established or not) - OPTIONAL
        :type link_state: ``int``
        :param clean_device_connection_event: Flag indicating to clean device connection event - OPTIONAL
        :type clean_device_connection_event: ``bool``
        """
        channel_receiver = ChannelUtils.get_receiver_channel(test_case=test_case)

        with ChannelUtils.channel_open_state(test_case=test_case, channel=channel_receiver):
            LogHelper.log_info(test_case=test_case, msg="Change keyboard host by link state")
            if link_state == LINK_NOT_ESTABLISHED:
                if test_case.f.PRODUCT.DEVICE.F_NbHosts == 1:
                    test_case.button_stimuli_emulator.enter_pairing_mode(host_index=1)
                else:
                    # Keyboard disallowed jump to a host that had not been paired before.
                    test_case.button_stimuli_emulator.enter_pairing_mode(host_index=2)
                # end if
            elif link_state == LINK_ESTABLISHED:
                test_case.button_stimuli_emulator.change_host(host_index=1)
            # end if

            if clean_device_connection_event:
                ChannelUtils.clean_messages(test_case=test_case, channel=channel_receiver,
                                            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                            class_type=DeviceConnection)
                # Clean-up Wireless Device Status notification related to the change host
                ChannelUtils.clean_messages(test_case=test_case, queue_name=HIDDispatcher.QueueName.EVENT,
                                            class_type=WirelessDeviceStatusBroadcastEvent)
            # end if
        # end with
    # end def _kbd_change_host_by_link_state

    @staticmethod
    def _mouse_change_host_by_link_state(test_case, link_state=LINK_ESTABLISHED):
        """
        Using the easy switch button, change host until the requested link state is achieved.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param link_state: targeted link state (Established or not) - OPTIONAL
        :type link_state: ``int``

        :return: Flag indicating if the link matches the requested state
        :rtype: ``bool``
        """
        state_flag = False
        channel_receiver = ChannelUtils.get_receiver_channel(test_case=test_case)

        with ChannelUtils.channel_open_state(test_case=test_case, channel=channel_receiver):
            LogHelper.log_info(test_case=test_case, msg="Change mouse host by link state")
            # Clean-up receiver connection event queue
            ChannelUtils.empty_queue(test_case=test_case, channel=channel_receiver,
                                     queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT)

            # Wake-up the device
            if test_case.button_stimuli_emulator is not None:
                test_case.button_stimuli_emulator.user_action()
            # end if

            for click_count in range(5):
                if test_case.button_stimuli_emulator is not None:
                    test_case.button_stimuli_emulator.change_host()
                # end if

                state_flag = ChannelUtils.wait_through_receiver_channel_link_status(
                    test_case=test_case, channel=channel_receiver, link_status=link_state,
                    device_index=DevicePairingTestUtils.DEFAULT_HOST_INDEX, allow_no_message=True)

                if test_case.button_stimuli_emulator is not None:
                    # Clean-up HID Mouse reports related to the user action
                    ChannelUtils.empty_queue(test_case=test_case, queue_name=HIDDispatcher.QueueName.HID)
                    # Clean-up Wireless Device Status notification related to the change host
                    ChannelUtils.clean_messages(test_case=test_case,
                                                queue_name=HIDDispatcher.QueueName.EVENT,
                                                class_type=WirelessDeviceStatusBroadcastEvent)
                # end if

                if state_flag:
                    return state_flag
                # end if
            # end for

            if not state_flag:
                raise ValueError("Short press on easy switch button do not issue DeviceConnection notification")
            # end if
        # end with
    # end def _mouse_change_host_by_link_state

    @classmethod
    def pair_device_to_host(cls, test_case, host=HOST.CH1 - 1):
        """
        Pair the device at the given host index and open channel

        :param test_case: Current test case
        :type test_case: ``BaseTestCase``
        :param host: The host index to pair the device to - OPTIONAL
        :type host: ``int``
        """
        DevicePairingTestUtils.set_authentication_method(test_case, test_case.config_manager)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case, 'Start the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        # Clean discovery notifications
        test_case.clean_message_type_in_queue(test_case.hidDispatcher.receiver_event_queue, (DeviceDiscovery,
                                                                                             DiscoveryStatus))

        DeviceBaseTestUtils.NvsHelper.change_host(test_case=test_case, host_index=host,
                                                  memory_manager=test_case.memory_manager)
        if test_case.last_ble_address is None:
            # Retrieve the last BLE address in the DUT NVS to correctly filter Device Discovery notifications
            test_case.last_ble_address = DeviceBaseTestUtils.NvsHelper.get_last_gap_address(
                test_case=test_case, memory_manager=test_case.device_memory_manager)
        # end if

        test_case.button_stimuli_emulator.enter_pairing_mode(host_index=host + 1)

        DiscoveryTestUtils.start_discovery(test_case)

        DiscoveryTestUtils.check_status_notification(
            test_case, DiscoveryStatus.DeviceDiscoveryStatus.START, DiscoveryStatus.ErrorType.NO_ERROR)

        test_case.clean_message_type_in_queue(test_case.hidDispatcher.receiver_event_queue, (DeviceRecovery,
                                                                                             DeviceDiscovery))

        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            test_case, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

        test_case.assertNotNone(device_discovery,
                                "device discovery should always be received")
        test_case.assertNotNone(device_discovery[DeviceDiscovery.PART.CONFIGURATION],
                                "Part 0 (configuration) should always be received")
        test_case.assertNotNone(device_discovery[DeviceDiscovery.PART.NAME_1],
                                "Part 1 (Device name first part) should always be received")

        DiscoveryTestUtils.DeviceDiscoveryNotificationChecker.DataChecker.check_protocol_type(
            test_case,
            device_discovery[DeviceDiscovery.PART.CONFIGURATION].data,
            DeviceDiscovery.DeviceDiscoveryPart0.BLE_PRO_PROTOCOL_TYPE)

        test_case.clean_message_type_in_queue(test_case.hidDispatcher.receiver_event_queue, DeviceDiscovery)

        bluetooth_address = device_discovery[DeviceDiscovery.PART.CONFIGURATION].data.bluetooth_address

        # Clean DeviceConnection to avoid errors in next call to verify_recovery_disconnection due to
        # previous events
        ChannelUtils.clean_messages(
            test_case=test_case,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=DeviceConnection,
            channel=test_case.current_channel)

        pairing_slot = DevicePairingTestUtils.pair_device(test_case, bluetooth_address)

        DeviceManagerUtils.set_channel(
            test_case=test_case,
            new_channel_id=ChannelIdentifier(
                port_index=ChannelUtils.get_port_index(test_case=test_case), device_index=pairing_slot),
            open_channel=True)
    # end def pair_device_to_host

    class NvsManager:
        """
        Non-Volatile Memory Manager class
        """
        RECEIVER_PAIRING_SLOT_COUNT = 6

        @classmethod
        def get_pairing_data(cls, test_case):
            """
            Parse NVS content from device and receiver memories to extract pairing information.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: List of tuple (slot, bluetooth address (LSB))
            :rtype: ``list[tuple]``
            """
            pairing_data = []
            for memory_manager in [test_case.device_memory_manager, test_case.receiver_memory_manager]:
                if memory_manager is not None:
                    memory_manager.read_nvs()
                    pairing_data.append(memory_manager.get_bluetooth_addresses())
                # end if
            # end for
            return pairing_data
        # end def get_pairing_data

        @classmethod
        def get_device_pairing_data_history(cls, test_case):
            """
            Get the device pairing data history from its NVS.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: The pairing chunk history for all pairing slots of the device
            :rtype: ``list[list[NvsChunk|BitFieldContainerMixin]]``
            """
            if test_case.memory_manager.nvs_parser is not None:
                nvs_parser = test_case.memory_manager.nvs_parser
            else:
                nvs_parser = test_case.get_dut_nvs_parser()
            # end if
            nvs_ble_bond_ids = []
            # Loop over the possible pairing slots
            for pairing_slot in range(DevicePairingTestUtils.NvsManager.RECEIVER_PAIRING_SLOT_COUNT):
                ble_bond_id = f'NVS_BLE_BOND_ID_{pairing_slot}'
                ble_bond_id_chunk = nvs_parser.get_chunk_history(ble_bond_id)
                nvs_ble_bond_ids.append(ble_bond_id_chunk)
            # end for

            return nvs_ble_bond_ids
        # end def get_device_pairing_data_history

        @classmethod
        def clean_pairing_data(cls, test_case):
            """
            Parse NVS content from device and receiver memories to clean pairing information.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            """
            if test_case.receiver_debugger is None:
                # Actual receiver use case
                DevicePairingTestUtils.unpair_all(test_case)
            # end if
        # end def clean_pairing_data

        @classmethod
        def check_device_pairing_data(cls, test_case, pairing_slot, bluetooth_address):
            """
            Check NVS BLE Bond ID chunk matching the given pairing slot.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param pairing_slot: device index
            :type pairing_slot: ``int``
            :param bluetooth_address: central or peripheral bluetooth address
            :type bluetooth_address: ``HexList``
            """
            # Dump device NVS
            test_case.device_memory_manager.read_nvs()
            # Extract the latest BLE pairing chunk
            device_chunk = test_case.device_memory_manager.get_active_chunk_by_name(
                f'NVS_BLE_BOND_ID_{int(Numeral(pairing_slot)) - 1}')
            # Check the Bluetooth address is matching
            test_case.assertEqual(
                obtained=device_chunk.bluetooth_low_energy_address.device_bluetooth_address,
                expected=bluetooth_address,
                msg="Pairing Status Notification and NVS BLE Bond Id chunk bluetooth address don't match")

            if test_case.receiver_memory_manager is not None:
                # Dump receiver NVS
                test_case.receiver_memory_manager.read_nvs()
                # Extract the BLE pairing chunk by bluetooth address
                receiver_chunks = test_case.receiver_memory_manager.get_ble_bond_id_chunks(
                    pairing_slot=None,
                    bluetooth_address=bluetooth_address)
                test_case.assertNotNone(receiver_chunks)
                test_case.assertEqual(len(receiver_chunks), 1,
                                      msg="Wrong number of chunk with the given bluetooth address")
                DevicePairingTestUtils.NvsManager.is_ble_bond_id_chunk_matching(test_case, device_chunk,
                                                                                receiver_chunks[0])
            # end if

            if test_case.f.SHARED.PAIRING.F_BLEProOsDetection:
                # Check OS detected type on the last occurrence
                test_case.assertEqual(obtained=int(Numeral(device_chunk.os_detected_type)),
                                      expected=BleNvsChunks.OsDetectedType.LOGITECH_BLE_PRO,
                                      msg='The OS detected type shall match the Logitech BLE Pro constant')
            # end if
        # end def check_device_pairing_data

        @classmethod
        def check_latency_removal_bit(cls, test_case, pairing_slot):
            """
            Check NVS BLE Bond ID chunk matching the given pairing slot.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param pairing_slot: device index
            :type pairing_slot: ``int``
            """
            # Dump receiver NVS
            test_case.memory_manager.read_nvs()
            # Extract the latest BLE pairing chunk
            device_chunk = test_case.memory_manager.get_active_chunk_by_name(
                f'NVS_BLE_BOND_ID_{int(Numeral(pairing_slot)) - 1}')
            # Check the Bluetooth address is matching
            test_case.assertEqual(
                obtained=device_chunk.ble_pro_attributes.ble_pro_attr_suppress_first_report_latency_bit,
                expected=1,
                msg="Latency removal bit in BLE attributes field from NVS BLE Bond Id chunk is not set")
        # end def check_latency_removal_bit

        @classmethod
        def check_os_detected(cls, test_case, pairing_slot, expected_os_type):
            """
            Check NVS BLE Bond ID chunk matching the given pairing slot.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param pairing_slot: device index
            :type pairing_slot: ``int``
            :param expected_os_type: OS detection byte value
            :type expected_os_type: ``int``
            """
            # Dump receiver NVS
            test_case.memory_manager.read_nvs()
            # Extract the latest BLE pairing chunk
            device_chunk = test_case.memory_manager.get_active_chunk_by_name(
                f'NVS_BLE_BOND_ID_{int(Numeral(pairing_slot)) - 1}')
            # Check the OS detected byte is matching
            test_case.assertEqual(
                obtained=int(Numeral(device_chunk.os_detected_type)),
                expected=expected_os_type,
                msg="OS detected type from NVS BLE Bond Id chunk is not correct")
        # end def check_os_detected

        @classmethod
        def check_receiver_pairing_data(cls, test_case, pairing_slot, bluetooth_address, entropy, auth_method):
            """
            Check NVS BLE Bond ID chunk matching the given pairing slot.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param pairing_slot: device index
            :type pairing_slot: ``int``
            :param bluetooth_address: central or peripheral bluetooth address
            :type bluetooth_address: ``HexList``
            :param entropy: pass key entropy
            :type entropy: ``HexList``
            :param auth_method: authentication method byte
            :type auth_method: ``HexList``
            """
            # Dump receiver NVS
            test_case.receiver_memory_manager.read_nvs()
            # Extract the latest BLE pairing chunk
            receiver_chunk = test_case.receiver_memory_manager.get_active_chunk_by_name(
                f'NVS_BLE_BOND_ID_{int(Numeral(pairing_slot)) - 1}')
            # Check the Bluetooth address is matching
            test_case.assertEqual(
                obtained=receiver_chunk.bluetooth_low_energy_address.device_bluetooth_address,
                expected=bluetooth_address,
                msg="Pairing Status Notification and NVS BLE Bond Id chunk bluetooth address don't match")
            # Check the Entropy and authentication method
            test_case.assertEqual(
                obtained=receiver_chunk.entropy,
                expected=entropy,
                msg="Pairing request and NVS BLE Bond Id chunk entropy values don't match")
            test_case.assertEqual(
                obtained=receiver_chunk.ble_pro_auth_control,
                expected=auth_method,
                msg="Pairing request and NVS BLE Bond Id chunk auth method values don't match")

            # Dump device NVS
            test_case.device_memory_manager.read_nvs()
            # Extract the BLE pairing chunk by bluetooth address
            device_chunks = test_case.device_memory_manager.get_ble_bond_id_chunks(
                pairing_slot=None,
                bluetooth_address=bluetooth_address)
            assert (device_chunks is not None and (1 <= len(device_chunks) <= 3))
            for chunk in device_chunks:
                DevicePairingTestUtils.NvsManager.is_ble_bond_id_chunk_matching(test_case, receiver_chunk, chunk)
            # end for
        # end def check_receiver_pairing_data

        @classmethod
        def is_ble_bond_id_chunk_matching(cls, test_case, receiver_chunk, device_chunk):
            """
            Check NVS BLE Bond ID chunks content.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param receiver_chunk: Receiver BLE pairing chunk
            :type receiver_chunk: ``ReceiverBleBondId``
            :param device_chunk: Device BLE pairing chunk
            :type device_chunk: ``DeviceBleBondIdV1``
            """
            # Check the Receiver and Device Keys are matching
            test_case.assertEqual(
                obtained=receiver_chunk.ble_gap_evt_auth_status, expected=device_chunk.ble_gap_evt_auth_status,
                msg="Receiver and device NVS BLE Bond Id chunks ble_gap_evt_auth_status values don't match")
            test_case.assertEqual(
                obtained=receiver_chunk.local_identity_key, expected=device_chunk.local_identity_key,
                msg="Receiver and device NVS BLE Bond Id chunks local_identity_key values don't match")
            test_case.assertEqual(
                obtained=receiver_chunk.remote_identity_key, expected=device_chunk.remote_identity_key,
                msg="Receiver and device NVS BLE Bond Id chunks remote_identity_key values don't match")
            test_case.assertEqual(
                obtained=receiver_chunk.remote_ble_gap_enc_info, expected=device_chunk.local_ble_gap_enc_info,
                msg="Receiver remote and device local ble_gap_enc_info values don't match")
            test_case.assertEqual(
                obtained=receiver_chunk.local_ble_gap_enc_info, expected=device_chunk.remote_ble_gap_enc_info,
                msg="Receiver local and device remote ble_gap_enc_info values don't match")
            test_case.assertEqual(
                obtained=receiver_chunk.local_gap_master_identification,
                expected=device_chunk.local_gap_master_identification,
                msg="Receiver and device NVS BLE Bond Id chunks local_gap_master_identification values don't match")
            test_case.assertEqual(
                obtained=receiver_chunk.remote_gap_master_identification,
                expected=device_chunk.remote_gap_master_identification,
                msg="Receiver and device NVS BLE Bond Id chunks remote_gap_master_identification values don't match")
        # end def is_ble_bond_id_chunk_matching
    # end class NvsManager

    class PerformDeviceConnectionResponseChecker(CommonBaseTestUtils.MessageChecker):
        """
        Perform Device Connection checker class
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the SetPerformDeviceConnection API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {}
        # end def get_default_check_map
    # end class PerformDeviceConnectionResponseChecker

    class PairingChecker(CommonBaseTestUtils.MessageChecker):
        """
        Pairing Notifications Checker class
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the PairingStatus API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {}
        # end def get_default_check_map

        @classmethod
        def set_bluetooth_address(cls, test_case, bt_address):
            """
            Set the discovered device bluetooth address for future use

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bt_address: Device bluetooth address
            :type bt_address: ``HexList``
            """
            test_case.bluetooth_address = bt_address
        # end def set_bluetooth_address

        @classmethod
        def get_bluetooth_address(cls, test_case):
            """
            Retrieve the stored device bluetooth address

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Device bluetooth address
            :rtype: ``HexList`` or ``None``
            """
            return test_case.bluetooth_address if hasattr(test_case, 'bluetooth_address') else None
        # end def get_bluetooth_address

        @classmethod
        def get_event(cls, test_case, expected_class, ignore_device_discovery=True, ignore_discovery_status=True,
                      ignore_device_recovery=True, timeout=2):
            """
            Get the next message in the receiver event queue ignoring potential discovery notifications

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param expected_class: Message class, should be a class inheriting from ``Hidpp1Message``
            :type expected_class: ``type``
            :param ignore_device_discovery: Skip DeviceDiscovery message from queue - OPTIONAL
            :type ignore_device_discovery: ``bool``
            :param ignore_discovery_status: Skip DiscoveryStatus message from queue - OPTIONAL
            :type ignore_discovery_status: ``bool``
            :param ignore_device_recovery: Skip DeviceRecovery message from queue - OPTIONAL
            :type ignore_device_recovery: ``bool``
            :param timeout: Time to wait for message before raising exception [seconds] - OPTIONAL
            :type timeout: ``int``

            :return: HID++ 1.0 notification
            :rtype: ``Hidpp1Message``
            """
            channel_receiver = ChannelUtils.get_receiver_channel(test_case=test_case)

            with ChannelUtils.channel_open_state(test_case=test_case, channel=channel_receiver):
                message = None
                logging_threshold = 1.5 * 10 ** 3
                start = perf_counter_ns()
                while message is None:
                    # Force temporarily a minimum timeout at 8 seconds
                    message = ChannelUtils.get_only(
                        test_case=test_case, channel=channel_receiver,
                        queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, timeout=max(timeout, 8),
                        received_trace_str=None)
                    delta = ((perf_counter_ns() // 10 ** 6) - (start // 10 ** 6))
                    if delta > logging_threshold:
                        test_case.log_warning(
                            message=f'Get message takes {delta}ms to complete (message type is '
                                    f'{message.__class__.__name__})',
                            warning_level=WarningLevel.ROBUSTNESS)
                    # end if
                    if isinstance(message, expected_class):
                        LogHelper.log_trace(test_case=test_case, msg=f"Received {message}\n")
                        return message
                    elif ((ignore_device_discovery and isinstance(message, DeviceDiscovery)) or
                          (ignore_discovery_status and isinstance(message, DiscoveryStatus)) or
                          (ignore_device_recovery and isinstance(message, DeviceRecovery))):
                        LogHelper.log_trace(test_case=test_case, msg=f"Ignored {message}\n")
                        message = None
                        continue
                    else:
                        raise AttributeError(f"Unexpected notification received: {message}")
                    # end if
                # end while
            # end with
        # end def get_event

        @classmethod
        def get_passkey_digits(cls, test_case):
            """
            Wait for a request display passkey notification and returns the provided digits

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: passkey digits
            :rtype: ``int``
            """
            LogHelper.log_info(test_case=test_case, msg="Get passkey digits")
            request_display_passkey = cls.get_event(test_case, RequestDisplayPassKey, timeout=3)
            test_case.assertNotNone(request_display_passkey, 'request_display_passkey notification not received')

            test_case.assertTrue(int(Numeral(request_display_passkey.passkey_length)) ==
                                 RequestDisplayPassKey.DEFAULT.PASSKEY_LENGTH,
                                 msg='Wrong passkey_length parameter received in request display passkey notification')
            cls.check_bt_address_and_padding(test_case, request_display_passkey)
            passkey_digits = int(ascii_converter(request_display_passkey.passkey_digits))
            return passkey_digits
        # end def get_passkey_digits

        @classmethod
        def check_no_passkey_digits(cls, test_case):
            """
            Check no request display passkey notification is returned

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            """
            channel_receiver = ChannelUtils.get_receiver_channel(test_case=test_case)

            with ChannelUtils.channel_open_state(test_case=test_case, channel=channel_receiver):
                LogHelper.log_info(test_case=test_case, msg="Check no passkey digits")
                # TODO: Is there a reason why we do not get only messages of the right type ? Do we need to empty the
                #  queue before getting RequestDisplayPassKey ?
                request_display_passkey = None
                message = ChannelUtils.get_only(test_case=test_case, channel=channel_receiver,
                                                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT)
                while request_display_passkey is None:
                    if isinstance(message, RequestDisplayPassKey):
                        request_display_passkey = message
                    else:
                        message = ChannelUtils.get_only(test_case=test_case, channel=channel_receiver,
                                                        queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT)
                    # end if
                # end while
                test_case.assertNone(request_display_passkey, 'request_display_passkey notification is received')
            # end with
        # end def check_no_passkey_digits

        @classmethod
        def get_display_passkey_start(cls, test_case):
            """
            Wait for a display passkey key start notification

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            """
            channel_receiver = ChannelUtils.get_receiver_channel(test_case=test_case)

            with ChannelUtils.channel_open_state(test_case=test_case, channel=channel_receiver):
                LogHelper.log_info(test_case=test_case, msg="Get display passkey start")
                display_passkey_key = ChannelUtils.get_only(
                    test_case=test_case, channel=channel_receiver,
                    queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DisplayPassKeyKey)
                test_case.assertTrue(int(Numeral(display_passkey_key.key_code)) ==
                                     DisplayPassKeyKey.KEY_CODE.PASSKEY_ENTRY_STARTED,
                                     msg='Wrong key_code parameter received in Display PassKey notification')
                cls.check_bt_address_and_padding(test_case, display_passkey_key)
            # end with
        # end def get_display_passkey_start

        @classmethod
        def get_display_passkey_entry(cls, test_case):
            """
            Wait for a display passkey key digit entered notification

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            """
            current_entropy = DevicePairingTestUtils.get_remaining_entropy(test_case)
            assert current_entropy is not None, "Cannot use this method if current_entropy has not been set"
            auth_method = DevicePairingTestUtils.get_authentication_method(test_case=test_case)
            assert auth_method is not None, "Cannot use this method if auth_method has not been set"
            channel_receiver = ChannelUtils.get_receiver_channel(test_case=test_case)

            with ChannelUtils.channel_open_state(test_case=test_case, channel=channel_receiver):
                LogHelper.log_info(test_case=test_case, msg="Get display passkey entry")
                try:
                    display_passkey_key = ChannelUtils.get_only(
                        test_case=test_case, channel=channel_receiver,
                        queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                        class_type=DisplayPassKeyKey)
                    test_case.assertTrue(int(Numeral(display_passkey_key.key_code)) ==
                                         DisplayPassKeyKey.KEY_CODE.PASSKEY_DIGIT_ENTERED,
                                         msg='Wrong key_code parameter received in Display PassKey notification')
                    cls.check_bt_address_and_padding(test_case, display_passkey_key)
                except QueueEmpty as exp:
                    if current_entropy == ENTROPY_FULFILLED:
                        # The firmware shall ignore the key pressed coming after the requested entropy
                        pass
                    else:
                        raise exp
                    # end if
                else:
                    full_filled = False
                    if auth_method == SetPerformDeviceConnectionRequest.MASK.EMU_2BUTTONS_AUTH_METHOD:
                        if current_entropy == ENTROPY_FULFILLED:
                            full_filled = True
                        else:
                            DevicePairingTestUtils.set_remaining_entropy(test_case,
                                                                         current_entropy - ENTROPY_PER_MSE_USER_ACTION)
                        # end if
                    elif auth_method == SetPerformDeviceConnectionRequest.MASK.PASSKEY_AUTH_METHOD:
                        if current_entropy < ENTROPY_FULFILLED:
                            full_filled = True
                        else:
                            DevicePairingTestUtils.set_remaining_entropy(test_case,
                                                                         current_entropy - ENTROPY_PER_KBD_USER_ACTION)
                        # end if
                    # end if
                    if full_filled:
                        test_case.log_warning("Unexpected DisplayPassKeyKey Digit entered notification received while "
                                              "entropy has already been fulfilled")
                    # end if
                # end try
            # end with
        # end def get_display_passkey_entry

        @classmethod
        def _get_display_passkey(cls, test_case):
            """
            Wait for a display passkey key completed notification

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Display pass key event
            :rtype: ``DisplayPassKeyKey``
            """
            channel_receiver = ChannelUtils.get_receiver_channel(test_case=test_case)

            with ChannelUtils.channel_open_state(test_case=test_case, channel=channel_receiver):
                return ChannelUtils.get_only(
                    test_case=test_case, channel=channel_receiver,
                    queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=DisplayPassKeyKey)
            # end with
        # end def _get_display_passkey

        @classmethod
        def get_display_passkey_end(cls, test_case):
            """
            Wait for a display passkey key completed notification

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            """
            LogHelper.log_info(test_case=test_case, msg="Get display passkey end")
            display_passkey_key = cls._get_display_passkey(test_case=test_case)
            test_case.assertTrue(int(Numeral(display_passkey_key.key_code)) ==
                                 DisplayPassKeyKey.KEY_CODE.PASSKEY_ENTRY_COMPLETED,
                                 msg='Wrong key_code parameter received in Display PassKey notification')
            cls.check_bt_address_and_padding(test_case, display_passkey_key)
        # end def get_display_passkey_end

        @classmethod
        def get_display_passkey_erased(cls, test_case):
            """
            Wait for a display passkey key erased notification

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            """
            LogHelper.log_info(test_case=test_case, msg="Get display passkey erased")
            display_passkey_key = cls._get_display_passkey(test_case=test_case)
            test_case.assertTrue(int(Numeral(display_passkey_key.key_code)) ==
                                 DisplayPassKeyKey.KEY_CODE.PASSKEY_DIGIT_ERASED,
                                 msg='Wrong key_code parameter received in Display PassKey notification')
            cls.check_bt_address_and_padding(test_case, display_passkey_key)
            current_entropy = DevicePairingTestUtils.get_remaining_entropy(test_case)
            DevicePairingTestUtils.set_remaining_entropy(test_case, current_entropy + ENTROPY_PER_KBD_USER_ACTION)
        # end def get_display_passkey_erased

        @classmethod
        def check_start_pairing_status(cls, test_case):
            """
            Wait for a start pairing status notification

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            """
            LogHelper.log_info(test_case=test_case, msg="Check start pairing status")
            pairing_status = cls.get_event(test_case, PairingStatus)
            test_case.assertTrue(int(Numeral(pairing_status.device_pairing_status)) ==
                                 PairingStatus.STATUS.PAIRING_START,
                                 msg='Wrong device_pairing_status parameter received in Pairing Status notification')
            test_case.assertTrue(int(Numeral(pairing_status.error_type)) == PairingStatus.ERROR_TYPE.NO_ERROR,
                                 msg='Wrong error_type parameter received in Pairing Status notification')
            cls.check_padding_is_zero(test_case, pairing_status)
            cls.set_bluetooth_address(test_case, pairing_status.bluetooth_address)
        # end def check_start_pairing_status

        @classmethod
        def check_notifications_absence(cls, test_case, ignore_pairing_status=False, ignore_request_passkey=False,
                                        ignore_display_passkey=False):
            """
            Check no start pairing status notification is returned

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param ignore_pairing_status: Raise an exception if set to False & ``PairingStatus`` message
                                          returned - OPTIONAL
            :type ignore_pairing_status: ``bool``
            :param ignore_request_passkey: Raise an exception if set to False & ``DisplayPassKeyKey`` message
                                           returned - OPTIONAL
            :type ignore_request_passkey: ``bool``
            :param ignore_display_passkey: Raise an exception if set to False & ``DisplayPassKeyKey`` message
                                           returned - OPTIONAL
            :type ignore_display_passkey: ``bool``
            """
            channel_receiver = ChannelUtils.get_receiver_channel(test_case=test_case)

            with ChannelUtils.channel_open_state(test_case=test_case, channel=channel_receiver):
                LogHelper.log_info(test_case=test_case, msg="Check notification absence")
                notifications = ChannelUtils.clean_messages(
                    test_case=test_case, channel=channel_receiver, queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                    class_type=(PairingStatus, RequestDisplayPassKey, DisplayPassKeyKey))

                pairing_status = None
                pairing_request = None
                pairing_display = None
                for notification in notifications:
                    if not ignore_pairing_status and isinstance(notification, PairingStatus):
                        pairing_status = notification
                    elif not ignore_request_passkey and isinstance(notification, RequestDisplayPassKey):
                        pairing_request = notification
                    elif not ignore_display_passkey and isinstance(notification, DisplayPassKeyKey):
                        pairing_display = notification
                    # end if
                # end for

                if not ignore_pairing_status:
                    test_case.assertNone(pairing_status, 'Pairing Status notification shall not be issued')
                # end if
                if not ignore_request_passkey:
                    test_case.assertNone(pairing_request, 'Request Display PassKey shall not be issued')
                # end if
                if not ignore_display_passkey:
                    test_case.assertNone(pairing_display, 'Display PassKey Key shall not be issued')
                # end if
            # end with
        # end def check_notifications_absence

        @classmethod
        def check_bt_address_and_padding(cls, test_case, message):
            """
            Wait for a stop pairing status notification

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: HID++ Message
            :type message: ``HidppMessage``
            """
            LogHelper.log_info(test_case=test_case, msg="Check BT address and padding")
            test_case.assertTrue(cls.get_bluetooth_address(test_case) == message.bluetooth_address,
                                 msg=f'Wrong Bluetooth address parameter({message.bluetooth_address}) received in '
                                     f'Pairing Status notification (not matching reference '
                                     f'{cls.get_bluetooth_address(test_case)})')
            cls.check_padding_is_zero(test_case, message)
        # end def check_bt_address_and_padding

        @classmethod
        def check_stop_pairing_status(cls, test_case, timeout=9):
            """
            Wait for a stop pairing status notification

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param timeout: Time to wait for message before raising exception [seconds] - OPTIONAL
                            Default is now 9 seconds to better handle recovery use case
            :type timeout: ``int``

            :return: pairing slot returned by the receiver
            :rtype: ``HexList``
            """
            channel_receiver = ChannelUtils.get_receiver_channel(test_case=test_case)

            with ChannelUtils.channel_open_state(test_case=test_case, channel=channel_receiver):
                LogHelper.log_info(test_case=test_case, msg="Check stop pairing status")
                pairing_status = ChannelUtils.get_only(
                    test_case=test_case, channel=channel_receiver, queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                    class_type=PairingStatus, timeout=timeout)
                test_case.assertTrue(
                    int(Numeral(pairing_status.device_pairing_status)) == PairingStatus.STATUS.PAIRING_STOP,
                    msg='Wrong device_pairing_status parameter received in Pairing Status notification')
                test_case.assertTrue(int(Numeral(pairing_status.error_type)) == PairingStatus.ERROR_TYPE.NO_ERROR,
                                     msg='Wrong error_type parameter received in Pairing Status notification')
                cls.check_bt_address_and_padding(test_case, pairing_status)
                return pairing_status.pairing_slot
            # end with
        # end def check_stop_pairing_status

        @classmethod
        def check_timeout_pairing_status(cls, test_case):
            """
            Wait for a timeout pairing status notification
            TODO: https://jira.logitech.io/browse/BPRO-182

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            """
            channel_receiver = ChannelUtils.get_receiver_channel(test_case=test_case)

            with ChannelUtils.channel_open_state(test_case=test_case, channel=channel_receiver):
                LogHelper.log_info(test_case=test_case, msg="Check timeout pairing status")
                pairing_status = ChannelUtils.get_only(
                    test_case=test_case, channel=channel_receiver, check_first_message=False,
                    queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT, class_type=PairingStatus)
                test_case.assertTrue(
                    int(Numeral(pairing_status.device_pairing_status)) == PairingStatus.STATUS.PAIRING_STOP,
                    msg='Wrong device_pairing_status parameter received in Pairing Status notification')
                test_case.assertTrue(int(Numeral(pairing_status.error_type)) in [PairingStatus.ERROR_TYPE.TIMEOUT,
                                                                                 PairingStatus.ERROR_TYPE.FAILED],
                                     msg='Wrong error_type parameter received in Pairing Status notification')
                # add warning
                if int(Numeral(pairing_status.error_type)) is PairingStatus.ERROR_TYPE.FAILED:
                    test_case.log_warning("Failed pairing status received while a timeout was expected")
                # end if
                cls.check_bt_address_and_padding(test_case, pairing_status)
            # end with
        # end def check_timeout_pairing_status

        @classmethod
        def check_failed_pairing_status(cls, test_case):
            """
            Wait for an error pairing status notification

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            """
            channel_receiver = ChannelUtils.get_receiver_channel(test_case=test_case)

            with ChannelUtils.channel_open_state(test_case=test_case, channel=channel_receiver):
                LogHelper.log_info(test_case=test_case, msg="Check failed pairing status")
                pairing_status = ChannelUtils.get_only(
                    test_case=test_case, channel=channel_receiver, queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                    class_type=PairingStatus, timeout=5)
                test_case.assertTrue(
                    int(Numeral(pairing_status.device_pairing_status)) == PairingStatus.STATUS.PAIRING_STOP,
                    msg='Wrong device_pairing_status parameter received in Pairing Status notification')
                test_case.assertTrue(int(Numeral(pairing_status.error_type)) == PairingStatus.ERROR_TYPE.FAILED,
                                     msg='Wrong error_type parameter received in Pairing Status notification')
                cls.check_bt_address_and_padding(test_case, pairing_status)
            # end with
        # end def check_failed_pairing_status

        @classmethod
        def check_cancel_pairing_status(cls, test_case, bypass_address_check=False):
            """
            Wait for a stop pairing status notification

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bypass_address_check: is the Bluetooth address value compared to the one coming from the start
                                         pairing notification - OPTIONAL
            :type bypass_address_check: ``bool``
            """
            LogHelper.log_info(test_case=test_case, msg="Check cancel pairing status")

            pairing_status = cls.get_event(test_case, PairingStatus)
            test_case.assertTrue(int(Numeral(pairing_status.device_pairing_status)) ==
                                 PairingStatus.STATUS.PAIRING_CANCEL,
                                 msg='Wrong device_pairing_status parameter received in Pairing Status notification')
            test_case.assertTrue(int(Numeral(pairing_status.error_type)) == PairingStatus.ERROR_TYPE.NO_ERROR,
                                 msg='Wrong error_type parameter received in Pairing Status notification')
            if not bypass_address_check:
                cls.check_bt_address_and_padding(test_case, pairing_status)
            # end if
        # end def check_cancel_pairing_status
    # end class PairingChecker
# end class DevicePairingTestUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
