#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.common.feature_1803.interface
:brief: HID++ 2.0 ``GpioAccess`` interface test suite
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2022/09/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.gpioaccessutils import GpioAccessTestUtils
from pytestbox.device.hidpp20.common.feature_1803.gpioaccess import GpioAccessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vinodh Selvaraj"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class GpioAccessInterfaceTestCase(GpioAccessTestCase):
    """
    Validate ``GpioAccess`` interface test cases
    """
    @features("Feature1803")
    @level("Interface")
    @services("Debugger")
    def test_set_group_in(self):
        """
        Validate ``SetGroupIn`` normal processing

        [0] setGroupIn(portNumber, gpioMask) -> None
        """
        port_number = 0
        gpio_mask = Numeral(self.config.F_GpioInputMask[port_number])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetGroupIn request")
        # --------------------------------------------------------------------------------------------------------------
        response = GpioAccessTestUtils.HIDppHelper.set_group_in(
            test_case=self,
            port_number=port_number,
            gpio_mask=HexList(gpio_mask))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetGroupInResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = GpioAccessTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_1803_index))
        }
        checker.check_fields(self, response, self.feature_1803.set_group_in_response_cls, check_map)

        self.testCaseChecked("INT_1803_0001", _AUTHOR)
    # end def test_set_group_in

    @features("Feature1803")
    @level("Interface")
    @services("Debugger")
    def test_write_group_out(self):
        """
        Validate ``WriteGroupOut`` normal processing

        [1] writeGroupOut(portNumber, gpioMask, value) -> None
        """
        port_number = 0
        gpio_mask = Numeral(self.config.F_GpioOutputMask[port_number])
        value = Numeral(self.config.F_GpioOutputValue[port_number])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send WriteGroupOut request")
        # --------------------------------------------------------------------------------------------------------------
        response = GpioAccessTestUtils.HIDppHelper.write_group_out(
            test_case=self,
            port_number=port_number,
            gpio_mask=HexList(gpio_mask),
            value=HexList(value))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check WriteGroupOutResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = GpioAccessTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_1803_index))
        }
        checker.check_fields(self, response, self.feature_1803.write_group_out_response_cls, check_map)

        self.testCaseChecked("INT_1803_0002", _AUTHOR)
    # end def test_write_group_out

    @features("Feature1803")
    @level("Interface")
    @services("Debugger")
    def test_read_group(self):
        """
        Validate ``ReadGroup`` normal processing

        [2] readGroup(portNumber, gpioMask) -> portNumber, gpioMask, value
        """
        port_number = 0
        gpio_mask = Numeral(self.config.F_GpioInputMask[port_number])
        value = Numeral(self.config.F_GpioInputValue[port_number])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadGroup request")
        # --------------------------------------------------------------------------------------------------------------
        response = GpioAccessTestUtils.HIDppHelper.read_group(
            test_case=self,
            port_number=port_number,
            gpio_mask=HexList(gpio_mask))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ReadGroupResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = GpioAccessTestUtils.ReadGroupResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_1803_index)),
            "port_number": (checker.check_port_number, port_number),
            "gpio_mask": (checker.check_gpio_mask, gpio_mask),
            "value": (checker.check_value, value)
        })
        checker.check_fields(self, response, self.feature_1803.read_group_response_cls, check_map)

        self.testCaseChecked("INT_1803_0003", _AUTHOR)
    # end def test_read_group

    @features("Feature1803")
    @level("Interface")
    @services("Debugger")
    def test_write_group(self):
        """
        Validate ``WriteGroup`` normal processing

        [3] writeGroup(portNumber, gpioMask, value) -> None
        """
        port_number = 0
        gpio_mask = Numeral(self.config.F_GpioInputMask[port_number])
        value = Numeral(self.config.F_GpioInputValue[port_number])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send WriteGroup request")
        # --------------------------------------------------------------------------------------------------------------
        response = GpioAccessTestUtils.HIDppHelper.write_group(
            test_case=self,
            port_number=port_number,
            gpio_mask=HexList(gpio_mask),
            value=HexList(value))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check WriteGroupResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = GpioAccessTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_1803_index))
        }
        checker.check_fields(self, response, self.feature_1803.write_group_response_cls, check_map)

        self.testCaseChecked("INT_1803_0004", _AUTHOR)
    # end def test_write_group

    @features("Feature1803v1")
    @features("Feature1803SupportReadGroupOut")
    @level("Interface")
    def test_read_group_out(self):
        """
        Validate ``ReadGroupOutV1`` normal processing

        [4] readGroupOut(portNumber, gpioMask) -> portNumber, gpioMask, value
        """
        port_number = 0
        gpio_mask = Numeral(self.config.F_GpioOutputMask[port_number])
        value = Numeral(self.config.F_GpioOutputValue[port_number])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadGroupOutV1 request")
        # --------------------------------------------------------------------------------------------------------------
        response = GpioAccessTestUtils.HIDppHelper.read_group_out(
            test_case=self,
            port_number=port_number,
            gpio_mask=HexList(gpio_mask))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ReadGroupOutResponseV1 fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = GpioAccessTestUtils.ReadGroupOutResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_1803_index)),
            "port_number": (checker.check_port_number, port_number),
            "gpio_mask": (checker.check_gpio_mask, gpio_mask),
            "value": (checker.check_value, value)
        })
        checker.check_fields(self, response, self.feature_1803.read_group_out_response_cls, check_map)

        self.testCaseChecked("INT_1803_0005", _AUTHOR)
    # end def test_read_group_out
# end class GpioAccessInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
