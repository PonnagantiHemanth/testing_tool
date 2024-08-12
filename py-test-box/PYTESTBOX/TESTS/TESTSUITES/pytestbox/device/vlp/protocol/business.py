#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.vlp.protocol.business
:brief: VLP protocol business test suite
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2023/07/10
"""

# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.error import VlpErrorCodes
from pyhid.vlp.vlpmessage import VlpMessage
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.vlp.protocol.protocol import VlpProtocolTestCase
from pytestbox.device.vlp.protocol.vlpprotocoltestutils import VlpProtocolTestUtils

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
_AUTHOR = "Martin Cryonnet"


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class VlpProtocolBusinessTestCase(VlpProtocolTestCase):
    """
    Validate VLP protocol business test cases
    """

    @features("VLP")
    @features("MultiPacket")
    @level("Business")
    def test_vlp_multi_packet(self):
        """
        Goal: Multi-packet transfer : "In practice, SW choses to use the SEQN from the last command packet sent by SW
        for that feature, incremented by 1. The SEQN field increments for every subsequent packet within a
        multi-packet transfer (one direction) and may not reset between transactions. Finally, the SEQN will wrap
        around if overflown."
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get multi-packet transfer payload")
        # --------------------------------------------------------------------------------------------------------------
        full_payload = self._get_multi_packet_payload()

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

        self.testCaseChecked("BUS_VLP_PROTOCOL_0001#1", _AUTHOR)
    # end def test_vlp_multi_packet

    @features("VLP")
    @features("MultiPacket")
    @level("Business")
    def test_vlp_multi_packet_seqn_wrap_around(self):
        """
        Goal: Multi-packet transfer : "In practice, SW choses to use the SEQN from the last command packet sent by SW
        for that feature, incremented by 1. The SEQN field increments for every subsequent packet within a
        multi-packet transfer (one direction) and may not reset between transactions. Finally, the SEQN will wrap
        around if overflown."
        """
        # Number of images. See log below.
        img_count = 4
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Get multi-packet transfer payload to set {img_count} images. Number of "
                                 f"images should be large enough to get a payload large enough to check all possible "
                                 f"sequence number values but not too large to not exceed function's max buffer")
        # --------------------------------------------------------------------------------------------------------------
        full_payload = self._get_multi_packet_payload(img_count=img_count)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Full payload size = {len(full_payload)}")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        test_seqn = []
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
            test_seqn.append(report.seqn)

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

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Check all values of sequence number have been tested")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=set(range(0, pow(2, VlpMessage.LEN.VLP_SEQUENCE_NUMBER))),
                         obtained=set(test_seqn),
                         msg="All values of sequence number should be tested")

        self.testCaseChecked("BUS_VLP_PROTOCOL_0001#2", _AUTHOR)
    # end def test_vlp_multi_packet_seqn_wrap_around

    @features("VLP")
    @features("MultiPacket")
    @level("Business")
    def test_vlp_multi_packet_continue_after_sequence_error(self):
        """
        Goal: "When SW receives SEQUENCE_ERROR it should wait briefly for additional ACK replies to prior command
        packets then continue sending from the oldest packet not acknowledged or the expected SEQN from the error
        message (whichever is newer). If SEQUENCE_ERROR reoccurs, SW will restart the entire transfer." => Check
        multi-packet transfer can be continued from the oldest valid SEQN after SEQUENCE_ERROR
        """

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get multi-packet transfer payload")
        # --------------------------------------------------------------------------------------------------------------
        full_payload = self._get_multi_packet_payload()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        report, remaining_payload = self._get_start_report(full_payload)
        trigger_seq_err = True
        for _ in range(len(full_payload) // self.report_payload_size + 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Report Sequence Number = {report.seqn}")
            # ----------------------------------------------------------------------------------------------------------
            ack = ChannelUtils.send(self, report=report, response_queue_name=HIDDispatcher.QueueName.VLP_COMMON)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ACK message")
            # ----------------------------------------------------------------------------------------------------------
            VlpProtocolTestUtils.check_ack_message(self, report, ack)

            if not report.begin and trigger_seq_err:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Trigger sequence error in multi-packet transfer")
                # ------------------------------------------------------------------------------------------------------
                VlpProtocolTestUtils.HIDppHelper.send_report_wait_error(
                    test_case=self, report=report, error_type=VlpErrorCodes, error_codes=[VlpErrorCodes.SEQUENCE_ERROR])
                trigger_seq_err = False
            # end if
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

        self.testCaseChecked("BUS_VLP_PROTOCOL_0002", _AUTHOR)
    # end def test_vlp_multi_packet_continue_after_sequence_error

    @features("VLP")
    @features("MultiPacket")
    @level("Business")
    def test_vlp_multi_packet_restart_after_two_sequence_error(self):
        """
        Goal: "When SW receives SEQUENCE_ERROR it should wait briefly for additional ACK replies to prior command
        packets then continue sending from the oldest packet not acknowledged or the expected SEQN from the error
        message (whichever is newer). If SEQUENCE_ERROR reoccurs, SW will restart the entire transfer." => Check
        multi-packet transfer can be continued from the oldest valid SEQN after SEQUENCE_ERROR
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get multi-packet transfer payload")
        # --------------------------------------------------------------------------------------------------------------
        full_payload = self._get_multi_packet_payload()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Start multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        report, _ = self._get_start_report(full_payload)
        ack = ChannelUtils.send(self, report=report, response_queue_name=HIDDispatcher.QueueName.VLP_COMMON)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ACK message")
        # --------------------------------------------------------------------------------------------------------------
        VlpProtocolTestUtils.check_ack_message(self, report, ack)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Trigger sequence error in multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        report.begin = 0
        VlpProtocolTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self, report=report, error_type=VlpErrorCodes, error_codes=[VlpErrorCodes.SEQUENCE_ERROR])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Trigger second sequence error in multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        report.begin = 0
        report.seqn += 2
        VlpProtocolTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self, report=report, error_type=VlpErrorCodes, error_codes=[VlpErrorCodes.SEQUENCE_ERROR])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Re-Start multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        self._vlp_transfer(full_payload)

        self.testCaseChecked("BUS_VLP_PROTOCOL_0003", _AUTHOR)
    # end def test_vlp_multi_packet_restart_after_two_sequence_error
# end class VlpProtocolBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
