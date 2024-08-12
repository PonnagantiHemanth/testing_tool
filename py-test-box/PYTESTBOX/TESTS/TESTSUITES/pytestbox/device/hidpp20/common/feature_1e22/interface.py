#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.common.feature_1e22.interface
:brief: HID++ 2.0 ``SPIDirectAccess`` interface test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2022/11/21
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pylibrary.tools.hexlist import HexList
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.spidirectaccessutils import SPIDirectAccessTestUtils
from pytestbox.device.base.spidirectaccessutils import SPI_PERIPHERAL_REGISTER_DICT
from pytestbox.device.hidpp20.common.feature_1e22.spidirectaccess import SPIDirectAccessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SPIDirectAccessInterfaceTestCase(SPIDirectAccessTestCase):
    """
    Validate ``SPIDirectAccess`` interface test cases
    """

    @features("Feature1E22")
    @level("Interface")
    def test_get_nb_devices(self):
        """
        Validate ``GetNbDevices`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetNbDevices request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1e22.get_nb_devices_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1e22_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1e22.get_nb_devices_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetNbDevicesResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = SPIDirectAccessTestUtils.GetNbDevicesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, report.device_index),
            "feature_index": (checker.check_feature_index, report.feature_index),
        })
        checker.check_fields(self, response, self.feature_1e22.get_nb_devices_response_cls, check_map)

        self.testCaseChecked("INT_1E22_0001", _AUTHOR)
    # end def test_get_nb_devices

    @features("Feature1E22")
    @level("Interface")
    def test_get_selected_device(self):
        """
        Validate ``GetSelectedDevice`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetSelectedDevice request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1e22.get_selected_device_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1e22_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1e22.get_selected_device_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetSelectedDeviceResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = SPIDirectAccessTestUtils.GetSelectedDeviceResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, report.device_index),
            "feature_index": (checker.check_feature_index, report.feature_index),
        })
        checker.check_fields(self, response, self.feature_1e22.get_selected_device_response_cls, check_map)

        self.testCaseChecked("INT_1E22_0002", _AUTHOR)
    # end def test_get_selected_device

    @features("Feature1E22")
    @features("Feature1E22WithSpiPeripheral")
    @level("Interface")
    def test_select_device(self):
        """
        Validate ``SelectDevice`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SelectDevice request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1e22.select_device_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1e22_index,
            device_idx=HexList(0x0),
            access_config=HexList(0x0))
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1e22.select_device_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SelectDeviceResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = SPIDirectAccessTestUtils.SelectDeviceResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, report.device_index),
            "feature_index": (checker.check_feature_index, report.feature_index),
        })
        checker.check_fields(self, response, self.feature_1e22.select_device_response_cls, check_map)

        self.testCaseChecked("INT_1E22_0003", _AUTHOR)
    # end def test_select_device

    @features("Feature1E22")
    @features("Feature1E22WithSpiPeripheral")
    @level("Interface")
    def test_spi_direct_access(self):
        """
        Validate ``SpiDirectAccess`` interface
        """
        n_bytes = HexList(0x1)
        optical_sensor_name = self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SpiDirectAccess request")
        # --------------------------------------------------------------------------------------------------------------
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
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1e22.spi_direct_access_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SpiDirectAccessResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = SPIDirectAccessTestUtils.SpiDirectAccessResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, report.device_index),
            "feature_index": (checker.check_feature_index, report.feature_index),
            "n_bytes": (checker.check_n_bytes, n_bytes),
            "data_out_1": (checker.check_data_out_1,
                           SPI_PERIPHERAL_REGISTER_DICT[optical_sensor_name]['product_id']['value'])
        })
        checker.check_fields(self, response, self.feature_1e22.spi_direct_access_response_cls, check_map)

        self.testCaseChecked("INT_1E22_0004", _AUTHOR)
    # end def test_spi_direct_access
# end class SPIDirectAccessInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
