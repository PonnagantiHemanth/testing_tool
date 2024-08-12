#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.vlp.common.feature_19a1.robustness
:brief: VLP 1.0 ``ContextualDisplay`` robustness test suite
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/12/14
"""

# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from os.path import join
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.configchange import ConfigChange
from pyhid.hidpp.features.configchange import SetConfigurationComplete
from pyhid.hidpp.features.configchange import SetConfigurationCompleteResponse
from pyhid.vlp.features.common.contextualdisplay import ConfigFormat
from pyhid.vlp.features.common.contextualdisplay import ContextualDisplay
from pyhid.vlp.features.common.contextualdisplay import GetDisplayInfoResponsePayloadMixin
from pyhid.vlp.features.common.contextualdisplay import GetDisplayInfo
from pyhid.vlp.features.common.contextualdisplay import ImageFormat
from pyhid.vlp.features.common.contextualdisplay import SetImagePayloadMixin
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_wrong_range
from pysetup import TESTS_PATH
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.displayinfoutils import ButtonInfoConfig
from pytestbox.base.displayinfoutils import DisplayInfoConfig
from pytestbox.base.displayinfoutils import VisibleAreaInfoConfig
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.oobstateutils import OobStateTestUtils
from pytestbox.device.vlp.base.contextualdisplayutils import ContextualDisplayTestUtils
from pytestbox.device.vlp.common.feature_19a1.contextualdisplay import ContextualDisplayTestCase
from pytestbox.device.vlp.protocol.vlpprotocoltestutils import VlpProtocolTestUtils
from pytestbox.shared.base.dfucontrolutils import DfuControlTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vinodh Selvaraj"
_DEVICE_STATE_EVENT_CHECK = "The Device State parameter differs from the one expected"
_CHECK_SET_CONFIG_RESPONSE = "Check SetConfigResponse fields"
_SEND_GET_CONFIG = "Send GetConfig request"
_CHECK_GET_CONFIG_RESPONSE = "Check GetConfigResponse fields"
_LOOP_END = "End Test Loop"
_LOOP_START_RESERVED = "Test loop over reserved range (several interesting values)"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class ContextualDisplayRobustnessTestCase(ContextualDisplayTestCase):
    """
   Validate ``ContextualDisplay`` robustness test cases
   """

    @features("Feature19A1")
    @level("Robustness")
    def test_get_capabilities_software_id(self):
        """
        Validate ``GetCapabilities`` software id field is ignored by the firmware

        [0] getCapabilities() -> deviceScreenCount, maxImageSize, maxImageFps, deviceCapabilities
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ContextualDisplay.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send getCapabilities request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ContextualDisplayTestUtils.HIDppHelper.get_capabilities(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check getCapabilities response fields")
            # ----------------------------------------------------------------------------------------------------------
            ContextualDisplayTestUtils.GetCapabilitiesResponseChecker.check_fields(
                self, response, self.feature_19a1.get_capabilities_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ROB_19A1_0001#1", _AUTHOR)
    # end def test_get_capabilities_software_id

    @features("Feature19A1")
    @level("Robustness")
    def test_get_display_info_software_id(self):
        """
        Validate ``getDisplayInfo`` software id field is ignored by the firmware

        [1] getDisplayInfo(displayIdx) -> displayShape, displayDimension, resHorizontal, resVertical, buttonCount,
        visibleAreaCount, button1, button2 … buttonN, visibleArea1, visibleArea2 … visibleAreaM
        """
        display_index = 1
        display_info = DisplayInfoConfig.from_index(
            self.f, display_index - 1, self.config_manager).display_info_payload
        display_shape = display_info.display_shape
        display_dimension = display_info.display_dimension
        horizontal_resolution = display_info.horizontal_resolution
        vertical_resolution = display_info.vertical_resolution
        button_count = display_info.button_count
        visible_area_count = display_info.visible_area_count

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ContextualDisplay.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send getDisplayInfo request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ContextualDisplayTestUtils.HIDppHelper.get_display_info(
                test_case=self,
                display_index=display_index,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check getDisplayInfo response fields")
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
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ROB_19A1_0001#2", _AUTHOR)
    # end def test_get_display_info_software_id

    @features("Feature19A1")
    @level("Robustness")
    def test_set_image_software_id(self):
        """
        Validate ``setImage`` software id field is ignored by the firmware

        [2] setImage(displayIdx, setImageFlags, imageCount, image1, image2… imageN) -> resultCode, count
        """
        images = []
        display_count = 1

        with open(join(TESTS_PATH, "IMAGE_FILES", "image.jpg"), "rb") as f:
            image = f.read()
            image_payload = HexList(bytearray(image))
            image_size = len(image_payload)
        # end with
        button_info = ButtonInfoConfig.from_index(
            self.f, 0, self.config_manager).button_info_payload

        images.append(ContextualDisplay.Image(image_format=ImageFormat.RGB_565,
                                              image_location_x=button_info.button_location_x,
                                              image_location_y=button_info.button_location_y,
                                              image_location_width=button_info.button_location_width,
                                              image_location_height=button_info.button_location_height,
                                              image_size=image_size,
                                              image_data=image_payload))

        payload = HexList(SetImagePayloadMixin(display_index=GetDisplayInfo.DEFAULT.DISPLAY_INDEX,
                                                defer_display_update=0,
                                                image_count=1,
                                                images=images))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ContextualDisplay.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send setImage request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
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
            LogHelper.log_check(self, "Check setImage response fields")
            # ----------------------------------------------------------------------------------------------------------
            for response in responses:
                checker = ContextualDisplayTestUtils.SetImageResponseChecker
                check_map = checker.get_default_check_map(self)
                check_map.update({
                    "count": (checker.check_count, display_count),
                })
                checker.check_fields(
                    self, response, self.feature_19a1.set_image_response_cls, check_map)
            # end for
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ROB_19A1_0001#3", _AUTHOR)
    # end def test_set_image_software_id

    @features("Feature19A1")
    @level("Robustness")
    def test_get_supported_device_states_software_id(self):
        """
        Validate ``getSupportedDeviceStates`` software id field is ignored by the firmware

        [3] getSupportedDeviceStates() -> deviceState1, deviceState2…deviceStateN
        """

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ContextualDisplay.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send getSupportedDeviceStates request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ContextualDisplayTestUtils.HIDppHelper.get_supported_device_states(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check getSupportedDeviceStates response fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ContextualDisplayTestUtils.GetSupportedDeviceStatesResponseChecker
            check_map = checker.get_default_check_map(self)
            for d_index in range(len(self.config.F_SupportedDeviceStates)):
                device_state_info = ({
                    "field_name": f"device_state_{d_index}",
                    "device_state": (checker.check_device_state, self.config.F_SupportedDeviceStates[d_index])
                })
                check_map.__setitem__(f"device_state_{d_index}",
                                      (checker.check_device_state_info, device_state_info))
            # end for
            checker.check_fields(self, response, self.feature_19a1.get_supported_device_states_response_cls, check_map)
            # end for
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ROB_19A1_0001#4", _AUTHOR)
    # end def test_get_supported_device_states_software_id

    @features("Feature19A1")
    @level("Robustness")
    def test_set_device_state_software_id(self):
        """
        Validate ``setDeviceState`` software id field is ignored by the firmware

        [4] setDeviceState(deviceState) -> deviceState
        """
        device_state = ContextualDisplay.DeviceState.STANDBY_ANIM_A1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ContextualDisplay.DEFAULT.SOFTWARE_ID)[1:]:
            # Alternate between device states A0 and A1 as per state machine design
            device_state = ContextualDisplay.DeviceState.STREAMING_A0 \
                if device_state == ContextualDisplay.DeviceState.STANDBY_ANIM_A1 \
                else ContextualDisplay.DeviceState.STANDBY_ANIM_A1
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send setDeviceState request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ContextualDisplayTestUtils.HIDppHelper.set_device_state(
                test_case=self,
                device_state=device_state,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check setDeviceState response fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ContextualDisplayTestUtils.SetDeviceStateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "device_state": (checker.check_device_state, device_state)
            })
            checker.check_fields(self, response, self.feature_19a1.set_device_state_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ROB_19A1_0001#5", _AUTHOR)
    # end def test_set_device_state_software_id

    @features("Feature19A1")
    @level("Robustness")
    def test_get_device_state_software_id(self):
        """
        Validate ``getDeviceState`` software id field is ignored by the firmware

        [5] getDeviceState() -> deviceState
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ContextualDisplay.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send getDeviceState request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ContextualDisplayTestUtils.HIDppHelper.get_device_state(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check getDeviceState response fields")
            # ----------------------------------------------------------------------------------------------------------
            ContextualDisplayTestUtils.GetDeviceStateResponseChecker.check_fields(
                self, response, self.feature_19a1.get_device_state_response_cls)
            # end for
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ROB_19A1_0001#6", _AUTHOR)
    # end def test_get_device_state_software_id

    @features("Feature19A1")
    @level("Robustness")
    def test_set_config_software_id(self):
        """
        Validate ``setConfig`` software id field is ignored by the firmware

        [6] setConfig(config) -> config
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ContextualDisplay.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send setConfig request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ContextualDisplayTestUtils.HIDppHelper.set_config(
                test_case=self,
                device_adopted=False,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check setConfig response fields")
            # ----------------------------------------------------------------------------------------------------------
            ContextualDisplayTestUtils.SetConfigResponseChecker.check_fields(
                self, response, self.feature_19a1.set_config_response_cls)
            # end for
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ROB_19A1_0001#7", _AUTHOR)
    # end def test_set_config_software_id

    @features("Feature19A1")
    @level("Robustness")
    def test_get_config_software_id(self):
        """
        Validate ``getConfig`` software id field is ignored by the firmware

        [7] getConfig() -> config
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ContextualDisplay.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send getConfig request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ContextualDisplayTestUtils.HIDppHelper.get_config(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check getConfig response fields")
            # ----------------------------------------------------------------------------------------------------------
            ContextualDisplayTestUtils.GetConfigResponseChecker.check_fields(
                self, response, self.feature_19a1.get_config_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ROB_19A1_0001#8", _AUTHOR)
    # end def test_get_config_software_id

    @features("Feature19A1")
    @level("Robustness")
    def test_set_image_reserved(self):
        """
        Validate ``setImage`` reserved bytes are ignored by the firmware
        """
        image_count = 1
        result_code = 0
        image_payload = HexList(self.color_code[ImageFormat.RGB_565] *
                                int(self.config.BUTTON_TABLE.F_ButtonLocationWidth[0], 16) *
                               int(self.config.BUTTON_TABLE.F_ButtonLocationHeight[0], 16))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_RESERVED)
        # --------------------------------------------------------------------------------------------------------------
        for wrong_reserved in compute_wrong_range(0, max_value=(1 << SetImagePayloadMixin.LEN.RESERVED) - 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetImage request with reserved: {wrong_reserved}")
            # ----------------------------------------------------------------------------------------------------------
            button_info = ButtonInfoConfig.from_index(
                self.f, 0, self.config_manager).button_info_payload

            image = ContextualDisplay.Image(image_format=ImageFormat.RGB_565,
                                            image_location_x=button_info.button_location_x,
                                            image_location_y=button_info.button_location_y,
                                            image_location_width=button_info.button_location_width,
                                            image_location_height=button_info.button_location_height,
                                            image_size=len(image_payload),
                                            image_data=image_payload)

            full_payload = SetImagePayloadMixin(display_index=GetDisplayInfo.DEFAULT.DISPLAY_INDEX,
                                                        defer_display_update=0,
                                                        image_count=image_count,
                                                        images=[image])
            full_payload.reserved = wrong_reserved

            responses = VlpProtocolTestUtils.VlpHelper.vlp_transfer(
                test_case=self,
                payload=HexList(full_payload),
                report_payload_size=self.report_payload_size,
                report_type=self.feature_19a1.set_image_cls,
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_19a1_index,
                start_seqn=0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetImageResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ContextualDisplayTestUtils.SetImageResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "result_code": (checker.check_result_code, result_code),
                "count": (checker.check_count, image_count)
            })
            checker.check_fields(self, responses[-1], self.feature_19a1.set_image_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_19A1_0002#1", _AUTHOR)
    # end def test_set_image_reserved

    @features("Feature19A1")
    @level("Robustness")
    def test_set_config_reserved(self):
        """
        Validate ``setConfig`` reserved bytes are ignored by the firmware
        """
        device_adopted = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_RESERVED)
        # --------------------------------------------------------------------------------------------------------------
        for wrong_reserved in compute_wrong_range(0, max_value=(1 << ConfigFormat.LEN.RESERVED) - 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetConfig request")
            # ----------------------------------------------------------------------------------------------------------
            response = ContextualDisplayTestUtils.HIDppHelper.set_config(
                test_case=self,
                reserved=wrong_reserved,
                device_adopted=device_adopted)

            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetConfig Response fields")
            # --------------------------------------------------------------------------------------------------------------
            checker = ContextualDisplayTestUtils.SetConfigResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "device_adopted": (checker.check_device_adopted, device_adopted)
            })
            checker.check_fields(self, response, self.feature_19a1.set_config_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_19A1_0002#2", _AUTHOR)
    # end def test_set_config_reserved

    @features("Feature0020")
    @features("Feature19A1")
    @level("Robustness")
    def test_0020_cookie_set_config(self):
        """
        Validate configuration set via 0x0020 has no effect
        """
        device_adopted = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x0020")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_0020_index = ChannelUtils.update_feature_mapping(self, feature_id=ConfigChange.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetConfig request")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.set_config(
            test_case=self,
            device_adopted=device_adopted)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_SET_CONFIG_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.SetConfigResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_adopted": (checker.check_device_adopted, device_adopted)
        })
        checker.check_fields(self, response, self.feature_19a1.set_config_response_cls, check_map)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetConfigurationCookie request with cookie value greater than 0")
        # ----------------------------------------------------------------------------------------------------------
        set_config_complete = SetConfigurationComplete(deviceIndex=HexList(ChannelUtils.get_device_index(self)),
                                                       featureId=self.feature_0020_index,
                                                       configurationCookie=HexList("0001"))
        set_config_complete_response = ChannelUtils.send(
            self, report=set_config_complete, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=SetConfigurationCompleteResponse)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetConfigurationCookieResponse fields")
        # ----------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=HexList('0001'),
                         obtained=set_config_complete_response.configurationCookie,
                         msg='The configurationCookie parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_GET_CONFIG)
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.get_config(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_GET_CONFIG_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.GetConfigResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_19a1.get_config_response_cls, check_map)

        self.testCaseChecked("ROB_19A1_0003", _AUTHOR)
    # end def test_0020_cookie_set_config

    @features("Feature19A1")
    @features("BootloaderAvailable")
    @level("Robustness")
    def test_device_state_change_dfu_timeout(self):
        """
        Validate DFU Confirmation screen time out changes the device state.
        """
        device_state = ContextualDisplay.DeviceState.STREAMING_A0
        dfu_device_state = ContextualDisplay.DeviceState.DFU_SCREEN_A6

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send SetDeviceState with state = {device_state}")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.set_device_state(
            test_case=self,
            device_state=device_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetDeviceStateResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.SetDeviceStateResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_state": (checker.check_device_state, device_state)
        })
        checker.check_fields(self, response, self.feature_19a1.set_device_state_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check deviceStateEvent received with state = {device_state}")
        # --------------------------------------------------------------------------------------------------------------
        device_state_event = ContextualDisplayTestUtils.HIDppHelper.device_state_event(test_case=self)

        self.assertEqual(expected=device_state,
                         obtained=device_state_event.device_state,
                         msg=_DEVICE_STATE_EVENT_CHECK)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Enable DFU")
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.set_dfu_control(test_case=self, enter_dfu=1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check deviceStateEvent received with state = {dfu_device_state}")
        # --------------------------------------------------------------------------------------------------------------
        device_state_event = ContextualDisplayTestUtils.HIDppHelper.device_state_event(test_case=self)

        self.assertEqual(expected=dfu_device_state,
                         obtained=device_state_event.device_state,
                         msg=_DEVICE_STATE_EVENT_CHECK)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetDeviceState request")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.get_device_state(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check GetDeviceStateResponse has device_state = {dfu_device_state}")
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.GetDeviceStateResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_state": (checker.check_device_state, dfu_device_state)
        })
        checker.check_fields(self, response, self.feature_19a1.get_device_state_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wait for DFU timeout")
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlTimeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check deviceStateEvent received with state = {device_state}")
        # --------------------------------------------------------------------------------------------------------------
        device_state_event = ContextualDisplayTestUtils.HIDppHelper.device_state_event(test_case=self)

        self.assertEqual(expected=device_state,
                         obtained=device_state_event.device_state,
                         msg=_DEVICE_STATE_EVENT_CHECK)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetDeviceState request")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.get_device_state(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check GetDeviceStateResponse has device_state = {device_state}")
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.GetDeviceStateResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_state": (checker.check_device_state, device_state)
        })
        checker.check_fields(self, response, self.feature_19a1.get_device_state_response_cls, check_map)

        self.testCaseChecked("ROB_19A1_0004", _AUTHOR)
    # end def test_device_state_change_dfu_timeout

    @features("Feature19A1")
    @level("Robustness")
    def test_device_adopted_state_device_reset(self):
        """
        Verify Device Adopted status is not changed after device reset
        """
        device_adopted = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetConfig with Device Adopted status=1")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.set_config(
            test_case=self,
            device_adopted=device_adopted)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_SET_CONFIG_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.SetConfigResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_adopted": (checker.check_device_adopted, device_adopted)
        })
        checker.check_fields(self, response, self.feature_19a1.set_config_response_cls, check_map)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Force device reset")
        # ----------------------------------------------------------------------------------------------------------
        self.usb_unplug_and_replug()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_GET_CONFIG)
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.get_config(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_GET_CONFIG_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.GetConfigResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_adopted": (checker.check_device_adopted, device_adopted)
        })
        checker.check_fields(self, response, self.feature_19a1.get_config_response_cls, check_map)

        self.testCaseChecked("ROB_19A1_0005", _AUTHOR)
    # end def test_device_adopted_state_device_reset

    @features("Feature1805")
    @features("Feature19A1")
    @level("Robustness")
    def test_device_adopted_state_after_oob(self):
        """
        Verify Device Adopted status is changed after OOB
        """
        device_adopted = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enable hidden features")
        # --------------------------------------------------------------------------------------------------------------
        ContextualDisplayTestUtils.HIDppHelper.enable_hidden_features(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get Feature index of 0x1805")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1805_index, self.feature_1805, _, _ = OobStateTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetConfig with Device Adopted status=1")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.set_config(
            test_case=self,
            device_adopted=device_adopted)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_SET_CONFIG_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.SetConfigResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_adopted": (checker.check_device_adopted, device_adopted)
        })
        checker.check_fields(self, response, self.feature_19a1.set_config_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetOobState request")
        # --------------------------------------------------------------------------------------------------------------
        response = OobStateTestUtils.HIDppHelper.set_oob_state(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetOobStateResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.MessageChecker.check_fields(
            test_case=self, message=response, expected_cls=self.feature_1805.set_oob_state_response_cls,
            check_map={})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset the device")
        # --------------------------------------------------------------------------------------------------------------
        self.usb_unplug_and_replug()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_GET_CONFIG)
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.get_config(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_GET_CONFIG_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.GetConfigResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_19a1.get_config_response_cls, check_map)

        self.testCaseChecked("ROB_19A1_0006", _AUTHOR)
    # end def test_device_adopted_state_after_oob
# end class ContextualDisplayRobustnessTestCase
