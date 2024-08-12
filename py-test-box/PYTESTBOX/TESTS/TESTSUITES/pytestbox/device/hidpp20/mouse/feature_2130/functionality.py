#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.mouse.feature_2130.functionality
:brief: HID++ 2.0 ``RatchetWheel`` functionality test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/12/01
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.mouse.ratchetwheel import RatchetWheel
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.ratchetwheelutils import RatchetWheelTestUtils
from pytestbox.device.hidpp20.mouse.feature_2130.ratchetwheel import RatchetWheelTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class RatchetWheelFunctionalityTestCase(RatchetWheelTestCase):
    """
    Validate ``RatchetWheel`` functionality test cases
    """

    @features("Feature2130")
    @level("Functionality")
    def test_set_wheel_mode(self):
        """
        Validate SetWheelMode functional processing
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over divert in range [0..1]")
        # --------------------------------------------------------------------------------------------------------------
        for i in [RatchetWheel.DIVERT.HID, RatchetWheel.DIVERT.HIDPP]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetWheelMode with divert = {i}")
            # ----------------------------------------------------------------------------------------------------------
            response = RatchetWheelTestUtils.HIDppHelper.set_mode_status(self, divert=i)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check SetWheelMode.divert = {i}")
            # ----------------------------------------------------------------------------------------------------------
            checker = RatchetWheelTestUtils.SetModeStatusResponseChecker
            check_map = checker.get_check_map(self, divert=i)
            checker.check_fields(self, response, self.feature_2130.set_mode_status_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetWheelMode")
            # ----------------------------------------------------------------------------------------------------------
            response = RatchetWheelTestUtils.HIDppHelper.get_wheel_mode(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check GetWheelMode.divert = {i}")
            # ----------------------------------------------------------------------------------------------------------
            checker = RatchetWheelTestUtils.GetWheelModeResponseChecker
            check_map = checker.get_check_map(self, divert=i)
            checker.check_fields(self, response, self.feature_2130.get_wheel_mode_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_2130_0001", _AUTHOR)
    # end def test_set_wheel_mode

    @features("Feature2130")
    @level("Functionality")
    @services("MainWheel")
    def test_check_delta_v_limit_scroll_up(self):
        """
        Validate delta V upper limit of Ratchet wheel using main wheel emulator
        """
        raise NotImplementedError('To be implemented when @services("MainWheel") is available')
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setWheelMode request with divert = 1")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getWheelMode request")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check divert is HID++ Divert Mode (1)")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over some interesting ratchet values in [1, 2, 4, 8, 16, 32, 64, 127]")
        # --------------------------------------------------------------------------------------------------------------
        for _ in []:  # TODO: fill this condition
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set Emulator wheel to Scroll UP and speed to maximum")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check all events with wheelMovement.deltaV>=0x01 and wheelMovement.deltaV<=0x7F"
                                      "and not(wheelMovement.deltaV >=0x80)")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setWheelMode request with divert = 0")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getWheelMode request")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check divert is HID mode (0)")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_2130_0002", _AUTHOR)
    # end def test_check_delta_v_limit_scroll_up

    @features("Feature2130")
    @level("Functionality")
    @services("MainWheel")
    def test_check_delta_v_limit_scroll_down(self):
        """
        Validate delta V lower limit of Ratchet wheel using main wheel emulator
        """
        raise NotImplementedError('To be implemented when @services("MainWheel") is available')
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setWheelMode request with divert = 1")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getWheelMode request")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check divert is HID++ Divert Mode (1)")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over some interesting ratchet values in [ 0xFF, 0xFE, 0xFC, 0xF8, 0xF0,"
                                 "0xE0, 0xC0, 0x81]")
        # --------------------------------------------------------------------------------------------------------------
        for _ in []:  # TODO: fill this condition
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set Emulator wheel to Scroll DOWN and speed to maximum.")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check all events with wheelMovement.deltaV>=0x81 and wheelMovement.deltaV"
                                      "<=0xFF and not(wheelMovement.deltaV <=0x80)")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setWheelMode request with divert = 0")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getWheelMode request")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check divert is HID mode (0)")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_2130_0003", _AUTHOR)
    # end def test_check_delta_v_limit_scroll_down
# end class RatchetWheelFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
