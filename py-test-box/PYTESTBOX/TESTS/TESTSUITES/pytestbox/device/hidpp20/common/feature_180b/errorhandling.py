#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_180b.errorhandling
:brief: HID++ 2.0 ``ConfigurableDeviceRegisters`` error handling test suite
:author: Udayathilagan <uelamaran@logitech.com>
:date: 2024/04/29
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.common.configurabledeviceregisters import REGISTERS
from pyhid.hidpp.features.common.configurabledeviceregisters import SetRegisterValue
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.configurabledeviceregistersutils import ConfigurableDeviceRegistersTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.hidpp20.common.feature_180b.configurabledeviceregisters \
    import ConfigurableDeviceRegistersTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Udayathilagan"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class ConfigurableDeviceRegistersErrorHandlingTestCase(ConfigurableDeviceRegistersTestCase):
    """
    Validate ``ConfigurableDeviceRegisters`` error handling test cases
    """

    @features("Feature180B")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_180b.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with a wrong function index: {function_index}")
            # ----------------------------------------------------------------------------------------------------------
            ConfigurableDeviceRegistersTestUtils.HIDppHelper.get_capabilities_and_check_error(
                test_case=self,
                error_codes=[Hidpp2ErrorCodes.INVALID_FUNCTION_ID],
                function_index=function_index)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_180B_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature180B")
    @level("ErrorHandling")
    def test_get_register_info_invalid_register(self):
        """
        Validate INVALID ARGUMENT is received when getRegisterInfo is called with registerId = 0
        """
        register_id = HexList(0x00)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getRegisterInfo with the registerId value as 0")
        # --------------------------------------------------------------------------------------------------------------
        get_register_info = self.feature_180b.get_register_info_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_180b_index,
            register_id=register_id
        )
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check INVALID_ARGUMENT is received")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurableDeviceRegistersTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=get_register_info,
            error_codes=[ErrorCodes.INVALID_ARGUMENT]
        )
        self.testCaseChecked("ERR_180B_0002", _AUTHOR)
    # end def test_get_register_info_invalid_register

    @features("Feature180B")
    @level("ErrorHandling")
    def test_get_register_value_invalid_register(self):
        """
        Validate INVALID ARGUMENT is received when getRegisterValue is called with registerId = 0
        """
        register_id = HexList(0x00)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getRegisterValue with the registerId value as 0")
        # --------------------------------------------------------------------------------------------------------------
        get_register_value = self.feature_180b.get_register_value_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_180b_index,
            register_id=register_id
        )
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check INVALID_ARGUMENT is received")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurableDeviceRegistersTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=get_register_value,
            error_codes=[ErrorCodes.INVALID_ARGUMENT]
        )
        self.testCaseChecked("ERR_180B_0003", _AUTHOR)
    # end def test_get_register_value_invalid_register

    @features("Feature180B")
    @level("ErrorHandling")
    def test_get_register_value_unsupported_register(self):
        """
        Validate INVALID ARGUMENT is received when getRegisterValue is called with unsupported registerId
        """
        all_registers_id = list(range(1, len(REGISTERS) + 1))
        list_of_supported_registers_id = [int(i) for i in self.config.F_SupportedRegisters]
        list_of_unsupported_registers_id = [id for id in all_registers_id if id not in list_of_supported_registers_id]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getRegisterValue with the unsupported registerId")
        # --------------------------------------------------------------------------------------------------------------
        get_register_value = self.feature_180b.get_register_value_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_180b_index,
            register_id=HexList(list_of_unsupported_registers_id[0])
        )
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check INVALID_ARGUMENT is received")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurableDeviceRegistersTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=get_register_value,
            error_codes=[ErrorCodes.INVALID_ARGUMENT]
        )
        self.testCaseChecked("ERR_180B_0004", _AUTHOR)
    # end def test_get_register_value_unsupported_register

    @features("Feature180B")
    @level("ErrorHandling")
    def test_set_register_value_invalid_register(self):
        """
        Validate INVALID ARGUMENT is received when setRegisterValue is called with registerId = 0
        """
        register_id = HexList(0x00)
        register_value = HexList(0x00)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setRegisterValue with the registerId value as 0")
        # --------------------------------------------------------------------------------------------------------------
        set_register_value = self.feature_180b.set_register_value_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_180b_index,
            register_id=register_id,
            register_value=register_value
        )
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check INVALID_ARGUMENT is received")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurableDeviceRegistersTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=set_register_value,
            error_codes=[ErrorCodes.INVALID_ARGUMENT]
        )
        self.testCaseChecked("ERR_180B_0006", _AUTHOR)
    # end def test_set_register_value_invalid_register

    @features("Feature180B")
    @level("ErrorHandling")
    def test_set_register_value_unsupported_register(self):
        """
        Validate INVALID ARGUMENT is received when setRegisterValue is called with unsupported registerId
        """
        all_registers_id = list(range(1, len(REGISTERS) + 1))
        list_of_supported_registers_id = [int(i) for i in self.config.F_SupportedRegisters]
        list_of_unsupported_registers_id = [id for id in all_registers_id if id not in list_of_supported_registers_id]
        register_value = HexList(0x00)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setRegisterValue with the unsupported registerId with valid value")
        # --------------------------------------------------------------------------------------------------------------
        set_register_value = self.feature_180b.set_register_value_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_180b_index,
            register_id=HexList(list_of_unsupported_registers_id[0]),
            register_value=register_value
        )
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check INVALID_ARGUMENT is received")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurableDeviceRegistersTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=set_register_value,
            error_codes=[ErrorCodes.INVALID_ARGUMENT]
        )
        self.testCaseChecked("ERR_180B_0007", _AUTHOR)
    # end def test_set_register_value_unsupported_register

    @features("Feature180B")
    @level("ErrorHandling")
    def test_set_register_value_non_configurable_register(self):
        """
        Validate NOT_ALLOWED is received when setRegisterValue is called with supported and not configurable
        registerId
        """
        register_id = HexList(0x02)
        register_value = HexList(0x00)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setRegisterValue with the supported and not configurable registerId with valid"
                                 "value")
        # --------------------------------------------------------------------------------------------------------------
        set_register_value = self.feature_180b.set_register_value_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_180b_index,
            register_id=register_id,
            register_value=register_value
        )
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check NOT_ALLOWED is received")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurableDeviceRegistersTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=set_register_value,
            error_codes=[ErrorCodes.NOT_ALLOWED]
        )
        self.testCaseChecked("ERR_180B_0008", _AUTHOR)
    # end def test_set_register_value_non_configurable_register

    @features("Feature180B")
    @level("ErrorHandling")
    def test_set_register_value_hw(self):
        """
        Validate HW_ERROR error code is received when getRegisterValue API is called with supported and configurable
        registerId
        """
        self.post_requisite_erase_and_flash = True
        register_id = 0x01
        register_value = HexList(0x01)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setRegisterValue with the supported and configurable registerId with "
                                 "the a value")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurableDeviceRegistersTestUtils.HIDppHelper.set_register_value(
            test_case=self,
            register_id=register_id,
            register_value=register_value,
            register_size=1)

        # ------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reconnect the channel")
        # ------------------------------------------------------------------------------------------------------
        if not self.current_channel.is_open:
            ChannelUtils.open_channel(test_case=self, channel=self.current_channel)
        # end if
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Activate features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setRegisterValue with the supported and configurable registerId with the same"
                                 "value")
        # --------------------------------------------------------------------------------------------------------------
        set_register_value = self.feature_180b.set_register_value_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_180b_index,
            register_id=register_id,
            register_value=register_value,
            register_size=1
        )
        reporter = SetRegisterValue.register_value_based_on_size(set_register_value, register_id=register_id,
                                                                 register_value=register_value, register_size=1)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check HW_ERROR  is received")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurableDeviceRegistersTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=reporter,
            error_codes=[ErrorCodes.HW_ERROR]
        )
        self.testCaseChecked("ERR_180B_0009", _AUTHOR)
    # end def test_set_register_value_hw
# end class ConfigurableDeviceRegistersErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
