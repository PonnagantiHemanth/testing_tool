#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.mouse.feature_2201.interface
:brief: HID++ 2.0 Adjustable DPI interface test suite
:author: Fred Chen <fchen7@logitech.com>
:date: 2021/06/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.adjustabledpiutils import AdjustableDpiTestUtils
from pytestbox.device.hidpp20.mouse.feature_2201.adjustabledpi import AdjustableDpiTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AdjustableDpiInterfaceTestCase(AdjustableDpiTestCase):
    """
    Validates Adjustable DPI Interface TestCases
    """
    @features('Feature2201')
    @level('Interface')
    def test_get_sensor_count(self):
        """
        Validates getSensorCount interface

        [0] getSensorCount() -> sensorCount
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getSensorCount')
        # --------------------------------------------------------------------------------------------------------------
        get_sensor_count_resp = AdjustableDpiTestUtils.HIDppHelper.get_sensor_count(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate getSensorCount.sensorCount value')
        # --------------------------------------------------------------------------------------------------------------
        AdjustableDpiTestUtils.GetSensorCountResponseChecker.check_fields(
            self, get_sensor_count_resp, self.feature_2201.get_sensor_count_response_cls)

        self.testCaseChecked("INT_2201_0001")
    # end def test_get_sensor_count

    @features('Feature2201')
    @level('Interface')
    def test_get_sensor_dpi_list(self):
        """
        Validates getSensorDpiList interface

        [1] getSensorDpiList(sensorIdx) -> sensorIdx, dpiList
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getSensorDpiList with sensorIdx = 0')
        # --------------------------------------------------------------------------------------------------------------
        get_sensor_dpi_list_resp = AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi_list(self, sensor_idx=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the response data from getSensorDpiList')
        # --------------------------------------------------------------------------------------------------------------
        AdjustableDpiTestUtils.GetSensorDpiListResponseChecker.check_fields(
            self, get_sensor_dpi_list_resp, self.feature_2201.get_sensor_dpi_list_response_cls)

        self.testCaseChecked("INT_2201_0002")
    # end def test_get_sensor_dpi_list

    @features('Feature2201')
    @level('Interface')
    def test_get_sensor_dpi(self):
        """
        Validates getSensorDpi interface

        v0
            [2] getSensorDpi(sensorIdx) -> sensorIdx, dpi
        v1~v2
            [2] getSensorDpi(sensorIdx) -> sensorIdx, dpi, defaultDpi
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getSensorDpi with sensorIdx = 0')
        # --------------------------------------------------------------------------------------------------------------
        get_sensor_dpi_resp = AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self, sensor_idx=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the response data from getSensorDpi')
        # --------------------------------------------------------------------------------------------------------------
        AdjustableDpiTestUtils.GetSensorDpiResponseChecker.check_fields(
            self, get_sensor_dpi_resp, self.feature_2201.get_sensor_dpi_response_cls)

        self.testCaseChecked("INT_2201_0003")
    # end def test_get_sensor_dpi

    @features('Feature2201')
    @level('Interface')
    @bugtracker('Footloose_SetDpiForEachSensor_Dpi')
    def test_set_sensor_dpi(self):
        """
        Validates setSensorDpi interface

        v0
            [3] setSensorDpi(sensorIdx, dpi)
        v1
            [3] setSensorDpi(sensorIdx, dpi) -> sensorIdx, dpi
        v2
            [3] setSensorDpi(sensorIdx, dpi, dpiLevel) -> sensorIdx, dpi, dpiLevel
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setSensorDpi with dpi=defaultDpi and set 0 to the other fields')
        # --------------------------------------------------------------------------------------------------------------
        set_sensor_dpi_resp = AdjustableDpiTestUtils.HIDppHelper.set_sensor_dpi(
                self, sensor_idx=0, dpi=self.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI.F_DpiDefault, dpi_level=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the response data from setSensorDpi')
        # --------------------------------------------------------------------------------------------------------------
        AdjustableDpiTestUtils.SetSensorDpiResponseChecker.check_fields(
            self, set_sensor_dpi_resp, self.feature_2201.set_sensor_dpi_response_cls)

        self.testCaseChecked("INT_2201_0004")
    # end def test_set_sensor_dpi

    @features('Feature2201v2+')
    @level('Interface')
    def test_get_number_of_dpi_levels(self):
        """
        Validate getNumberofDpiLevels interface

        v2
            [4] getNumberofDpiLevels() -> dpiLevels
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getNumerofDpiLevels')
        # --------------------------------------------------------------------------------------------------------------
        get_number_of_dpi_levels_resp = AdjustableDpiTestUtils.HIDppHelper.get_number_of_dpi_levels(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate getNumerofDpiLevels.dpiLevels value')
        # --------------------------------------------------------------------------------------------------------------
        AdjustableDpiTestUtils.GetNumberOfDpiLevelsResponseChecker.check_fields(
            self, get_number_of_dpi_levels_resp, self.feature_2201.get_number_of_dpi_levels_response_cls)

        self.testCaseChecked("INT_2201_0005")
    # end def test_get_number_of_dpi_levels
# end class AdjustableDpiInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
