#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1803.robustness
:brief: HID++ 2.0 ``GpioAccess`` robustness test suite
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/06/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.gpioaccess import GpioAccess
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.gpioaccessutils import GpioAccessTestUtils
from pytestbox.device.hidpp20.common.feature_1803.gpioaccess import GpioAccessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vinodh Selvaraj"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class GpioAccessRobustnessTestCase(GpioAccessTestCase):
    """
    Validate ``GpioAccess`` robustness test cases
    """

    @features("Feature1803")
    @level("Robustness")
    @services("Debugger")
    def test_set_group_in_software_id(self):
        """
        Validate ``SetGroupIn`` software id field is ignored by the firmware

        [0] setGroupIn(portNumber, gpioMask) -> None

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.PortNumber.GpioMask.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.
        0xPP.0xPP.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        port_number = 0
        gpio_mask = Numeral(self.config.F_GpioInputMask[port_number])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(GpioAccess.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetGroupIn request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = GpioAccessTestUtils.HIDppHelper.set_group_in(
                test_case=self,
                port_number=port_number,
                gpio_mask=HexList(gpio_mask),
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetGroupInResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            GpioAccessTestUtils.MessageChecker.check_fields(
                self, response, self.feature_1803.set_group_in_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1803_0001#1", _AUTHOR)
    # end def test_set_group_in_software_id

    @features("Feature1803")
    @level("Robustness")
    @services("Debugger")
    def test_write_group_out_software_id(self):
        """
        Validate ``WriteGroupOut`` software id field is ignored by the firmware

        [1] writeGroupOut(portNumber, gpioMask, value) -> None

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.PortNumber.GpioMask.Value.0xPP.0xPP.0xPP.0xPP.0xPP.
        0xPP.0xPP

        SwID boundary values [0..F]
        """
        port_number = 0
        gpio_mask = Numeral(self.config.F_GpioOutputMask[port_number])
        value = Numeral(self.config.F_GpioOutputValue[port_number])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(GpioAccess.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send WriteGroupOut request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = GpioAccessTestUtils.HIDppHelper.write_group_out(
                test_case=self,
                port_number=port_number,
                gpio_mask=HexList(gpio_mask),
                value=HexList(value),
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check WriteGroupOutResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            GpioAccessTestUtils.MessageChecker.check_fields(
                self, response, self.feature_1803.write_group_out_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1803_0001#2", _AUTHOR)
    # end def test_write_group_out_software_id

    @features("Feature1803")
    @level("Robustness")
    @services("Debugger")
    def test_read_group_software_id(self):
        """
        Validate ``ReadGroup`` software id field is ignored by the firmware

        [2] readGroup(portNumber, gpioMask) -> portNumber, gpioMask, value

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.PortNumber.GpioMask.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.
        0xPP.0xPP.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        port_number = 0
        gpio_mask = Numeral(self.config.F_GpioInputMask[port_number])
        value = Numeral(self.config.F_GpioInputValue[port_number])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(GpioAccess.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadGroup request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = GpioAccessTestUtils.HIDppHelper.read_group(
                test_case=self,
                port_number=port_number,
                gpio_mask=HexList(gpio_mask),
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ReadGroupResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = GpioAccessTestUtils.ReadGroupResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "port_number": (checker.check_port_number, port_number),
                "gpio_mask": (checker.check_gpio_mask, gpio_mask),
                "value": (checker.check_value, value)
            })
            checker.check_fields(self, response, self.feature_1803.read_group_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1803_0001#3", _AUTHOR)
    # end def test_read_group_software_id

    @features("Feature1803")
    @level("Robustness")
    @services("Debugger")
    def test_write_group_software_id(self):
        """
        Validate ``WriteGroup`` software id field is ignored by the firmware

        [3] writeGroup(portNumber, gpioMask, value) -> None

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.PortNumber.GpioMask.Value.0xPP.0xPP.0xPP.0xPP.0xPP.
        0xPP.0xPP

        SwID boundary values [0..F]
        """
        port_number = 0
        gpio_mask = Numeral(self.config.F_GpioInputMask[port_number])
        value = Numeral(self.config.F_GpioInputValue[port_number])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(GpioAccess.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send WriteGroup request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = GpioAccessTestUtils.HIDppHelper.write_group(
                test_case=self,
                port_number=port_number,
                gpio_mask=HexList(gpio_mask),
                value=HexList(value),
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check WriteGroupResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            GpioAccessTestUtils.MessageChecker.check_fields(
                self, response, self.feature_1803.write_group_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1803_0001#4", _AUTHOR)
    # end def test_write_group_software_id

    @features("Feature1803v1")
    @features("Feature1803SupportReadGroupOut")
    @level("Robustness")
    def test_read_group_out_software_id_v1(self):
        """
        Validate ``ReadGroupOutV1`` software id field is ignored by the firmware

        [4] readGroupOut(portNumber, gpioMask) -> portNumber, gpioMask, value

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.PortNumber.GpioMask.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.
        0xPP.0xPP.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        port_number = 0
        gpio_mask = Numeral(self.config.F_GpioOutputMask[port_number])
        value = Numeral(self.config.F_GpioOutputValue[port_number])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(GpioAccess.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadGroupOutV1 request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = GpioAccessTestUtils.HIDppHelper.read_group_out(
                test_case=self,
                port_number=port_number,
                gpio_mask=HexList(gpio_mask),
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ReadGroupOutResponseV1 fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = GpioAccessTestUtils.ReadGroupOutResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "port_number": (checker.check_port_number, port_number),
                "gpio_mask": (checker.check_gpio_mask, gpio_mask),
                "value": (checker.check_value, value)
            })
            checker.check_fields(self, response, self.feature_1803.read_group_out_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1803_0001#5", _AUTHOR)
    # end def test_read_group_out_software_id_v1

    @features("Feature1803")
    @level("Robustness")
    @services("Debugger")
    def test_set_group_in_padding(self):
        """
        Validate ``SetGroupIn`` padding bytes are ignored by the firmware

        [0] setGroupIn(portNumber, gpioMask) -> None

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.PortNumber.GpioMask.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.
        0xPP.0xPP.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        port_number = 0
        gpio_mask = Numeral(self.config.F_GpioInputMask[port_number])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1803.set_group_in_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetGroupIn request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = GpioAccessTestUtils.HIDppHelper.set_group_in(
                test_case=self,
                port_number=port_number,
                gpio_mask=HexList(gpio_mask),
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetGroupInResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            GpioAccessTestUtils.MessageChecker.check_fields(
                self, response, self.feature_1803.set_group_in_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1803_0002#1", _AUTHOR)
    # end def test_set_group_in_padding

    @features("Feature1803")
    @level("Robustness")
    @services("Debugger")
    def test_write_group_out_padding(self):
        """
        Validate ``WriteGroupOut`` padding bytes are ignored by the firmware

        [1] writeGroupOut(portNumber, gpioMask, value) -> None

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.PortNumber.GpioMask.Value.0xPP.0xPP.0xPP.0xPP.0xPP.
        0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        port_number = 0
        gpio_mask = Numeral(self.config.F_GpioOutputMask[port_number])
        value = Numeral(self.config.F_GpioOutputValue[port_number])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1803.write_group_out_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send WriteGroupOut request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = GpioAccessTestUtils.HIDppHelper.write_group_out(
                test_case=self,
                port_number=port_number,
                gpio_mask=HexList(gpio_mask),
                value=HexList(value),
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check WriteGroupOutResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            GpioAccessTestUtils.MessageChecker.check_fields(
                self, response, self.feature_1803.write_group_out_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1803_0002#2", _AUTHOR)
    # end def test_write_group_out_padding

    @features("Feature1803")
    @level("Robustness")
    @services("Debugger")
    def test_read_group_padding(self):
        """
        Validate ``ReadGroup`` padding bytes are ignored by the firmware

        [2] readGroup(portNumber, gpioMask) -> portNumber, gpioMask, value

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.PortNumber.GpioMask.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.
        0xPP.0xPP.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        port_number = 0
        gpio_mask = Numeral(self.config.F_GpioInputMask[port_number])
        value = Numeral(self.config.F_GpioInputValue[port_number])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1803.read_group_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadGroup request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = GpioAccessTestUtils.HIDppHelper.read_group(
                test_case=self,
                port_number=port_number,
                gpio_mask=HexList(gpio_mask),
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ReadGroupResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = GpioAccessTestUtils.ReadGroupResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "port_number": (checker.check_port_number, port_number),
                "gpio_mask": (checker.check_gpio_mask, gpio_mask),
                "value": (checker.check_value, value)
            })
            checker.check_fields(self, response, self.feature_1803.read_group_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1803_0002#3", _AUTHOR)
    # end def test_read_group_padding

    @features("Feature1803")
    @level("Robustness")
    @services("Debugger")
    def test_write_group_padding(self):
        """
        Validate ``WriteGroup`` padding bytes are ignored by the firmware

        [3] writeGroup(portNumber, gpioMask, value) -> None

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.PortNumber.GpioMask.Value.0xPP.0xPP.0xPP.0xPP.0xPP.
        0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        port_number = 0
        gpio_mask = Numeral(self.config.F_GpioInputMask[port_number])
        value = Numeral(self.config.F_GpioInputValue[port_number])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1803.write_group_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send WriteGroup request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = GpioAccessTestUtils.HIDppHelper.write_group(
                test_case=self,
                port_number=port_number,
                gpio_mask=HexList(gpio_mask),
                value=HexList(value),
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check WriteGroupResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            GpioAccessTestUtils.MessageChecker.check_fields(
                self, response, self.feature_1803.write_group_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1803_0002#4", _AUTHOR)
    # end def test_write_group_padding

    @features("Feature1803v1")
    @features("Feature1803SupportReadGroupOut")
    @level("Robustness")
    @services("Debugger")
    def test_read_group_out_padding_v1(self):
        """
        Validate ``ReadGroupOutV1`` padding bytes are ignored by the firmware

        [4] readGroupOut(portNumber, gpioMask) -> portNumber, gpioMask, value

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.PortNumber.GpioMask.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.
        0xPP.0xPP.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        port_number = 0
        gpio_mask = Numeral(self.config.F_GpioOutputMask[port_number])
        value = Numeral(self.config.F_GpioOutputValue[port_number])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1803.read_group_out_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadGroupOutV1 request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = GpioAccessTestUtils.HIDppHelper.read_group_out(
                test_case=self,
                port_number=port_number,
                gpio_mask=HexList(gpio_mask),
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ReadGroupOutResponseV1 fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = GpioAccessTestUtils.ReadGroupOutResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "port_number": (checker.check_port_number, port_number),
                "gpio_mask": (checker.check_gpio_mask, gpio_mask),
                "value": (checker.check_value, value)
            })
            checker.check_fields(self, response, self.feature_1803.read_group_out_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1803_0002#5", _AUTHOR)
    # end def test_read_group_out_padding_v1
# end class GpioAccessRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
