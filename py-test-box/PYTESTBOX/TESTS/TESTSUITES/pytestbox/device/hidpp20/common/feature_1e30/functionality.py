#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.common.feature_1e30.functionality
:brief: HID++ 2.0 ``I2CDirectAccess`` functionality test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2022/12/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pylibrary.emulator.keyid import KEY_ID
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.i2cdirectaccessutils import I2CDirectAccessTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.hidpp20.common.feature_1e30.i2cdirectaccess import I2CDirectAccessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class I2CDirectAccessFunctionalityTestCase(I2CDirectAccessTestCase):
    """
    Validate ``I2CDirectAccess`` functionality test cases
    """

    @features("Feature1E30")
    @features("Feature1E30WithI2cPeripheral")
    @level("Functionality")
    @services("TouchModule")
    def test_enabled_disable_fw_access(self):
        """
        Verify the MCU FW cannot/can communicate with the selected I2C peripheral when the disableFwAccess is
        enabled/disabled
        """
        self.access_config.disabled_fw_access = self.fw_access.DISABLED
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send selectDevice request with accessConfig = {self.access_config}")
        # --------------------------------------------------------------------------------------------------------------
        response = I2CDirectAccessTestUtils.HIDppHelper.select_device(
            test_case=self, device_idx=0, access_config=self.access_config)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Wait selectDevice response and check the accessConfig equals {self.access_config}")
        # --------------------------------------------------------------------------------------------------------------
        checker = I2CDirectAccessTestUtils.SelectDeviceResponseChecker
        check_map = checker.get_default_check_map(self)
        access_config_check_map = I2CDirectAccessTestUtils.AccessConfigChecker.get_check_map(
            access_config=self.access_config)
        check_map.update({
            "access_config": (checker.check_access_config, access_config_check_map)
        })
        checker.check_fields(self, response, self.feature_1e30.select_device_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Emulate finger movement on touchpad (Or perform other user actions from the"
                                 "corresponding I2C peripheral)")
        # --------------------------------------------------------------------------------------------------------------
        # TODO - Implement the emulation method

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check no corresponding HID report is received from the DUT")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID, timeout=2)

        self.access_config.disabled_fw_access = self.fw_access.ENABLED
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send selectDevice request with accessConfig = {self.access_config}")
        # --------------------------------------------------------------------------------------------------------------
        response = I2CDirectAccessTestUtils.HIDppHelper.select_device(
            test_case=self, device_idx=0, access_config=self.access_config)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Wait selectDevice response and check the accessConfig equals {self.access_config}")
        # --------------------------------------------------------------------------------------------------------------
        checker = I2CDirectAccessTestUtils.SelectDeviceResponseChecker
        check_map = checker.get_default_check_map(self)
        access_config_check_map = I2CDirectAccessTestUtils.AccessConfigChecker.get_check_map(
            access_config=self.access_config)
        check_map.update({
            "access_config": (checker.check_access_config, access_config_check_map)
        })
        checker.check_fields(self, response, self.feature_1e30.select_device_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Emulate finger movement on touchpad (Or perform other user actions from the"
                                 "corresponding I2C peripheral)")
        # --------------------------------------------------------------------------------------------------------------
        # TODO - Implement the emulation method

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the corresponding HID report is received from the DUT")
        # --------------------------------------------------------------------------------------------------------------
        hid_report = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        self.assertNotNone(obtained=hid_report, msg='No HID report received')

        self.testCaseChecked("FUN_1E30_0001", _AUTHOR)
    # end def test_enabled_disable_fw_access

    @features("Feature1E30")
    @features("Feature1E30WithI2cPeripheral")
    @level("Functionality")
    def test_get_access_config_from_selected_device(self):
        """
        Verify the getSelectedDevice request can return the latest change of accessConfig that changed by
        selectedDevice request
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over access_config in range [0..1]")
        # --------------------------------------------------------------------------------------------------------------
        for access_config in [self.fw_access.ENABLED, self.fw_access.DISABLED]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Test Loop over device_idx in range [0..{self.config.F_NumberOfDevices}]")
            # ----------------------------------------------------------------------------------------------------------
            for device_idx in range(0, self.config.F_NumberOfDevices):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send selectDevice request with accessConfig = {access_config}")
                # ------------------------------------------------------------------------------------------------------
                response = I2CDirectAccessTestUtils.HIDppHelper.select_device(
                    test_case=self, device_idx=device_idx, access_config=access_config)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Wait selectDevice response and check the accessConfig equals {access_config}")
                # ------------------------------------------------------------------------------------------------------
                checker = I2CDirectAccessTestUtils.SelectDeviceResponseChecker
                check_map = checker.get_default_check_map(self)
                access_config_check_map = I2CDirectAccessTestUtils.AccessConfigChecker.get_check_map(
                    access_config=access_config)
                check_map.update({
                    "device_idx": (checker.check_device_idx, device_idx),
                    "access_config": (checker.check_access_config, access_config_check_map)
                })
                checker.check_fields(self, response, self.feature_1e30.select_device_response_cls, check_map)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send getSelectedDevice request")
                # ------------------------------------------------------------------------------------------------------
                response = I2CDirectAccessTestUtils.HIDppHelper.get_selected_device(test_case=self)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Wait getSelectedDevice response and check the accessConfig = {access_config}")
                # ------------------------------------------------------------------------------------------------------
                checker = I2CDirectAccessTestUtils.GetSelectedDeviceResponseChecker
                check_map = checker.get_default_check_map(self)
                access_config_check_map = I2CDirectAccessTestUtils.AccessConfigChecker.get_check_map(
                    access_config=access_config)
                check_map.update({
                    "device_idx": (checker.check_device_idx, device_idx),
                    "access_config": (checker.check_access_config, access_config_check_map)
                })
                checker.check_fields(self, response, self.feature_1e30.get_selected_device_response_cls, check_map)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1E30_0002", _AUTHOR)
    # end def test_get_access_config_from_selected_device

    @features("Feature1E30")
    @features("Feature1E30WithI2cPeripheral")
    @level("Functionality")
    def test_i2c_write_read_with_enable_fw_access(self):
        """
        Check the MCU FW can write/read the register value by sending i2cWriteDirectAccess/i2cReadDirectAccess
        request, while the regular communication with the I2C peripheral is enabled.
        """
        self.access_config.disabled_fw_access = self.fw_access.ENABLED
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test I2C write/read with enabled fw access")
        # --------------------------------------------------------------------------------------------------------------
        self._test_i2c_write_read(access_config=self.access_config)

        self.testCaseChecked("FUN_1E30_0003", _AUTHOR)
    # end def test_i2c_write_read_with_enable_fw_access

    @features("Feature1E30")
    @features("Feature1E30WithI2cPeripheral")
    @level("Functionality")
    def test_i2c_write_read_with_disable_fw_access(self):
        """
        Check the MCU FW can write/read the register value by sending i2cWriteDirectAccess/i2cReadDirectAccess
        request, while the regular communication with the I2C peripheral is disabled.
        """
        self.access_config.disabled_fw_access = self.fw_access.DISABLED
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test I2C write/read with disabled fw access")
        # --------------------------------------------------------------------------------------------------------------
        self._test_i2c_write_read(access_config=self.access_config)

        self.testCaseChecked("FUN_1E30_0004", _AUTHOR)
    # end def test_i2c_write_read_with_disable_fw_access

    @features("Feature1E30")
    @features("Feature1E30WithI2cPeripheral")
    @features("Feature1830")
    @level("Functionality")
    @services("RequiredKeys", (KEY_ID.BUTTON_1,))
    def test_access_config_reset_after_deep_sleep(self):
        """
        Verify the accessConfig settings are reset to the default value, after the device is woke-up from the
        deep-sleep mode
        """
        self.access_config.disabled_fw_access = self.fw_access.DISABLED
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send selectDevice request with accessConfig = 1")
        # --------------------------------------------------------------------------------------------------------------
        response = I2CDirectAccessTestUtils.HIDppHelper.select_device(
            test_case=self, device_idx=0, access_config=self.access_config)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait selectDevice request and check the accessConfig equals 1")
        # --------------------------------------------------------------------------------------------------------------
        checker = I2CDirectAccessTestUtils.SelectDeviceResponseChecker
        check_map = checker.get_default_check_map(self)
        access_config_check_map = I2CDirectAccessTestUtils.AccessConfigChecker.get_check_map(
            access_config=self.access_config)
        check_map.update({
            "access_config": (checker.check_access_config, access_config_check_map)
        })
        checker.check_fields(self, response, self.feature_1e30.select_device_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send 0x1830.setPowerMode request with powerMode = 3 (deep-sleep mode)")
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform an user action to wake up the device")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable hidden features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getSelectedDevice request with accessConfig")
        # --------------------------------------------------------------------------------------------------------------
        response = I2CDirectAccessTestUtils.HIDppHelper.get_selected_device(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getSelectedDevice response and check the accessConfig is reset")
        # --------------------------------------------------------------------------------------------------------------
        checker = I2CDirectAccessTestUtils.GetSelectedDeviceResponseChecker
        checker.check_fields(self, response, self.feature_1e30.get_selected_device_response_cls)

        self.testCaseChecked("FUN_1E30_0005", _AUTHOR)
    # end def test_access_config_reset_after_deep_sleep

    @features("Feature1E30")
    @features("Feature1E30WithI2cPeripheral")
    @level("Functionality")
    def test_access_config_reset_after_power_cycle(self):
        """
        Verify the accessConfig settings are reset to the default value, after a device power cycle
        """
        self.access_config.disable_fw_access = self.fw_access.DISABLED
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send selectDevice request with accessConfig = {self.access_config}")
        # --------------------------------------------------------------------------------------------------------------
        response = I2CDirectAccessTestUtils.HIDppHelper.select_device(
            test_case=self, device_idx=0, access_config=self.access_config)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Wait selectDevice request and check the accessConfig equals {self.access_config}")
        # --------------------------------------------------------------------------------------------------------------
        checker = I2CDirectAccessTestUtils.SelectDeviceResponseChecker
        check_map = checker.get_default_check_map(self)
        access_config_check_map = I2CDirectAccessTestUtils.AccessConfigChecker.get_check_map(
            access_config=self.access_config)
        check_map.update({
            "access_config": (checker.check_access_config, access_config_check_map)
        })
        checker.check_fields(self, response, self.feature_1e30.select_device_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power OFF -> ON the device")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable hidden features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getSelectedDevice request with accessConfig")
        # --------------------------------------------------------------------------------------------------------------
        response = I2CDirectAccessTestUtils.HIDppHelper.get_selected_device(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getSelectedDevice response and check the accessConfig is reset")
        # --------------------------------------------------------------------------------------------------------------
        checker = I2CDirectAccessTestUtils.GetSelectedDeviceResponseChecker
        checker.check_fields(self, response, self.feature_1e30.get_selected_device_response_cls)

        self.testCaseChecked("FUN_1E30_0006", _AUTHOR)
    # end def test_access_config_reset_after_power_cycle
# end class I2CDirectAccessFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
