#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.common.rftest
:brief: HID++ 2.0 ``RFTest`` command interface definition
:author: Jerry Lin
:date: 2020/03/09
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC

from pyhid.bitfield import BitField
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidppmessage import TYPE
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class RFTest(HidppMessage):
    """
    The purpose of this feature is for compliance RF approval test. 
    """
    FEATURE_ID = 0x1890
    MAX_FUNCTION_INDEX_V0 = 4
    MAX_FUNCTION_INDEX_V1 = 5
    MAX_FUNCTION_INDEX_V2ToV8 = 6
    MAX_FUNCTION_INDEX_V9 = 7

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, **kwargs)
    # end def __init__
# end class RFTest


class RFTestModel(FeatureModel):
    """
    Define ``RFTest`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        RF_SEND_PERIODIC_MSG = 0
        RF_TX_CW = 1
        RF_RX_CONTINUOUS = 2
        SET_RF_TX_CW_SWEEP = 3
        SET_RF_RX_CONTINUOUS_SWEEP = 4
        RF_SEND_PERIODIC_MSG_NO_ACK = 5
        RF_RECEIVE_PERIODIC_MSG = 6
        RF_SEND_PERIODIC_FULL_DUTY_MSG = 7
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``RFTest`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        return {
            "feature_base": RFTest,
            "versions": {
                RFTestV0.VERSION: {
                    "main_cls": RFTestV0,
                    "api": {
                        "functions": {
                            cls.INDEX.RF_SEND_PERIODIC_MSG: {"request": RFSendPeriodicMsgV0ToV2,
                                                             "response": RFSendPeriodicMsgResponseV0ToV9},
                            cls.INDEX.RF_TX_CW: {"request": RFTxCWV0ToV5, "response": RFTxCWResponseV0ToV9, },
                            cls.INDEX.RF_RX_CONTINUOUS: {"request": RFRxContinuousV0ToV5,
                                                         "response": RFRxContinuousResponseV0ToV9, },
                            cls.INDEX.SET_RF_TX_CW_SWEEP: {"request": SetRfTxCWSweepV0ToV5,
                                                           "response": SetRfTxCWSweepResponseV0ToV9, },
                            cls.INDEX.SET_RF_RX_CONTINUOUS_SWEEP: {"request": SetRfRxContinuousSweepV0ToV5,
                                                                   "response": SetRfRxContinuousSweepResponseV0ToV9, },
                        }
                    },
                },
                RFTestV1.VERSION: {
                    "main_cls": RFTestV1,
                    "api": {
                        "functions": {
                            cls.INDEX.RF_SEND_PERIODIC_MSG: {"request": RFSendPeriodicMsgV0ToV2,
                                                             "response": RFSendPeriodicMsgResponseV0ToV9},
                            cls.INDEX.RF_TX_CW: {"request": RFTxCWV0ToV5, "response": RFTxCWResponseV0ToV9, },
                            cls.INDEX.RF_RX_CONTINUOUS: {"request": RFRxContinuousV0ToV5,
                                                         "response": RFRxContinuousResponseV0ToV9, },
                            cls.INDEX.SET_RF_TX_CW_SWEEP: {"request": SetRfTxCWSweepV0ToV5,
                                                           "response": SetRfTxCWSweepResponseV0ToV9, },
                            cls.INDEX.SET_RF_RX_CONTINUOUS_SWEEP: {"request": SetRfRxContinuousSweepV0ToV5,
                                                                   "response": SetRfRxContinuousSweepResponseV0ToV9, },
                            cls.INDEX.RF_SEND_PERIODIC_MSG_NO_ACK: {"request": RFSendPeriodicMsgNoAckV1ToV2,
                                                                    "response": RFSendPeriodicMsgNoAckResponseV1ToV9, },
                        }
                    },
                },
                RFTestV2.VERSION: {
                    "main_cls": RFTestV2,
                    "api": {
                        "functions": {
                            cls.INDEX.RF_SEND_PERIODIC_MSG: {"request": RFSendPeriodicMsgV0ToV2,
                                                             "response": RFSendPeriodicMsgResponseV0ToV9},
                            cls.INDEX.RF_TX_CW: {"request": RFTxCWV0ToV5, "response": RFTxCWResponseV0ToV9, },
                            cls.INDEX.RF_RX_CONTINUOUS: {"request": RFRxContinuousV0ToV5,
                                                         "response": RFRxContinuousResponseV0ToV9, },
                            cls.INDEX.SET_RF_TX_CW_SWEEP: {"request": SetRfTxCWSweepV0ToV5,
                                                           "response": SetRfTxCWSweepResponseV0ToV9, },
                            cls.INDEX.SET_RF_RX_CONTINUOUS_SWEEP: {"request": SetRfRxContinuousSweepV0ToV5,
                                                                   "response": SetRfRxContinuousSweepResponseV0ToV9, },
                            cls.INDEX.RF_SEND_PERIODIC_MSG_NO_ACK: {"request": RFSendPeriodicMsgNoAckV1ToV2,
                                                                    "response": RFSendPeriodicMsgNoAckResponseV1ToV9, },
                            cls.INDEX.RF_RECEIVE_PERIODIC_MSG: {"request": RFReceivePeriodicMsgV2,
                                                                "response": RFReceivePeriodicMsgResponseV2ToV9, },
                        }
                    },
                },
                RFTestV3.VERSION: {
                    "main_cls": RFTestV3,
                    "api": {
                        "functions": {
                            cls.INDEX.RF_SEND_PERIODIC_MSG: {"request": RFSendPeriodicMsgV3ToV5,
                                                             "response": RFSendPeriodicMsgResponseV0ToV9},
                            cls.INDEX.RF_TX_CW: {"request": RFTxCWV0ToV5, "response": RFTxCWResponseV0ToV9, },
                            cls.INDEX.RF_RX_CONTINUOUS: {"request": RFRxContinuousV0ToV5,
                                                         "response": RFRxContinuousResponseV0ToV9, },
                            cls.INDEX.SET_RF_TX_CW_SWEEP: {"request": SetRfTxCWSweepV0ToV5,
                                                           "response": SetRfTxCWSweepResponseV0ToV9, },
                            cls.INDEX.SET_RF_RX_CONTINUOUS_SWEEP: {"request": SetRfRxContinuousSweepV0ToV5,
                                                                   "response": SetRfRxContinuousSweepResponseV0ToV9, },
                            cls.INDEX.RF_SEND_PERIODIC_MSG_NO_ACK: {"request": RFSendPeriodicMsgNoAckV3ToV5,
                                                                    "response": RFSendPeriodicMsgNoAckResponseV1ToV9, },
                            cls.INDEX.RF_RECEIVE_PERIODIC_MSG: {"request": RFReceivePeriodicMsgV3ToV9,
                                                                "response": RFReceivePeriodicMsgResponseV2ToV9, },
                        }
                    },
                },
                RFTestV4.VERSION: {
                    "main_cls": RFTestV4,
                    "api": {
                        "functions": {
                            cls.INDEX.RF_SEND_PERIODIC_MSG: {"request": RFSendPeriodicMsgV3ToV5,
                                                             "response": RFSendPeriodicMsgResponseV0ToV9},
                            cls.INDEX.RF_TX_CW: {"request": RFTxCWV0ToV5, "response": RFTxCWResponseV0ToV9, },
                            cls.INDEX.RF_RX_CONTINUOUS: {"request": RFRxContinuousV0ToV5,
                                                         "response": RFRxContinuousResponseV0ToV9, },
                            cls.INDEX.SET_RF_TX_CW_SWEEP: {"request": SetRfTxCWSweepV0ToV5,
                                                           "response": SetRfTxCWSweepResponseV0ToV9, },
                            cls.INDEX.SET_RF_RX_CONTINUOUS_SWEEP: {"request": SetRfRxContinuousSweepV0ToV5,
                                                                   "response": SetRfRxContinuousSweepResponseV0ToV9, },
                            cls.INDEX.RF_SEND_PERIODIC_MSG_NO_ACK: {"request": RFSendPeriodicMsgNoAckV3ToV5,
                                                                    "response": RFSendPeriodicMsgNoAckResponseV1ToV9, },
                            cls.INDEX.RF_RECEIVE_PERIODIC_MSG: {"request": RFReceivePeriodicMsgV3ToV9,
                                                                "response": RFReceivePeriodicMsgResponseV2ToV9, },
                        }
                    },
                },
                RFTestV5.VERSION: {
                    "main_cls": RFTestV5,
                    "api": {
                        "functions": {
                            cls.INDEX.RF_SEND_PERIODIC_MSG: {"request": RFSendPeriodicMsgV3ToV5,
                                                             "response": RFSendPeriodicMsgResponseV0ToV9},
                            cls.INDEX.RF_TX_CW: {"request": RFTxCWV0ToV5, "response": RFTxCWResponseV0ToV9, },
                            cls.INDEX.RF_RX_CONTINUOUS: {"request": RFRxContinuousV0ToV5,
                                                         "response": RFRxContinuousResponseV0ToV9, },
                            cls.INDEX.SET_RF_TX_CW_SWEEP: {"request": SetRfTxCWSweepV0ToV5,
                                                           "response": SetRfTxCWSweepResponseV0ToV9, },
                            cls.INDEX.SET_RF_RX_CONTINUOUS_SWEEP: {"request": SetRfRxContinuousSweepV0ToV5,
                                                                   "response": SetRfRxContinuousSweepResponseV0ToV9, },
                            cls.INDEX.RF_SEND_PERIODIC_MSG_NO_ACK: {"request": RFSendPeriodicMsgNoAckV3ToV5,
                                                                    "response": RFSendPeriodicMsgNoAckResponseV1ToV9, },
                            cls.INDEX.RF_RECEIVE_PERIODIC_MSG: {"request": RFReceivePeriodicMsgV3ToV9,
                                                                "response": RFReceivePeriodicMsgResponseV2ToV9, },
                        }
                    },
                },
                RFTestV6.VERSION: {
                    "main_cls": RFTestV6,
                    "api": {
                        "functions": {
                            cls.INDEX.RF_SEND_PERIODIC_MSG: {"request": RFSendPeriodicMsgV6ToV9,
                                                             "response": RFSendPeriodicMsgResponseV0ToV9},
                            cls.INDEX.RF_TX_CW: {"request": RFTxCWV6ToV9, "response": RFTxCWResponseV0ToV9, },
                            cls.INDEX.RF_RX_CONTINUOUS: {"request": RFRxContinuousV6ToV9,
                                                         "response": RFRxContinuousResponseV0ToV9, },
                            cls.INDEX.SET_RF_TX_CW_SWEEP: {"request": SetRfTxCWSweepV6,
                                                           "response": SetRfTxCWSweepResponseV0ToV9, },
                            cls.INDEX.SET_RF_RX_CONTINUOUS_SWEEP: {"request": SetRfRxContinuousSweepV6,
                                                                   "response": SetRfRxContinuousSweepResponseV0ToV9, },
                            cls.INDEX.RF_SEND_PERIODIC_MSG_NO_ACK: {"request": RFSendPeriodicMsgNoAckV6ToV9,
                                                                    "response": RFSendPeriodicMsgNoAckResponseV1ToV9, },
                            cls.INDEX.RF_RECEIVE_PERIODIC_MSG: {"request": RFReceivePeriodicMsgV3ToV9,
                                                                "response": RFReceivePeriodicMsgResponseV2ToV9, },
                        }
                    },
                },
                RFTestV7.VERSION: {
                    "main_cls": RFTestV7,
                    "api": {
                        "functions": {
                            cls.INDEX.RF_SEND_PERIODIC_MSG: {"request": RFSendPeriodicMsgV6ToV9,
                                                             "response": RFSendPeriodicMsgResponseV0ToV9},
                            cls.INDEX.RF_TX_CW: {"request": RFTxCWV6ToV9, "response": RFTxCWResponseV0ToV9, },
                            cls.INDEX.RF_RX_CONTINUOUS: {"request": RFRxContinuousV6ToV9,
                                                         "response": RFRxContinuousResponseV0ToV9, },
                            cls.INDEX.SET_RF_TX_CW_SWEEP: {"request": SetRfTxCWSweepV7ToV9,
                                                           "response": SetRfTxCWSweepResponseV0ToV9, },
                            cls.INDEX.SET_RF_RX_CONTINUOUS_SWEEP: {"request": SetRfRxContinuousSweepV7ToV9,
                                                                   "response": SetRfRxContinuousSweepResponseV0ToV9, },
                            cls.INDEX.RF_SEND_PERIODIC_MSG_NO_ACK: {"request": RFSendPeriodicMsgNoAckV6ToV9,
                                                                    "response": RFSendPeriodicMsgNoAckResponseV1ToV9, },
                            cls.INDEX.RF_RECEIVE_PERIODIC_MSG: {"request": RFReceivePeriodicMsgV3ToV9,
                                                                "response": RFReceivePeriodicMsgResponseV2ToV9, },
                        }
                    },
                },
                RFTestV8.VERSION: {
                    "main_cls": RFTestV8,
                    "api": {
                        "functions": {
                            cls.INDEX.RF_SEND_PERIODIC_MSG: {"request": RFSendPeriodicMsgV6ToV9,
                                                             "response": RFSendPeriodicMsgResponseV0ToV9},
                            cls.INDEX.RF_TX_CW: {"request": RFTxCWV6ToV9, "response": RFTxCWResponseV0ToV9, },
                            cls.INDEX.RF_RX_CONTINUOUS: {"request": RFRxContinuousV6ToV9,
                                                         "response": RFRxContinuousResponseV0ToV9, },
                            cls.INDEX.SET_RF_TX_CW_SWEEP: {"request": SetRfTxCWSweepV7ToV9,
                                                           "response": SetRfTxCWSweepResponseV0ToV9, },
                            cls.INDEX.SET_RF_RX_CONTINUOUS_SWEEP: {"request": SetRfRxContinuousSweepV7ToV9,
                                                                   "response": SetRfRxContinuousSweepResponseV0ToV9, },
                            cls.INDEX.RF_SEND_PERIODIC_MSG_NO_ACK: {"request": RFSendPeriodicMsgNoAckV6ToV9,
                                                                    "response": RFSendPeriodicMsgNoAckResponseV1ToV9, },
                            cls.INDEX.RF_RECEIVE_PERIODIC_MSG: {"request": RFReceivePeriodicMsgV3ToV9,
                                                                "response": RFReceivePeriodicMsgResponseV2ToV9, },
                        }
                    },
                },
                RFTestV9.VERSION: {
                    "main_cls": RFTestV9,
                    "api": {
                        "functions": {
                            cls.INDEX.RF_SEND_PERIODIC_MSG: {"request": RFSendPeriodicMsgV6ToV9,
                                                             "response": RFSendPeriodicMsgResponseV0ToV9},
                            cls.INDEX.RF_TX_CW: {"request": RFTxCWV6ToV9, "response": RFTxCWResponseV0ToV9, },
                            cls.INDEX.RF_RX_CONTINUOUS: {"request": RFRxContinuousV6ToV9,
                                                         "response": RFRxContinuousResponseV0ToV9, },
                            cls.INDEX.SET_RF_TX_CW_SWEEP: {"request": SetRfTxCWSweepV7ToV9,
                                                           "response": SetRfTxCWSweepResponseV0ToV9, },
                            cls.INDEX.SET_RF_RX_CONTINUOUS_SWEEP: {"request": SetRfRxContinuousSweepV7ToV9,
                                                                   "response": SetRfRxContinuousSweepResponseV0ToV9, },
                            cls.INDEX.RF_SEND_PERIODIC_MSG_NO_ACK: {"request": RFSendPeriodicMsgNoAckV6ToV9,
                                                                    "response": RFSendPeriodicMsgNoAckResponseV1ToV9, },
                            cls.INDEX.RF_RECEIVE_PERIODIC_MSG: {"request": RFReceivePeriodicMsgV3ToV9,
                                                                "response": RFReceivePeriodicMsgResponseV2ToV9, },
                            cls.INDEX.RF_SEND_PERIODIC_FULL_DUTY_MSG: {
                                "request": RFSendPeriodicFullDutyMsgV9,
                                "response": RFSendPeriodicFullDutyMsgResponseV9, },
                        }
                    },
                },
            }
        }
    # end def _get_data_model
# end class RFTestModel


class RFTestFactory(FeatureFactory):
    """
    Get ``RFTest`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``RFTest`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``RFTestInterface``
        """
        return RFTestModel.get_main_cls(version)()
    # end def create
# end class RFTestFactory


class RFTestInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``RFTest``
    """

    def __init__(self):
        # Requests
        self.rf_send_periodic_msg_cls = None
        self.rf_tx_cw_cls = None
        self.rf_rx_continuous_cls = None
        self.set_rf_tx_cw_sweep_cls = None
        self.set_rf_rx_continuous_sweep_cls = None
        self.rf_send_periodic_msg_no_ack_cls = None
        self.rf_receive_periodic_msg_cls = None
        self.rf_send_periodic_full_duty_msg_cls = None

        # Responses
        self.rf_send_periodic_msg_response_cls = None
        self.rf_tx_cw_response_cls = None
        self.rf_rx_continuous_response_cls = None
        self.set_rf_tx_cw_sweep_response_cls = None
        self.set_rf_rx_continuous_sweep_response_cls = None
        self.rf_send_periodic_msg_no_ack_response_cls = None
        self.rf_receive_periodic_msg_response_cls = None
        self.rf_send_periodic_full_duty_msg_response_cls = None
    # end def __init__
