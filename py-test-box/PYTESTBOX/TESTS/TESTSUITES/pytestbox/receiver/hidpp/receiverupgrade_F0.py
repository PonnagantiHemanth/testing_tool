#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.receiver.hidpp.receiverupgrade_F0
:brief: Validates OTA receiver firmware upgrade feature
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2020/03/02
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pytestbox.base.basetest import ReceiverBaseTestCase
from pyharness.selector import features
from pyharness.extensions import level
from pyharness.core import TYPE_SUCCESS
from pylibrary.tools.numeral import Numeral
from pyhid.hidpp.features.common.dfu import Dfu
from pyhid.hidpp.hidpp1.registers.enterupgrademode import SetEnterUpgradeModeRequest
from pyhid.hidpp.hidpp1.registers.enterupgrademode import GetEnterUpgradeModeRequest
from pyhid.hidpp.hidpp1.registers.enterupgrademode import GetEnterUpgradeModeResponse
from pyhid.hidpp.hidpp1.registers.enterupgrademode import ENTER_USB_UPGRADE_KEY
from pyhid.hidpp.hidpp1.registers.enterupgrademode import APP_STATE_KEY
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.base.dfuutils import DfuTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ReceiverUpgradeTestCase(ReceiverBaseTestCase):
    """
    Receiver Firmware Upgrade TestCases
    """
    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            if self.status != TYPE_SUCCESS:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "The target shall be forced back in Main Application mode")
                # ------------------------------------------------------------------------------------------------------
                DfuTestUtils.force_target_on_application(test_case=self)
            # end if
        # end with
        super().tearDown()
    # end def tearDown

    @features('DfuControlReadCapabilities')
    @level('Functionality')
    def test_read_upgrade_mode(self):
        """
        Validate firmware upgrade mode reading (F0 00)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read upgrade mode")
        # --------------------------------------------------------------------------------------------------------------
        read_upgrade_mode = GetEnterUpgradeModeRequest()
        read_upgrade_mode_response = ChannelUtils.send(self,
                                                       read_upgrade_mode,
                                                       HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                                                       response_class_type=GetEnterUpgradeModeResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate firmware upgrade mode")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=APP_STATE_KEY,
                         obtained=read_upgrade_mode_response.key,
                         msg='The key parameter differs from the one expected')

        self.testCaseChecked("FNT_RCV-F0_0001")
    # end def test_read_upgrade_mode

    @features('DfuControlDfuAvailable')
    @level('Functionality')
    def test_enter_upgrade_mode_accepted(self):
        """
        Validate enter USB firmware upgrade mode using 0xF0 is accepted
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enable HID++ reporting")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.set_hidpp_reporting(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send enter USB firmware upgrade mode request")
        # --------------------------------------------------------------------------------------------------------------
        write_upgrade_mode = SetEnterUpgradeModeRequest(key=ENTER_USB_UPGRADE_KEY)
        ChannelUtils.send_only(self, write_upgrade_mode)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Error code message queue is empty")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(self, HIDDispatcher.QueueName.RECEIVER_ERROR, timeout=.4)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wait for USB disconnection and reconnection")
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Root.GetFeature(0x00D0)")
        # --------------------------------------------------------------------------------------------------------------
        self.bootloader_dfu_feature_id = ChannelUtils.update_feature_mapping(self, Dfu.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Restart function to jump back on application")
        # --------------------------------------------------------------------------------------------------------------
        DfuTestUtils.send_dfu_restart_function(test_case=self,
                                               bootloader_dfu_feature_id=self.bootloader_dfu_feature_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Enable HID++ reporting")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.set_hidpp_reporting(self)

        self.testCaseChecked("FNT_RCV-F0_0002")
    # end def test_enter_upgrade_mode_accepted

    @features('NoDfuControl')
    @level('Functionality')
    def test_enter_upgrade_mode_not_accepted(self):
        """
        Validate enter USB firmware upgrade mode using 0xF0 is not accepted
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enable HID++ reporting")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.set_hidpp_reporting(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send enter USB firmware upgrade mode request")
        # --------------------------------------------------------------------------------------------------------------
        write_upgrade_mode = SetEnterUpgradeModeRequest(key=ENTER_USB_UPGRADE_KEY)
        error_response = ChannelUtils.send(
            self, write_upgrade_mode, HIDDispatcher.QueueName.RECEIVER_ERROR, response_class_type=Hidpp1ErrorCodes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, "Verify Hidpp1ErrorCodes received with register = 0xF0 and error_code = 0x01 (ERR_INVALID_SUBID)")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=Hidpp1Data.Hidpp1RegisterAddress.ENTER_FIRMWARE_UPGRADE_MODE,
                         obtained=int(Numeral(error_response.register)),
                         msg="The parameter register differs from the expected one")
        self.assertEqual(expected=Hidpp1ErrorCodes.ERR_INVALID_ADDRESS,
                         obtained=int(Numeral(error_response.error_code)),
                         msg="The parameter error_code differs from the expected one")

        self.testCaseChecked("FNT_RCV-F0_0003")
    # end def test_enter_upgrade_mode_not_accepted
# end class ReceiverUpgradeTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
