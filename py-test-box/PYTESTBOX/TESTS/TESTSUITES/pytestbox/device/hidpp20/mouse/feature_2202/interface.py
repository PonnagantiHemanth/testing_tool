#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.mouse.feature_2202.interface
:brief: HID++ 2.0 ``ExtendedAdjustableDpi`` interface test suite
:author: Fred Chen <fchen7@logitech.com>
:date: 2022/06/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pyhid.hidpp.features.mouse.extendedadjustabledpi import ExtendedAdjustableDpi
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.extendedadjustabledpiutils import ExtendedAdjustableDpiTestUtils
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytestbox.device.hidpp20.mouse.feature_2202.extendedadjustabledpi import ExtendedAdjustableDpiTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Fred Chen"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ExtendedAdjustableDpiInterfaceTestCase(ExtendedAdjustableDpiTestCase):
    """
    Validate ``ExtendedAdjustableDpi`` interface test cases
    """

    @features("Feature2202")
    @level("Interface")
    def test_get_sensor_count(self):
        """
        Validate ``GetSensorCount`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetSensorCount request")
        # --------------------------------------------------------------------------------------------------------------
        response = ExtendedAdjustableDpiTestUtils.HIDppHelper.get_sensor_count(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetSensorCountResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.GetSensorCountResponseChecker.check_fields(
            self, response, self.feature_2202.get_sensor_count_response_cls)

        self.testCaseChecked("INT_2202_0001", _AUTHOR)
    # end def test_get_sensor_count

    @features("Feature2202")
    @level("Interface")
    def test_get_sensor_capabilities(self):
        """
        Validate ``GetSensorCapabilities`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetSensorCapabilities request with sensor_idx = 0")
        # --------------------------------------------------------------------------------------------------------------
        response = ExtendedAdjustableDpiTestUtils.HIDppHelper.get_sensor_capabilities(test_case=self, sensor_idx=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetSensorCapabilitiesResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.GetSensorCapabilitiesResponseChecker.check_fields(
            self, response, self.feature_2202.get_sensor_capabilities_response_cls)

        self.testCaseChecked("INT_2202_0002", _AUTHOR)
    # end def test_get_sensor_capabilities

    @features("Feature2202")
    @level("Interface")
    def test_get_sensor_dpi_ranges(self):
        """
        Validate ``GetSensorDpiRanges`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Send GetSensorDpiRanges request with sensor_idx = 0, direction = X, dpi_range_req_idx = 0")
        # --------------------------------------------------------------------------------------------------------------
        response = ExtendedAdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi_ranges(
            test_case=self, sensor_idx=0, direction=ExtendedAdjustableDpi.Direction.X, dpi_range_req_idx=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetSensorDpiRangesResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.GetSensorDpiRangesResponseChecker.check_fields(
            self, response, self.feature_2202.get_sensor_dpi_ranges_response_cls)

        self.testCaseChecked("INT_2202_0003", _AUTHOR)
    # end def test_get_sensor_dpi_ranges

    @features("Feature2202")
    @features("ProfileSupported")
    @level("Interface")
    def test_get_sensor_dpi_list(self):
        """
        Validate ``GetSensorDpiList`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetSensorDpiList request with sensor_idx = 0, direction = X")
        # --------------------------------------------------------------------------------------------------------------
        response = ExtendedAdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi_list(
            test_case=self, sensor_idx=0, direction=ExtendedAdjustableDpi.Direction.X)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetSensorDpiListResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.GetSensorDpiListResponseChecker.check_fields(
            self, response, self.feature_2202.get_sensor_dpi_list_response_cls)

        self.testCaseChecked("INT_2202_0004", _AUTHOR)
    # end def test_get_sensor_dpi_list

    @features("Feature2202")
    @features("ProfileSupported")
    @level("Interface")
    def test_get_sensor_lod_list(self):
        """
        Validate ``GetSensorLodList`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetSensorLodList request with sensor_idx = 0")
        # --------------------------------------------------------------------------------------------------------------
        response = ExtendedAdjustableDpiTestUtils.HIDppHelper.get_sensor_lod_list(test_case=self, sensor_idx=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetSensorLodListResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.GetSensorLodListResponseChecker.check_fields(
            self, response, self.feature_2202.get_sensor_lod_list_response_cls)

        self.testCaseChecked("INT_2202_0005", _AUTHOR)
    # end def test_get_sensor_lod_list

    @features("Feature2202")
    @level("Interface")
    def test_get_sensor_dpi_parameters(self):
        """
        Validate ``GetSensorDpiParameters`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetSensorDpiParameters request with sensor_idx = 0")
        # --------------------------------------------------------------------------------------------------------------
        response = ExtendedAdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi_parameters(test_case=self, sensor_idx=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetSensorDpiParametersResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.GetSensorDpiParametersResponseChecker.check_fields(
            self, response, self.feature_2202.get_sensor_dpi_parameters_response_cls)

        self.testCaseChecked("INT_2202_0006", _AUTHOR)
    # end def test_get_sensor_dpi_parameters

    @features("Feature2202")
    @features("Feature8100")
    @level("Interface")
    def test_set_sensor_dpi_parameters(self):
        """
        Validate ``SetSensorDpiParameters`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Send SetSensorDpiParameters request with sensor_idx = 0 and set DPI and Lod with default settings")
        # --------------------------------------------------------------------------------------------------------------
        response = ExtendedAdjustableDpiTestUtils.HIDppHelper.set_sensor_dpi_parameters(
            test_case=self,
            sensor_idx=0,
            dpi_x=self.config.F_DefaultDpiX,
            dpi_y=self.config.F_DefaultDpiY,
            lod=self.config.F_DefaultLod)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetSensorDpiParametersResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.SetSensorDpiParametersResponseChecker.check_fields(
            self, response, self.feature_2202.set_sensor_dpi_parameters_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetSensorDpiParametersEvent is received")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.sensor_dpi_parameters_event(test_case=self)

        self.testCaseChecked("INT_2202_0007", _AUTHOR)
    # end def test_set_sensor_dpi_parameters

    @features("Feature2202")
    @features("Feature8100")
    @level("Interface")
    def test_show_sensor_dpi_status(self):
        """
        Validate ``ShowSensorDpiStatus`` interface
        """
        default_dpi_level = self.config_manager.get_feature(
            ConfigurationManager.ID.OOB_PROFILES_DEFAULT_DPI_INDEX)[0] + 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ShowSensorDpiStatus request with sensor_idx = 0, "
                                 f"dpi_level={default_dpi_level}, led_hold_type=0, button_num=0")
        # --------------------------------------------------------------------------------------------------------------
        response = ExtendedAdjustableDpiTestUtils.HIDppHelper.show_sensor_dpi_status(
            test_case=self,
            sensor_idx=0,
            dpi_level=default_dpi_level,
            led_hold_type=ExtendedAdjustableDpi.LedHoldType.TIMER_BASED,
            button_num=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ShowSensorDpiStatusResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.ShowSensorDpiStatusResponseChecker.check_fields(
            self, response, self.feature_2202.show_sensor_dpi_status_response_cls)

        self.testCaseChecked("INT_2202_0008", _AUTHOR)
    # end def test_show_sensor_dpi_status

    @features("Feature2202")
    @features("Feature8100")
    @features("DpiCalibrationSupported")
    @level("Interface")
    def test_get_dpi_calibration_info(self):
        """
        Validate ``GetDpiCalibrationInfo`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetDpiCalibrationInfo request with sensor_idx = 0")
        # --------------------------------------------------------------------------------------------------------------
        response = ExtendedAdjustableDpiTestUtils.HIDppHelper.get_dpi_calibration_info(test_case=self, sensor_idx=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetDpiCalibrationInfoResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.GetDpiCalibrationInfoResponseChecker.check_fields(
            self, response, self.feature_2202.get_dpi_calibration_info_response_cls)

        self.testCaseChecked("INT_2202_0009", _AUTHOR)
    # end def test_get_dpi_calibration_info

    @features("Feature2202")
    @features("Feature8100")
    @features("DpiCalibrationSupported")
    @level("Interface")
    def test_start_dpi_calibration(self):
        """
        Validate ``StartDpiCalibration`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send StartDpiCalibration request")
        # --------------------------------------------------------------------------------------------------------------
        expected_count = ExtendedAdjustableDpiTestUtils.compute_expected_count(
            self, ExtendedAdjustableDpi.Direction.X, self.config.F_MouseLength)
        response = ExtendedAdjustableDpiTestUtils.HIDppHelper.start_dpi_calibration(
            test_case=self,
            sensor_idx=0,
            direction=ExtendedAdjustableDpi.Direction.X,
            expected_count=expected_count,
            calib_type=ExtendedAdjustableDpi.CalibType.HW,
            calib_start_timeout=0,
            calib_hw_process_timeout=0,
            calib_sw_process_timeout=0
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check StartDpiCalibrationResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ExtendedAdjustableDpiTestUtils.StartDpiCalibrationResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map['expected_count'] = (checker.check_expected_count, expected_count)
        checker.check_fields(self, response, self.feature_2202.start_dpi_calibration_response_cls, check_map)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetSensorDpiParametersEvent is received")
        # ----------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.dpi_calibration_completed_event(test_case=self)

        self.testCaseChecked("INT_2202_0010", _AUTHOR)
    # end def test_start_dpi_calibration

    @features("Feature2202")
    @features("Feature8100")
    @features("DpiCalibrationSupported")
    @level("Interface")
    def test_set_dpi_calibration(self):
        """
        Validate ``SetDpiCalibration`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetDpiCalibration request with sensor_idx = 0, direction = X, "
                                 "calib_cor = 0x0000 (Revert to OOB)")
        # --------------------------------------------------------------------------------------------------------------
        response = ExtendedAdjustableDpiTestUtils.HIDppHelper.set_dpi_calibration(
            test_case=self,
            sensor_idx=0,
            direction=ExtendedAdjustableDpi.Direction.X,
            calib_cor=ExtendedAdjustableDpi.RevertCommand.TO_OOB_PROFILE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetDpiCalibrationResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.SetDpiCalibrationResponseChecker.check_fields(
            self, response, self.feature_2202.set_dpi_calibration_response_cls)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetSensorDpiParametersEvent is received")
        # ----------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.sensor_dpi_parameters_event(test_case=self)

        self.testCaseChecked("INT_2202_0011", _AUTHOR)
    # end def test_set_dpi_calibration
# end class ExtendedAdjustableDpiInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
