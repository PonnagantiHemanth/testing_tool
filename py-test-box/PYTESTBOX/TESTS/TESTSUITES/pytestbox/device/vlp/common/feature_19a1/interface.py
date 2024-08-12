#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.vlp.common.feature_19a1.interface
:brief: VLP 1.0 ``ContextualDisplay`` interface test suite
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/11/02
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from os.path import join
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.vlp.features.common.contextualdisplay import GetDisplayInfoResponsePayloadMixin
from pyhid.vlp.features.common.contextualdisplay import ImageFormat
from pyhid.vlp.features.common.contextualdisplay import SetImageResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pysetup import TESTS_PATH
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


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class ContextualDisplayInterfaceTestCase(ContextualDisplayTestCase):
    """
    Validate ``ContextualDisplay`` interface test cases
    """

    @features("Feature19A1")
    @level("Interface")
    def test_get_capabilities(self):
        """
        Validate ``GetCapabilities`` normal processing

        [0] getCapabilities() -> deviceScreenCount, maxImageSize, maxImageFps, deviceCapabilities
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetCapabilities request")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.get_capabilities(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.DeviceCapabilitiesChecker
        device_capabilities = {
            "deferrable_display_update_capability": (checker.check_deferrable_display_update_capability,
                                                     self.deferrable_display_capability),
            "rgb_565": (checker.check_rgb_565, self.rgb_565_capability),
            "rgb_888": (checker.check_rgb_888, self.rgb_888_capability),
            "jpeg": (checker.check_jpeg, self.jpeg_capability),
            "calibrated": (checker.check_calibrated, self.calibrated_capability),
            "origin": (checker.check_origin, self.origin),
            "reserved": (checker.check_reserved, 0x0)
        }
        checker = ContextualDisplayTestUtils.GetCapabilitiesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_19a1_index)),
            "device_screen_count": (checker.check_device_screen_count, self.config.F_DeviceScreenCount),
            "max_image_size": (checker.check_max_image_size, self.config.F_MaxImageSize),
            "max_image_fps": (checker.check_max_image_fps, self.config.F_MaxImageFPS),
            "device_capabilities": (checker.check_device_capabilities, device_capabilities)
        })
        checker.check_fields(self, response, self.feature_19a1.get_capabilities_response_cls, check_map)

        self.testCaseChecked("INT_19A1_0001", _AUTHOR)
    # end def test_get_capabilities

    @features("Feature19A1")
    @level("Interface")
    def test_get_display_info(self):
        """
        Validate ``GetDisplayInfo`` normal processing

        [1] getDisplayInfo(displayIndex) -> displayShape, displayDimension, horizontalResolution,
        verticalResolution, buttonCount, visibleAreaCount, buttonInfo, visibleAreaInfo
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
        LogHelper.log_step(self, "Send GetDisplayInfo request")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.get_display_info(
            test_case=self,
            display_index=display_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetDisplayInfoResponse fields")
        # --------------------------------------------------------------------------------------------------------------
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
                "field_name" : f"button_info_{b_index}",
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

        self.testCaseChecked("INT_19A1_0002", _AUTHOR)
    # end def test_get_display_info

    @features("Feature19A1")
    @level("Interface")
    def test_set_image(self):
        """
        Validate ``SetImage`` normal processing

        [2] setImage(displayIndex, imageCount, imageData) -> resultCode, count
        """
        image_count = 1
        image_format = ImageFormat.JPEG
        result_code = int(SetImageResponse.DISPLAY_UPDATED)

        with open(join(TESTS_PATH, "IMAGE_FILES", "image.jpg"), "rb") as f:
            image = f.read()
            image_payload = bytearray(image)
        # end with

        self.img = HexList(image_payload)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetImage request")
        # --------------------------------------------------------------------------------------------------------------
        payload = ContextualDisplayTestUtils._get_multi_packet_set_image_payload(
            test_case=self, image_format=image_format, img_count=image_count, defer_display_update=False)

        responses = VlpProtocolTestUtils.VlpHelper.vlp_transfer(
            test_case=self,
            payload=payload,
            report_payload_size=self.report_payload_size,
            report_type=self.feature_19a1.set_image_cls,
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_19a1_index,
            ack=True,
            start_seqn=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetImageResponse fields")
        # --------------------------------------------------------------------------------------------------------------
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

        self.testCaseChecked("INT_19A1_0003", _AUTHOR)
    # end def test_set_image

    @features("Feature19A1")
    @level("Interface")
    def test_get_supported_device_states(self):
        """
        Validate ``GetSupportedDeviceStates`` normal processing

        [3] getSupportedDeviceStates() -> deviceState
        """
        device_states = self.config.F_SupportedDeviceStates
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetSupportedDeviceStates request")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.get_supported_device_states(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetSupportedDeviceStatesResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.GetSupportedDeviceStatesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_19a1_index)),
        })
        for d_index in range(len(device_states)):
            device_state_info = ({
                "field_name": f"device_state_{d_index}",
                "device_state" : (checker.check_device_state, device_states[d_index])
            })
            check_map.__setitem__(f"device_state_{d_index}",
                                  (checker.check_device_state_info, device_state_info))
        # end for
        checker.check_fields(self, response, self.feature_19a1.get_supported_device_states_response_cls, check_map)

        self.testCaseChecked("INT_19A1_0004", _AUTHOR)
    # end def test_get_supported_device_states

    @features("Feature19A1")
    @level("Interface")
    def test_set_device_state(self):
        """
        Validate ``SetDeviceState`` normal processing

        [4] setDeviceState(deviceState) -> deviceState
        """
        device_state = HexList(Numeral(self.config.F_SetDeviceStates[0]))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetDeviceState request")
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
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_19a1_index)),
            "device_state": (checker.check_device_state, device_state)
        })
        checker.check_fields(self, response, self.feature_19a1.set_device_state_response_cls, check_map)

        self.testCaseChecked("INT_19A1_0005", _AUTHOR)
    # end def test_set_device_state

    @features("Feature19A1")
    @level("Interface")
    def test_get_device_state(self):
        """
        Validate ``GetDeviceState`` normal processing

        [5] getDeviceState() -> deviceState
        """
        device_state = HexList(Numeral(self.config.F_DefaultDeviceState))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetDeviceState request")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.get_device_state(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetDeviceStateResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.GetDeviceStateResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_19a1_index)),
            "device_state": (checker.check_device_state, device_state)
        })
        checker.check_fields(self, response, self.feature_19a1.get_device_state_response_cls, check_map)

        self.testCaseChecked("INT_19A1_0006", _AUTHOR)
    # end def test_get_device_state

    @features("Feature19A1")
    @level("Interface")
    def test_set_config(self):
        """
        Validate ``SetConfig`` normal processing

        [6] setConfig(config) -> config
        """
        device_adopted = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetConfig request")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.set_config(
            test_case=self,
            device_adopted=device_adopted)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetConfigResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.SetConfigResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_19a1_index)),
            "device_adopted": (checker.check_device_adopted, device_adopted)
        })
        checker.check_fields(self, response, self.feature_19a1.set_config_response_cls, check_map)

        self.testCaseChecked("INT_19A1_0007", _AUTHOR)
    # end def test_set_config

    @features("Feature19A1")
    @level("Interface")
    def test_get_config(self):
        """
        Validate ``GetConfig`` normal processing

        [7] getConfig() -> config
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetConfig request")
        # --------------------------------------------------------------------------------------------------------------
        response = ContextualDisplayTestUtils.HIDppHelper.get_config(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetConfigResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ContextualDisplayTestUtils.GetConfigResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_19a1.get_config_response_cls, check_map)

        self.testCaseChecked("INT_19A1_0008", _AUTHOR)
    # end def test_get_config
# end class ContextualDisplayInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
