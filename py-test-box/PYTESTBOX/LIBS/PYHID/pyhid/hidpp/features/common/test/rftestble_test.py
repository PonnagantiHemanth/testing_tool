#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
""" @package pyhid.hidpp.feature.common.test.rftestble_test

@brief  HID++ 2.0 rf test ble test module

@author Jerry Lin

@date   2020/04/21
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList
from unittest import TestCase

from pyhid.hidpp.features.common.rftestble import RFBLEReceivePeriodicMsgV2
from pyhid.hidpp.features.common.rftestble import RFBLEReceivePeriodicMsgV3ToV9
from pyhid.hidpp.features.common.rftestble import RFBLERxContinuousV0ToV5
from pyhid.hidpp.features.common.rftestble import RFBLERxContinuousV6ToV9
from pyhid.hidpp.features.common.rftestble import RFBLESendPeriodicFullDutyMsgResponseV9
from pyhid.hidpp.features.common.rftestble import RFBLESendPeriodicFullDutyMsgV9
from pyhid.hidpp.features.common.rftestble import RFBLESendPeriodicMsgNoAckV1ToV2
from pyhid.hidpp.features.common.rftestble import RFBLESendPeriodicMsgNoAckV3ToV5
from pyhid.hidpp.features.common.rftestble import RFBLESendPeriodicMsgNoAckV6ToV9
from pyhid.hidpp.features.common.rftestble import RFBLESendPeriodicMsgResponseV0ToV9
from pyhid.hidpp.features.common.rftestble import RFBLESendPeriodicMsgV0ToV2
from pyhid.hidpp.features.common.rftestble import RFBLESendPeriodicMsgV3ToV5
from pyhid.hidpp.features.common.rftestble import RFBLESendPeriodicMsgV6ToV9
from pyhid.hidpp.features.common.rftestble import RFBLETxCWV0ToV5
from pyhid.hidpp.features.common.rftestble import RFBLETxCWV6ToV9
from pyhid.hidpp.features.common.rftestble import RFTestBLE
from pyhid.hidpp.features.common.rftestble import RFTestBLEFactory
from pyhid.hidpp.features.common.rftestble import RFTestBLEV0
from pyhid.hidpp.features.common.rftestble import RFTestBLEV1
from pyhid.hidpp.features.common.rftestble import RFTestBLEV2
from pyhid.hidpp.features.common.rftestble import RFTestBLEV3
from pyhid.hidpp.features.common.rftestble import RFTestBLEV4
from pyhid.hidpp.features.common.rftestble import RFTestBLEV5
from pyhid.hidpp.features.common.rftestble import RFTestBLEV6
from pyhid.hidpp.features.common.rftestble import RFTestBLEV7
from pyhid.hidpp.features.common.rftestble import RFTestBLEV8
from pyhid.hidpp.features.common.rftestble import RFTestBLEV9
from pyhid.hidpp.features.common.rftestble import SetRfBLERxContinuousSweepV0ToV5
from pyhid.hidpp.features.common.rftestble import SetRfBLERxContinuousSweepV6
from pyhid.hidpp.features.common.rftestble import SetRfBLERxContinuousSweepV7ToV9
from pyhid.hidpp.features.common.rftestble import SetRfBLETxCWSweepV0ToV5
from pyhid.hidpp.features.common.rftestble import SetRfBLETxCWSweepV6
from pyhid.hidpp.features.common.rftestble import SetRfBLETxCWSweepV7ToV9
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class RFTestBLEInstantiationTestCase(TestCase):
    """
    DeviceInformation testing classes instantiations
    """

    @staticmethod
    def test_rf_ble_test():
        """
        Tests DeviceInformation class instantiation
        """
        my_class = RFTestBLE(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = RFTestBLE(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_rf_ble_test

    @staticmethod
    def test_rf_ble_send_periodic_msg_v0_to_v2():
        """
        Tests RFBLESendPeriodicMsgV0ToV2 class instantiation
        """
        my_class = RFBLESendPeriodicMsgV0ToV2(device_index=0,
                                              feature_index=0,
                                              address=HexList('00' * (
                                                      RFBLESendPeriodicMsgV0ToV2.LEN.ADDRESS // 8)),
                                              channel=0,
                                              power=0,
                                              period=0,
                                              condition=0,
                                              nbmsg=HexList('00' * (
                                                    RFBLESendPeriodicMsgV0ToV2.LEN.NBMSG // 8)),)

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFBLESendPeriodicMsgV0ToV2(device_index=0xFF,
                                              feature_index=0xFF,
                                              address=HexList('FF' * (
                                                      RFBLESendPeriodicMsgV0ToV2.LEN.ADDRESS // 8)),
                                              channel=0xFF,
                                              power=0xFF,
                                              period=0xFF,
                                              condition=0xFF,
                                              nbmsg=HexList('FF' * (
                                                    RFBLESendPeriodicMsgV0ToV2.LEN.NBMSG // 8)),)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_ble_send_periodic_msg_v0_to_v2

    @staticmethod
    def test_rf_ble_send_periodic_msg_v3_to_v5():
        """
        Tests RFBLESendPeriodicMsgV3ToV5 class instantiation
        """
        my_class = RFBLESendPeriodicMsgV3ToV5(device_index=0,
                                              feature_index=0,
                                              address=HexList('00' * (
                                                      RFBLESendPeriodicMsgV3ToV5.LEN.ADDRESS // 8)),
                                              channel=0,
                                              power=0,
                                              period=0,
                                              condition=0,
                                              nbmsg=HexList('00' * (
                                                      RFBLESendPeriodicMsgV3ToV5.LEN.NBMSG // 8)),
                                              radio_mode=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFBLESendPeriodicMsgV3ToV5(device_index=0xFF,
                                              feature_index=0xFF,
                                              address=HexList('FF' * (
                                                      RFBLESendPeriodicMsgV3ToV5.LEN.ADDRESS // 8)),
                                              channel=0xFF,
                                              power=0xFF,
                                              period=0xFF,
                                              condition=0xFF,
                                              nbmsg=HexList('FF' * (
                                                    RFBLESendPeriodicMsgV3ToV5.LEN.NBMSG // 8)),
                                              radio_mode=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_ble_send_periodic_msg_v3_to_v5

    @staticmethod
    def test_rf_ble_send_periodic_msg_v6_to_v9():
        """
        Tests RFBLESendPeriodicMsgV6ToV9 class instantiation
        """
        my_class = RFBLESendPeriodicMsgV6ToV9(
            device_index=0,
            feature_index=0,
            address=HexList('00' * (
                    RFBLESendPeriodicMsgV6ToV9.LEN.ADDRESS // 8)),
            channel=0,
            power=0,
            period=0,
            condition=0,
            nbmsg=HexList('00' * (
                    RFBLESendPeriodicMsgV6ToV9.LEN.NBMSG // 8)),
            radio_mode=0,
            payload_size=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFBLESendPeriodicMsgV6ToV9(
            device_index=0xFF,
            feature_index=0xFF,
            address=HexList('FF' * (
                    RFBLESendPeriodicMsgV6ToV9.LEN.ADDRESS // 8)),
            channel=0xFF,
            power=0xFF,
            period=0xFF,
            condition=0xFF,
            nbmsg=HexList('FF' * (
                    RFBLESendPeriodicMsgV6ToV9.LEN.NBMSG // 8)),
            radio_mode=0xFF,
            payload_size=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_ble_send_periodic_msg_v6_to_v9

    @staticmethod
    def test_rf_ble_send_periodic_msg_response_v0_to_v9():
        """
        Tests RFBLESendPeriodicMsgResponseV0ToV9 class instantiation
        """
        my_class = RFBLESendPeriodicMsgResponseV0ToV9(
            device_index=0,
            feature_index=0,
            nb_msg_ack=HexList('00' * (RFBLESendPeriodicMsgResponseV0ToV9.LEN.NB_MSG_ACK // 8))
        )

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFBLESendPeriodicMsgResponseV0ToV9(
            device_index=0xFF,
            feature_index=0xFF,
            nb_msg_ack=HexList('FF' * (RFBLESendPeriodicMsgResponseV0ToV9.LEN.NB_MSG_ACK // 8))
        )

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_ble_send_periodic_msg_response_v0_to_v9

    @staticmethod
    def test_rf_ble_tx_cw_v0_to_v5():
        """
        Tests RFBLETxCWV0ToV5 class instantiation
        """
        my_class = RFBLETxCWV0ToV5(
            device_index=0,
            feature_index=0,
            channel=0,
            power=0,
            timeout=HexList('00' * (RFBLETxCWV0ToV5.LEN.TIMEOUT // 8)))

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFBLETxCWV0ToV5(
            device_index=0xFF,
            feature_index=0xFF,
            channel=0xFF,
            power=0xFF,
            timeout=HexList('FF' * (RFBLETxCWV0ToV5.LEN.TIMEOUT // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_ble_tx_cw_v0_to_v5

    @staticmethod
    def test_rf_ble_tx_cw_v6_to_v9():
        """
        Tests RFBLETxCWV6ToV9 class instantiation
        """
        my_class = RFBLETxCWV6ToV9(
            device_index=0,
            feature_index=0,
            channel=0,
            power=0,
            timeout=HexList('00' * (RFBLETxCWV6ToV9.LEN.TIMEOUT // 8)),
            condition=0,
            radio_mode=0
        )

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFBLETxCWV6ToV9(
            device_index=0xFF,
            feature_index=0xFF,
            channel=0xFF,
            power=0xFF,
            timeout=HexList('FF' * (RFBLETxCWV6ToV9.LEN.TIMEOUT // 8)),
            condition=0xFF,
            radio_mode=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_ble_tx_cw_v6_to_v9

    @staticmethod
    def test_rf_ble_rx_continuous_v0_to_v5():
        """
        Tests RFBLERxContinuousV0ToV5 class instantiation
        """
        my_class = RFBLERxContinuousV0ToV5(
            device_index=0,
            feature_index=0,
            channel=0,
            power=0,
            timeout=HexList('00' * (RFBLERxContinuousV0ToV5.LEN.TIMEOUT // 8)))

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFBLERxContinuousV0ToV5(
            device_index=0xFF,
            feature_index=0xFF,
            channel=0xFF,
            power=0xFF,
            timeout=HexList('FF' * (RFBLERxContinuousV0ToV5.LEN.TIMEOUT // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_ble_rx_continuous_v0_to_v5

    @staticmethod
    def test_rf_ble_rx_continuous_v6_to_v9():
        """
        Tests RFBLERxContinuousV6ToV9 class instantiation
        """
        my_class = RFBLERxContinuousV6ToV9(
            device_index=0,
            feature_index=0,
            channel=0,
            power=0,
            timeout=HexList('00' * (RFBLERxContinuousV6ToV9.LEN.TIMEOUT // 8)),
            condition=0,
            radio_mode=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFBLERxContinuousV6ToV9(
            device_index=0xFF,
            feature_index=0xFF,
            channel=0xFF,
            power=0xFF,
            timeout=HexList('FF' * (RFBLERxContinuousV6ToV9.LEN.TIMEOUT // 8)),
            condition=0xFF,
            radio_mode=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_ble_rx_continuous_v6_to_v9

    @staticmethod
    def test_set_rf_ble_tx_cw_sweep_v0_to_v5():
        """
        Tests SetRfBLETxCWSweepV0ToV5 class instantiation
        """
        my_class = SetRfBLETxCWSweepV0ToV5(device_index=0, feature_index=0, channel_min=0,
                                           channel_max=0, power=0, sweep_period=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRfBLETxCWSweepV0ToV5(device_index=0xFF, feature_index=0xFF, channel_min=0xFF,
                                           channel_max=0xFF, power=0xFF, sweep_period=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_rf_ble_tx_cw_sweep_v0_to_v5

    @staticmethod
    def test_set_rf_ble_tx_cw_sweep_v6():
        """
        Tests SetRfBLETxCWSweepV6 class instantiation
        """
        my_class = SetRfBLETxCWSweepV6(device_index=0, feature_index=0, channel_min=0,
                                       channel_max=0, power=0, sweep_period=0, condition=0, radio_mode=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRfBLETxCWSweepV6(device_index=0xFF, feature_index=0xFF, channel_min=0xFF,
                                       channel_max=0xFF, power=0xFF, sweep_period=0xFF, condition=0xFF, radio_mode=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_rf_ble_tx_cw_sweep_v6

    @staticmethod
    def test_set_rf_ble_tx_cw_sweep_v7_to_v9():
        """
        Tests SetRfBLETxCWSweepV7ToV9 class instantiation
        """
        my_class = SetRfBLETxCWSweepV7ToV9(device_index=0, feature_index=0, channel_min=0,
                                           channel_max=0, power=0, sweep_period=0, condition=0, radio_mode=0, nb_sweep=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRfBLETxCWSweepV7ToV9(device_index=0xFF, feature_index=0xFF, channel_min=0xFF,
                                           channel_max=0xFF, power=0xFF, sweep_period=0xFF, condition=0xFF,
                                           radio_mode=0xFF, nb_sweep=0xFFFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_rf_ble_tx_cw_sweep_v7_to_v9

    @staticmethod
    def test_set_rf_ble_rx_continuous_sweep_v0_to_v5():
        """
        Tests SetRfBLERxContinuousSweepV0ToV5 class instantiation
        """
        my_class = SetRfBLERxContinuousSweepV0ToV5(device_index=0, feature_index=0, channel_min=0,
                                                   channel_max=0, power=0, sweep_period=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRfBLERxContinuousSweepV0ToV5(device_index=0xFF, feature_index=0xFF, channel_min=0xFF,
                                                   channel_max=0xFF, power=0xFF, sweep_period=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_rf_ble_rx_continuous_sweep_v0_to_v5

    @staticmethod
    def test_set_rf_ble_rx_continuous_sweep_v6():
        """
        Tests SetRfBLERxContinuousSweepV6 class instantiation
        """
        my_class = SetRfBLERxContinuousSweepV6(device_index=0, feature_index=0, channel_min=0,
                                               channel_max=0, power=0, sweep_period=0, condition=0, radio_mode=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRfBLERxContinuousSweepV6(device_index=0xFF, feature_index=0xFF, channel_min=0xFF,
                                               channel_max=0xFF, power=0xFF, sweep_period=0xFF, condition=0xFF,
                                               radio_mode=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_rf_ble_rx_continuous_sweep_v6

    @staticmethod
    def test_set_rf_ble_rx_continuous_sweep_v7_to_v9():
        """
        Tests SetRfBLERxContinuousSweepV7ToV9 class instantiation
        """
        my_class = SetRfBLERxContinuousSweepV7ToV9(device_index=0, feature_index=0, channel_min=0,
                                                   channel_max=0, power=0, sweep_period=0, condition=0, radio_mode=0,
                                                   nb_sweep=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRfBLERxContinuousSweepV7ToV9(device_index=0xFF, feature_index=0xFF, channel_min=0xFF,
                                                   channel_max=0xFF, power=0xFF, sweep_period=0xFF, condition=0xFF,
                                                   radio_mode=0xFF, nb_sweep=0xFFFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_rf_ble_rx_continuous_sweep_v7_to_v9

    @staticmethod
    def test_rf_ble_send_periodic_msg_no_ack_v1_to_v2():
        """
        Tests RFBLESendPeriodicMsgNoAckV1ToV2 class instantiation
        """
        my_class = RFBLESendPeriodicMsgNoAckV1ToV2(
            device_index=0,
            feature_index=0,
            address=HexList('00' * (RFBLESendPeriodicMsgNoAckV1ToV2.LEN.ADDRESS // 8)),
            channel=0,
            power=0,
            period=0,
            condition=0,
            nbmsg=HexList('00' * (RFBLESendPeriodicMsgNoAckV1ToV2.LEN.NBMSG // 8)),)

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFBLESendPeriodicMsgNoAckV1ToV2(
            device_index=0xFF,
            feature_index=0xFF,
            address=HexList('FF' * (RFBLESendPeriodicMsgNoAckV1ToV2.LEN.ADDRESS // 8)),
            channel=0xFF,
            power=0xFF,
            period=0xFF,
            condition=0xFF,
            nbmsg=HexList('FF' * (RFBLESendPeriodicMsgNoAckV1ToV2.LEN.NBMSG // 8)),)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_ble_send_periodic_msg_no_ack_v1_to_v2

    @staticmethod
    def test_rf_ble_send_periodic_msg_no_ack_v3_to_v5():
        """
        Tests RFBLESendPeriodicMsgNoAckV3ToV5 class instantiation
        """
        my_class = RFBLESendPeriodicMsgNoAckV3ToV5(
            device_index=0,
            feature_index=0,
            address=HexList('00' * (RFBLESendPeriodicMsgNoAckV3ToV5.LEN.ADDRESS // 8)),
            channel=0,
            power=0,
            period=0,
            condition=0,
            nbmsg=HexList('00' * (RFBLESendPeriodicMsgNoAckV3ToV5.LEN.NBMSG // 8)),
            radio_mode=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFBLESendPeriodicMsgNoAckV3ToV5(
            device_index=0xFF,
            feature_index=0xFF,
            address=HexList('FF' * (RFBLESendPeriodicMsgNoAckV3ToV5.LEN.ADDRESS // 8)),
            channel=0xFF,
            power=0xFF,
            period=0xFF,
            condition=0xFF,
            nbmsg=HexList('FF' * (RFBLESendPeriodicMsgNoAckV3ToV5.LEN.NBMSG // 8)),
            radio_mode=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_ble_send_periodic_msg_no_ack_v3_to_v5

    @staticmethod
    def test_rf_ble_send_periodic_msg_no_ack_v6_to_v9():
        """
        Tests RFBLESendPeriodicMsgNoAckV6Tov9 class instantiation
        """
        my_class = RFBLESendPeriodicMsgNoAckV6ToV9(
            device_index=0,
            feature_index=0,
            address=HexList('00' * (RFBLESendPeriodicMsgNoAckV6ToV9.LEN.ADDRESS // 8)),
            channel=0,
            power=0,
            period=0,
            condition=0,
            nbmsg=HexList('00' * (RFBLESendPeriodicMsgNoAckV6ToV9.LEN.NBMSG // 8)),
            radio_mode=0,
            payload_size=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFBLESendPeriodicMsgNoAckV6ToV9(
            device_index=0xFF,
            feature_index=0xFF,
            address=HexList('FF' * (RFBLESendPeriodicMsgNoAckV6ToV9.LEN.ADDRESS // 8)),
            channel=0xFF,
            power=0xFF,
            period=0xFF,
            condition=0xFF,
            nbmsg=HexList('FF' * (RFBLESendPeriodicMsgNoAckV6ToV9.LEN.NBMSG // 8)),
            radio_mode=0xFF,
            payload_size=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_ble_send_periodic_msg_no_ack_v6_to_v9

    @staticmethod
    def test_rf_ble_receive_periodic_msg_v2():
        """
        Tests RFBLEReceivePeriodicMsgV2 class instantiation
        """
        my_class = RFBLEReceivePeriodicMsgV2(
            device_index=0,
            feature_index=0,
            address=HexList('00' * (RFBLEReceivePeriodicMsgV2.LEN.ADDRESS // 8)),
            channel=0,
            power=0,
            condition=0,
            timeout=HexList('00' * (RFBLEReceivePeriodicMsgV2.LEN.TIMEOUT // 8)),)

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFBLEReceivePeriodicMsgV2(
            device_index=0xFF,
            feature_index=0xFF,
            address=HexList('FF' * (RFBLEReceivePeriodicMsgV2.LEN.ADDRESS // 8)),
            channel=0xFF,
            power=0xFF,
            condition=0xFF,
            timeout=HexList('FF' * (RFBLEReceivePeriodicMsgV2.LEN.TIMEOUT // 8)),)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_ble_receive_periodic_msg_v2

    @staticmethod
    def test_rf_ble_receive_periodic_msg_v3_to_v9():
        """
        Tests RFBLEReceivePeriodicMsgV3ToV9 class instantiation
        """
        my_class = RFBLEReceivePeriodicMsgV3ToV9(
            device_index=0,
            feature_index=0,
            address=HexList('00' * (RFBLEReceivePeriodicMsgV3ToV9.LEN.ADDRESS // 8)),
            channel=0,
            power=0,
            condition=0,
            timeout=HexList('00' * (RFBLEReceivePeriodicMsgV3ToV9.LEN.TIMEOUT // 8)),
            radio_mode=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFBLEReceivePeriodicMsgV3ToV9(
            device_index=0xFF,
            feature_index=0xFF,
            address=HexList('FF' * (RFBLEReceivePeriodicMsgV3ToV9.LEN.ADDRESS // 8)),
            channel=0xFF,
            power=0xFF,
            condition=0xFF,
            timeout=HexList('FF' * (RFBLEReceivePeriodicMsgV3ToV9.LEN.TIMEOUT // 8)),
            radio_mode=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_ble_receive_periodic_msg_v3_to_v9

    @staticmethod
    def test_rf_ble_send_periodic_full_duty_msg_v9():
        """
        Tests RFBLESendPeriodicFullDutyMsgV9 class instantiation
        """
        my_class = RFBLESendPeriodicFullDutyMsgV9(
            device_index=0,
            feature_index=0,
            channel=0,
            power=0,
            timeout=HexList('00' * (RFBLESendPeriodicFullDutyMsgV9.LEN.TIMEOUT // 8)),
            condition=0,
            radio_mode=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFBLESendPeriodicFullDutyMsgV9(
            device_index=0xFF,
            feature_index=0xFF,
            channel=0xFF,
            power=0xFF,
            timeout=HexList('FF' * (RFBLESendPeriodicFullDutyMsgV9.LEN.TIMEOUT // 8)),
            condition=0xFF,
            radio_mode=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_ble_send_periodic_full_duty_msg_v9

    @staticmethod
    def test_rf_ble_send_periodic_full_duty_msg_response_v9():
        """
        Tests RFBLESendPeriodicFullDutyMsgResponseV9 class instantiation
        """
        my_class = RFBLESendPeriodicFullDutyMsgResponseV9(
            device_index=0,
            feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = RFBLESendPeriodicFullDutyMsgResponseV9(
            device_index=0xFF,
            feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_rf_ble_send_periodic_full_duty_msg_response_v9
# end class RFTestBLEInstantiationTestCase


class RFTestBLETestCase(TestCase):
    """
    RF Test factory testing
    """
    @classmethod
    def setUpClass(cls):
        cls.expected = {
            0: {
                "cls": RFTestBLEV0,
                "interfaces": {
                    "rf_send_periodic_msg_cls": RFBLESendPeriodicMsgV0ToV2,
                    "rf_send_periodic_msg_response_cls": RFBLESendPeriodicMsgResponseV0ToV9,
                    "rf_tx_cw_cls": RFBLETxCWV0ToV5,
                    "rf_rx_continuous_cls": RFBLERxContinuousV0ToV5,
                    "set_rf_tx_cw_sweep_cls": SetRfBLETxCWSweepV0ToV5,
                    "set_rf_rx_continuous_sweep_cls": SetRfBLERxContinuousSweepV0ToV5,
                    "rf_tx_cw_response_cls": None,
                    "rf_rx_continuous_response_cls": None,
                    "set_rf_tx_cw_sweep_response_cls": None,
                    "set_rf_rx_continuous_sweep_response_cls": None,
                },
                "max_function_index": 4
            },
            1: {
                "cls": RFTestBLEV1,
                "interfaces": {
                    "rf_send_periodic_msg_cls": RFBLESendPeriodicMsgV0ToV2,
                    "rf_send_periodic_msg_response_cls": RFBLESendPeriodicMsgResponseV0ToV9,
                    "rf_tx_cw_cls": RFBLETxCWV0ToV5,
                    "rf_rx_continuous_cls": RFBLERxContinuousV0ToV5,
                    "set_rf_tx_cw_sweep_cls": SetRfBLETxCWSweepV0ToV5,
                    "set_rf_rx_continuous_sweep_cls": SetRfBLERxContinuousSweepV0ToV5,
                    "rf_send_periodic_msg_no_ack_cls": RFBLESendPeriodicMsgNoAckV1ToV2,
                    "rf_tx_cw_response_cls": None,
                    "rf_rx_continuous_response_cls": None,
                    "set_rf_tx_cw_sweep_response_cls": None,
                    "set_rf_rx_continuous_sweep_response_cls": None,
                    "rf_send_periodic_msg_no_ack_response_cls": None,
                },
                "max_function_index": 5
            },
            2: {
                "cls": RFTestBLEV2,
                "interfaces": {
                    "rf_send_periodic_msg_cls": RFBLESendPeriodicMsgV0ToV2,
                    "rf_send_periodic_msg_response_cls": RFBLESendPeriodicMsgResponseV0ToV9,
                    "rf_tx_cw_cls": RFBLETxCWV0ToV5,
                    "rf_rx_continuous_cls": RFBLERxContinuousV0ToV5,
                    "set_rf_tx_cw_sweep_cls": SetRfBLETxCWSweepV0ToV5,
                    "set_rf_rx_continuous_sweep_cls": SetRfBLERxContinuousSweepV0ToV5,
                    "rf_send_periodic_msg_no_ack_cls": RFBLESendPeriodicMsgNoAckV1ToV2,
                    "rf_receive_periodic_msg_cls": RFBLEReceivePeriodicMsgV2,
                    "rf_tx_cw_response_cls": None,
                    "rf_rx_continuous_response_cls": None,
                    "set_rf_tx_cw_sweep_response_cls": None,
                    "set_rf_rx_continuous_sweep_response_cls": None,
                    "rf_send_periodic_msg_no_ack_response_cls": None,
                    "rf_receive_periodic_msg_response_cls": None,
                },
                "max_function_index": 6
            },
            3: {
                "cls": RFTestBLEV3,
                "interfaces": {
                    "rf_send_periodic_msg_cls": RFBLESendPeriodicMsgV3ToV5,
                    "rf_send_periodic_msg_response_cls": RFBLESendPeriodicMsgResponseV0ToV9,
                    "rf_tx_cw_cls": RFBLETxCWV0ToV5,
                    "rf_rx_continuous_cls": RFBLERxContinuousV0ToV5,
                    "set_rf_tx_cw_sweep_cls": SetRfBLETxCWSweepV0ToV5,
                    "set_rf_rx_continuous_sweep_cls": SetRfBLERxContinuousSweepV0ToV5,
                    "rf_send_periodic_msg_no_ack_cls": RFBLESendPeriodicMsgNoAckV3ToV5,
                    "rf_receive_periodic_msg_cls": RFBLEReceivePeriodicMsgV3ToV9,
                    "rf_tx_cw_response_cls": None,
                    "rf_rx_continuous_response_cls": None,
                    "set_rf_tx_cw_sweep_response_cls": None,
                    "set_rf_rx_continuous_sweep_response_cls": None,
                    "rf_send_periodic_msg_no_ack_response_cls": None,
                    "rf_receive_periodic_msg_response_cls": None,
                },
                "max_function_index": 6
            },
            4: {
                "cls": RFTestBLEV4,
                "interfaces": {
                    "rf_send_periodic_msg_cls": RFBLESendPeriodicMsgV3ToV5,
                    "rf_send_periodic_msg_response_cls": RFBLESendPeriodicMsgResponseV0ToV9,
                    "rf_tx_cw_cls": RFBLETxCWV0ToV5,
                    "rf_rx_continuous_cls": RFBLERxContinuousV0ToV5,
                    "set_rf_tx_cw_sweep_cls": SetRfBLETxCWSweepV0ToV5,
                    "set_rf_rx_continuous_sweep_cls": SetRfBLERxContinuousSweepV0ToV5,
                    "rf_send_periodic_msg_no_ack_cls": RFBLESendPeriodicMsgNoAckV3ToV5,
                    "rf_receive_periodic_msg_cls": RFBLEReceivePeriodicMsgV3ToV9,
                    "rf_tx_cw_response_cls": None,
                    "rf_rx_continuous_response_cls": None,
                    "set_rf_tx_cw_sweep_response_cls": None,
                    "set_rf_rx_continuous_sweep_response_cls": None,
                    "rf_send_periodic_msg_no_ack_response_cls": None,
                    "rf_receive_periodic_msg_response_cls": None,
                },
                "max_function_index": 6
            },
            5: {
                "cls": RFTestBLEV5,
                "interfaces": {
                    "rf_send_periodic_msg_cls": RFBLESendPeriodicMsgV3ToV5,
                    "rf_send_periodic_msg_response_cls": RFBLESendPeriodicMsgResponseV0ToV9,
                    "rf_tx_cw_cls": RFBLETxCWV0ToV5,
                    "rf_rx_continuous_cls": RFBLERxContinuousV0ToV5,
                    "set_rf_tx_cw_sweep_cls": SetRfBLETxCWSweepV0ToV5,
                    "set_rf_rx_continuous_sweep_cls": SetRfBLERxContinuousSweepV0ToV5,
                    "rf_send_periodic_msg_no_ack_cls": RFBLESendPeriodicMsgNoAckV3ToV5,
                    "rf_receive_periodic_msg_cls": RFBLEReceivePeriodicMsgV3ToV9,
                    "rf_tx_cw_response_cls": None,
                    "rf_rx_continuous_response_cls": None,
                    "set_rf_tx_cw_sweep_response_cls": None,
                    "set_rf_rx_continuous_sweep_response_cls": None,
                    "rf_send_periodic_msg_no_ack_response_cls": None,
                    "rf_receive_periodic_msg_response_cls": None,

                },
                "max_function_index": 6
            },
            6: {
                "cls": RFTestBLEV6,
                "interfaces": {
                    "rf_send_periodic_msg_cls": RFBLESendPeriodicMsgV6ToV9,
                    "rf_send_periodic_msg_response_cls": RFBLESendPeriodicMsgResponseV0ToV9,
                    "rf_tx_cw_cls": RFBLETxCWV6ToV9,
                    "rf_rx_continuous_cls": RFBLERxContinuousV6ToV9,
                    "set_rf_tx_cw_sweep_cls": SetRfBLETxCWSweepV6,
                    "set_rf_rx_continuous_sweep_cls": SetRfBLERxContinuousSweepV6,
                    "rf_send_periodic_msg_no_ack_cls": RFBLESendPeriodicMsgNoAckV6ToV9,
                    "rf_receive_periodic_msg_cls": RFBLEReceivePeriodicMsgV3ToV9,
                    "rf_tx_cw_response_cls": None,
                    "rf_rx_continuous_response_cls": None,
                    "set_rf_tx_cw_sweep_response_cls": None,
                    "set_rf_rx_continuous_sweep_response_cls": None,
                    "rf_send_periodic_msg_no_ack_response_cls": None,
                    "rf_receive_periodic_msg_response_cls": None,

                },
                "max_function_index": 6
            },
            7: {
                "cls": RFTestBLEV7,
                "interfaces": {
                    "rf_send_periodic_msg_cls": RFBLESendPeriodicMsgV6ToV9,
                    "rf_send_periodic_msg_response_cls": RFBLESendPeriodicMsgResponseV0ToV9,
                    "rf_tx_cw_cls": RFBLETxCWV6ToV9,
                    "rf_rx_continuous_cls": RFBLERxContinuousV6ToV9,
                    "set_rf_tx_cw_sweep_cls": SetRfBLETxCWSweepV7ToV9,
                    "set_rf_rx_continuous_sweep_cls": SetRfBLERxContinuousSweepV7ToV9,
                    "rf_send_periodic_msg_no_ack_cls": RFBLESendPeriodicMsgNoAckV6ToV9,
                    "rf_receive_periodic_msg_cls": RFBLEReceivePeriodicMsgV3ToV9,
                    "rf_tx_cw_response_cls": None,
                    "rf_rx_continuous_response_cls": None,
                    "set_rf_tx_cw_sweep_response_cls": None,
                    "set_rf_rx_continuous_sweep_response_cls": None,
                    "rf_send_periodic_msg_no_ack_response_cls": None,
                    "rf_receive_periodic_msg_response_cls": None,

                },
                "max_function_index": 6
            },
            8: {
                "cls": RFTestBLEV8,
                "interfaces": {
                    "rf_send_periodic_msg_cls": RFBLESendPeriodicMsgV6ToV9,
                    "rf_send_periodic_msg_response_cls": RFBLESendPeriodicMsgResponseV0ToV9,
                    "rf_tx_cw_cls": RFBLETxCWV6ToV9,
                    "rf_rx_continuous_cls": RFBLERxContinuousV6ToV9,
                    "set_rf_tx_cw_sweep_cls": SetRfBLETxCWSweepV7ToV9,
                    "set_rf_rx_continuous_sweep_cls": SetRfBLERxContinuousSweepV7ToV9,
                    "rf_send_periodic_msg_no_ack_cls": RFBLESendPeriodicMsgNoAckV6ToV9,
                    "rf_receive_periodic_msg_cls": RFBLEReceivePeriodicMsgV3ToV9,
                    "rf_tx_cw_response_cls": None,
                    "rf_rx_continuous_response_cls": None,
                    "set_rf_tx_cw_sweep_response_cls": None,
                    "set_rf_rx_continuous_sweep_response_cls": None,
                    "rf_send_periodic_msg_no_ack_response_cls": None,
                    "rf_receive_periodic_msg_response_cls": None,

                },
                "max_function_index": 6
            },
            9: {
                "cls": RFTestBLEV9,
                "interfaces": {
                    "rf_send_periodic_msg_cls": RFBLESendPeriodicMsgV6ToV9,
                    "rf_send_periodic_msg_response_cls": RFBLESendPeriodicMsgResponseV0ToV9,
                    "rf_tx_cw_cls": RFBLETxCWV6ToV9,
                    "rf_rx_continuous_cls": RFBLERxContinuousV6ToV9,
                    "set_rf_tx_cw_sweep_cls": SetRfBLETxCWSweepV7ToV9,
                    "set_rf_rx_continuous_sweep_cls": SetRfBLERxContinuousSweepV7ToV9,
                    "rf_send_periodic_msg_no_ack_cls": RFBLESendPeriodicMsgNoAckV6ToV9,
                    "rf_receive_periodic_msg_cls": RFBLEReceivePeriodicMsgV3ToV9,
                    "rf_tx_cw_response_cls": None,
                    "rf_rx_continuous_response_cls": None,
                    "set_rf_tx_cw_sweep_response_cls": None,
                    "set_rf_rx_continuous_sweep_response_cls": None,
                    "rf_send_periodic_msg_no_ack_response_cls": None,
                    "rf_receive_periodic_msg_response_cls": None,
                    "rf_send_periodic_full_duty_msg_cls": RFBLESendPeriodicFullDutyMsgV9,
                    "rf_send_periodic_full_duty_msg_response_cls": RFBLESendPeriodicFullDutyMsgResponseV9,
                },
                "max_function_index": 7
            },
        }
    # end def setUpClass

    def test_rf_test_factory(self):
        """
        Tests RFTestBLEFactory
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(RFTestBLEFactory.create(version)), expected["cls"])
        # end for loop
    # end def test_rf_test_factory

    def test_rf_test_factory_version_out_of_range(self):
        """
        Tests RFTestBLEFactory with out of range versions
        """
        for version in [-1, 10]:
            with self.assertRaises(KeyError):
                RFTestBLEFactory.create(version)
    # end def test_rf_test_factory_version_out_of_range

    def test_rf_test_factory_interfaces(self):
        """
        Check RFTestBLEFactory returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            rf_test = RFTestBLEFactory.create(version)
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
            rf_test = RFTestBLEFactory.create(version)
            self.assertEqual(rf_test.get_max_function_index(), expected["max_function_index"])
        # end for loop
    # end def test_get_max_function_index
# end class RFTestBLETestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
