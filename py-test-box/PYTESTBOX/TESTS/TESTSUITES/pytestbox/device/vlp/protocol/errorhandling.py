#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.vlp.protocol.errorhandling
:brief: VLP protocol error handling test suite
:author: Martin Cryonnet <mcryonnet@logitch.com>
:date: 2023/07/10
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pychannel.usbchannel import LogitechReportId
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pyhid.hidpp.features.error import VlpErrorCodes
from pyhid.vlp.features.common.contextualdisplay import ContextualDisplay
from pyhid.vlp.features.common.contextualdisplay import GetDisplayInfo
from pyhid.vlp.features.common.contextualdisplay import ImageFormat
from pyhid.vlp.features.common.contextualdisplay import SetImagePayloadMixin
from pyhid.vlp.vlpmessage import VlpMessage
from pyhid.vlp.vlpmessage import VlpMessageRaw
from pyhid.vlp.vlpmessage import VlpMessageRawPayload
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import choices
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.vlprootutils import VLPRootTestUtils
from pytestbox.device.vlp.protocol.protocol import VlpProtocolTestCase
from pytestbox.device.vlp.protocol.vlpprotocoltestutils import VlpProtocolTestUtils

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
_AUTHOR = "Martin Cryonnet"


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class VlpProtocolErrorHandlingTestCase(VlpProtocolTestCase):
    """
    Validate VLP protocol error handling test cases
    """
    @features("VLP")
    @level("ErrorHandling")
    def test_longer_payload_size_static_function(self):
        """
        Goal: Forward compatibility : "In VLP, the static size payload buffer will not tolerate any non-zero bytes
        that are beyond the declared payload size needs in the function documentation even, if they are successfully
        delivered via a VLP report. The former limitation does not apply to the dynamic payload functions of the VLP."
        => Check longer payload can not be sent and VLP error is returned for static functions
        """
        # Payload without padding
        feature_set_report = VlpMessageRaw(
            report_id=LogitechReportId.REPORT_ID_EXTENDED_VLP_MESSAGE,
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=0x01,
            function_index=0x2,
            begin=True,
            end=True,
            ack=True,
            seqn=0
        )

        # Choose N values to test
        n_values = 5
        min_value = 1
        max_value = self.vlp_extended_report_size - VlpMessage.HEADER_SIZE_BYTES
        values = choices(my_list=list(range(min_value, max_value)), elem_nb=n_values)
        # Make sure min and max values are part of the test
        values += [min_value, max_value]
        values = sorted(set(values))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Loop over {len(values)} padding sizes")
        # --------------------------------------------------------------------------------------------------------------
        for padding_size in values:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Add padding up to {padding_size}")
            # ----------------------------------------------------------------------------------------------------------
            feature_set_report.payload = HexList("AA" * padding_size)
            VlpProtocolTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self, report=feature_set_report, error_codes=[VlpErrorCodes.OUT_OF_MEMORY])
        # end for

        self.testCaseChecked("ERR_VLP_PROTOCOL_0001", _AUTHOR)
    # end def test_longer_payload_size_static_function

    @features("VLP")
    @level("ErrorHandling")
    def test_longer_payload_size_dynamic_function(self):
        """
        Goal: Forward compatibility : "For the dynamic payload functions the FW shall accept any payload size up to
        the declared payload size in the feature enumeration." => Check payload longer than declared payload size can
        not be sent for dynamic functions
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
                           - SetImagePayloadMixin.LEN.HEADER // 8
                           + 1)
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
            if not report.end:
                ack = ChannelUtils.send(self, report=report, response_queue_name=HIDDispatcher.QueueName.VLP_COMMON)
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check ACK message")
                # ------------------------------------------------------------------------------------------------------
                VlpProtocolTestUtils.check_ack_message(self, report, ack)
                report, remaining_payload = VlpProtocolTestUtils.VlpHelper.get_next_report(
                    report, remaining_payload, self.report_payload_size)
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "End multi-packet transfer")
                # ------------------------------------------------------------------------------------------------------
                VlpProtocolTestUtils.HIDppHelper.send_report_wait_error(
                    test_case=self, report=report, error_codes=[VlpErrorCodes.OUT_OF_MEMORY])
                break
            # end if
        else:
            self.fail("Multi-packet transfer end was not reached")
        # end for

        self.testCaseChecked("ERR_VLP_PROTOCOL_0002", _AUTHOR)
    # end def test_longer_payload_size_dynamic_function

    @features("VLP")
    @level("ErrorHandling")
    def test_multi_packet_with_single_packet_same_feature(self):
        """
        "Goal : When BEGIN == 0, FW should check FUNC_ID, SW_ID, and SEQN, and if it doesn’t continue an existing
        transfer (FUNC_ID, SW_ID matches and SEQN is incremented by one) FW should reply with an error (cf. VLP
        errors) and ignore the packet." => Check changing FuncId during multi-packet transfer returns an error
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get multi-packet transfer payload")
        # --------------------------------------------------------------------------------------------------------------
        full_payload = self._get_multi_packet_payload()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get first report of multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        report, remaining_payload = self._get_start_report(full_payload)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get other function for the same feature")
        # --------------------------------------------------------------------------------------------------------------
        report_single_packet = self.feature_19a1.get_capabilities_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_19a1_index
        )
        VlpProtocolTestUtils.VlpHelper.add_padding(report_single_packet, self.vlp_normal_report_size)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Start multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        ack = ChannelUtils.send(self, report=report, response_queue_name=HIDDispatcher.QueueName.VLP_COMMON)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ACK message")
        # --------------------------------------------------------------------------------------------------------------
        VlpProtocolTestUtils.check_ack_message(self, report, ack)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send other function for the same feature")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.send(
            self, report=report_single_packet, response_queue_name=HIDDispatcher.QueueName.VLP_COMMON)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Continue multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        report, _ = VlpProtocolTestUtils.VlpHelper.get_next_report(report, remaining_payload, self.report_payload_size)
        VlpProtocolTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self, report=report, error_codes=[VlpErrorCodes.TRANSACTION_ERROR])

        self.testCaseChecked("ERR_VLP_PROTOCOL_0003", _AUTHOR)
    # end def test_multi_packet_with_single_packet_same_feature

    @features("VLP")
    @level("ErrorHandling")
    def test_multi_packet_change_func_id(self):
        """
        "Goal : When BEGIN == 0, FW should check FUNC_ID, SW_ID, and SEQN, and if it doesn’t continue an existing
        transfer (FUNC_ID, SW_ID matches and SEQN is incremented by one) FW should reply with an error (cf. VLP
        errors) and ignore the packet." => Check changing FuncId during multi-packet transfer returns an error
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get multi-packet transfer payload")
        # --------------------------------------------------------------------------------------------------------------
        full_payload = self._get_multi_packet_payload()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get first report of multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        report, remaining_payload = self._get_start_report(full_payload)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Start multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        ack = ChannelUtils.send(self, report=report, response_queue_name=HIDDispatcher.QueueName.VLP_COMMON)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ACK message")
        # --------------------------------------------------------------------------------------------------------------
        VlpProtocolTestUtils.check_ack_message(self, report, ack)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Continue multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        report, _ = VlpProtocolTestUtils.VlpHelper.get_next_report(report, remaining_payload, self.report_payload_size)
        report.function_index = 0
        VlpProtocolTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self, report=report, error_codes=[VlpErrorCodes.TRANSACTION_ERROR])

        self.testCaseChecked("ERR_VLP_PROTOCOL_0004", _AUTHOR)
    # end def test_multi_packet_change_func_id

    @features("VLP")
    @level("ErrorHandling")
    def test_multi_packet_change_sw_id(self):
        """
        "Goal : When BEGIN == 0, FW should check FUNC_ID, SW_ID, and SEQN, and if it doesn’t continue an existing
        transfer (FUNC_ID, SW_ID matches and SEQN is incremented by one) FW should reply with an error (cf. VLP
        errors) and ignore the packet." => Check changing SwId during multi-packet transfer returns an error
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get multi-packet transfer payload")
        # --------------------------------------------------------------------------------------------------------------
        full_payload = self._get_multi_packet_payload()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get first report of multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        report, remaining_payload = self._get_start_report(full_payload)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Start multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        ack = ChannelUtils.send(self, report=report, response_queue_name=HIDDispatcher.QueueName.VLP_COMMON)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ACK message")
        # --------------------------------------------------------------------------------------------------------------
        VlpProtocolTestUtils.check_ack_message(self, report, ack)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Continue multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        report, _ = VlpProtocolTestUtils.VlpHelper.get_next_report(report, remaining_payload, self.report_payload_size)
        report.software_id = 0
        VlpProtocolTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self, report=report, error_codes=[VlpErrorCodes.TRANSACTION_ERROR])

        self.testCaseChecked("ERR_VLP_PROTOCOL_0005", _AUTHOR)
    # end def test_multi_packet_change_sw_id

    @features("VLP")
    @level("ErrorHandling")
    def test_multi_packet_no_begin(self):
        """
        Goal: TRANSACTION ERROR "is returned by FW when there is a serious issue with a transfer or a transaction
        between SW and FW. Notably, if FUNC_ID or SW_ID doesn’t match or there was no ongoing transfer" => Check
        TRANSACTION_ERROR when there was no ongoing transfer
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get multi-packet transfer payload")
        # --------------------------------------------------------------------------------------------------------------
        full_payload = self._get_multi_packet_payload()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get first report of multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        report, _ = self._get_start_report(full_payload)
        report.begin = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Start multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        VlpProtocolTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self, report=report, error_codes=[VlpErrorCodes.TRANSACTION_ERROR])

        self.testCaseChecked("ERR_VLP_PROTOCOL_0006", _AUTHOR)
    # end def test_multi_packet_no_begin

    @features("VLP")
    @level("ErrorHandling")
    def test_multi_packet_sequence_error_repeat_seqn(self):
        """
        Goal: "When BEGIN == 0, FW should check FUNC_ID, SW_ID, and SEQN, and if it doesn’t continue an existing
        transfer (FUNC_ID, SW_ID matches and SEQN is incremented by one) FW should reply with an error (cf. VLP
        errors) and ignore the packet." => Check repeating SEQN twice, without incrementing, returns an error
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get multi-packet transfer payload")
        # --------------------------------------------------------------------------------------------------------------
        full_payload = self._get_multi_packet_payload()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get first report of multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        report, remaining_payload = self._get_start_report(full_payload)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Start multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        ack = ChannelUtils.send(self, report=report, response_queue_name=HIDDispatcher.QueueName.VLP_COMMON)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ACK message")
        # --------------------------------------------------------------------------------------------------------------
        VlpProtocolTestUtils.check_ack_message(self, report, ack)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Continue multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        report, _ = VlpProtocolTestUtils.VlpHelper.get_next_report(report, remaining_payload, self.report_payload_size)
        ack = ChannelUtils.send(self, report=report, response_queue_name=HIDDispatcher.QueueName.VLP_COMMON)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ACK message")
        # --------------------------------------------------------------------------------------------------------------
        VlpProtocolTestUtils.check_ack_message(self, report, ack)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send twice to trigger sequence error in multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        err_rsp = VlpProtocolTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self, report=report, error_codes=[VlpErrorCodes.SEQUENCE_ERROR])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check expected sequence error and received sequence error in error message")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(obtained=err_rsp.seqn_exp, expected=report.seqn + 1,
                         msg="Expected sequence number should be sequence number from the report incremented of 1")
        self.assertEqual(obtained=err_rsp.seqn_rcv, expected=report.seqn,
                         msg="Received sequence number should be sequence number from the report")

        self.testCaseChecked("ERR_VLP_PROTOCOL_0007", _AUTHOR)
    # end def test_multi_packet_sequence_error_repeat_seqn

    @features("VLP")
    @level("ErrorHandling")
    def test_multi_packet_sequence_error_skip_seqn(self):
        """
        Goal: "When BEGIN == 0, FW should check FUNC_ID, SW_ID, and SEQN, and if it doesn’t continue an existing
        transfer (FUNC_ID, SW_ID matches and SEQN is incremented by one) FW should reply with an error (cf. VLP
        errors) and ignore the packet." => Check incrementing SEQN by 2 or more returns an error
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get multi-packet transfer payload")
        # --------------------------------------------------------------------------------------------------------------
        full_payload = self._get_multi_packet_payload()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get first report of multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        start_report, remaining_payload = self._get_start_report(full_payload)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Start multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        ack = ChannelUtils.send(self, report=start_report, response_queue_name=HIDDispatcher.QueueName.VLP_COMMON)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ACK message")
        # --------------------------------------------------------------------------------------------------------------
        VlpProtocolTestUtils.check_ack_message(self, start_report, ack)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Continue multi-packet transfer, increment sequence number of more than 1")
        # --------------------------------------------------------------------------------------------------------------
        report, _ = VlpProtocolTestUtils.VlpHelper.get_next_report(
            start_report, remaining_payload, self.report_payload_size)
        report.seqn += 1
        err_rsp = VlpProtocolTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self, report=report, error_codes=[VlpErrorCodes.SEQUENCE_ERROR])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check expected sequence error and received sequence error in error message")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(obtained=err_rsp.seqn_exp, expected=start_report.seqn + 1,
                         msg="Expected sequence number should be sequence number from the report incremented of 1")
        self.assertEqual(obtained=err_rsp.seqn_rcv, expected=report.seqn,
                         msg="Received sequence number should be sequence number from the report")

        self.testCaseChecked("ERR_VLP_PROTOCOL_0008", _AUTHOR)
    # end def test_multi_packet_sequence_error_skip_seqn

    @features("VLP")
    @level("ErrorHandling")
    def test_multi_packet_sequence_error_decrement_seqn(self):
        """
        Goal: "When BEGIN == 0, FW should check FUNC_ID, SW_ID, and SEQN, and if it doesn’t continue an existing
        transfer (FUNC_ID, SW_ID matches and SEQN is incremented by one) FW should reply with an error (cf. VLP
        errors) and ignore the packet." => Check decrementing SEQN returns an error
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get multi-packet transfer payload")
        # --------------------------------------------------------------------------------------------------------------
        full_payload = self._get_multi_packet_payload()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get first report of multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        start_report, remaining_payload = self._get_start_report(full_payload)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Start multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        ack = ChannelUtils.send(self, report=start_report, response_queue_name=HIDDispatcher.QueueName.VLP_COMMON)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ACK message")
        # --------------------------------------------------------------------------------------------------------------
        VlpProtocolTestUtils.check_ack_message(self, start_report, ack)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Continue multi-packet transfer, increment sequence number of more than 1")
        # --------------------------------------------------------------------------------------------------------------
        report, _ = VlpProtocolTestUtils.VlpHelper.get_next_report(
            start_report, remaining_payload, self.report_payload_size)
        report.seqn = (report.seqn - 1) % pow(2, VlpMessage.LEN.VLP_SEQUENCE_NUMBER)
        err_rsp = VlpProtocolTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self, report=report, error_codes=[VlpErrorCodes.SEQUENCE_ERROR])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check expected sequence error and received sequence error in error message")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(obtained=err_rsp.seqn_exp, expected=start_report.seqn + 1,
                         msg="Expected sequence number should be sequence number from the report incremented of 1")
        self.assertEqual(obtained=err_rsp.seqn_rcv, expected=report.seqn,
                         msg="Received sequence number should be sequence number from the report")

        self.testCaseChecked("ERR_VLP_PROTOCOL_0009", _AUTHOR)
    # end def test_multi_packet_sequence_error_decrement_seqn

    @features("VLP")
    @level("ErrorHandling")
    def test_single_packet_hidpp_error_ack(self):
        """
        Goal: "The FW replies to every command packet containing ACK == 1 by sending an ACK reply, response,
        or error packet while if ACK == 0, the FW shall not send any response for that packet."
        => Check error is received when ACK = 1
        """
        feature_set_report = VlpMessageRawPayload(
            report_id=VlpMessage.DEFAULT.REPORT_ID_NORMAL_VLP_MESSAGE,
            device_index=ChannelUtils.get_device_index(self),
            feature_index=0x01,
            function_index=0x1,
            begin=True,
            end=True,
            ack=True,
            sequence_number=0,
            payload=HexList("03"), # TODO : 3 = feature_set.get_count + 1
        )
        VlpProtocolTestUtils.VlpHelper.add_padding(feature_set_report, self.vlp_normal_report_size)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send VLP single packet with ACK = 1")
        # --------------------------------------------------------------------------------------------------------------
        VlpProtocolTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self, report=feature_set_report, error_codes=[VlpErrorCodes.INVALID_ARGUMENT])

        self.testCaseChecked("ERR_VLP_PROTOCOL_0010", _AUTHOR)
    # end def test_single_packet_hidpp_error_ack

    @features("VLP")
    @level("ErrorHandling")
    def test_multi_packet_sequence_error_no_ack(self):
        """
         Goal: "The FW replies to every command packet containing ACK == 1 by sending an ACK reply, response,
         or error packet while if ACK == 0, the FW shall not send any response for that packet." => Check VLP error
         is received when ACK = 0
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get multi-packet transfer payload")
        # --------------------------------------------------------------------------------------------------------------
        full_payload = self._get_multi_packet_payload()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get first report of multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        start_report, remaining_payload = self._get_start_report(full_payload)
        start_report.ack = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Start multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.send_only(self, report=start_report)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Continue multi-packet transfer, increment sequence number of more than 1")
        # --------------------------------------------------------------------------------------------------------------
        report, _ = VlpProtocolTestUtils.VlpHelper.get_next_report(
            start_report, remaining_payload, self.report_payload_size)
        report.seqn += 1
        err_rsp = VlpProtocolTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self, report=report, error_codes=[VlpErrorCodes.SEQUENCE_ERROR])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check expected sequence error and received sequence error in error message")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(obtained=err_rsp.seqn_exp, expected=start_report.seqn + 1,
                         msg="Expected sequence number should be sequence number from the report incremented of 1")
        self.assertEqual(obtained=err_rsp.seqn_rcv, expected=report.seqn,
                         msg="Received sequence number should be sequence number from the report")

        self.testCaseChecked("ERR_VLP_PROTOCOL_0011", _AUTHOR)
    # end def test_multi_packet_sequence_error_no_ack

    @features("VLP")
    @level("ErrorHandling")
    def test_multi_packet_invalid_argument_ack_end_only(self):
        """
         Goal: "In case of errors such as incorrect invalid payload or other (cf. HID++ 2.0 error codes)) FW shall
         continue to ACK reply normally (if ACK == 1) until the command transfer is complete and the payload is
         processed. If END == 1 and ACK == 0 no error will be returned"
         => Check error is received when END = 1 and ACK = 1
        """
        x_y_img = self._get_image_positions()
        image = ContextualDisplay.Image(image_format=ImageFormat.RGB_565,
                                        image_location_x=x_y_img[0][0],
                                        image_location_y=x_y_img[0][1],
                                        image_location_width=self.img_width,
                                        image_location_height=self.img_height,
                                        image_size=len(self.img),
                                        image_data=self.img)

        full_payload = HexList(SetImagePayloadMixin(display_index=GetDisplayInfo.DEFAULT.DISPLAY_INDEX,
                                                    defer_display_update=True,
                                                    image_count=0x0A,   # Invalid argument
                                                    images=[image]))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        report, remaining_payload = self._get_start_report(full_payload)
        report.ack = False
        for _ in range(len(full_payload) // self.report_payload_size + 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Report Sequence Number = {report.seqn}")
            # ----------------------------------------------------------------------------------------------------------
            if not report.end:
                ChannelUtils.send_only(self, report=report)
                report, remaining_payload = VlpProtocolTestUtils.VlpHelper.get_next_report(
                    report, remaining_payload, self.report_payload_size)
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "End multi-packet transfer")
                # ------------------------------------------------------------------------------------------------------
                report.ack = True
                VlpProtocolTestUtils.HIDppHelper.send_report_wait_error(
                    test_case=self, report=report, error_codes=[VlpErrorCodes.INVALID_ARGUMENT])
                break
            # end if
        else:
            self.fail("Multi-packet transfer end was not reached")
        # end for

        self.testCaseChecked("ERR_VLP_PROTOCOL_0012", _AUTHOR)
    # end def test_multi_packet_invalid_argument_ack_end_only

    @features("VLP")
    @level("ErrorHandling")
    def test_multi_packet_invalid_argument_ack(self):
        """
          Goal: "In case of errors such as incorrect invalid payload or other (cf. HID++ 2.0 error codes)) FW shall
          continue to ACK reply normally (if ACK == 1) until the command transfer is complete and the payload is
          processed. If END == 1 and ACK == 0 no error will be returned" => Check error is received when END = 1 and
          ACK = 1
        """
        x_y_img = self._get_image_positions()
        image = ContextualDisplay.Image(image_format=ImageFormat.RGB_565,
                                        image_location_x=x_y_img[0][0],
                                        image_location_y=x_y_img[0][1],
                                        image_location_width=self.img_width,
                                        image_location_height=self.img_height,
                                        image_size=len(self.img),
                                        image_data=self.img)

        full_payload = HexList(SetImagePayloadMixin(display_index=GetDisplayInfo.DEFAULT.DISPLAY_INDEX,
                                                    defer_display_update=True,
                                                    image_count=0x0A,  # Invalid argument
                                                    images=[image]))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        report, remaining_payload = self._get_start_report(full_payload)
        for _ in range(len(full_payload) // self.report_payload_size + 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Report Sequence Number = {report.seqn}")
            # ----------------------------------------------------------------------------------------------------------
            if not report.end:
                ack = ChannelUtils.send(self, report=report, response_queue_name=HIDDispatcher.QueueName.VLP_COMMON)
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check ACK message")
                # ------------------------------------------------------------------------------------------------------
                VlpProtocolTestUtils.check_ack_message(self, report, ack)
                report, remaining_payload = VlpProtocolTestUtils.VlpHelper.get_next_report(
                    report, remaining_payload, self.report_payload_size)
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "End multi-packet transfer")
                # ------------------------------------------------------------------------------------------------------
                VlpProtocolTestUtils.HIDppHelper.send_report_wait_error(
                    test_case=self, report=report, error_codes=[VlpErrorCodes.INVALID_ARGUMENT])
                break
            # end if
        else:
            self.fail("Multi-packet transfer end was not reached")
        # end for

        self.testCaseChecked("ERR_VLP_PROTOCOL_0013", _AUTHOR)
    # end def test_multi_packet_invalid_argument_ack
# end class VlpProtocolErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
