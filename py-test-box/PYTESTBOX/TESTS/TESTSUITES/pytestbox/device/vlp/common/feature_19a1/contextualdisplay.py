#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.vlp.device.hidpp20.common.feature_19a1.contextualdisplay
:brief: Validate VLP 1.0 ``ContextualDisplay`` feature
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/11/02
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pychannel.channelinterfaceclasses import LinkEnablerInfo
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.vlp.vlpmessage import VlpMessage
from pyhid.vlp.vlpmessage import VlpMessageHeader
from pyhid.vlp.features.common.contextualdisplay import ContextualDisplay
from pyhid.vlp.features.common.contextualdisplay import GetDisplayInfo
from pyhid.vlp.features.common.contextualdisplay import ImageFormat
from pyhid.vlp.features.common.contextualdisplay import SetImagePayloadMixin
from pyhid.vlp.features.common.contextualdisplay import SetImageResponse
from pylibrary.tools.hexlist import HexList
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.displayinfoutils import ButtonInfoConfig
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.vlp.base.contextualdisplayutils import ContextualDisplayTestUtils
from pytestbox.device.vlp.protocol.vlpprotocoltestutils import VlpProtocolTestUtils
from pyusb.libusbdriver import LibusbDriver


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class ContextualDisplayTestCase(DeviceBaseTestCase):
    """
    Validate ``ContextualDisplay`` TestCases in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()

        report_id_size = VlpMessage.LEN.REPORT_ID // 8
        self.vlp_normal_report_size = VlpProtocolTestUtils.get_report_count_vlp_normal(self) + report_id_size
        self.vlp_extended_report_size = VlpProtocolTestUtils.get_report_count_vlp_extended(self) + report_id_size
        self.report_payload_size = self.vlp_extended_report_size - VlpMessageHeader.HEADER_SIZE_BYTES
        # Logi Breakthrough Teal
        self.color_code = {
            ImageFormat.RGB_888: '00FDCF',
            ImageFormat.RGB_565: '5907'
        }
        self.splash_animation_duration = 5.5

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Change default sending method on current channel")
        # --------------------------------------------------------------------------------------------------------------
        self.current_channel.send_data = self.current_channel.send_data_interrupt_write

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x19A1 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_19a1_index, self.feature_19a1, _, _ = ContextualDisplayTestUtils.HIDppHelper.get_vlp_parameters(
            test_case=self)

        self.config = self.f.PRODUCT.FEATURES.VLP.COMMON.CONTEXTUAL_DISPLAY
        self.deferrable_display_capability = int(self.config.F_CapabilitiesFlags[0])
        self.rgb_565_capability = int(self.config.F_CapabilitiesFlags[1])
        self.rgb_888_capability = int(self.config.F_CapabilitiesFlags[2])
        self.jpeg_capability = int(self.config.F_CapabilitiesFlags[3])
        self.calibrated_capability = int(self.config.F_CapabilitiesFlags[4])
        self.origin = int(self.config.F_CapabilitiesFlags[5])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Set Device Adopted state to False")
        # --------------------------------------------------------------------------------------------------------------
        ContextualDisplayTestUtils.HIDppHelper.set_config(test_case=self, device_adopted=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Sleep to allow time for device state transition animation to complete")
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.splash_animation_duration)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Clear Device State Event messages")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.VLP_EVENT,
            class_type=self.feature_19a1.device_state_event_cls)
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            with CommonBaseTestUtils.EmulatorHelper.debugger_closed(debugger=self.debugger):
                try:
                    LibusbDriver.disable_usb_port(port_index=ChannelUtils.get_port_index(test_case=self))
                finally:
                    LibusbDriver.enable_usb_port(port_index=ChannelUtils.get_port_index(test_case=self))
                # end try
            # end with
        # end with
        super().tearDown()
    # end def tearDown

    def usb_unplug_and_replug(self, wait_end_of_state_transition=True):
        """
        Perform device reset by disable/enable USB port simulating unplug/replug
        """
        try:
            LibusbDriver.disable_usb_port(port_index=ChannelUtils.get_port_index(test_case=self))
        finally:
            LibusbDriver.enable_usb_port(port_index=ChannelUtils.get_port_index(test_case=self))
        # end try
        CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(test_case=self)

        if wait_end_of_state_transition:
            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Sleep to allow time for device state transition animation to complete")
            # --------------------------------------------------------------------------------------------------------------
            sleep(self.splash_animation_duration)
        # end if
    # end def usb_unplug_and_replug

    def create_images(self, image_format, x_res=0, y_res=0, image_payload=None, buttons=0, image_size=None):
        """
        Create Image(s) based on the image data and resolution

        :return: list of images
        :rtype: ``list[ContextualDisplay.Image]``
        """
        max_memory = int(self.config.F_FeatureMaxMemory)
        cumulative_payload_size = 0
        image_payload = HexList(self.color_code[image_format] * x_res * y_res) \
            if image_payload is None else image_payload
        image_size = len(image_payload) if image_size is None else image_size

        images = []
        buttons = [buttons] if not isinstance(buttons, list) else buttons
        for index in buttons:
            button_info = ButtonInfoConfig.from_index(
                self.f, index, self.config_manager).button_info_payload
            cumulative_payload_size += image_size
            if cumulative_payload_size >= max_memory:
                break
            # end if
            images.append(
                ContextualDisplay.Image(image_format=image_format,
                                        image_location_x=button_info.button_location_x,
                                        image_location_y=button_info.button_location_y,
                                        image_location_width=button_info.button_location_width if x_res == 0
                                        else x_res,
                                        image_location_height=button_info.button_location_height if y_res == 0
                                        else y_res,
                                        image_size=image_size,
                                        image_data=image_payload))
        # end for
        return images
    # end def create_images

    def send_images(self, images, ack=True, error_code=None):
        """
        Send Set Image API

        :return: list of responses if ack is True else None
        :rtype: ``list[VlpMessage]|None``
        """
        responses = None
        full_payload = SetImagePayloadMixin(display_index=GetDisplayInfo.DEFAULT.DISPLAY_INDEX,
                                            defer_display_update=0,
                                            image_count=len(images),
                                            images=images)
        if error_code is not None:
            report, remaining_payload = VlpProtocolTestUtils.VlpHelper.get_next_report(
                previous_report=None,
                remaining_payload=HexList(full_payload),
                report_payload_size=self.report_payload_size,
                report_type=self.feature_19a1.set_image_cls,
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_19a1_index,
                ack=True,
                seqn=0
            )
            for _ in range(len(HexList(full_payload)) // self.report_payload_size + 1):
                ChannelUtils.send_only(test_case=self, report=report, channel=None)
                if not report.end:
                    report, remaining_payload = VlpProtocolTestUtils.VlpHelper.get_next_report(
                        report, remaining_payload, self.report_payload_size)
                else:
                    break
                # end if
            else:
                self.fail("Multi-packet transfer end was not reached")
            # end for
        else:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send SetImage VLP Request')
            # ----------------------------------------------------------------------------------------------------------
            responses = VlpProtocolTestUtils.VlpHelper.vlp_transfer(
                test_case=self,
                payload=HexList(full_payload),
                report_payload_size=self.report_payload_size,
                report_type=self.feature_19a1.set_image_cls,
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_19a1_index,
                ack=ack,
                start_seqn=0)
        # end if
        return responses
    # end def send_images

    def validate_response(self, responses=None, result_code=None, error_code=None, image_count=0):
        """
        Validate Set Image Response/Error Codes

        :param responses: List of responses to be validated
        :type responses: ``list[VlpMessage]``
        :param result_code: Expected result code
        :type result_code: ``int|None``
        :param error_code: Expected error code
        :type error_code: ``int|None``
        :param image_count: Expected image count
        :type image_count: ``int``
        """
        image_count = 0 if (result_code is not None and
                            result_code >= SetImageResponse.UNSUPPORTED_IMAGE_RESOLUTION) else image_count
        if error_code is not None:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check Error Codes {error_code} returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            error_message = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.ERROR,
                                                  class_type=ErrorCodes)

            self.assertEqual(expected=error_code,
                             obtained=error_message.errorCode,
                             msg=f'The received error code {error_message.errorCode} '
                                 f'do not match the expected one {error_code}!')
        else:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, f"Check response received with result code={result_code}")
            # ----------------------------------------------------------------------------------------------------------
            checker = ContextualDisplayTestUtils.SetImageResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "result_code": (checker.check_result_code, result_code),
                "count": (checker.check_count, image_count)
            })
            checker.check_fields(self, responses[-1], self.feature_19a1.set_image_response_cls, check_map)
        # end if
    # end def validate_response

    def set_image_and_validate(self, image_format, x_res=0, y_res=0, result_code=None, image_count=0, ack=True,
                               error_code=None, image_size=None, buttons=0, image_payload=None):
        """
        Send Set Image API and validate Response/Error codes.
        """
        images = self.create_images(image_format=image_format,
                                    x_res=x_res,
                                    y_res=y_res,
                                    image_payload=image_payload,
                                    buttons=buttons,
                                    image_size=image_size)

        responses = self.send_images(images=images,
                                     ack=ack,
                                     error_code=error_code)

        self.validate_response(responses=responses,
                               result_code=result_code,
                               error_code=error_code,
                               image_count=image_count)
    # end def set_image_and_validate
# end class ContextualDisplayTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