# end class RFTestInterface


class RFTestV0(RFTestInterface):
    """
    Define ``RFTestV0`` feature

    This feature provides model and unit specific information for version 0

    [0] RFSendPeriodicMsg(address, channel, power, period, condition, nbmsg) -> Acked packet

    [1] RFTxCW(channel, power, timeout)

    [2] RFRxContinuous(channel, power, timeout)

    [3] SetRfTxCWSweep(channelmin, channelmax, sweepperiod, power, timeout)

    [4] SetRfRxContinuousSweep(address, channel, power, NbMessage)
    """
    VERSION = 0

    def __init__(self):
        # See ``RFTest.__init__``
        super().__init__()
        index = RFTestModel.INDEX

        # Requests
        self.rf_send_periodic_msg_cls = RFTestModel.get_request_cls(
            self.VERSION, index.RF_SEND_PERIODIC_MSG)
        self.rf_tx_cw_cls = RFTestModel.get_request_cls(
            self.VERSION, index.RF_TX_CW)
        self.rf_rx_continuous_cls = RFTestModel.get_request_cls(
            self.VERSION, index.RF_RX_CONTINUOUS)
        self.set_rf_tx_cw_sweep_cls = RFTestModel.get_request_cls(
            self.VERSION, index.SET_RF_TX_CW_SWEEP)
        self.set_rf_rx_continuous_sweep_cls = RFTestModel.get_request_cls(
            self.VERSION, index.SET_RF_RX_CONTINUOUS_SWEEP)

        # Responses
        self.rf_send_periodic_msg_response_cls = RFTestModel.get_response_cls(
            self.VERSION, index.RF_SEND_PERIODIC_MSG)
        self.rf_tx_cw_response_cls = RFTestModel.get_response_cls(
            self.VERSION, index.RF_TX_CW)
        self.rf_rx_continuous_response_cls = RFTestModel.get_response_cls(
            self.VERSION, index.RF_RX_CONTINUOUS)
        self.set_rf_tx_cw_sweep_response_cls = RFTestModel.get_response_cls(
            self.VERSION, index.SET_RF_TX_CW_SWEEP)
        self.set_rf_rx_continuous_sweep_response_cls = RFTestModel.get_response_cls(
            self.VERSION, index.SET_RF_RX_CONTINUOUS_SWEEP)
    # end def __init__

    def get_max_function_index(self):
        # See ``RFTestInterface.get_max_function_index``
        return RFTestModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class RFTestV0


