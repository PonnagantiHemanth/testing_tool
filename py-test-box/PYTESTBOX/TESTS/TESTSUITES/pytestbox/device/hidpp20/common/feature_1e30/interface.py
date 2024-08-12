#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.common.feature_1e30.interface
:brief: HID++ 2.0 ``I2CDirectAccess`` interface test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2022/12/06
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
from pytestbox.device.base.i2cdirectaccessutils import I2CDirectAccessTestUtils
from pytestbox.device.hidpp20.common.feature_1e30.i2cdirectaccess import I2CDirectAccessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class I2CDirectAccessInterfaceTestCase(I2CDirectAccessTestCase):
    """
    Validate ``I2CDirectAccess`` interface test cases
    """

    @features("Feature1E30")
    @level("Interface")
    def test_get_nb_devices(self):
        """
        Validate ``GetNbDevices`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetNbDevices request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1e30.get_nb_devices_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1e30_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1e30.get_nb_devices_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetNbDevicesResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = I2CDirectAccessTestUtils.GetNbDevicesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, report.device_index),
            "feature_index": (checker.check_feature_index, report.feature_index),
        })
        checker.check_fields(self, response, self.feature_1e30.get_nb_devices_response_cls, check_map)

        self.testCaseChecked("INT_1E30_0001", _AUTHOR)
    # end def test_get_nb_devices

    @features("Feature1E30")
    @level("Interface")
    def test_get_selected_device(self):
        """
        Validate ``GetSelectedDevice`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetSelectedDevice request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1e30.get_selected_device_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1e30_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1e30.get_selected_device_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetSelectedDeviceResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = I2CDirectAccessTestUtils.GetSelectedDeviceResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, report.device_index),
            "feature_index": (checker.check_feature_index, report.feature_index),
        })
        checker.check_fields(self, response, self.feature_1e30.get_selected_device_response_cls, check_map)

        self.testCaseChecked("INT_1E30_0002", _AUTHOR)
    # end def test_get_selected_device

    @features("Feature1E30")
    @features("Feature1E30WithI2cPeripheral")
    @level("Interface")
    def test_select_device(self):
        """
        Validate ``SelectDevice`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SelectDevice request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1e30.select_device_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1e30_index,
            device_idx=HexList(0x0),
            access_config=HexList(0x0))
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1e30.select_device_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SelectDeviceResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = I2CDirectAccessTestUtils.SelectDeviceResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, report.device_index),
            "feature_index": (checker.check_feature_index, report.feature_index),
        })
        checker.check_fields(self, response, self.feature_1e30.select_device_response_cls, check_map)

        self.testCaseChecked("INT_1E30_0003", _AUTHOR)
    # end def test_select_device

    @features("Feature1E30")
    @features("Feature1E30WithI2cPeripheral")
    @level("Interface")
    def test_i2c_read_direct_access(self):
        """
        Validate ``I2CReadDirectAccess`` interface
        """
        n_bytes = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send I2CReadDirectAccess request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1e30.i2c_read_direct_access_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1e30_index,
            n_bytes=n_bytes,
            register_address=0x00)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1e30.i2c_read_direct_access_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check I2CReadDirectAccessResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = I2CDirectAccessTestUtils.I2CReadDirectAccessResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, report.device_index),
            "feature_index": (checker.check_feature_index, report.feature_index),
            "n_bytes": (checker.check_n_bytes, n_bytes),
        })
        checker.check_fields(self, response, self.feature_1e30.i2c_read_direct_access_response_cls, check_map)

        self.testCaseChecked("INT_1E30_0004", _AUTHOR)
    # end def test_i2c_read_direct_access

    @features("Feature1E30")
    @features("Feature1E30WithI2cPeripheral")
    @level("Interface")
    def test_i2c_write_direct_access(self):
        """
        Validate ``I2CWriteDirectAccess`` interface
        """
        n_bytes = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send I2CWriteDirectAccess request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1e30.i2c_write_direct_access_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1e30_index,
            n_bytes=n_bytes,
            register_address=HexList(0x0),
            data_in_1=HexList(0x0),
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
            data_in_14=HexList(0x0))
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1e30.i2c_write_direct_access_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check I2CWriteDirectAccessResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = I2CDirectAccessTestUtils.I2CWriteDirectAccessResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, report.device_index),
            "feature_index": (checker.check_feature_index, report.feature_index),
            "n_bytes": (checker.check_n_bytes, n_bytes),
        })
        checker.check_fields(self, response, self.feature_1e30.i2c_write_direct_access_response_cls, check_map)

        self.testCaseChecked("INT_1E30_0005", _AUTHOR)
    # end def test_i2c_write_direct_access
# end class I2CDirectAccessInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
