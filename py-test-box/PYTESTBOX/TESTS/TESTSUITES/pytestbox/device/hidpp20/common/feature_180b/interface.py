#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_180b.interface
:brief: HID++ 2.0 ``ConfigurableDeviceRegisters`` interface test suite
:author: Udayathilagan <uelamaran@logitech.com>
:date: 2024/05/08
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.configurabledeviceregistersutils import ConfigurableDeviceRegistersTestUtils
from pyhid.hidpp.features.common.configurabledeviceregisters import GetRegisterValueResponse
from pyhid.hidpp.features.common.configurabledeviceregisters import REGISTERS
from pytestbox.device.hidpp20.common.feature_180b.configurabledeviceregisters \
    import ConfigurableDeviceRegistersTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Udayathilagan"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class ConfigurableDeviceRegistersInterfaceTestCase(ConfigurableDeviceRegistersTestCase):
    """
    Validate ``ConfigurableDeviceRegisters`` interface test cases
    """

    @features("Feature180B")
    @level("Interface")
    def test_get_capabilities(self):
        """
        Validate ``GetCapabilities`` normal processing

        [0] getCapabilities() -> capabilities
        """
        capabilities = self.config.F_Capabilities
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetCapabilities request")
        # --------------------------------------------------------------------------------------------------------------
        response = ConfigurableDeviceRegistersTestUtils.HIDppHelper.get_capabilities(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ConfigurableDeviceRegistersTestUtils.GetCapabilitiesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_180b_index)),
            "capabilities": (checker.check_capabilities, capabilities)
        })
        checker.check_fields(self, response, self.feature_180b.get_capabilities_response_cls, check_map)

        self.testCaseChecked("INT_180B_0001", _AUTHOR)
    # end def test_get_capabilities

    @features("Feature180B")
    @level("Interface")
    def test_get_register_info(self):
        """
        Validate ``GetRegisterInfo`` normal processing

        [1] getRegisterInfo(register_id) -> configurable, supported, register_size
        """
        register_id = REGISTERS.READ_PROTECTION_LEVEL
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetRegisterInfo request")
        # --------------------------------------------------------------------------------------------------------------
        response = ConfigurableDeviceRegistersTestUtils.HIDppHelper.get_register_info(
            test_case=self,
            register_id=HexList(register_id))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetRegisterInfoResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ConfigurableDeviceRegistersTestUtils.GetRegisterInfoResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_180b_index)),
            "configurable": (checker.check_configurable, self.register_data[register_id]["configurable"]),
            "supported": (checker.check_supported, self.register_data[register_id]["supported"]),
            "register_size": (checker.check_register_size, self.register_data[register_id]["register_size"])
        })
        checker.check_fields(self, response, self.feature_180b.get_register_info_response_cls, check_map)

        self.testCaseChecked("INT_180B_0002", _AUTHOR)
    # end def test_get_register_info

    @features("Feature180B")
    @level("Interface")
    def test_get_register_value(self):
        """
        Validate ``GetRegisterValue`` normal processing

        [2] getRegisterValue(register_id) -> register_value
        """
        register_id = HexList(REGISTERS.READ_PROTECTION_LEVEL)
        register_value = HexList(0x00)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetRegisterValue request")
        # --------------------------------------------------------------------------------------------------------------
        response = ConfigurableDeviceRegistersTestUtils.HIDppHelper.get_register_value(
            test_case=self,
            register_id=register_id,
            )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetRegisterValueResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ConfigurableDeviceRegistersTestUtils.GetRegisterValueResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_180b_index)),
            "register_value": (checker.check_register_value, register_value)
        })
        checker.check_fields(self, response, GetRegisterValueResponse, check_map)

        self.testCaseChecked("INT_180B_0003", _AUTHOR)
    # end def test_get_register_value

    @features("Feature180B")
    @level("Interface")
    def test_set_register_value(self):
        """
        Validate ``SetRegisterValue`` normal processing

        [3] setRegisterValue(register_id, register_value) -> None
        """
        self.post_requisite_erase_and_flash = True

        register_id = REGISTERS.READ_PROTECTION_LEVEL
        register_value = HexList(0x01)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetRegisterValue request")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurableDeviceRegistersTestUtils.HIDppHelper.set_register_value(
            test_case=self,
            register_id=register_id,
            register_value=register_value,
            register_size=1)
        self.testCaseChecked("INT_180B_0004", _AUTHOR)
    # end def test_set_register_value
# end class ConfigurableDeviceRegistersInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
