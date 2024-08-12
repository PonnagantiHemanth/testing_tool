#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.peripheral.feature_9001.errorhandling
:brief: HID++ 2.0 ``PMW3816andPMW3826`` error handling test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2023/01/10
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import skip

from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicemanagedeactivatablefeaturesauthutils import \
    DeviceManageDeactivatableFeaturesAuthTestUtils
from pytestbox.device.base.pmw3816andpmw3826utils import PMW3816andPMW3826TestUtils
from pytestbox.device.base.spidirectaccessutils import SPI_PERIPHERAL_REGISTER_DICT
from pytestbox.device.hidpp20.peripheral.feature_9001.pmw3816andpmw3826 import PMW3816andPMW3826TestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PMW3816andPMW3826ErrorHandlingTestCase(PMW3816andPMW3826TestCase):
    """
    Validate ``PMW3816andPMW3826`` errorhandling test cases
    """

    @features("Feature9001")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        register_address = \
            SPI_PERIPHERAL_REGISTER_DICT[self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName]["product_id"]["address"]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_9001.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadSensorRegister request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_9001.read_sensor_register_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_9001_index,
                register_address=HexList(register_address))
            report.function_index = function_index

            PMW3816andPMW3826TestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_FUNCTION_ID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_9001_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature9001")
    @level("ErrorHandling")
    def test_read_sensor_without_enabling_manufacturing_features(self):
        """
        Validate Not Allowed Error is thrown when Read Sensor Register API is called without enabling Manufacturing
        Feature.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Disable TDE Manufacturing Feature")
        # --------------------------------------------------------------------------------------------------------------
        DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(
            self, disable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Read Sensor Register API")
        # --------------------------------------------------------------------------------------------------------------
        register_address = \
            SPI_PERIPHERAL_REGISTER_DICT[self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName]["product_id"]["address"]
        report = self.feature_9001.read_sensor_register_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_9001_index,
            register_address=register_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate NOT_ALLOWED error code is returned.")
        # --------------------------------------------------------------------------------------------------------------
        PMW3816andPMW3826TestUtils.HIDppHelper.send_report_wait_error(
            self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_9001_0002#1", _AUTHOR)
    # end def test_read_sensor_without_enabling_manufacturing_features

    @features("Feature9001")
    @level("ErrorHandling")
    def test_write_sensor_without_enabling_manufacturing_features(self):
        """
        Validate Not Allowed Error is thrown when Write Sensor Register API is called without enabling Manufacturing
        Feature.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Disable TDE Manufacturing Feature")
        # --------------------------------------------------------------------------------------------------------------
        DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(
            self, disable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Write Sensor Register API")
        # --------------------------------------------------------------------------------------------------------------
        register_address = \
            SPI_PERIPHERAL_REGISTER_DICT[self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName]["product_id"]["address"]
        report = self.feature_9001.write_sensor_register_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_9001_index,
            register_address=register_address,
            register_value=HexList(0x0))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate NOT_ALLOWED error code is returned.")
        # --------------------------------------------------------------------------------------------------------------
        PMW3816andPMW3826TestUtils.HIDppHelper.send_report_wait_error(
            self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_9001_0002#2", _AUTHOR)
    # end def test_write_sensor_without_enabling_manufacturing_features

    @features("Feature9001")
    @level("ErrorHandling")
    def test_reset_sensor_without_enabling_manufacturing_features(self):
        """
        Validate Not Allowed Error is thrown when Reset Sensor API is called without enabling Manufacturing Feature.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Disable TDE Manufacturing Feature")
        # --------------------------------------------------------------------------------------------------------------
        DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(
            self, disable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Reset Sensor API")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_9001.reset_sensor_cls(
                device_index=ChannelUtils.get_device_index(self),
                feature_index=self.feature_9001_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate NOT_ALLOWED error code is returned.")
        # --------------------------------------------------------------------------------------------------------------
        PMW3816andPMW3826TestUtils.HIDppHelper.send_report_wait_error(
            self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_9001_0002#3", _AUTHOR)
    # end def test_reset_sensor_without_enabling_manufacturing_features

    @features("Feature9001")
    @level("ErrorHandling")
    @skip("NotSupported")
    def test_shutdown_sensor_without_enabling_manufacturing_features(self):
        """
        Validate Not Allowed Error is thrown when Shutdown Sensor API is called without enabling Manufacturing
        Feature.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Disable TDE Manufacturing Feature")
        # --------------------------------------------------------------------------------------------------------------
        DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(
            self, disable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Shutdown Sensor API")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_9001.shutdown_sensor_cls(
            device_index=ChannelUtils.get_device_index(self),
            feature_index=self.feature_9001_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate NOT_ALLOWED error code is returned.")
        # --------------------------------------------------------------------------------------------------------------
        PMW3816andPMW3826TestUtils.HIDppHelper.send_report_wait_error(
            self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_9001_0002#4", _AUTHOR)
    # end def test_shutdown_sensor_without_enabling_manufacturing_features

    @features("Feature9001")
    @level("ErrorHandling")
    def test_tracking_test_without_enabling_manufacturing_features(self):
        """
        Validate Not Allowed Error is thrown when Tracking Test API is called without enabling Manufacturing Feature.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Disable TDE Manufacturing Feature")
        # --------------------------------------------------------------------------------------------------------------
        DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(
            self, disable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Tracking Test API with count=0")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_9001.tracking_test_cls(
            device_index=ChannelUtils.get_device_index(self),
            feature_index=self.feature_9001_index,
            count=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate NOT_ALLOWED error code is returned.")
        # --------------------------------------------------------------------------------------------------------------
        PMW3816andPMW3826TestUtils.HIDppHelper.send_report_wait_error(
            self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_9001_0002#5", _AUTHOR)
    # end def test_tracking_test_without_enabling_manufacturing_features

    @features("Feature9001v0")
    @level("ErrorHandling")
    def test_frame_capture_without_enabling_manufacturing_features(self):
        """
        Validate Not Allowed Error is thrown when Frame Capture API is called without enabling Manufacturing Feature.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Disable TDE Manufacturing Feature")
        # --------------------------------------------------------------------------------------------------------------
        DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(
            self, disable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Frame Capture API")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_9001.frame_capture_cls(
            device_index=ChannelUtils.get_device_index(self),
            feature_index=self.feature_9001_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate NOT_ALLOWED error code is returned.")
        # --------------------------------------------------------------------------------------------------------------
        PMW3816andPMW3826TestUtils.HIDppHelper.send_report_wait_error(
            self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])
        self.testCaseChecked("ERR_9001_0002#6", _AUTHOR)
    # end def test_frame_capture_without_enabling_manufacturing_features

    @features("Feature9001v1")
    @level("ErrorHandling")
    def test_strap_data_without_enabling_manufacturing_features(self):
        """
        Validate Not Allowed Error is thrown when Get Strap Data API is called without enabling Manufacturing Feature.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Disable TDE Manufacturing Feature")
        # --------------------------------------------------------------------------------------------------------------
        DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(
            self, disable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Get Strap Data API")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_9001.get_strap_data_cls(
            device_index=ChannelUtils.get_device_index(self),
            feature_index=self.feature_9001_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate NOT_ALLOWED error code is returned.")
        # --------------------------------------------------------------------------------------------------------------
        PMW3816andPMW3826TestUtils.HIDppHelper.send_report_wait_error(
            self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_9001_0002#7", _AUTHOR)
    # end def test_strap_data_without_enabling_manufacturing_features

    @features("Feature9001")
    @level("ErrorHandling")
    def test_continuous_power_without_enabling_manufacturing_features(self):
        """
        Validate Not Allowed Error is thrown when Continuous Power API is called without enabling Manufacturing
        Feature.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Disable TDE Manufacturing Feature")
        # --------------------------------------------------------------------------------------------------------------
        DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(
            self, disable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Continuous Power API")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_9001.continuous_power_cls(
            device_index=ChannelUtils.get_device_index(self),
            feature_index=self.feature_9001_index,
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate NOT_ALLOWED error code is returned.")
        # --------------------------------------------------------------------------------------------------------------
        PMW3816andPMW3826TestUtils.HIDppHelper.send_report_wait_error(
            self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_9001_0002#8", _AUTHOR)
    # end def test_continuous_power_without_enabling_manufacturing_features
# end class PMW3816andPMW3826ErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
