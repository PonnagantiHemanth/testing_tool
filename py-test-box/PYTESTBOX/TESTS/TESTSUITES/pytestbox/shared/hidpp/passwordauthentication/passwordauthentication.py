#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.shared.hidpp.passwordauthentication.passwordauthentication
:brief: Shared test case for the validation of Password Authentication
        (HID++ 2.0 common feature 0x1602 and
        HID++ 1.0 registers 0xF7 & 0xF8)
:author: Gautham S B <gsb@logitech.com>
:date: 2022/10/17
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC

from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuth
from pylibrary.tools.hexlist import HexList
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class SharedPasswordAuthenticationTestCase(CommonBaseTestCase, ABC):
    """
    Validates Password Authentication TestCases on receiver/device
    """
    ManageUtils = None
    PasswordAuthenticationTestUtils = None

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.post_requisite_reload_nvs = False
        self.post_requisite_reset_receiver = False

        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Read initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.NvsHelper.backup_nvs(self)

        x1e02_state_chunks = self.memory_manager.get_chunks_by_name("NVS_X1E02_STATE_ID")
        if x1e02_state_chunks and HexList(x1e02_state_chunks[-1]) != HexList(0x00):
            self.post_requisite_reload_nvs = True
            state = ManageDeactivatableFeaturesAuth.BitMap(manufacturing=0, compliance=0, gothard=0)
            self.ManageUtils.NvsHelper.force_state(self, state)
        # end if
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites
        """
        with self.manage_post_requisite():
            if self.post_requisite_reload_nvs:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                CommonBaseTestUtils.NvsHelper.restore_nvs(self)
            # end if
        # end with
        with self.manage_post_requisite():
            if self.post_requisite_reset_receiver:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Reset the receiver')
                # ------------------------------------------------------------------------------------------------------
                ReceiverTestUtils.reset_receiver(self, skip_link_established_verification=True)
            # end if
        # end with
        super().tearDown()
    # end def tearDown
# end class SharedPasswordAuthenticationTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
