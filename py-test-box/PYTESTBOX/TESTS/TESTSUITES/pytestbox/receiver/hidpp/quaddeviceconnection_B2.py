#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.receiver.hidpp.equaddeviceconnection_B2
    :brief: Validates HID++ Device Connection and Disconnection registers
    :author: Martin Cryonnet
    :date: 2020/05/12
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
import time

from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.registers.quaddeviceconnection import QuadDeviceConnection
from pyhid.hidpp.hidpp1.registers.quaddeviceconnection import SetQuadDeviceConnectionRequest
from pyhid.hidpp.hidpp1.registers.quaddeviceconnection import SetQuadDeviceConnectionResponse
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetest import ReceiverBaseTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class QuadDeviceConnectionTestCase(ReceiverBaseTestCase):
    """
    Command Set TestCases
    """
    @features('NoRcvUFYEnumeration')
    @level('Functionality')
    def test_quad_device_connection_not_supported(self):
        """
        Validates 0xB2 - Device Connection and Disconnection

        Perform a QUAD or eQUAD device connection setup should not be possible
        """
        # ----------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send Device Connection Open Lock request ')
        # ----------------------------------------------------------------------------
        req = SetQuadDeviceConnectionRequest(
            connect_devices=QuadDeviceConnection.ConnectDevices.OPEN_LOCK,
            device_number=0x00,
            open_lock_timeout=QuadDeviceConnection.OpenLockTimeout.USE_DEFAULT
        )

        self.send_report_to_device(req)
        time.sleep(0.5)
        resp = self.clean_message_type_in_queue(self.hidDispatcher.receiver_response_queue,
                                                SetQuadDeviceConnectionResponse)
        err_resp = self.clean_message_type_in_queue(self.hidDispatcher.receiver_error_message_queue, Hidpp1ErrorCodes)

        # ----------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check no valid response is received')
        # ----------------------------------------------------------------------------
        self.assertListEqual(resp, [], f'QUAD or eQUAD Device Connection request should not be accepted')

        # ----------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Check error message returned by the device')
        # ----------------------------------------------------------------------------
        self.assertGreater(len(err_resp), 0, f'QUAD or eQUAD Device Connection request should raise an error')
        self.assertTupleEqual(
            (Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER, Hidpp1Data.Hidpp1RegisterAddress.QUAD_DEVICE_CONNECTION),
            (int(Numeral(err_resp[0].command_sub_id)), int(Numeral(err_resp[0].address))),
            f'QUAD or eQUAD Device Connection request should raise an error')

        self.assertEqual(Hidpp1ErrorCodes.ERR_INVALID_ADDRESS, int(err_resp[0].error_code),
                         f'QUAD or eQUAD Device Connection request should raise an ERR_INVALID_ADDRESS error')
    # end def test_quad_device_connection_not_supported
# end class QuadDeviceConnectionTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