class RFTestV1(RFTestV0):
    """
    Define ``RFTestV1`` feature

    This feature provides model and unit specific information for version 1


    [0] RFSendPeriodicMsg(address, channel, power, period, condition, nbmsg) -> Acked packet

    [1] RFTxCW(channel, power, timeout)

    [2] RFRxContinuous(channel, power, timeout)

    [3] SetRfTxCWSweep(channelmin, channelmax, sweepperiod, power, timeout)

    [4] SetRfRxContinuousSweep(address, channel, power, NbMessage)

    [5] RFSendPeriodicMsgNoAck(address, channel, power, period, condition, nbmsg)
    """
    VERSION = 1

    def __init__(self):
        # See ``RFTest.__init__``
        super().__init__()
        index = RFTestModel.INDEX

        # Requests
        self.rf_send_periodic_msg_no_ack_cls = RFTestModel.get_request_cls(
            self.VERSION, index.RF_SEND_PERIODIC_MSG_NO_ACK)

        # Responses
        self.rf_send_periodic_msg_no_ack_response_cls = RFTestModel.get_response_cls(
            self.VERSION, index.RF_SEND_PERIODIC_MSG_NO_ACK)
    # end def __init__

    def get_max_function_index(self):
        # See ``RFTestInterface.get_max_function_index``
        return RFTestModel.get_base_cls().MAX_FUNCTION_INDEX_V1
    # end def get_max_function_index
# end class RFTestV1


class RFTestV2(RFTestV1):
    """
    Define ``RFTestV2`` feature

    This feature provides model and unit specific information for version 2

    [0] RFSendPeriodicMsg(address, channel, power, period, condition, nbmsg) -> Acked packet

    [1] RFTxCW(channel, power, timeout)

    [2] RFRxContinuous(channel, power, timeout)

    [3] SetRfTxCWSweep(channelmin, channelmax, sweepperiod, power, timeout)

    [4] SetRfRxContinuousSweep(address, channel, power, NbMessage)

    [5] RFSendPeriodicMsgNoAck(address, channel, power, period, condition, nbmsg)

    [6] RFReceivePeriodicMsg(address, channel, power, condition, timeout)
    """
    VERSION = 2

    def __init__(self):
        # See ``RFTest.__init__``
        super().__init__()
        index = RFTestModel.INDEX

        # Requests
        self.rf_receive_periodic_msg_cls = RFTestModel.get_request_cls(
            self.VERSION, index.RF_RECEIVE_PERIODIC_MSG)

        # Responses
        self.rf_receive_periodic_msg_response_cls = RFTestModel.get_response_cls(
            self.VERSION, index.RF_RECEIVE_PERIODIC_MSG)
    # end def __init__

    def get_max_function_index(self):
        # See ``RFTestInterface.get_max_function_index``
        return RFTestModel.get_base_cls().MAX_FUNCTION_INDEX_V2ToV8
    # end def get_max_function_index
# end class RFTestV2


class RFTestV3(RFTestV2):
    """
    Define ``RFTestV3`` feature

    This feature provides model and unit specific information for version 3

    [0] RFSendPeriodicMsg(address, channel, power, period, condition, nbmsg, radiomode) -> Acked packet

    [1] RFTxCW(channel, power, timeout)

    [2] RFRxContinuous(channel, power, timeout)

    [3] SetRfTxCWSweep(channelmin, channelmax, power, sweepperiod)

    [4] SetRfRxContinuousSweep(channelMin, channelMax, power, sweepperiod)

    [5] RFSendPeriodicMsgNoAck(address, channel, power, period, condition, nbmsg, radiomode)

    [6] RFReceivePeriodicMsg(address, channel, power, condition, timeout, radiomode)
    """
    VERSION = 3
# end class RFTestV3


class RFTestV4(RFTestV2):
    """
    Define ``RFTestV4`` feature

    This feature provides model and unit specific information for version 4

    [0] RFSendPeriodicMsg(address, channel, power, period, condition, nbmsg, radiomode) -> Acked packet

    [1] RFTxCW(channel, power, timeout)

    [2] RFRxContinuous(channel, power, timeout)

    [3] SetRfTxCWSweep(channelmin, channelmax, power, sweepperiod)

    [4] SetRfRxContinuousSweep(channelMin, channelMax, power, sweepperiod)

    [5] RFSendPeriodicMsgNoAck(address, channel, power, period, condition, nbmsg, radiomode)

    [6] RFReceivePeriodicMsg(address, channel, power, condition, timeout, radiomode)
    """
    VERSION = 4
# end class RFTestV4


class RFTestV5(RFTestV2):
    """
    Define ``RFTestV5`` feature

    This feature provides model and unit specific information for version 5

    [0] RFSendPeriodicMsg(address, channel, power, period, condition, nbmsg, radiomode) -> Acked packet

    [1] RFTxCW(channel, power, timeout)

    [2] RFRxContinuous(channel, power, timeout)

    [3] SetRfTxCWSweep(channelmin, channelmax, power, sweepperiod)

    [4] SetRfRxContinuousSweep(channelMin, channelMax, power, sweepperiod)

    [5] RFSendPeriodicMsgNoAck(address, channel, power, period, condition, nbmsg, radiomode)

    [6] RFReceivePeriodicMsg(address, channel, power, condition, timeout, radiomode)
    """
    VERSION = 5
# end class RFTestV5


class RFTestV6(RFTestV5):
    """
    Define ``RFTestV6`` feature

    This feature provides model and unit specific information for version 6

    [0] RFSendPeriodicMsg(address, channel, power, period, condition, nbmsg, radiomode, payloadSize) -> Acked packet

    [1] RFTxCW(channel, power, timeout, condition, radiomode)

    [2] RFRxContinuous(channel, power, timeout, condition, radiomode)

    [3] SetRfTxCWSweep(channelmin, channelmax, power, sweepperiod, condition, radiomode)

    [4] SetRfRxContinuousSweep(channelMin, channelMax, power, sweepperiod, condition, radiomode)

    [5] RFSendPeriodicMsgNoAck(address, channel, power, period, condition, nbmsg, radiomode, payloadSize)

    [6] RFReceivePeriodicMsg(address, channel, power, condition, timeout, radiomode)
    """
    VERSION = 6
# end class RFTestV6


class RFTestV7(RFTestV6):
    """
    Define ``RFTestV7`` feature

    This feature provides model and unit specific information for version 7

    [0] RFSendPeriodicMsg(address, channel, power, period, condition, nbmsg, radiomode, payloadSize) -> Acked packet

    [1] RFTxCW(channel, power, timeout, condition, radiomode)

    [2] RFRxContinuous(channel, power, timeout, condition, radiomode)

    [3] SetRfTxCWSweep(channelmin, channelmax, power, sweepperiod, condition, radiomode, nbsweep)

    [4] SetRfRxContinuousSweep(channelMin, channelMax, power, sweepperiod, condition, radiomode, nbsweep)

    [5] RFSendPeriodicMsgNoAck(address, channel, power, period, condition, nbmsg, radiomode, payloadSize)

    [6] RFReceivePeriodicMsg(address, channel, power, condition, timeout, radiomode)
    """
    VERSION = 7
# end class RFTestV7


class RFTestV8(RFTestV6):
    """
    Define ``RFTestV8`` feature

    This feature provides model and unit specific information for version 8

    [0] RFSendPeriodicMsg(address, channel, power, period, condition, nbmsg, radiomode, payloadSize) -> Acked packet

    [1] RFTxCW(channel, power, timeout, condition, radiomode)

    [2] RFRxContinuous(channel, power, timeout, condition, radiomode)

    [3] SetRfTxCWSweep(channelmin, channelmax, power, sweepperiod, condition, radiomode, nbsweep)

    [4] SetRfRxContinuousSweep(channelMin, channelMax, power, sweepperiod, condition, radiomode, nbsweep)

    [5] RFSendPeriodicMsgNoAck(address, channel, power, period, condition, nbmsg, radiomode, payloadSize)

    [6] RFReceivePeriodicMsg(address, channel, power, condition, timeout, radiomode)
    """
    VERSION = 8
# end class RFTestV8


