#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.common.feature_1e30.robustness
:brief: HID++ 2.0 ``I2CDirectAccess`` robustness test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2022/12/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.i2cdirectaccess import I2CDirectAccess
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.i2cdirectaccessutils import I2CDirectAccessTestUtils
from pytestbox.device.hidpp20.common.feature_1e30.i2cdirectaccess import I2CDirectAccessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class I2CDirectAccessRobustnessTestCase(I2CDirectAccessTestCase):
    """
    Validate ``I2CDirectAccess`` robustness test cases
    """

    @features("Feature1E30")
    @level("Robustness")
    def test_get_nb_devices_software_id(self):
        """
        Validate ``GetNbDevices`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(I2CDirectAccess.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetNbDevices request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1e30.get_nb_devices_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1e30_index)
            report.software_id = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1e30.get_nb_devices_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetNbDevicesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            I2CDirectAccessTestUtils.GetNbDevicesResponseChecker.check_fields(
                self, response, self.feature_1e30.get_nb_devices_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1E30_0001#1", _AUTHOR)
    # end def test_get_nb_devices_software_id

    @features("Feature1E30")
    @level("Robustness")
    def test_get_selected_device_software_id(self):
        """
        Validate ``GetSelectedDevice`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(I2CDirectAccess.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetSelectedDevice request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1e30.get_selected_device_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1e30_index)
            report.software_id = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1e30.get_selected_device_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetSelectedDeviceResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            I2CDirectAccessTestUtils.GetSelectedDeviceResponseChecker.check_fields(
                self, response, self.feature_1e30.get_selected_device_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1E30_0001#2", _AUTHOR)
    # end def test_get_selected_device_software_id

    @features("Feature1E30")
    @features("Feature1E30WithI2cPeripheral")
    @level("Robustness")
    def test_select_device_software_id(self):
        """
        Validate ``SelectDevice`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.DeviceIdx.AccessConfig.0xPP

        SwID boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(I2CDirectAccess.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SelectDevice request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1e30.select_device_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1e30_index,
                device_idx=0x00,
                access_config=I2CDirectAccess.AccessConfig())
            report.software_id = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1e30.select_device_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SelectDeviceResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            I2CDirectAccessTestUtils.SelectDeviceResponseChecker.check_fields(
                self, response, self.feature_1e30.select_device_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1E30_0001#3", _AUTHOR)
    # end def test_select_device_software_id

    @features("Feature1E30")
    @features("Feature1E30WithI2cPeripheral")
    @level("Robustness")
    def test_i2c_read_direct_access_software_id(self):
        """
        Validate ``I2CReadDirectAccess`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.NBytes.RegisterAddress.0xPP

        SwID boundary values [0..F]
        """
        n_bytes = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(I2CDirectAccess.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send I2CReadDirectAccess request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1e30.i2c_read_direct_access_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1e30_index,
                n_bytes=n_bytes,
                register_address=0x00)
            report.software_id = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1e30.i2c_read_direct_access_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check I2CReadDirectAccessResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = I2CDirectAccessTestUtils.I2CReadDirectAccessResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "n_bytes": (checker.check_n_bytes, n_bytes),
            })
            checker.check_fields(self, response, self.feature_1e30.i2c_read_direct_access_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1E30_0001#4", _AUTHOR)
    # end def test_i2c_read_direct_access_software_id

    @features("Feature1E30")
    @features("Feature1E30WithI2cPeripheral")
    @level("Robustness")
    def test_i2c_write_direct_access_software_id(self):
        """
        Validate ``I2CWriteDirectAccess`` software id field is ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.NBytes.RegisterAddress.DataIn1.DataIn2.DataIn3.
        DataIn4.DataIn5.DataIn6.DataIn7.DataIn8.DataIn9.DataIn10.DataIn11.DataIn12.DataIn13.DataIn14

        SwID boundary values [0..F]
        """
        n_bytes = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(I2CDirectAccess.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send I2CWriteDirectAccess request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1e30.i2c_write_direct_access_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1e30_index,
                n_bytes=n_bytes,
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
            report.software_id = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1e30.i2c_write_direct_access_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check I2CWriteDirectAccessResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = I2CDirectAccessTestUtils.I2CWriteDirectAccessResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "n_bytes": (checker.check_n_bytes, n_bytes),
            })
            checker.check_fields(self, response, self.feature_1e30.i2c_write_direct_access_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1E30_0001#5", _AUTHOR)
    # end def test_i2c_write_direct_access_software_id

    @features("Feature1E30")
    @level("Robustness")
    def test_get_nb_devices_padding(self):
        """
        Validate ``GetNbDevices`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1e30.get_nb_devices_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetNbDevices request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1e30_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1e30.get_nb_devices_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetNbDevicesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            I2CDirectAccessTestUtils.GetNbDevicesResponseChecker.check_fields(
                self, response, self.feature_1e30.get_nb_devices_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1E30_0002#1", _AUTHOR)
    # end def test_get_nb_devices_padding

    @features("Feature1E30")
    @level("Robustness")
    def test_get_selected_device_padding(self):
        """
        Validate ``GetSelectedDevice`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1e30.get_selected_device_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetSelectedDevice request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1e30_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1e30.get_selected_device_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetSelectedDeviceResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            I2CDirectAccessTestUtils.GetSelectedDeviceResponseChecker.check_fields(
                self, response, self.feature_1e30.get_selected_device_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1E30_0002#2", _AUTHOR)
    # end def test_get_selected_device_padding

    @features("Feature1E30")
    @features("Feature1E30WithI2cPeripheral")
    @level("Robustness")
    def test_select_device_padding(self):
        """
        Validate ``SelectDevice`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.DeviceIdx.AccessConfig.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1e30.select_device_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SelectDevice request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1e30_index,
                device_idx=0x00,
                access_config=I2CDirectAccess.AccessConfig())
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1e30.select_device_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SelectDeviceResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            I2CDirectAccessTestUtils.SelectDeviceResponseChecker.check_fields(
                self, response, self.feature_1e30.select_device_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1E30_0002#3", _AUTHOR)
    # end def test_select_device_padding

    @features("Feature1E30")
    @features("Feature1E30WithI2cPeripheral")
    @level("Robustness")
    def test_i2c_read_direct_access_padding(self):
        """
        Validate ``I2CReadDirectAccess`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.NBytes.RegisterAddress.0xPP

        Padding (PP) boundary values [00..FF]
        """
        n_bytes = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1e30.i2c_read_direct_access_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send I2CReadDirectAccess request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1e30_index,
                n_bytes=n_bytes,
                register_address=0x00)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1e30.i2c_read_direct_access_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check I2CReadDirectAccessResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = I2CDirectAccessTestUtils.I2CReadDirectAccessResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "n_bytes": (checker.check_n_bytes, n_bytes),
            })
            checker.check_fields(self, response, self.feature_1e30.i2c_read_direct_access_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1E30_0002#4", _AUTHOR)
    # end def test_i2c_read_direct_access_padding

    @features("Feature1E30")
    @features("Feature1E30WithI2cPeripheral")
    @level("Robustness")
    def test_reserved_bits_of_access_config(self):
        """
        Validate the reserved bits of accessConfig are ignored by the FW
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over access_config in [0x03, 0x05, 0x06, 0x07, 0x80, 0xFC, 0xFF]")
        # --------------------------------------------------------------------------------------------------------------
        for access_config in [0x03, 0x05, 0x06, 0x07, 0x80, 0xFC, 0xFF]:
            access_config = I2CDirectAccess.AccessConfig(disable_fw_access=access_config & self.fw_access.MASK,
                                                         reserved=access_config >> 1)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send selectDevice request with accessConfig = {access_config}")
            # ----------------------------------------------------------------------------------------------------------
            response = I2CDirectAccessTestUtils.HIDppHelper.select_device(test_case=self,
                                                                          device_idx=0,
                                                                          access_config=access_config)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Wait selectDevice response and check the accessConfig equals {access_config}")
            # ----------------------------------------------------------------------------------------------------------
            checker = I2CDirectAccessTestUtils.SelectDeviceResponseChecker
            check_map = checker.get_default_check_map(self)
            access_config_check_map = I2CDirectAccessTestUtils.AccessConfigChecker.get_check_map(
                access_config=access_config)
            check_map.update({
                "access_config": (checker.check_access_config, access_config_check_map)
            })
            checker.check_fields(self, response, self.feature_1e30.select_device_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1E30_0003", _AUTHOR)
    # end def test_reserved_bits_of_access_config
# end class I2CDirectAccessRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
