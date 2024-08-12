#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.receiver.connectionscheme.pairing
    :brief: Validates 'device pairing' feature
    :author: Christophe Roquebert
    :date: 2020/03/10
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetest import ReceiverBaseTestCase
from pytestbox.shared.connectionscheme.pairing_functionality import SharedPairingFunctionalityTestCase
from pytestbox.shared.connectionscheme.pairing_functionality import SharedUnpairingFunctionalityTestCase
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pyharness.selector import features
from pyharness.extensions import level
from pyharness.selector import services
from time import sleep
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class PairingFunctionalityTestCase(SharedPairingFunctionalityTestCase, ReceiverBaseTestCase):
    def setUp(self):
        """
        Handles test prerequisites.
        """
        super().setUp()
    # end def setUp

    def tearDown(self):
        """
        Handles test post-requisites.
        """
        super().tearDown()
    # end def tearDown

    @features('BLEDevicePairing')
    @level('Functionality')
    @services('Debugger')
    def test_reset_receiver_during_pairing_sequence(self):
        """
        Unplug the receiver during a passkey entry sequence, then restart the discovery / pairing sequence
        when the receiver is available.
        """

        # ---------------------------------------------------------------------------
        self.logTitle2("Test Step 1: Send 'Perform device connection' request with Connect Devices = 1 i.e. "
                           "Pairing")
        # ---------------------------------------------------------------------------
        DevicePairingTestUtils.start_pairing_sequence(self, self.device_bluetooth_address, log_check=True)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for a start pairing status notification')
        # ---------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.check_start_pairing_status(self)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Wait for a display passkey notification')
        # ---------------------------------------------------------------------------
        passkey_digits = DevicePairingTestUtils.PairingChecker.get_passkey_digits(self)

        # ---------------------------------------------------------------------------
        self.logTitle2('''Test Check 3: Wait for a 'Digit Start' passkey notification''')
        # ---------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.get_display_passkey_start(self)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Loop over part of the passkey inputs list provided by the receiver')
        # ---------------------------------------------------------------------------
        DevicePairingTestUtils.generate_keystrokes(self, passkey_digits, end=2, log_check=True)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Power off/on the receiver')
        # ---------------------------------------------------------------------------
        self.reset(hardware_reset=True)
        # Re-enable HID++ reporting
        self.enable_hidpp_reporting()

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 4: Restart the discovery sequence')
        # ---------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 5: Restart the pairing sequence')
        # ---------------------------------------------------------------------------
        pairing_slot = DevicePairingTestUtils.pair_device(self, bluetooth_address)

        self.testCaseChecked("FNT_DEV_PAIR_0036")
    # end def test_reset_receiver_during_pairing_sequence
# end class PairingFunctionalityTestCase


class UnpairingFunctionalityTestCase(SharedUnpairingFunctionalityTestCase, ReceiverBaseTestCase):
    """
    Receiver Unpairing Functional TestCases
    """

# end class PairingFunctionalityTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
