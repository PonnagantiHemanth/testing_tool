#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1f30.interface
:brief: HID++ 2.0 ``TemperatureMeasurement`` interface test suite
:author: Sanjib Hazra <shazra@logitech.com>
:date: 2021/03/10
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.temperaturemeasurementutils import TemperatureMeasurementTestUtils
from pytestbox.device.hidpp20.common.feature_1f30.temperaturemeasurement import TemperatureMeasurementTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Sanjib Hazra"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TemperatureMeasurementInterfaceTestCase(TemperatureMeasurementTestCase):
    """
    Validates ``TemperatureMeasurement`` interface test cases
    """
    @features("Feature1F30")
    @level("Interface")
    def test_get_info_interface(self):
        """
        Validate ``GetInfo`` interface
        """
        sensor_count = self.f.PRODUCT.FEATURES.COMMON.TEMPERATURE_MEASUREMENT.F_SensorCount
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send GetInfo request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1f30.get_info_cls(
            device_index=self.deviceIndex,
            feature_index=self.feature_1f30_index)
        response = self.send_report_wait_response(
            report=report,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=self.feature_1f30.get_info_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetInfoResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = TemperatureMeasurementTestUtils.GetInfoResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
            "sensor_count": (checker.check_sensor_count, sensor_count),
        })
        checker.check_fields(self, response, self.feature_1f30.get_info_response_cls, check_map)

        self.testCaseChecked("INT_1F30_0001", _AUTHOR)
    # end def test_get_info_interface

    @features("Feature1F30")
    @level("Interface")
    def test_get_temperature_interface(self):
        """
        Validate ``GetTemperature`` interface
        """
        sensor_id = 0
        temperature = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send GetTemperature request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1f30.get_temperature_cls(
            device_index=self.deviceIndex,
            feature_index=self.feature_1f30_index,
            sensor_id=sensor_id)
        response = self.send_report_wait_response(
            report=report,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=self.feature_1f30.get_temperature_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetTemperatureResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = TemperatureMeasurementTestUtils.GetTemperatureResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
            "sensor_id": (checker.check_sensor_id, sensor_id),
            "temperature": (checker.check_temperature, temperature),
        })
        checker.check_fields(self, response, self.feature_1f30.get_temperature_response_cls, check_map)

        self.testCaseChecked("INT_1F30_0002", _AUTHOR)
    # end def test_get_temperature_interface
# end class TemperatureMeasurementInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
