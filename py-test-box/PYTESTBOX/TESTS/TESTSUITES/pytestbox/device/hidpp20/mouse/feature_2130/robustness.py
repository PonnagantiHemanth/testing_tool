#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.mouse.feature_2130.robustness
:brief: HID++ 2.0 ``RatchetWheel`` robustness test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/12/01
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.mouse.ratchetwheel import RatchetWheel
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.ratchetwheelutils import RatchetWheelTestUtils
from pytestbox.device.hidpp20.mouse.feature_2130.ratchetwheel import RatchetWheelTestCase

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
class RatchetWheelRobustnessTestCase(RatchetWheelTestCase):
    """
    Validate ``RatchetWheel`` robustness test cases
    """

    @features("Feature2130")
    @level("Robustness")
    def test_get_wheel_mode_software_id(self):
        """
        Validate ``GetWheelMode`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        divert = RatchetWheel.DIVERT.HID
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(RatchetWheel.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetWheelMode request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_2130.get_wheel_mode_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2130_index)
            report.software_id = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2130.get_wheel_mode_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetWheelModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = RatchetWheelTestUtils.GetWheelModeResponseChecker
            check_map = checker.get_check_map(self, divert=divert)
            checker.check_fields(self, response, self.feature_2130.get_wheel_mode_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2130_0001#1", _AUTHOR)
    # end def test_get_wheel_mode_software_id

    @features("Feature2130")
    @level("Robustness")
    def test_set_mode_status_software_id(self):
        """
        Validate ``SetModeStatus`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.Flag.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """

        divert = RatchetWheel.DIVERT.HID
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(RatchetWheel.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetModeStatus request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_2130.set_mode_status_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2130_index,
                divert=divert)
            report.software_id = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2130.set_mode_status_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetModeStatusResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = RatchetWheelTestUtils.SetModeStatusResponseChecker
            check_map = checker.get_check_map(self, divert=divert)
            checker.check_fields(self, response, self.feature_2130.set_mode_status_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2130_0001#2", _AUTHOR)
    # end def test_set_mode_status_software_id

    @features("Feature2130")
    @level("Robustness")
    def test_get_wheel_mode_padding(self):
        """
        Validate ``GetWheelMode`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        divert = RatchetWheel.DIVERT.HID
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_2130.get_wheel_mode_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetWheelMode request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2130_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2130.get_wheel_mode_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetWheelModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = RatchetWheelTestUtils.SetModeStatusResponseChecker
            check_map = checker.get_check_map(self, divert=divert)
            checker.check_fields(self, response, self.feature_2130.get_wheel_mode_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2130_0002#1", _AUTHOR)
    # end def test_get_wheel_mode_padding

    @features("Feature2130")
    @level("Robustness")
    def test_set_mode_status_padding(self):
        """
        Validate ``SetModeStatus`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.Flag.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        divert = RatchetWheel.DIVERT.HID
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_2130.set_mode_status_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetModeStatus request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_2130_index,
                divert=divert)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=self.feature_2130.set_mode_status_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetModeStatusResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = RatchetWheelTestUtils.SetModeStatusResponseChecker
            check_map = checker.get_check_map(self, divert=divert)
            checker.check_fields(self, response, self.feature_2130.set_mode_status_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2130_0002#2", _AUTHOR)
    # end def test_set_mode_status_padding

    @features("Feature2130")
    @level("Robustness")
    @services("MainWheel")
    def test_set_wheel_mode_delta_value(self):
        """
        Verify delta value returned by firmware is not equal to 0x80

          [0] GetWheelMode() -> divert
          [1] SetWheelMode(divert) -> divert
        """
        raise NotImplementedError('To be implemented when @services("MainWheel") is available')
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setWheelMode request with divert = 0")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify the setWheelMode Response fields")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getWheelMode request")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check getWheelMode response, divert is HID mode (0)")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over various wheel movement LEFT/RIGHT/UP/DOWN")
        # --------------------------------------------------------------------------------------------------------------
        for _ in []:  # TODO: fill this condition
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Use Kosmos to set the roller movement to max speed")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check wheelMovement event received")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check deltaH value is not equal to 0x80")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check deltaV value is not equal to 0x80")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_2130_0003", _AUTHOR)
    # end def test_set_wheel_mode_delta_value
# end class RatchetWheelRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
