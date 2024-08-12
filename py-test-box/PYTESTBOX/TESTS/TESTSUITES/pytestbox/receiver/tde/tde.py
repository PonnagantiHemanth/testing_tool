#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.receiver.tde.tde
:brief: Validates TDE sequence
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/05/12
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hidpp.hidpp1.registers.rfregisteraccess import RFRegisterAccess
from pyhid.hidpp.hidpp1.registers.testmodecontrol import TestModeControl
from pytestbox.base.basetest import ReceiverBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.shared.base.tdeutils import TDETestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class TDETestCase(ReceiverBaseTestCase):
    """
    TDE TestCases
    """
    def setUp(self):
        """
        Creates the test context of selected plug-in.
        """
        self.post_requisite_disable_rf = False

        # Inherited setup
        super().setUp()
    # end setUp

    def tearDown(self):
        """
        Handles test post-requisites.
        """
        # noinspection PyBroadException
        try:
            # Disable Test Mode
            ReceiverTestUtils.HIDppHelper.activate_features(test_case=self, manufacturing=True)
            # Disable RF Test Mode
            if self.post_requisite_disable_rf:
                TDETestUtils.set_rf_test_mode_enable(self, RFRegisterAccess.TestModeEnableDisable.RF_OFF)
            # end if
            TDETestUtils.set_test_mode_control(self, TestModeControl.TestModeEnable.DISABLE_TEST_MODE)

            # Clear TDE data in NVS
            if self.memory_manager is not None:
                self.memory_manager.read_nvs()
                self.memory_manager.invalidate_chunks(["NVS_TDE_MFG_ACCESS_ID",])
                CommonBaseTestUtils.load_nvs(self)
            # end if
        except Exception:
            self.log_traceback_as_warning(supplementary_message="Exception in tearDown:")
        finally:
            super().tearDown()
    # end def tearDown
# end class TDETestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
