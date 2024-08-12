#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.vlp.protocol.vlpprotocoltestutils
:brief: Helpers for VLP protocol
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2023/11/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pyhid.bitfield import BitField
from pyhid.hid.interfacedescriptors import VlpInterfaceDescriptor
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.vlp.vlpmessage import VlpMessage
from pyhid.vlp.vlpmessage import VlpMessageHeader
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class VlpProtocolTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on VLP Protocol
    """

    @staticmethod
    def get_report_count_vlp_normal(test_case, channel=None):
        """
        Get VLP Normal report size (including payload and report id)

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param channel: Channel - OPTIONAL
        :type channel: ``BaseCommunicationChannel`` or ``None``

        :return: Report count in VLP Normal descriptor
        :rtype: ``int``
        """
        channel = channel if channel is not None else test_case.current_channel
        descriptors = channel.get_descriptors()
        vlp_interface_descriptors = [descriptor for descriptor in descriptors
                                     if isinstance(descriptor, VlpInterfaceDescriptor)]
        assert len(vlp_interface_descriptors) == 1, "1 VLP interface should be found for the channel"
        vlp_interface_descriptor = vlp_interface_descriptors[0]
        report_count = to_int(vlp_interface_descriptor.vlp1_normal_report_count[1:], little_endian=True)
        return report_count
    # end def get_report_count_vlp_normal

    @staticmethod
    def get_report_count_vlp_extended(test_case, channel=None):
        """
        Get VLP Extended report size (including payload and report id)

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param channel: Channel - OPTIONAL
        :type channel: ``BaseCommunicationChannel`` or ``None``

        :return: Report count in VLP E descriptor
        :rtype: ``int``
        """
        channel = channel if channel is not None else test_case.current_channel
        descriptors = channel.get_descriptors()
        vlp_interface_descriptors = [descriptor for descriptor in descriptors
                                     if isinstance(descriptor, VlpInterfaceDescriptor)]
        assert len(vlp_interface_descriptors) == 1, "1 VLP interface should be found for the channel"
        vlp_interface_descriptor = vlp_interface_descriptors[0]
        report_count = to_int(vlp_interface_descriptor.vlp1_extended_report_count[1:], little_endian=True)
        return report_count
    # end def get_report_count_vlp_extended

    @classmethod
    def check_ack_message(cls, test_case, request, ack_msg):
        """
        Check ack message received after a request

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param request: Sent request
        :type request: ``VlpMessage``
        :param ack_msg: Received request
        :type ack_msg: ``VlpMessage``
        """
        ack_msg_header = VlpMessageHeader.fromHexList(HexList(ack_msg))
        check_map = cls.VlpMessageChecker.get_default_check_map(test_case)
        check_map.update({
            "ack": (cls.VlpMessageChecker.check_ack, False),
            "seqn": (cls.VlpMessageChecker.check_seqn, request.seqn),
        })
        cls.VlpMessageChecker.check_fields(test_case, ack_msg_header, VlpMessageHeader, check_map)
    # end check_ack_message

    class VlpHelper:
        """
        VLP Helper class
        """

        @staticmethod
        def add_padding(report, final_report_size):
            """
            Add padding to a report. The most common usage is to fill the size declared in the HID descriptor.
            See also: https://jira.logitech.io/browse/LEX-120

            :param report: The report to pad
            :type report: ``VlpMessage``
            :param final_report_size: The size of the resulting report with padding
            :type final_report_size: ``int``
            """
            padding_size = final_report_size - len(report)
            padding_field = BitField(
                fid=report.FIELDS[-1].fid - 1,
                length=padding_size * 8,
                title='Padding',
                name='padding',
                default_value=HexList("00" * padding_size),
            ),
            report.FIELDS += padding_field
        # end def add_padding

        @staticmethod
        def get_next_report(previous_report, remaining_payload, report_payload_size, report_type=None,
                            device_index=None, feature_index=None, ack=None, seqn=None):
            """
            Get next report following the given report

            :param previous_report: Previous report
            :type previous_report: ``VlpMessage`` or ``None``
            :param remaining_payload: Remaining payload to send
            :type remaining_payload: ``HexList``
            :param report_payload_size: Report payload size
            :type report_payload_size: ``int``
            :param report_type: Report type, inherited from ``VlpMessageRawPayload`` - OPTIONAL
            :type report_type: ``type``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int|HexList``
            :param feature_index: Feature index - OPTIONAL
            :type feature_index: ``int|HexList``
            :param ack: Ack - OPTIONAL
            :type ack: ``bool|int``
            :param seqn: Sequence number - OPTIONAL
            :type seqn: ``int``

            :return: The next report and the remaining payload
            :rtype: ``tuple[VlpMessage|HexList]``
            """
            if previous_report is None:
                begin = True
            else:
                report_type = type(previous_report) if report_type is None else report_type
                device_index = previous_report.device_index if device_index is None else device_index
                feature_index = previous_report.feature_index if feature_index is None else feature_index
                begin = False
                ack = previous_report.ack if ack is None else ack
                seqn = (previous_report.seqn + 1) % pow(2, VlpMessage.LEN.VLP_SEQUENCE_NUMBER) if seqn is None else seqn
            # end if

            if report_payload_size >= len(remaining_payload):
                # No more data, end transfer
                end = True
                payload = remaining_payload
                payload.addPadding(size=report_payload_size, pattern="00", fromLeft=False)
            else:
                # Continue transfer
                end = False
                payload = remaining_payload[:report_payload_size]
            # end if

            remaining_payload = remaining_payload[report_payload_size:]

            next_report = report_type(
                device_index=device_index,
                feature_index=feature_index,
                begin=begin,
                end=end,
                ack=ack,
                seqn=seqn,
                vlp_payload=payload
            )

            return next_report, remaining_payload
        # end def get_next_report

        @classmethod
        def vlp_transfer(cls, test_case, payload, report_payload_size, report_type=None, device_index=None,
                         feature_index=None, ack=True, start_seqn=None, channel=None,
                         response_queue_name=HIDDispatcher.QueueName.VLP_COMMON):
            """
            Generic method to send VLP transfer (automatically decide if multi-packet is required)

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param payload: Payload to send
            :type payload: ``HexList``
            :param report_payload_size: Report payload size
            :type report_payload_size: ``int``
            :param report_type: Report type, inherited from ``VlpMessageRawPayload`` - OPTIONAL
            :type report_type: ``type``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int|HexList``
            :param feature_index: Feature index - OPTIONAL
            :type feature_index: ``int|HexList``
            :param ack: Ack - OPTIONAL
            :type ack: ``bool|int``
            :param start_seqn: Initial sequence number - OPTIONAL
            :type start_seqn: ``int``
            :param channel: Channel - OPTIONAL
            :type channel: ``BaseCommunicationChannel`` or ``None``
            :param response_queue_name: Queue name to get responses
            :type response_queue_name: ``str``

            :return: List of Ack messages
            :rtype: ``tuple[VlpMessage|HexList]``
            """
            ack_msg = []

            report, remaining_payload = cls.get_next_report(
                previous_report=None,
                remaining_payload=payload,
                report_payload_size=report_payload_size,
                report_type=report_type,
                device_index=device_index if device_index is not None else ChannelUtils.get_device_index(
                    test_case=test_case, channel=channel),
                feature_index=feature_index,
                ack=ack,
                seqn=start_seqn
            )
            for _ in range(len(payload) // report_payload_size + 1):
                if ack:
                    message = ChannelUtils.send(
                        test_case=test_case, report=report,
                        response_queue_name=response_queue_name, channel=channel)
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(test_case, "Check ACK message")
                    # --------------------------------------------------------------------------------------------------
                    VlpProtocolTestUtils.check_ack_message(test_case, report, message)
                    ack_msg.append(message)
                else:
                    ChannelUtils.send_only(test_case=test_case, report=report, channel=channel)
                # end if
                if not report.end:
                    report, remaining_payload = VlpProtocolTestUtils.VlpHelper.get_next_report(
                        report, remaining_payload, report_payload_size)
                else:
                    break
                # end if
            else:
                test_case.fail("Multi-packet transfer end was not reached")
            # end for
            return ack_msg
        # end def vlp_transfer

        @classmethod
        def send(cls, test_case, report, response_queue_name, channel=None,
                 send_timeout=BaseCommunicationChannel.GENERIC_SEND_TIMEOUT,
                 get_timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT, response_class_type=None,
                 skip_error_message=False):
            """
            Send VLP request and get multi-packet response

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param report: The report to send
            :type report: ``TimestampedBitFieldContainerMixin``
            :param response_queue_name: The queue name (names can be found in ``HIDDispatcher.QueueName``)
            :type response_queue_name: ``str``
            :param channel: The channel to use. If ``None``, ``test_case.current_channel`` is used - OPTIONAL
            :type channel: ``BaseCommunicationChannel`` or ``None``
            :param send_timeout: The timeout of the send action in seconds (0 disable it) - OPTIONAL
            :type send_timeout: ``float``
            :param get_timeout: The timeout of the received action in seconds (0 disable it) - OPTIONAL
            :type get_timeout: ``float``
            :param response_class_type: The type of expected message. If ``None``, the type is not checked - OPTIONAL
            :type response_class_type: ``type`` or ``tuple[type]`` or ``None``
            :param skip_error_message: Flag indicating if the automatic error catching mechanism should be skipped or
                                       not. This will be always True if the queue is hid_message_queue (HID++ error message
                                       are not important to HID messages) - OPTIONAL
            :type skip_error_message: ``bool``

            :return: The message get from the queue
            :rtype: ``response_class_type``
            """
            responses = []
            response = ChannelUtils.send(test_case=test_case,
                                         report=report,
                                         response_queue_name=response_queue_name,
                                         channel=channel,
                                         send_timeout=send_timeout,
                                         get_timeout=get_timeout,
                                         response_class_type=response_class_type,
                                         skip_error_message=skip_error_message)
            responses.append(response)
            while not response.end:
                response = ChannelUtils.get_only(test_case=test_case,
                                                 channel=channel,
                                                 queue_name=response_queue_name,
                                                 class_type=response_class_type,
                                                 timeout=get_timeout,
                                                 skip_error_message=skip_error_message)
                responses.append(response)
            # end while
            return responses
        # end def send

        @staticmethod
        def get_parsed_multi_packet_payload(vlp_messages, payload_parsing_class):
            """
            Get parsed payload of VLP multi-packet transfer

            :param vlp_messages: VLP messages
            :type vlp_messages: ``list[VlpMessageRawPayload]``
            :param payload_parsing_class: Class to parse the full payload
            :type payload_parsing_class: ``BitFieldContainerMixin``

            :return: Parsed payload
            :rtype: ``BitFieldContainerMixin``
            """
            payload = HexList()
            for vlp_message in vlp_messages:
                payload += vlp_message.payload
            # end for
            return payload_parsing_class.fromHexList(payload)
        # end def get_parsed_multi_packet_payload
    # end class VlpHelper

    class VlpMessageChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Help to check VLP message
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            # See ``DeviceBaseTestUtils.MessageChecker.get_default_check_map``
            return {
                "begin": (cls.check_begin, True),
                "end": (cls.check_end, True),
                "ack": (cls.check_ack, True),
                "seqn": (cls.check_seqn, 0),
            }
        # end def get_default_check_map

        @staticmethod
        def check_begin(test_case, message, expected):
            """
            Check begin flag

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: VLP Message to check
            :type message: ``VlpMessage``
            :param expected: Expected value
            :type expected: ``int|HexList|bool``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(message.begin),
                msg="The BEGIN parameter differs from the one expected")
        # end def check_begin

        @staticmethod
        def check_end(test_case, message, expected):
            """
            Check end flag

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: VLP Message to check
            :type message: ``VlpMessage``
            :param expected: Expected value
            :type expected: ``int|HexList|bool``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(message.end),
                msg="The END parameter differs from the one expected")
        # end def check_end

        @staticmethod
        def check_ack(test_case, message, expected):
            """
            Check ack flag

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: VLP Message to check
            :type message: ``VlpMessage``
            :param expected: Expected value
            :type expected: ``int|HexList|bool``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(message.ack),
                msg="The ACK parameter differs from the one expected")
        # end def check_ack

        @staticmethod
        def check_seqn(test_case, message, expected):
            """
            Check sequence number

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: VLP Message to check
            :type message: ``VlpMessage``
            :param expected: Expected value
            :type expected: ``int|HexList|bool``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(message.seqn),
                msg="The SEQN parameter differs from the one expected")
        # end def check_seqn
    # end class AckChecker
# end class VlpProtocolTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
