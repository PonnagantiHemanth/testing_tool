#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.vlp.common.feature_19a1.functionality
:brief: VLP 1.0 ``ContextualDisplay`` functionality test suite
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/12/14
"""
import time
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from enum import IntEnum
from os.path import join
from time import sleep

from pyharness.core import TestException
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.vlp.features.common.contextualdisplay import ContextualDisplay
from pyhid.vlp.features.common.contextualdisplay import GetDisplayInfoResponsePayloadMixin
from pyhid.vlp.features.common.contextualdisplay import ImageFormat
from pyhid.vlp.features.common.contextualdisplay import SetImageResponse
from pylibrary.tools.hexlist import HexList
from pysetup import TESTS_PATH
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.displayinfoutils import ButtonInfoConfig
from pytestbox.base.displayinfoutils import DisplayInfoConfig
from pytestbox.base.displayinfoutils import VisibleAreaInfoConfig
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.vlp.base.contextualdisplayutils import ContextualDisplayTestUtils
from pytestbox.device.vlp.common.feature_19a1.contextualdisplay import ContextualDisplayTestCase
from pytestbox.device.vlp.protocol.vlpprotocoltestutils import VlpProtocolTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vinodh Selvaraj"
_DEVICE_STATE_EVENT_CHECK = "The Device State parameter differs from the one expected"
_TEST_LOOP_START = "Test Loop over all available display index"
_TEST_LOOP_END = "End Test Loop"
_HALF_A_SECOND = 0.5


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class ContextualDisplayFunctionalityTestCase(ContextualDisplayTestCase):
    """
   Validate ``ContextualDisplay`` functionality test cases
   """

    def _send_vlp_image_check_response(self, image_count, image_format, image_payload, result_code,
                                       defer_display_update=False):
        """
        Reusable method to send request and verify response set_image processing

        :param image_count: Number of images in payload
        :type image_count: ``int|HexList``
        :param image_format: Format of image
        :type image_format: ``int|HexList``
        :param image_payload: HexList of byte array of the selected image
        :type image_payload: ``HexList``
        :param result_code: Result Code to be validated in the response.
        :type result_code: ``int|HexList``
        :param defer_display_update: Flasg for defer display update
        :type defer_display_update: ``int|bool``
        """
        self.img = image_payload

        payload = ContextualDisplayTestUtils._get_multi_packet_set_image_payload(
            test_case=self, img_count=image_count, image_format=image_format, defer_display_update=defer_display_update)

        responses = VlpProtocolTestUtils.VlpHelper.vlp_transfer(
            test_case=self,
            payload=payload,
            report_payload_size=self.report_payload_size,
            report_type=self.feature_19a1.set_image_cls,
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_19a1_index,
            ack=True,
            start_seqn=0)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetImageResponse fields")
        # ----------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.SetImageResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_19a1_index)),
            "result_code": (checker.check_result_code, result_code),
            "count": (checker.check_count, image_count)
        })
        for response in responses:
            checker.check_fields(self, response, self.feature_19a1.set_image_response_cls, check_map)
        # end for
    # end def _send_vlp_image_check_response

    @features("VLP")
    @features("MultiPacket")
    @features("Feature19A1")
    @features("Feature19A1Capability", (ContextualDisplay.Capabilities.JPEG,))
    @level("Functionality")
    def test_set_image_on_all_displays(self):
        """
        Validate User is able to set image on all available contextual display screens
        """
        image_count = 1
        result_code = int(SetImageResponse.DISPLAY_UPDATED)

        with open(join(TESTS_PATH, "IMAGE_FILES", "image.jpg"), "rb") as f:
            image = f.read()
            image_payload = HexList(bytearray(image))
        # end with

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _TEST_LOOP_START)
        # --------------------------------------------------------------------------------------------------------------

        for display_index in range(self.config.F_DeviceScreenCount):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetImage with displayIdx = {display_index}")
            # ----------------------------------------------------------------------------------------------------------
            self._send_vlp_image_check_response(image_format=ImageFormat.JPEG, image_count=image_count,
                                                image_payload=image_payload, result_code=result_code)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _TEST_LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_19A1_0001", _AUTHOR)
    # end def test_set_image_on_all_displays

    @features("VLP")
    @features("MultiPacket")
    @features("Feature19A1")
    @features("Feature19A1Capability", (ContextualDisplay.Capabilities.JPEG,))
    @level("Functionality")
    def test_set_image_multiple_button_jpeg(self):
        """
        Validate User is able to set JPG format image of varying size to all available screens
        """
        image_count = 1
        result_code = int(SetImageResponse.DISPLAY_UPDATED)

        with open(join(TESTS_PATH, "IMAGE_FILES", "image.jpg"), "rb") as f:
            image = f.read()
            image_payload = HexList(bytearray(image))
        # end with
        with open(join(TESTS_PATH, "IMAGE_FILES", "multi_button_image.jpg"), "rb") as f:
            image = f.read()
            multi_image_payload = HexList(bytearray(image))
        # end with
        with open(join(TESTS_PATH, "IMAGE_FILES", "full_screen_image.jpg"), "rb") as f:
            image = f.read()
            full_image_payload = HexList(bytearray(image))
        # end with

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _TEST_LOOP_START)
        # --------------------------------------------------------------------------------------------------------------
        for display_index in range(self.config.F_DeviceScreenCount):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetImage with displayIdx = {display_index} and format=JPEG(0x00) " +
                               "jpg image with size = single button image")
            # ----------------------------------------------------------------------------------------------------------
            self._send_vlp_image_check_response(image_format=ImageFormat.JPEG, image_count=image_count,
                                                image_payload=image_payload, result_code=result_code)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetImage with displayIdx = {display_index} and format=JPEG(0x00) " +
                               "jpg image with size = multi button image")
            # ----------------------------------------------------------------------------------------------------------
            self._send_vlp_image_check_response(image_format=ImageFormat.JPEG, image_count=image_count,
                                                image_payload=multi_image_payload, result_code=result_code)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetImage with displayIdx = {display_index} and format=JPEG(0x00) " +
                               "jpg image with size = full screen image")
            # ----------------------------------------------------------------------------------------------------------
            self._send_vlp_image_check_response(image_format=ImageFormat.JPEG, image_count=image_count,
                                                image_payload=full_image_payload, result_code=result_code)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _TEST_LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_19A1_0002", _AUTHOR)
    # end def test_set_image_multiple_button_jpeg

    @features("VLP")
    @features("MultiPacket")
    @features("Feature19A1")
    @features("Feature19A1Capability", (ContextualDisplay.Capabilities.RGB_565,))
    @level("Functionality")
    def test_set_image_multiple_button_rgb565(self):
        """
        Validate User is able to set RGB565 format image of varying size to all available screens
        """
        image_count = 1
        result_code = int(SetImageResponse.DISPLAY_UPDATED)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _TEST_LOOP_START)
        # --------------------------------------------------------------------------------------------------------------
        for d_index in range(self.config.F_DeviceScreenCount):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetImage with displayIdx = {d_index} and format=RGB_565(0x01) " +
                               "jpg image with size = single button image")
            # ----------------------------------------------------------------------------------------------------------
            self.set_image_and_validate(
                image_format=ImageFormat.RGB_565,
                x_res=int(self.config.BUTTON_TABLE.F_ButtonLocationWidth[d_index], 16),
                y_res=int(self.config.BUTTON_TABLE.F_ButtonLocationHeight[d_index], 16),
                buttons=[0],
                result_code=result_code,
                image_count=image_count)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetImage with displayIdx = {d_index} and format=RGB_565(0x01) " +
                               "jpg image with size = multi button image")
            # ----------------------------------------------------------------------------------------------------------
            image_count = len(list(range(int(self.config.DISPLAY_INFO_TABLE.F_ButtonCount[d_index])//2)))
            self.set_image_and_validate(
                image_format=ImageFormat.RGB_565,
                x_res=int(self.config.BUTTON_TABLE.F_ButtonLocationWidth[d_index], 16),
                y_res=int(self.config.BUTTON_TABLE.F_ButtonLocationHeight[d_index], 16),
                buttons=list(range(int(self.config.DISPLAY_INFO_TABLE.F_ButtonCount[d_index])//2)),
                result_code=result_code,
                image_count=image_count)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetImage with displayIdx = {d_index} and format=RGB_565(0x01) " +
                               "jpg image with size = full screen image")
            # ----------------------------------------------------------------------------------------------------------
            image_count = len(list(range(int(self.config.DISPLAY_INFO_TABLE.F_ButtonCount[d_index]))))
            self.set_image_and_validate(
                image_format=ImageFormat.RGB_565,
                x_res=int(self.config.BUTTON_TABLE.F_ButtonLocationWidth[d_index], 16)//2,
                y_res=int(self.config.BUTTON_TABLE.F_ButtonLocationHeight[d_index], 16)//2,
                buttons=list(range(int(self.config.DISPLAY_INFO_TABLE.F_ButtonCount[d_index]))),
                result_code=result_code,
                image_count=image_count)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _TEST_LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_19A1_0003", _AUTHOR)
    # end def test_set_image_multiple_button_rgb565

    @features("VLP")
    @features("MultiPacket")
    @features("Feature19A1")
    @features("Feature19A1Capability", (ContextualDisplay.Capabilities.RGB_888,))
    @level("Functionality")
    def test_set_image_multiple_button_rgb888(self):
        """
        Validate User is able to set RGB888 format image of varying size to all available screens
        """
        image_count = 1
        result_code = int(SetImageResponse.DISPLAY_UPDATED)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _TEST_LOOP_START)
        # --------------------------------------------------------------------------------------------------------------
        for d_index in range(self.config.F_DeviceScreenCount):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetImage with displayIdx = {d_index} and format=RGB_888(0x02) " +
                               "jpg image with size = single button image")
            # ----------------------------------------------------------------------------------------------------------
            self.set_image_and_validate(
                image_format=ImageFormat.RGB_888,
                x_res=int(self.config.BUTTON_TABLE.F_ButtonLocationWidth[d_index], 16),
                y_res=int(self.config.BUTTON_TABLE.F_ButtonLocationHeight[d_index], 16),
                buttons=[0],
                result_code=result_code,
                image_count=image_count)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetImage with displayIdx = {d_index} and format=RGB_888(0x02) " +
                               "jpg image with size = multi button image")
            # ----------------------------------------------------------------------------------------------------------
            self.set_image_and_validate(
                image_format=ImageFormat.RGB_888,
                x_res=int(self.config.BUTTON_TABLE.F_ButtonLocationWidth[d_index], 16),
                y_res=int(self.config.BUTTON_TABLE.F_ButtonLocationHeight[d_index], 16),
                buttons=list(range(int(self.config.DISPLAY_INFO_TABLE.F_ButtonCount[d_index]) // 2)),
                result_code=result_code,
                image_count=image_count)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetImage with displayIdx = {d_index} and format=RGB_565(0x02) " +
                               "jpg image with size = full screen image")
            # ----------------------------------------------------------------------------------------------------------
            self.set_image_and_validate(
                image_format=ImageFormat.RGB_888,
                x_res=int(self.config.BUTTON_TABLE.F_ButtonLocationWidth[d_index], 16),
                y_res=int(self.config.BUTTON_TABLE.F_ButtonLocationHeight[d_index], 16),
                buttons=list(range(int(self.config.DISPLAY_INFO_TABLE.F_ButtonCount[d_index]))),
                result_code=result_code,
                image_count=image_count)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _TEST_LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_19A1_0004", _AUTHOR)
    # end def test_set_image_multiple_button_rgb888

    @features("VLP")
    @features("Feature19A1")
    @level("Functionality")
    def test_set_supported_device_states(self):
        """
        Validate all supported device states and verify DeviceStateEvent is received.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all supported device states")
        # --------------------------------------------------------------------------------------------------------------
        for device_state in self.config.F_SetDeviceStates:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetDeviceState request with device_state={device_state}")
            # ----------------------------------------------------------------------------------------------------------
            response = ContextualDisplayTestUtils.HIDppHelper.set_device_state(
                test_case=self,
                device_state=HexList(device_state))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetDeviceStateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ContextualDisplayTestUtils.SetDeviceStateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "device_index": (checker.check_device_index, HexList(self.original_device_index)),
                "feature_index": (checker.check_feature_index, HexList(self.feature_19a1_index)),
                "device_state": (checker.check_device_state, device_state)
            })
            checker.check_fields(self, response, self.feature_19a1.set_device_state_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Sleep to allow time for device state transition to complete")
            # ----------------------------------------------------------------------------------------------------------
            sleep(_HALF_A_SECOND)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetDeviceState request")
            # ----------------------------------------------------------------------------------------------------------
            response = ContextualDisplayTestUtils.HIDppHelper.get_device_state(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetDeviceStateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ContextualDisplayTestUtils.GetDeviceStateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "device_index": (checker.check_device_index, HexList(self.original_device_index)),
                "feature_index": (checker.check_feature_index, HexList(self.feature_19a1_index)),
                "device_state": (checker.check_device_state, device_state)
            })
            checker.check_fields(self, response, self.feature_19a1.get_device_state_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Verify device state event is received with the selected device state")
            # ----------------------------------------------------------------------------------------------------------
            device_state_event = ContextualDisplayTestUtils.HIDppHelper.device_state_event(test_case=self)

            self.assertEqual(expected=HexList(device_state),
                             obtained=device_state_event.device_state,
                             msg=_DEVICE_STATE_EVENT_CHECK)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _TEST_LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_19A1_0005", _AUTHOR)
    # end def test_set_supported_device_states

    @features("VLP")
    @features("MultiPacket")
    @features("Feature19A1")
    @level("Functionality")
    def test_get_display_info(self):
        """
        Validate Display Info for all available displays
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all available display indexes")
        # --------------------------------------------------------------------------------------------------------------
        for display_index in self.config.DISPLAY_INFO_TABLE.F_DisplayIndex[:-1]:
            display_info = DisplayInfoConfig.from_index(
                self.f, int(display_index), self.config_manager).display_info_payload
            display_shape = display_info.display_shape
            display_dimension = display_info.display_dimension
            horizontal_resolution = display_info.horizontal_resolution
            vertical_resolution = display_info.vertical_resolution
            button_count = display_info.button_count
            visible_area_count = display_info.visible_area_count
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetDisplayInfo request")
            # ----------------------------------------------------------------------------------------------------------
            response = ContextualDisplayTestUtils.HIDppHelper.get_display_info(
                test_case=self,
                display_index=int(display_index) + 1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetDisplayInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ContextualDisplayTestUtils.GetDisplayInfoResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "device_index": (checker.check_device_index, HexList(self.original_device_index)),
                "feature_index": (checker.check_feature_index, HexList(self.feature_19a1_index)),
                "display_shape": (checker.check_display_shape, display_shape),
                "display_dimension": (checker.check_display_dimension, display_dimension),
                "horizontal_resolution": (checker.check_horizontal_resolution, horizontal_resolution),
                "vertical_resolution": (checker.check_vertical_resolution, vertical_resolution),
                "button_count": (checker.check_button_count, button_count),
                "visible_area_count": (checker.check_visible_area_count, visible_area_count)})
            button_checker = ContextualDisplayTestUtils.ButtonInfoChecker
            for b_index in range(int(Numeral(button_count))):
                button_info_config = ButtonInfoConfig.from_index(
                    self.f, b_index, self.config_manager).button_info_payload
                button_info = ({
                    "field_name": f"button_info_{b_index}",
                    "button_shape": (button_checker.check_button_shape,
                                     button_info_config.button_shape),
                    "button_location_x": (button_checker.check_button_location_x,
                                          button_info_config.button_location_x),
                    "button_location_y": (button_checker.check_button_location_y,
                                          button_info_config.button_location_y),
                    "button_location_width": (button_checker.check_button_location_width,
                                              button_info_config.button_location_width),
                    "button_location_height": (button_checker.check_button_location_height,
                                               button_info_config.button_location_height)
                })
                check_map.__setitem__(f"button_info_{b_index}", (checker.check_button_info, button_info))
            # end for
            visible_checker = ContextualDisplayTestUtils.VisibleAreaInfoChecker
            for v_index in range(int(Numeral(visible_area_count))):
                visible_area_info_config = VisibleAreaInfoConfig.from_index(
                    self.f, v_index, self.config_manager).visible_area_info_payload
                visible_area_info = ({
                    "field_name": f"visible_area_info_{v_index}",
                    "visible_area_shape": (visible_checker.check_visible_area_shape,
                                           visible_area_info_config.visible_area_shape),
                    "visible_area_location_x": (visible_checker.check_visible_area_location_x,
                                                visible_area_info_config.visible_area_location_x),
                    "visible_area_location_y": (visible_checker.check_visible_area_location_y,
                                                visible_area_info_config.visible_area_location_y),
                    "visible_area_width": (visible_checker.check_visible_area_width,
                                           visible_area_info_config.visible_area_width),
                    "visible_area_height": (visible_checker.check_visible_area_height,
                                            visible_area_info_config.visible_area_height)
                })
                check_map.__setitem__(f"visible_area_info_{v_index}",
                                      (checker.check_visible_area_info, visible_area_info))
            # end for
            checker.check_fields(self, response, GetDisplayInfoResponsePayloadMixin, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _TEST_LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_19A1_0006", _AUTHOR)
    # end def test_get_display_info

    @features("VLP")
    @features("Feature19A1")
    @level("Functionality")
    def test_device_adopted_status(self):
        """
        Validate device adopted status and respective device State
        """
        splash_device_state = ContextualDisplay.DeviceState.SPLASH_ANIM_A4
        device_state_adopted = ContextualDisplay.DeviceState.STANDBY_ANIM_A2
        device_state_not_adopted = ContextualDisplay.DeviceState.ONBOARDING_ANIM_A5

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Set config with deviceAdopted=1")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.set_config(test_case=self, device_adopted=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetConfig Response fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.SetConfigResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_adopted": (checker.check_device_adopted, True)
        })
        checker.check_fields(self, response, self.feature_19a1.set_config_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Get Config")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.get_config(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify response received has deviceAdopted=1")
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.GetConfigResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_adopted": (checker.check_device_adopted, True)
        })
        checker.check_fields(self, response, self.feature_19a1.get_config_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Clear Device State Event messages")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.VLP_EVENT,
            class_type=self.feature_19a1.device_state_event_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset the device")
        # --------------------------------------------------------------------------------------------------------------
        self.usb_unplug_and_replug(wait_end_of_state_transition=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check splash screen device state")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.get_device_state(test_case=self)
        self.assertEqual(expected=HexList(Numeral(splash_device_state)),
                         obtained=response.device_state,
                         msg=_DEVICE_STATE_EVENT_CHECK)

        device_state_event = None
        try:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check splash screen deviceStateEvent received")
            # ----------------------------------------------------------------------------------------------------------
            device_state_event = ContextualDisplayTestUtils.HIDppHelper.device_state_event(
                test_case=self, timeout=self.splash_animation_duration)
            self.assertEqual(expected=HexList(Numeral(splash_device_state)),
                             obtained=device_state_event.device_state,
                             msg=_DEVICE_STATE_EVENT_CHECK)
            device_state_event = ContextualDisplayTestUtils.HIDppHelper.device_state_event(test_case=self)
        except (TestException, AssertionError) as e:
            self.log_warning(message="Splash screen state event was not caught. Please check with USB analyzer",
                             force_console_print=True)
            self.log_warning(f"Test exception reported as warning: {e}")
            if device_state_event is None:
                device_state_event = ContextualDisplayTestUtils.HIDppHelper.device_state_event(test_case=self)
            # end if
        # end try

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check standby screen deviceStateEvent received")
        # ----------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=HexList(Numeral(device_state_adopted)),
                         obtained=device_state_event.device_state,
                         msg=_DEVICE_STATE_EVENT_CHECK)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check standby screen device state")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.get_device_state(test_case=self)
        self.assertEqual(expected=HexList(Numeral(device_state_adopted)),
                         obtained=response.device_state,
                         msg=_DEVICE_STATE_EVENT_CHECK)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Set config with deviceAdopted=0")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.set_config(test_case=self, device_adopted=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate SetConfig Response fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.SetConfigResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_adopted": (checker.check_device_adopted, False)
        })
        checker.check_fields(self, response, self.feature_19a1.set_config_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Get Config")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.get_config(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify response received has deviceAdopted=0")
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.GetConfigResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_adopted": (checker.check_device_adopted, False)
        })
        checker.check_fields(self, response, self.feature_19a1.get_config_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset the device")
        # --------------------------------------------------------------------------------------------------------------
        self.usb_unplug_and_replug(wait_end_of_state_transition=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check splash screen device state")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.get_device_state(test_case=self)
        self.assertEqual(expected=HexList(Numeral(splash_device_state)),
                         obtained=response.device_state,
                         msg=_DEVICE_STATE_EVENT_CHECK)

        device_state_event = None
        try:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check splash screen deviceStateEvent received")
            # ----------------------------------------------------------------------------------------------------------
            device_state_event = ContextualDisplayTestUtils.HIDppHelper.device_state_event(
                test_case=self, timeout=self.splash_animation_duration)
            self.assertEqual(expected=HexList(Numeral(splash_device_state)),
                             obtained=device_state_event.device_state,
                             msg=_DEVICE_STATE_EVENT_CHECK)
            device_state_event = ContextualDisplayTestUtils.HIDppHelper.device_state_event(test_case=self)
        except (TestException, AssertionError) as e:
            self.log_warning(message="Splash screen state event was not caught. Please check with USB analyzer",
                             force_console_print=True)
            self.log_warning(f"Test exception reported as warning: {e}")
            if device_state_event is None:
                device_state_event = ContextualDisplayTestUtils.HIDppHelper.device_state_event(test_case=self)
            # end if
        # end try

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check onboarding screen deviceStateEvent received")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=HexList(Numeral(device_state_not_adopted)),
                         obtained=device_state_event.device_state,
                         msg=_DEVICE_STATE_EVENT_CHECK)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check onboarding screen device state")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.get_device_state(test_case=self)
        self.assertEqual(expected=HexList(Numeral(device_state_not_adopted)),
                         obtained=response.device_state,
                         msg=_DEVICE_STATE_EVENT_CHECK)

        self.testCaseChecked("FUN_19A1_0007", _AUTHOR)
    # end def test_device_adopted_status
# end class ContextualDisplayFunctionalityTestCase
