#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.mouse.feature_2202.robustness
:brief: HID++ 2.0 ``ExtendedAdjustableDpi`` robustness test suite
:author: Fred Chen <fchen7@logitech.com>
:date: 2022/06/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pyhid.hidpp.features.mouse.extendedadjustabledpi import ExtendedAdjustableDpi
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.extendedadjustabledpiutils import ExtendedAdjustableDpiTestUtils
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytestbox.device.hidpp20.mouse.feature_2202.extendedadjustabledpi import ExtendedAdjustableDpiTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Fred Chen"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ExtendedAdjustableDpiRobustnessTestCase(ExtendedAdjustableDpiTestCase):
    """
    Validate ``ExtendedAdjustableDpi`` robustness test cases
    """

    @features("Feature2202")
    @level("Robustness")
    def test_get_sensor_count_software_id(self):
        """
        Validate ``GetSensorCount`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ExtendedAdjustableDpi.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetSensorCount request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_2202.get_sensor_count_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2202_index)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2202.get_sensor_count_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetSensorCountResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.GetSensorCountResponseChecker.check_fields(
                self, response, self.feature_2202.get_sensor_count_response_cls)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2202_0001#1", _AUTHOR)
    # end def test_get_sensor_count_software_id

    @features("Feature2202")
    @level("Robustness")
    def test_get_sensor_capabilities_software_id(self):
        """
        Validate ``GetSensorCapabilities`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.SensorIdx.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        sensor_idx = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ExtendedAdjustableDpi.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetSensorCapabilities request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_2202.get_sensor_capabilities_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2202_index,
                sensor_idx=sensor_idx)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2202.get_sensor_capabilities_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetSensorCapabilitiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.GetSensorCapabilitiesResponseChecker.check_fields(
                self, response, self.feature_2202.get_sensor_capabilities_response_cls)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2202_0001#2", _AUTHOR)
    # end def test_get_sensor_capabilities_software_id

    @features("Feature2202")
    @level("Robustness")
    def test_get_sensor_dpi_ranges_software_id(self):
        """
        Validate ``GetSensorDpiRanges`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.SensorIdx.Direction.DpiRangeReqIdx

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        sensor_idx = 0
        direction = ExtendedAdjustableDpi.Direction.X
        dpi_range_req_idx = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ExtendedAdjustableDpi.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetSensorDpiRanges request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_2202.get_sensor_dpi_ranges_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2202_index,
                sensor_idx=sensor_idx,
                direction=direction,
                dpi_range_req_idx=dpi_range_req_idx)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2202.get_sensor_dpi_ranges_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetSensorDpiRangesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.GetSensorDpiRangesResponseChecker.check_fields(
                self, response, self.feature_2202.get_sensor_dpi_ranges_response_cls)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2202_0001#3", _AUTHOR)
    # end def test_get_sensor_dpi_ranges_software_id

    @features("Feature2202")
    @level("Robustness")
    def test_get_sensor_dpi_list_software_id(self):
        """
        Validate ``GetSensorDpiList`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.SensorIdx.Direction.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        sensor_idx = 0
        direction = ExtendedAdjustableDpi.Direction.X
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ExtendedAdjustableDpi.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetSensorDpiList request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_2202.get_sensor_dpi_list_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2202_index,
                sensor_idx=sensor_idx,
                direction=direction)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2202.get_sensor_dpi_list_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetSensorDpiListResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.GetSensorDpiListResponseChecker.check_fields(
                self, response, self.feature_2202.get_sensor_dpi_list_response_cls)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2202_0001#4", _AUTHOR)
    # end def test_get_sensor_dpi_list_software_id

    @features("Feature2202")
    @level("Robustness")
    def test_get_sensor_lod_list_software_id(self):
        """
        Validate ``GetSensorLodList`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.SensorIdx.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        sensor_idx = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ExtendedAdjustableDpi.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetSensorLodList request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_2202.get_sensor_lod_list_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2202_index,
                sensor_idx=sensor_idx)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2202.get_sensor_lod_list_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetSensorLodListResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.GetSensorLodListResponseChecker.check_fields(
                self, response, self.feature_2202.get_sensor_lod_list_response_cls)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2202_0001#5", _AUTHOR)
    # end def test_get_sensor_lod_list_software_id

    @features("Feature2202")
    @level("Robustness")
    def test_get_sensor_dpi_parameters_software_id(self):
        """
        Validate ``GetSensorDpiParameters`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.SensorIdx.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        sensor_idx = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ExtendedAdjustableDpi.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetSensorDpiParameters request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_2202.get_sensor_dpi_parameters_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2202_index,
                sensor_idx=sensor_idx)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2202.get_sensor_dpi_parameters_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetSensorDpiParametersResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.GetSensorDpiParametersResponseChecker.check_fields(
                self, response, self.feature_2202.get_sensor_dpi_parameters_response_cls)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2202_0001#6", _AUTHOR)
    # end def test_get_sensor_dpi_parameters_software_id

    @features("Feature2202")
    @features("Feature8100")
    @level("Robustness")
    def test_set_sensor_dpi_parameters_software_id(self):
        """
        Validate ``SetSensorDpiParameters`` software id field is ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.SensorIdx.DpiX.DpiY.Lod.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP
                 .0xPP.0xPP.0xPP.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        sensor_idx = 0
        dpi_x = self.config.F_DefaultDpiX
        dpi_y = self.config.F_DefaultDpiY
        lod = self.config.F_DefaultLod
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ExtendedAdjustableDpi.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetSensorDpiParameters request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_2202.set_sensor_dpi_parameters_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2202_index,
                sensor_idx=sensor_idx,
                dpi_x=dpi_x,
                dpi_y=dpi_y,
                lod=lod)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2202.set_sensor_dpi_parameters_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetSensorDpiParametersResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.SetSensorDpiParametersResponseChecker.check_fields(
                self, response, self.feature_2202.set_sensor_dpi_parameters_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetSensorDpiParametersEvent is received")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.HIDppHelper.sensor_dpi_parameters_event(test_case=self)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2202_0001#7", _AUTHOR)
    # end def test_set_sensor_dpi_parameters_software_id

    @features("Feature2202")
    @features("Feature8100")
    @level("Robustness")
    def test_show_sensor_dpi_status_software_id(self):
        """
        Validate ``ShowSensorDpiStatus`` software id field is ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.SensorIdx.DpiLevel.LedHoldType.ButtonNum.0xPP.0xPP.
                 0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        sensor_idx = 0
        dpi_level = self.config_manager.get_feature(ConfigurationManager.ID.OOB_PROFILES_DEFAULT_DPI_INDEX)[0] + 1
        led_hold_type = ExtendedAdjustableDpi.LedHoldType.TIMER_BASED
        button_num = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ExtendedAdjustableDpi.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ShowSensorDpiStatus request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_2202.show_sensor_dpi_status_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2202_index,
                sensor_idx=sensor_idx,
                dpi_level=dpi_level,
                led_hold_type=led_hold_type,
                button_num=button_num)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2202.show_sensor_dpi_status_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ShowSensorDpiStatusResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.ShowSensorDpiStatusResponseChecker.check_fields(
                self, response, self.feature_2202.show_sensor_dpi_status_response_cls)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2202_0001#8", _AUTHOR)
    # end def test_show_sensor_dpi_status_software_id

    @features("Feature2202")
    @features("Feature8100")
    @features("DpiCalibrationSupported")
    @level("Robustness")
    def test_get_dpi_calibration_info_software_id(self):
        """
        Validate ``GetDpiCalibrationInfo`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.SensorIdx.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        sensor_idx = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ExtendedAdjustableDpi.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetDpiCalibrationInfo request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_2202.get_dpi_calibration_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2202_index,
                sensor_idx=sensor_idx)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2202.get_dpi_calibration_info_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetDpiCalibrationInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.GetDpiCalibrationInfoResponseChecker.check_fields(
                self, response, self.feature_2202.get_dpi_calibration_info_response_cls)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2202_0001#9", _AUTHOR)
    # end def test_get_dpi_calibration_info_software_id

    @features("Feature2202")
    @features("Feature8100")
    @features("DpiCalibrationSupported")
    @level("Robustness")
    def test_start_dpi_calibration_software_id(self):
        """
        Validate ``StartDpiCalibration`` software id field is ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.SensorIdx.Direction.ExpectedCount.CalibType.
                 CalibStartTimeout.CalibHWProcessTimeout.CalibSWProcessTimeout.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        sensor_idx = 0
        direction = ExtendedAdjustableDpi.Direction.X
        expected_count = ExtendedAdjustableDpiTestUtils.compute_expected_count(
            self, ExtendedAdjustableDpi.Direction.X, self.config.F_MouseLength)
        calib_type = ExtendedAdjustableDpi.CalibType.HW
        calib_start_timeout = 0
        calib_hw_process_timeout = 0
        calib_sw_process_timeout = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ExtendedAdjustableDpi.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send StartDpiCalibration request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_2202.start_dpi_calibration_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2202_index,
                sensor_idx=sensor_idx,
                direction=direction,
                expected_count=expected_count,
                calib_type=calib_type,
                calib_start_timeout=calib_start_timeout,
                calib_hw_process_timeout=calib_hw_process_timeout,
                calib_sw_process_timeout=calib_sw_process_timeout)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2202.start_dpi_calibration_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check StartDpiCalibrationResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableDpiTestUtils.StartDpiCalibrationResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map['expected_count'] = (checker.check_expected_count, expected_count)
            checker.check_fields(self, response, self.feature_2202.start_dpi_calibration_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetSensorDpiParametersEvent is received")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.HIDppHelper.dpi_calibration_completed_event(test_case=self)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2202_0001#10", _AUTHOR)
    # end def test_start_dpi_calibration_software_id

    @features("Feature2202")
    @features("Feature8100")
    @features("DpiCalibrationSupported")
    @level("Robustness")
    def test_set_dpi_calibration_software_id(self):
        """
        Validate ``SetDpiCalibration`` software id field is ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.SensorIdx.Direction.CalibCor.0xPP.0xPP.0xPP.0xPP.0xPP
                 .0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        sensor_idx = 0
        direction = ExtendedAdjustableDpi.Direction.X
        calib_cor = ExtendedAdjustableDpi.RevertCommand.TO_OOB_PROFILE
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ExtendedAdjustableDpi.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetDpiCalibration request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_2202.set_dpi_calibration_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2202_index,
                sensor_idx=sensor_idx,
                direction=direction,
                calib_cor=calib_cor)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2202.set_dpi_calibration_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetDpiCalibrationResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.SetDpiCalibrationResponseChecker.check_fields(
                self, response, self.feature_2202.set_dpi_calibration_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetSensorDpiParametersEvent is received")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.HIDppHelper.sensor_dpi_parameters_event(test_case=self)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2202_0001#11", _AUTHOR)
    # end def test_set_dpi_calibration_software_id

    @features("Feature2202")
    @level("Robustness")
    def test_get_sensor_count_padding(self):
        """
        Validate ``GetSensorCount`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_2202.get_sensor_count_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetSensorCount request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2202_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2202.get_sensor_count_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetSensorCountResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.GetSensorCountResponseChecker.check_fields(
                self, response, self.feature_2202.get_sensor_count_response_cls)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2202_0002#1", _AUTHOR)
    # end def test_get_sensor_count_padding

    @features("Feature2202")
    @level("Robustness")
    def test_get_sensor_capabilities_padding(self):
        """
        Validate ``GetSensorCapabilities`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.SensorIdx.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        sensor_idx = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_2202.get_sensor_capabilities_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetSensorCapabilities request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2202_index,
                sensor_idx=sensor_idx)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2202.get_sensor_capabilities_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetSensorCapabilitiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.GetSensorCapabilitiesResponseChecker.check_fields(
                self, response, self.feature_2202.get_sensor_capabilities_response_cls)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2202_0002#2", _AUTHOR)
    # end def test_get_sensor_capabilities_padding

    @features("Feature2202")
    @level("Robustness")
    def test_get_sensor_dpi_list_padding(self):
        """
        Validate ``GetSensorDpiList`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.SensorIdx.Direction.0xPP

        Padding (PP) boundary values [00..FF]
        """
        sensor_idx = 0
        direction = ExtendedAdjustableDpi.Direction.X
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_2202.get_sensor_dpi_list_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetSensorDpiList request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2202_index,
                sensor_idx=sensor_idx,
                direction=direction)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2202.get_sensor_dpi_list_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetSensorDpiListResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.GetSensorDpiListResponseChecker.check_fields(
                self, response, self.feature_2202.get_sensor_dpi_list_response_cls)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2202_0002#3", _AUTHOR)
    # end def test_get_sensor_dpi_list_padding

    @features("Feature2202")
    @level("Robustness")
    def test_get_sensor_lod_list_padding(self):
        """
        Validate ``GetSensorLodList`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.SensorIdx.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        sensor_idx = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_2202.get_sensor_lod_list_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetSensorLodList request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2202_index,
                sensor_idx=sensor_idx)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2202.get_sensor_lod_list_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetSensorLodListResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.GetSensorLodListResponseChecker.check_fields(
                self, response, self.feature_2202.get_sensor_lod_list_response_cls)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2202_0002#4", _AUTHOR)
    # end def test_get_sensor_lod_list_padding

    @features("Feature2202")
    @level("Robustness")
    def test_get_sensor_dpi_parameters_padding(self):
        """
        Validate ``GetSensorDpiParameters`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.SensorIdx.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        sensor_idx = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_2202.get_sensor_dpi_parameters_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetSensorDpiParameters request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2202_index,
                sensor_idx=sensor_idx)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2202.get_sensor_dpi_parameters_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetSensorDpiParametersResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.GetSensorDpiParametersResponseChecker.check_fields(
                self, response, self.feature_2202.get_sensor_dpi_parameters_response_cls)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2202_0002#5", _AUTHOR)
    # end def test_get_sensor_dpi_parameters_padding

    @features("Feature2202")
    @features("Feature8100")
    @features("DpiCalibrationSupported")
    @level("Robustness")
    def test_get_dpi_calibration_info_padding(self):
        """
        Validate ``GetDpiCalibrationInfo`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.SensorIdx.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        sensor_idx = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_2202.get_dpi_calibration_info_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetDpiCalibrationInfo request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2202_index,
                sensor_idx=sensor_idx)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2202.get_dpi_calibration_info_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetDpiCalibrationInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.GetDpiCalibrationInfoResponseChecker.check_fields(
                self, response, self.feature_2202.get_dpi_calibration_info_response_cls)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2202_0002#6", _AUTHOR)
    # end def test_get_dpi_calibration_info_padding

    @features("Feature2202")
    @features("Feature8100")
    @level("Robustness")
    def test_set_sensor_dpi_parameters_padding(self):
        """
        Validate ``SetSensorDpiParameters`` padding bytes are ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.SensorIdx.DpiX.DpiY.Lod.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP
                 .0xPP.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        sensor_idx = 0
        dpi_x = self.config.F_DefaultDpiX
        dpi_y = self.config.F_DefaultDpiY
        lod = self.config.F_DefaultLod
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_2202.set_sensor_dpi_parameters_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetSensorDpiParameters request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2202_index,
                sensor_idx=sensor_idx,
                dpi_x=dpi_x,
                dpi_y=dpi_y,
                lod=lod)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2202.set_sensor_dpi_parameters_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetSensorDpiParameters fields")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.SetSensorDpiParametersResponseChecker.check_fields(
                self, response, self.feature_2202.set_sensor_dpi_parameters_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetSensorDpiParametersEvent is received")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.HIDppHelper.sensor_dpi_parameters_event(test_case=self)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2202_0002#7", _AUTHOR)
    # end def test_set_sensor_dpi_parameters_padding

    @features("Feature2202")
    @features("Feature8100")
    @level("Robustness")
    def test_show_sensor_dpi_status_padding(self):
        """
        Validate ``ShowSensorDpiStatus`` padding bytes are ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.SensorIdx.DpiLevel.LedHoldType.ButtonNum.0xPP.0xPP.
                 0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        default_dpi_level = self.config_manager.get_feature(
            ConfigurationManager.ID.OOB_PROFILES_DEFAULT_DPI_INDEX)[0] + 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_2202.show_sensor_dpi_status_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ShowSensorDpiStatus request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2202_index,
                sensor_idx=0,
                dpi_level=default_dpi_level,
                led_hold_type=ExtendedAdjustableDpi.LedHoldType.TIMER_BASED,
                button_num=0)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2202.show_sensor_dpi_status_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ShowSensorDpiStatus fields")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.ShowSensorDpiStatusResponseChecker.check_fields(
                self, response, self.feature_2202.show_sensor_dpi_status_response_cls)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2202_0002#8", _AUTHOR)
    # end def test_show_sensor_dpi_status_padding

    @features("Feature2202")
    @features("Feature8100")
    @features("DpiCalibrationSupported")
    @level("Robustness")
    def test_start_dpi_calibration_padding(self):
        """
        Validate ``StartDpiCalibration`` padding bytes are ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.SensorIdx.Direction.ExpectedCount.CalibType.
                 CalibStartTimeout.CalibHWProcessTimeout.CalibSWProcessTimeout.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        expected_count = ExtendedAdjustableDpiTestUtils.compute_expected_count(
            self, ExtendedAdjustableDpi.Direction.X, self.config.F_MouseLength)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_2202.start_dpi_calibration_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send StartDpiCalibration request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2202_index,
                sensor_idx=0,
                direction=ExtendedAdjustableDpi.Direction.X,
                expected_count=expected_count,
                calib_type=ExtendedAdjustableDpi.CalibType.HW,
                calib_start_timeout=0,
                calib_hw_process_timeout=0,
                calib_sw_process_timeout=0)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2202.start_dpi_calibration_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check StartDpiCalibration fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableDpiTestUtils.StartDpiCalibrationResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map['expected_count'] = (checker.check_expected_count, expected_count)
            checker.check_fields(self, response, self.feature_2202.start_dpi_calibration_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetSensorDpiParametersEvent is received")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.HIDppHelper.dpi_calibration_completed_event(test_case=self)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2202_0002#9", _AUTHOR)
    # end def test_start_dpi_calibration_padding

    @features("Feature2202")
    @features("Feature8100")
    @features("DpiCalibrationSupported")
    @level("Robustness")
    def test_set_dpi_calibration_padding(self):
        """
        Validate ``SetDpiCalibration`` padding bytes are ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.SensorIdx.Direction.CalibCor.0xPP.0xPP.0xPP.0xPP.0xPP
                 .0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_2202.set_dpi_calibration_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetDpiCalibration request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2202_index,
                sensor_idx=0,
                direction=ExtendedAdjustableDpi.Direction.X,
                calib_cor=ExtendedAdjustableDpi.RevertCommand.TO_OOB_PROFILE)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2202.set_dpi_calibration_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetDpiCalibration fields")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.SetDpiCalibrationResponseChecker.check_fields(
                self, response, self.feature_2202.set_dpi_calibration_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetSensorDpiParametersEvent is received")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableDpiTestUtils.HIDppHelper.sensor_dpi_parameters_event(test_case=self)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2202_0002#10", _AUTHOR)
    # end def test_set_dpi_calibration_padding

    @features("Feature2202")
    @features("Feature8100")
    @features("DpiCalibrationSupported")
    @level("Robustness")
    @services("RequiredKeys", (KEY_ID.BUTTON_1,))
    def test_dpi_calibration_timeout(self):
        """
        Verify the device send calibration failed notification after timeout
        """
        start_timeout = 3
        hw_timeout = 3
        expected_count = 2000
        direction = ExtendedAdjustableDpi.Direction.X
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send startDpiCalibration with calibStartTimeout = {start_timeout} sec")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.start_dpi_calibration(
            test_case=self, sensor_idx=0, direction=direction, expected_count=expected_count,
            calib_type=ExtendedAdjustableDpi.CalibType.HW, calib_start_timeout=start_timeout,
            calib_hw_process_timeout=hw_timeout, calib_sw_process_timeout=hw_timeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Wait {start_timeout} sec then check received calibration failed notification "
                                  "(dpiCalibrationCompletedEvent.calibCor = 0x8000)")
        # --------------------------------------------------------------------------------------------------------------
        sleep(start_timeout + 0.01)
        event = ExtendedAdjustableDpiTestUtils.HIDppHelper.dpi_calibration_completed_event(self)
        self.assertEqual(expected=0x8000, obtained=to_int(event.calib_cor),
                         msg='Shall receive calibration failed notification.')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send startDpiCalibration with calibHWProcessTimeout = {hw_timeout} sec")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.start_dpi_calibration(
            test_case=self, sensor_idx=0, direction=direction, expected_count=expected_count,
            calib_type=ExtendedAdjustableDpi.CalibType.HW, calib_start_timeout=start_timeout,
            calib_hw_process_timeout=hw_timeout, calib_sw_process_timeout=hw_timeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press and hold mouse left button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(KEY_ID.BUTTON_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Wait {hw_timeout} sec then check received calibration failed notification "
                                  "(dpiCalibrationCompletedEvent.calibCor = 0x8000)")
        # --------------------------------------------------------------------------------------------------------------
        sleep(hw_timeout + 0.01)
        event = ExtendedAdjustableDpiTestUtils.HIDppHelper.dpi_calibration_completed_event(self)
        self.assertEqual(expected=0x8000, obtained=to_int(event.calib_cor),
                         msg='Shall receive calibration failed notification.')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Release mouse left button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(KEY_ID.BUTTON_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send startDpiCalibration with calibSWProcessTimeout = {hw_timeout} sec")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.HIDppHelper.start_dpi_calibration(
            test_case=self, sensor_idx=0, direction=direction, expected_count=expected_count,
            calib_type=ExtendedAdjustableDpi.CalibType.SW, calib_start_timeout=start_timeout,
            calib_hw_process_timeout=hw_timeout, calib_sw_process_timeout=hw_timeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Wait {hw_timeout} sec then check received calibration failed notification "
                                  "(dpiCalibrationCompletedEvent.calibCor = 0x8000)")
        # --------------------------------------------------------------------------------------------------------------
        sleep(hw_timeout + 0.01)
        event = ExtendedAdjustableDpiTestUtils.HIDppHelper.dpi_calibration_completed_event(self)
        self.assertEqual(expected=0x8000, obtained=to_int(event.calib_cor),
                         msg='Shall receive calibration failed notification.')

        self.testCaseChecked("ROB_2202_0003", _AUTHOR)
    # end def test_dpi_calibration_timeout
# end class ExtendedAdjustableDpiRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
