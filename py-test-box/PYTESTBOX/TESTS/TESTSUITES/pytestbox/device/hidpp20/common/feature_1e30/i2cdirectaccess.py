#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.common.feature_1e30.i2cdirectaccess
:brief: Validate HID++ 2.0 ``I2CDirectAccess`` feature
:author: YY Liu <yliu5@logitech.com>
:date: 2022/12/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.i2cdirectaccess import I2CDirectAccess
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.i2cdirectaccessutils import I2CDirectAccessTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class I2CDirectAccessTestCase(DeviceBaseTestCase):
    """
    Validate ``I2CDirectAccess`` TestCases in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Activate features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x1E30 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1e30_index, self.feature_1e30, _, _ = I2CDirectAccessTestUtils.HIDppHelper.get_parameters(self)

        self.config = self.f.PRODUCT.FEATURES.COMMON.I2C_DIRECT_ACCESS
        self.fw_access = I2CDirectAccess.AccessConfig.FwAccess
        self.access_config = I2CDirectAccess.AccessConfig(disabled_fw_access=self.fw_access.ENABLED)
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, 'Empty WirelessDeviceStatusBroadcastEvent queue')
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.clean_messages(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                                        class_type=WirelessDeviceStatusBroadcastEvent)
        # end with

        super().tearDown()
    # end def tearDown

    def _test_i2c_write_read(self, access_config):
        """
        Check the MCU FW can write/read the register value by sending i2cWriteDirectAccess/i2cReadDirectAccess
        request.

        :param access_config: Access Config
        :type access_config: ``int | HexList | I2CDirectAccess.AccessConfig``
        """
        n_bytes = 1
        default_access_config = I2CDirectAccess.AccessConfig(disabled_fw_access=self.fw_access.ENABLED)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over device_idx in range(getNbDevices.numberOfDevices)")
        # --------------------------------------------------------------------------------------------------------------
        for device_idx in range(self.config.F_NumberOfDevices):
            resister_name = I2CDirectAccessTestUtils.get_writeable_register_name(test_case=self)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Send selectDevice request with deviceIdx = {device_idx}, accessConfig = {access_config}")
            # ----------------------------------------------------------------------------------------------------------
            response = I2CDirectAccessTestUtils.HIDppHelper.select_device(
                test_case=self, device_idx=device_idx, access_config=access_config)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Wait selectDevice response and check the accessConfig equals {access_config}")
            # ----------------------------------------------------------------------------------------------------------
            checker = I2CDirectAccessTestUtils.SelectDeviceResponseChecker
            check_map = checker.get_default_check_map(self)
            access_config_check_map = I2CDirectAccessTestUtils.AccessConfigChecker.get_check_map(
                access_config=access_config)
            check_map.update({
                "device_idx": (checker.check_device_idx, device_idx),
                "access_config": (checker.check_access_config, access_config_check_map)
            })
            checker.check_fields(self, response, self.feature_1e30.select_device_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send i2cReadDirectAccess request")
            # ----------------------------------------------------------------------------------------------------------
            i2c_read_response = I2CDirectAccessTestUtils.i2c_read_register(
                test_case=self, device_index=device_idx, n_bytes=n_bytes, register_name=resister_name)
            data_to_be_written = 0xFF - to_int(i2c_read_response.data_out_1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send i2cWriteDirectAccess request to change the specific register value")
            # ----------------------------------------------------------------------------------------------------------
            i2c_write_response = I2CDirectAccessTestUtils.i2c_write_register(
                test_case=self, device_index=device_idx, register_name=resister_name, data=data_to_be_written)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait i2cWriteDirectAccess response and check its inputs fields are as expected")
            # ----------------------------------------------------------------------------------------------------------
            checker = I2CDirectAccessTestUtils.I2CWriteDirectAccessResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "n_bytes": (checker.check_n_bytes, n_bytes)
            })
            checker.check_fields(
                self, i2c_write_response, self.feature_1e30.i2c_write_direct_access_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send i2cReadDirectAccess request")
            # ----------------------------------------------------------------------------------------------------------
            response = I2CDirectAccessTestUtils.i2c_read_register(
                test_case=self, device_index=device_idx, n_bytes=n_bytes, register_name=resister_name)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait i2cReadDirectAccess response and check the register's value is as expected")
            # ----------------------------------------------------------------------------------------------------------
            checker = I2CDirectAccessTestUtils.I2CReadDirectAccessResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "n_bytes": (checker.check_n_bytes, n_bytes),
                "data_out_1": (checker.check_data_out_1, data_to_be_written)
            })
            checker.check_fields(self, response, self.feature_1e30.i2c_read_direct_access_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send i2cWriteDirectAccess request to change the specific register value")
            # ----------------------------------------------------------------------------------------------------------
            I2CDirectAccessTestUtils.i2c_write_register(test_case=self,
                                                        device_index=device_idx,
                                                        register_name=resister_name,
                                                        data=to_int(i2c_read_response.data_out_1))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self,
                f"Send selectDevice request with deviceIdx = {device_idx}, accessConfig = {default_access_config}")
            # ----------------------------------------------------------------------------------------------------------
            I2CDirectAccessTestUtils.HIDppHelper.select_device(
                test_case=self, device_idx=device_idx, access_config=default_access_config)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
    # end def _test_i2c_write_read
# end class I2CDirectAccessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
