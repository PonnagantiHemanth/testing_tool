#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.keyboard.feature_4540.robustness
:brief: HID++ 2.0 ``KeyboardInternationalLayouts`` robustness test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/12/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.keyboard.keyboardinternationallayouts import KeyboardInternationalLayouts
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keyboardinternationallayoutsutils import KeyboardInternationalLayoutsTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4540.keyboardinternationallayouts \
    import KeyboardInternationalLayoutsTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class KeyboardInternationalLayoutsRobustnessTestCase(KeyboardInternationalLayoutsTestCase):
    """
    Validate ``KeyboardInternationalLayouts`` robustness test cases
    """

    @features("Feature4540")
    @level("Robustness")
    @services("Debugger")
    def test_get_keyboard_layout_software_id(self):
        """
        Validate ``GetKeyboardLayout`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(KeyboardInternationalLayouts.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetKeyboardLayout request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_4540.get_keyboard_layout_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_4540_index)
            report.software_id = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=self.feature_4540.get_keyboard_layout_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetKeyboardLayoutResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = KeyboardInternationalLayoutsTestUtils.GetKeyboardLayoutResponseChecker
            checker.check_fields(self, response, self.feature_4540.get_keyboard_layout_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4540_0001#1", _AUTHOR)
    # end def test_get_keyboard_layout_software_id

    @features("Feature4540")
    @level("Robustness")
    @services("Debugger")
    def test_get_keyboard_layout_padding(self):
        """
        Validate ``GetKeyboardLayout`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_4540.get_keyboard_layout_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetKeyboardLayout request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_4540_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=self.feature_4540.get_keyboard_layout_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetKeyboardLayoutResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = KeyboardInternationalLayoutsTestUtils.GetKeyboardLayoutResponseChecker
            checker.check_fields(self, response, self.feature_4540.get_keyboard_layout_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4540_0002#1", _AUTHOR)
    # end def test_get_keyboard_layout_padding
# end class KeyboardInternationalLayoutsRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
