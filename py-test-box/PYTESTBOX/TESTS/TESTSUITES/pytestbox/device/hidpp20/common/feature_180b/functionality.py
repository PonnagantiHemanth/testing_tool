#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_180b.functionality
:brief: HID++ 2.0 ``ConfigurableDeviceRegisters`` functionality test suite
:author: Udayathilagan <uelamaran@logitech.com>
:date: 2024/04/29
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.configurabledeviceregistersutils import ConfigurableDeviceRegistersTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.hidpp20.common.feature_180b.configurabledeviceregisters \
    import ConfigurableDeviceRegistersTestCase
from pyhid.hidpp.features.common.configurabledeviceregisters import GetRegisterValueResponse
from pyhid.hidpp.features.common.configurabledeviceregisters import DEFAULT_REGISTER_SIZE_MAP

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
class ConfigurableDeviceRegistersFunctionalityTestCase(ConfigurableDeviceRegistersTestCase):
    """
    Validate ``ConfigurableDeviceRegisters`` functionality test cases
    """

    @features("Feature180B")
    @level("Functionality")
    def test_get_register_info_for_all(self):
        """
        Check getRegisterInfo for all available register IDs
        """

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over in valid range of register id")
        # --------------------------------------------------------------------------------------------------------------
        for register_id in self.register_data.keys():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send getRegisterInfo with current register id")
            # ----------------------------------------------------------------------------------------------------------
            response = ConfigurableDeviceRegistersTestUtils.HIDppHelper.get_register_info(
                test_case=self,
                register_id=HexList(register_id))
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check getRegisterInfo response fields.")
            # ----------------------------------------------------------------------------------------------------------
            checker = ConfigurableDeviceRegistersTestUtils.GetRegisterInfoResponseChecker()
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "configurable": (checker.check_configurable, self.register_data[register_id]["configurable"]),
                "supported": (checker.check_supported, self.register_data[register_id]["supported"]),
                "register_size": (checker.check_register_size, self.register_data[register_id]["register_size"])
            })
            if not response.supported:
                check_map.update({
                    "configurable": (checker.check_configurable, False),
                    "supported": (checker.check_supported, False),
                    "register_size": (checker.check_register_size, 0)
                })
            # end if
            checker.check_fields(self, response, self.feature_180b.get_register_info_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End test loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_180B_0001", _AUTHOR)
    # end def test_get_register_info_for_all

    @features("Feature180B")
    @level("Functionality")
    def test_get_register_value_for_all(self):
        """
        Check getRegisterValue can be called for all supported register IDs

        :raise ``ValueError``: If the Register Id is not supported.
        """

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over in valid range of register id")
        # --------------------------------------------------------------------------------------------------------------
        for register_id in self.list_of_supported_registers_id:
            register_id = HexList(register_id)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send getRegisterInfo with current register id")
            # ----------------------------------------------------------------------------------------------------------
            response = ConfigurableDeviceRegistersTestUtils.HIDppHelper.get_register_info(
                test_case=self,
                register_id=register_id)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "If the register is supported")
            # ----------------------------------------------------------------------------------------------------------
            if response.supported:
                register_size = response.register_size
                # ----------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send getRegisterValue with current register id")
                # ----------------------------------------------------------------------------------------------------------
                response = ConfigurableDeviceRegistersTestUtils.HIDppHelper.get_register_value(
                    test_case=self,
                    register_id=register_id,
                    register_size=int(Numeral(register_size))
                )
                # ----------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check the response fields")
                # ----------------------------------------------------------------------------------------------------------
                checker = ConfigurableDeviceRegistersTestUtils.GetRegisterValueResponseChecker
                check_map = checker.get_default_check_map(self)
                check_map.update({
                    "device_index": (checker.check_device_index, HexList(self.original_device_index)),
                    "feature_index": (checker.check_feature_index, HexList(self.feature_180b_index)),
                    "register_value": (checker.check_register_value, response.register_value)
                })
                checker.check_fields(self, response, GetRegisterValueResponse, check_map)

            else:
                raise ValueError(f"Register Id {register_id} is not supported")
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_180B_0002", _AUTHOR)
    # end def test_get_register_value_for_all

    @features("Feature180B")
    @level("Functionality")
    def test_set_register_value_for_all(self):
        """
        Check setRegisterValue can be called for all configurable register IDs
        """
        self.post_requisite_erase_and_flash = True

        supported_register_values = [HexList(0x01)]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over in valid range of configurable register")
        # --------------------------------------------------------------------------------------------------------------
        for register_id in self.list_of_configurable_registers:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send a getRegisterInfo command with the current registerId.")
            # ----------------------------------------------------------------------------------------------------------
            response = ConfigurableDeviceRegistersTestUtils.HIDppHelper.get_register_info(
                test_case=self,
                register_id=HexList(register_id))
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "If the register is supported and configurable")
            # ----------------------------------------------------------------------------------------------------------
            if response.supported:
                # ----------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "Test loop over in valid supported value")
                # ----------------------------------------------------------------------------------------------------------
                for supported_register_value in supported_register_values:
                    # ------------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, "Send setRegisterValue command for the same registerId with "
                                             "registerValue.")
                    # ------------------------------------------------------------------------------------------------------
                    ConfigurableDeviceRegistersTestUtils.HIDppHelper.set_register_value(
                        test_case=self,
                        register_id=register_id,
                        register_value=supported_register_value,
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
                    # ------------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, "Send getRegisterValue for the same RegisterId")
                    # ------------------------------------------------------------------------------------------------------
                    response = ConfigurableDeviceRegistersTestUtils.HIDppHelper.get_register_value(
                        test_case=self,
                        register_id=HexList(register_id),
                        register_size=DEFAULT_REGISTER_SIZE_MAP[int(Numeral(register_id))]
                    )
                    # ------------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, "Check that the response field's register value is the same as what we")
                    # ------------------------------------------------------------------------------------------------------
                    checker = ConfigurableDeviceRegistersTestUtils.GetRegisterValueResponseChecker
                    check_map = checker.get_default_check_map(self)
                    check_map.update({
                        "device_index": (checker.check_device_index, HexList(self.original_device_index)),
                        "feature_index": (checker.check_feature_index, HexList(self.feature_180b_index)),
                        "register_value": (checker.check_register_value, supported_register_value)
                    })
                    checker.check_fields(self, response, GetRegisterValueResponse, check_map)
                # end for
                # ----------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "End Test Loop")
                # ----------------------------------------------------------------------------------------------------------
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_180B_0003", _AUTHOR)
    # end def test_set_register_value_for_all
# end class ConfigurableDeviceRegistersFunctionalityTestCase
