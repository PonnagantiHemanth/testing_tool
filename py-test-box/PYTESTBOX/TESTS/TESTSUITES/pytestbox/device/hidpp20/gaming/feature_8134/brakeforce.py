#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_8134.brakeforce
:brief: Validate HID++ 2.0 ``BrakeForce`` feature
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/02/26
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.brakeforceutils import BrakeForceTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BrakeForceTestCase(DeviceBaseTestCase):
    """
    Validate ``BrakeForce`` TestCases in Application mode
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
        LogHelper.log_prerequisite(self, "Get feature 0x8134 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_8134_index, self.feature_8134, _, _ = BrakeForceTestUtils.HIDppHelper.get_parameters(self)

        self.config = self.f.PRODUCT.FEATURES.GAMING.BRAKE_FORCE
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites
        """
        # noinspection PyBroadException
        try:
            if self.post_requisite_reload_nvs:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.NvsHelper.restore_nvs(self)
                self.post_requisite_reload_nvs = False
            # end if
        except Exception:
            self.log_traceback_as_warning(supplementary_message="Exception in tearDown:")
        finally:
            super().tearDown()
        # end try
    # end def tearDown
# end class BrakeForceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
