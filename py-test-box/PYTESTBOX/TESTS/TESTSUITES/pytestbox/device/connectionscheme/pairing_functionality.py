#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.connectionscheme.pairing
:brief: Validate 'device pairing' feature
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2020/06/23
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import choice
from time import sleep

from pyharness.core import TYPE_ERROR
from pyharness.core import TestException
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.notifications.requestdisplaypasskey import RequestDisplayPassKey
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.connectionscheme.pairing_functionality import SharedPairingFunctionalityTestCase
from pytestbox.shared.connectionscheme.pairing_functionality import SharedUnpairingFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
LOWEST_PASSKEY_WITHOUT_ZERO_START = 100_000


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PairingFunctionalityTestCase(SharedPairingFunctionalityTestCase, DeviceBaseTestCase):
    """
    TestCase class for device paring functionality tests
    """

    MAX_LOOP_COUNT = 10
    DIGIT_ERASED_RETRY_COUNTER = 6

    @features('BLEDevicePairing')
    @level('Functionality')
    @services('Debugger')
    def test_reset_device_during_pairing_sequence(self):
        """
        Power off/on the DUT during a passkey entry sequence, then restart the discovery / pairing sequence
        when the device is available.
        """
        # noinspection DuplicatedCode
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send 'Perform device connection' request with Connect Devices = 1 i.e. Pairing")
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
        LogHelper.log_check(self, "Wait for a 'Digit Start' passkey notification")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.get_display_passkey_start(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Loop over part of the passkey inputs list provided by the receiver')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.generate_keystrokes(self, passkey_digits, end=2, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off/on the device')
        # --------------------------------------------------------------------------------------------------------------
        self.debugger.reset()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a failed pairing status notification')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.check_failed_pairing_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force again the device in pairing mode')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.change_host_by_link_state(
            self, link_state=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Restart the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Restart the pairing sequence')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        self.testCaseChecked("FNT_DEV_PAIR_0035")
    # end def test_reset_device_during_pairing_sequence

    @features('BLEDevicePairing')
    @features('PasskeyAuthenticationMethod')
    @level('Functionality')
    def test_all_digits_combination(self):
        """
        standard passkey emulation authentication method: Run pairing sequence multiple times
        until all digits was part of the passkey (numPad and standardKey)
        """
        infinite_loop_protection_count = 0
        digits_bitmap = HexList("03FF")
        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Loop until all digits have been included in the passkey')
        # --------------------------------------------------------------------------------------------------------------
        while digits_bitmap != HexList("0000") and infinite_loop_protection_count < self.MAX_LOOP_COUNT:
            # noinspection DuplicatedCode
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'start the discovery sequence')
            # ----------------------------------------------------------------------------------------------------------
            bluetooth_address = DiscoveryTestUtils.discover_device(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send 'Perform device connection' request with Connect Devices = 1 (i.e Pairing)")
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.start_pairing_sequence(self, bluetooth_address)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a start pairing status notification')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.check_start_pairing_status(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a display passkey notification')
            # ----------------------------------------------------------------------------------------------------------
            passkey_digits = DevicePairingTestUtils.PairingChecker.get_passkey_digits(self)
            for index in reversed(range(RequestDisplayPassKey.PASSKEY_IN_DIGITS)):
                digit_value = (passkey_digits // (10 ** index)) % 10
                digits_bitmap.clearBit(digit_value)
            # end for

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait for a 'Digit Start' passkey notification")
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.PairingChecker.get_display_passkey_start(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Loop over passkey inputs list provided by the receiver')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.generate_keystrokes(self, passkey_digits)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'User enters the last passkey input')
            # ----------------------------------------------------------------------------------------------------------
            # noinspection DuplicatedCode
            DevicePairingTestUtils.generate_end_of_sequence(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a stop pairing status notification')
            # ----------------------------------------------------------------------------------------------------------
            pairing_slot = DevicePairingTestUtils.PairingChecker.check_stop_pairing_status(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a device connection notification')
            # ----------------------------------------------------------------------------------------------------------
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
            # end while
            infinite_loop_protection_count += 1

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Unpair the device')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.unpair_slot(self, int(Numeral(pairing_slot)))
        # end while

        self.testCaseChecked("FNT_DEV_PAIR_0038")
    # end def test_all_digits_combination

    @features('BLEDevicePairing')
    @features('PasskeyAuthenticationMethod')
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_RETURN_ENTER, KEY_ID.KEYPAD_ENTER,))
    def test_both_enter_keys(self):
        """
        standard passkey emulation authentication method: Check both "Enter keys" are working to end the sequence
        """
        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('''Test Loop over both 'enter' keys''')
        # --------------------------------------------------------------------------------------------------------------
        for keypad_key in [True, False]:

            # noinspection DuplicatedCode
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'start the discovery sequence')
            # ----------------------------------------------------------------------------------------------------------
            bluetooth_address = DiscoveryTestUtils.discover_device(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send 'Perform device connection' request with Connect Devices = 1 (i.e Pairing)")
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.start_pairing_sequence(self, bluetooth_address)

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
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.generate_keystrokes(self, passkey_digits)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'User enters the last passkey input')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.generate_end_of_sequence(self, keypad_key=keypad_key)

            # noinspection DuplicatedCode
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a stop pairing status notification')
            # ----------------------------------------------------------------------------------------------------------
            pairing_slot = DevicePairingTestUtils.PairingChecker.check_stop_pairing_status(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a device connection notification')
            # ----------------------------------------------------------------------------------------------------------
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
            # end while

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Unpair the device')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.unpair_slot(self, int(Numeral(pairing_slot)))
        # end for

        self.testCaseChecked("FNT_DEV_PAIR_0039")
    # end def test_both_enter_keys

    @features('BLEDevicePairing')
    @features('PasskeyAuthenticationMethod')
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_BACKSPACE,))
    def test_backspace_key(self):
        """
        standard passkey emulation authentication method: Check "Backspace key" is working to delete a digit entry.
        """
        # noinspection DuplicatedCode
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'start the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send 'Perform device connection' request with Connect Devices = 1 (i.e Pairing)")
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
        LogHelper.log_check(self, "Wait for a 'Digit Start' passkey notification")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.get_display_passkey_start(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Loop over passkey inputs list provided by the receiver except the last one")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.generate_keystrokes(self, passkey_digits, end=0, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Delete the previous key by pressing the 'backspace' key")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.press_delete_key(self, key_name='backspace')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter the last 2 keys')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.generate_keystrokes(self, passkey_digits, start=1, log_check=True)

        # noinspection DuplicatedCode
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'User enters the end of sequence input')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.generate_end_of_sequence(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a stop pairing status notification')
        # --------------------------------------------------------------------------------------------------------------
        pairing_slot = DevicePairingTestUtils.PairingChecker.check_stop_pairing_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a device connection notification')
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
        # end while

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Unpair the device')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.unpair_slot(self, int(Numeral(pairing_slot)))

        self.testCaseChecked("FNT_DEV_PAIR_0040")
    # end def test_backspace_key

    @features('BLEDevicePairing')
    @features('PasskeyAuthenticationMethod')
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_BACKSPACE,))
    def test_delete_multiple_entries(self):
        """
        standard passkey emulation authentication method: Check that pressing the "Backspace key" multiple times in
        succession allow to delete the digit entries (test up to 6  keys deletion)
        """
        retry = self.DIGIT_ERASED_RETRY_COUNTER
        # Initialize the delete key counter
        index = 1
        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('''Test Loop over the number of digit in the standard passkey''')
        # --------------------------------------------------------------------------------------------------------------
        while index < (RequestDisplayPassKey.PASSKEY_IN_DIGITS + 1):
            # noinspection DuplicatedCode
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'start the discovery sequence')
            # ----------------------------------------------------------------------------------------------------------
            bluetooth_address = DiscoveryTestUtils.discover_device(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send 'Perform device connection' request with Connect Devices = 1 (i.e Pairing)")
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.start_pairing_sequence(self, bluetooth_address)

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
            LogHelper.log_step(self, f"Loop over the first {index} passkey inputs provided by the receiver")
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.generate_keystrokes(self, passkey_digits,
                                                       end=(RequestDisplayPassKey.PASSKEY_IN_DIGITS - 1 - index),
                                                       log_check=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Undo the previous {index} key presses")
            # ----------------------------------------------------------------------------------------------------------
            # noinspection DuplicatedCode
            try:
                for del_count in range(index):
                    sleep(DevicePairingTestUtils.KEYSTROKE_INTERVAL)
                    DevicePairingTestUtils.press_delete_key(self, key_name='backspace')
                # end for
            except AssertionError as e:
                if retry > 0 and passkey_digits < LOWEST_PASSKEY_WITHOUT_ZERO_START:
                    retry -= 1
                    self.log_warning('No event when pressing the delete key. Cancel the pairing\n',
                                     force_console_print=True)
                    DevicePairingTestUtils.cancel_pairing(self)
                    continue
                else:
                    raise TestException(TYPE_ERROR, "Backspace key does not generate notification after "
                                                    f"{self.DIGIT_ERASED_RETRY_COUNTER} retries "
                                                    f"when passkey is {passkey_digits:06d} (should only fail "
                                                    f"on passkey starting with zero see "
                                                    f"https://jira.logitech.io/browse/BT-597) ({e})")
                # end if
            # end try

            # noinspection DuplicatedCode
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Resend the whole digits sequence")
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.generate_keystrokes(self, passkey_digits, log_check=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'User enters the end of sequence input')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.generate_end_of_sequence(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a stop pairing status notification')
            # ----------------------------------------------------------------------------------------------------------
            pairing_slot = DevicePairingTestUtils.PairingChecker.check_stop_pairing_status(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a device connection notification')
            # ----------------------------------------------------------------------------------------------------------
            message_count = 0
            while message_count < 5:
                # noinspection DuplicatedCode
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
            # end while

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Unpair the device')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.unpair_slot(self, int(Numeral(pairing_slot)))
            # Increase the delete key counter
            index += 1
        # end while

        self.testCaseChecked("FNT_DEV_PAIR_0041")
    # end def test_delete_multiple_entries

    @features('BLEDevicePairing')
    @features('PasskeyAuthenticationMethod')
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_BACKSPACE,))
    def test_delete_more_entries(self):
        """
        standard passkey emulation authentication method: Check that pressing the "Backspace key"
        more times in succession than the number of digit entries are ignored
        """
        retry = self.DIGIT_ERASED_RETRY_COUNTER
        # Initialize the delete key counter
        index = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over the number of digit in the standard passkey from 1 to '
                                 f'{RequestDisplayPassKey.PASSKEY_IN_DIGITS}')
        # --------------------------------------------------------------------------------------------------------------
        while index < (RequestDisplayPassKey.PASSKEY_IN_DIGITS+1):
            # noinspection DuplicatedCode
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'start the discovery sequence')
            # ----------------------------------------------------------------------------------------------------------
            bluetooth_address = DiscoveryTestUtils.discover_device(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send 'Perform device connection' request with Connect Devices = 1 (i.e Pairing)")
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.start_pairing_sequence(self, bluetooth_address)

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
            LogHelper.log_step(self, f"Loop over the first {index} passkey inputs provided by the receiver")
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.generate_keystrokes(self, passkey_digits,
                                                       end=(RequestDisplayPassKey.PASSKEY_IN_DIGITS - 1 - index),
                                                       log_check=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {index + 1} times the 'Backspace' key")
            # ----------------------------------------------------------------------------------------------------------
            # noinspection DuplicatedCode
            try:
                for del_count in range(index):
                    sleep(DevicePairingTestUtils.KEYSTROKE_INTERVAL)
                    DevicePairingTestUtils.press_delete_key(self, key_name='backspace')
                # end for
                DevicePairingTestUtils.press_delete_key(self, key_name='backspace', ignore_erased_notification=True)
            except AssertionError as e:
                if retry > 0 and passkey_digits < LOWEST_PASSKEY_WITHOUT_ZERO_START:
                    retry -= 1
                    self.log_warning('No event when pressing the delete key. Cancel the pairing\n',
                                     force_console_print=True)
                    DevicePairingTestUtils.cancel_pairing(self)
                    continue
                else:
                    raise TestException(TYPE_ERROR, "Backspace key does not generate notification after "
                                                    f"{self.DIGIT_ERASED_RETRY_COUNTER} retries "
                                                    f"when passkey is {passkey_digits:06d} (should only fail "
                                                    f"on passkey starting with zero see "
                                                    f"https://jira.logitech.io/browse/BT-597) ({e})")
                # end if
            # end try
            # noinspection DuplicatedCode
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Resend the whole digits sequence")
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.generate_keystrokes(self, passkey_digits, log_check=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'User enters the end of sequence input')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.generate_end_of_sequence(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a stop pairing status notification')
            # ----------------------------------------------------------------------------------------------------------
            pairing_slot = DevicePairingTestUtils.PairingChecker.check_stop_pairing_status(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a device connection notification')
            # ----------------------------------------------------------------------------------------------------------
            message_count = 0
            # noinspection DuplicatedCode
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
            # end while

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Unpair the device')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.unpair_slot(self, int(Numeral(pairing_slot)))
            # Increase the delete key counter
            index += 1
        # end while

        self.testCaseChecked("FNT_DEV_PAIR_0042")
    # end def test_delete_more_entries

    @features('BLEDevicePairing')
    @features('PasskeyAuthenticationMethod')
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_Z, KEY_ID.KEYBOARD_EQUAL_AND_PLUS,
                               KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_SEMICOLON_AND_COLON, ))
    def test_other_keys_ignored(self):
        """
        Standard passkey emulation authentication method robustness test: check only numeric keys have effect ;
        others keys are ignored.
        """
        # TODO Find a better way to provide the complete list of key for a given key matrix
        other_ignored_keys = [KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_Z, KEY_ID.KEYBOARD_EQUAL_AND_PLUS,
                              KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_SEMICOLON_AND_COLON]
        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('''Test Loop over the keys that shall be ignored on the current matrix''')
        # --------------------------------------------------------------------------------------------------------------
        while len(other_ignored_keys) > 0:
            # noinspection DuplicatedCode
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'start the discovery sequence')
            # ----------------------------------------------------------------------------------------------------------
            bluetooth_address = DiscoveryTestUtils.discover_device(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send 'Perform device connection' request with Connect Devices = 1 (i.e Pairing)")
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.start_pairing_sequence(self, bluetooth_address)

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
            LogHelper.log_step(self, "Loop over the passkey inputs provided by the receiver")
            # ----------------------------------------------------------------------------------------------------------
            for digit_index in reversed(range(RequestDisplayPassKey.PASSKEY_IN_DIGITS)):
                DevicePairingTestUtils.generate_keystrokes(self, passkey_digits, start=digit_index, end=digit_index - 1,
                                                           log_check=True)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Press any key in the ignored key list")
                # ------------------------------------------------------------------------------------------------------
                key_id = None
                if len(other_ignored_keys) > 0:
                    key_id = choice(other_ignored_keys)
                    other_ignored_keys.remove(key_id)
                # end if
                DevicePairingTestUtils.generate_user_action(self, key_id=key_id)
            # end for
            # noinspection DuplicatedCode
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'User enters the end of sequence input')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.generate_end_of_sequence(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a stop pairing status notification')
            # ----------------------------------------------------------------------------------------------------------
            pairing_slot = DevicePairingTestUtils.PairingChecker.check_stop_pairing_status(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for a device connection notification')
            # ----------------------------------------------------------------------------------------------------------
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
            # end while

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Unpair the device')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.unpair_slot(self, int(Numeral(pairing_slot)))
        # end while

        self.testCaseChecked("FNT_DEV_PAIR_0043")
    # end def test_other_keys_ignored
# end class PairingFunctionalityTestCase


class UnpairingFunctionalityTestCase(SharedUnpairingFunctionalityTestCase, DeviceBaseTestCase):
    """
    Device Unpairing Functional TestCases
    """

# end class UnpairingFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
