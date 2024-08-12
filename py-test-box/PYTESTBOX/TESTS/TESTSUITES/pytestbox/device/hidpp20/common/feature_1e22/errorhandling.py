#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.common.feature_1e22.errorhandling
:brief: HID++ 2.0 ``SPIDirectAccess`` error handling test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2022/11/21
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.spidirectaccessutils import SPIDirectAccessTestUtils
from pytestbox.device.hidpp20.common.feature_1e22.spidirectaccess import SPIDirectAccessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SPIDirectAccessErrorHandlingTestCase(SPIDirectAccessTestCase):
    """
    Validate ``SPIDirectAccess`` errorhandling test cases
    """

    @features("Feature1E22")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_1e22.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetNbDevices request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1e22.get_nb_devices_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1e22_index)
            report.function_index = function_index

            SPIDirectAccessTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_FUNCTION_ID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_1E22_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature1E22")
    @features("NoFeature1E22WithSpiPeripheral")
    @level("ErrorHandling")
    def test_not_allowed_selected_device_request(self):
        """
        Validate that sending selectDevice request will raise an NOT_ALLOWED(0x05) error, if the
        getNbDevice.numberOfDevice is 0
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send selectDevice request with deviceIdx = 0, accessConfig = 0")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1e22.select_device_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1e22_index,
            device_idx=0,
            access_config=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check NOT_ALLOWED(0x05) error code is returned by the DUT")
        # --------------------------------------------------------------------------------------------------------------
        SPIDirectAccessTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_1E22_0002", _AUTHOR)
    # end def test_not_allowed_selected_device_request

    @features("Feature1E22")
    @features("Feature1E22WithSpiPeripheral")
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
            report = self.feature_1e22.select_device_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1e22_index,
                device_idx=invalid_device_idx,
                access_config=0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check INVALID_ARGUMENT(0x02) error code is returned by the DUT")
            # ----------------------------------------------------------------------------------------------------------
            SPIDirectAccessTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1E22_0003", _AUTHOR)
    # end def test_invalid_device_idx

    @features("Feature1E22")
    @features("NoFeature1E22WithSpiPeripheral")
    @level("ErrorHandling")
    def test_not_allowed_spi_direct_access_request(self):
        """
        Validate that sending spiDirectAccess request will raise an NOT_ALLOWED(0x05) error, if the
        getNbDevices.numberOfDevice is 0
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send spiDirectAccess request with nBytes = 1, DataIn = [0x00]")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1e22.spi_direct_access_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1e22_index,
            n_bytes=1,
            data_in_1=0,
            data_in_2=0,
            data_in_3=0,
            data_in_4=0,
            data_in_5=0,
            data_in_6=0,
            data_in_7=0,
            data_in_8=0,
            data_in_9=0,
            data_in_10=0,
            data_in_11=0,
            data_in_12=0,
            data_in_13=0,
            data_in_14=0,
            data_in_15=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check NOT_ALLOWED(0x05) error code is returned by the DUT")
        # --------------------------------------------------------------------------------------------------------------
        SPIDirectAccessTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_1E22_0004", _AUTHOR)
    # end def test_not_allowed_spi_direct_access_request

    @features("Feature1E22")
    @features("Feature1E22WithSpiPeripheral")
    @level("ErrorHandling")
    def test_invalid_n_bytes(self):
        """
        Validate that spiDirectAccess request will raise an INVALID_ARGUMENT(0x02) error, if the nBytes is equal to 0
        or greater than 15
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop: invalid_number_of_bytes in [0x00, 0x10, 0x20, 0x40, 0x80, 0xFF]")
        # --------------------------------------------------------------------------------------------------------------
        for invalid_number_of_bytes in [0x00, 0x10, 0x20, 0x40, 0x80, 0xFF]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, "Send spiDirectAccess request with nBytes = invalid_number_of_bytes, DataIn = [0x00]")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1e22.spi_direct_access_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1e22_index,
                n_bytes=invalid_number_of_bytes,
                data_in_1=0,
                data_in_2=0,
                data_in_3=0,
                data_in_4=0,
                data_in_5=0,
                data_in_6=0,
                data_in_7=0,
                data_in_8=0,
                data_in_9=0,
                data_in_10=0,
                data_in_11=0,
                data_in_12=0,
                data_in_13=0,
                data_in_14=0,
                data_in_15=0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check INVALID_ARGUMENT(0x02) error code is returned by the DUT")
            # ----------------------------------------------------------------------------------------------------------
            SPIDirectAccessTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1E22_0005", _AUTHOR)
    # end def test_invalid_n_bytes
# end class SPIDirectAccessErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
