#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.mouse.feature_2130.ratchetwheel
:brief: Validate HID++ 2.0 ``RatchetWheel`` feature
:author: Gautham S B <gsb@logitech.com>
:date: 2022/11/30
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.ratchetwheelutils import RatchetWheelTestUtils
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class RatchetWheelTestCase(DeviceBaseTestCase):
    """
    Validate ``RatchetWheel`` TestCases in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Post requisite flags definition
        self.post_requisite_unpair_all = False
        self.post_requisite_reload_nvs = False
        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.NvsHelper.backup_nvs(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x2130 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_2130_index, self.feature_2130, self.device_index, _ = \
            RatchetWheelTestUtils.HIDppHelper.get_parameters(self)
        self.config = self.f.PRODUCT.FEATURES.MOUSE.RATCHET_WHEEL

    def tearDown(self):
        """
        Handle test post-requisites
        """
        with self.manage_post_requisite():
            if self.post_requisite_unpair_all:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Clean receiver pairing information")
                # ------------------------------------------------------------------------------------------------------
                DevicePairingTestUtils.unpair_all(self)
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_reload_nvs:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.NvsHelper.restore_nvs(self)
            # end if
        # end with
        super().tearDown()
    # end def tearDown
# end class RatchetWheelTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
