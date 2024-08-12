#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_18a1.robustness
:brief: HID++ 2.0 ``LEDTest`` robustness test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2023/06/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.common.ledtest import LEDTest
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.ledtestutils import LEDTestTestUtils
from pytestbox.device.hidpp20.common.feature_18a1.ledtest import LEDTestTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_RESERVED = "Test loop over reserved range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class LEDTestRobustnessTestCase(LEDTestTestCase):
    """
    Validate ``LEDTest`` robustness test cases
    """

    @features("Feature18A1")
    @level("Robustness")
    def test_get_led_list_software_id(self):
        """
        Validate ``GetLEDList`` software id field is ignored by the firmware

        [0] getLEDList() -> ledMaskPresence1, ledMaskPresence2, ledGenericMaskPresence1, ledGenericMaskPresence2,
        ledGenericMaskPresence3

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(LEDTest.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetLEDList request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = LEDTestTestUtils.HIDppHelper.get_led_list(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetLEDListResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = LEDTestTestUtils.GetLEDListResponseChecker
            checker.check_fields(self, response, self.feature_18a1.get_led_list_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_18A1_0001#1", _AUTHOR)
    # end def test_get_led_list_software_id

    @features("Feature18A1")
    @level("Robustness")
    def test_get_led_test_mode_software_id(self):
        """
        Validate ``GetLEDTestMode`` software id field is ignored by the firmware

        [1] getLEDTestMode() -> ledMaskState1, ledMaskPresence2, ledGenericMaskState1, ledGenericMaskState2,
        ledGenericMaskState3

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(LEDTest.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetLEDTestMode request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = LEDTestTestUtils.HIDppHelper.get_led_test_mode(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetLEDTestModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = LEDTestTestUtils.GetLEDTestModeResponseChecker
            checker.check_fields(self, response, self.feature_18a1.get_led_test_mode_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_18A1_0001#2", _AUTHOR)
    # end def test_get_led_test_mode_software_id

    @features("Feature18A1")
    @level("Robustness")
    def test_set_led_test_mode_software_id(self):
        """
        Validate ``SetLEDTestMode`` software id field is ignored by the firmware

        [2] setLEDTestMode(ledMaskState1, ledMaskState2, ledGenericMaskState1, ledGenericMaskState2,
        ledGenericMaskState3) -> None

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.LEDMaskState1BitMap.LEDGenericMaskState1BitMap.
        LEDGenericMaskState2BitMap.LEDGenericMaskState3BitMap.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(LEDTest.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetLEDTestMode request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = LEDTestTestUtils.HIDppHelper.set_led_test_mode(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetLEDTestModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = LEDTestTestUtils.SetLEDTestModeResponseChecker
            checker.check_fields(self, response, self.feature_18a1.set_led_test_mode_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_18A1_0001#3", _AUTHOR)
    # end def test_set_led_test_mode_software_id

    @features("Feature18A1")
    @level("Robustness")
    def test_get_led_list_padding(self):
        """
        Validate ``GetLEDList`` padding bytes are ignored by the firmware

        [0] getLEDList() -> ledMaskPresence1, ledMaskPresence2, ledGenericMaskPresence1, ledGenericMaskPresence2,
        ledGenericMaskPresence3

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_18a1.get_led_list_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetLEDList request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = LEDTestTestUtils.HIDppHelper.get_led_list(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetLEDListResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = LEDTestTestUtils.GetLEDListResponseChecker
            checker.check_fields(self, response, self.feature_18a1.get_led_list_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_18A1_0002#1", _AUTHOR)
    # end def test_get_led_list_padding

    @features("Feature18A1")
    @level("Robustness")
    def test_get_led_test_mode_padding(self):
        """
        Validate ``GetLEDTestMode`` padding bytes are ignored by the firmware

        [1] getLEDTestMode() -> ledMaskState1, ledMaskState2, ledGenericMaskState1, ledGenericMaskState2,
        ledGenericMaskState3

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_18a1.get_led_test_mode_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetLEDTestMode request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = LEDTestTestUtils.HIDppHelper.get_led_test_mode(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetLEDTestModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = LEDTestTestUtils.GetLEDTestModeResponseChecker
            checker.check_fields(self, response, self.feature_18a1.get_led_test_mode_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_18A1_0002#2", _AUTHOR)
    # end def test_get_led_test_mode_padding

    @features("Feature18A1")
    @level("Robustness")
    def test_set_led_test_mode_padding(self):
        """
        Validate ``SetLEDTestMode`` padding bytes are ignored by the firmware

        [2] setLEDTestMode(ledMaskState1, ledMaskState2, ledGenericMaskState1, ledGenericMaskState2,
        ledGenericMaskState3) -> None

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.LEDMaskState1BitMap.LEDGenericMaskState1BitMap.
        LEDGenericMaskState2BitMap.LEDGenericMaskState3BitMap.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_18a1.set_led_test_mode_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetLEDTestMode request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = LEDTestTestUtils.HIDppHelper.set_led_test_mode(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetLEDTestModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = LEDTestTestUtils.SetLEDTestModeResponseChecker
            checker.check_fields(self, response, self.feature_18a1.set_led_test_mode_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_18A1_0002#3", _AUTHOR)
    # end def test_set_led_test_mode_padding
# end class LEDTestRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
