#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.common.feature_1e30.errorhandling
:brief: HID++ 2.0 ``I2CDirectAccess`` error handling test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2022/12/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import skip

from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyhid.hidpp.features.common.i2cdirectaccess import I2CDirectAccess
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.i2cdirectaccessutils import I2CDirectAccessTestUtils
from pytestbox.device.hidpp20.common.feature_1e30.i2cdirectaccess import I2CDirectAccessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class I2CDirectAccessErrorHandlingTestCase(I2CDirectAccessTestCase):
    """
    Validate ``I2CDirectAccess`` errorhandling test cases
    """

    @features("Feature1E30")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_1e30.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetNbDevices request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1e30.get_nb_devices_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1e30_index)
            report.function_index = function_index

            I2CDirectAccessTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_FUNCTION_ID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_1E30_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature1E30")
    @features("NoFeature1E30WithI2cPeripheral")
    @level("ErrorHandling")
    def test_not_allowed_selected_device_request(self):
        """
        Validate that sending selectDevice request will raise an NOT_ALLOWED(0x05) error, if the
        getNbDevice.numberOfDevice is 0
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send selectDevice request with deviceIdx = 0, accessConfig = 0")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1e30.select_device_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1e30_index,
            device_idx=0,
            access_config=I2CDirectAccess.AccessConfig())

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check NOT_ALLOWED(0x05) error code is returned by the DUT")
        # --------------------------------------------------------------------------------------------------------------
        I2CDirectAccessTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_1E30_0002", _AUTHOR)
    # end def test_not_allowed_selected_device_request

    @features("Feature1E30")
    @features("Feature1E30WithI2cPeripheral")
    @level("ErrorHandling")
    def test_invalid_device_idx(self):
        """
        Validate that sending selectDevice request will raise an INVALID_ARGUMENT(0x02) error, if the deviceIdx is
        greater than or equal to getNbDevices.numberOfDevices
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop: invalid_device_index in range(getNbDevice.numberOfDevice, 0xFF)")
        # --------------------------------------------------------------------------------------------------------------
        for invalid_device_idx in compute_wrong_range(value=list(range(self.config.F_NumberOfDevices)), max_value=0xFF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send selectDevice request with deviceIdx = {invalid_device_idx}, "
                                     "accessConfig = 0")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1e30.select_device_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1e30_index,
                device_idx=invalid_device_idx,
                access_config=I2CDirectAccess.AccessConfig())

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check INVALID_ARGUMENT(0x02) error code is returned by the DUT")
            # ----------------------------------------------------------------------------------------------------------
            I2CDirectAccessTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1E30_0003", _AUTHOR)
    # end def test_invalid_device_idx

    @features("Feature1E30")
    @features("NoFeature1E30WithI2cPeripheral")
    @level("ErrorHandling")
    def test_not_allowed_i2c_read_direct_access_request(self):
        """
        Validate that sending i2cReadDirectAccess request will raise an NOT_ALLOWED(0x05) error, if the
        getNbDevices.numberOfDevice is 0
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send i2cReadDirect request with nBytes = 1, registerAddress = 0x00")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1e30.i2c_read_direct_access_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1e30_index,
            n_bytes=1,
            register_address=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check NOT_ALLOWED(0x05) error code is returned by the DUT")
        # --------------------------------------------------------------------------------------------------------------
        I2CDirectAccessTestUtils.HIDppHelper.send_report_wait_error(test_case=self,
                                                                    report=report,
                                                                    error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_1E30_0004", _AUTHOR)
    # end def test_not_allowed_i2c_read_direct_access_request

    @features("Feature1E30")
    @features("Feature1E30WithI2cPeripheral")
    @level("ErrorHandling")
    def test_invalid_n_bytes_wih_i2c_read_direct_access(self):
        """
        Validate that sending i2cReadDirectAccess request will raise an INVALID_ARGUMENT(0x02) error, if the nBytes is
        equal to 0 or greater than 15
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop: invalid_number_of_bytes in [0x00, 0x10, 0x20, 0x40, 0x80, 0xFF]")
        # --------------------------------------------------------------------------------------------------------------
        for invalid_number_of_bytes in [0x00, 0x10, 0x20, 0x40, 0x80, 0xFF]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send i2cReadDirectAccess request with nBytes = {invalid_number_of_bytes}, "
                                     "registerAddress = 0x00")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1e30.i2c_read_direct_access_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1e30_index,
                n_bytes=invalid_number_of_bytes,
                register_address=0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check INVALID_ARGUMENT(0x02) error code is returned by the DUT")
            # ----------------------------------------------------------------------------------------------------------
            I2CDirectAccessTestUtils.HIDppHelper.send_report_wait_error(test_case=self,
                                                                        report=report,
                                                                        error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1E30_0005", _AUTHOR)
    # end def test_invalid_n_bytes_wih_i2c_read_direct_access

    @features("Feature1E30")
    @features("Feature1E30WithI2cPeripheral")
    @level("ErrorHandling")
    def test_mismatch_needed_bytes(self):
        """
        Validate that sending i2cReadDirectAccess request will raise an INVALID_ARGUMENT(0x02) error, if the nBytes
        doesn't equal the number of bytes of the needed bytes.
        """
        mismatch_needed_bytes = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send i2cReadDirectAccess request with nBytes = {mismatch_needed_bytes}, "
                                 "registerAddress = 0x00")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1e30.i2c_read_direct_access_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1e30_index,
            n_bytes=mismatch_needed_bytes,
            register_address=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check INVALID_ARGUMENT(0x02) error code is returned by the DUT")
        # --------------------------------------------------------------------------------------------------------------
        I2CDirectAccessTestUtils.HIDppHelper.send_report_wait_error(test_case=self,
                                                                    report=report,
                                                                    error_codes=[ErrorCodes.INVALID_ARGUMENT])

        self.testCaseChecked("ERR_1E30_0006", _AUTHOR)
    # end def test_mismatch_needed_bytes

    @features("Feature1E30")
    @features("Feature1E30WithI2cPeripheral")
    @level("ErrorHandling")
    @skip("In development")
    def test_i2c_nack_with_read_direct_access(self):
        """
        Validate that sending i2cReadDirectAccess request will raise an HW_ERROR(0x04) error, if I2C packet has been
        NACKed
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send i2cReadDirectAccess request")
        # --------------------------------------------------------------------------------------------------------------
        # TODO - Make the I2C acknowledge bit in NAK state

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check HW_ERROR(0x04) error code is returned by the DUT")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1E30_0007", _AUTHOR)
    # end def test_i2c_nack_with_read_direct_access

    @features("Feature1E30")
    @features("NoFeature1E30WithI2cPeripheral")
    @level("ErrorHandling")
    def test_not_allowed_i2c_write_direct_access_request(self):
        """
        Validate that sending i2cWriteDirectAccess request will raise an NOT_ALLOWED(0x05) error, if the
        getNbDevices.numberOfDevice is 0
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send i2cWriteDirectAccess request with nBytes = 1, DataIn = [0x00]")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1e30.i2c_write_direct_access_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1e30_index,
            n_bytes=1,
            register_address=0x00,
            data_in_1=0x00,
            data_in_2=0x00,
            data_in_3=0x00,
            data_in_4=0x00,
            data_in_5=0x00,
            data_in_6=0x00,
            data_in_7=0x00,
            data_in_8=0x00,
            data_in_9=0x00,
            data_in_10=0x00,
            data_in_11=0x00,
            data_in_12=0x00,
            data_in_13=0x00,
            data_in_14=0x00)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check NOT_ALLOWED(0x05) error code is returned by the DUT")
        # --------------------------------------------------------------------------------------------------------------
        I2CDirectAccessTestUtils.HIDppHelper.send_report_wait_error(test_case=self,
                                                                    report=report,
                                                                    error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_1E30_0008", _AUTHOR)
    # end def test_not_allowed_i2c_write_direct_access_request

    @features("Feature1E30")
    @features("Feature1E30WithI2cPeripheral")
    @level("ErrorHandling")
    @bugtracker("I2cWriteDirectAccess_InvalidNBytes")
    def test_invalid_n_bytes_wih_i2c_write_direct_access(self):
        """
        Validate that sending i2cWriteDirectAccess request will raise an INVALID_ARGUMENT(0x02) error, if the nBytes
        is equal to 0 or greater than 13
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop: invalid_number_of_bytes in [0x00, 0x0E, 0x10, 0x20, 0x40, 0x80, 0xFF]")
        # --------------------------------------------------------------------------------------------------------------
        for invalid_number_of_bytes in [0x00, 0x0E, 0x10, 0x20, 0x40, 0x80, 0xFF]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, "Send i2cWriteDirectAccess request with nBytes = invalid_number_of_bytes, DataIn = [0x00]")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1e30.i2c_write_direct_access_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1e30_index,
                n_bytes=invalid_number_of_bytes,
                register_address=0x00,
                data_in_1=0x00,
                data_in_2=0x00,
                data_in_3=0x00,
                data_in_4=0x00,
                data_in_5=0x00,
                data_in_6=0x00,
                data_in_7=0x00,
                data_in_8=0x00,
                data_in_9=0x00,
                data_in_10=0x00,
                data_in_11=0x00,
                data_in_12=0x00,
                data_in_13=0x00,
                data_in_14=0x00)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check INVALID_ARGUMENT(0x02) error code is returned by the DUT")
            # ----------------------------------------------------------------------------------------------------------
            I2CDirectAccessTestUtils.HIDppHelper.send_report_wait_error(test_case=self,
                                                                        report=report,
                                                                        error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1E30_0009", _AUTHOR)
    # end def test_invalid_n_bytes_wih_i2c_write_direct_access

    @features("Feature1E30")
    @features("Feature1E30WithI2cPeripheral")
    @level("ErrorHandling")
    @skip("In development")
    def test_i2c_nack_with_write_direct_access(self):
        """
        Validate that sending i2cWriteDirectAccess request will raise an HW_ERROR(0x04) error, if I2C packet has been
        NACKed
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send i2cWriteDirectAccess request")
        # --------------------------------------------------------------------------------------------------------------
        # TODO - Make the I2C acknowledge bit in NAK state

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check HW_ERROR(0x04) error code is returned by the DUT")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1E30_0010", _AUTHOR)
    # end def test_i2c_nack_with_write_direct_access

    @features("Feature1E30")
    @features("Feature1E30WithI2cPeripheral")
    @level("ErrorHandling")
    def test_accessing_disabled_hidden_feature(self):
        """
        Validate that sending getNbDevice request will raise an NOT_ALLOWED(0x05) error, if the hidden features are
        not enabled.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power OFF -> ON the DUT to reset the device")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getNbDevice request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1e30.get_nb_devices_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1e30_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check NOT_ALLOWED(0x05) error code is returned by the DUT")
        # --------------------------------------------------------------------------------------------------------------
        I2CDirectAccessTestUtils.HIDppHelper.send_report_wait_error(test_case=self,
                                                                    report=report,
                                                                    error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_1E30_0011", _AUTHOR)
    # end def test_accessing_disabled_hidden_feature
# end class I2CDirectAccessErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