class RFTestV9(RFTestV8):
    """
    Define ``RFTestV9`` feature

    This feature provides model and unit specific information for version 9

    [0] RFSendPeriodicMsg(address, channel, power, period, condition, nbmsg, radiomode, payloadSize) -> Acked packet

    [1] RFTxCW(channel, power, timeout, condition, radiomode)

    [2] RFRxContinuous(channel, power, timeout, condition, radiomode)

    [3] SetRfTxCWSweep(channelmin, channelmax, power, sweepperiod, condition, radiomode, nbsweep)

    [4] SetRfRxContinuousSweep(channelMin, channelMax, power, sweepperiod, condition, radiomode, nbsweep)

    [5] RFSendPeriodicMsgNoAck(address, channel, power, period, condition, nbmsg, radiomode, payloadSize)

    [6] RFReceivePeriodicMsg(address, channel, power, condition, timeout, radiomode)

    [7] RFSendPeriodicFullDutyMsg(channel, power, timeout, condition, radiomode)
    """
    VERSION = 9

    def __init__(self):
        # See ``RFTest.__init__``
        super().__init__()
        index = RFTestModel.INDEX

        # Requests
        self.rf_send_periodic_full_duty_msg_cls = RFTestModel.get_request_cls(
            self.VERSION, index.RF_SEND_PERIODIC_FULL_DUTY_MSG)

        # Responses
        self.rf_send_periodic_full_duty_msg_response_cls = RFTestModel.get_response_cls(
            self.VERSION, index.RF_SEND_PERIODIC_FULL_DUTY_MSG)
    # end def __init__

    def get_max_function_index(self):
        # See ``RFTestInterface.get_max_function_index``
        return RFTestModel.get_base_cls().MAX_FUNCTION_INDEX_V9
    # end def get_max_function_index
# end class RFTest9


