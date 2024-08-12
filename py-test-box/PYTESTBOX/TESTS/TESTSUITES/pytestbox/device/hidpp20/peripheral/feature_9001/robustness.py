#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.peripheral.feature_9001.robustness
:brief: HID++ 2.0 ``PMW3816andPMW3826`` robustness test suite
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
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import PMW3816andPMW3826
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
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
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PMW3816andPMW3826RobustnessTestCase(PMW3816andPMW3826TestCase):
    """
    Validate ``PMW3816andPMW3826`` robustness test cases
    """

    @features("Feature9001")
    @level("Robustness")
    def test_read_sensor_register_software_id(self):
        """
        Validate ``ReadSensorRegister`` software id field is ignored by the firmware

        [0] readSensorRegister(registerAddress) -> registerValue

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RegisterAddress.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        register_address = \
            SPI_PERIPHERAL_REGISTER_DICT[self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName]["product_id"]["address"]
        register_value = \
            SPI_PERIPHERAL_REGISTER_DICT[self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName]["product_id"]["value"]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(PMW3816andPMW3826.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadSensorRegister request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.read_sensor_register(
                test_case=self,
                register_address=register_address,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ReadSensorRegisterResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = PMW3816andPMW3826TestUtils.ReadSensorRegisterResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "register_value": (checker.check_register_value, register_value)
            })
            checker.check_fields(self, response, self.feature_9001.read_sensor_register_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9001_0001#1", _AUTHOR)
    # end def test_read_sensor_register_software_id

    @features("Feature9001")
    @level("Robustness")
    def test_write_sensor_register_software_id(self):
        """
        Validate ``WriteSensorRegister`` software id field is ignored by the firmware

        [1] writeSensorRegister(registerAddress, registerValue) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RegisterAddress.RegisterValue.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        register_address = \
            SPI_PERIPHERAL_REGISTER_DICT[self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName]["dpi"]["address"]
        register_value = HexList(0x00)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(PMW3816andPMW3826.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send WriteSensorRegister request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.write_sensor_register(
                test_case=self,
                register_address=register_address,
                register_value=register_value,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check WriteSensorRegisterResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(
                self, response, self.feature_9001.write_sensor_register_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9001_0001#2", _AUTHOR)
    # end def test_write_sensor_register_software_id

    @features("Feature9001")
    @level("Robustness")
    def test_reset_sensor_software_id(self):
        """
        Validate ``ResetSensor`` software id field is ignored by the firmware

        [2] resetSensor() -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(PMW3816andPMW3826.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ResetSensor request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.reset_sensor(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ResetSensorResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(
                self, response, self.feature_9001.reset_sensor_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9001_0001#3", _AUTHOR)
    # end def test_reset_sensor_software_id

    @features("Feature9001")
    @level("Robustness")
    @skip("NotSupported")
    def test_shutdown_sensor_software_id(self):
        """
        Validate ``ShutdownSensor`` software id field is ignored by the firmware

        [3] shutdownSensor() -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(PMW3816andPMW3826.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ShutdownSensor request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.shutdown_sensor(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ShutdownSensorResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(
                self, response, self.feature_9001.shutdown_sensor_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9001_0001#4", _AUTHOR)
    # end def test_shutdown_sensor_software_id

    @features("Feature9001")
    @level("Robustness")
    def test_tracking_test_software_id(self):
        """
        Validate ``TrackingTest`` software id field is ignored by the firmware

        [4] trackingTest(count) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.Count.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        count = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(PMW3816andPMW3826.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send TrackingTest request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.tracking_test(
                test_case=self,
                count=count,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check TrackingTestResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(
                self, response, self.feature_9001.tracking_test_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9001_0001#5", _AUTHOR)
    # end def test_tracking_test_software_id

    @features("Feature9001v0")
    @level("Robustness")
    @bugtracker("Unexpected_FrameCapture_Response")
    def test_frame_capture_software_id_v0(self):
        """
        Validate ``FrameCaptureV0`` software id field is ignored by the firmware

        [5] frameCapture() -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(PMW3816andPMW3826.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send FrameCaptureV0 request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.frame_capture(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check FrameCaptureResponseV0 fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(
                self, response, self.feature_9001.frame_capture_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9001_0001#6", _AUTHOR)
    # end def test_frame_capture_software_id_v0

    @features("Feature9001v1")
    @level("Robustness")
    def test_get_strap_data_software_id_v1(self):
        """
        Validate ``GetStrapDataV1`` software id field is ignored by the firmware

        [5] getStrapData() -> sensor, strapMeasurementX

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
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
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(PMW3816andPMW3826.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetStrapDataV1 request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.get_strap_data(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetStrapDataResponseV1 fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = PMW3816andPMW3826TestUtils.GetStrapDataResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "sensor": (checker.check_sensor, sensor),
                "strap_measurement_x": (checker.check_strap_measurement_x, strap_measurement_x)
            })
            checker.check_fields(self, response, self.feature_9001.get_strap_data_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9001_0001#7", _AUTHOR)
    # end def test_get_strap_data_software_id_v1

    @features("Feature9001")
    @level("Robustness")
    def test_continuous_power_software_id(self):
        """
        Validate ``ContinuousPower`` software id field is ignored by the firmware

        [6] continuousPower() -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(PMW3816andPMW3826.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ContinuousPower request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.continuous_power(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ContinuousPowerResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(
                self, response, self.feature_9001.continuous_power_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9001_0001#8", _AUTHOR)
    # end def test_continuous_power_software_id

    @features("Feature9001")
    @level("Robustness")
    def test_read_sensor_register_padding(self):
        """
        Validate ``ReadSensorRegister`` padding bytes are ignored by the firmware

        [0] readSensorRegister(registerAddress) -> registerValue

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RegisterAddress.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        register_address = \
            SPI_PERIPHERAL_REGISTER_DICT[self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName]["product_id"]["address"]
        register_value = \
            SPI_PERIPHERAL_REGISTER_DICT[self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName]["product_id"]["value"]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_9001.read_sensor_register_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadSensorRegister request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.read_sensor_register(
                test_case=self,
                register_address=register_address,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ReadSensorRegisterResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = PMW3816andPMW3826TestUtils.ReadSensorRegisterResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "register_value": (checker.check_register_value, register_value)
            })
            checker.check_fields(self, response, self.feature_9001.read_sensor_register_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9001_0002#1", _AUTHOR)
    # end def test_read_sensor_register_padding

    @features("Feature9001")
    @level("Robustness")
    def test_write_sensor_register_padding(self):
        """
        Validate ``WriteSensorRegister`` padding bytes are ignored by the firmware

        [1] writeSensorRegister(registerAddress, registerValue) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RegisterAddress.RegisterValue.0xPP

        Padding (PP) boundary values [00..FF]
        """
        register_address = \
            SPI_PERIPHERAL_REGISTER_DICT[self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName]["product_id"]["address"]
        register_value = HexList(0x00)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_9001.write_sensor_register_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send WriteSensorRegister request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.write_sensor_register(
                test_case=self,
                register_address=register_address,
                register_value=register_value,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check WriteSensorRegisterResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(
                self, response, self.feature_9001.write_sensor_register_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9001_0002#2", _AUTHOR)
    # end def test_write_sensor_register_padding

    @features("Feature9001")
    @level("Robustness")
    def test_reset_sensor_padding(self):
        """
        Validate ``ResetSensor`` padding bytes are ignored by the firmware

        [2] resetSensor() -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_9001.reset_sensor_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ResetSensor request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.reset_sensor(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ResetSensorResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(
                self, response, self.feature_9001.reset_sensor_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9001_0002#3", _AUTHOR)
    # end def test_reset_sensor_padding

    @features("Feature9001")
    @level("Robustness")
    @skip("NotSupported")
    def test_shutdown_sensor_padding(self):
        """
        Validate ``ShutdownSensor`` padding bytes are ignored by the firmware

        [3] shutdownSensor() -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_9001.shutdown_sensor_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ShutdownSensor request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.shutdown_sensor(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ShutdownSensorResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(
                self, response, self.feature_9001.shutdown_sensor_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9001_0002#4", _AUTHOR)
    # end def test_shutdown_sensor_padding

    @features("Feature9001")
    @level("Robustness")
    def test_tracking_test_padding(self):
        """
        Validate ``TrackingTest`` padding bytes are ignored by the firmware

        [4] trackingTest(count) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.Count.0xPP

        Padding (PP) boundary values [00..FF]
        """
        count = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_9001.tracking_test_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send TrackingTest request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.tracking_test(
                test_case=self,
                count=count,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check TrackingTestResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(
                self, response, self.feature_9001.tracking_test_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9001_0002#5", _AUTHOR)
    # end def test_tracking_test_padding

    @features("Feature9001v0")
    @level("Robustness")
    @bugtracker("Unexpected_FrameCapture_Response")
    def test_frame_capture_padding_v0(self):
        """
        Validate ``FrameCaptureV0`` padding bytes are ignored by the firmware

        [5] frameCapture() -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_9001.frame_capture_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send FrameCaptureV0 request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.frame_capture(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check FrameCaptureResponseV0 fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(
                self, response, self.feature_9001.frame_capture_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9001_0002#6", _AUTHOR)
    # end def test_frame_capture_padding_v0

    @features("Feature9001v1")
    @level("Robustness")
    def test_get_strap_data_padding_v1(self):
        """
        Validate ``GetStrapDataV1`` padding bytes are ignored by the firmware

        [5] getStrapData() -> sensor, strapMeasurementX

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
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
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_9001.get_strap_data_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetStrapDataV1 request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.get_strap_data(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetStrapDataResponseV1 fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = PMW3816andPMW3826TestUtils.GetStrapDataResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "sensor": (checker.check_sensor, sensor),
                "strap_measurement_x": (checker.check_strap_measurement_x, strap_measurement_x)
            })
            checker.check_fields(self, response, self.feature_9001.get_strap_data_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9001_0002#7", _AUTHOR)
    # end def test_get_strap_data_padding_v1

    @features("Feature9001")
    @level("Robustness")
    def test_continuous_power_padding(self):
        """
        Validate ``ContinuousPower`` padding bytes are ignored by the firmware

        [6] continuousPower() -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_9001.continuous_power_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ContinuousPower request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.continuous_power(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ContinuousPowerResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(
                self, response, self.feature_9001.continuous_power_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9001_0002#8", _AUTHOR)
    # end def test_continuous_power_padding

    @features("Feature9001")
    @level("Robustness")
    def test_write_on_read_only_register(self):
        """
        Validate Write action performed on a Register which supports Read only.
        """
        sensor_map = SPI_PERIPHERAL_REGISTER_DICT[self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over Read only registers in [0x00, 0x01, 0x03, 0x04, 0x05, 0x06, 0x07,"
                                 "0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x16, 0x59, 0x5F]")
        # --------------------------------------------------------------------------------------------------------------
        for register in self.config.F_ReadOnlyRegisters:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send Write Register with value=0xFF on the selected register.")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.write_sensor_register(
                test_case=self,
                register_address=sensor_map[register]["address"],
                register_value=HexList(0xFF))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "validate write sensor register response fields.")
            # ----------------------------------------------------------------------------------------------------------
            checker = DeviceTestUtils.MessageChecker
            check_map = {}
            checker.check_fields(self, message=response,
                                 expected_cls=self.feature_9001.write_sensor_register_response_cls,
                                 check_map=check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9001_0003", _AUTHOR)
    # end def test_write_on_read_only_register

    @features("Feature9001")
    @level("Robustness")
    def test_read_on_write_only_register(self):
        """
        Validate Read action performed on a Register which supports Write only.
        """
        sensor_map = SPI_PERIPHERAL_REGISTER_DICT[self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over Write only registers in [0x3A, 0x3B]")
        # --------------------------------------------------------------------------------------------------------------
        for register in self.config.F_WriteOnlyRegisters:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send Read Register for the selected register.")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.read_sensor_register(
                self, register_address=sensor_map[register]["address"])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verify the register value is 0x00.")
            # ----------------------------------------------------------------------------------------------------------
            checker = PMW3816andPMW3826TestUtils.ReadSensorRegisterResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "register_value": (checker.check_register_value, HexList(0x0))
            })
            checker.check_fields(self, response, self.feature_9001.read_sensor_register_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9001_0004", _AUTHOR)
    # end def test_read_on_write_only_register

    @features("Feature9001")
    @level("Robustness")
    def test_read_invalid_register(self):
        """
        Validate Invalid Register read through Read Sensor always returns 0x00
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop through several interesting values in Invalid Register range.")
        # --------------------------------------------------------------------------------------------------------------
        for register in compute_sup_values([self.config.F_MaxRegisterAddress]):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send Read Sensor for the selected Register.")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.read_sensor_register(
                self, register_address=HexList(register))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verify the Returned value is 0x00.")
            # ----------------------------------------------------------------------------------------------------------
            checker = PMW3816andPMW3826TestUtils.ReadSensorRegisterResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "register_value": (checker.check_register_value, HexList(0xFF))
            })
            checker.check_fields(self, response, self.feature_9001.read_sensor_register_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9001_0005", _AUTHOR)
    # end def test_read_invalid_register

    @features("Feature9001")
    @level("Robustness")
    def test_write_invalid_register(self):
        """
        Validate Invalid Register written through Write Sensor does not return an error.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop through several interesting values in Invalid Register range.")
        # --------------------------------------------------------------------------------------------------------------
        for register in compute_sup_values([self.config.F_MaxRegisterAddress]):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send Write Sensor for the selected Register with value=0x00")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.write_sensor_register(
                test_case=self,
                register_address=HexList(register),
                register_value=HexList(0x0))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verify the response is success.")
            # ----------------------------------------------------------------------------------------------------------
            checker = DeviceTestUtils.MessageChecker
            check_map = {}
            checker.check_fields(self, message=response,
                                 expected_cls=self.feature_9001.write_sensor_register_response_cls,
                                 check_map=check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9001_0006", _AUTHOR)
    # end def test_write_invalid_register

    @features("Feature9001")
    @level("Robustness")
    def test_write_and_read_invalid_register(self):
        """
        Validate Invalid Register written through Write Sensor and read through Read Sensor returns 0.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop through several interesting values in Invalid Register range.")
        # --------------------------------------------------------------------------------------------------------------
        for register in compute_sup_values([self.config.F_MaxRegisterAddress]):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send Write Sensor for the selected Register with value = 0xFF")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.write_sensor_register(
                test_case=self,
                register_address=HexList(register),
                register_value=HexList(0xFF))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "validate write sensor register response fields.")
            # ----------------------------------------------------------------------------------------------------------
            checker = DeviceTestUtils.MessageChecker
            check_map = {}
            checker.check_fields(self, message=response,
                                 expected_cls=self.feature_9001.write_sensor_register_response_cls,
                                 check_map=check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send Read Sensor for the selected Register.")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.read_sensor_register(
                self, register_address=HexList(register))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verify the Returned value is 0xFF.")
            # ----------------------------------------------------------------------------------------------------------
            checker = PMW3816andPMW3826TestUtils.ReadSensorRegisterResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "register_value": (checker.check_register_value, HexList(0xFF))
            })
            checker.check_fields(self, response, self.feature_9001.read_sensor_register_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_9001_0007", _AUTHOR)
    # end def test_write_and_read_invalid_register
# end class PMW3816andPMW3826RobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
