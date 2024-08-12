#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.peripheral.feature_9215.robustness
:brief: HID++ 2.0 ``Ads1231`` robustness test suite
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/06/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.ads1231utils import Ads1231TestUtils
from pytestbox.device.hidpp20.peripheral.feature_9215.ads1231 import Ads1231TestCase
from pyhid.hidpp.features.peripheral.ads1231 import Ads1231
from pytestbox.base.loghelper import LogHelper

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vasudev Mukkamala"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class Ads1231RobustnessTestCase(Ads1231TestCase):
    """
    Validates ``Ads1231`` robustness test cases
    """
    @features("Feature9215")
    @level("Robustness")
    def test_set_monitor_mode_software_id(self):
        """
        Validate ``SetMonitorMode`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.Count.Threshold

        SwID boundary values [0..F]
        """
        self.post_requisite_reload_nvs = True
        count = 0
        threshold = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(Ads1231.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetMonitorMode request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_9215.set_monitor_mode_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_9215_index,
                count=count,
                threshold=threshold)
            report.softwareId = software_id
            response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.peripheral_message_queue,
                response_class_type=self.feature_9215.set_monitor_mode_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetMonitorModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = DeviceTestUtils.MessageChecker
            check_map = {
                "deviceIndex": (checker.check_device_index, report.deviceIndex),
                "featureIndex": (checker.check_feature_index, report.featureIndex),
            }
            checker.check_fields(self, response, self.feature_9215.set_monitor_mode_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9215_0001", _AUTHOR)
    # end def test_set_monitor_mode_software_id

    @features("Feature9215")
    @level("Robustness")
    def test_shutdown_and_reset_sensor_robustness(self):
        """
        Validates ``ShutdownSensor`` and ``ResetSensor`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex.0xPP.0xPP.0xPP
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_9215.shutdown_sensor_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ShutdownSensor request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(device_index=self.deviceIndex,
                                 feature_index=self.feature_9215_index)
            report.padding = padding
            response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.peripheral_message_queue,
                response_class_type=self.feature_9215.shutdown_sensor_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ShutdownSensorResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=report.deviceIndex,
                             obtained=response.deviceIndex,
                             msg="The deviceIndex parameter differs from the one expected")
            self.assertEqual(expected=report.featureIndex,
                             obtained=response.featureIndex,
                             msg="The featureIndex parameter differs from the one expected")
            # end for

            # powering sensor back on
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ResetSensor request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_9215.reset_sensor_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_9215_index)
            report.padding = padding
            response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.peripheral_message_queue,
                response_class_type=self.feature_9215.reset_sensor_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ResetSensorResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=report.deviceIndex,
                             obtained=response.deviceIndex,
                             msg="The deviceIndex parameter differs from the one expected")
            self.assertEqual(expected=report.featureIndex,
                             obtained=response.featureIndex,
                             msg="The featureIndex parameter differs from the one expected")
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9215_0002", _AUTHOR)
        self.testCaseChecked("ROB_9215_0003", _AUTHOR)
    # end def test_shutdown_and_reset_sensor_robustness

    @features("Feature9215")
    @level("Robustness")
    def test_calibrate_padding(self):
        """
        Validate ``Calibrate`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RefPointIndex.RefPointOutValue.0xPP

        Padding (PP) boundary values [00..FF]
        """
        self.post_requisite_reload_nvs = True
        ref_point_index = HexList("01")
        ref_point_out_value = HexList("30")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_9215.calibrate_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Calibrate request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(device_index=self.deviceIndex,
                                 feature_index=self.feature_9215_index,
                                 ref_point_index=ref_point_index,
                                 ref_point_out_value=ref_point_out_value)
            report.padding = padding
            response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.peripheral_message_queue,
                response_class_type=self.feature_9215.calibrate_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check CalibrateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = DeviceTestUtils.MessageChecker
            check_map = {
                "deviceIndex": (checker.check_device_index, report.deviceIndex),
                "featureIndex": (checker.check_feature_index, report.featureIndex),
            }
            checker.check_fields(self, response, self.feature_9215.calibrate_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9215_0004", _AUTHOR)
    # end def test_calibrate_padding

    @features("Feature9215")
    @level("Robustness")
    def test_read_calibration_padding(self):
        """
        Validate ``ReadCalibration`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RefPointIndex.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
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
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_9215.read_calibration_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadCalibration request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(device_index=self.deviceIndex,
                                 feature_index=self.feature_9215_index,
                                 ref_point_index=ref_point_index)
            report.padding = padding
            response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.peripheral_message_queue,
                response_class_type=self.feature_9215.read_calibration_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ReadCalibrationResponse fields")
            # ----------------------------------------------------------------------------------------------------------
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
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9215_0005", _AUTHOR)
    # end def test_read_calibration_padding

    @features("Feature9215")
    @level("Robustness")
    def test_write_calibration_padding(self):
        """
        Validate ``WriteCalibration`` padding bytes are ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RefPointIndex.RefPointOutValue.RefPointCalValue.

        0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        self.post_requisite_reload_nvs = True
        ref_point_index = HexList("01")
        ref_point_out_value = HexList("30")
        ref_point_cal_value = HexList("F01000")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_9215.write_calibration_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send WriteCalibration request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(device_index=self.deviceIndex,
                                 feature_index=self.feature_9215_index,
                                 ref_point_index=ref_point_index,
                                 ref_point_out_value=ref_point_out_value,
                                 ref_point_cal_value=ref_point_cal_value)
            report.padding = padding
            response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.peripheral_message_queue,
                response_class_type=self.feature_9215.write_calibration_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check WriteCalibrationResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = Ads1231TestUtils.WriteCalibrationResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "deviceIndex": (checker.check_device_index, report.deviceIndex),
                "featureIndex": (checker.check_feature_index, report.featureIndex),
                "ref_point_index": (checker.check_ref_point_index, ref_point_index),
                "ref_point_out_value": (checker.check_ref_point_out_value, ref_point_out_value),
                "ref_point_cal_value": (checker.check_ref_point_cal_value, ref_point_cal_value),
            })
            checker.check_fields(self, response, self.feature_9215.write_calibration_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9215_0006", _AUTHOR)
    # end def test_write_calibration_padding

    @features("Feature9215")
    @level("Robustness")
    def test_read_other_nvs_data_padding(self):
        """
        Validate ``ReadOtherNvsData`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.DataFieldId.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        data_field_id = HexList("00")
        data = HexList("400000000000000000000000000000")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send WriteOtherNvsData request")
        # --------------------------------------------------------------------------------------------------------------
        Ads1231TestUtils.HIDppHelper.write_other_nvs_data(self, data_field_id=data_field_id, data=data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_9215.read_other_nvs_data_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadOtherNvsData request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(device_index=self.deviceIndex,
                                 feature_index=self.feature_9215_index,
                                 data_field_id=data_field_id)
            report.padding = padding
            response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.peripheral_message_queue,
                response_class_type=self.feature_9215.read_other_nvs_data_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ReadOtherNvsDataResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = Ads1231TestUtils.ReadOtherNvsDataResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "deviceIndex": (checker.check_device_index, report.deviceIndex),
                "featureIndex": (checker.check_feature_index, report.featureIndex),
                "data_field_id": (checker.check_data_field_id, data_field_id),
                "data": (checker.check_data, data),
            })
            checker.check_fields(self, response, self.feature_9215.read_other_nvs_data_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9215_0007", _AUTHOR)
    # end def test_read_other_nvs_data_padding

    @features("Feature9215WithManDynCal")
    @level("Robustness")
    def test_manage_dynamic_calibration_parameters_padding(self):
        """
        Validate ``ManageDynamicCalibrationParameters`` padding bytes are ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.Command.OffsetExtension.OffsetAdjustmentCount.

        DynamicThreshold.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        self.post_requisite_reload_nvs = True
        command_set = HexList("80")
        offset_extension_set = HexList("07")
        offset_adjustment_count_set = HexList("0014")
        dynamic_threshold_set = HexList("05")

        command_get = HexList("00")
        offset_extension_get = HexList("00")
        offset_adjustment_count_get = HexList("0000")
        dynamic_threshold_get = HexList("00")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_9215.manage_dynamic_calibration_parameters_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ManageDynamicCalibrationParameters request (set) with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(device_index=self.deviceIndex,
                                 feature_index=self.feature_9215_index,
                                 command=command_set,
                                 offset_extension=offset_extension_set,
                                 offset_adjustment_count=offset_adjustment_count_set,
                                 dynamic_threshold=dynamic_threshold_set)
            report.padding = padding
            response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.peripheral_message_queue,
                response_class_type=self.feature_9215.manage_dynamic_calibration_parameters_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ManageDynamicCalibrationParametersResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = Ads1231TestUtils.ManageDynamicCalibrationParametersResponseChecker
            checker.check_fields(self, response, self.feature_9215.manage_dynamic_calibration_parameters_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ManageDynamicCalibrationParameters request (get) with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_9215.manage_dynamic_calibration_parameters_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_9215_index,
                command=command_get,
                offset_extension=offset_extension_get,
                offset_adjustment_count=offset_adjustment_count_get,
                dynamic_threshold=dynamic_threshold_get)
            report.padding = padding
            response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.peripheral_message_queue,
                response_class_type=self.feature_9215.manage_dynamic_calibration_parameters_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ManageDynamicCalibrationParametersResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = Ads1231TestUtils.ManageDynamicCalibrationParametersResponseChecker
            checker.check_fields(self, response, self.feature_9215.manage_dynamic_calibration_parameters_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9215_0008", _AUTHOR)
    # end def test_manage_dynamic_calibration_parameters_padding
# end class Ads1231RobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
