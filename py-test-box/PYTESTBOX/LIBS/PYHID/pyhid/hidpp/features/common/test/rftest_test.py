#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
""" @package pyhid.hidpp.feature.common.test.rftest_test

@brief  HID++ 2.0 rf test test module

@author Jerry Lin

@date   2020/04/21
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hidpp.features.common.rftest import RFReceivePeriodicMsgResponseV2ToV9
from pyhid.hidpp.features.common.rftest import RFReceivePeriodicMsgV2
from pyhid.hidpp.features.common.rftest import RFReceivePeriodicMsgV3ToV9
from pyhid.hidpp.features.common.rftest import RFRxContinuousResponseV0ToV9
from pyhid.hidpp.features.common.rftest import RFRxContinuousV0ToV5
from pyhid.hidpp.features.common.rftest import RFRxContinuousV6ToV9
from pyhid.hidpp.features.common.rftest import RFSendPeriodicFullDutyMsgResponseV9
from pyhid.hidpp.features.common.rftest import RFSendPeriodicFullDutyMsgV9
from pyhid.hidpp.features.common.rftest import RFSendPeriodicMsgNoAckResponseV1ToV9
from pyhid.hidpp.features.common.rftest import RFSendPeriodicMsgNoAckV1ToV2
from pyhid.hidpp.features.common.rftest import RFSendPeriodicMsgNoAckV3ToV5
from pyhid.hidpp.features.common.rftest import RFSendPeriodicMsgNoAckV6ToV9
from pyhid.hidpp.features.common.rftest import RFSendPeriodicMsgResponseV0ToV9
from pyhid.hidpp.features.common.rftest import RFSendPeriodicMsgV0ToV2
from pyhid.hidpp.features.common.rftest import RFSendPeriodicMsgV3ToV5
from pyhid.hidpp.features.common.rftest import RFSendPeriodicMsgV6ToV9
from pyhid.hidpp.features.common.rftest import RFTest
from pyhid.hidpp.features.common.rftest import RFTestFactory
from pyhid.hidpp.features.common.rftest import RFTestV0
from pyhid.hidpp.features.common.rftest import RFTestV1
from pyhid.hidpp.features.common.rftest import RFTestV2
from pyhid.hidpp.features.common.rftest import RFTestV3
from pyhid.hidpp.features.common.rftest import RFTestV4
from pyhid.hidpp.features.common.rftest import RFTestV5
from pyhid.hidpp.features.common.rftest import RFTestV6
from pyhid.hidpp.features.common.rftest import RFTestV7
from pyhid.hidpp.features.common.rftest import RFTestV8
from pyhid.hidpp.features.common.rftest import RFTestV9
from pyhid.hidpp.features.common.rftest import RFTxCWResponseV0ToV9
from pyhid.hidpp.features.common.rftest import RFTxCWV0ToV5
from pyhid.hidpp.features.common.rftest import RFTxCWV6ToV9
from pyhid.hidpp.features.common.rftest import SetRfRxContinuousSweepResponseV0ToV9
from pyhid.hidpp.features.common.rftest import SetRfRxContinuousSweepV0ToV5
from pyhid.hidpp.features.common.rftest import SetRfRxContinuousSweepV6
from pyhid.hidpp.features.common.rftest import SetRfRxContinuousSweepV7ToV9
from pyhid.hidpp.features.common.rftest import SetRfTxCWSweepResponseV0ToV9
from pyhid.hidpp.features.common.rftest import SetRfTxCWSweepV0ToV5
from pyhid.hidpp.features.common.rftest import SetRfTxCWSweepV6
from pyhid.hidpp.features.common.rftest import SetRfTxCWSweepV7ToV9
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList
from unittest import TestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class RFTestInstantiationTestCase(TestCase):
    """
    DeviceInformation testing classes instantiations
    """

    @staticmethod
    def test_rf_test():
        """
        Tests DeviceInformation class instantiation
        """
        my_class = RFTest(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = RFTest(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_rf_test

    @staticmethod
    def test_rf_send_periodic_msg_v0_to_v2():
        """
        Tests RFSendPeriodicMsgV0ToV2 class instantiation
        """
        my_class = RFSendPeriodicMsgV0ToV2(device_index=0,
                                           feature_index=0,
                                           address=HexList('00' * (
                                                   RFSendPeriodicMsgV0ToV2.LEN.ADDRESS // 8)),
                                           channel=0,
                                           power=0,
                                           period=0,
                                           condition=0,
                                           nbmsg=HexList('00' * (
                                                 RFSendPeriodicMsgV0ToV2.LEN.NBMSG // 8)),)

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFSendPeriodicMsgV0ToV2(device_index=0xFF,
                                           feature_index=0xFF,
                                           address=HexList('FF' * (
                                                   RFSendPeriodicMsgV0ToV2.LEN.ADDRESS // 8)),
                                           channel=0xFF,
                                           power=0xFF,
                                           period=0xFF,
                                           condition=0xFF,
                                           nbmsg=HexList('FF' * (
                                                   RFSendPeriodicMsgV0ToV2.LEN.NBMSG // 8)),)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_send_periodic_msg_v0_to_v2

    @staticmethod
    def test_rf_send_periodic_msg_v3_to_v5():
        """
        Tests RFSendPeriodicMsgV3ToV5 class instantiation
        """
        my_class = RFSendPeriodicMsgV3ToV5(device_index=0,
                                           feature_index=0,
                                           address=HexList('00' * (
                                                   RFSendPeriodicMsgV3ToV5.LEN.ADDRESS // 8)),
                                           channel=0,
                                           power=0,
                                           period=0,
                                           condition=0,
                                           nbmsg=HexList('00' * (
                                                   RFSendPeriodicMsgV3ToV5.LEN.NBMSG // 8)),
                                           radio_mode=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFSendPeriodicMsgV3ToV5(device_index=0xFF,
                                           feature_index=0xFF,
                                           address=HexList('FF' * (
                                                   RFSendPeriodicMsgV3ToV5.LEN.ADDRESS // 8)),
                                           channel=0xFF,
                                           power=0xFF,
                                           period=0xFF,
                                           condition=0xFF,
                                           nbmsg=HexList('FF' * (
                                                   RFSendPeriodicMsgV3ToV5.LEN.NBMSG // 8)),
                                           radio_mode=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_send_periodic_msg_v3_to_v5

    @staticmethod
    def test_rf_send_periodic_msg_v6_to_v9():
        """
        Tests RFSendPeriodicMsgV6ToV9 class instantiation
        """
        my_class = RFSendPeriodicMsgV6ToV9(device_index=0,
                                           feature_index=0,
                                           address=HexList('00' * (
                                                   RFSendPeriodicMsgV6ToV9.LEN.ADDRESS // 8)),
                                           channel=0,
                                           power=0,
                                           period=0,
                                           condition=0,
                                           nbmsg=HexList('00' * (
                                                   RFSendPeriodicMsgV6ToV9.LEN.NBMSG // 8)),
                                           radio_mode=0,
                                           payload_size=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFSendPeriodicMsgV6ToV9(device_index=0xFF,
                                           feature_index=0xFF,
                                           address=HexList('FF' * (
                                                   RFSendPeriodicMsgV6ToV9.LEN.ADDRESS // 8)),
                                           channel=0xFF,
                                           power=0xFF,
                                           period=0xFF,
                                           condition=0xFF,
                                           nbmsg=HexList('FF' * (
                                                   RFSendPeriodicMsgV6ToV9.LEN.NBMSG // 8)),
                                           radio_mode=0xFF,
                                           payload_size=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_send_periodic_msg_v6_to_v9

    @staticmethod
    def test_rf_send_periodic_msg_response_v0_to_v9():
        """
        Tests RFSendPeriodicMsgResponseV0ToV9 class instantiation
        """
        my_class = RFSendPeriodicMsgResponseV0ToV9(device_index=0,
                                                   feature_index=0,
                                                   nb_msg_ack=HexList('00' * (
                                                              RFSendPeriodicMsgResponseV0ToV9.LEN.NB_MSG_ACK // 8)))

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFSendPeriodicMsgResponseV0ToV9(device_index=0xFF,
                                                   feature_index=0xFF,
                                                   nb_msg_ack=HexList('FF' * (
                                                              RFSendPeriodicMsgResponseV0ToV9.LEN.NB_MSG_ACK // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_send_periodic_msg_response_v0_to_v9

    @staticmethod
    def test_rf_tx_cw_v0_to_v5():
        """
        Tests RFTxCWV0ToV5 class instantiation
        """
        my_class = RFTxCWV0ToV5(
            device_index=0,
            feature_index=0,
            channel=0,
            power=0,
            timeout=HexList('00' * (RFTxCWV0ToV5.LEN.TIMEOUT // 8)))

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFTxCWV0ToV5(
            device_index=0xFF,
            feature_index=0xFF,
            channel=0xFF,
            power=0xFF,
            timeout=HexList('FF' * (RFTxCWV0ToV5.LEN.TIMEOUT // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_tx_cw_v0_to_v5

    @staticmethod
    def test_rf_tx_cw_v6_to_v9():
        """
        Tests RFTxCWV6ToV9 class instantiation
        """
        my_class = RFTxCWV6ToV9(
            device_index=0,
            feature_index=0,
            channel=0,
            power=0,
            timeout=HexList('00' * (RFTxCWV6ToV9.LEN.TIMEOUT // 8)),
            condition=0,
            radio_mode=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFTxCWV6ToV9(
            device_index=0xFF,
            feature_index=0xFF,
            channel=0xFF,
            power=0xFF,
            timeout=HexList('FF' * (RFTxCWV6ToV9.LEN.TIMEOUT // 8)),
            condition=0xFF,
            radio_mode=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_tx_cw_v6_to_v9

    @staticmethod
    def test_rf_rx_continuous_v0_to_v5():
        """
        Tests RFRxContinuousV0ToV5 class instantiation
        """
        my_class = RFRxContinuousV0ToV5(
            device_index=0,
            feature_index=0,
            channel=0,
            power=0,
            timeout=HexList('00' * (RFRxContinuousV0ToV5.LEN.TIMEOUT // 8)))

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFRxContinuousV0ToV5(
            device_index=0xFF,
            feature_index=0xFF,
            channel=0xFF,
            power=0xFF,
            timeout=HexList('FF' * (RFRxContinuousV0ToV5.LEN.TIMEOUT // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_rx_continuous_v0_to_v5

    @staticmethod
    def test_rf_rx_continuous_v6_to_v9():
        """
        Tests RFRxContinuousV6ToV9 class instantiation
        """
        my_class = RFRxContinuousV6ToV9(
            device_index=0,
            feature_index=0,
            channel=0,
            power=0,
            timeout=HexList('00' * (RFRxContinuousV6ToV9.LEN.TIMEOUT // 8)),
            condition=0,
            radio_mode=0
        )

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFRxContinuousV6ToV9(
            device_index=0xFF,
            feature_index=0xFF,
            channel=0xFF,
            power=0xFF,
            timeout=HexList('FF' * (RFRxContinuousV6ToV9.LEN.TIMEOUT // 8)),
            condition=0xFF,
            radio_mode=0xFF
        )

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_rx_continuous_v6_to_v9

    @staticmethod
    def test_set_rf_tx_cw_sweep_v0_to_v5():
        """
        Tests SetRfTxCWSweepV0ToV5 class instantiation
        """
        my_class = SetRfTxCWSweepV0ToV5(device_index=0, feature_index=0, channel_min=0,
                                        channel_max=0, power=0, sweep_period=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRfTxCWSweepV0ToV5(device_index=0xFF, feature_index=0xFF, channel_min=0xFF,
                                        channel_max=0xFF, power=0xFF, sweep_period=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_rf_tx_cw_sweep_v0_to_v5

    @staticmethod
    def test_set_rf_tx_cw_sweep_v6():
        """
        Tests SetRfTxCWSweepV6 class instantiation
        """
        my_class = SetRfTxCWSweepV6(device_index=0, feature_index=0, channel_min=0,
                                    channel_max=0, power=0, sweep_period=0, condition=0, radio_mode=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRfTxCWSweepV6(device_index=0xFF, feature_index=0xFF, channel_min=0xFF,
                                    channel_max=0xFF, power=0xFF, sweep_period=0xFF, condition=0, radio_mode=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_rf_tx_cw_sweep_v6

    @staticmethod
    def test_set_rf_tx_cw_sweep_v7_to_v9():
        """
        Tests SetRfTxCWSweepV7ToV9 class instantiation
        """
        my_class = SetRfTxCWSweepV7ToV9(device_index=0, feature_index=0, channel_min=0,
                                        channel_max=0, power=0, sweep_period=0, condition=0, radio_mode=0, nb_sweep=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRfTxCWSweepV7ToV9(device_index=0xFF, feature_index=0xFF, channel_min=0xFF,
                                        channel_max=0xFF, power=0xFF, sweep_period=0xFF, condition=0xFF, radio_mode=0xFF,
                                        nb_sweep=0xFFFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_rf_tx_cw_sweep_v7_to_v9

    @staticmethod
    def test_set_rf_rx_continuous_sweep_v0_to_v5():
        """
        Tests SetRfRxContinuousSweepV0ToV5 class instantiation
        """
        my_class = SetRfRxContinuousSweepV0ToV5(device_index=0, feature_index=0, channel_min=0,
                                                channel_max=0, power=0, sweep_period=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRfRxContinuousSweepV0ToV5(device_index=0xFF, feature_index=0xFF, channel_min=0xFF,
                                                channel_max=0xFF, power=0xFF, sweep_period=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_rf_rx_continuous_sweep_v0_to_v5

    @staticmethod
    def test_set_rf_rx_continuous_sweep_v6():
        """
        Tests SetRfRxContinuousSweepV6 class instantiation
        """
        my_class = SetRfRxContinuousSweepV6(device_index=0, feature_index=0, channel_min=0,
                                            channel_max=0, power=0, sweep_period=0, condition=0, radio_mode=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRfRxContinuousSweepV6(device_index=0xFF, feature_index=0xFF, channel_min=0xFF,
                                            channel_max=0xFF, power=0xFF, sweep_period=0xFF, condition=0xFF,
                                            radio_mode=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_rf_rx_continuous_sweep_v6

    @staticmethod
    def test_set_rf_rx_continuous_sweep_v7_to_v9():
        """
        Tests SetRfRxContinuousSweepV7ToV9 class instantiation
        """
        my_class = SetRfRxContinuousSweepV7ToV9(device_index=0, feature_index=0, channel_min=0,
                                                channel_max=0, power=0, sweep_period=0, condition=0, radio_mode=0,
                                                nb_sweep=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRfRxContinuousSweepV7ToV9(device_index=0xFF, feature_index=0xFF, channel_min=0xFF,
                                                channel_max=0xFF, power=0xFF, sweep_period=0xFF, condition=0xFF,
                                                radio_mode=0xFF, nb_sweep=0xFFFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_rf_rx_continuous_sweep_v7_to_v9

    @staticmethod
    def test_rf_send_periodic_msg_no_ack_v1_to_v2():
        """
        Tests RFSendPeriodicMsgNoAckV1ToV2 class instantiation
        """
        my_class = RFSendPeriodicMsgNoAckV1ToV2(
            device_index=0,
            feature_index=0,
            address=HexList('00' * (RFSendPeriodicMsgNoAckV1ToV2.LEN.ADDRESS // 8)),
            channel=0,
            power=0,
            period=0,
            condition=0,
            nbmsg=HexList('00' * (RFSendPeriodicMsgNoAckV1ToV2.LEN.NBMSG // 8)),)

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFSendPeriodicMsgNoAckV1ToV2(
            device_index=0xFF,
            feature_index=0xFF,
            address=HexList('FF' * (RFSendPeriodicMsgNoAckV1ToV2.LEN.ADDRESS // 8)),
            channel=0xFF,
            power=0xFF,
            period=0xFF,
            condition=0xFF,
            nbmsg=HexList('FF' * (RFSendPeriodicMsgNoAckV1ToV2.LEN.NBMSG // 8)),)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_send_periodic_msg_no_ack_v1_to_v2

    @staticmethod
    def test_rf_send_periodic_msg_no_ack_v3_to_v5():
        """
        Tests RFSendPeriodicMsgNoAckV3ToV5 class instantiation
        """
        my_class = RFSendPeriodicMsgNoAckV3ToV5(
            device_index=0,
            feature_index=0,
            address=HexList('00' * (RFSendPeriodicMsgNoAckV3ToV5.LEN.ADDRESS // 8)),
            channel=0,
            power=0,
            period=0,
            condition=0,
            nbmsg=HexList('00' * (RFSendPeriodicMsgNoAckV3ToV5.LEN.NBMSG // 8)),
            radio_mode=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFSendPeriodicMsgNoAckV3ToV5(
            device_index=0xFF,
            feature_index=0xFF,
            address=HexList('FF' * (RFSendPeriodicMsgNoAckV3ToV5.LEN.ADDRESS // 8)),
            channel=0xFF,
            power=0xFF,
            period=0xFF,
            condition=0xFF,
            nbmsg=HexList('FF' * (RFSendPeriodicMsgNoAckV3ToV5.LEN.NBMSG // 8)),
            radio_mode=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_send_periodic_msg_no_ack_v3_to_v5

    @staticmethod
    def test_rf_send_periodic_msg_no_ack_v6_to_v9():
        """
        Tests RFSendPeriodicMsgNoAckV6 class instantiation
        """
        my_class = RFSendPeriodicMsgNoAckV6ToV9(
            device_index=0,
            feature_index=0,
            address=HexList('00' * (RFSendPeriodicMsgNoAckV6ToV9.LEN.ADDRESS // 8)),
            channel=0,
            power=0,
            period=0,
            condition=0,
            nbmsg=HexList('00' * (RFSendPeriodicMsgNoAckV6ToV9.LEN.NBMSG // 8)),
            radio_mode=0,
            payload_size=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFSendPeriodicMsgNoAckV6ToV9(
            device_index=0xFF,
            feature_index=0xFF,
            address=HexList('FF' * (RFSendPeriodicMsgNoAckV6ToV9.LEN.ADDRESS // 8)),
            channel=0xFF,
            power=0xFF,
            period=0xFF,
            condition=0xFF,
            nbmsg=HexList('FF' * (RFSendPeriodicMsgNoAckV6ToV9.LEN.NBMSG // 8)),
            radio_mode=0xFF,
            payload_size=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_send_periodic_msg_no_ack_v6_to_v9

    @staticmethod
    def test_rf_receive_periodic_msg_v2():
        """
        Tests RFReceivePeriodicMsgV2 class instantiation
        """
        my_class = RFReceivePeriodicMsgV2(
            device_index=0,
            feature_index=0,
            address=HexList('00' * (RFReceivePeriodicMsgV2.LEN.ADDRESS // 8)),
            channel=0,
            power=0,
            condition=0,
            timeout=HexList('00' * (RFReceivePeriodicMsgV2.LEN.TIMEOUT // 8)),)

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFReceivePeriodicMsgV2(
            device_index=0xFF,
            feature_index=0xFF,
            address=HexList('FF' * (RFReceivePeriodicMsgV2.LEN.ADDRESS // 8)),
            channel=0xFF,
            power=0xFF,
            condition=0xFF,
            timeout=HexList('FF' * (RFReceivePeriodicMsgV2.LEN.TIMEOUT // 8)),)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_receive_periodic_msg_v2

    @staticmethod
    def test_rf_receive_periodic_msg_v3_to_v9():
        """
        Tests RFReceivePeriodicMsgV3ToV6 class instantiation
        """
        my_class = RFReceivePeriodicMsgV3ToV9(
            device_index=0,
            feature_index=0,
            address=HexList('00' * (RFReceivePeriodicMsgV3ToV9.LEN.ADDRESS // 8)),
            channel=0,
            power=0,
            condition=0,
            timeout=HexList('00' * (RFReceivePeriodicMsgV3ToV9.LEN.TIMEOUT // 8)),
            radio_mode=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFReceivePeriodicMsgV3ToV9(
            device_index=0xFF,
            feature_index=0xFF,
            address=HexList('FF' * (RFReceivePeriodicMsgV3ToV9.LEN.ADDRESS // 8)),
            channel=0xFF,
            power=0xFF,
            condition=0xFF,
            timeout=HexList('FF' * (RFReceivePeriodicMsgV3ToV9.LEN.TIMEOUT // 8)),
            radio_mode=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_receive_periodic_msg_v3_to_v9

    @staticmethod
    def test_rf_send_periodic_full_duty_msg_v9():
        """
        Tests RFSendPeriodicFullDutyMsgV9 class instantiation
        """
        my_class = RFSendPeriodicFullDutyMsgV9(
            device_index=0,
            feature_index=0,
            channel=0,
            power=0,
            timeout=HexList('00' * (RFSendPeriodicFullDutyMsgV9.LEN.TIMEOUT // 8)),
            condition=0,
            radio_mode=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFSendPeriodicFullDutyMsgV9(
            device_index=0xFF,
            feature_index=0xFF,
            channel=0xFF,
            power=0xFF,
            timeout=HexList('FF' * (RFSendPeriodicFullDutyMsgV9.LEN.TIMEOUT // 8)),
            condition=0xFF,
            radio_mode=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_send_periodic_full_duty_msg_v9

    @staticmethod
    def test_rf_send_periodic_full_duty_msg_response_v9():
        """
        Tests RFSendPeriodicFullDutyMsgResponseV9 class instantiation
        """
        my_class = RFSendPeriodicFullDutyMsgResponseV9(
            device_index=0,
            feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFSendPeriodicFullDutyMsgResponseV9(
            device_index=0xFF,
            feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_send_periodic_full_duty_msg_v9
# end class RFTestInstantiationTestCase


class RFTestTestCase(TestCase):
    """
    RF Test factory testing
    """
    @classmethod
    def setUpClass(cls):
        cls.expected = {
            0: {
                "cls": RFTestV0,
                "interfaces": {
                    "rf_send_periodic_msg_cls": RFSendPeriodicMsgV0ToV2,
                    "rf_send_periodic_msg_response_cls": RFSendPeriodicMsgResponseV0ToV9,
                    "rf_tx_cw_cls": RFTxCWV0ToV5,
                    "rf_tx_cw_response_cls": RFTxCWResponseV0ToV9,
                    "rf_rx_continuous_cls": RFRxContinuousV0ToV5,
                    "rf_rx_continuous_response_cls": RFRxContinuousResponseV0ToV9,
                    "set_rf_tx_cw_sweep_cls": SetRfTxCWSweepV0ToV5,
                    "set_rf_tx_cw_sweep_response_cls": SetRfTxCWSweepResponseV0ToV9,
                    "set_rf_rx_continuous_sweep_cls": SetRfRxContinuousSweepV0ToV5,
                    "set_rf_rx_continuous_sweep_response_cls": SetRfRxContinuousSweepResponseV0ToV9,
                },
                "max_function_index": 4
            },
            1: {
                "cls": RFTestV1,
                "interfaces": {
                    "rf_send_periodic_msg_cls": RFSendPeriodicMsgV0ToV2,
                    "rf_send_periodic_msg_response_cls": RFSendPeriodicMsgResponseV0ToV9,
                    "rf_tx_cw_cls": RFTxCWV0ToV5,
                    "rf_tx_cw_response_cls": RFTxCWResponseV0ToV9,
                    "rf_rx_continuous_cls": RFRxContinuousV0ToV5,
                    "rf_rx_continuous_response_cls": RFRxContinuousResponseV0ToV9,
                    "set_rf_tx_cw_sweep_cls": SetRfTxCWSweepV0ToV5,
                    "set_rf_tx_cw_sweep_response_cls": SetRfTxCWSweepResponseV0ToV9,
                    "set_rf_rx_continuous_sweep_cls": SetRfRxContinuousSweepV0ToV5,
                    "set_rf_rx_continuous_sweep_response_cls": SetRfRxContinuousSweepResponseV0ToV9,
                    "rf_send_periodic_msg_no_ack_cls": RFSendPeriodicMsgNoAckV1ToV2,
                    "rf_send_periodic_msg_no_ack_response_cls": RFSendPeriodicMsgNoAckResponseV1ToV9,
                },
                "max_function_index": 5
            },
            2: {
                "cls": RFTestV2,
                "interfaces": {
                    "rf_send_periodic_msg_cls": RFSendPeriodicMsgV0ToV2,
                    "rf_send_periodic_msg_response_cls": RFSendPeriodicMsgResponseV0ToV9,
                    "rf_tx_cw_cls": RFTxCWV0ToV5,
                    "rf_tx_cw_response_cls": RFTxCWResponseV0ToV9,
                    "rf_rx_continuous_cls": RFRxContinuousV0ToV5,
                    "rf_rx_continuous_response_cls": RFRxContinuousResponseV0ToV9,
                    "set_rf_tx_cw_sweep_cls": SetRfTxCWSweepV0ToV5,
                    "set_rf_tx_cw_sweep_response_cls": SetRfTxCWSweepResponseV0ToV9,
                    "set_rf_rx_continuous_sweep_cls": SetRfRxContinuousSweepV0ToV5,
                    "set_rf_rx_continuous_sweep_response_cls": SetRfRxContinuousSweepResponseV0ToV9,
                    "rf_send_periodic_msg_no_ack_cls": RFSendPeriodicMsgNoAckV1ToV2,
                    "rf_send_periodic_msg_no_ack_response_cls": RFSendPeriodicMsgNoAckResponseV1ToV9,
                    "rf_receive_periodic_msg_cls": RFReceivePeriodicMsgV2,
                    "rf_receive_periodic_msg_response_cls": RFReceivePeriodicMsgResponseV2ToV9,
                },
                "max_function_index": 6
            },
            3: {
                "cls": RFTestV3,
                "interfaces": {
                    "rf_send_periodic_msg_cls": RFSendPeriodicMsgV3ToV5,
                    "rf_send_periodic_msg_response_cls": RFSendPeriodicMsgResponseV0ToV9,
                    "rf_tx_cw_cls": RFTxCWV0ToV5,
                    "rf_tx_cw_response_cls": RFTxCWResponseV0ToV9,
                    "rf_rx_continuous_cls": RFRxContinuousV0ToV5,
                    "rf_rx_continuous_response_cls": RFRxContinuousResponseV0ToV9,
                    "set_rf_tx_cw_sweep_cls": SetRfTxCWSweepV0ToV5,
                    "set_rf_tx_cw_sweep_response_cls": SetRfTxCWSweepResponseV0ToV9,
                    "set_rf_rx_continuous_sweep_cls": SetRfRxContinuousSweepV0ToV5,
                    "set_rf_rx_continuous_sweep_response_cls": SetRfRxContinuousSweepResponseV0ToV9,
                    "rf_send_periodic_msg_no_ack_cls": RFSendPeriodicMsgNoAckV3ToV5,
                    "rf_send_periodic_msg_no_ack_response_cls": RFSendPeriodicMsgNoAckResponseV1ToV9,
                    "rf_receive_periodic_msg_cls": RFReceivePeriodicMsgV3ToV9,
                    "rf_receive_periodic_msg_response_cls": RFReceivePeriodicMsgResponseV2ToV9,
                },
                "max_function_index": 6
            },
            4: {
                "cls": RFTestV4,
                "interfaces": {
                    "rf_send_periodic_msg_cls": RFSendPeriodicMsgV3ToV5,
                    "rf_send_periodic_msg_response_cls": RFSendPeriodicMsgResponseV0ToV9,
                    "rf_tx_cw_cls": RFTxCWV0ToV5,
                    "rf_tx_cw_response_cls": RFTxCWResponseV0ToV9,
                    "rf_rx_continuous_cls": RFRxContinuousV0ToV5,
                    "rf_rx_continuous_response_cls": RFRxContinuousResponseV0ToV9,
                    "set_rf_tx_cw_sweep_cls": SetRfTxCWSweepV0ToV5,
                    "set_rf_tx_cw_sweep_response_cls": SetRfTxCWSweepResponseV0ToV9,
                    "set_rf_rx_continuous_sweep_cls": SetRfRxContinuousSweepV0ToV5,
                    "set_rf_rx_continuous_sweep_response_cls": SetRfRxContinuousSweepResponseV0ToV9,
                    "rf_send_periodic_msg_no_ack_cls": RFSendPeriodicMsgNoAckV3ToV5,
                    "rf_send_periodic_msg_no_ack_response_cls": RFSendPeriodicMsgNoAckResponseV1ToV9,
                    "rf_receive_periodic_msg_cls": RFReceivePeriodicMsgV3ToV9,
                    "rf_receive_periodic_msg_response_cls": RFReceivePeriodicMsgResponseV2ToV9,
                },
                "max_function_index": 6
            },
            5: {
                "cls": RFTestV5,
                "interfaces": {
                    "rf_send_periodic_msg_cls": RFSendPeriodicMsgV3ToV5,
                    "rf_send_periodic_msg_response_cls": RFSendPeriodicMsgResponseV0ToV9,
                    "rf_tx_cw_cls": RFTxCWV0ToV5,
                    "rf_tx_cw_response_cls": RFTxCWResponseV0ToV9,
                    "rf_rx_continuous_cls": RFRxContinuousV0ToV5,
                    "rf_rx_continuous_response_cls": RFRxContinuousResponseV0ToV9,
                    "set_rf_tx_cw_sweep_cls": SetRfTxCWSweepV0ToV5,
                    "set_rf_tx_cw_sweep_response_cls": SetRfTxCWSweepResponseV0ToV9,
                    "set_rf_rx_continuous_sweep_cls": SetRfRxContinuousSweepV0ToV5,
                    "set_rf_rx_continuous_sweep_response_cls": SetRfRxContinuousSweepResponseV0ToV9,
                    "rf_send_periodic_msg_no_ack_cls": RFSendPeriodicMsgNoAckV3ToV5,
                    "rf_send_periodic_msg_no_ack_response_cls": RFSendPeriodicMsgNoAckResponseV1ToV9,
                    "rf_receive_periodic_msg_cls": RFReceivePeriodicMsgV3ToV9,
                    "rf_receive_periodic_msg_response_cls": RFReceivePeriodicMsgResponseV2ToV9,
                },
                "max_function_index": 6
            },
            6: {
                "cls": RFTestV6,
                "interfaces": {
                    "rf_send_periodic_msg_cls": RFSendPeriodicMsgV6ToV9,
                    "rf_send_periodic_msg_response_cls": RFSendPeriodicMsgResponseV0ToV9,
                    "rf_tx_cw_cls": RFTxCWV6ToV9,
                    "rf_tx_cw_response_cls": RFTxCWResponseV0ToV9,
                    "rf_rx_continuous_cls": RFRxContinuousV6ToV9,
                    "rf_rx_continuous_response_cls": RFRxContinuousResponseV0ToV9,
                    "set_rf_tx_cw_sweep_cls": SetRfTxCWSweepV6,
                    "set_rf_tx_cw_sweep_response_cls": SetRfTxCWSweepResponseV0ToV9,
                    "set_rf_rx_continuous_sweep_cls": SetRfRxContinuousSweepV6,
                    "set_rf_rx_continuous_sweep_response_cls": SetRfRxContinuousSweepResponseV0ToV9,
                    "rf_send_periodic_msg_no_ack_cls": RFSendPeriodicMsgNoAckV6ToV9,
                    "rf_send_periodic_msg_no_ack_response_cls": RFSendPeriodicMsgNoAckResponseV1ToV9,
                    "rf_receive_periodic_msg_cls": RFReceivePeriodicMsgV3ToV9,
                    "rf_receive_periodic_msg_response_cls": RFReceivePeriodicMsgResponseV2ToV9,
                },
                "max_function_index": 6
            },
            7: {
                "cls": RFTestV7,
                "interfaces": {
                    "rf_send_periodic_msg_cls": RFSendPeriodicMsgV6ToV9,
                    "rf_send_periodic_msg_response_cls": RFSendPeriodicMsgResponseV0ToV9,
                    "rf_tx_cw_cls": RFTxCWV6ToV9,
                    "rf_tx_cw_response_cls": RFTxCWResponseV0ToV9,
                    "rf_rx_continuous_cls": RFRxContinuousV6ToV9,
                    "rf_rx_continuous_response_cls": RFRxContinuousResponseV0ToV9,
                    "set_rf_tx_cw_sweep_cls": SetRfTxCWSweepV7ToV9,
                    "set_rf_tx_cw_sweep_response_cls": SetRfTxCWSweepResponseV0ToV9,
                    "set_rf_rx_continuous_sweep_cls": SetRfRxContinuousSweepV7ToV9,
                    "set_rf_rx_continuous_sweep_response_cls": SetRfRxContinuousSweepResponseV0ToV9,
                    "rf_send_periodic_msg_no_ack_cls": RFSendPeriodicMsgNoAckV6ToV9,
                    "rf_send_periodic_msg_no_ack_response_cls": RFSendPeriodicMsgNoAckResponseV1ToV9,
                    "rf_receive_periodic_msg_cls": RFReceivePeriodicMsgV3ToV9,
                    "rf_receive_periodic_msg_response_cls": RFReceivePeriodicMsgResponseV2ToV9,
                },
                "max_function_index": 6
            },
            8: {
                "cls": RFTestV8,
                "interfaces": {
                    "rf_send_periodic_msg_cls": RFSendPeriodicMsgV6ToV9,
                    "rf_send_periodic_msg_response_cls": RFSendPeriodicMsgResponseV0ToV9,
                    "rf_tx_cw_cls": RFTxCWV6ToV9,
                    "rf_tx_cw_response_cls": RFTxCWResponseV0ToV9,
                    "rf_rx_continuous_cls": RFRxContinuousV6ToV9,
                    "rf_rx_continuous_response_cls": RFRxContinuousResponseV0ToV9,
                    "set_rf_tx_cw_sweep_cls": SetRfTxCWSweepV7ToV9,
                    "set_rf_tx_cw_sweep_response_cls": SetRfTxCWSweepResponseV0ToV9,
                    "set_rf_rx_continuous_sweep_cls": SetRfRxContinuousSweepV7ToV9,
                    "set_rf_rx_continuous_sweep_response_cls": SetRfRxContinuousSweepResponseV0ToV9,
                    "rf_send_periodic_msg_no_ack_cls": RFSendPeriodicMsgNoAckV6ToV9,
                    "rf_send_periodic_msg_no_ack_response_cls": RFSendPeriodicMsgNoAckResponseV1ToV9,
                    "rf_receive_periodic_msg_cls": RFReceivePeriodicMsgV3ToV9,
                    "rf_receive_periodic_msg_response_cls": RFReceivePeriodicMsgResponseV2ToV9,
                },
                "max_function_index": 6
            },
            9: {
                "cls": RFTestV9,
                "interfaces": {
                    "rf_send_periodic_msg_cls": RFSendPeriodicMsgV6ToV9,
                    "rf_send_periodic_msg_response_cls": RFSendPeriodicMsgResponseV0ToV9,
                    "rf_tx_cw_cls": RFTxCWV6ToV9,
                    "rf_tx_cw_response_cls": RFTxCWResponseV0ToV9,
                    "rf_rx_continuous_cls": RFRxContinuousV6ToV9,
                    "rf_rx_continuous_response_cls": RFRxContinuousResponseV0ToV9,
                    "set_rf_tx_cw_sweep_cls": SetRfTxCWSweepV7ToV9,
                    "set_rf_tx_cw_sweep_response_cls": SetRfTxCWSweepResponseV0ToV9,
                    "set_rf_rx_continuous_sweep_cls": SetRfRxContinuousSweepV7ToV9,
                    "set_rf_rx_continuous_sweep_response_cls": SetRfRxContinuousSweepResponseV0ToV9,
                    "rf_send_periodic_msg_no_ack_cls": RFSendPeriodicMsgNoAckV6ToV9,
                    "rf_send_periodic_msg_no_ack_response_cls": RFSendPeriodicMsgNoAckResponseV1ToV9,
                    "rf_receive_periodic_msg_cls": RFReceivePeriodicMsgV3ToV9,
                    "rf_receive_periodic_msg_response_cls": RFReceivePeriodicMsgResponseV2ToV9,
                    "rf_send_periodic_full_duty_msg_cls": RFSendPeriodicFullDutyMsgV9,
                    "rf_send_periodic_full_duty_msg_response_cls": RFSendPeriodicFullDutyMsgResponseV9,
                },
                "max_function_index": 7
            },
        }
    # end def setUpClass

    def test_rf_test_factory(self):
        """
        Tests RFTestFactory
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(RFTestFactory.create(version)), expected["cls"])
        # end for loop
    # end def test_rf_test_factory

    def test_rf_test_factory_version_out_of_range(self):
        """
        Tests RFTestFactory with out of range versions
        """
        for version in [-1, 10]:
            with self.assertRaises(KeyError):
                RFTestFactory.create(version)
    # end def test_rf_test_factory_version_out_of_range

    def test_rf_test_factory_interfaces(self):
        """
        Check RFTestFactory returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            rf_test = RFTestFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(rf_test, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(rf_test, interface)
                # end if
            # end for loop
        # end for loop
    # end def test_rf_test_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check get_max_function_index returns correct value at each version
        """
        for version, expected in self.expected.items():
            rf_test = RFTestFactory.create(version)
            self.assertEqual(rf_test.get_max_function_index(), expected["max_function_index"])
        # end for loop
    # end def test_get_max_function_index
# end class RFTestTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
