#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.vlp.protocol.robustness
:brief: VLP protocol robustness test suite
:author: Martin Cryonnet <mcryonnet@logitch.com>
:date: 2023/07/10
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.error import VlpErrorCodes
from pyhid.vlp.features.common.contextualdisplay import ContextualDisplay
from pyhid.vlp.features.common.contextualdisplay import GetDisplayInfo
from pyhid.vlp.features.common.contextualdisplay import ImageFormat
from pyhid.vlp.features.common.contextualdisplay import SetImagePayloadMixin
from pyhid.vlp.features.important.vlpfeatureset import VLPFeatureSet
from pyhid.vlp.features.important.vlproot import VLPRoot
from pyhid.vlp.vlpmessage import VlpMessage
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pylibrary.tools.numeral import Numeral
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.vlprootutils import VLPRootTestUtils
from pytestbox.device.vlp.base.vlpfeaturesetutils import VLPFeatureSetTestUtils
from pytestbox.device.vlp.protocol.protocol import VlpProtocolTestCase
from pytestbox.device.vlp.protocol.vlpprotocoltestutils import VlpProtocolTestUtils

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
_AUTHOR = "Martin Cryonnet"


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class VlpProtocolRobustnessTestCase(VlpProtocolTestCase):
    """
    Validate VLP protocol robustness test cases
    """
    @features("VLP")
    @level("Robustness")
    def test_payload_size(self):
        """
        "For the dynamic payload functions the FW shall accept any payload size up to the declared payload size in
        the feature enumeration." => Check payload up to declared payload size can be sent
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x19A1 payload size")
        # --------------------------------------------------------------------------------------------------------------
        response = VLPRootTestUtils.HIDppHelper.get_feature_index(
            self,
            report_id=VlpMessage.DEFAULT.REPORT_ID_NORMAL_VLP_MESSAGE,
            feature_id=ContextualDisplay.FEATURE_ID,
            vlp_begin=True,
            vlp_end=True,
            vlp_ack=True
        )
        feature_max_memory = to_int(response.feature_max_memory)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Feature 0x19A1 max memory: {feature_max_memory}")
        # --------------------------------------------------------------------------------------------------------------
        x_y_img = self._get_image_positions()
        image_data_size = (feature_max_memory
                           - ContextualDisplay.Image.LEN.HEADER // 8
                           - SetImagePayloadMixin.LEN.HEADER // 8)
        image_data = HexList("AA" * image_data_size)
        image = ContextualDisplay.Image(image_format=ImageFormat.RGB_565,
                                        image_location_x=x_y_img[0][0],
                                        image_location_y=x_y_img[0][1],
                                        image_location_width=self.img_width,
                                        image_location_height=self.img_height,
                                        image_size=len(image_data),
                                        image_data=image_data)

        full_payload = HexList(SetImagePayloadMixin(display_index=GetDisplayInfo.DEFAULT.DISPLAY_INDEX,
                                                    defer_display_update=True,
                                                    image_count=1,
                                                    images=[image]))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        report, remaining_payload = self._get_start_report(full_payload)
        for _ in range(len(full_payload) // self.report_payload_size + 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Report Sequence Number = {report.seqn}")
            # ----------------------------------------------------------------------------------------------------------
            ack = ChannelUtils.send(self, report=report, response_queue_name=HIDDispatcher.QueueName.VLP_COMMON)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ACK message")
            # ----------------------------------------------------------------------------------------------------------
            VlpProtocolTestUtils.check_ack_message(self, report, ack)
            if not report.end:
                report, remaining_payload = VlpProtocolTestUtils.VlpHelper.get_next_report(
                    report, remaining_payload, self.report_payload_size)
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "End multi-packet transfer")
                # ------------------------------------------------------------------------------------------------------
                break
            # end if
        else:
            self.fail("Multi-packet transfer end was not reached")
        # end for

        self.testCaseChecked("ROB_VLP_PROTOCOL_0001", _AUTHOR)
    # end def test_payload_size

    @features("VLP")
    @level("Robustness")
    @bugtracker('VLPNoForwardBackwardCompatibility')
    def test_backward_compatibility(self):
        """
        Goal: "For backwards compatibility, implementations for new versions of a VLP feature should be designed to
        accept the shorter payload lengths sent by older versions of that feature."
        => Check shorter payload can be sent

        Goal: "Missing data should be treated as if it has the value 0." => Check missing data of shorter payload are
        treated as 0
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Get Feature ID function (0x0103) without any parameters")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_0103.get_feature_id_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=VLPFeatureSet.FEATURE_INDEX,
            feature_idx=HexList("00"))
        report.FIELDS = report.FIELDS[:-1]
        response = ChannelUtils.send(self, report=report, response_queue_name=HIDDispatcher.QueueName.VLP_IMPORTANT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Check response corresponds to feature index = 0")
        # --------------------------------------------------------------------------------------------------------------
        checker = VLPFeatureSetTestUtils.GetFeatureIDResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "feature_idx": (checker.check_feature_idx, self.feature_0102_index),
                "feature_id": (checker.check_feature_id, Numeral(VLPRoot.FEATURE_ID)),
                "feature_version": (checker.check_feature_version, self.feature_0102.VERSION),
                "feature_type": (checker.check_feature_type, self.FEATURE_TYPE_NOT_HIDDEN),
                "feature_max_memory": (
                    checker.check_feature_max_memory, self.f.PRODUCT.FEATURES.VLP.IMPORTANT.ROOT.F_FeatureMaxMemory)
            }
        )
        checker.check_fields(self, response, self.feature_0103.get_feature_id_response_cls, check_map)

        self.testCaseChecked("ROB_VLP_PROTOCOL_0002", _AUTHOR)
    # end def test_backward_compatibility

    @features("VLP")
    @features("MultiPacket")
    @level("Functionality")
    def test_vlp_multi_packet_continue_after_multiple_sequence_error(self):
        """
        Goal: "When SW receives SEQUENCE_ERROR it should wait briefly for additional ACK replies to prior command
        packets then continue sending from the oldest packet not acknowledged or the expected SEQN from the error
        message (whichever is newer). If SEQUENCE_ERROR reoccurs, SW will restart the entire transfer." => Check
        multi-packet transfer can be continued from the oldest valid SEQN after SEQUENCE_ERROR, even if multiple
        SEQUENCE_ERROR errors occur (not consecutively)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get multi-packet transfer payload")
        # --------------------------------------------------------------------------------------------------------------
        full_payload = self._get_multi_packet_payload()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        report, remaining_payload = self._get_start_report(full_payload)
        ack = ChannelUtils.send(self, report=report, response_queue_name=HIDDispatcher.QueueName.VLP_COMMON)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ACK message")
        # --------------------------------------------------------------------------------------------------------------
        VlpProtocolTestUtils.check_ack_message(self, report, ack)
        report, remaining_payload = VlpProtocolTestUtils.VlpHelper.get_next_report(
            report, remaining_payload, self.report_payload_size)
        for _ in range(len(full_payload) // self.report_payload_size + 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Report Sequence Number = {report.seqn}")
            # ----------------------------------------------------------------------------------------------------------
            ack = ChannelUtils.send(self, report=report, response_queue_name=HIDDispatcher.QueueName.VLP_COMMON)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ACK message")
            # ----------------------------------------------------------------------------------------------------------
            VlpProtocolTestUtils.check_ack_message(self, report, ack)

            if not report.end:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send twice to trigger sequence error in multi-packet transfer")
                # ------------------------------------------------------------------------------------------------------
                VlpProtocolTestUtils.HIDppHelper.send_report_wait_error(
                    test_case=self, report=report, error_codes=[VlpErrorCodes.SEQUENCE_ERROR])
                report, remaining_payload = VlpProtocolTestUtils.VlpHelper.get_next_report(
                    report, remaining_payload, self.report_payload_size)
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "End multi-packet transfer")
                # ------------------------------------------------------------------------------------------------------
                break
            # end if
        else:
            self.fail("Multi-packet transfer end was not reached")
        # end for

        self.testCaseChecked("ROB_VLP_PROTOCOL_0002", _AUTHOR)
    # end def test_vlp_multi_packet_continue_after_multiple_sequence_error

    @features("VLP")
    @features("MultiPacket")
    @level("Functionality")
    def test_vlp_multi_packet_continue_after_multiple_consecutive_sequence_error(self):
        """
        Goal: "When SW receives SEQUENCE_ERROR it should wait briefly for additional ACK replies to prior command
        packets then continue sending from the oldest packet not acknowledged or the expected SEQN from the error
        message (whichever is newer). If SEQUENCE_ERROR reoccurs, SW will restart the entire transfer."
        => Check multi-packet transfer can be continued from the oldest valid SEQN after SEQUENCE_ERROR,
        even if multiple SEQUENCE_ERROR errors occur (consecutively)
        Note: This is not the recommended behavior for the SW. The SW should restart the entire transfer if
        SEQUENCE_ERROR reoccurs. This test checks the behavior of the firmware if the SW doesn't respect this rule.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get multi-packet transfer payload")
        # --------------------------------------------------------------------------------------------------------------
        full_payload = self._get_multi_packet_payload()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        report, remaining_payload = self._get_start_report(full_payload)
        ack = ChannelUtils.send(self, report=report, response_queue_name=HIDDispatcher.QueueName.VLP_COMMON)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ACK message")
        # --------------------------------------------------------------------------------------------------------------
        VlpProtocolTestUtils.check_ack_message(self, report, ack)
        report, remaining_payload = VlpProtocolTestUtils.VlpHelper.get_next_report(
            report, remaining_payload, self.report_payload_size)
        for _ in range(len(full_payload) // self.report_payload_size + 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Report Sequence Number = {report.seqn}")
            # ----------------------------------------------------------------------------------------------------------
            ack = ChannelUtils.send(self, report=report, response_queue_name=HIDDispatcher.QueueName.VLP_COMMON)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ACK message")
            # ----------------------------------------------------------------------------------------------------------
            VlpProtocolTestUtils.check_ack_message(self, report, ack)

            if not report.end:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send {report.seqn} to trigger sequence error in multi-packet transfer")
                # ------------------------------------------------------------------------------------------------------
                for _ in range(report.seqn):
                    VlpProtocolTestUtils.HIDppHelper.send_report_wait_error(
                        test_case=self, report=report, error_codes=[VlpErrorCodes.SEQUENCE_ERROR])
                # end for
                report, remaining_payload = VlpProtocolTestUtils.VlpHelper.get_next_report(
                    report, remaining_payload, self.report_payload_size)
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "End multi-packet transfer")
                # ------------------------------------------------------------------------------------------------------
                break
            # end if
        else:
            self.fail("Multi-packet transfer end was not reached")
        # end for

        self.testCaseChecked("ROB_VLP_PROTOCOL_0003", _AUTHOR)
    # end def test_vlp_multi_packet_continue_after_multiple_consecutive_sequence_error
# end class VlpProtocolRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
