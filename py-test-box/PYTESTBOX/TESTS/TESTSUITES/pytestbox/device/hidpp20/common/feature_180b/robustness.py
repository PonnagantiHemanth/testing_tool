#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_180b.robustness
:brief: HID++ 2.0 ``ConfigurableDeviceRegisters`` robustness test suite
:author: Udayathilagan <uelamaran@logitech.com>
:date: 2024/04/29
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.common.configurabledeviceregisters import ConfigurableDeviceRegisters
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.configurabledeviceregistersutils import ConfigurableDeviceRegistersTestUtils
from pytestbox.device.hidpp20.common.feature_180b.configurabledeviceregisters \
    import ConfigurableDeviceRegistersTestCase
from pyhid.hidpp.features.common.configurabledeviceregisters import REGISTERS


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Udayathilagan"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class ConfigurableDeviceRegistersRobustnessTestCase(ConfigurableDeviceRegistersTestCase):
    """
    Validate ``ConfigurableDeviceRegisters`` robustness test cases
    """

    @features("Feature180B")
    @level("Robustness")
    def test_get_capabilities_software_id(self):
        """
        Validate ``GetCapabilities`` software id field is ignored by the firmware

        [0] getCapabilities() -> capabilities

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        capabilities = HexList(self.config.F_Capabilities)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ConfigurableDeviceRegisters.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ConfigurableDeviceRegistersTestUtils.HIDppHelper.get_capabilities(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ConfigurableDeviceRegistersTestUtils.GetCapabilitiesResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "capabilities": (checker.check_capabilities, capabilities)
            })
            checker.check_fields(self, response, self.feature_180b.get_capabilities_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_180B_0001#1", _AUTHOR)
    # end def test_get_capabilities_software_id

    @features("Feature180B")
    @level("Robustness")
    def test_get_register_info_software_id(self):
        """
        Validate ``GetRegisterInfo`` software id field is ignored by the firmware

        [1] getRegisterInfo(register_id) -> register_size

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RegisterId.0xPP

        SwID boundary values [0..F]
        """
        register_id = REGISTERS.READ_PROTECTION_LEVEL
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ConfigurableDeviceRegisters.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetRegisterInfo request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ConfigurableDeviceRegistersTestUtils.HIDppHelper.get_register_info(
                test_case=self,
                register_id=HexList(register_id),
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetRegisterInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ConfigurableDeviceRegistersTestUtils.GetRegisterInfoResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "configurable": (checker.check_configurable, self.register_data[register_id]["configurable"]),
                "supported": (checker.check_supported, self.register_data[register_id]["supported"]),
                "register_size": (checker.check_register_size, self.register_data[register_id]["register_size"])
            })
            checker.check_fields(self, response, self.feature_180b.get_register_info_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_180B_0001#2", _AUTHOR)
    # end def test_get_register_info_software_id

    @features("Feature180B")
    @level("Robustness")
    def test_get_register_value_software_id(self):
        """
        Validate ``GetRegisterValue`` software id field is ignored by the firmware

        [2] getRegisterValue(register_id) -> register_value

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RegisterId.0xPP

        SwID boundary values [0..F]
        """
        register_id = HexList(REGISTERS.READ_PROTECTION_LEVEL)
        register_value = HexList(0x0)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ConfigurableDeviceRegisters.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetRegisterValue request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ConfigurableDeviceRegistersTestUtils.HIDppHelper.get_register_value(
                test_case=self,
                register_id=register_id,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetRegisterValueResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ConfigurableDeviceRegistersTestUtils.GetRegisterValueResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "register_value": (checker.check_register_value, register_value)
            })
            checker.check_fields(self, response, self.feature_180b.get_register_value_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_180B_0001#3", _AUTHOR)
    # end def test_get_register_value_software_id

    @features("Feature180B")
    @level("Robustness")
    def test_get_capabilities_padding(self):
        """
        Validate ``GetCapabilities`` padding bytes are ignored by the firmware

        [0] getCapabilities() -> capabilities

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        capabilities = HexList(self.config.F_Capabilities)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_180b.get_capabilities_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = ConfigurableDeviceRegistersTestUtils.HIDppHelper.get_capabilities(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ConfigurableDeviceRegistersTestUtils.GetCapabilitiesResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "capabilities": (checker.check_capabilities, capabilities)
            })
            checker.check_fields(self, response, self.feature_180b.get_capabilities_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_180B_0002#1", _AUTHOR)
    # end def test_get_capabilities_padding

    @features("Feature180B")
    @level("Robustness")
    def test_get_register_info_padding(self):
        """
        Validate ``GetRegisterInfo`` padding bytes are ignored by the firmware

        [1] getRegisterInfo(register_id) -> register_size

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RegisterId.0xPP

        Padding (PP) boundary values [00..FF]
        """
        register_id = REGISTERS.READ_PROTECTION_LEVEL
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_180b.get_register_info_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetRegisterInfo request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = ConfigurableDeviceRegistersTestUtils.HIDppHelper.get_register_info(
                test_case=self,
                register_id=HexList(register_id),
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetRegisterInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ConfigurableDeviceRegistersTestUtils.GetRegisterInfoResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "configurable": (checker.check_configurable, self.register_data[register_id]["configurable"]),
                "supported": (checker.check_supported, self.register_data[register_id]["supported"]),
                "register_size": (checker.check_register_size, self.register_data[register_id]["register_size"])
            })
            checker.check_fields(self, response, self.feature_180b.get_register_info_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_180B_0002#2", _AUTHOR)
    # end def test_get_register_info_padding

    @features("Feature180B")
    @level("Robustness")
    def test_get_register_value_padding(self):
        """
        Validate ``GetRegisterValue`` padding bytes are ignored by the firmware

        [2] getRegisterValue(register_id) -> register_value

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RegisterId.0xPP

        Padding (PP) boundary values [00..FF]
        """
        register_id = HexList(REGISTERS.READ_PROTECTION_LEVEL)
        register_value = HexList(0x00)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_180b.get_register_value_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetRegisterValue request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = ConfigurableDeviceRegistersTestUtils.HIDppHelper.get_register_value(
                test_case=self,
                register_id=register_id,
                padding=padding)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetRegisterValueResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ConfigurableDeviceRegistersTestUtils.GetRegisterValueResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "register_value": (checker.check_register_value, register_value)
            })
            checker.check_fields(self, response, self.feature_180b.get_register_value_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_180B_0002#3", _AUTHOR)
    # end def test_get_register_value_padding
# end class ConfigurableDeviceRegistersRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
