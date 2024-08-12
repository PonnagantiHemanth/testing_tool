#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1803.functionality
:brief: HID++ 2.0 ``GpioAccess`` functionality test suite
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/06/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.gpioaccessutils import GpioAccessTestUtils
from pytestbox.device.hidpp20.common.feature_1803.gpioaccess import GpioAccessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vinodh Selvaraj"
_LOOP_OVER_ALL_PORTS = "Test loop over all ports"
_END_LOOP = "End Test Loop"
_VALIDATE_API_SUCCESS = "Validate api call success"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class GpioAccessFunctionalityTestCase(GpioAccessTestCase):
    """
    Validate ``GpioAccess`` functionality test cases
    """

    @features("Feature1803")
    @level("Functionality")
    @services("Debugger")
    def test_set_group_in(self):
        """
        Validate ``SetGroupIn`` request API.
        
        [0] SetGroupIn(portNumber, gpioMask) -> void
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_OVER_ALL_PORTS)
        # --------------------------------------------------------------------------------------------------------------
        for port_number in range(self.config.F_NumberOfPorts):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetGroupIn for Port {port_number} with project specific GpioMask and Value")
            # ----------------------------------------------------------------------------------------------------------
            set_group_in_response = GpioAccessTestUtils.HIDppHelper.set_group_in(
                test_case=self, port_number=port_number, gpio_mask=self.config.F_GpioInputMask[port_number])
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _VALIDATE_API_SUCCESS)
            # ----------------------------------------------------------------------------------------------------------
            GpioAccessTestUtils.MessageChecker.check_fields(
                test_case=self, message=set_group_in_response, expected_cls=self.feature_1803.set_group_in_response_cls,
                check_map={})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1803_0001", _AUTHOR)
    # end def test_set_group_in

    @features("Feature1803")
    @level("Functionality")
    @services("Debugger")
    def test_write_group_out(self):
        """
        Validate ``WriteGroupOut`` request API.
        
        [1] WriteGroupOut(portNumber, gpioMask, value) -> void
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_OVER_ALL_PORTS)
        # --------------------------------------------------------------------------------------------------------------
        for port_number in range(self.config.F_NumberOfPorts):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Send WriteGroupOut for Port {port_number} with project specific GpioMask and Value")
            # ----------------------------------------------------------------------------------------------------------
            write_group_out_response = GpioAccessTestUtils.HIDppHelper.write_group_out(
                test_case=self, port_number=port_number,
                gpio_mask=self.config.F_GpioOutputMask[port_number],
                value=self.config.F_GpioOutputValue[port_number])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _VALIDATE_API_SUCCESS)
            # ----------------------------------------------------------------------------------------------------------
            GpioAccessTestUtils.MessageChecker.check_fields(
                test_case=self, message=write_group_out_response,
                expected_cls=self.feature_1803.write_group_out_response_cls, check_map={})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1803_0002", _AUTHOR)
    # end def test_write_group_out

    @features("Feature1803")
    @level("Functionality")
    @services("Debugger")
    def test_read_group(self):
        """
        Validate ``ReadGroup`` request API.
        
        [2] ReadGroup(portNumber, gpioMask) -> portNumber, gpioMask, value
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_OVER_ALL_PORTS)
        # --------------------------------------------------------------------------------------------------------------
        for port_number in range(self.config.F_NumberOfPorts):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Send ReadGroup for Port {port_number} with project specific GpioInputMask and Value")
            # ----------------------------------------------------------------------------------------------------------
            read_group_response = GpioAccessTestUtils.HIDppHelper.read_group(
                test_case=self, port_number=port_number, gpio_mask=self.config.F_GpioInputMask[port_number])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate the PortNumber, GpioInputMask and value with project specific settings")
            # ----------------------------------------------------------------------------------------------------------
            checker = GpioAccessTestUtils.ReadGroupResponseChecker
            check_map = checker.get_default_check_map(test_case=self)
            check_map.update({
                "port_number": (checker.check_port_number, port_number),
                "gpio_mask": (checker.check_gpio_mask, self.config.F_GpioInputMask[port_number]),
                "value": (checker.check_value, self.config.F_GpioInputValue[port_number])
            })
            checker.check_fields(test_case=self, message=read_group_response,
                                 expected_cls=self.feature_1803.read_group_response_cls, check_map=check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1803_0003", _AUTHOR)
    # end def test_read_group

    @features("Feature1803")
    @level("Functionality")
    @services("Debugger")
    def test_write_group(self):
        """
        Validate ``WriteGroup`` request API.
        
        [3] WriteGroup( portNumber, gpioMask, value) -> void
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_OVER_ALL_PORTS)
        # --------------------------------------------------------------------------------------------------------------
        for port_number in range(self.config.F_NumberOfPorts):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Send WriteGroup for Port {port_number} with project specific GpioInputMask and Value")
            # ----------------------------------------------------------------------------------------------------------
            write_group_response = GpioAccessTestUtils.HIDppHelper.write_group(
                test_case=self, port_number=port_number,
                gpio_mask=self.config.F_GpioInputMask[port_number], value=self.config.F_GpioInputValue[port_number])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _VALIDATE_API_SUCCESS)
            # ----------------------------------------------------------------------------------------------------------
            GpioAccessTestUtils.MessageChecker.check_fields(
                test_case=self, message=write_group_response, expected_cls=self.feature_1803.write_group_response_cls,
                check_map={})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Send WriteGroup for Port {port_number} with project specific GpioOutputMask and Value")
            # ----------------------------------------------------------------------------------------------------------
            write_group_response = GpioAccessTestUtils.HIDppHelper.write_group(
                test_case=self, port_number=port_number,
                gpio_mask=self.config.F_GpioOutputMask[port_number], value=self.config.F_GpioOutputValue[port_number])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _VALIDATE_API_SUCCESS)
            # ----------------------------------------------------------------------------------------------------------
            GpioAccessTestUtils.MessageChecker.check_fields(
                test_case=self, message=write_group_response, expected_cls=self.feature_1803.write_group_response_cls,
                check_map={})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1803_0004", _AUTHOR)
    # end def test_write_group

    @features("Feature1803")
    @features("Feature1803HasUnusedGPIO")
    @level("Functionality")
    @services("Debugger")
    def test_unused_gpio_input_zero(self):
        """
        Check all the Unused Gpio input value is zero
        
        [0] SetGroupIn(portNumber, gpioMask) -> void
        """
        unused_value = 0x00000000

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_OVER_ALL_PORTS)
        # --------------------------------------------------------------------------------------------------------------
        for port_number in range(self.config.F_NumberOfPorts):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetGroupIn for Port {port_number} with Unused Gpio Mask")
            # ----------------------------------------------------------------------------------------------------------
            set_group_in_response = GpioAccessTestUtils.HIDppHelper.set_group_in(
                test_case=self, port_number=port_number, gpio_mask=self.config.F_GpioUnusedMask[port_number])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _VALIDATE_API_SUCCESS)
            # ----------------------------------------------------------------------------------------------------------
            GpioAccessTestUtils.MessageChecker.check_fields(
                test_case=self, message=set_group_in_response, expected_cls=self.feature_1803.set_group_in_response_cls,
                check_map={})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadGroup for Port {port_number} with Unused Gpio Mask")
            # ----------------------------------------------------------------------------------------------------------
            read_group_response = GpioAccessTestUtils.HIDppHelper.read_group(
                test_case=self, port_number=port_number, gpio_mask=self.config.F_GpioUnusedMask[port_number])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate the value field in the response is zero")
            # ----------------------------------------------------------------------------------------------------------
            checker = GpioAccessTestUtils.ReadGroupResponseChecker
            check_map = checker.get_default_check_map(test_case=self)
            check_map.update({
                "port_number": (checker.check_port_number, port_number),
                "gpio_mask": (checker.check_gpio_mask, self.config.F_GpioUnusedMask[port_number]),
                "value": (checker.check_value, unused_value)
            })
            checker.check_fields(test_case=self, message=read_group_response,
                                 expected_cls=self.feature_1803.read_group_response_cls, check_map=check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1803_0005", _AUTHOR)
    # end def test_unused_gpio_input_zero

    @features("Feature1803v1")
    @features("Feature1803SupportReadGroupOut")
    @level("Functionality")
    @services("Debugger")
    def test_read_group_out(self):
        """
        Validate ``ReadGroupOut`` request API.

        [4] ReadGroupOut(portNumber, gpioMask) -> value
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_OVER_ALL_PORTS)
        # --------------------------------------------------------------------------------------------------------------
        for port_number in range(self.config.F_NumberOfPorts):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadGroupOut for Port {port_number} with project specific GpioOutputMask")
            # ----------------------------------------------------------------------------------------------------------
            read_group_out_response = GpioAccessTestUtils.HIDppHelper.read_group_out(
                test_case=self, port_number=port_number, gpio_mask=self.config.F_GpioOutputMask[port_number])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate the PortNumber, GpioOutputMask and value with project specific"
                                      "settings")
            # ----------------------------------------------------------------------------------------------------------
            checker = GpioAccessTestUtils.ReadGroupOutResponseChecker
            check_map = checker.get_default_check_map(test_case=self)
            check_map.update({
                "port_number": (checker.check_port_number, port_number),
                "gpio_mask": (checker.check_gpio_mask, self.config.F_GpioOutputMask[port_number]),
                "value": (checker.check_value, self.config.F_GpioOutputValue[port_number])
            })
            checker.check_fields(test_case=self, message=read_group_out_response,
                                 expected_cls=self.feature_1803.read_group_out_response_cls, check_map=check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1803_0006", _AUTHOR)
    # end def test_read_group_out

    @features("Feature1803v1")
    @features("Feature1803HasUnusedGPIO")
    @features("Feature1803SupportReadGroupOut")
    @level("Functionality")
    @services("Debugger")
    def test_unused_gpio_output_zero(self):
        """
        Check all the Unused Gpio output value is zero

        [0] WriteGroupOut(portNumber, gpioMask) -> void

        [4] ReadGroupOut(portNumber, gpioMask) -> value
        """
        unused_value = 0x00000000
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_OVER_ALL_PORTS)
        # --------------------------------------------------------------------------------------------------------------
        for port_number in range(self.config.F_NumberOfPorts):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Send WriteGroupOut for Port {port_number} with unused GpioMask and Value")
            # ----------------------------------------------------------------------------------------------------------
            write_group_out_response = GpioAccessTestUtils.HIDppHelper.write_group_out(
                test_case=self, port_number=port_number,
                gpio_mask=self.config.F_GpioUnusedMask[port_number],
                value=unused_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _VALIDATE_API_SUCCESS)
            # ----------------------------------------------------------------------------------------------------------
            GpioAccessTestUtils.MessageChecker.check_fields(
                test_case=self, message=write_group_out_response,
                expected_cls=self.feature_1803.write_group_out_response_cls, check_map={})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadGroupOut for Port {port_number} with project specific GpioUnusedMask")
            # ----------------------------------------------------------------------------------------------------------
            read_group_out_response = GpioAccessTestUtils.HIDppHelper.read_group_out(
                test_case=self, port_number=port_number, gpio_mask=self.config.F_GpioUnusedMask[port_number])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate the PortNumber, GpioUnusedMask and value with project specific"
                                      "settings")
            # ----------------------------------------------------------------------------------------------------------
            checker = GpioAccessTestUtils.ReadGroupOutResponseChecker
            check_map = checker.get_default_check_map(test_case=self)
            check_map.update({
                "port_number": (checker.check_port_number, port_number),
                "gpio_mask": (checker.check_gpio_mask, self.config.F_GpioUnusedMask[port_number]),
                "value": (checker.check_value, unused_value)
            })
            checker.check_fields(test_case=self, message=read_group_out_response,
                                 expected_cls=self.feature_1803.read_group_out_response_cls, check_map=check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1803_0007", _AUTHOR)
    # end def test_unused_gpio_output_zero
# end class GpioAccessFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
