#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.touchpad.feature_6100.interface
:brief: HID++ 2.0 ``TouchpadRawXY`` interface test suite
:author: Masan Xu <mxu11@logitech.com>
:date: 2022/05/11
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.touchpad.touchpadrawxy import ReportBitmap
from pyhid.hidpp.features.touchpad.touchpadrawxy import SetGesturesHandlingOutput
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.touchpadrawxyutils import TouchpadRawXYTestUtils
from pytestbox.device.hidpp20.touchpad.feature_6100.touchpadrawxy import TouchpadRawXYTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Masan Xu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TouchpadRawXYInterfaceTestCase(TouchpadRawXYTestCase):
    """
    Validate ``TouchpadRawXY`` interface test cases
    """

    @features("Feature6100")
    @level("Interface")
    def test_get_touchpad_info_interface(self):
        """
        Validate ``GetTouchpadInfo`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetTouchpadInfo request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_6100.get_touchpad_info_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_6100_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.TOUCHPAD,
            response_class_type=self.feature_6100.get_touchpad_info_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetTouchpadInfoResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = TouchpadRawXYTestUtils.GetTouchpadInfoResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
        })
        checker.check_fields(self, response, self.feature_6100.get_touchpad_info_response_cls, check_map)

        self.testCaseChecked("INT_6100_0001", _AUTHOR)
    # end def test_get_touchpad_info_interface

    @features("Feature6100")
    @level("Interface")
    def test_get_raw_report_state_interface(self):
        """
        Validate ``GetRawReportState`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetRawReportState request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_6100.get_raw_report_state_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_6100_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.TOUCHPAD,
            response_class_type=self.feature_6100.get_raw_report_state_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetRawReportStateResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = TouchpadRawXYTestUtils.GetRawReportStateResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
        })
        checker.check_fields(self, response, self.feature_6100.get_raw_report_state_response_cls, check_map)

        self.testCaseChecked("INT_6100_0002", _AUTHOR)
    # end def test_get_raw_report_state_interface

    @features("Feature6100")
    @level("Interface")
    def test_set_raw_report_state_interface(self):
        """
        Validate ``SetRawReportState`` interface
        """
        self.post_requisite_reload_nvs = True
        width_height_bytes = ReportBitmap.STATE.DISABLED
        major_minor = ReportBitmap.STATE.DISABLED
        native_gesture = ReportBitmap.STATE.DISABLED
        width_height = ReportBitmap.STATE.DISABLED
        enhanced = ReportBitmap.STATE.DISABLED
        force_data = ReportBitmap.STATE.DISABLED
        raw = ReportBitmap.STATE.DISABLED
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetRawReportState request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_6100.set_raw_report_state_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_6100_index,
            width_height_bytes = width_height_bytes,
            major_minor = major_minor,
            native_gesture = native_gesture,
            width_height = width_height,
            enhanced = enhanced,
            force_data = force_data,
            raw = raw)

        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.TOUCHPAD,
            response_class_type=self.feature_6100.set_raw_report_state_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetRawReportStateResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
        }
        checker.check_fields(self, response, self.feature_6100.set_raw_report_state_response_cls, check_map)

        self.testCaseChecked("INT_6100_0003", _AUTHOR)
    # end def test_set_raw_report_state_interface

    @features("Feature6100")
    @level("Interface")
    def test_get_gestures_handling_output_interface(self):
        """
        Validate ``GetGesturesHandlingOutput`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetGesturesHandlingOutput request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_6100.get_gestures_handling_output_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_6100_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.TOUCHPAD,
            response_class_type=self.feature_6100.get_gestures_handling_output_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetGesturesHandlingOutputResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = TouchpadRawXYTestUtils.GetGesturesHandlingOutputResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
        })
        checker.check_fields(self, response, self.feature_6100.get_gestures_handling_output_response_cls, check_map)

        self.testCaseChecked("INT_6100_0004", _AUTHOR)
    # end def test_get_gestures_handling_output_interface

    @features("Feature6100")
    @level("Interface")
    def test_set_gestures_handling_output_interface(self):
        """
        Validate ``SetGesturesHandlingOutput`` interface
        """
        self.post_requisite_reload_nvs = True

        # Default GestureHandlingOutput
        one_finger_click = SetGesturesHandlingOutput.HandlingOutput.SUPPORTED_AND_HID
        one_finger_tap = SetGesturesHandlingOutput.HandlingOutput.SUPPORTED_AND_HID
        one_finger_move = SetGesturesHandlingOutput.HandlingOutput.SUPPORTED_AND_HID
        not_defined_gestures = SetGesturesHandlingOutput.HandlingOutput.NOT_ALLOWED_0
        one_finger_click_hold_and_other_fingers_moves = SetGesturesHandlingOutput.HandlingOutput.SUPPORTED_AND_HID
        one_finger_click_hold_and_move = SetGesturesHandlingOutput.HandlingOutput.SUPPORTED_AND_HID
        one_finger_double_click = SetGesturesHandlingOutput.HandlingOutput.SUPPORTED_AND_HID
        one_finger_double_tap = SetGesturesHandlingOutput.HandlingOutput.SUPPORTED_AND_HID
        two_fingers_tap = SetGesturesHandlingOutput.HandlingOutput.NOT_ALLOWED_3
        one_finger_double_tap_not_release_the_2nd_tap = SetGesturesHandlingOutput.HandlingOutput.SUPPORTED_AND_HID
        one_finger_on_the_left_corner = SetGesturesHandlingOutput.HandlingOutput.SUPPORTED_BUT_NO_HID
        one_finger_on_the_right_corner = SetGesturesHandlingOutput.HandlingOutput.SUPPORTED_BUT_NO_HID
        three_fingers_tap_and_drag = SetGesturesHandlingOutput.HandlingOutput.NOT_ALLOWED_0
        two_fingers_slide_left_right = SetGesturesHandlingOutput.HandlingOutput.NOT_ALLOWED_3
        two_fingers_scroll_up_down = SetGesturesHandlingOutput.HandlingOutput.NOT_ALLOWED_3
        two_fingers_click = SetGesturesHandlingOutput.HandlingOutput.NOT_ALLOWED_3
        three_fingers_swipe = SetGesturesHandlingOutput.HandlingOutput.NOT_ALLOWED_0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetGesturesHandlingOutput request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_6100.set_gestures_handling_output_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_6100_index,
            one_finger_click=one_finger_click,
            one_finger_tap=one_finger_tap,
            one_finger_move=one_finger_move,
            not_defined_gestures=not_defined_gestures,
            one_finger_click_hold_and_other_fingers_moves=one_finger_click_hold_and_other_fingers_moves,
            one_finger_click_hold_and_move=one_finger_click_hold_and_move,
            one_finger_double_click=one_finger_double_click,
            one_finger_double_tap=one_finger_double_tap,
            two_fingers_tap=two_fingers_tap,
            one_finger_double_tap_not_release_the_2nd_tap=one_finger_double_tap_not_release_the_2nd_tap,
            one_finger_on_the_left_corner=one_finger_on_the_left_corner,
            one_finger_on_the_right_corner=one_finger_on_the_right_corner,
            three_fingers_tap_and_drag=three_fingers_tap_and_drag,
            two_fingers_slide_left_right=two_fingers_slide_left_right,
            two_fingers_scroll_up_down=two_fingers_scroll_up_down,
            two_fingers_click=two_fingers_click,
            three_fingers_swipe=three_fingers_swipe)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.TOUCHPAD,
            response_class_type=self.feature_6100.set_gestures_handling_output_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetGesturesHandlingOutputResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
        }
        checker.check_fields(self, response, self.feature_6100.set_gestures_handling_output_response_cls, check_map)

        self.testCaseChecked("INT_6100_0005", _AUTHOR)
    # end def test_set_gestures_handling_output_interface
# end class TouchpadRawXYInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
