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
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.connectionscheme.pairing import SharedPairingTestCase
from pyharness.selector import features
from pyharness.extensions import level
from pyharness.selector import services
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionRequest
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionResponse
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from time import sleep
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.hidpp1message import Hidpp1Message


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class PairingTestCase(SharedPairingTestCase, ReceiverBaseTestCase):
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
    def test_device_connect(self):
        """
        Validates device connect request (82 C1)

        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Force the device to connect')
        # ---------------------------------------------------------------------------
        write_device_connect = SetPerformDeviceConnectionRequest(
            connect_devices=SetPerformDeviceConnectionRequest.ConnectState.PAIRING,
            bluetooth_address=HexList("AABBCCDDEEFF"), emu_2buttons_auth_method=True)
        write_device_connect_response = self.send_report_wait_response(
            report=write_device_connect,
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=SetPerformDeviceConnectionResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate device connect response')
        # ---------------------------------------------------------------------------
        DevicePairingTestUtils.PerformDeviceConnectionResponseChecker.check_fields(self, write_device_connect_response,
                                                                                   SetPerformDeviceConnectionResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Wait for a start pairing status notification')
        # ---------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.check_start_pairing_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Perform device connection request with Connect Devices = Cancel Pairing")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.cancel_pairing(self)

        self.testCaseChecked("FNT_RCV-C1_0001")

    # end def test_device_connect
# end class PairingTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
