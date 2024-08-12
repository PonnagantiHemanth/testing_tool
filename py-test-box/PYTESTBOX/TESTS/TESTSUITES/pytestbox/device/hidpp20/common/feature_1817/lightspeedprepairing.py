#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.common.feature_1817.lightspeedprepairing
:brief: Validate HID++ 2.0 ``LightspeedPrepairing`` feature
:author: Zane Lu <zlu@logitech.com>
:date: 2022/06/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hidpp.features.common.lightspeedprepairing import PrepairingManagement
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.lightspeedprepairingutils import LightspeedPrepairingTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LightspeedPrepairingTestCase(DeviceBaseTestCase):
    """
    Validate ``LightspeedPrepairing`` TestCases in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enable manufacturing features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x1817 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1817_index, self.feature_1817, _, _ = LightspeedPrepairingTestUtils.HIDppHelper.get_parameters(self)

        self.config = self.f.PRODUCT.FEATURES.COMMON.LIGHTSPEED_PREPAIRING
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites
        """
        # noinspection PyBroadException
        with self.manage_post_requisite():
            if self.post_requisite_reload_nvs:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.NvsHelper.restore_nvs(self)
                self.post_requisite_reload_nvs = False
            # end if
        # end with

        super().tearDown()
    # end def tearDown

    def _test_get_the_first_available_slot(self):
        """
        Get the first available slot from the settings

        :return: The first available slot from the settings
        :rtype: ``PrepairingManagement.PairingSlot``

        :raise: ``AssertionError`` If there is no available slot found in the settings of LIGHTSPEED_PREPAIRING
        """
        for slot_availability, slot in zip((self.config.F_Ls2Slot, self.config.F_LsSlot, self.config.F_CrushSlot,),
                                           (PrepairingManagement.PairingSlot.LS2, PrepairingManagement.PairingSlot.LS,
                                            PrepairingManagement.PairingSlot.CRUSH)):
            if slot_availability:
                return slot
            # end if
        # end for

        raise AssertionError("There is no available slot found in the settings.")
    # end _test_get_the_first_available_slot
# end class LightspeedPrepairingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
