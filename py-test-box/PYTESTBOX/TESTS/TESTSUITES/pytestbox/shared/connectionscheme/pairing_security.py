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
from datetime import datetime
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionRequest
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.connectionscheme.pairing import SharedCommonPairingTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SharedPairingSecurityTestCase(SharedCommonPairingTestCase, ABC):
    """
    Shared Pairing Security TestCases
    """
    TIMEOUT_MARGIN = 1

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
    def test_pairing_max_time(self):
        """
        Check Perform Device pairing timeout is not lower than 30s
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Perform device connection request with Connect Devices = 1 i.e. Pairing')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.start_pairing_sequence(self, self.device_bluetooth_address, log_check=True)

        start_time = datetime.now()
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
        LogHelper.log_step(self, 'Loop over passkey inputs list provided by the receiver')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.generate_keystrokes(self, passkey_digits, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for just below 30s')
        # --------------------------------------------------------------------------------------------------------------
        delay = datetime.now() - start_time
        if not (delay.total_seconds() > (self.PAIRING_TIMEOUT - self.TIMEOUT_MARGIN)):
            sleep(self.PAIRING_TIMEOUT - self.TIMEOUT_MARGIN - delay.total_seconds())
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'User enters the last passkey input')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.generate_end_of_sequence(self, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a stop pairing status notification''')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.check_stop_pairing_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a device connection notification''')
        # --------------------------------------------------------------------------------------------------------------
        device_connection = ChannelUtils.get_only(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection)

        device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
        device_info = device_info_class.fromHexList(HexList(device_connection.information))
        assert (int(Numeral(device_info.device_info_link_status)) == DeviceConnection.LinkStatus.LINK_ESTABLISHED)

        self.testCaseChecked("FNT_DEV_PAIR_0025")
    # end def test_pairing_max_time

    @features('BLEDevicePairing')
    @level('Functionality')
    def test_user_action_timeout(self):
        """
        Check Perform Device pairing timeout is 30s
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Perform device connection request with Connect Devices = 1 i.e. Pairing')
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
        LogHelper.log_step(self, 'Emulate a random user action')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.generate_keystrokes(self, passkey_digits, start=0, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'wait 30s')
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.PAIRING_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 6: Wait for a timeout pairing status notification')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.check_timeout_pairing_status(self)

        self.testCaseChecked("FNT_DEV_PAIR_0026")
    # end def test_user_action_timeout

    @features('BLEDevicePairing')
    @level('Security')
    def test_bad_passkey(self):
        """
        2 buttons emulation authentication method robustness test: 1 keystroke doesn't match its requested action
        or
        Standard passkey emulation authentication method robustness test: 1 keystroke doesn't match its requested action
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Perform device connection request with Connect Devices = 1 i.e. Pairing')
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
        LogHelper.log_step(self, 'Corrupt the passkey code')
        # --------------------------------------------------------------------------------------------------------------
        passkey_digits -= 1

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Loop over passkey inputs list provided by the receiver')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.generate_keystrokes(self, passkey_digits, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'User enters the last passkey input')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.generate_end_of_sequence(self, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a failed pairing status notification''')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.check_failed_pairing_status(self)

        self.testCaseChecked("FNT_DEV_PAIR_0027")
        self.testCaseChecked("FNT_DEV_PAIR_0030")
    # end def test_bad_passkey

    @features('BLEDevicePairing')
    @level('Security')
    def test_fewer_keystrokes(self):
        """
        2 buttons emulation authentication method robustness test: fewer keystrokes than requested
        or
        Standard passkey emulation authentication method robustness test: fewer keystrokes than requested
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Perform device connection request with Connect Devices = 1 i.e. Pairing')
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
        LogHelper.log_step(self, 'Loop over passkey inputs list provided by the receiver except the last one')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.generate_keystrokes(self, passkey_digits, end=0, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'User enters the end of sequence input')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.generate_end_of_sequence(self, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a failed pairing status notification''')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.check_failed_pairing_status(self)

        self.testCaseChecked("FNT_DEV_PAIR_0028")
        self.testCaseChecked("FNT_DEV_PAIR_0031")
    # end def test_fewer_keystrokes

    @features('BLEDevicePairing')
    @level('Security')
    def test_more_keystrokes(self):
        """
        2 buttons emulation authentication method robustness test: more keystrokes than requested
        or
        Standard passkey emulation authentication method robustness test: more keystrokes than requested
        Check keystroke after the max number are ignored by the firmware
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Perform device connection request with Connect Devices = 1 i.e. Pairing')
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
        LogHelper.log_step(self, 'Loop over passkey inputs list provided by the receiver')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.generate_keystrokes(self, passkey_digits, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Redo the last keystroke')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.generate_keystrokes(self, passkey_digits, start=0, log_check=True,
                                                   digit_to_ignore_display_key_check=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'User enters the last passkey input')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.generate_end_of_sequence(self, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a success pairing status notification')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.check_stop_pairing_status(self)

        self.testCaseChecked("FNT_DEV_PAIR_0029")
        self.testCaseChecked("FNT_DEV_PAIR_0032")
    # end def test_more_keystrokes

    @features('BLEDevicePairing')
    @level('Security')
    def test_shifted_keystrokes(self):
        """
        2 buttons emulation authentication method robustness test: shifted keystrokes
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Perform device connection request with Connect Devices = 1 i.e. Pairing')
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
        LogHelper.log_step(self, 'Trigger 2 keystrokes (take the two last ones from the actual passkey)')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.generate_keystrokes(self, passkey_digits, start=1, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Loop over passkey inputs list provided by the receiver')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.generate_keystrokes(self, passkey_digits, log_check=True,
                                                   digit_to_ignore_display_key_check=1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'User enters the last passkey input')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.generate_end_of_sequence(self, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a failed pairing status notification''')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.check_failed_pairing_status(self)

        self.testCaseChecked("FNT_DEV_PAIR_0029")
    # end def test_shifted_keystrokes

    @features('BLEDevicePairing')
    @features('Passkey2ButtonsAuthenticationMethod')
    @level('Functionality')
    def test_inter_keystroke_timeout(self):
        """
        Check timeout between 2 user actions is not lower than 30s
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Perform device connection request with Connect Devices = 1 i.e. Pairing')
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

        for index in reversed(range(SetPerformDeviceConnectionRequest.DEFAULT.ENTROPY_LENGTH_MAX)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Loop over passkey inputs list provided by the receiver')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.generate_keystrokes(self, passkey_digits, start=index, end=index-1, log_check=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for just below 30s')
            # ----------------------------------------------------------------------------------------------------------
            sleep(self.PAIRING_TIMEOUT - 2*self.TIMEOUT_MARGIN)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'User enters the last passkey input')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.generate_end_of_sequence(self, log_check=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a stop pairing status notification')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.check_stop_pairing_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for a device connection notification')
        # --------------------------------------------------------------------------------------------------------------
        device_connection = ChannelUtils.get_only(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection)

        device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
        device_info = device_info_class.fromHexList(HexList(device_connection.information))
        assert (int(Numeral(device_info.device_info_link_status)) == DeviceConnection.LinkStatus.LINK_ESTABLISHED)

        self.testCaseChecked("FNT_DEV_PAIR_0025")
    # end def test_inter_keystroke_timeout
# end class SharedPairingSecurityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
