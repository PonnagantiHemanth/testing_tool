#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.peripheral.feature_92e2.testkeysdisplay
:brief: Validate HID++ 2.0 ``TestKeysDisplay`` feature
:author: Gautham S B <gsb@logitech.com>
:date: 2024/04/02
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.testkeysdisplayutils import TestKeysDisplayTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class TestKeysDisplayTestCase(DeviceBaseTestCase):
    """
    Validate ``TestKeysDisplay`` TestCases in Application mode
    """
    BLACK = "000000"
    BLUE = "0000FF"
    GREEN = "00FF00"
    RED = "FF0000"
    WHITE = "FFFFFF"
    DEFAULT_VALUE_COUNT = 5
    MAX_DUTY_PWM = 1000
    MIN_DUTY_PWM = 0
    POWER_OFF = 0
    POWER_ON = 1

    def setUp(self):
        """
        Handle test prerequisites
        """
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
        LogHelper.log_prerequisite(self, "Get feature 0x92E2 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_92e2_index, self.feature_92e2, self.device_index, _ = (
            TestKeysDisplayTestUtils.HIDppHelper.get_parameters(test_case=self))

        self.config = self.f.PRODUCT.FEATURES.PERIPHERAL.TEST_KEYS_DISPLAY
        self.key_matrix = TestKeysDisplayTestUtils.create_key_matrix(self)
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
                DeviceTestUtils.NvsHelper.restore_nvs(self)
                self.post_requisite_reload_nvs = False
            # end if
        # end with
        super().tearDown()
    # end def tearDown
# end class TestKeysDisplayTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
