#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.vlp.common.feature_19a1.business
:brief: VLP 1.0 ``ContextualDisplay`` business test suite
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/12/14
"""

# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from os.path import join
from random import sample
from time import sleep
from time import time
from unittest import skip

from pyharness.core import TestException
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.vlp.features.common.contextualdisplay import ContextualDisplay
from pyhid.vlp.features.common.contextualdisplay import ImageFormat
from pyhid.vlp.features.common.contextualdisplay import SetImageResponse
from pysetup import TESTS_PATH
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.brightnesscontrolutils import BrightnessControlTestUtils
from pytestbox.device.base.keepaliveutils import KeepAliveTestUtils
from pytestbox.device.vlp.base.contextualdisplayutils import ContextualDisplayTestUtils
from pytestbox.device.vlp.common.feature_19a1.contextualdisplay import ContextualDisplayTestCase
from pytestbox.shared.base.dfucontrolutils import DfuControlTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vinodh Selvaraj"
_CHECK_EVENT = "Check keepAliveTimeout Event response field"
_DEVICE_STATE_EVENT_CHECK = "The Device State parameter differs from the one expected"
_DISPLAY_INDEX_CHECK = "The Display Index parameter differs from the one expected"
_ENABLE_DFU = "Send Enable DFU"
_END_TEST_LOOP = "End Test Loop"
_BUTTON_INDEX_CHECK = "The Button Index parameter differs from the one expected"
_SEND_GET_DEVICE_STATE = "Send GetDeviceState request"
_VALIDATE_RESPONSE = "Check response fields"
_VALIDATE_DEVICE_STATE = "Verify device state event is received with the selected device state"

BUTTON_MAP = {
    1: KEY_ID.BUTTON_1,
    2: KEY_ID.BUTTON_2,
    3: KEY_ID.BUTTON_3,
    4: KEY_ID.BUTTON_4,
    5: KEY_ID.BUTTON_5,
    6: KEY_ID.BUTTON_6,
    7: KEY_ID.BUTTON_7,
    8: KEY_ID.BUTTON_8,
    9: KEY_ID.BUTTON_9
}


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class ContextualDisplayBusinessTestCase(ContextualDisplayTestCase):
    """
   Validate ``ContextualDisplay`` business test cases
   """

    @features("Feature19A1")
    @features("Feature19A1Capability", (ContextualDisplay.Capabilities.RGB_888, ContextualDisplay.Capabilities.RGB_565,
                                        ContextualDisplay.Capabilities.JPEG), 2)
    @level("Business")
    def test_set_image_set_multiple_formats(self):
        """
        Validate user is able to set image in one format and switch to another image of a different format.
        """
        image_count = 1
        result_code = int(SetImageResponse.DISPLAY_UPDATED)
        with open(join(TESTS_PATH, "IMAGE_FILES", "image.jpg"), "rb") as f:
            image = f.read()
            image_payload = HexList(bytearray(image))
        # end with

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Loop over supported display index")
        # --------------------------------------------------------------------------------------------------------------
        for d_index in range(self.config.F_DeviceScreenCount):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Pick any 3 Indexes within 0..button_count")
            # ----------------------------------------------------------------------------------------------------------
            buttons = sample(list(range(int(self.config.DISPLAY_INFO_TABLE.F_ButtonCount[d_index]))), 3)

            if self.jpeg_capability:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Send Set Image with display_index={d_index} a JPEG Image " +
                         f"and button location/height/width as per the config of {buttons[0]}")
                # ------------------------------------------------------------------------------------------------------
                self.set_image_and_validate(result_code=result_code,
                                            image_count=image_count,
                                            buttons=buttons[0],
                                            image_format=ImageFormat.JPEG,
                                            image_payload=image_payload)
            # end if

            if self.rgb_565_capability:
                image_payload = HexList(self.color_code[ImageFormat.RGB_565] *
                                        int(self.config.BUTTON_TABLE.F_ButtonLocationWidth[buttons[1]], 16) *
                                        int(self.config.BUTTON_TABLE.F_ButtonLocationHeight[buttons[1]], 16))
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send Set Image with display_index=selected index and RGB565 image "
                                         "and button location/height/width as per the config of button_index_2")
                # ------------------------------------------------------------------------------------------------------
                self.set_image_and_validate(
                    image_format=ImageFormat.RGB_565,
                    x_res=int(self.config.BUTTON_TABLE.F_ButtonLocationWidth[buttons[1]], 16),
                    y_res=int(self.config.BUTTON_TABLE.F_ButtonLocationHeight[buttons[1]], 16),
                    buttons=buttons[1],
                    result_code=result_code,
                    image_count=image_count)
            # end if

            if self.rgb_888_capability:
                image_payload = HexList(self.color_code[ImageFormat.RGB_888] *
                                        int(self.config.BUTTON_TABLE.F_ButtonLocationWidth[buttons[2]], 16) *
                                        int(self.config.BUTTON_TABLE.F_ButtonLocationHeight[buttons[2]], 16))
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send Set image with display_index=selected index and RGB888 image "
                                         "and button location/height/width as per the config of button_index_3")
                # ------------------------------------------------------------------------------------------------------
                self.set_image_and_validate(
                    image_format=ImageFormat.RGB_888,
                    x_res=int(self.config.BUTTON_TABLE.F_ButtonLocationWidth[buttons[2]], 16),
                    y_res=int(self.config.BUTTON_TABLE.F_ButtonLocationHeight[buttons[2]], 16),
                    buttons=buttons[2],
                    result_code=result_code,
                    image_count=image_count)
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_19A1_0001", _AUTHOR)
    # end def test_set_image_set_multiple_formats

    @features("Feature19A1")
    @level("Business")
    @skip("ELF Helper to be implemented")
    def test_set_image_defer_update(self):
        """
        Check image is not displayed when the defer display flag is enabled and displayed in the next packet when the
        flag is disabled.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send set image with defer display update = 1 and imageData=valid/good image")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read Transfer Buffer")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify the image is not updated")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the device state = A0 via getDevice state.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send set image with defer display update = 0 and imageData=valid/good image")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read Transfer Buffer")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify the image is updated")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the device state = A0 via getDevice state.")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_19A1_0002", _AUTHOR)
    # end def test_set_image_defer_update

    @features("Feature19A1")
    @features("BootloaderAvailable")
    @level("Business")
    def test_set_image_defer_update(self):
        """
        Check Device state is DFU confirmation after Enable DFU
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _ENABLE_DFU)
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.set_dfu_control(test_case=self, enter_dfu=1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_GET_DEVICE_STATE)
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.get_device_state(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _VALIDATE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.GetDeviceStateResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_state": (checker.check_device_state, ContextualDisplay.DeviceState.DFU_SCREEN_A6)
        })
        checker.check_fields(self, response, self.feature_19a1.get_device_state_response_cls, check_map)

        self.testCaseChecked("BUS_19A1_0003", _AUTHOR)
    # end def test_set_image_defer_update

    @features("Feature19A1")
    @features("Feature8040")
    @level("Business")
    def test_set_device_state_brightness_8040(self):
        """
        Verify Set device state does not affect the brightness level set via 8040
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get Feature 0x8040 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_8040_index, self.feature_8040, _, _ = BrightnessControlTestUtils.HIDppHelper.get_parameters(
            test_case=self)
        self.feature_8040_config = self.f.PRODUCT.FEATURES.GAMING.BRIGHTNESS_CONTROL

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set brightness to minimum level above 0")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.set_brightness(
            test_case=self,
            brightness=int(self.feature_8040_config.F_PreDefineBrightnessLevels[1]))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _VALIDATE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = BrightnessControlTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8040_index))
        }
        checker.check_fields(self, response, self.feature_8040.set_brightness_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set Device State = 0xA0.")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.set_device_state(
            test_case=self,
            device_state= ContextualDisplay.DeviceState.STREAMING_A0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _VALIDATE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.SetDeviceStateResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_state": (checker.check_device_state,
                             HexList(ContextualDisplay.DeviceState.STREAMING_A0))
        })
        checker.check_fields(self, response, self.feature_19a1.set_device_state_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get current brightness")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_brightness(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check brightness is at the same level.")
        # --------------------------------------------------------------------------------------------------------------
        checker = BrightnessControlTestUtils.GetBrightnessResponseChecker
        check_map = checker.get_check_map(brightness=int(self.feature_8040_config.F_PreDefineBrightnessLevels[1]))
        checker.check_fields(test_case=self, message=response,
                             expected_cls=self.feature_8040.get_brightness_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set Device State = 0xA1.")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.set_device_state(
            test_case=self,
            device_state=ContextualDisplay.DeviceState.STANDBY_ANIM_A1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _VALIDATE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.SetDeviceStateResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_state": (checker.check_device_state,
                             HexList(ContextualDisplay.DeviceState.STANDBY_ANIM_A1))
        })
        checker.check_fields(self, response, self.feature_19a1.set_device_state_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get current brightness")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_brightness(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check brightness is at the same level.")
        # --------------------------------------------------------------------------------------------------------------
        checker = BrightnessControlTestUtils.GetBrightnessResponseChecker
        check_map = checker.get_check_map(brightness=int(self.feature_8040_config.F_PreDefineBrightnessLevels[1]))
        checker.check_fields(test_case=self, message=response,
                             expected_cls=self.feature_8040.get_brightness_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set brightness to maximum level.")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.set_brightness(
            test_case=self,
            brightness=int(self.feature_8040_config.F_MaxBrightness))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _VALIDATE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = BrightnessControlTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8040_index))
        }
        checker.check_fields(self, response, self.feature_8040.set_brightness_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set Device State = 0xA0.")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.set_device_state(
            test_case=self,
            device_state=ContextualDisplay.DeviceState.STREAMING_A0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _VALIDATE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.SetDeviceStateResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_state": (checker.check_device_state,
                             HexList(ContextualDisplay.DeviceState.STREAMING_A0))
        })
        checker.check_fields(self, response, self.feature_19a1.set_device_state_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get current brightness")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_brightness(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check brightness is at maximum level")
        # --------------------------------------------------------------------------------------------------------------
        checker = BrightnessControlTestUtils.GetBrightnessResponseChecker
        check_map = checker.get_check_map(brightness=self.feature_8040_config.F_MaxBrightness)
        checker.check_fields(test_case=self, message=response,
                             expected_cls=self.feature_8040.get_brightness_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set Device State = 0xA1.")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.set_device_state(
            test_case=self,
            device_state=ContextualDisplay.DeviceState.STANDBY_ANIM_A1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _VALIDATE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.SetDeviceStateResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_state": (checker.check_device_state,
                             HexList(ContextualDisplay.DeviceState.STANDBY_ANIM_A1))
        })
        checker.check_fields(self, response, self.feature_19a1.set_device_state_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get current brightness")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_brightness(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check brightness is at maximum level")
        # --------------------------------------------------------------------------------------------------------------
        checker = BrightnessControlTestUtils.GetBrightnessResponseChecker
        check_map = checker.get_check_map(brightness=self.feature_8040_config.F_MaxBrightness)
        checker.check_fields(test_case=self, message=response,
                             expected_cls=self.feature_8040.get_brightness_response_cls, check_map=check_map)

        self.testCaseChecked("BUS_19A1_0004", _AUTHOR)
    # end def test_set_device_state_brightness_8040

    @features("Feature19A1")
    @level("Business")
    def test_all_button_events(self):
        """
        Verify Button Event received in correct order for all keys
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all available buttons.")
        # --------------------------------------------------------------------------------------------------------------
        for d_index in range(1, self.config.F_DeviceScreenCount + 1):
            for button in range(1, int(self.config.DISPLAY_INFO_TABLE.F_ButtonCount[d_index - 1]) + 1):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Press the selected button {BUTTON_MAP[button]}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_press(key_id=BUTTON_MAP[button])

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Check make button event is received for the selected button index at the " +
                                   "end of the payload")
                # ------------------------------------------------------------------------------------------------------
                make_button_event = ContextualDisplayTestUtils.HIDppHelper.button_event(test_case=self)

                self.assertEqual(expected=HexList(d_index),
                                 obtained=make_button_event.display_index,
                                 msg=_DISPLAY_INDEX_CHECK)
                self.assertEqual(expected=HexList(button),
                                 obtained=make_button_event.__getattr__(f"button_index_{button - 1}").button_index,
                                 msg=_BUTTON_INDEX_CHECK)
                self.assertEqual(expected=HexList(0),
                                 obtained=make_button_event.__getattr__(f"button_index_{button}").button_index,
                                 msg=_BUTTON_INDEX_CHECK)
            # end for
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all available buttons.")
        # --------------------------------------------------------------------------------------------------------------
        for d_index in range(1, self.config.F_DeviceScreenCount + 1):
            for button in range(1, int(self.config.DISPLAY_INFO_TABLE.F_ButtonCount[d_index - 1]) + 1):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Press the selected button {BUTTON_MAP[button]}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_release(key_id=BUTTON_MAP[button])

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self,
                                   "check break Button Event is received without the index of the button released.")
                # ------------------------------------------------------------------------------------------------------
                break_button_event = ContextualDisplayTestUtils.HIDppHelper.button_event(test_case=self)

                self.assertEqual(expected=HexList(d_index),
                                 obtained=break_button_event.display_index,
                                 msg=_DISPLAY_INDEX_CHECK)
                # check button index 0 byte has data of button 2 instead of button 1 or 00 if all buttons are released
                button_index_data = 0 if button == int(self.config.DISPLAY_INFO_TABLE.F_ButtonCount[d_index - 1]) \
                    else button + 1
                self.assertEqual(expected=HexList(button_index_data),
                                 obtained=break_button_event.__getattr__("button_index_0").button_index,
                                 msg=_BUTTON_INDEX_CHECK)
            # end for
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check No other event is received")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       class_type=self.feature_19a1.button_event_cls,
                                       queue_name=HIDDispatcher.QueueName.VLP_EVENT)

        self.testCaseChecked("BUS_19A1_0005", _AUTHOR)
    # end def test_all_button_events

    @features("Feature19A1")
    @level("Business")
    def test_all_supported_device_states(self):
        """
        Verify all supported device states
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all SW supported device states.")
        # --------------------------------------------------------------------------------------------------------------
        for device_state in HexList(self.config.F_SetDeviceStates):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Send SetDeviceState with selected state.")
            # ----------------------------------------------------------------------------------------------------------
            response = ContextualDisplayTestUtils.HIDppHelper.set_device_state(
                test_case=self,
                device_state=device_state)

            checker = ContextualDisplayTestUtils.SetDeviceStateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "device_state": (checker.check_device_state, device_state)
            })
            checker.check_fields(self, response, self.feature_19a1.set_device_state_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Check the device state event returned is same as input.")
            # ----------------------------------------------------------------------------------------------------------
            device_state_event = ContextualDisplayTestUtils.HIDppHelper.device_state_event(test_case=self)

            self.assertEqual(expected=HexList(device_state),
                             obtained=device_state_event.device_state,
                             msg=_DEVICE_STATE_EVENT_CHECK)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Send GetDeviceState")
            # ----------------------------------------------------------------------------------------------------------
            response = ContextualDisplayTestUtils.HIDppHelper.get_device_state(test_case=self)

            # -----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Validate GetDeviceState state is same as input.")
            # ----------------------------------------------------------------------------------------------------------
            checker = ContextualDisplayTestUtils.GetDeviceStateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "device_state": (checker.check_device_state, device_state)
            })
            checker.check_fields(self, response, self.feature_19a1.get_device_state_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_19A1_0006", _AUTHOR)
    # end def test_all_supported_device_states

    @features("Feature19A1")
    @level("Business")
    def test_device_state_transition_adopted(self):
        """
        Check device state transition behaviour when deviceAdopted
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Set config with deviceAdopted=1")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.set_config(test_case=self, device_adopted=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate SetConfig Response fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.SetConfigResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_adopted": (checker.check_device_adopted, True)
        })
        checker.check_fields(self, response, self.feature_19a1.set_config_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset the device")
        # --------------------------------------------------------------------------------------------------------------
        self.usb_unplug_and_replug(wait_end_of_state_transition=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check splash screen device state")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.get_device_state(test_case=self)
        self.assertEqual(expected=ContextualDisplay.DeviceState.SPLASH_ANIM_A4,
                         obtained=response.device_state,
                         msg=_DEVICE_STATE_EVENT_CHECK)

        device_state_event = None
        try:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check splash screen deviceStateEvent received")
            # ----------------------------------------------------------------------------------------------------------
            device_state_event = ContextualDisplayTestUtils.HIDppHelper.device_state_event(
                test_case=self, timeout=self.splash_animation_duration)
            self.assertEqual(expected=ContextualDisplay.DeviceState.SPLASH_ANIM_A4,
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
        self.assertEqual(expected=ContextualDisplay.DeviceState.STANDBY_ANIM_A2,
                         obtained=device_state_event.device_state,
                         msg=_DEVICE_STATE_EVENT_CHECK)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check standby screen device state")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.get_device_state(test_case=self)
        self.assertEqual(expected=ContextualDisplay.DeviceState.STANDBY_ANIM_A2,
                         obtained=response.device_state,
                         msg=_DEVICE_STATE_EVENT_CHECK)

        self.testCaseChecked("BUS_19A1_0007", _AUTHOR)
    # end def test_device_state_transition_adopted

    @features("Feature19A1")
    @level("Business")
    def test_device_state_transition_not_adopted(self):
        """
        Check device state transition behaviour when not deviceAdopted
        """
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
        LogHelper.log_step(self, "Empty VLP Event Queue")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.VLP_EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset the device")
        # --------------------------------------------------------------------------------------------------------------
        self.usb_unplug_and_replug(wait_end_of_state_transition=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check splash screen device state")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.get_device_state(test_case=self)
        self.assertEqual(expected=ContextualDisplay.DeviceState.SPLASH_ANIM_A4,
                         obtained=response.device_state,
                         msg=_DEVICE_STATE_EVENT_CHECK)

        device_state_event = None
        try:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check splash screen deviceStateEvent received")
            # ----------------------------------------------------------------------------------------------------------
            device_state_event = ContextualDisplayTestUtils.HIDppHelper.device_state_event(
                test_case=self, timeout=self.splash_animation_duration)
            self.assertEqual(expected=ContextualDisplay.DeviceState.SPLASH_ANIM_A4,
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
        self.assertEqual(expected=ContextualDisplay.DeviceState.ONBOARDING_ANIM_A5,
                         obtained=device_state_event.device_state,
                         msg=_DEVICE_STATE_EVENT_CHECK)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check onboarding screen device state")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.get_device_state(test_case=self)
        self.assertEqual(expected=ContextualDisplay.DeviceState.ONBOARDING_ANIM_A5,
                         obtained=response.device_state,
                         msg=_DEVICE_STATE_EVENT_CHECK)

        self.testCaseChecked("BUS_19A1_0008", _AUTHOR)
    # end def test_device_state_transition_not_adopted

    @features("Feature19A1")
    @level("Business")
    @skip("Test Framework Currently doesn't support USB suspend")
    def test_device_state_transition_usb_suspend(self):
        """
        Check Device state Transition after USB Suspend.

        Note: Test Framework Currently doesn't support USB suspend.
        """
        self.testCaseChecked("BUS_19A1_0009", _AUTHOR)
    # end def test_device_state_transition_usb_suspend

    @features("Feature19A1")
    @features("Feature8040")
    @level("Business")
    @skip("USB device Current measurement to be implemented")
    def test_device_state_transition_sleep_8040(self):
        """
        Check device state transition during sleep using 0x8040
        """
        self.testCaseChecked("BUS_19A1_0010", _AUTHOR)
    # end def test_device_state_transition_sleep_8040

    @features("Feature19A1")
    @features("BootloaderAvailable")
    @level("Business")
    def test_device_state_transition_after_dfu_timeout(self):
        """
        Check device state transition after DFU Timeout
        """
        default_device_state = ContextualDisplay.DeviceState.ONBOARDING_ANIM_A5

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_GET_DEVICE_STATE)
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.get_device_state(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _VALIDATE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.GetDeviceStateResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_state": (checker.check_device_state, default_device_state)
        })
        checker.check_fields(self, response, self.feature_19a1.get_device_state_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _ENABLE_DFU)
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.set_dfu_control(test_case=self, enter_dfu=1)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Verify device state event is received with the DFU Screen state")
        # ----------------------------------------------------------------------------------------------------------
        device_state_event = ContextualDisplayTestUtils.HIDppHelper.device_state_event(test_case=self)

        self.assertEqual(expected=HexList(ContextualDisplay.DeviceState.DFU_SCREEN_A6),
                         obtained=device_state_event.device_state,
                         msg=_DEVICE_STATE_EVENT_CHECK)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wait for DFU timeout")
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlTimeout)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _VALIDATE_DEVICE_STATE)
        # ----------------------------------------------------------------------------------------------------------
        device_state_event = ContextualDisplayTestUtils.HIDppHelper.device_state_event(test_case=self)

        self.assertEqual(expected=HexList(default_device_state),
                         obtained=device_state_event.device_state,
                         msg=_DEVICE_STATE_EVENT_CHECK)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop Set the device in various states")
        # --------------------------------------------------------------------------------------------------------------
        for device_state in HexList(self.config.F_SetDeviceStates):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetDeviceState request with device_state={device_state}")
            # ----------------------------------------------------------------------------------------------------------
            response = ContextualDisplayTestUtils.HIDppHelper.set_device_state(
                test_case=self,
                device_state=device_state)

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
            LogHelper.log_step(self, "Verify device state event is received for the selected state")
            # ----------------------------------------------------------------------------------------------------------
            device_state_event = ContextualDisplayTestUtils.HIDppHelper.device_state_event(test_case=self)

            self.assertEqual(expected=HexList(Numeral(device_state)),
                             obtained=device_state_event.device_state,
                             msg=_DEVICE_STATE_EVENT_CHECK)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _ENABLE_DFU)
            # ----------------------------------------------------------------------------------------------------------
            DfuControlTestUtils.set_dfu_control(test_case=self, enter_dfu=1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Verify device state event is received with DFU Screen state")
            # ----------------------------------------------------------------------------------------------------------
            device_state_event = ContextualDisplayTestUtils.HIDppHelper.device_state_event(test_case=self)

            self.assertEqual(expected=HexList(ContextualDisplay.DeviceState.DFU_SCREEN_A6),
                             obtained=device_state_event.device_state,
                             msg=_DEVICE_STATE_EVENT_CHECK)

            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Wait for DFU timeout")
            # --------------------------------------------------------------------------------------------------------------
            sleep(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlTimeout)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _VALIDATE_DEVICE_STATE)
            # ----------------------------------------------------------------------------------------------------------
            device_state_event = ContextualDisplayTestUtils.HIDppHelper.device_state_event(test_case=self)

            self.assertEqual(expected=HexList(device_state),
                             obtained=device_state_event.device_state,
                             msg=_DEVICE_STATE_EVENT_CHECK)
        # end for

        self.testCaseChecked("BUS_19A1_0012", _AUTHOR)
    # end def test_device_state_transition_after_dfu_timeout

    @features("Feature0008")
    @features("Feature19A1")
    @level("Business")
    def test_device_state_transition_during_keep_alive(self):
        """
        Check device state transition after Keep alive Timeout
        """
        max_timeout = self.f.PRODUCT.FEATURES.COMMON.KEEP_ALIVE.F_TimeoutMax
        one_millisecond = 1000
        streaming_device_state = ContextualDisplay.DeviceState.STREAMING_A0
        standby_device_state = ContextualDisplay.DeviceState.STANDBY_ANIM_A1

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get Feature index 0x0008")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_0008_index, self.feature_0008, _, _ = KeepAliveTestUtils.HIDppHelper.get_parameters(
            test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setKeepAlive with requestedTimeout = TimeoutMax.")
        # --------------------------------------------------------------------------------------------------------------
        response = KeepAliveTestUtils.HIDppHelper.keep_alive(
            test_case=self,
            requested_timeout=HexList(Numeral(max_timeout)))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _VALIDATE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = KeepAliveTestUtils.KeepAliveResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "final_timeout": (checker.check_final_timeout, HexList(Numeral(max_timeout)))
        })
        checker.check_fields(self, response, self.feature_0008.keep_alive_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Set the device in Streaming State {streaming_device_state}")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.set_device_state(
            test_case=self, device_state=streaming_device_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _VALIDATE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.SetDeviceStateResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_state": (checker.check_device_state, streaming_device_state)
        })
        checker.check_fields(self, response, self.feature_19a1.set_device_state_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_GET_DEVICE_STATE)
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.get_device_state(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _VALIDATE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.GetDeviceStateResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_state": (checker.check_device_state, streaming_device_state)
        })
        checker.check_fields(self, response, self.feature_19a1.get_device_state_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check deviceStateEvent is received with deviceState={streaming_device_state}")
        # --------------------------------------------------------------------------------------------------------------
        device_state_event = ContextualDisplayTestUtils.HIDppHelper.device_state_event(test_case=self)

        self.assertEqual(expected=HexList(streaming_device_state),
                         obtained=device_state_event.device_state,
                         msg=_DEVICE_STATE_EVENT_CHECK)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the keepAliveTimeout Event is received after TimeoutMax.")
        # --------------------------------------------------------------------------------------------------------------
        response = KeepAliveTestUtils.HIDppHelper.keep_alive_timeout_event(
            test_case=self,
            check_first_message=False,
            timeout=round(max_timeout / one_millisecond) + 1)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_EVENT)
        # ----------------------------------------------------------------------------------------------------------
        checker = KeepAliveTestUtils.KeepAliveTimeoutEventChecker
        checker.check_fields(self, response, self.feature_0008.keep_alive_timeout_event_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the deviceStateEvent is received with " +
                            f"deviceState={standby_device_state} after keepalivetimeout.")
        # --------------------------------------------------------------------------------------------------------------
        device_state_event = ContextualDisplayTestUtils.HIDppHelper.device_state_event(test_case=self)

        self.assertEqual(expected=HexList(standby_device_state),
                         obtained=device_state_event.device_state,
                         msg=_DEVICE_STATE_EVENT_CHECK)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_GET_DEVICE_STATE)
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.get_device_state(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _VALIDATE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.GetDeviceStateResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_state": (checker.check_device_state, standby_device_state)
        })
        checker.check_fields(self, response, self.feature_19a1.get_device_state_response_cls, check_map)

        self.testCaseChecked("BUS_19A1_0013", _AUTHOR)
    # end def test_device_state_transition_during_keep_alive
# end class ContextualDisplayBusinessTestCase
