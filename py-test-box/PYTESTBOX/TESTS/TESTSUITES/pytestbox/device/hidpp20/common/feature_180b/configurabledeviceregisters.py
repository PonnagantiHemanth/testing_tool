#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_180b.configurabledeviceregisters
:brief: Validate HID++ 2.0 ``ConfigurableDeviceRegisters`` feature
:author: Udayathilagan <uelamaran@logitech.com>
:date: 2024/05/08
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from os.path import join
# noinspection PyUnresolvedReferences
from pysetup import TESTS_PATH

from pyhid.hidpp.features.common.configurabledeviceregisters import REGISTERS
from pyhid.hidpp.features.common.configurabledeviceregisters import DEFAULT_REGISTER_SIZE_MAP
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.configurabledeviceregistersutils import ConfigurableDeviceRegistersTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class ConfigurableDeviceRegistersTestCase(DeviceBaseTestCase):
    """
    Validate ``ConfigurableDeviceRegisters`` TestCases in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        self.post_requisite_erase_and_flash = False

        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Activate features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x180B index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_180b_index, self.feature_180b, _, _ = (ConfigurableDeviceRegistersTestUtils.HIDppHelper.
                                                            get_parameters(test_case=self))

        self.config = self.f.PRODUCT.FEATURES.COMMON.CONFIGURABLE_DEVICE_REGISTERS
        self.list_of_supported_registers_id = [int(i) for i in self.config.F_SupportedRegisters]
        self.list_of_configurable_registers = [int(i) for i in self.config.F_ConfigurableRegisters]
        self.list_of_variable_register_size = [int(i) for i in self.config.F_VariableRegisterSize]

        self.register_data = {}
        for register in REGISTERS:
            is_supported = register.value in self.list_of_supported_registers_id
            is_configurable = register.value in self.list_of_configurable_registers
            variable_size = self.list_of_variable_register_size[register.value - 1] if register.value - 1 < len(
                self.list_of_variable_register_size) else 0
            register_size = variable_size if variable_size != 0 else DEFAULT_REGISTER_SIZE_MAP.get(register, 0)

            self.register_data[register] = {
                "supported": is_supported,
                "configurable": is_configurable,
                "register_size": register_size
            }
        # end for
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites
        """
        # noinspection PyBroadException
        with self.manage_post_requisite():
            if self.post_requisite_erase_and_flash:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Re-flashing the default hex file")
                # ------------------------------------------------------------------------------------------------------
                self.debugger.erase_and_flash_firmware(
                    firmware_hex_file=join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_HexFileName))
                self.reset()
            # end if
        # end with
        super().tearDown()
    # end def tearDown
# end class ConfigurableDeviceRegistersTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
