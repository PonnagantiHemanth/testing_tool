#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.receiver.tde.prepairing
:brief: Validate BLE Pro Prepairing
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/06/11
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hidpp.hidpp1.registers.testmodecontrol import TestModeControl
from pylibrary.tools.hexlist import HexList
from pytestbox.base.basetest import ReceiverBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.tdeutils import TDETestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class PrepairingTestCase(ReceiverBaseTestCase):
    """
    Prepairing TestCases
    """
    def setUp(self):
        """
        Handle test prerequisites
        """
        self.post_requisite_reset_receiver = False

        super().setUp()

        # Define test values
        self.prepairing_slot = 0x02
        self.device_address = HexList('123456789ABC')
        self.ltk_key = HexList('000102030405060708090A0B0C0D0E0F')
        self.irk_local_key = HexList('101112131415161718191A1B1C1D1E1F')
        self.irk_remote_key = HexList('202122232425262728292A2B2C2D2E2F')
        self.csrk_local_key = HexList('303132333435363738393A3B3C3D3E3F')
        self.csrk_remote_key = HexList('404142434445464748494A4B4C4D4E4F')

        ReceiverTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
    # end def setUp

    def tearDown(self):
        """
        Handles test post requisites
        """
        with self.manage_post_requisite():
            TDETestUtils.set_test_mode_control(self, TestModeControl.TestModeEnable.DISABLE_TEST_MODE)
            DevicePairingTestUtils.NvsManager.clean_pairing_data(self)
        # end with
        with self.manage_post_requisite():
            if self.post_requisite_reset_receiver and self.receiver_debugger is not None:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Reset the receiver')
                # ------------------------------------------------------------------------------------------------------
                self.receiver_debugger.reset(soft_reset=False)
            # end if
        # end with
        super().tearDown()
    # end def tearDown
# end class PrepairingTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
