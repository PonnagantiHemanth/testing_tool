#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.peripheral.feature_9001.interface
:brief: HID++ 2.0 ``PMW3816andPMW3826`` interface test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2023/01/09
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import skip

from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pylibrary.tools.hexlist import HexList
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.pmw3816andpmw3826utils import PMW3816andPMW3826TestUtils
from pytestbox.device.base.spidirectaccessutils import OpticalSensorName
from pytestbox.device.base.spidirectaccessutils import SPI_PERIPHERAL_REGISTER_DICT
from pytestbox.device.hidpp20.peripheral.feature_9001.pmw3816andpmw3826 import PMW3816andPMW3826TestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PMW3816andPMW3826InterfaceTestCase(PMW3816andPMW3826TestCase):
    """
    Validate ``PMW3816andPMW3826`` interface test cases
    """

    @features("Feature9001")
    @level("Interface")
    def test_read_sensor_register(self):
        """
        Validate ``ReadSensorRegister`` interface
        """
        register_address = \
            SPI_PERIPHERAL_REGISTER_DICT[self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName]["product_id"]["address"]
        register_value = \
            SPI_PERIPHERAL_REGISTER_DICT[self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName]["product_id"]["value"]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadSensorRegister request")
        # --------------------------------------------------------------------------------------------------------------
        response = PMW3816andPMW3826TestUtils.HIDppHelper.read_sensor_register(
            test_case=self,
            register_address=register_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ReadSensorRegisterResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = PMW3816andPMW3826TestUtils.ReadSensorRegisterResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_9001_index)),
            "register_value": (checker.check_register_value, HexList(register_value))
        })
        checker.check_fields(self, response, self.feature_9001.read_sensor_register_response_cls, check_map)
        self.testCaseChecked("INT_9001_0001", _AUTHOR)
    # end def test_read_sensor_register

    @features("Feature9001")
    @level("Interface")
    def test_write_sensor_register(self):
        """
        Validate ``WriteSensorRegister`` interface
        """
        register_address = \
            SPI_PERIPHERAL_REGISTER_DICT[self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName]["dpi"]["address"]
        register_value = HexList(0x0)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send WriteSensorRegister request")
        # --------------------------------------------------------------------------------------------------------------
        response = PMW3816andPMW3826TestUtils.HIDppHelper.write_sensor_register(
            test_case=self,
            register_address=register_address,
            register_value=register_value)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check WriteSensorRegisterResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_9001_index)),
        }
        checker.check_fields(self, response, self.feature_9001.write_sensor_register_response_cls, check_map)

        self.testCaseChecked("INT_9001_0002", _AUTHOR)
    # end def test_write_sensor_register

    @features("Feature9001")
    @level("Interface")
    def test_reset_sensor(self):
        """
        Validate ``ResetSensor`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ResetSensor request")
        # --------------------------------------------------------------------------------------------------------------
        response = PMW3816andPMW3826TestUtils.HIDppHelper.reset_sensor(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ResetSensorResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_9001_index)),
        }
        checker.check_fields(self, response, self.feature_9001.reset_sensor_response_cls, check_map)

        self.testCaseChecked("INT_9001_0003", _AUTHOR)
    # end def test_reset_sensor

    @features("Feature9001")
    @level("Interface")
    @skip("NotSupported")
    def test_shutdown_sensor(self):
        """
        Validate ``ShutdownSensor`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ShutdownSensor request")
        # --------------------------------------------------------------------------------------------------------------
        response = PMW3816andPMW3826TestUtils.HIDppHelper.shutdown_sensor(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ShutdownSensorResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_9001_index)),
        }
        checker.check_fields(self, response, self.feature_9001.shutdown_sensor_response_cls, check_map)

        self.testCaseChecked("INT_9001_0004", _AUTHOR)
    # end def test_shutdown_sensor

    @features("Feature9001")
    @level("Interface")
    def test_tracking_test(self):
        """
        Validate ``TrackingTest`` interface
        """
        count = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send TrackingTest request")
        # --------------------------------------------------------------------------------------------------------------
        response = PMW3816andPMW3826TestUtils.HIDppHelper.tracking_test(
            test_case=self,
            count=count)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check TrackingTestResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_9001_index)),
        }
        checker.check_fields(self, response, self.feature_9001.tracking_test_response_cls, check_map)

        self.testCaseChecked("INT_9001_0005", _AUTHOR)
    # end def test_tracking_test

    @features("Feature9001v0")
    @level("Interface")
    @bugtracker("Unexpected_FrameCapture_Response")
    def test_frame_capture(self):
        """
        Validate ``FrameCapture`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send FrameCapture request")
        # --------------------------------------------------------------------------------------------------------------
        response = PMW3816andPMW3826TestUtils.HIDppHelper.frame_capture(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check FrameCaptureResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        PMW3816andPMW3826TestUtils.MessageChecker.check_padding_is_zero(self, response)

        self.testCaseChecked("INT_9001_0006", _AUTHOR)
    # end def test_frame_capture

    @features("Feature9001v1")
    @level("Interface")
    def test_get_strap_data(self):
        """
        Validate ``GetStrapData`` interface
        """
        sensor = None
        if self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName == OpticalSensorName.TOG6:
            sensor = 0
        elif self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName == OpticalSensorName.TOGX:
            sensor = 1
        # end if
        strap_measurement_x = self.config.F_StrapData
        self.assertIsNotNone(sensor, "Sensor name is not defined in product settings")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetStrapData request")
        # --------------------------------------------------------------------------------------------------------------
        response = PMW3816andPMW3826TestUtils.HIDppHelper.get_strap_data(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetStrapDataResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = PMW3816andPMW3826TestUtils.GetStrapDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_9001_index)),
            "sensor": (checker.check_sensor, HexList(sensor)),
            "strap_measurement_x": (checker.check_strap_measurement_x, strap_measurement_x),
        })
        checker.check_fields(self, response, self.feature_9001.get_strap_data_response_cls, check_map)

        self.testCaseChecked("INT_9001_0007", _AUTHOR)
    # end def test_get_strap_data

    @features("Feature9001")
    @level("Interface")
    def test_continuous_power(self):
        """
        Validate ``ContinuousPower`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ContinuousPower request")
        # --------------------------------------------------------------------------------------------------------------
        response = PMW3816andPMW3826TestUtils.HIDppHelper.continuous_power(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ContinuousPowerResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_9001_index)),
        }
        checker.check_fields(self, response, self.feature_9001.continuous_power_response_cls, check_map)

        self.testCaseChecked("INT_9001_0008", _AUTHOR)
    # end def test_continuous_power
# end class PMW3816andPMW3826InterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
