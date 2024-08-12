#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.connectionscheme.pairing_robustness
:brief: Device BLE connection scheme pairing robustness test suite
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/05/16
"""
from time import sleep

# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.notifications.requestdisplaypasskey import RequestDisplayPassKey
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.connectionscheme.pairing_robustness import SharedPairingRobustnessTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class PairingRobustnessTestCase(SharedPairingRobustnessTestCase, DeviceBaseTestCase):
    """
    Device Pairing Robustness TestCases
    """

    @features('BLEDevicePairing')
    @features('PasskeyAuthenticationMethod')
    @level('Robustness')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_BACKSPACE,))
    @bugtracker('Erasing_Leading_Zero')
    def test_delete_zero_leading_passkey(self):
        """
        Verify erasing a leading zero in the passkey exchange
        """
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

        for index in range(1, RequestDisplayPassKey.PASSKEY_IN_DIGITS + 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Enter {index} '0' key")
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.generate_keystrokes(self, 0,
                                                       end=(RequestDisplayPassKey.PASSKEY_IN_DIGITS - 1 - index),
                                                       log_check=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {index} times the 'Backspace' key")
            # ----------------------------------------------------------------------------------------------------------
            # noinspection DuplicatedCode

            for del_count in range(index):
                sleep(DevicePairingTestUtils.KEYSTROKE_INTERVAL)
                DevicePairingTestUtils.press_delete_key(self, key_name='backspace')
            # end for
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send the whole digit sequence")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.generate_keystrokes(self, passkey_digits)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'User enters the end of sequence input')
        # --------------------------------------------------------------------------------------------------------------
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
    # end def test_delete_zero_leading_passkey
# end class PairingRobustnessTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
