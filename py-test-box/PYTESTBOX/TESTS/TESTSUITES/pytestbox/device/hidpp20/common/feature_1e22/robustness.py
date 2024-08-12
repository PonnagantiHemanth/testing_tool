#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.common.feature_1e22.robustness
:brief: HID++ 2.0 ``SPIDirectAccess`` robustness test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2022/11/21
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.spidirectaccess import SPIDirectAccess
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.spidirectaccessutils import SPIDirectAccessTestUtils
from pytestbox.device.base.spidirectaccessutils import SPI_PERIPHERAL_REGISTER_DICT
from pytestbox.device.hidpp20.common.feature_1e22.spidirectaccess import SPIDirectAccessTestCase

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
class SPIDirectAccessRobustnessTestCase(SPIDirectAccessTestCase):
    """
    Validate ``SPIDirectAccess`` robustness test cases
    """

    @features("Feature1E22")
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
        for software_id in compute_inf_values(SPIDirectAccess.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetNbDevices request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1e22.get_nb_devices_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1e22_index)
            report.software_id = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1e22.get_nb_devices_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetNbDevicesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            SPIDirectAccessTestUtils.GetNbDevicesResponseChecker.check_fields(
                self, response, self.feature_1e22.get_nb_devices_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1E22_0001#1", _AUTHOR)
    # end def test_get_nb_devices_software_id

    @features("Feature1E22")
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
        for software_id in compute_inf_values(SPIDirectAccess.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetSelectedDevice request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1e22.get_selected_device_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1e22_index)
            report.software_id = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1e22.get_selected_device_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetSelectedDeviceResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = SPIDirectAccessTestUtils.GetSelectedDeviceResponseChecker
            checker.check_fields(self, response, self.feature_1e22.get_selected_device_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1E22_0001#2", _AUTHOR)
    # end def test_get_selected_device_software_id

    @features("Feature1E22")
    @features("Feature1E22WithSpiPeripheral")
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
        for software_id in compute_inf_values(SPIDirectAccess.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SelectDevice request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1e22.select_device_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1e22_index,
                device_idx=HexList(0x0),
                access_config=HexList(0x0))
            report.software_id = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1e22.select_device_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SelectDeviceResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = SPIDirectAccessTestUtils.SelectDeviceResponseChecker
            checker.check_fields(self, response, self.feature_1e22.select_device_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1E22_0001#3", _AUTHOR)
    # end def test_select_device_software_id

    @features("Feature1E22")
    @features("Feature1E22WithSpiPeripheral")
    @level("Robustness")
    def test_spi_direct_access_software_id(self):
        """
        Validate ``SpiDirectAccess`` software id field is ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.NBytes.DataIn1.DataIn2.DataIn3.DataIn4.DataIn5.
        DataIn6.DataIn7.DataIn8.DataIn9.DataIn10.DataIn11.DataIn12.DataIn13.DataIn14.DataIn15

        SwID boundary values [0..F]
        """
        n_bytes = 1
        optical_sensor_name = self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(SPIDirectAccess.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SpiDirectAccess request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1e22.spi_direct_access_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1e22_index,
                n_bytes=n_bytes,
                data_in_1=SPI_PERIPHERAL_REGISTER_DICT[optical_sensor_name]['product_id']['address'],
                data_in_2=HexList(0x0),
                data_in_3=HexList(0x0),
                data_in_4=HexList(0x0),
                data_in_5=HexList(0x0),
                data_in_6=HexList(0x0),
                data_in_7=HexList(0x0),
                data_in_8=HexList(0x0),
                data_in_9=HexList(0x0),
                data_in_10=HexList(0x0),
                data_in_11=HexList(0x0),
                data_in_12=HexList(0x0),
                data_in_13=HexList(0x0),
                data_in_14=HexList(0x0),
                data_in_15=HexList(0x0))
            report.software_id = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1e22.spi_direct_access_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SpiDirectAccessResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = SPIDirectAccessTestUtils.SpiDirectAccessResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "n_bytes": (checker.check_n_bytes, n_bytes),
                "data_out_1": (checker.check_data_out_1,
                               SPI_PERIPHERAL_REGISTER_DICT[optical_sensor_name]['product_id']['value']),
            })
            checker.check_fields(self, response, self.feature_1e22.spi_direct_access_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1E22_0001#4", _AUTHOR)
    # end def test_spi_direct_access_software_id

    @features("Feature1E22")
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
        request_cls = self.feature_1e22.get_nb_devices_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetNbDevices request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1e22_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1e22.get_nb_devices_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetNbDevicesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            SPIDirectAccessTestUtils.GetNbDevicesResponseChecker.check_fields(
                self, response, self.feature_1e22.get_nb_devices_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1E22_0002#1", _AUTHOR)
    # end def test_get_nb_devices_padding

    @features("Feature1E22")
    @level("Robustness")
    @bugtracker("GetSelectedDevice_PaddingBytesHandling")
    def test_get_selected_device_padding(self):
        """
        Validate ``GetSelectedDevice`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1e22.get_selected_device_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetSelectedDevice request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1e22_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1e22.get_selected_device_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetSelectedDeviceResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = SPIDirectAccessTestUtils.GetSelectedDeviceResponseChecker
            checker.check_fields(self, response, self.feature_1e22.get_selected_device_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1E22_0002#2", _AUTHOR)
    # end def test_get_selected_device_padding

    @features("Feature1E22")
    @features("Feature1E22WithSpiPeripheral")
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
        request_cls = self.feature_1e22.select_device_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SelectDevice request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1e22_index,
                device_idx=HexList(0x0),
                access_config=HexList(0x0))
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1e22.select_device_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SelectDeviceResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = SPIDirectAccessTestUtils.SelectDeviceResponseChecker
            checker.check_fields(self, response, self.feature_1e22.select_device_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1E22_0002#3", _AUTHOR)
    # end def test_select_device_padding

    @features("Feature1E22")
    @features("Feature1E22WithSpiPeripheral")
    @level("Robustness")
    def test_reserved_bits_of_access_config(self):
        """
        Validate the reserved bits of accessConfig are ignored by the FW
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over access_config in [0x05, 0x06, 0x07, 0x80, 0xFC, 0xFF]")
        # --------------------------------------------------------------------------------------------------------------
        for access_config in [0x05, 0x06, 0x07, 0x80, 0xFC, 0xFF]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send selectDevice request with accessConfig = {access_config}")
            # ----------------------------------------------------------------------------------------------------------
            response = SPIDirectAccessTestUtils.HIDppHelper.select_device(test_case=self,
                                                                          device_idx=0,
                                                                          access_config=access_config)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Wait selectDevice response and check the accessConfig equal to {access_config}")
            # ----------------------------------------------------------------------------------------------------------
            checker = SPIDirectAccessTestUtils.SelectDeviceResponseChecker
            check_map = checker.get_default_check_map(self)
            access_config_check_map = SPIDirectAccessTestUtils.AccessConfigChecker.get_check_map(
                access_config=access_config)
            check_map.update({
                "device_idx": (checker.check_device_idx, 0),
                "access_config": (checker.check_access_config, access_config_check_map)
            })
            checker.check_fields(self, response, self.feature_1e22.select_device_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1E22_0003", _AUTHOR)
    # end def test_reserved_bits_of_access_config
# end class SPIDirectAccessRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