class LongEmptyPacketDataFormat(RFTest):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - RFTxCWResponse
        - RFRxContinuousResponse
        - SetRfTxCWSweepResponse
        - SetRfRxContinuousSweepResponse
        - RFSendPeriodicMsgNoAckResponse
        - RFReceivePeriodicMsgResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(RFTest.FID):
        # See ``RFTest.FID``
        PADDING = RFTest.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(RFTest.LEN):
        # See ``RFTest.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = RFTest.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RFTest.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class RFSendPeriodicMsgPacketDataFormat(RFTest):
    """
    This class is to be used as a base class for several messages in this feature.
        - RFSendPeriodicMsgV0ToV2
        - RFSendPeriodicMsgNoAckV0ToV2

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Address                       40
    Channel                       8
    Power                         8
    Period                        8
    Condition                     8
    NbMsg                         16
    Padding                       40
    ============================  ==========
    """

    class FID(RFTest.FID):
        # See ``RFTest.FID``
        ADDRESS = RFTest.FID.SOFTWARE_ID - 1
        CHANNEL = ADDRESS - 1
        POWER = CHANNEL - 1
        PERIOD = POWER - 1
        CONDITION = PERIOD - 1
        NBMSG = CONDITION - 1
        PADDING = NBMSG - 1
    # end class FID

    class LEN(RFTest.LEN):
        # See ``RFTest.LEN``
        ADDRESS = 0x28
        CHANNEL = 0x8
        POWER = 0x8
        PERIOD = 0x8
        CONDITION = 0x8
        NBMSG = 0x10
        PADDING = 0x28
    # end class LEN

    FIELDS = RFTest.FIELDS + (
        BitField(FID.ADDRESS,
                 LEN.ADDRESS,
                 title='Address',
                 name='address',
                 checks=(CheckHexList(LEN.ADDRESS // 8), CheckInt(),)),
        BitField(FID.CHANNEL,
                 LEN.CHANNEL,
                 title='Channel',
                 name='channel',
                 checks=(CheckHexList(LEN.CHANNEL // 8), CheckByte(),)),
        BitField(FID.POWER,
                 LEN.POWER,
                 title='Power',
                 name='power',
                 checks=(CheckHexList(LEN.POWER // 8), CheckByte(),)),
        BitField(FID.PERIOD,
                 LEN.PERIOD,
                 title='Period',
                 name='period',
                 checks=(CheckHexList(LEN.PERIOD // 8), CheckByte(),)),
        BitField(FID.CONDITION,
                 LEN.CONDITION,
                 title='Condition',
                 name='condition',
                 checks=(CheckHexList(LEN.CONDITION // 8), CheckByte(),)),
        BitField(FID.NBMSG,
                 LEN.NBMSG,
                 title='NbMsg',
                 name='nbmsg',
                 checks=(CheckHexList(LEN.NBMSG // 8), CheckInt(),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RFTest.DEFAULT.PADDING),
    )
# end class RFSendPeriodicMsgPacketDataFormat


class RFSendPeriodicMsgV0ToV2(RFSendPeriodicMsgPacketDataFormat):
    """
    RFTest RFSendPeriodicMsg implementation class for versions 0 to 2.

    Device sends periodic message.

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Address                       40
    Channel                       8
    Power                         8
    Period                        8
    Condition                     8
    NbMsg                         16
    Padding                       40
    ============================  ==========
    """
    VERSION = (0, 1, 2,)

    def __init__(self, device_index, feature_index, address=0, channel=0, power=0, period=0, condition=0, nbmsg=0,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param address: eQuad base and destination address
        :type address: ``HexList``
        :param channel: RF test channel
        :type channel: ``int`` or ``HexList``
        :param power: Output power
        :type power: ``int`` or ``HexList``
        :param period: 1ms per unit MSB first
        :type period: ``int`` or ``HexList``
        :param condition: Condition on how is sent the message
        :type condition: ``int`` or ``HexList``
        :param nbmsg: Number of message to be sent
        :type nbmsg: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=RFSendPeriodicMsgResponseV0ToV9.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        self.address = address
        self.channel = channel
        self.power = power
        self.period = period
        self.condition = condition
        self.nbmsg = nbmsg
    # end def __init__
# end class RFSendPeriodicMsgV0ToV2


class RFSendPeriodicMsgV3ToV5(RFSendPeriodicMsgV0ToV2):
    """
    RFTest RFSendPeriodicMsg implementation class for versions 3 to 5.

    Device sends periodic message.

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Channel                       8
    Power                         8
    Period                        8
    Condition                     8
    NbMsg                         16
    Radio Mode                    8
    Padding                       32
    ============================  ==========
    """
    VERSION = (3, 4, 5,)

    class FID(RFSendPeriodicMsgV0ToV2.FID):
        # See ``RFSendPeriodicMsgV0ToV2.FID``
        RADIO_MODE = RFSendPeriodicMsgV0ToV2.FID.NBMSG - 1
        PADDING = RADIO_MODE - 1
    # end class FID

    class LEN(RFSendPeriodicMsgV0ToV2.LEN):
        # See ``RFSendPeriodicMsgV0ToV2.LEN``
        RADIO_MODE = 0x8
        PADDING = 0x20
    # end class LEN

    FIELDS = RFSendPeriodicMsgV0ToV2.FIELDS[:-1] + (
        BitField(FID.RADIO_MODE,
                 LEN.RADIO_MODE,
                 title='Radio Mode',
                 name='radio_mode',
                 checks=(CheckHexList(LEN.RADIO_MODE // 8), CheckByte(),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RFTest.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, address=0, channel=0, power=0, period=0, condition=0, nbmsg=0,
                 radio_mode=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param address: eQuad base and destination address
        :type address: ``HexList``
        :param channel: RF test channel
        :type channel: ``int`` or ``HexList``
        :param power: Output power
        :type power: ``int`` or ``HexList``
        :param period: 1ms per unit MSB first
        :type period: ``int`` or ``HexList``
        :param condition: Condition on how is sent the message
        :type condition: ``int`` or ``HexList``
        :param nbmsg: Number of message to be sent
        :type nbmsg: ``HexList``
        :param radio_mode: Default / Unifying / Gaming
        :type radio_mode: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index, feature_index, address, channel, power, period, condition, nbmsg, **kwargs)
        self.radio_mode = radio_mode
    # end def __init__
# end class RFSendPeriodicMsgV3ToV5


class RFSendPeriodicMsgV6ToV9(RFSendPeriodicMsgV3ToV5):
    """
    RFTest RFSendPeriodicMsg implementation class for versions 6 to 9.

    Device sends periodic message.

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Address                       40
    Channel                       8
    Power                         8
    Period                        8
    Condition                     8
    NbMsg                         16
    Radio Mode                    8
    payloadSize                   8
    Padding                       24
    ============================  ==========
    """
    VERSION = (6, 7, 8, 9,)

    class FID(RFSendPeriodicMsgV3ToV5.FID):
        # See ``RFSendPeriodicMsgV3ToV5.FID``
        PAYLOAD_SIZE = 0xF3
        PADDING = 0xF2
    # end class FID

    class LEN(RFSendPeriodicMsgV3ToV5.LEN):
        # See ``RFSendPeriodicMsgV3ToV5.LEN``
        PAYLOAD_SIZE = 0x08
        PADDING = 0x18
    # end class LEN

    FIELDS = RFSendPeriodicMsgV3ToV5.FIELDS[:-1] + (
        BitField(FID.PAYLOAD_SIZE,
                 LEN.PAYLOAD_SIZE,
                 title='Payload Size',
                 name='payload_size',
                 checks=(CheckHexList(LEN.PAYLOAD_SIZE // 8), CheckByte(),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RFTest.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, address=0, channel=0, power=6, period=0, condition=0, nbmsg=0,
                 radio_mode=0, payload_size=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param address: eQuad base and destination address
        :type address: ``HexList``
        :param channel: RF test channel
        :type channel: ``int`` or ``HexList``
        :param power: Output power
        :type power: ``int`` or ``HexList``
        :param period: 1ms per unit MSB first
        :type period: ``int`` or ``HexList``
        :param condition: Condition on how is sent the message
        :type condition: ``int`` or ``HexList``
        :param nbmsg: Number of message to be sent
        :type nbmsg: ``HexList``
        :param radio_mode: Default / Unifying / Gaming
        :type radio_mode: ``int`` or ``HexList``
        :param payload_size: This parameter encodes the ESB pay-load size.
        :type payload_size: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index, feature_index, address, channel, power, period, condition, nbmsg, radio_mode,
                         **kwargs)
        self.payload_size = payload_size
    # end def __init__
# end class RFSendPeriodicMsgV6ToV9


class RFSendPeriodicMsgResponseV0ToV9(RFTest):
    """
    Define ``RFSendPeriodicMsgResponse`` implementation class for versions 0 to 9.

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    NbMsgAck                      16
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (RFSendPeriodicMsgV0ToV2, RFSendPeriodicMsgV3ToV5, RFSendPeriodicMsgV6ToV9)
    VERSION = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9,)
    FUNCTION_INDEX = 0

    class FID(RFTest.FID):
        # See ``RFTest.FID``
        NB_MSG_ACK = 0xFA
        PADDING = 0xF9
    # end class FID

    class LEN(RFTest.LEN):
        # See ``RFTest.LEN``
        NB_MSG_ACK = 0x10
        PADDING = 0x70
    # end class LEN

    FIELDS = RFTest.FIELDS + (
        BitField(FID.NB_MSG_ACK,
                 LEN.NB_MSG_ACK,
                 title='Nb_Msg_Ack',
                 name='nb_msg_ack',
                 checks=(CheckHexList(LEN.NB_MSG_ACK // 8), CheckInt(),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RFTest.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, nb_msg_ack=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param nb_msg_ack: number of message acknowledge
        :type nb_msg_ack: ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index, feature_index,
                         function_index=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.nb_msg_ack = nb_msg_ack
    # end def __init__
# end class RFSendPeriodicMsgResponseV0ToV9


class RFTxRxPacketDataFormat(RFTest):
    """
    This class is to be used as a base class for several messages in this feature.
        - RFTxCWV0ToV5
        - RFRxContinuousV0ToV5

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Channel                       8
    Power                         8
    Timeout                       16
    Padding                       96
    ============================  ==========
    """

    class FID(RFTest.FID):
        # See ``RFTest.FID``
        CHANNEL = 0xFA
        POWER = 0xF9
        TIMEOUT = 0xF8
        PADDING = 0xF7
    # end class FID

    class LEN(RFTest.LEN):
        # See ``RFTest.LEN``
        CHANNEL = 0x08
        POWER = 0x08
        TIMEOUT = 0x10
        PADDING = 0x60
    # end class LEN

    FIELDS = RFTest.FIELDS + (
        BitField(FID.CHANNEL,
                 LEN.CHANNEL,
                 title='Channel',
                 name='channel',
                 checks=(CheckHexList(LEN.CHANNEL // 8), CheckByte(),)),
        BitField(FID.POWER,
                 LEN.POWER,
                 title='Power',
                 name='power',
                 checks=(CheckHexList(LEN.POWER // 8), CheckByte(),)),
        BitField(FID.TIMEOUT,
                 LEN.TIMEOUT,
                 title='Timeout',
                 name='timeout',
                 checks=(CheckHexList(LEN.TIMEOUT // 8), CheckInt(),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RFTest.DEFAULT.PADDING),
    )
# end class RFTxRxPacketDataFormat


class RFTxCWV0ToV5(RFTxRxPacketDataFormat):
    """
    Define RFTest RFTxCW implementation class for versions 0 to 5.

    Device configures its transmitter to send a true continuous wave for a pre defined period of time.
    """
    VERSION = (0, 1, 2, 3, 4, 5,)

    def __init__(self, device_index, feature_index, channel=0, power=0, timeout=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param channel: RF test channel
        :type channel: ``int`` or ``HexList``
        :param power: Output power
        :type power: ``int`` or ``HexList``
        :param timeout: 10ms per unit
        :type timeout: ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=RFTxCWResponseV0ToV9.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG, **kwargs)
        self.channel = channel
        self.power = power
        self.timeout = timeout
    # end def __init__
# end class RFTxCWV0ToV5


class RFTxCWV6ToV9(RFTxCWV0ToV5):
    """
    RFTest RFTxCW implementation class for version 6 to 9.

    Device configures its transmitter to send a true continuous wave for a pre defined period of time.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Channel                       8
    Power                         8
    Timeout                       16
    Condition                     8
    Radio Mode                    8
    Padding                       80
    ============================  ==========
    """
    VERSION = (6, 7, 8, 9,)

    class FID(RFTxCWV0ToV5.FID):
        # See ``RFTxCWV0ToV5.FID``
        CONDITION = 0xF7
        RADIO_MODE = 0xF6
        PADDING = 0xF5
    # end class FID

    class LEN(RFTxCWV0ToV5.LEN):
        # See ``RFTxCWV0ToV5.LEN``
        CONDITION = 0x08
        RADIO_MODE = 0x08
        PADDING = 0x50
    # end class LEN

    FIELDS = RFTxCWV0ToV5.FIELDS[:-1] + (
        BitField(FID.CONDITION,
                 LEN.CONDITION,
                 title='Condition',
                 name='condition',
                 checks=(CheckHexList(LEN.CONDITION // 8), CheckByte(),)),
        BitField(FID.RADIO_MODE,
                 LEN.RADIO_MODE,
                 title='Radio Mode',
                 name='radio_mode',
                 checks=(CheckHexList(LEN.RADIO_MODE // 8), CheckByte(),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RFTest.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, channel=0, power=0, timeout=0, condition=0, radio_mode=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param channel: RF test channel
        :type channel: ``int`` or ``HexList``
        :param power: Output power
        :type power: ``int`` or ``HexList``
        :param timeout: 10ms per unit
        :type timeout: ``HexList``
        :param condition: Device dependent test condition
        :type condition: ``int`` or ``HexList``
        :param radio_mode: Indicates that the appropriate registers should be set to select the given mode.
        :type radio_mode: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index, feature_index, channel, power, timeout, **kwargs)
        self.condition = condition
        self.radio_mode = radio_mode
    # end def __init__
# end class RFTxCWV6ToV9


class RFTxCWResponseV0ToV9(LongEmptyPacketDataFormat):
    """
    Define ``RFTxCWResponse`` implementation class for versions 0 to 9
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (RFTxCWV0ToV5, RFTxCWV6ToV9,)
    VERSION = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class RFTxCWResponseV0ToV9


class RFRxContinuousV0ToV5(RFTxRxPacketDataFormat):
    """
    Define RFTest RFRxContinuous implementation class for versions 0 to 5.

    Device is configured as continuous receiving on a specified channel.
    """
    VERSION = (0, 1, 2, 3, 4, 5,)

    def __init__(self, device_index, feature_index, channel=0, power=0, timeout=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param channel: RF test channel
        :type channel: ``int`` or ``HexList``
        :param power: Output power
        :type power: ``int`` or ``HexList``
        :param timeout: 10ms per unit
        :type timeout: ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=RFRxContinuousResponseV0ToV9.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        self.channel = channel
        self.power = power
        self.timeout = timeout
    # end def __init__
# end class RFRxContinuousV0ToV5


class RFRxContinuousV6ToV9(RFRxContinuousV0ToV5):
    """
    RFTest RFRxContinuous implementation class for versions 6 to 9.

    Device is configured as continuous receiving on a specified channel.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Channel                       8
    Power                         8
    Timeout                       16
    Condition                     8
    Radio Mode                    8
    Padding                       80
    ============================  ==========
    """
    VERSION = (6, 7, 8, 9,)

    class FID(RFRxContinuousV0ToV5.FID):
        # See ``RFRxContinuousV0ToV5.FID``
        CONDITION = 0xF7
        RADIO_MODE = 0xF6
        PADDING = 0xF5
    # end class FID

    class LEN(RFRxContinuousV0ToV5.LEN):
        # See ``RFRxContinuousV0ToV5.LEN``
        CONDITION = 0x08
        RADIO_MODE = 0x08
        PADDING = 0x50
    # end class LEN

    FIELDS = RFRxContinuousV0ToV5.FIELDS[:-1] + (
        BitField(FID.CONDITION,
                 LEN.CONDITION,
                 title='Condition',
                 name='condition',
                 checks=(CheckHexList(LEN.CONDITION // 8), CheckByte(),)),
        BitField(FID.RADIO_MODE,
                 LEN.RADIO_MODE,
                 title='Radio Mode',
                 name='radio_mode',
                 checks=(CheckHexList(LEN.RADIO_MODE // 8), CheckByte(),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RFTest.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, channel=0, power=0, timeout=0, condition=0, radio_mode=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param channel: RF test channel
        :type channel: ``int`` or ``HexList``
        :param power: Output power
        :type power: ``int`` or ``HexList``
        :param timeout: 10ms per unit
        :type timeout: ``HexList``
        :param condition: Device dependent test condition
        :type condition: ``int`` or ``HexList``
        :param radio_mode: Indicates that the appropriate registers should be set to select the given mode.
        :type radio_mode: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index, feature_index, channel, power, timeout, **kwargs)
        self.condition = condition
        self.radio_mode = radio_mode
    # end def __init__
# end class RFRxContinuousV6ToV9


class RFRxContinuousResponseV0ToV9(LongEmptyPacketDataFormat):
    """
    Define ``RFRxContinuousResponse`` implementation class for versions 0 to 9
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (RFRxContinuousV0ToV5, RFRxContinuousV6ToV9,)
    VERSION = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9,)
    FUNCTION_INDEX = 2

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class RFRxContinuousResponseV0ToV9


class SetRfTxRxPacketDataFormat(RFTest):
    """
    This class is to be used as a base class for several messages in this feature.
        - SetRfTxCWSweepV0ToV5
        - SetRfRxContinuousSweepV0ToV5

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    ChannelMin                    8
    ChannelMax                    8
    Power                         8
    Sweep Period                  8
    Padding                       96
    ============================  ==========
    """

    class FID(RFTest.FID):
        # See ``RFTest.FID``
        CHANNEL_MIN = 0xFA
        CHANNEL_MAX = 0xF9
        POWER = 0xF8
        SWEEP_PERIOD = 0xF7
        PADDING = 0xF6
    # end class FID

    class LEN(RFTest.LEN):
        # See ``RFTest.LEN``
        CHANNEL_MIN = 0x08
        CHANNEL_MAX = 0x08
        POWER = 0x08
        SWEEP_PERIOD = 0x08
        PADDING = 0x60
    # end class LEN

    FIELDS = RFTest.FIELDS + (
        BitField(FID.CHANNEL_MIN,
                 LEN.CHANNEL_MIN,
                 title='ChannelMin',
                 name='channel_min',
                 checks=(CheckHexList(LEN.CHANNEL_MIN // 8), CheckByte(),)),
        BitField(FID.CHANNEL_MAX,
                 LEN.CHANNEL_MAX,
                 title='ChannelMAX',
                 name='channel_max',
                 checks=(CheckHexList(LEN.CHANNEL_MAX // 8), CheckByte(),)),
        BitField(FID.POWER,
                 LEN.POWER,
                 title='Power',
                 name='power',
                 checks=(CheckHexList(LEN.POWER // 8), CheckByte(),)),
        BitField(FID.SWEEP_PERIOD,
                 LEN.SWEEP_PERIOD,
                 title='Sweep Period',
                 name='sweep_period',
                 checks=(CheckHexList(LEN.SWEEP_PERIOD // 8), CheckByte(),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RFTest.DEFAULT.PADDING),
    )
# end class SetRfTxRx


class SetRfTxCWSweepV0ToV5(SetRfTxRxPacketDataFormat):
    """
    RFTest SetRfTxCWSweep implementation class for versions 0 to 5.

    Device configures its transmitter to send a true continuous wave
    for a pre defined period of time from channel min to channel max by step of 1 Mhz.
    """
    VERSION = (0, 1, 2, 3, 4, 5,)

    def __init__(self, device_index, feature_index, channel_min=0, channel_max=0, power=0, sweep_period=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param channel_min: Minimum channel
        :type channel_min: ``int`` or ``HexList``
        :param channel_max: Maximum channel
        :type channel_max: ``int`` or ``HexList``
        :param power: Output power
        :type power: ``int`` or ``HexList``
        :param sweep_period: 10ms per unit
        :type sweep_period: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetRfTxCWSweepResponseV0ToV9.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.channel_min = channel_min
        self.channel_max = channel_max
        self.power = power
        self.sweep_period = sweep_period
    # end def __init__
# end class SetRfTxCWSweepV0ToV5


class SetRfTxCWSweepV6(SetRfTxCWSweepV0ToV5):
    """
    RFTest SetRfTxCWSweep implementation class for version 6.

    Device configures its transmitter to send a true continuous wave
    for a pre defined period of time from channel min to channel max by step of 1 Mhz.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    ChannelMin                    8
    ChannelMax                    8
    Power                         8
    Sweep Period                  8
    Condition                     8
    Radio Mode                    8
    Padding                       80
    ============================  ==========
    """
    FUNCTION_INDEX = 3
    VERSION = (6,)

    class FID(SetRfTxCWSweepV0ToV5.FID):
        # See ``SetRfTxCWSweepV0ToV5.FID``
        CONDITION = 0xF6
        RADIO_MODE = 0xF5
        PADDING = 0xF4
    # end class FID

    class LEN(SetRfTxCWSweepV0ToV5.LEN):
        # See ``SetRfTxCWSweepV0ToV5.LEN``
        CONDITION = 0x08
        RADIO_MODE = 0x08
        PADDING = 0x50
    # end class LEN

    FIELDS = SetRfTxCWSweepV0ToV5.FIELDS[:-1] + (
        BitField(FID.CONDITION,
                 LEN.CONDITION,
                 title='Condition',
                 name='condition',
                 checks=(CheckHexList(LEN.CONDITION // 8), CheckByte(),)),
        BitField(FID.RADIO_MODE,
                 LEN.RADIO_MODE,
                 title='Radio Mode',
                 name='radio_mode',
                 checks=(CheckHexList(LEN.RADIO_MODE // 8), CheckByte(),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RFTest.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, channel_min=0, channel_max=0, power=0, sweep_period=0, condition=0,
                 radio_mode=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param channel_min: Minimum channel
        :type channel_min: ``int`` or ``HexList``
        :param channel_max: Maximum channel
        :type channel_max: ``int`` or ``HexList``
        :param power: Output power
        :type power: ``int`` or ``HexList``
        :param sweep_period: 10ms per unit
        :type sweep_period: ``int`` or ``HexList``
        :param condition: Device dependent test condition
        :type condition: ``int`` or ``HexList``
        :param radio_mode: Indicates that the appropriate registers should be set to select the given mode.
        :type radio_mode: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index, feature_index, channel_min, channel_max, power, sweep_period, **kwargs)
        self.condition = condition
        self.radio_mode = radio_mode
    # end def __init__
# end class SetRfTxCWSweepV6


class SetRfTxCWSweepV7ToV9(SetRfTxCWSweepV6):
    """
    RFTest SetRfTxCWSweep implementation class for versions 7 to 9

    Device configures its transmitter to send a true continuous wave
    for a pre defined period of time from channel min to channel max by step of 1 Mhz.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    ChannelMin                    8
    ChannelMax                    8
    Power                         8
    Sweep Period                  8
    Condition                     8
    Radio Mode                    8
    Nb Sweep                      16
    Padding                       64
    ============================  ==========
    """
    FUNCTION_INDEX = 3
    VERSION = (7, 8, 9,)

    class FID(SetRfTxCWSweepV6.FID):
        # See ``SetRfTxCWSweepV6.FID``
        NB_SWEEP = 0xF4
        PADDING = 0xF3
    # end class FID

    class LEN(SetRfTxCWSweepV6.LEN):
        # See ``SetRfTxCWSweepV6.LEN``
        NB_SWEEP = 0x10
        PADDING = 0x40
    # end class LEN

    FIELDS = SetRfTxCWSweepV6.FIELDS[:-1] + (
        BitField(FID.NB_SWEEP,
                 LEN.NB_SWEEP,
                 title='Nb Sweep',
                 name='nb_sweep',
                 aliases=('nbsweep',),
                 checks=(CheckHexList(LEN.NB_SWEEP // 8), CheckInt(),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RFTest.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, channel_min=0, channel_max=0, power=0, sweep_period=0, condition=0,
                 radio_mode=0, nb_sweep=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param channel_min: Minimum channel
        :type channel_min: ``int`` or ``HexList``
        :param channel_max: Maximum channel
        :type channel_max: ``int`` or ``HexList``
        :param power: Output power
        :type power: ``int`` or ``HexList``
        :param sweep_period: 10ms per unit
        :type sweep_period: ``int`` or ``HexList``
        :param condition: Device dependent test condition
        :type condition: ``int`` or ``HexList``
        :param radio_mode: Indicates that the appropriate registers should be set to select the given mode.
        :type radio_mode: ``int`` or ``HexList``
        :param nb_sweep: Number of full sweeps to be executed.
        :type nb_sweep: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index, feature_index, channel_min, channel_max, power, sweep_period, condition,
                         radio_mode, **kwargs)
        self.nb_sweep = nb_sweep
    # end def __init__
# end class SetRfTxCWSweepV7ToV9


class SetRfTxCWSweepResponseV0ToV9(LongEmptyPacketDataFormat):
    """
    Define ``SetRfTxCWSweepResponse`` implementation class for versions 0 to 9
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetRfTxCWSweepV0ToV5, SetRfTxCWSweepV6, SetRfTxCWSweepV7ToV9,)
    VERSION = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9,)
    FUNCTION_INDEX = 3

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class SetRfTxCWSweepResponseV0ToV9


class SetRfRxContinuousSweepV0ToV5(SetRfTxRxPacketDataFormat):
    """
    Define ``SetRfRxContinuousSweep`` implementation class for versions 0 to 5.

    Device configures its radio to receive for a pre defined period of time
    from channel min to channel max by step of 1 Mhz.
    """

    def __init__(self, device_index, feature_index, channel_min=0, channel_max=0, power=0, sweep_period=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param channel_min: Minimum channel
        :type channel_min: ``int`` or ``HexList``
        :param channel_max: Maximum channel
        :type channel_max: ``int`` or ``HexList``
        :param power: Output power
        :type power: ``int`` or ``HexList``
        :param sweep_period: 10ms per unit
        :type sweep_period: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetRfRxContinuousSweepResponseV0ToV9.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        self.channel_min = channel_min
        self.channel_max = channel_max
        self.power = power
        self.sweep_period = sweep_period
    # end def __init__
# end class SetRfRxContinuousSweepV0ToV5


class SetRfRxContinuousSweepV6(SetRfRxContinuousSweepV0ToV5):
    """
    Define ``SetRfRxContinuousSweep`` implementation class for version 6.

    Device configures its radio to receive for a pre defined period of time
    from channel min to channel max by step of 1 Mhz.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    ChannelMin                    8
    ChannelMax                    8
    Power                         8
    Sweep Period                  8
    Condition                     8
    Radio Mode                    8
    Padding                       80
    ============================  ==========
    """
    VERSION = (6,)

    class FID(SetRfRxContinuousSweepV0ToV5.FID):
        # See ``SetRfRxContinuousSweepV0ToV5.FID``
        CONDITION = 0xF6
        RADIO_MODE = 0xF5
        PADDING = 0xF4
    # end class FID

    class LEN(SetRfRxContinuousSweepV0ToV5.LEN):
        # See ``SetRfRxContinuousSweepV0ToV5.LEN``
        CONDITION = 0x08
        RADIO_MODE = 0x08
        PADDING = 0x50
    # end class LEN

    FIELDS = SetRfRxContinuousSweepV0ToV5.FIELDS[:-1] + (
        BitField(FID.CONDITION,
                 LEN.CONDITION,
                 title='Condition',
                 name='condition',
                 checks=(CheckHexList(LEN.CONDITION // 8), CheckByte(),)),
        BitField(FID.RADIO_MODE,
                 LEN.RADIO_MODE,
                 title='Radio Mode',
                 name='radio_mode',
                 checks=(CheckHexList(LEN.RADIO_MODE // 8), CheckByte(),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RFTest.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, channel_min=0, channel_max=0, power=0, sweep_period=0, condition=0,
                 radio_mode=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param channel_min: Minimum channel
        :type channel_min: ``int`` or ``HexList``
        :param channel_max: Maximum channel
        :type channel_max: ``int`` or ``HexList``
        :param power: Output power
        :type power: ``int`` or ``HexList``
        :param sweep_period: 10ms per unit
        :type sweep_period: ``int`` or ``HexList``
        :param condition: Device dependent test condition
        :type condition: ``int`` or ``HexList``
        :param radio_mode: Indicates that the appropriate registers should be set to select the given mode.
        :type radio_mode: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index, feature_index, channel_min, channel_max, power, sweep_period, **kwargs)
        self.condition = condition
        self.radio_mode = radio_mode
    # end def __init__
# end class SetRfRxContinuousSweepV6


class SetRfRxContinuousSweepV7ToV9(SetRfRxContinuousSweepV6):
    """
    RFTest SetRfRxContinuousSweep implementation class for versions 7 to 9.

    Device configures its radio to receive for a pre defined period of time
    from channel min to channel max by step of 1 Mhz.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    ChannelMin                    8
    ChannelMax                    8
    Power                         8
    Sweep Period                  8
    Condition                     8
    Radio Mode                    8
    Nb Sweep                      16
    Padding                       64
    ============================  ==========
    """
    VERSION = (7, 8, 9,)

    class FID(SetRfRxContinuousSweepV6.FID):
        # See ``SetRfRxContinuousSweepV6.FID``
        NB_SWEEP = 0xF4
        PADDING = 0xF3
    # end class FID

    class LEN(SetRfRxContinuousSweepV0ToV5.LEN):
        # See ``SetRfRxContinuousSweepV0ToV5.LEN``
        NB_SWEEP = 0x10
        PADDING = 0x40
    # end class LEN

    FIELDS = SetRfRxContinuousSweepV6.FIELDS[:-1] + (
        BitField(FID.NB_SWEEP,
                 LEN.NB_SWEEP,
                 title='Nb Sweep',
                 name='nb_sweep',
                 aliases=('nbsweep',),
                 checks=(CheckHexList(LEN.NB_SWEEP // 8), CheckInt(),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RFTest.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, channel_min=0, channel_max=0, power=0, sweep_period=0, condition=0,
                 radio_mode=0, nb_sweep=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param channel_min: Minimum channel
        :type channel_min: ``int`` or ``HexList``
        :param channel_max: Maximum channel
        :type channel_max: ``int`` or ``HexList``
        :param power: Output power
        :type power: ``int`` or ``HexList``
        :param sweep_period: 10ms per unit
        :type sweep_period: ``int`` or ``HexList``
        :param condition: Device dependent test condition
        :type condition: ``int`` or ``HexList``
        :param radio_mode: Indicates that the appropriate registers should be set to select the given mode.
        :type radio_mode: ``int`` or ``HexList``
        :param nb_sweep: Number of full sweeps to be executed.
        :type nb_sweep: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index, feature_index, channel_min, channel_max, power, sweep_period, condition,
                         radio_mode, **kwargs)
        self.nb_sweep = nb_sweep
    # end def __init__
# end class SetRfRxContinuousSweepV7ToV9


class SetRfRxContinuousSweepResponseV0ToV9(LongEmptyPacketDataFormat):
    """
    Define ``SetRfRxContinuousSweepResponse`` implementation class for versions 0 to 9
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetRfRxContinuousSweepV0ToV5, SetRfRxContinuousSweepV6, SetRfRxContinuousSweepV7ToV9,)
    VERSION = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9,)
    FUNCTION_INDEX = 4

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class SetRfRxContinuousSweepResponseV0ToV9


class RFSendPeriodicMsgNoAckV1ToV2(RFSendPeriodicMsgPacketDataFormat):
    """
    Define ``RFSendPeriodicMsgNoAck`` implementation class for version 1 to 2.

    Device configures its transmitter to send a true continuous data message out.
    Since device need high duration packet transmit, it don?t need receive acknowledge from receiver.
    """
    VERSION = (1, 2,)

    def __init__(self, device_index, feature_index, address=0, channel=0, power=0, period=0, condition=0, nbmsg=0,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param address: eQuad base and destination address
        :type address: ``HexList``
        :param channel: RF test channel
        :type channel: ``int`` or ``HexList``
        :param power: Output power
        :type power: ``int`` or ``HexList``
        :param period: 1ms per unit MSB first
        :type period: ``int`` or ``HexList``
        :param condition: Condition on how is sent the message
        :type condition: ``int`` or ``HexList``
        :param nbmsg: Number of message to be sent
        :type nbmsg: ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=RFSendPeriodicMsgNoAckResponseV1ToV9.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.address = address
        self.channel = channel
        self.power = power
        self.period = period
        self.condition = condition
        self.nbmsg = nbmsg
    # end def __init__
# end class RFSendPeriodicMsgNoAckV1ToV2


class RFSendPeriodicMsgNoAckV3ToV5(RFSendPeriodicMsgNoAckV1ToV2):
    """
    RFTest RFSendPeriodicMsgNoAck implementation class for version 3 to 5.

    Device sends periodic message.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Address                       40
    Channel                       8
    Power                         8
    Period                        8
    Condition                     8
    NbMsg                         16
    Radio Mode                    8
    Padding                       32
    ============================  ==========
    """
    VERSION = (3, 4, 5,)

    class FID(RFSendPeriodicMsgV0ToV2.FID):
        # See ``RFSendPeriodicMsgV0ToV2.FID``
        RADIO_MODE = RFSendPeriodicMsgV0ToV2.FID.NBMSG - 1
        PADDING = RADIO_MODE - 1
    # end class FID

    class LEN(RFSendPeriodicMsgV0ToV2.LEN):
        # See ``RFSendPeriodicMsgV0ToV2.LEN``
        RADIO_MODE = 0x8
        PADDING = 0x20
    # end class LEN

    FIELDS = RFSendPeriodicMsgV0ToV2.FIELDS[:-1] + (
        BitField(FID.RADIO_MODE,
                 LEN.RADIO_MODE,
                 title='Radio Mode',
                 name='radio_mode',
                 checks=(CheckHexList(LEN.RADIO_MODE // 8), CheckByte(),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RFTest.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, channel=0, address=0, power=0, period=0, condition=0, nbmsg=0,
                 radio_mode=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param address: eQuad base and destination address
        :type address: ``HexList``
        :param channel: RF test channel
        :type channel: ``int`` or ``HexList``
        :param power: Output power
        :type power: ``int`` or ``HexList``
        :param period: 1ms per unit MSB first
        :type period: ``int`` or ``HexList``
        :param condition: Condition on how is sent the message
        :type condition: ``int`` or ``HexList``
        :param nbmsg: Number of message to be sent
        :type nbmsg: ``HexList``
        :param radio_mode: Default / Unifying / Gaming
        :type radio_mode: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index, feature_index, address, channel, power, period, condition, nbmsg,
                         **kwargs)
        self.radio_mode = radio_mode
    # end def __init__
# end class RFSendPeriodicMsgNoAckV3ToV5


class RFSendPeriodicMsgNoAckV6ToV9(RFSendPeriodicMsgNoAckV3ToV5):
    """
    RFTest RFSendPeriodicMsgNoAck implementation class for versions 6 to 9.

    Device sends periodic message.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Address                       40
    Channel                       8
    Power                         8
    Period                        8
    Condition                     8
    NbMsg                         16
    Radio Mode                    8
    Payload Size                  8
    Padding                       24
    ============================  ==========
    """
    VERSION = (6, 7, 8, 9,)

    class FID(RFSendPeriodicMsgNoAckV3ToV5.FID):
        # See ``RFSendPeriodicMsgNoAckV3ToV5.FID``
        PAYLOAD_SIZE = 0xF3
        PADDING = 0xF2
    # end class FID

    class LEN(RFSendPeriodicMsgNoAckV3ToV5.LEN):
        # See ``RFSendPeriodicMsgNoAckV3ToV5.LEN``
        PAYLOAD_SIZE = 0x08
        PADDING = 0x18
    # end class LEN

    FIELDS = RFSendPeriodicMsgNoAckV3ToV5.FIELDS[:-1] + (
        BitField(FID.PAYLOAD_SIZE,
                 LEN.PAYLOAD_SIZE,
                 title='Payload Size',
                 name='payload_size',
                 checks=(CheckHexList(LEN.PAYLOAD_SIZE // 8), CheckByte(),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RFTest.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, address=0, channel=0, power=0, period=0, condition=0, nbmsg=0,
                 radio_mode=0, payload_size=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param address: eQuad base and destination address
        :type address: ``HexList``
        :param channel: RF test channel
        :type channel: ``int`` or ``HexList``
        :param power: Output power
        :type power: ``int`` or ``HexList``
        :param period: 1ms per unit MSB first
        :type period: ``int`` or ``HexList``
        :param condition: Condition on how is sent the message
        :type condition: ``int`` or ``HexList``
        :param nbmsg: Number of message to be sent
        :type nbmsg: ``HexList``
        :param radio_mode: Default / Unifying / Gaming
        :type radio_mode: ``int`` or ``HexList``
        :param payload_size: This parameter encodes the ESB pay-load size.
        :type payload_size: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index, feature_index, channel, address, power, period, condition, nbmsg, radio_mode,
                         **kwargs)
        self.payload_size = payload_size
    # end def __init__
# end class RFSendPeriodicMsgNoAckV6ToV9


class RFSendPeriodicMsgNoAckResponseV1ToV9(LongEmptyPacketDataFormat):
    """
    Define ``RFSendPeriodicMsgNoAckResponse`` implementation class for versions 1 to 9
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (RFSendPeriodicMsgNoAckV1ToV2, RFSendPeriodicMsgNoAckV3ToV5, RFSendPeriodicMsgNoAckV6ToV9,)
    VERSION = (1, 2, 3, 4, 5, 6, 7, 8, 9,)
    FUNCTION_INDEX = 5

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class RFSendPeriodicMsgNoAckResponseV1ToV9


class RFReceivePeriodicMsgV2(RFTest):
    """
    Define ``RFReceivePeriodicMsg`` implementation class for version 2

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Address                       40
    Channel                       8
    Power                         8
    Condition                     8
    Timeout                       16
    Padding                       48
    ============================  ==========
    """
    VERSION = (2,)

    class FID(RFTest.FID):
        # See ``RFTest.FID``
        ADDRESS = RFTest.FID.SOFTWARE_ID - 1
        CHANNEL = ADDRESS - 1
        POWER = CHANNEL - 1
        CONDITION = POWER - 1
        TIMEOUT = CONDITION - 1
        PADDING = TIMEOUT - 1
    # end class FID

    class LEN(RFTest.LEN):
        # See ``RFTest.LEN``
        ADDRESS = 0x28
        CHANNEL = 0x8
        POWER = 0x8
        CONDITION = 0x8
        TIMEOUT = 0x10
        PADDING = 0x30
    # end class LEN

    FIELDS = RFTest.FIELDS + (
        BitField(fid=FID.ADDRESS, length=LEN.ADDRESS,
                 title="Address", name="address",
                 checks=(CheckHexList(LEN.ADDRESS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.ADDRESS) - 1),)),
        BitField(fid=FID.CHANNEL, length=LEN.CHANNEL,
                 title="Channel", name="channel",
                 checks=(CheckHexList(LEN.CHANNEL // 8),
                         CheckByte(),)),
        BitField(fid=FID.POWER, length=LEN.POWER,
                 title="Power", name="power",
                 checks=(CheckHexList(LEN.POWER // 8),
                         CheckByte(),)),
        BitField(fid=FID.CONDITION, length=LEN.CONDITION,
                 title="Condition", name="condition",
                 checks=(CheckHexList(LEN.CONDITION // 8),
                         CheckByte(),)),
        BitField(fid=FID.TIMEOUT, length=LEN.TIMEOUT,
                 title="Timeout", name="timeout",
                 checks=(CheckHexList(LEN.TIMEOUT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.TIMEOUT) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",

                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RFTest.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, address=0, channel=0, power=0, condition=0, timeout=0, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
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
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=RFReceivePeriodicMsgResponseV2ToV9.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.address = address
        self.channel = channel
        self.power = power
        self.condition = condition
        self.timeout = timeout
    # end def __init__
# end class RFReceivePeriodicMsgV5


class RFReceivePeriodicMsgV3ToV9(RFReceivePeriodicMsgV2):
    """
    Define ``RFReceivePeriodicMsg`` implementation class for versions 3 to 9

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Address                       40
    Channel                       8
    Power                         8
    Condition                     8
    Timeout                       16
    Radio Mode                    8
    Padding                       40
    ============================  ==========
    """
    VERSION = (3, 4, 5, 6, 7, 8, 9,)

    class FID(RFReceivePeriodicMsgV2.FID):
        # See ``RFTest.FID``
        RADIO_MODE = RFReceivePeriodicMsgV2.FID.TIMEOUT - 1
        PADDING = RADIO_MODE - 1
    # end class FID

    class LEN(RFReceivePeriodicMsgV2.LEN):
        # See ``RFTest.LEN``
        RADIO_MODE = 0x8
        PADDING = 0x28
    # end class LEN

    FIELDS = RFReceivePeriodicMsgV2.FIELDS[:-1] + (
        BitField(fid=FID.RADIO_MODE, length=LEN.RADIO_MODE,
                 title="RadioMode", name="radio_mode",
                 checks=(CheckHexList(LEN.RADIO_MODE // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RFTest.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, address=0, channel=0, power=0, condition=0, timeout=0, radio_mode=0,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
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
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         address=address, channel=channel, power=power, condition=condition, timeout=timeout,
                         **kwargs)
        self.radio_mode = radio_mode
    # end def __init__
# end class RFReceivePeriodicMsgV3ToV9


class RFReceivePeriodicMsgResponseV2ToV9(LongEmptyPacketDataFormat):
    """
    Define ``RFReceivePeriodicMsgResponse`` implementation class for versions 2 to 9
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (RFReceivePeriodicMsgV2, RFReceivePeriodicMsgV3ToV9,)
    VERSION = (2, 3, 4, 5, 6, 7, 8, 9,)
    FUNCTION_INDEX = 6

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class RFReceivePeriodicMsgResponseV2ToV9


class RFSendPeriodicFullDutyMsgV9(RFTest):
    """
    Define ``RFSendPeriodicFullDutyMsg`` implementation class for versions 9

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Channel                       8
    Power                         8
    Timeout                       16
    Condition                     8
    Radio Mode                    8
    Padding                       80
    ============================  ==========
    """
    VERSION = (9,)

    class FID(RFTest.FID):
        # See ``RFTest.FID``
        CHANNEL = RFTest.FID.SOFTWARE_ID - 1
        POWER = CHANNEL - 1
        TIMEOUT = POWER - 1
        CONDITION = TIMEOUT - 1
        RADIO_MODE = CONDITION - 1
        PADDING = RADIO_MODE - 1
    # end class FID

    class LEN(RFTest.LEN):
        # See ``RFTest.LEN``
        CHANNEL = 0x08
        POWER = 0x08
        TIMEOUT = 0x10
        CONDITION = 0x08
        RADIO_MODE = 0x08
        PADDING = 0x50
    # end class LEN

    FIELDS = RFTest.FIELDS + (
        BitField(fid=FID.CHANNEL, length=LEN.CHANNEL,
                 title="Channel", name="channel",
                 checks=(CheckHexList(LEN.CHANNEL // 8),
                         CheckByte(),)),
        BitField(fid=FID.POWER, length=LEN.POWER,
                 title="Power", name="power",
                 checks=(CheckHexList(LEN.POWER // 8),
                         CheckByte(),)),
        BitField(fid=FID.TIMEOUT, length=LEN.TIMEOUT,
                 title="Timeout", name="timeout",
                 checks=(CheckHexList(LEN.TIMEOUT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.TIMEOUT) - 1),)),
        BitField(fid=FID.CONDITION, length=LEN.CONDITION,
                 title="Condition", name="condition",
                 checks=(CheckHexList(LEN.CONDITION // 8),
                         CheckByte(),)),
        BitField(fid=FID.RADIO_MODE, length=LEN.RADIO_MODE,
                 title="RadioMode", name="radio_mode",
                 checks=(CheckHexList(LEN.RADIO_MODE // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=RFTest.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, channel=0, power=0, timeout=0, condition=0, radio_mode=0,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
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
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=RFSendPeriodicFullDutyMsgResponseV9.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.channel = channel
        self.power = power
        self.timeout = timeout
        self.condition = condition
        self.radio_mode = radio_mode
    # end def __init__
# end class RFSendPeriodicFullDutyMsgV9


class RFSendPeriodicFullDutyMsgResponseV9(LongEmptyPacketDataFormat):
    """
    Define ``RFSendPeriodicFullDutyMsgResponse`` implementation class for versions 9
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (RFSendPeriodicFullDutyMsgV9,)
    VERSION = (9,)
    FUNCTION_INDEX = 7

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class RFSendPeriodicFullDutyMsgResponseV9

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
