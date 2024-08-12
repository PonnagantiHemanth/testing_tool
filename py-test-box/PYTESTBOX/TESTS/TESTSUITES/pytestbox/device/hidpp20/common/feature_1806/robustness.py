#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1806.robustness
:brief: HID++ 2.0 ConfigurableDeviceProperties robustness test suite
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/04/28
"""

# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.device.hidpp20.common.feature_1806.configurabledeviceproperties import \
    ConfigurableDevicePropertiesTestCase

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
_AUTHOR = "Suresh Thiyagarajan"
LogHelper = CommonBaseTestUtils.LogHelper


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ConfigurableDevicePropertiesRobustnessTestCase(ConfigurableDevicePropertiesTestCase):
    """
    Validates ConfigurableDeviceProperties robustness test cases
    """
    @features("Feature1806")
    @level("Robustness")
    def test_software_id(self):
        """
        Validates software index
        """
        request_cls = self.feature_1806.get_device_name_max_count_cls
        for software_id in compute_inf_values(request_cls.DEFAULT.SOFTWARE_ID):
            # --------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetDeviceNameMaxCount request with software_id:{software_id}")
            # --------------------------------------------------------------------------------------------
            report = request_cls(self.deviceIndex, self.feature_1806_index)
            report.softwareId = software_id
            response = self.send_report_wait_response(
                    report=report,
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=self.feature_1806.get_device_name_max_count_response_cls)
            # -----------------------------------------------------------------
            LogHelper.log_check(self, "Check softwareId in its validity range")
            # -----------------------------------------------------------------
            self.assertEqual(expected=report.softwareId,
                             obtained=response.softwareId,
                             msg="The softwareId parameter differs from the one expected")
        # end for
        self.testCaseChecked("ROB_1806_0001", _AUTHOR)
    # end def test_software_id

    @features("Feature1806")
    @level("Robustness")
    def test_padding(self):
        """
        Validates padding
        """
        request_cls = self.feature_1806.get_device_name_max_count_cls
        expected_value = HexList(self.f.PRODUCT.FEATURES.COMMON.CONFIGURABLE_DEVICE_PROPERTIES.F_DeviceNameMaxCount)
        for padding_value in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING,
                                                              request_cls.LEN.PADDING // 8))):
            # ------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetDeviceNameMaxCount request with padding_value:{padding_value}")
            # ------------------------------------------------------------------------------------------------
            report = request_cls(self.deviceIndex, self.feature_1806_index)
            report.padding = padding_value
            response = self.send_report_wait_response(
                    report=report,
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=self.feature_1806.get_device_name_max_count_response_cls)

            # --------------------------------------------------------------------
            LogHelper.log_check(self, "Check padding_value in its validity range")
            # --------------------------------------------------------------------
            self.assertEqual(expected=expected_value,
                             obtained=response.device_name_max_count,
                             msg="The device_name_max_count parameter differs from the one expected")
        # end for
        self.testCaseChecked("ROB_1806_0002", _AUTHOR)
    # end def test_padding
# end class ConfigurableDevicePropertiesRobustnessTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
