#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.base.rftestutils
:brief: Helpers for ``RFTest`` feature
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/05/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.rftest import RFTest
from pyhid.hidpp.features.common.rftest import RFTestFactory
from pyhid.hidpp.features.common.rftest import RFSendPeriodicFullDutyMsgResponseV9
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int, Numeral
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class RFTestTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``RFTest`` feature
    """

    class RFSendPeriodicMsgResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``RFSendPeriodicMsgResponseV0ToV8``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "nb_msg_ack": (
                    cls.check_nb_msg_ack,
                    None)
            }
        # end def get_default_check_map

        @staticmethod
        def check_nb_msg_ack(test_case, response, expected):
            """
            Check nb_msg_ack field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: RFSendPeriodicMsgResponse to check
            :type response: ``pyhid.hidpp.features.common.rftest.RFSendPeriodicMsgResponseV0ToV8``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="NbMsgAck shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.nb_msg_ack),
                msg=f"The nb_msg_ack parameter differs "
                    f"(expected:{expected}, obtained:{response.nb_msg_ack})")
        # end def check_nb_msg_ack
    # end class RFSendPeriodicMsgResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=RFTest.FEATURE_ID, factory=RFTestFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def rf_send_periodic_msg(cls, test_case, address, channel=0, power=6, period=0, condition=0, nbmsg=0,
                                 radio_mode=0, payload_size=11, device_index=None, port_index=None, send_only=False):
            """
            Process ``RFSendPeriodicMsg``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param address: eQuad base and destination addresses.
            :type address: ``int`` or ``HexList``
            :param channel: RF test channel
            :type channel: ``int`` or ``HexList``
            :param power: output power
            :type power: ``int`` or ``HexList``
            :param period: 1ms per unit MSB first
            :type period: ``int`` or ``HexList``
            :param condition: Device dependent test condition
            :type condition: ``int`` or ``HexList``
            :param nbmsg: Number of message to be sent, 0xFFFF means infinite
            :type nbmsg: ``int`` or ``HexList``
            :param radio_mode: Radio Mode
            :type radio_mode: ``int`` or ``HexList``
            :param payload_size: ESB pay-load size
            :type payload_size: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``
            :param send_only: Flag indicating if we shall wait for a response (``False`` which is the default behavior)
                              or skip this operation (``True``) - OPTIONAL
            :type send_only: ``bool``

            :return: RFSendPeriodicMsgResponse
            :rtype: ``pyhid.hidpp.features.common.rftest.RFSendPeriodicMsgResponseV0ToV8`` or ``None``
            """
            feature_1890_index, feature_1890, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1890.rf_send_periodic_msg_cls(
                device_index=device_index,
                feature_index=feature_1890_index,
                address=HexList(address),
                channel=HexList(channel),
                power=HexList(power),
                period=HexList(period),
                condition=HexList(condition),
                nbmsg=HexList(Numeral(nbmsg, feature_1890.rf_send_periodic_msg_cls.LEN.NBMSG // 8)),
                radio_mode=HexList(radio_mode),
                payload_size=HexList(payload_size))
            if send_only:
                ChannelUtils.send_only(
                    test_case=test_case,
                    report=report)
                response = None
            else:
                response = ChannelUtils.send(
                    test_case=test_case,
                    report=report,
                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                    response_class_type=feature_1890.rf_send_periodic_msg_response_cls)
            # end if
            return response
        # end def rf_send_periodic_msg

        @classmethod
        def rf_tx_cw(cls, test_case, channel=0, power=6, timeout=0, condition=0, radio_mode=0, device_index=None,
                     port_index=None, send_only=False):
            """
            Process ``RFTxCW``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param channel: RF test channel - OPTIONAL
            :type channel: ``int`` or ``HexList``
            :param power: output power - OPTIONAL
            :type power: ``int`` or ``HexList``
            :param timeout: 10ms per unit - OPTIONAL
            :type timeout: ``int`` or ``HexList``
            :param condition: Device dependent test condition - OPTIONAL
            :type condition: ``int`` or ``HexList``
            :param radio_mode: Radio Mode - OPTIONAL
            :type radio_mode: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``
            :param send_only: Flag indicating if we shall wait for a response (``False`` which is the default behavior)
                              or skip this operation (``True``) - OPTIONAL
            :type send_only: ``bool``

            :return: RFTxCWResponse
            :rtype: ``pyhid.hidpp.features.common.rftest.RFTxCWResponseV0ToV8`` or ``None``
            """
            feature_1890_index, feature_1890, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1890.rf_tx_cw_cls(
                device_index=device_index,
                feature_index=feature_1890_index,
                channel=HexList(channel),
                power=HexList(power),
                timeout=HexList(Numeral(timeout, 2)),
                condition=HexList(condition),
                radio_mode=HexList(radio_mode))
            if send_only:
                ChannelUtils.send_only(
                    test_case=test_case,
                    report=report)
                response = None
            else:
                response = ChannelUtils.send(
                    test_case=test_case,
                    report=report,
                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                    response_class_type=feature_1890.rf_tx_cw_response_cls)
            # end if
            return response
        # end def rf_tx_cw

        @classmethod
        def rf_rx_continuous(cls, test_case, channel, power, timeout, condition, radio_mode, device_index=None,
                             port_index=None, send_only=False):
            """
            Process ``RFRxContinuous``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param channel: Channel
            :type channel: ``int`` or ``HexList``
            :param power: Power
            :type power: ``int`` or ``HexList``
            :param timeout: Timeout
            :type timeout: ``int`` or ``HexList``
            :param condition: Condition
            :type condition: ``int`` or ``HexList``
            :param radio_mode: Radio Mode
            :type radio_mode: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``
            :param send_only: Flag indicating if we shall wait for a response (``False`` which is the default behavior)
                              or skip this operation (``True``) - OPTIONAL
            :type send_only: ``bool``

            :return: RFRxContinuousResponse
            :rtype: ``pyhid.hidpp.features.common.rftest.RFRxContinuousResponseV0ToV8`` or ``None``
            """
            feature_1890_index, feature_1890, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1890.rf_rx_continuous_cls(
                device_index=device_index,
                feature_index=feature_1890_index,
                channel=HexList(channel),
                power=HexList(power),
                timeout=HexList(timeout),
                condition=HexList(condition),
                radio_mode=HexList(radio_mode))
            if send_only:
                ChannelUtils.send_only(
                    test_case=test_case,
                    report=report)
                response = None
            else:
                response = ChannelUtils.send(
                    test_case=test_case,
                    report=report,
                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                    response_class_type=feature_1890.rf_rx_continuous_response_cls)
            # end if
            return response
        # end def rf_rx_continuous

        @classmethod
        def set_rf_tx_cw_sweep(cls, test_case, channel_min, channel_max, power, sweep_period, condition, radio_mode,
                               nb_sweep, device_index=None, port_index=None, send_only=False):
            """
            Process ``SetRfTxCWSweep``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param channel_min: minimum channel
            :type channel_min: ``int`` or ``HexList``
            :param channel_max: maximum channel
            :type channel_max: ``int`` or ``HexList``
            :param power: output power
            :type power: ``int`` or ``HexList``
            :param sweep_period: 10ms per unit
            :type sweep_period: ``int`` or ``HexList``
            :param condition: Device dependent test condition
            :type condition: ``int`` or ``HexList``
            :param radio_mode: Radio Mode
            :type radio_mode: ``int`` or ``HexList``
            :param nb_sweep: Number of full sweeps to be executed
            :type nb_sweep: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``
            :param send_only: Flag indicating if we shall wait for a response (``False`` which is the default behavior)
                              or skip this operation (``True``) - OPTIONAL
            :type send_only: ``bool``

            :return: SetRfTxCWSweepResponse
            :rtype: ``pyhid.hidpp.features.common.rftest.SetRfTxCWSweepResponseV0ToV8`` or ``None``
            """
            feature_1890_index, feature_1890, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1890.set_rf_tx_cw_sweep_cls(
                device_index=device_index,
                feature_index=feature_1890_index,
                channel_min=HexList(channel_min),
                channel_max=HexList(channel_max),
                power=HexList(power),
                sweep_period=HexList(sweep_period),
                condition=HexList(condition),
                radio_mode=HexList(radio_mode),
                nb_sweep=HexList(nb_sweep))
            if send_only:
                ChannelUtils.send_only(
                    test_case=test_case,
                    report=report)
                response = None
            else:
                response = ChannelUtils.send(
                    test_case=test_case,
                    report=report,
                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                    response_class_type=feature_1890.set_rf_tx_cw_sweep_response_cls)
            # end if
            return response
        # end def set_rf_tx_cw_sweep

        @classmethod
        def set_rf_rx_continuous_sweep(cls, test_case, channel_min, channel_max, power, sweep_period, condition,
                                       radio_mode, nb_sweep, device_index=None, port_index=None, send_only=False):
            """
            Process ``SetRfRxContinuousSweep``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param channel_min: Channel Min
            :type channel_min: ``int`` or ``HexList``
            :param channel_max: Channel Max
            :type channel_max: ``int`` or ``HexList``
            :param power: Power
            :type power: ``int`` or ``HexList``
            :param sweep_period: Sweep Period
            :type sweep_period: ``int`` or ``HexList``
            :param condition: Condition
            :type condition: ``int`` or ``HexList``
            :param radio_mode: Radio Mode
            :type radio_mode: ``int`` or ``HexList``
            :param nb_sweep: Nb Sweep
            :type nb_sweep: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``
            :param send_only: Flag indicating if we shall wait for a response (``False`` which is the default behavior)
                              or skip this operation (``True``) - OPTIONAL
            :type send_only: ``bool``

            :return: SetRfRxContinuousSweepResponse
            :rtype: ``pyhid.hidpp.features.common.rftest.SetRfRxContinuousSweepResponseV0ToV8`` or ``None``
            """
            feature_1890_index, feature_1890, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1890.set_rf_rx_continuous_sweep_cls(
                device_index=device_index,
                feature_index=feature_1890_index,
                channel_min=HexList(channel_min),
                channel_max=HexList(channel_max),
                power=HexList(power),
                sweep_period=HexList(sweep_period),
                condition=HexList(condition),
                radio_mode=HexList(radio_mode),
                nb_sweep=HexList(nb_sweep))
            if send_only:
                ChannelUtils.send_only(
                    test_case=test_case,
                    report=report)
                response = None
            else:
                response = ChannelUtils.send(
                    test_case=test_case,
                    report=report,
                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                    response_class_type=feature_1890.set_rf_rx_continuous_sweep_response_cls)
            # end if
            return response
        # end def set_rf_rx_continuous_sweep

        @classmethod
        def rf_send_periodic_msg_no_ack(cls, test_case, address, channel=0, power=6, period=0, condition=0, nbmsg=0,
                                        radio_mode=0, payload_size=0, device_index=None, port_index=None,
                                        send_only=False):
            """
            Process ``RFSendPeriodicMsgNoAck``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param address: Address
            :type address: ``int`` or ``HexList``
            :param channel: Channel
            :type channel: ``int`` or ``HexList``
            :param power: Power
            :type power: ``int`` or ``HexList``
            :param period: Period
            :type period: ``int`` or ``HexList``
            :param condition: Condition
            :type condition: ``int`` or ``HexList``
            :param nbmsg: NbMsg
            :type nbmsg: ``int`` or ``HexList``
            :param radio_mode: Radio Mode
            :type radio_mode: ``int`` or ``HexList``
            :param payload_size: Payload Size
            :type payload_size: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``
            :param send_only: Flag indicating if we shall wait for a response (``False`` which is the default behavior)
                              or skip this operation (``True``) - OPTIONAL
            :type send_only: ``bool``

            :return: RFSendPeriodicMsgNoAckResponse
            :rtype: ``pyhid.hidpp.features.common.rftest.RFSendPeriodicMsgNoAckResponseV1ToV8`` or ``None``
            """
            feature_1890_index, feature_1890, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1890.rf_send_periodic_msg_no_ack_cls(
                device_index=device_index,
                feature_index=feature_1890_index,
                address=HexList(address),
                channel=HexList(channel),
                power=HexList(power),
                period=HexList(period),
                condition=HexList(condition),
                nbmsg=HexList(Numeral(nbmsg, feature_1890.rf_send_periodic_msg_no_ack_cls.LEN.NBMSG // 8)),
                radio_mode=HexList(radio_mode),
                payload_size=HexList(payload_size))
            if send_only:
                ChannelUtils.send_only(
                    test_case=test_case,
                    report=report)
                response = None
            else:
                response = ChannelUtils.send(
                    test_case=test_case,
                    report=report,
                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                    response_class_type=feature_1890.rf_send_periodic_msg_no_ack_response_cls)
            # end if
            return response
        # end def rf_send_periodic_msg_no_ack

        @classmethod
        def rf_receive_periodic_msg(cls, test_case, address, channel, power, condition, timeout, radio_mode,
                                    device_index=None, port_index=None, send_only=False):
            """
            Process ``RFReceivePeriodicMsg``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param address: eQuad base and destination addresses.
            :type address: ``int`` or ``HexList``
            :param channel: RF test channel
            :type channel: ``int`` or ``HexList``
            :param power: output power
            :type power: ``int`` or ``HexList``
            :param condition: Device dependent test condition
            :type condition: ``int`` or ``HexList``
            :param timeout: 10ms per unit
            :type timeout: ``int`` or ``HexList``
            :param radio_mode: Radio Mode
            :type radio_mode: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``
            :param send_only: Flag indicating if we shall wait for a response (``False`` which is the default behavior)
                              or skip this operation (``True``) - OPTIONAL
            :type send_only: ``bool``

            :return: RFReceivePeriodicMsgResponse
            :rtype: ``pyhid.hidpp.features.common.rftest.RFReceivePeriodicMsgResponseV2ToV8`` or ``None``
            """
            feature_1890_index, feature_1890, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1890.rf_receive_periodic_msg_cls(
                device_index=device_index,
                feature_index=feature_1890_index,
                address=HexList(address),
                channel=HexList(channel),
                power=HexList(power),
                condition=HexList(condition),
                timeout=HexList(timeout),
                radio_mode=HexList(radio_mode))
            if send_only:
                ChannelUtils.send_only(
                    test_case=test_case,
                    report=report)
                response = None
            else:
                response = ChannelUtils.send(
                    test_case=test_case,
                    report=report,
                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                    response_class_type=feature_1890.rf_receive_periodic_msg_response_cls)
            # end if
            return response
        # end def rf_receive_periodic_msg

        @classmethod
        def rf_send_periodic_full_duty_msg(cls, test_case, channel, power, timeout, condition, radio_mode,
                                           device_index=None, port_index=None, send_only=False):
            """
            Process ``RFSendPeriodicFullDutyMsg``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param channel: RF test channel
            :type channel: ``int`` or ``HexList``
            :param power: output power
            :type power: ``int`` or ``HexList``
            :param timeout: 10ms per unit
            :type timeout: ``int`` or ``HexList``
            :param condition: Device dependent test condition
            :type condition: ``int`` or ``HexList``
            :param radio_mode: Radio Mode
            :type radio_mode: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``
            :param send_only: Flag indicating if we shall wait for a response (``False`` which is the default behavior)
                              or skip this operation (``True``) - OPTIONAL
            :type send_only: ``bool``

            :return: RFSendPeriodicFullDutyMsgResponse
            :rtype: ``RFSendPeriodicFullDutyMsgResponseV9`` or ``None``
            """
            feature_1890_index, feature_1890, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1890.rf_send_periodic_full_duty_msg_cls(
                device_index=device_index,
                feature_index=feature_1890_index,
                channel=HexList(channel),
                power=HexList(power),
                timeout=HexList(timeout),
                condition=HexList(condition),
                radio_mode=HexList(radio_mode))
            if send_only:
                ChannelUtils.send_only(
                    test_case=test_case,
                    report=report)
                response = None
            else:
                response = ChannelUtils.send(
                    test_case=test_case,
                    report=report,
                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                    response_class_type=feature_1890.rf_send_periodic_full_duty_msg_response_cls)
            # end if
            return response
        # end def rf_send_periodic_full_duty_msg
    # end class HIDppHelper
# end class RFTestTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
