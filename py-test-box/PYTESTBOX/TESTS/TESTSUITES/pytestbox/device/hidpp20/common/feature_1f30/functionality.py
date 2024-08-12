#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.common.feature_1f30.functionality
:brief: HID++ 2.0 ``TemperatureMeasurement`` functionality test suite
:author: Sanjib Hazra <shazra@logitech.com>
:date: 2021/11/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.numeral import Numeral
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
class TemperatureMeasurementFunctionalityTestCase(TemperatureMeasurementTestCase):
    """
    Validates ``TemperatureMeasurement`` functionality test cases
    """
    @features("Feature1F30")
    @level("Interface")
    def test_get_temperature_functionality(self):
        """
        Validate ``GetTemperature`` functionality
        """
        temperature = None
        for sensor_id in range(int(Numeral(self.f.PRODUCT.FEATURES.COMMON.TEMPERATURE_MEASUREMENT.F_SensorCount))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetTemperature request for sensor_id {sensor_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1f30.get_temperature_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_1f30_index,
                sensor_id=sensor_id)
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
        self.testCaseChecked("FUN_1F30_0001", _AUTHOR)
    # end def test_get_temperature_functionality
# end class TemperatureMeasurementFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
