#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1803.errorhandling
:brief: HID++ 2.0 ``GpioAccess`` error handling test suite
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/06/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.gpioaccessutils import GpioAccessTestUtils
from pytestbox.device.hidpp20.common.feature_1803.gpioaccess import GpioAccessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vinodh Selvaraj"
_LOOP_END = "End Test Loop"
_LOOP_FORBIDDEN_GPIO = "Test loop over Forbidden gpio for each port"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"
_LOOP_PORT_NUMBERS = "Test loop over with different port numbers"
_CHECK_ERROR_CODE = "Check 'INVALID ARGUMENT' Error Code returned by the device"
_ZERO_BIT_MASK = [HexList('00000000'), HexList('0000')]


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class GpioAccessErrorHandlingTestCase(GpioAccessTestCase):
    """
    Validate ``GpioAccess`` errorhandling test cases
    """

    @features("Feature1803")
    @level("ErrorHandling")
    @services("Debugger")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        port_number = 0x0
        gpio_mask = 0x0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_1803.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetGroupIn request with a wrong function index: {function_index}")
            # ----------------------------------------------------------------------------------------------------------
            GpioAccessTestUtils.HIDppHelper.set_group_in_and_check_error(
                test_case=self,
                error_codes=[Hidpp2ErrorCodes.INVALID_FUNCTION_ID],
                port_number=port_number,
                gpio_mask=HexList(gpio_mask),
                function_index=function_index)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_1803_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature1803")
    @level("ErrorHandling")
    @services("Debugger")
    def test_set_group_in_wrong_port_number(self):
        """
        Validates wrong parameter (port_number)
        
        [0] SetGroupIn(portNumber, gpioMask) -> void
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_PORT_NUMBERS)
        # --------------------------------------------------------------------------------------------------------------
        for port_number in compute_wrong_range(value=list(range(self.config.F_NumberOfPorts + 1)), max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetGroupIn with wrong PortNumber={port_number}")
            # ----------------------------------------------------------------------------------------------------------
            GpioAccessTestUtils.HIDppHelper.set_group_in_and_check_error(
                test_case=self,
                error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT],
                port_number=port_number,
                gpio_mask=0)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1803_0002", _AUTHOR)
    # end def test_set_group_in_wrong_port_number

    @features("Feature1803")
    @level("ErrorHandling")
    @services("Debugger")
    def test_write_group_out_wrong_port_number(self):
        """
        Validates wrong parameter (port_number)
        
        [1] WriteGroupOut(portNumber, gpioMask, value) -> void
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_PORT_NUMBERS)
        # --------------------------------------------------------------------------------------------------------------
        for port_number in compute_wrong_range(value=list(range(self.config.F_NumberOfPorts + 1)), max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send WriteGroupOut with wrong PortNumber={port_number}")
            # ----------------------------------------------------------------------------------------------------------
            GpioAccessTestUtils.HIDppHelper.write_group_out_and_check_error(
                test_case=self,
                error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT],
                port_number=HexList(port_number),
                gpio_mask=0,
                value=0)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1803_0003", _AUTHOR)
    # end def test_write_group_out_wrong_port_number

    @features("Feature1803")
    @level("ErrorHandling")
    @services("Debugger")
    def test_read_group_wrong_port_number(self):
        """
        Validates wrong parameter (port_number)
        
        [2] ReadGroup(portNumber, gpioMask) -> portNumber, gpioMask, value
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_PORT_NUMBERS)
        # --------------------------------------------------------------------------------------------------------------
        for port_number in compute_wrong_range(value=list(range(self.config.F_NumberOfPorts + 1)), max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadGroup with wrong PortNumber={port_number}")
            # ----------------------------------------------------------------------------------------------------------
            GpioAccessTestUtils.HIDppHelper.read_group_and_check_error(
                test_case=self,
                error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT],
                port_number=HexList(port_number),
                gpio_mask=0)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1803_0004", _AUTHOR)
    # end def test_read_group_wrong_port_number

    @features("Feature1803")
    @level("ErrorHandling")
    @services("Debugger")
    def test_write_group_wrong_port_number(self):
        """
        Validates wrong parameter (port_number)
        
        [3] WriteGroup(portNumber, gpioMask, value) -> void
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_PORT_NUMBERS)
        # --------------------------------------------------------------------------------------------------------------
        for port_number in compute_wrong_range(value=list(range(self.config.F_NumberOfPorts + 1)), max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send WriteGroup with wrong PortNumber={port_number}")
            # ----------------------------------------------------------------------------------------------------------
            GpioAccessTestUtils.HIDppHelper.write_group_and_check_error(
                test_case=self,
                error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT],
                port_number=HexList(port_number),
                gpio_mask=0,
                value=0)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1803_0005", _AUTHOR)
    # end def test_write_group_wrong_port_number

    @features("Feature1803")
    @features("Feature1803HasForbiddenMask")
    @level("ErrorHandling")
    @services("Debugger")
    def test_read_group_out_wrong_port_number(self):
        """
        Validates wrong parameter (port_number)

        [4] ReadGroupOut(portNumber, gpioMask) -> value
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_PORT_NUMBERS)
        # --------------------------------------------------------------------------------------------------------------
        for port_number in compute_wrong_range(value=list(range(self.config.F_NumberOfPorts + 1)), max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send ReadGroupOut with wrong PortNumbers")
            # ----------------------------------------------------------------------------------------------------------
            GpioAccessTestUtils.HIDppHelper.read_group_out_and_check_error(
                test_case=self,
                error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT],
                port_number=port_number,
                gpio_mask=0)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1803_0010", _AUTHOR)
    # end def test_read_group_out_wrong_parameter

    @features("Feature1803")
    @features("Feature1803HasForbiddenMask")
    @level("ErrorHandling")
    @services("Debugger")
    def test_set_group_in_forbidden_mask(self):
        """
        Ignore request when sending argument of forbidden GpioMask
        
        [0] SetGroupIn(portNumber, gpioMask) -> void
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_FORBIDDEN_GPIO)
        # --------------------------------------------------------------------------------------------------------------
        for port_number in range(self.config.F_NumberOfPorts):
            for bit_position in range(len(HexList(self.config.F_GpioForbiddenMask[port_number]))*8):
                if HexList(self.config.F_GpioForbiddenMask[port_number]).testBit(bit_position):
                    forbidden_gpio_mask = _ZERO_BIT_MASK[port_number]
                    forbidden_gpio_mask.setBit(bit_position)
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(
                        self, f"Send SetGroupIn with gpio_mask={forbidden_gpio_mask} and port_number={port_number}")
                    # --------------------------------------------------------------------------------------------------
                    GpioAccessTestUtils.HIDppHelper.set_group_in_and_check_error(
                        test_case=self,
                        error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT],
                        port_number=HexList(port_number),
                        gpio_mask=forbidden_gpio_mask)
                    forbidden_gpio_mask.invertBit(bit_position)
                # end if
            # end for
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1803_0006", _AUTHOR)
    # end def test_set_group_in_forbidden_mask

    @features("Feature1803")
    @features("Feature1803HasForbiddenMask")
    @level("ErrorHandling")
    @services("Debugger")
    def test_write_group_out_forbidden_mask(self):
        """
        Ignore request when sending argument of forbidden GpioMask
        
        [1] WriteGroupOut(portNumber, gpioMask, value) -> void
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_FORBIDDEN_GPIO)
        # --------------------------------------------------------------------------------------------------------------
        for port_number in range(self.config.F_NumberOfPorts):
            for bit_position in range(len(HexList(self.config.F_GpioForbiddenMask[port_number]))*8):
                if HexList(self.config.F_GpioForbiddenMask[port_number]).testBit(bit_position):
                    forbidden_gpio_mask = _ZERO_BIT_MASK[port_number]
                    forbidden_gpio_mask.setBit(bit_position)
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(
                        self, f"Send WriteGroupOut with gpio_mask={forbidden_gpio_mask} and port_number={port_number}")
                    # --------------------------------------------------------------------------------------------------
                    GpioAccessTestUtils.HIDppHelper.write_group_out_and_check_error(
                        test_case=self,
                        error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT],
                        port_number=HexList(port_number),
                        gpio_mask=HexList(self.config.F_GpioForbiddenMask[port_number]),
                        value=0)
                    forbidden_gpio_mask.invertBit(bit_position)
                # end if
            # end for
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1803_0007", _AUTHOR)
    # end def test_write_group_out_forbidden_mask

    @features("Feature1803")
    @features("Feature1803HasForbiddenMask")
    @level("ErrorHandling")
    @services("Debugger")
    def test_read_group_forbidden_mask(self):
        """
        Ignore request when sending argument of forbidden GpioMask
        
        [2] ReadGroup(portNumber, gpioMask) -> portNumber, gpioMask, value
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_FORBIDDEN_GPIO)
        # --------------------------------------------------------------------------------------------------------------
        for port_number in range(self.config.F_NumberOfPorts):
            for bit_position in range(len(HexList(self.config.F_GpioForbiddenMask[port_number])) * 8):
                if HexList(self.config.F_GpioForbiddenMask[port_number]).testBit(bit_position):
                    forbidden_gpio_mask = _ZERO_BIT_MASK[port_number]
                    forbidden_gpio_mask.setBit(bit_position)
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(
                        self, f"Send ReadGroup with gpio_mask={forbidden_gpio_mask} and port_number={port_number}")
                    # --------------------------------------------------------------------------------------------------
                    GpioAccessTestUtils.HIDppHelper.read_group_and_check_error(
                        test_case=self,
                        error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT],
                        port_number=HexList(port_number),
                        gpio_mask=forbidden_gpio_mask)
                # end if
            # end for
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1803_0008", _AUTHOR)
    # end def test_read_group_forbidden_mask

    @features("Feature1803")
    @features("Feature1803HasForbiddenMask")
    @level("ErrorHandling")
    @services("Debugger")
    def test_write_group_forbidden_mask(self):
        """
        Ignore request when sending argument of forbidden GpioMask
        
        [3] WriteGroup(portNumber, gpioMask, value) -> void
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_FORBIDDEN_GPIO)
        # --------------------------------------------------------------------------------------------------------------
        for port_number in range(self.config.F_NumberOfPorts):
            for bit_position in range(len(HexList(self.config.F_GpioForbiddenMask[port_number])) * 8):
                if HexList(self.config.F_GpioForbiddenMask[port_number]).testBit(bit_position):
                    forbidden_gpio_mask = _ZERO_BIT_MASK[port_number]
                    forbidden_gpio_mask.setBit(bit_position)
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(
                        self, f"Send WriteGroup with gpio_mask={forbidden_gpio_mask} and port_number={port_number}")
                    # --------------------------------------------------------------------------------------------------
                    GpioAccessTestUtils.HIDppHelper.write_group_and_check_error(
                        test_case=self,
                        error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT],
                        port_number=HexList(port_number),
                        gpio_mask=forbidden_gpio_mask,
                        value=0)
                # end if
            # end for
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1803_0009", _AUTHOR)
    # end def test_write_group_forbidden_mask

    @features("Feature1803")
    @features("Feature1803HasForbiddenMask")
    @level("ErrorHandling")
    @services("Debugger")
    def test_read_group_out_forbidden_mask(self):
        """
        Ignore request when sending argument of forbidden GpioMask

        [4] ReadGroupOut(portNumber, gpioMask) -> value
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_FORBIDDEN_GPIO)
        # --------------------------------------------------------------------------------------------------------------
        for port_number in range(self.config.F_NumberOfPorts):
            for bit_position in range(len(HexList(self.config.F_GpioForbiddenMask[port_number])) * 8):
                if HexList(self.config.F_GpioForbiddenMask[port_number]).testBit(bit_position):
                    forbidden_gpio_mask = _ZERO_BIT_MASK[port_number]
                    forbidden_gpio_mask.setBit(bit_position)
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(
                        self, f"Send ReadGroupOut with gpio_mask={forbidden_gpio_mask} and port_number={port_number}")
                    # --------------------------------------------------------------------------------------------------
                    GpioAccessTestUtils.HIDppHelper.read_group_out_and_check_error(
                        test_case=self,
                        error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT],
                        port_number=HexList(port_number),
                        gpio_mask=forbidden_gpio_mask)
                # end if
            # end for
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1803_0011", _AUTHOR)
    # end def test_read_group_out_forbidden_mask
# end class GpioAccessErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
