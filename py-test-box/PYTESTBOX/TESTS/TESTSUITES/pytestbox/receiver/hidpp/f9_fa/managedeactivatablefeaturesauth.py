#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.receiver.hidpp.f9_fa.managedeactivatablefeaturesauth
:brief: Validates HID++ 1.0 Manage Deactivatable Features with authentication (0xF9 & 0xFA)
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2021/02/19
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hidpp.hidpp1.registers.testmodecontrol import TestModeControl
from pytestbox.base.basetest import ReceiverBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.receiver.base.passwordauthenticationutils import ReceiverPasswordAuthenticationTestUtils
from pytestbox.receiver.base.receivermanagedeactivatablefeaturesauthutils import \
    ReceiverManageDeactivatableFeaturesAuthTestUtils
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.shared.base.tdeutils import TDETestUtils
from pytestbox.shared.hidpp.managedeactivatablefeaturesauth.managedeactivatablefeaturesauth import \
    SharedManageDeactivatableFeaturesAuthTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ReceiverManageDeactivatableFeaturesAuthTestCase(SharedManageDeactivatableFeaturesAuthTestCase,
                                                      ReceiverBaseTestCase):
    """
    Validate the Manage deactivatable features mechanism based on authentication TestCases with a receiver as a DUT
    """
    ManageDeactivatableFeaturesAuthTestUtils = ReceiverManageDeactivatableFeaturesAuthTestUtils
    PasswordAuthenticationTestUtils = ReceiverPasswordAuthenticationTestUtils
    TestUtilsFacade = ReceiverTestUtils

    def setUp(self):
        """
        Handles test prerequisites.
        """
        super().setUp()

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, 'Enable Test Mode Control')
        # ---------------------------------------------------------------------------
        TDETestUtils.set_check_test_mode(
            self, test_mode_enable=TestModeControl.TestModeEnable.ENABLE_MANUFACTURING_TEST_MODE)
    # end def setUp
# end class ReceiverManageDeactivatableFeaturesAuthTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
