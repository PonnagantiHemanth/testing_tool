#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.vlp.protocol.protocol
:brief: VLP protocol test suite
:author: Martin Cryonnet <mcryonnet@logitch.com>
:date: 2023/07/10
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.vlp.features.common.contextualdisplay import ContextualDisplay
from pyhid.vlp.features.common.contextualdisplay import ContextualDisplayFactory
from pyhid.vlp.features.common.contextualdisplay import GetDisplayInfo
from pyhid.vlp.features.common.contextualdisplay import GetDisplayInfoResponsePayloadMixin
from pyhid.vlp.features.common.contextualdisplay import ImageFormat
from pyhid.vlp.features.common.contextualdisplay import SetImagePayloadMixin
from pyhid.vlp.vlpmessage import VlpMessage
from pyhid.vlp.vlpmessage import VlpMessageHeader
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.vlprootutils import VLPRootTestUtils
from pytestbox.device.vlp.base.vlpfeaturesetutils import VLPFeatureSetTestUtils
from pytestbox.device.vlp.protocol.vlpprotocoltestutils import VlpProtocolTestUtils

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
_AUTHOR = "Martin Cryonnet"


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class VlpProtocolTestCase(DeviceBaseTestCase):
    """
    Validate VLP protocol test cases
    """
    FEATURE_TYPE_NOT_HIDDEN = False
    FEATURE_TYPE_HIDDEN = True

    def setUp(self):
        # See ``DeviceBaseTestCase.setUp``
        super().setUp()

        report_id_size = VlpMessage.LEN.REPORT_ID // 8
        self.vlp_normal_report_size = VlpProtocolTestUtils.get_report_count_vlp_normal(self) + report_id_size
        self.vlp_extended_report_size = VlpProtocolTestUtils.get_report_count_vlp_extended(self) + report_id_size
        self.report_payload_size = self.vlp_extended_report_size - VlpMessageHeader.HEADER_SIZE_BYTES

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Change default sending method on current channel")
        # --------------------------------------------------------------------------------------------------------------
        self.current_channel.send_data = self.current_channel.send_data_interrupt_write

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x0102 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_0102_index, self.feature_0102, _, _ = VLPRootTestUtils.HIDppHelper.get_vlp_parameters(
            test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x0103 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_0103_index, self.feature_0103, _, _ = \
            VLPFeatureSetTestUtils.HIDppHelper.get_vlp_parameters(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x19A1 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_19a1_index, self.feature_19a1, _, _ = VlpProtocolTestUtils.HIDppHelper.get_vlp_parameters(
            test_case=self, feature_id=ContextualDisplay.FEATURE_ID, factory=ContextualDisplayFactory)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get display info")
        # --------------------------------------------------------------------------------------------------------------
        get_display_info = self.feature_19a1.get_display_info_cls(
            device_index=ChannelUtils.get_device_index(self),
            feature_index=self.feature_19a1_index,
            display_index=self.feature_19a1.get_display_info_cls.DEFAULT.DISPLAY_INDEX)

        get_display_info_responses = VlpProtocolTestUtils.VlpHelper.send(
            self,
            report=get_display_info,
            response_queue_name=HIDDispatcher.QueueName.VLP_COMMON,
            response_class_type=self.feature_19a1.get_display_info_response_cls)

        self.display_info = VlpProtocolTestUtils.VlpHelper.get_parsed_multi_packet_payload(
            get_display_info_responses, GetDisplayInfoResponsePayloadMixin)

        self.img_width = to_int(self.display_info.button_info_0.button_location_width)
        self.img_height = to_int(self.display_info.button_info_0.button_location_height)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self,
                                   f"Define a {self.img_width}px x {self.img_height}px 16 bits Bitmap RGB565 grey test "
                                   f"image to use for large transfers")
        # --------------------------------------------------------------------------------------------------------------
        self.img = HexList("18C6" * self.img_width * self.img_height)
    # end def setUp

    def tearDown(self):
        # See ``DeviceBaseTestCase.tearDown``
        with self.manage_post_requisite():
            self.current_channel.send_data = self.current_channel.send_data_control_write
        # end with
        super().tearDown()
    # end def tearDown

    def _get_image_positions(self):
        """
        Get image coordinates
        """
        return [
            (getattr(self.display_info, f"button_info_{button_index}").button_location_x,
             getattr(self.display_info, f"button_info_{button_index}").button_location_y)
            for button_index in range(to_int(self.display_info.button_count))]
    # end def _get_image_positions

    def _get_multi_packet_payload(self, img_count=1):
        """
        Get full data to send throw VLP multi-packet transfer

        :param img_count: Number of images
        :type img_count: ``int``

        :return: Full VLP multi-packet payload
        :rtype: ``HexList``
        """
        # Images positions
        x_y_img = self._get_image_positions()
        images = [ContextualDisplay.Image(image_format=ImageFormat.RGB_565,
                                          image_location_x=x_y_img[image_index][0],
                                          image_location_y=x_y_img[image_index][1],
                                          image_location_width=self.img_width,
                                          image_location_height=self.img_height,
                                          image_size=len(self.img),
                                          image_data=self.img)
                  for image_index in range(img_count)
                  ]

        set_image_payload = SetImagePayloadMixin(display_index=GetDisplayInfo.DEFAULT.DISPLAY_INDEX,
                                                 defer_display_update=True,
                                                 image_count=img_count,
                                                 images=images)

        return HexList(set_image_payload)
    # end def _get_multi_packet_payload

    def _get_start_report(self, full_payload, start_seqn=0):
        """
        Get first report to start a VLP transfer

        :param full_payload: Full payload to send
        :type full_payload: ``HexList``

        :return: The start report and the remaining payload
        :rtype: ``tuple[VlpMessage, HexList]``
        """
        report, remaining_payload = VlpProtocolTestUtils.VlpHelper.get_next_report(
            previous_report=None,
            remaining_payload=full_payload,
            report_payload_size=self.report_payload_size,
            report_type=self.feature_19a1.set_image_cls,
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_19a1_index,
            ack=True,
            seqn=start_seqn
        )
        return report, remaining_payload
    # end def _get_start_report

    def _vlp_transfer(self, full_payload, start_seqn=0):
        """
        Send standard VLP transfer for the VLP protocol tests

        :param full_payload: Full payload to send
        :type full_payload: ``HexList``
        :param start_seqn: Initial sequence number
        :type start_seqn: ``int``
        """
        return VlpProtocolTestUtils.VlpHelper.vlp_transfer(test_case=self,
                                                    payload=full_payload,
                                                    report_payload_size=self.report_payload_size,
                                                    report_type=self.feature_19a1.set_image_cls,
                                                    device_index=ChannelUtils.get_device_index(test_case=self),
                                                    feature_index=self.feature_19a1_index,
                                                    start_seqn=start_seqn)
    # end def _vlp_transfer
# end class VlpProtocolTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
