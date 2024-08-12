#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1f30.robustness
:brief: HID++ 2.0 ``TemperatureMeasurement`` robustness test suite
:author: Sanjib Hazra <shazra@logitech.com>
:date: 2021/06/07
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.common.temperaturemeasurement import TemperatureMeasurement
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.temperaturemeasurementutils import TemperatureMeasurementTestUtils
from pytestbox.device.hidpp20.common.feature_1f30.temperaturemeasurement import TemperatureMeasurementTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Sanjib Hazra"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TemperatureMeasurementRobustnessTestCase(TemperatureMeasurementTestCase):
    """
    Validates ``TemperatureMeasurement`` robustness test cases
    """
    @features("Feature1F30")
    @level("Robustness")
    def test_get_info_software_id(self):
        """
        Validate ``GetInfo`` software id field is ignored by the firmware
        """
        sensor_count = self.f.PRODUCT.FEATURES.COMMON.TEMPERATURE_MEASUREMENT.F_SensorCount
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(TemperatureMeasurement.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetInfo request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1f30.get_info_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_1f30_index)
            report.softwareId = software_id
            response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=self.feature_1f30.get_info_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = TemperatureMeasurementTestUtils.GetInfoResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "deviceIndex": (checker.check_device_index, report.deviceIndex),
                "featureIndex": (checker.check_feature_index, report.featureIndex),
                "sensor_count": (checker.check_sensor_count, sensor_count),
            })
            checker.check_fields(self, response, self.feature_1f30.get_info_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1F30_0001", _AUTHOR)
    # end def test_get_info_software_id

    @features("Feature1F30")
    @level("Robustness")
    def test_get_temperature_software_id(self):
        """
        Validate ``GetTemperature`` software id field is ignored by the firmware
        """
        sensor_id = 0
        temperature = None
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(TemperatureMeasurement.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetTemperature request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1f30.get_temperature_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_1f30_index,
                sensor_id=sensor_id)
            report.softwareId = software_id
            response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=self.feature_1f30.get_temperature_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetTemperatureResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = TemperatureMeasurementTestUtils.GetTemperatureResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "deviceIndex": (checker.check_device_index, report.deviceIndex),
                "featureIndex": (checker.check_feature_index, report.featureIndex),
                "sensor_id": (checker.check_sensor_id, sensor_id),
                "temperature": (checker.check_temperature, temperature),
            })
            checker.check_fields(self, response, self.feature_1f30.get_temperature_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1F30_0002", _AUTHOR)
    # end def test_get_temperature_software_id

    @features("Feature1F30")
    @level("Robustness")
    def test_get_info_padding(self):
        """
        Validate ``GetInfo`` padding bytes are ignored by the firmware
        """
        sensor_count = self.f.PRODUCT.FEATURES.COMMON.TEMPERATURE_MEASUREMENT.F_SensorCount
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1f30.get_info_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetInfo request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_1f30_index)
            report.padding = padding
            response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=self.feature_1f30.get_info_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = TemperatureMeasurementTestUtils.GetInfoResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "deviceIndex": (checker.check_device_index, report.deviceIndex),
                "featureIndex": (checker.check_feature_index, report.featureIndex),
                "sensor_count": (checker.check_sensor_count, sensor_count),
            })
            checker.check_fields(self, response, self.feature_1f30.get_info_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1F30_0003", _AUTHOR)
    # end def test_get_info_padding

    @features("Feature1F30")
    @level("Robustness")
    def test_get_temperature_padding(self):
        """
        Validate ``GetTemperature`` padding bytes are ignored by the firmware
        """
        sensor_id = 0
        temperature = None
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1f30.get_temperature_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetTemperature request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_1f30_index,
                sensor_id=sensor_id)
            report.padding = padding
            response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=self.feature_1f30.get_temperature_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetTemperatureResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = TemperatureMeasurementTestUtils.GetTemperatureResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "deviceIndex": (checker.check_device_index, report.deviceIndex),
                "featureIndex": (checker.check_feature_index, report.featureIndex),
                "sensor_id": (checker.check_sensor_id, sensor_id),
                "temperature": (checker.check_temperature, temperature),
            })
            checker.check_fields(self, response, self.feature_1f30.get_temperature_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1F30_0004", _AUTHOR)
    # end def test_get_temperature_padding
# end class TemperatureMeasurementRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
