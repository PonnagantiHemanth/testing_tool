#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.vlp.protocol.functionality
:brief: VLP protocol functionality test suite
:author: Martin Cryonnet <mcryonnet@logitch.com>
:date: 2023/11/01
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from random import randint
from time import sleep

from pychannel.usbchannel import LogitechReportId
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pyhid.hidpp.features.error import VlpErrorCodes
from pyhid.hidpp.features.root import RootFactory
from pyhid.vlp.features.common.contextualdisplay import SetImagePayloadMixin
from pyhid.vlp.features.important.vlpfeatureset import VLPFeatureSet
from pyhid.vlp.features.important.vlproot import VLPRoot
from pyhid.vlp.vlpmessage import VlpMessage
from pyhid.vlp.vlpmessage import VlpMessageHeader
from pyhid.vlp.vlpmessage import VlpMessageRawPayload
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import choices
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
class VlpProtocolFunctionalityTestCase(VlpProtocolTestCase):
    """
    Validate VLP protocol functionality test cases
    """

    @features("VLP")
    @level("Functionality")
    def test_send_vlp_normal_report(self):
        """
        Goal: "For a device to be considered VLP-capable, the normal VLP report is required, while the extended one is
        optional" => Check VLP Normal report is supported
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self,
                           f"Send VLP normal report (report id = {VlpMessage.DEFAULT.REPORT_ID_NORMAL_VLP_MESSAGE})")
        # --------------------------------------------------------------------------------------------------------------
        response = VLPRootTestUtils.HIDppHelper.get_feature_index(
            self,
            report_id=VlpMessage.DEFAULT.REPORT_ID_NORMAL_VLP_MESSAGE,
            feature_id=VLPRoot.FEATURE_ID,
            vlp_begin=True,
            vlp_end=True,
            vlp_ack=True
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self,
                            "Check valid response is received, i.e. device replies to VLP Normal report without error")
        # --------------------------------------------------------------------------------------------------------------
        checker = VLPRootTestUtils.GetFeatureIndexResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "feature_index": (checker.check_feature_index, HexList(self.feature_0102_index)),
            "feature_id": (checker.check_feature_id, VLPRoot.FEATURE_ID),
            "feature_idx": (checker.check_feature_idx, HexList(self.feature_0102_index)),
            "feature_version": (checker.check_feature_version, self.feature_0102.VERSION),
            "feature_max_memory": (checker.check_feature_max_memory,
                                   self.f.PRODUCT.FEATURES.VLP.IMPORTANT.ROOT.F_FeatureMaxMemory)
        })
        checker.check_fields(test_case=self,
                             message=response,
                             expected_cls=self.feature_0102.get_feature_index_response_cls,
                             check_map=check_map)

        self.testCaseChecked("FUN_VLP_PROTOCOL_0001", _AUTHOR)
    # end def test_send_vlp_normal_report

    @features("VLP")
    @level("Functionality")
    def test_0102_0103_supported(self):
        """
        Goal: Check both features 0x0102 and 0x0103 are supported if VLP is supported
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "With feature 0x0102 - VLP Root, get feature index of 0x0102 - VLP Root")
        # --------------------------------------------------------------------------------------------------------------
        response = VLPRootTestUtils.HIDppHelper.get_feature_index(
            self,
            feature_id=VLPRoot.FEATURE_ID,
            vlp_begin=True,
            vlp_end=True,
            vlp_ack=True
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check valid response is received, i.e. 0x0102 - VLP Root is supported")
        # --------------------------------------------------------------------------------------------------------------
        checker = VLPRootTestUtils.GetFeatureIndexResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "feature_id": (checker.check_feature_id, VLPRoot.FEATURE_ID),
            "feature_idx": (checker.check_feature_idx, HexList(VLPRoot.FEATURE_INDEX)),
            "feature_version": (checker.check_feature_version, self.feature_0102.VERSION),
            "feature_max_memory": (checker.check_feature_max_memory,
                                   self.f.PRODUCT.FEATURES.VLP.IMPORTANT.ROOT.F_FeatureMaxMemory)
        })
        checker.check_fields(test_case=self,
                             message=response,
                             expected_cls=self.feature_0102.get_feature_index_response_cls,
                             check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Get feature 0x0103 feature config")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_set_config = self.f.PRODUCT.FEATURES.VLP.IMPORTANT.FEATURE_SET

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "With feature 0x0102 - VLP Root, get feature index of 0x0103 - VLP Feature Set")
        # --------------------------------------------------------------------------------------------------------------
        response = VLPRootTestUtils.HIDppHelper.get_feature_index(
            self,
            report_id=VlpMessage.DEFAULT.REPORT_ID_NORMAL_VLP_MESSAGE,
            feature_id=VLPFeatureSet.FEATURE_ID,
            vlp_begin=True,
            vlp_end=True,
            vlp_ack=True
        )
        feature_0103_version = response.feature_version

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self,
                            "Check valid response is received, with feature index for 0x0103 - Feature Set != 0x00")
        # --------------------------------------------------------------------------------------------------------------
        checker = VLPRootTestUtils.GetFeatureIndexResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "feature_index": (checker.check_feature_index, HexList(VLPRoot.FEATURE_INDEX)),
            "feature_id": (checker.check_feature_id, VLPFeatureSet.FEATURE_ID),
            "feature_idx": (checker.check_feature_idx, HexList(self.feature_0103_index)),
            "feature_version": (checker.check_feature_version, self.feature_0103.VERSION),
            "feature_max_memory": (checker.check_feature_max_memory, self.feature_set_config.F_FeatureMaxMemory)
        })
        checker.check_fields(test_case=self,
                             message=response,
                             expected_cls=self.feature_0102.get_feature_index_response_cls,
                             check_map=check_map)

        self.assertNotEqual(VLPRoot.FEATURE_NOT_FOUND, response.feature_idx,
                            f"Feature Index for 0x0103 - Feature Set should not be {VLPRoot.FEATURE_NOT_FOUND} ("
                            f"feature not found), because it should be supported")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "With feature 0x0103 - VLP Feature Set, get feature Id of 0x0102 - VLP Root")
        # --------------------------------------------------------------------------------------------------------------
        feature_set_response = VLPFeatureSetTestUtils.HIDppHelper.get_feature_id(self, VLPRoot.FEATURE_INDEX)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Check valid response is received, with feature id = {VLPRoot.FEATURE_ID} at feature index 0x00")
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
        checker.check_fields(self, feature_set_response, self.feature_0103.get_feature_id_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, "With feature 0x0103 - VLP Feature Set, get feature Id of 0x0103 - VLP Feature Set")
        # --------------------------------------------------------------------------------------------------------------
        feature_set_response = VLPFeatureSetTestUtils.HIDppHelper.get_feature_id(
            self, HexList(VLPFeatureSet.FEATURE_INDEX))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Check valid response is received, with feature id = 0x0103 at feature index 0x01")
        # --------------------------------------------------------------------------------------------------------------
        checker = VLPFeatureSetTestUtils.GetFeatureIDResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "feature_idx": (checker.check_feature_idx, self.feature_0103_index),
                "feature_id": (checker.check_feature_id, Numeral(VLPFeatureSet.FEATURE_ID)),
                "feature_version": (checker.check_feature_version, feature_0103_version),
                "feature_type": (checker.check_feature_type, self.FEATURE_TYPE_NOT_HIDDEN),
                "feature_max_memory": (checker.check_feature_max_memory, self.feature_set_config.F_FeatureMaxMemory)
            }
        )
        checker.check_fields(self, feature_set_response, self.feature_0103.get_feature_id_response_cls, check_map)

        self.testCaseChecked("FUN_VLP_PROTOCOL_0002", _AUTHOR)
    # end def test_0102_0103_supported

    @features("VLP")
    @features("VLPExtended")
    @level("Functionality")
    def test_vlp_report_type(self):
        """
        ==== Choosing VLP report for payload

        Each device/software is then free to choose either normal or extended VLP for transferring the VLP packets.
        The type of report to be used is not fixed per feature or even function. It depends on the actual payload to
        be sent and the choice is open to both device and software. For example a command may be invoked via an
        extended VLP while the response returns using a normal VLP report.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Loop over VLP report ids")
        # --------------------------------------------------------------------------------------------------------------
        for report_id in (LogitechReportId.REPORT_ID_NORMAL_VLP_MESSAGE,
                          LogitechReportId.REPORT_ID_EXTENDED_VLP_MESSAGE):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send VLP report with report id = {report_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = VLPRootTestUtils.HIDppHelper.get_feature_index(
                self,
                report_id=report_id,
                feature_id=VLPRoot.FEATURE_ID,
                vlp_begin=True,
                vlp_end=True,
                vlp_ack=True
            )

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check response report id is in VLP report ids")
            # ----------------------------------------------------------------------------------------------------------
            self.assertIn(response.report_id, (HexList(LogitechReportId.REPORT_ID_NORMAL_VLP_MESSAGE),
                                               HexList(LogitechReportId.REPORT_ID_EXTENDED_VLP_MESSAGE)))
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_VLP_PROTOCOL_0003", _AUTHOR)
    # end def test_vlp_report_type

    @features("VLP")
    @features("VLPExtended")
    @features("MultiPacket")
    @features("MultiPacketMultiReportTypes")
    @level("Functionality")
    def test_vlp_multi_packet_multi_report_types(self):
        """
        "The multi-packet transfer MUST take place within the same report type, neither device nor host shall switch
        report types in the middle of a multi-packet transfer. Nevertheless, the device may choose to tolerate a
        switch of report type within the same multi-packet transfer and continue the transfer." => Check multiple
        report sizes can be used during a multi-packet transfer
        """
        report_ids = (
            LogitechReportId.REPORT_ID_NORMAL_VLP_MESSAGE,
            LogitechReportId.REPORT_ID_EXTENDED_VLP_MESSAGE
        )
        report_sizes = (self.vlp_normal_report_size, self.vlp_extended_report_size)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get multi-packet transfer payload")
        # --------------------------------------------------------------------------------------------------------------
        full_payload = self._get_multi_packet_payload()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        report, remaining_payload = self._get_start_report(full_payload)
        for _ in range(len(full_payload) // min(report_sizes) + 1):
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
                    report,
                    remaining_payload,
                    report_sizes[report.seqn % len(report_ids)] - VlpMessageHeader.HEADER_SIZE_BYTES)
                report.report_id = report_ids[report.seqn % len(report_ids)]
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "End multi-packet transfer")
                # ------------------------------------------------------------------------------------------------------
                break
            # end if
        else:
            self.fail("Multi-packet transfer end was not reached")
        # end for

        self.testCaseChecked("FUN_VLP_PROTOCOL_0004", _AUTHOR)
    # end def test_vlp_multi_packet_multi_report_types

    @features("VLP")
    @features("VLPExtended")
    @features("MultiPacket")
    @level("Functionality")
    def test_vlp_multi_packet_seqn_init_value(self):
        """
        Goal: Multi-packet transfer : SEQN :
        * "Initial value for a command transfer can be chosen arbitrary by SW."
        * "When BEGIN == 1, FW should accept any SEQN value."
        => Check transfer can be started with any value for Seqn
        """
        values = choices(list(range(pow(2, VlpMessage.LEN.VLP_SEQUENCE_NUMBER))),
                         elem_nb=pow(2, VlpMessage.LEN.VLP_SEQUENCE_NUMBER) // 3)
        values += [0, 1, pow(2, VlpMessage.LEN.VLP_SEQUENCE_NUMBER) - 1]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get multi-packet transfer payload")
        # --------------------------------------------------------------------------------------------------------------
        full_payload = self._get_multi_packet_payload()

        for seqn in set(values):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Re-Start multi-packet transfer from SEQN = {seqn}")
            # ----------------------------------------------------------------------------------------------------------
            self._vlp_transfer(full_payload, start_seqn=seqn)
        # end for

        self.testCaseChecked("FUN_VLP_PROTOCOL_0005", _AUTHOR)
    # end def test_vlp_multi_packet_seqn_init_value

    @features("VLP")
    @features("VLPExtended")
    @features("MultiPacket")
    @level("Functionality")
    def test_vlp_multi_packet_no_timeout(self):
        """
        "If a transfer is incomplete within the FW, it remains incomplete indefinitely until continued. There is no
        timeout in the FW requiring a transfer to complete within in a specific period"
        => Check incomplete transfer can be continued after a break
        """
        # Pick 4 random values, between 1 second and 1 minute
        pause_times = sorted([randint(1, 60) for _ in range(4)])

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
                pause_time = pause_times.pop(0) if pause_times else 0
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"Wait {pause_time}s before next packet")
                # ------------------------------------------------------------------------------------------------------
                sleep(pause_time)
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "End multi-packet transfer")
                # ------------------------------------------------------------------------------------------------------
                break
            # end if
        else:
            self.fail("Multi-packet transfer end was not reached")
        # end for

        self.testCaseChecked("FUN_VLP_PROTOCOL_0006", _AUTHOR)
    # end def test_vlp_multi_packet_no_timeout

    @features("VLP")
    @features("VLPExtended")
    @features("MultiPacket")
    @level("Functionality")
    def test_vlp_multi_packet_with_user_action(self):
        """
        "If a transfer is incomplete within the FW, it remains incomplete indefinitely until continued. There is no
        timeout in the FW requiring a transfer to complete within in a specific period"
        => Check incomplete transfer can be continued after a user action
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
            LogHelper.log_info(self, "Perform user action")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.user_action()

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

        self.testCaseChecked("FUN_VLP_PROTOCOL_0007", _AUTHOR)
    # end def test_vlp_multi_packet_with_user_action

    @features("VLP")
    @features("VLPExtended")
    @features("MultiPacket")
    @level("Functionality")
    def test_vlp_multi_packet_with_hidpp(self):
        """
        "If a transfer is incomplete within the FW, it remains incomplete indefinitely until continued. There is no
        timeout in the FW requiring a transfer to complete within in a specific period"
        => Check incomplete transfer can be continued after a HID++ request
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get the 0x0000 root feature object")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_0000 = RootFactory.create(
            self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.IMPORTANT.ROOT))
        feature_id = self.feature_0000.get_feature_cls.FEATURE_ID
        get_feature = self.feature_0000.get_feature_cls(
            deviceIndex=ChannelUtils.get_device_index(test_case=self),
            featureId=feature_id)

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
            LogHelper.log_info(self, "Send HID++ request : Root - Get Feature")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.send(
                test_case=self,
                report=get_feature,
                response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                response_class_type=self.feature_0000.get_feature_response_cls)

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

        self.testCaseChecked("FUN_VLP_PROTOCOL_0008", _AUTHOR)
    # end def test_vlp_multi_packet_with_hidpp

    @features("VLP")
    @features("VLPExtended")
    @features("MultiPacket")
    @level("Functionality")
    def test_vlp_multi_packet_transfer_restart_after_first_packet(self):
        """
        Goal: "If there was already a multi-packet transfer in progress for that feature but it is incomplete,
        that transfer is silently discarded and a new one is started." / "If a transfer is incomplete within the FW,
        it remains incomplete indefinitely until a new transfer with BEGIN == 1 is received." => Check new
        multi-packet transfer can be started after first packet
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
        LogHelper.log_step(self, "Re-Start multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        self._vlp_transfer(full_payload)

        self.testCaseChecked("FUN_VLP_PROTOCOL_0009", _AUTHOR)
    # end def test_vlp_multi_packet_transfer_restart_after_first_packet

    @features("VLP")
    @features("VLPExtended")
    @features("MultiPacket")
    @level("Functionality")
    def test_vlp_multi_packet_transfer_restart_after_middle_packet(self):
        """
        Goal: "If there was already a multi-packet transfer in progress for that feature but it is incomplete,
        that transfer is silently discarded and a new one is started." / "If a transfer is incomplete within the FW,
        it remains incomplete indefinitely until a new transfer with BEGIN == 1 is received." => Check new
        multi-packet transfer can be started after middle packet
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get multi-packet transfer payload")
        # --------------------------------------------------------------------------------------------------------------
        full_payload = self._get_multi_packet_payload()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Start multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        report, remaining_payload = self._get_start_report(full_payload)
        ack = ChannelUtils.send(self, report=report, response_queue_name=HIDDispatcher.QueueName.VLP_COMMON)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ACK message")
        # --------------------------------------------------------------------------------------------------------------
        VlpProtocolTestUtils.check_ack_message(self, report, ack)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Continue multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        report, remaining_payload = VlpProtocolTestUtils.VlpHelper.get_next_report(
            report, remaining_payload, self.report_payload_size)
        ack = ChannelUtils.send(self, report=report, response_queue_name=HIDDispatcher.QueueName.VLP_COMMON)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ACK message")
        # --------------------------------------------------------------------------------------------------------------
        VlpProtocolTestUtils.check_ack_message(self, report, ack)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Re-Start multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        self._vlp_transfer(full_payload)

        self.testCaseChecked("FUN_VLP_PROTOCOL_0010", _AUTHOR)
    # end def test_vlp_multi_packet_transfer_restart_after_middle_packet

    @features("VLP")
    @features("VLPExtended")
    @features("MultiPacket")
    @level("Functionality")
    def test_vlp_multi_packet_with_single_packet_vlp(self):
        """
        Goal: Check incomplete transfer can be continued after a single packet VLP transfer for another feature
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get feature 0x0102 VLP Root report")
        # --------------------------------------------------------------------------------------------------------------
        _, feature_0102, device_index, _ = VLPRootTestUtils.HIDppHelper.get_vlp_parameters(self)
        feature_0102_report = feature_0102.get_feature_index_cls(
            device_index=device_index,
            software_id=0xF,
            feature_id=VLPRoot.FEATURE_ID,
            vlp_begin=True,
            vlp_end=True,
            vlp_ack=True,
            vlp_sequence_number=0)
        VlpProtocolTestUtils.VlpHelper.add_padding(feature_0102_report, self.vlp_normal_report_size)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get multi-packet transfer payload")
        # --------------------------------------------------------------------------------------------------------------
        full_payload = self._get_multi_packet_payload()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Continue multi-packet transfer, with single packet VLP requests (other feature")
        # --------------------------------------------------------------------------------------------------------------
        report, remaining_payload = self._get_start_report(full_payload)
        for _ in range(len(full_payload) // self.report_payload_size + 1):
            # ---------------------------------------------------------------------------------
            LogHelper.log_info(self, 'Send Root GetFeature with VLP Root feature Id')
            # ---------------------------------------------------------------------------------
            ChannelUtils.send(
                test_case=self,
                report=feature_0102_report,
                response_queue_name=HIDDispatcher.QueueName.VLP_IMPORTANT,
                response_class_type=feature_0102.get_feature_index_response_cls)

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

        self.testCaseChecked("FUN_VLP_PROTOCOL_0011", _AUTHOR)
    # end def test_vlp_multi_packet_with_single_packet_vlp

    @features("VLP")
    @level("Functionality")
    def test_single_packet_ack(self):
        """
        Goal: "The FW replies to every command packet containing ACK == 1 by sending an ACK reply, response,
        or error packet while if ACK == 0, the FW shall not send any response for that packet."
        => Check response is received when ACK = 1
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send VLP single packet with ACK = 1")
        # --------------------------------------------------------------------------------------------------------------
        response = VLPRootTestUtils.HIDppHelper.get_feature_index(
            self,
            report_id=VlpMessage.DEFAULT.REPORT_ID_NORMAL_VLP_MESSAGE,
            feature_id=VLPRoot.FEATURE_ID,
            vlp_begin=True,
            vlp_end=True,
            vlp_ack=True
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check response is received when ACK = 1")
        # --------------------------------------------------------------------------------------------------------------
        checker = VLPRootTestUtils.GetFeatureIndexResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "feature_index": (checker.check_feature_index, HexList(self.feature_0102_index)),
            "feature_id": (checker.check_feature_id, VLPRoot.FEATURE_ID),
            "feature_idx": (checker.check_feature_idx, HexList(self.feature_0102_index)),
            "feature_version": (checker.check_feature_version, self.feature_0102.VERSION),
            "feature_max_memory": (checker.check_feature_max_memory,
                                   self.f.PRODUCT.FEATURES.VLP.IMPORTANT.ROOT.F_FeatureMaxMemory)
        })
        checker.check_fields(test_case=self,
                             message=response,
                             expected_cls=self.feature_0102.get_feature_index_response_cls,
                             check_map=check_map)

        self.testCaseChecked("FUN_VLP_PROTOCOL_0012", _AUTHOR)
    # end def test_single_packet_ack

    @features("VLP")
    @level("Functionality")
    def test_single_packet_no_ack(self):
        """
         Goal: "The FW replies to every command packet containing ACK == 1 by sending an ACK reply, response,
         or error packet while if ACK == 0, the FW shall not send any response for that packet."
         => Check no response is received when ACK = 0
        """
        _, feature_0102, device_index, _ = VLPRootTestUtils.HIDppHelper.get_vlp_parameters(self)
        feature_0102_report = feature_0102.get_feature_index_cls(
            device_index=device_index,
            software_id=0xF,
            feature_id=VLPRoot.FEATURE_ID,
            vlp_begin=True,
            vlp_end=True,
            vlp_ack=False,
            vlp_sequence_number=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send VLP single packet with ACK = 0")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.send_only(test_case=self, report=feature_0102_report)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check no response is received when ACK = 0")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.VLP_IMPORTANT, timeout=1.0,
                                       class_type=self.feature_0102.get_feature_index_response_cls)

        self.testCaseChecked("FUN_VLP_PROTOCOL_0013", _AUTHOR)
    # end def test_single_packet_no_ack

    @features("VLP")
    @level("Functionality")
    def test_single_packet_hidpp_error_no_ack(self):
        """
        Goal: "In case of errors such as incorrect invalid payload or other (cf. HID++ 2.0 error codes) FW shall
        continue to ACK reply normally (if ACK == 1) until the command transfer is complete and the payload is
        processed. If END == 1 and ACK == 0 no error will be returned" => Check no error is received when END = 1
        and ACK = 0

        See https://jira.logitech.io/browse/LEX-123
        """
        # TODO : Use feature 0x0103 when available
        feature_set_report = VlpMessageRawPayload(
            report_id=LogitechReportId.REPORT_ID_NORMAL_VLP_MESSAGE,
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_0103_index,
            function_index=0x1,
            begin=True,
            end=True,
            ack=False,
            seqn=0,
            payload = HexList("FF")
        )
        VlpProtocolTestUtils.VlpHelper.add_padding(feature_set_report, self.vlp_normal_report_size)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send VLP single packet with ACK = 0")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.send_only(test_case=self, report=feature_set_report)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check no response nor error is received when ACK = 0")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.VLP_IMPORTANT, timeout=1.0,
                                       class_type=VlpMessage)
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.ERROR,
                                       timeout=1.0,
                                       class_type=(Hidpp2ErrorCodes, VlpErrorCodes))

        self.testCaseChecked("FUN_VLP_PROTOCOL_0014", _AUTHOR)
    # end def test_single_packet_hidpp_error_no_ack

    @features("VLP")
    @features("MultiPacket")
    @level("Functionality")
    def test_vlp_multi_packet_ack(self):
        """
        Goal: "The FW replies to every command packet containing ACK == 1 by sending an ACK reply, response,
        or error packet while if ACK == 0, the FW shall not send any response for that packet."
        => Check Ack is received when ACK = 1
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

        self.testCaseChecked("FUN_VLP_PROTOCOL_0015", _AUTHOR)
    # end def test_vlp_multi_packet_ack

    @features("VLP")
    @features("MultiPacket")
    @level("Functionality")
    def test_vlp_multi_packet_no_ack(self):
        """
        Goal: "The FW replies to every command packet containing ACK == 1 by sending an ACK reply, response,
        or error packet while if ACK == 0, the FW shall not send any response for that packet."
        => Check nothing is received when ACK = 0 for all packets
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get multi-packet transfer payload")
        # --------------------------------------------------------------------------------------------------------------
        full_payload = self._get_multi_packet_payload()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        report, remaining_payload = self._get_start_report(full_payload)
        report.ack = False
        for _ in range(len(full_payload) // self.report_payload_size + 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Report Sequence Number = {report.seqn}")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.send_only(self, report=report)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check no ack is received when ACK = 0")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.VLP_IMPORTANT,
                                           timeout=0.5,
                                           class_type=VlpMessage)
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.VLP_COMMON,
                                           timeout=0.5,
                                           class_type=VlpMessage)
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

        self.testCaseChecked("FUN_VLP_PROTOCOL_0016", _AUTHOR)
    # end def test_vlp_multi_packet_no_ack

    @features("VLP")
    @features("MultiPacket")
    @level("Functionality")
    def test_vlp_multi_packet_hidpp_error_no_ack(self):
        """
        Goal: "In case of errors such as incorrect invalid payload or other (cf. HID++ 2.0 error codes)) FW shall
        continue to ACK reply normally (if ACK == 1) until the command transfer is complete and the payload is
        processed. If END == 1 and ACK == 0 no error will be returned" => Check no error is received when END = 1
        and ACK = 0

        See https://jira.logitech.io/browse/LEX-123
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get multi-packet transfer payload")
        # --------------------------------------------------------------------------------------------------------------
        full_payload = self._get_multi_packet_payload()
        full_payload = SetImagePayloadMixin.fromHexList(full_payload)
        full_payload.image_count = 0xF  # imageCount out of range to trigger invalid argument error
        full_payload = HexList(full_payload)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        report, remaining_payload = self._get_start_report(full_payload)
        report.ack = False
        for _ in range(len(full_payload) // self.report_payload_size + 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Report Sequence Number = {report.seqn}")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.send_only(self, report=report)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check no ack is received when ACK = 0")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.VLP_IMPORTANT,
                                           timeout=0.5,
                                           class_type=VlpMessage)
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.VLP_COMMON,
                                           timeout=0.5,
                                           class_type=VlpMessage)
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.ERROR,
                                           timeout=0.5,
                                           class_type=(Hidpp2ErrorCodes, VlpErrorCodes))
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

        self.testCaseChecked("FUN_VLP_PROTOCOL_0017", _AUTHOR)
    # end def test_vlp_multi_packet_hidpp_error_no_ack

    @features("VLP")
    @features("MultiPacket")
    @level("Functionality")
    def test_vlp_multi_packet_hidpp_error_middle_ack_end_no_ack(self):
        """
        Goal: "In case of errors such as incorrect invalid payload or other (cf. HID++ 2.0 error codes)) FW shall
        continue to ACK reply normally (if ACK == 1) until the command transfer is complete and the payload is
        processed. If END == 1 and ACK == 0 no error will be returned" => Check no error is received when END = 1
        and ACK = 0

        See https://jira.logitech.io/browse/LEX-123
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get multi-packet transfer payload")
        # --------------------------------------------------------------------------------------------------------------
        full_payload = self._get_multi_packet_payload()
        full_payload = SetImagePayloadMixin.fromHexList(full_payload)
        full_payload.image_count = 0xF  # imageCount out of range to trigger invalid argument error
        full_payload = HexList(full_payload)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Multi-packet transfer")
        # --------------------------------------------------------------------------------------------------------------
        report, remaining_payload = self._get_start_report(full_payload)
        for _ in range(len(full_payload) // self.report_payload_size + 1):
            if not report.end:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Report Sequence Number = {report.seqn}")
                # ------------------------------------------------------------------------------------------------------
                ack = ChannelUtils.send(self, report=report, response_queue_name=HIDDispatcher.QueueName.VLP_COMMON)
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check ACK message")
                # ------------------------------------------------------------------------------------------------------
                VlpProtocolTestUtils.check_ack_message(self, report, ack)
                report, remaining_payload = VlpProtocolTestUtils.VlpHelper.get_next_report(
                    report, remaining_payload, self.report_payload_size)
            else:
                report.ack = False
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Report Sequence Number = {report.seqn}")
                # ------------------------------------------------------------------------------------------------------
                ChannelUtils.send_only(self, report=report)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check no ack is received when ACK = 0")
                # ------------------------------------------------------------------------------------------------------
                ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.VLP_IMPORTANT,
                                               timeout=0.5,
                                               class_type=VlpMessage)
                ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.VLP_COMMON,
                                               timeout=0.5,
                                               class_type=VlpMessage)
                ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.ERROR,
                                               timeout=0.5,
                                               class_type=(Hidpp2ErrorCodes, VlpErrorCodes))
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "End multi-packet transfer")
                # ------------------------------------------------------------------------------------------------------
                break
            # end if
        else:
            self.fail("Multi-packet transfer end was not reached")
        # end for

        self.testCaseChecked("FUN_VLP_PROTOCOL_0018", _AUTHOR)
    # end def test_vlp_multi_packet_hidpp_error_middle_ack_end_no_ack
# end class VlpProtocolFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
