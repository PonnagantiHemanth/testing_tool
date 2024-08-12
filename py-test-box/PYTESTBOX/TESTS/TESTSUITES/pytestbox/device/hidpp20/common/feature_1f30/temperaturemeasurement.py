#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1f30.temperaturemeasurement
:brief: Validate HID++ 2.0 ``TemperatureMeasurement`` feature
:author: Sanjib Hazra <shazra@logitech.com>
:date: 2021/06/07
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.temperaturemeasurementutils import TemperatureMeasurementTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TemperatureMeasurementTestCase(DeviceBaseTestCase):
    """
    Validates ``TemperatureMeasurement`` TestCases in Application mode
    """
    def setUp(self):
        """
        Handles test prerequisites.
        """
        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enable manufacturing features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x1F30 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1f30_index, self.feature_1f30, _, _ = TemperatureMeasurementTestUtils.HIDppHelper.get_parameters(self)
    # end def setUp
# end class TemperatureMeasurementTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
