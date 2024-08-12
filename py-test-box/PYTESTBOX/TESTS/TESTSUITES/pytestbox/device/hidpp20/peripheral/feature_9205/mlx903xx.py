#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.peripheral.feature_9205.mlx903xx
:brief: Validate HID++ 2.0 ``MLX903xx`` feature
:author: Gautham S B <gsb@logitech.com>
:date: 2023/03/02
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.mlx903xxutils import MLX903xxTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class MLX903xxTestCase(DeviceBaseTestCase):
    """
    Validate ``MLX903xx`` TestCases in Application mode
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
        LogHelper.log_prerequisite(self, "Activate features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x9205 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_9205_index, self.feature_9205, _, _ = MLX903xxTestUtils.HIDppHelper.get_parameters(
            test_case=self)

        self.config = self.f.PRODUCT.FEATURES.PERIPHERAL.MLX903XX
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Power reset Target DUT")
        # --------------------------------------------------------------------------------------------------------------
        MLX903xxTestUtils.ResetHelper.hardware_reset(self)

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
# end class MLX903xxTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
