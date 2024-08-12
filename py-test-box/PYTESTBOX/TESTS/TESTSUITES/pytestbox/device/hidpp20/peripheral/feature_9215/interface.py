#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.peripheral.feature_9215.interface
:brief: HID++ 2.0 ``Ads1231`` interface test suite
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/06/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.ads1231utils import Ads1231TestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.hidpp20.peripheral.feature_9215.ads1231 import Ads1231TestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vasudev Mukkamala"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class Ads1231InterfaceTestCase(Ads1231TestCase):
    """
    Validate ``Ads1231`` interface test cases
    """

    @features("Feature9215")
    @level("Interface")
    def test_shutdown_and_reset_sensor_interface(self):
        """
        Validate ``ShutdownSensor`` interface
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send ShutdownSensor request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_9215.shutdown_sensor_cls(
            device_index=self.deviceIndex,
            feature_index=self.feature_9215_index)
        response = self.send_report_wait_response(
            report=report,
            response_queue=self.hidDispatcher.peripheral_message_queue,
            response_class_type=self.feature_9215.shutdown_sensor_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ShutdownSensorResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
        }
        checker.check_fields(self, response, self.feature_9215.shutdown_sensor_response_cls, check_map)

        # powering sensor back on
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send ResetSensor request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_9215.reset_sensor_cls(
            device_index=self.deviceIndex,
            feature_index=self.feature_9215_index)
        response = self.send_report_wait_response(
            report=report,
            response_queue=self.hidDispatcher.peripheral_message_queue,
            response_class_type=self.feature_9215.reset_sensor_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ResetSensorResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
        }
        checker.check_fields(self, response, self.feature_9215.reset_sensor_response_cls, check_map)

        self.testCaseChecked("INT_9215_0001", _AUTHOR)
        self.testCaseChecked("INT_9215_0002", _AUTHOR)
    # end def test_shutdown_and_reset_sensor_interface

    @features("Feature9215")
    @level("Interface")
    def test_set_monitor_mode_interface(self):
        """
        Validate ``SetMonitorMode`` interface
        """
        self.post_requisite_reload_nvs = True
        count = HexList("0000")
        threshold = HexList("00")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send SetMonitorMode request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_9215.set_monitor_mode_cls(
            device_index=self.deviceIndex,
            feature_index=self.feature_9215_index,
            count=count,
            threshold=threshold)
        response = self.send_report_wait_response(
            report=report,
            response_queue=self.hidDispatcher.peripheral_message_queue,
            response_class_type=self.feature_9215.set_monitor_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetMonitorModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
        }
        checker.check_fields(self, response, self.feature_9215.set_monitor_mode_response_cls, check_map)

        self.testCaseChecked("INT_9215_0003", _AUTHOR)
    # end def test_set_monitor_mode_interface

    @features("Feature9215")
    @level("Interface")
    def test_calibrate_interface(self):
        """
        Validate ``Calibrate`` interface
        """
        self.post_requisite_reload_nvs = True
        ref_point_index = 0
        ref_point_out_value = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send Calibrate request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_9215.calibrate_cls(
            device_index=self.deviceIndex,
            feature_index=self.feature_9215_index,
            ref_point_index=ref_point_index,
            ref_point_out_value=ref_point_out_value)
        response = self.send_report_wait_response(
            report=report,
            response_queue=self.hidDispatcher.peripheral_message_queue,
            response_class_type=self.feature_9215.calibrate_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check CalibrateResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
        }
        checker.check_fields(self, response, self.feature_9215.calibrate_response_cls, check_map)

        self.testCaseChecked("INT_9215_0004", _AUTHOR)
    # end def test_calibrate_interface

    @features("Feature9215")
    @level("Interface")
    def test_read_and_write_calibration_interface(self):
        """
        Validate ``ReadCalibration`` interface
        """
        self.post_requisite_reload_nvs = True
        ref_point_index = HexList("01")
        ref_point_out_value = HexList("30")
        ref_point_cal_value = HexList("F01000")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send WriteCalibration request")
        # --------------------------------------------------------------------------------------------------------------
        Ads1231TestUtils.HIDppHelper.write_calibration(self,
                                                       ref_point_index=ref_point_index,
                                                       ref_point_out_value=ref_point_out_value,
                                                       ref_point_cal_value=ref_point_cal_value)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send ReadCalibration request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_9215.read_calibration_cls(
            device_index=self.deviceIndex,
            feature_index=self.feature_9215_index,
            ref_point_index=ref_point_index)
        response = self.send_report_wait_response(
            report=report,
            response_queue=self.hidDispatcher.peripheral_message_queue,
            response_class_type=self.feature_9215.read_calibration_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ReadCalibrationResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = Ads1231TestUtils.ReadCalibrationResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
            "ref_point_index": (checker.check_ref_point_index, ref_point_index),
            "ref_point_out_value": (checker.check_ref_point_out_value, ref_point_out_value),
            "ref_point_cal_value": (checker.check_ref_point_cal_value, ref_point_cal_value),
        })
        checker.check_fields(self, response, self.feature_9215.read_calibration_response_cls, check_map)

        self.testCaseChecked("INT_9215_0005", _AUTHOR)
        self.testCaseChecked("INT_9215_0006", _AUTHOR)
    # end def test_read_and_write_calibration_interface

    @features("Feature9215")
    @level("Interface")
    def test_read_and_write_other_nvs_data_interface(self):
        """
        Validate ``ReadOtherNvsData`` interface
        """
        self.post_requisite_reload_nvs = True
        data_field_id = HexList("00")
        data = HexList("400000000000000000000000000000")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send WriteOtherNvsData request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_9215.write_other_nvs_data_cls(
            device_index=self.deviceIndex,
            feature_index=self.feature_9215_index,
            data_field_id=data_field_id,
            data=data)
        self.send_report_wait_response(
            report=report,
            response_queue=self.hidDispatcher.peripheral_message_queue,
            response_class_type=self.feature_9215.write_other_nvs_data_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send ReadOtherNvsData request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_9215.read_other_nvs_data_cls(
            device_index=self.deviceIndex,
            feature_index=self.feature_9215_index,
            data_field_id=data_field_id)
        response = self.send_report_wait_response(
            report=report,
            response_queue=self.hidDispatcher.peripheral_message_queue,
            response_class_type=self.feature_9215.read_other_nvs_data_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ReadOtherNvsDataResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = Ads1231TestUtils.ReadOtherNvsDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
            "data_field_id": (checker.check_data_field_id, data_field_id),
            "data": (checker.check_data, data),
        })
        checker.check_fields(self, response, self.feature_9215.read_other_nvs_data_response_cls, check_map)

        self.testCaseChecked("INT_9215_0007", _AUTHOR)
        self.testCaseChecked("INT_9215_0008", _AUTHOR)
    # end def test_read_and_write_other_nvs_data_interface

    @features("Feature9215WithManDynCal")
    @level("Interface")
    def test_manage_dynamic_calibration_parameters_interface(self):
        """
        Validate ``ManageDynamicCalibrationParameters`` interface
        """
        self.post_requisite_reload_nvs = True
        command_get_value = HexList("00")
        offset_extension = HexList("07")
        offset_adjustment_count = HexList("0014")
        dynamic_threshold = HexList("05")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send ManageDynamicCalibrationParameters request with command:get")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_9215.manage_dynamic_calibration_parameters_cls(
            device_index=self.deviceIndex,
            feature_index=self.feature_9215_index,
            command=command_get_value,
            offset_extension=offset_extension,
            offset_adjustment_count=offset_adjustment_count,
            dynamic_threshold=dynamic_threshold)
        response = self.send_report_wait_response(
            report=report,
            response_queue=self.hidDispatcher.peripheral_message_queue,
            response_class_type=self.feature_9215.manage_dynamic_calibration_parameters_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ManageDynamicCalibrationParametersResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = Ads1231TestUtils.ManageDynamicCalibrationParametersResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
            "command": (checker.check_command, command_get_value),
            "offset_extension": (checker.check_offset_extension, offset_extension),
            "offset_adjustment_count": (checker.check_offset_adjustment_count, offset_adjustment_count),
            "dynamic_threshold": (checker.check_dynamic_threshold, dynamic_threshold),
        })
        checker.check_fields(self, response, self.feature_9215.manage_dynamic_calibration_parameters_response_cls,
                             check_map)

        self.testCaseChecked("INT_9215_0009", _AUTHOR)
    # end def test_manage_dynamic_calibration_parameters_interface
# end class Ads1231InterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
