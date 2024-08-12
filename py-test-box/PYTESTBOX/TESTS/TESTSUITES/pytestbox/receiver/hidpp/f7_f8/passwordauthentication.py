#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.hidpp.f7_f8.passwordauthentication
:brief: Validate HID++ 1.0 ``PasswordAuthentication`` feature
:author: Gautham S B <gsb@logitech.com>
:date: 2022/10/17
"""

# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hidpp.hidpp1.registers.testmodecontrol import TestModeControl
from pytestbox.base.basetest import ReceiverBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.receiver.base.passwordauthenticationutils import ReceiverPasswordAuthenticationTestUtils
from pytestbox.receiver.base.receivermanagedeactivatablefeaturesauthutils import \
    ReceiverManageDeactivatableFeaturesAuthTestUtils
from pytestbox.shared.base.tdeutils import TDETestUtils
from pytestbox.shared.hidpp.passwordauthentication.passwordauthentication import SharedPasswordAuthenticationTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ReceiverPasswordAuthenticationTestCase(SharedPasswordAuthenticationTestCase, ReceiverBaseTestCase):
    """
    Validate ``PasswordAuthentication`` TestCases in Application mode with a receiver as DUT
    """
    ManageUtils = ReceiverManageDeactivatableFeaturesAuthTestUtils
    PasswordAuthenticationTestUtils = ReceiverPasswordAuthenticationTestUtils

    def setUp(self):
        """
        Handle test prerequisites.
        """
        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enable Test Mode Control")
        # --------------------------------------------------------------------------------------------------------------
        TDETestUtils.set_check_test_mode(
            test_case=self, test_mode_enable=TestModeControl.TestModeEnable.ENABLE_MANUFACTURING_TEST_MODE)
    # end def setUp
# end class ReceiverPasswordAuthenticationTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
