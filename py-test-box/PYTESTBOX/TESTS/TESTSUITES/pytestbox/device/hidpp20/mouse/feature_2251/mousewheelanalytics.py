#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.mouse.feature_2251.mousewheelanalytics
:brief: Validate HID++ 2.0 ``MouseWheelAnalytics`` feature
:author: Gautham S B <gsb@logitech.com>
:date: 2023/10/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hidpp.features.mouse.mousewheelanalytics import MouseWheelAnalytics
from pyhid.hidpp.features.mouse.smartshift import SetRatchetControlMode
from pyhid.hidpp.features.mouse.smartshift import SmartShift
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.mousewheelanalyticsutils import MouseWheelAnalyticsTestUtils
from pytestbox.device.base.smartshiftunableutils import SmartShiftTunableTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class MouseWheelAnalyticsTestCase(DeviceBaseTestCase):
    """
    Validate ``MouseWheelAnalytics`` TestCases in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()

        self.post_requisite_set_wheel_to_ratchet_mode = False
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x2251 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_2251_index, self.feature_2251, self.device_index, _ = MouseWheelAnalyticsTestUtils.HIDppHelper.\
            get_parameters(test_case=self)

        self.config = self.f.PRODUCT.FEATURES.MOUSE.MOUSE_WHEEL_ANALYTICS
    # end def setUp

    def tearDown(self):
        """
        Handle test postrequisites
        """
        with self.manage_post_requisite():
            if self.post_requisite_set_wheel_to_ratchet_mode:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Set main wheel to ratchet mode if DUT supports '
                                                   'feature 0x2110 or 0x2111')
                # ------------------------------------------------------------------------------------------------------
                self.set_wheel_mode(MouseWheelAnalytics.WheelMode.RATCHET)
                self.post_requisite_set_wheel_to_ratchet_mode = False
            # end if
        # end with

        super().tearDown()
    # end def tearDown

    def set_wheel_mode(self, wheel_mode):
        """
        Set the main wheel mode (ratchet/freespin) for DUT's that support feature 0x2110 or feature 0x2111

        :param wheel_mode: The wheel mode
        :type wheel_mode: ``MouseWheelAnalytics.WheelMode``

        :raise ``AssertionError``: Assert wheel_mode class type that raise an exception
        """
        assert isinstance(wheel_mode, MouseWheelAnalytics.WheelMode)
        if self.f.PRODUCT.FEATURES.MOUSE.SMART_SHIFT:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Set wheel to {wheel_mode.name} mode")
            # ----------------------------------------------------------------------------------------------------------
            feature_2110_index = ChannelUtils.update_feature_mapping(
                test_case=self, feature_id=SmartShift.FEATURE_ID)
            SetRatchetControlMode(device_index=self.device_index, feature_index=feature_2110_index,
                                  wheel_mode=int(Numeral(wheel_mode)))
        elif self.f.PRODUCT.FEATURES.MOUSE.SMART_SHIFT_TUNABLE:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Set wheel to {wheel_mode.name} mode")
            # ----------------------------------------------------------------------------------------------------------
            SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode(self, wheel_mode=wheel_mode)
        else:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "DUT does not support feature 0x2110 or 0x2111, Skipping this step")
            # ----------------------------------------------------------------------------------------------------------
        # end if
    # end def set_wheel_mode
# end class MouseWheelAnalyticsTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
