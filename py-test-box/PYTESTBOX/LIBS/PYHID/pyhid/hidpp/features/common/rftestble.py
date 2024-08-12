#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.features.common.rftestble
    :brief: HID++ 2.0 RF test BLE command interface definition
    :author: Jerry Lin
    :date: 2020/03/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC

from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.features.common.rftest import RFReceivePeriodicMsgV2
from pyhid.hidpp.features.common.rftest import RFReceivePeriodicMsgV3ToV9
from pyhid.hidpp.features.common.rftest import RFRxContinuousV0ToV5
from pyhid.hidpp.features.common.rftest import RFRxContinuousV6ToV9
from pyhid.hidpp.features.common.rftest import RFSendPeriodicMsgNoAckV1ToV2
from pyhid.hidpp.features.common.rftest import RFSendPeriodicMsgNoAckV3ToV5
from pyhid.hidpp.features.common.rftest import RFSendPeriodicMsgNoAckV6ToV9
from pyhid.hidpp.features.common.rftest import RFSendPeriodicMsgResponseV0ToV9
from pyhid.hidpp.features.common.rftest import RFSendPeriodicMsgV0ToV2
from pyhid.hidpp.features.common.rftest import RFSendPeriodicMsgV3ToV5
from pyhid.hidpp.features.common.rftest import RFSendPeriodicMsgV6ToV9
from pyhid.hidpp.features.common.rftest import RFSendPeriodicFullDutyMsgV9
from pyhid.hidpp.features.common.rftest import RFSendPeriodicFullDutyMsgResponseV9
from pyhid.hidpp.features.common.rftest import RFTest
from pyhid.hidpp.features.common.rftest import RFTestInterface
from pyhid.hidpp.features.common.rftest import RFTxCWV0ToV5
from pyhid.hidpp.features.common.rftest import RFTxCWV6ToV9
from pyhid.hidpp.features.common.rftest import SetRfRxContinuousSweepV0ToV5
from pyhid.hidpp.features.common.rftest import SetRfRxContinuousSweepV6
from pyhid.hidpp.features.common.rftest import SetRfRxContinuousSweepV7ToV9
from pyhid.hidpp.features.common.rftest import SetRfTxCWSweepV0ToV5
from pyhid.hidpp.features.common.rftest import SetRfTxCWSweepV6
from pyhid.hidpp.features.common.rftest import SetRfTxCWSweepV7ToV9


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class RFTestBLE(RFTest):
    """
    RF Test BLE implementation class

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Params                        24
    ============================  ==========
    """
    FEATURE_ID = 0x1891
# end class RFTestBLE


class RFTestBLEModel(FeatureModel):
    """
    RF test BLE feature model
    """
    class INDEX:
        """
        Functions indexes
        """
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
        RF test BLE feature data model
        """
        return {
            "feature_base": RFTestBLE,
            "versions": {
                RFTestBLEV0.VERSION: {
                    "main_cls": RFTestBLEV0,
                    "api": {
                        "functions": {
                            cls.INDEX.RF_SEND_PERIODIC_MSG: {"request": RFBLESendPeriodicMsgV0ToV2,
                                                             "response": RFBLESendPeriodicMsgResponseV0ToV9},
                            cls.INDEX.RF_TX_CW: {"request": RFBLETxCWV0ToV5, "response": None, },
                            cls.INDEX.RF_RX_CONTINUOUS: {"request": RFBLERxContinuousV0ToV5, "response": None, },
                            cls.INDEX.SET_RF_TX_CW_SWEEP: {"request": SetRfBLETxCWSweepV0ToV5, "response": None, },
                            cls.INDEX.SET_RF_RX_CONTINUOUS_SWEEP: {"request": SetRfBLERxContinuousSweepV0ToV5,
                                                                   "response": None, },
                        }
                    },
                },
                RFTestBLEV1.VERSION: {
                    "main_cls": RFTestBLEV1,
                    "api": {
                        "functions": {
                            cls.INDEX.RF_SEND_PERIODIC_MSG: {"request": RFBLESendPeriodicMsgV0ToV2,
                                                             "response": RFBLESendPeriodicMsgResponseV0ToV9},
                            cls.INDEX.RF_TX_CW: {"request": RFBLETxCWV0ToV5, "response": None, },
                            cls.INDEX.RF_RX_CONTINUOUS: {"request": RFBLERxContinuousV0ToV5, "response": None, },
                            cls.INDEX.SET_RF_TX_CW_SWEEP: {"request": SetRfBLETxCWSweepV0ToV5, "response": None, },
                            cls.INDEX.SET_RF_RX_CONTINUOUS_SWEEP: {"request": SetRfBLERxContinuousSweepV0ToV5,
                                                                   "response": None, },
                            cls.INDEX.RF_SEND_PERIODIC_MSG_NO_ACK: {"request": RFBLESendPeriodicMsgNoAckV1ToV2,
                                                                    "response": None, },
                        }
                    },
                },
                RFTestBLEV2.VERSION: {
                    "main_cls": RFTestBLEV2,
                    "api": {
                        "functions": {
                            cls.INDEX.RF_SEND_PERIODIC_MSG: {"request": RFBLESendPeriodicMsgV0ToV2,
                                                             "response": RFBLESendPeriodicMsgResponseV0ToV9},
                            cls.INDEX.RF_TX_CW: {"request": RFBLETxCWV0ToV5, "response": None, },
                            cls.INDEX.RF_RX_CONTINUOUS: {"request": RFBLERxContinuousV0ToV5, "response": None, },
                            cls.INDEX.SET_RF_TX_CW_SWEEP: {"request": SetRfBLETxCWSweepV0ToV5, "response": None, },
                            cls.INDEX.SET_RF_RX_CONTINUOUS_SWEEP: {"request": SetRfBLERxContinuousSweepV0ToV5,
                                                                   "response": None, },
                            cls.INDEX.RF_SEND_PERIODIC_MSG_NO_ACK: {"request": RFBLESendPeriodicMsgNoAckV1ToV2,
                                                                    "response": None, },
                            cls.INDEX.RF_RECEIVE_PERIODIC_MSG: {"request": RFBLEReceivePeriodicMsgV2,
                                                                "response": None, },
                        }
                    },
                },
                RFTestBLEV3.VERSION: {
                    "main_cls": RFTestBLEV3,
                    "api": {
                        "functions": {
                            cls.INDEX.RF_SEND_PERIODIC_MSG: {"request": RFBLESendPeriodicMsgV3ToV5,
                                                             "response": RFBLESendPeriodicMsgResponseV0ToV9},
                            cls.INDEX.RF_TX_CW: {"request": RFBLETxCWV0ToV5, "response": None, },
                            cls.INDEX.RF_RX_CONTINUOUS: {"request": RFBLERxContinuousV0ToV5, "response": None, },
                            cls.INDEX.SET_RF_TX_CW_SWEEP: {"request": SetRfBLETxCWSweepV0ToV5, "response": None, },
                            cls.INDEX.SET_RF_RX_CONTINUOUS_SWEEP: {"request": SetRfBLERxContinuousSweepV0ToV5,
                                                                   "response": None, },
                            cls.INDEX.RF_SEND_PERIODIC_MSG_NO_ACK: {"request": RFBLESendPeriodicMsgNoAckV3ToV5,
                                                                    "response": None, },
                            cls.INDEX.RF_RECEIVE_PERIODIC_MSG: {"request": RFBLEReceivePeriodicMsgV3ToV9,
                                                                "response": None, },
                        }
                    },
                },
                RFTestBLEV4.VERSION: {
                    "main_cls": RFTestBLEV4,
                    "api": {
                        "functions": {
                            cls.INDEX.RF_SEND_PERIODIC_MSG: {"request": RFBLESendPeriodicMsgV3ToV5,
                                                             "response": RFBLESendPeriodicMsgResponseV0ToV9},
                            cls.INDEX.RF_TX_CW: {"request": RFBLETxCWV0ToV5, "response": None, },
                            cls.INDEX.RF_RX_CONTINUOUS: {"request": RFBLERxContinuousV0ToV5, "response": None, },
                            cls.INDEX.SET_RF_TX_CW_SWEEP: {"request": SetRfBLETxCWSweepV0ToV5, "response": None, },
                            cls.INDEX.SET_RF_RX_CONTINUOUS_SWEEP: {"request": SetRfBLERxContinuousSweepV0ToV5,
                                                                   "response": None, },
                            cls.INDEX.RF_SEND_PERIODIC_MSG_NO_ACK: {"request": RFBLESendPeriodicMsgNoAckV3ToV5,
                                                                    "response": None, },
                            cls.INDEX.RF_RECEIVE_PERIODIC_MSG: {"request": RFBLEReceivePeriodicMsgV3ToV9,
                                                                "response": None, },
                        }
                    },
                },
                RFTestBLEV5.VERSION: {
                    "main_cls": RFTestBLEV5,
                    "api": {
                        "functions": {
                            cls.INDEX.RF_SEND_PERIODIC_MSG: {"request": RFBLESendPeriodicMsgV3ToV5,
                                                             "response": RFBLESendPeriodicMsgResponseV0ToV9},
                            cls.INDEX.RF_TX_CW: {"request": RFBLETxCWV0ToV5, "response": None, },
                            cls.INDEX.RF_RX_CONTINUOUS: {"request": RFBLERxContinuousV0ToV5, "response": None, },
                            cls.INDEX.SET_RF_TX_CW_SWEEP: {"request": SetRfBLETxCWSweepV0ToV5, "response": None, },
                            cls.INDEX.SET_RF_RX_CONTINUOUS_SWEEP: {"request": SetRfBLERxContinuousSweepV0ToV5,
                                                                   "response": None, },
                            cls.INDEX.RF_SEND_PERIODIC_MSG_NO_ACK: {"request": RFBLESendPeriodicMsgNoAckV3ToV5,
                                                                    "response": None, },
                            cls.INDEX.RF_RECEIVE_PERIODIC_MSG: {"request": RFBLEReceivePeriodicMsgV3ToV9,
                                                                "response": None, },
                        }
                    },
                },
                RFTestBLEV6.VERSION: {
                    "main_cls": RFTestBLEV6,
                    "api": {
                        "functions": {
                            cls.INDEX.RF_SEND_PERIODIC_MSG: {"request": RFBLESendPeriodicMsgV6ToV9,
                                                             "response": RFBLESendPeriodicMsgResponseV0ToV9},
                            cls.INDEX.RF_TX_CW: {"request": RFBLETxCWV6ToV9, "response": None, },
                            cls.INDEX.RF_RX_CONTINUOUS: {"request": RFBLERxContinuousV6ToV9, "response": None, },
                            cls.INDEX.SET_RF_TX_CW_SWEEP: {"request": SetRfBLETxCWSweepV6, "response": None, },
                            cls.INDEX.SET_RF_RX_CONTINUOUS_SWEEP: {"request": SetRfBLERxContinuousSweepV6,
                                                                   "response": None, },
                            cls.INDEX.RF_SEND_PERIODIC_MSG_NO_ACK: {"request": RFBLESendPeriodicMsgNoAckV6ToV9,
                                                                    "response": None, },
                            cls.INDEX.RF_RECEIVE_PERIODIC_MSG: {"request": RFBLEReceivePeriodicMsgV3ToV9,
                                                                "response": None, },
                        }
                    },
                },
                RFTestBLEV7.VERSION: {
                    "main_cls": RFTestBLEV7,
                    "api": {
                        "functions": {
                            cls.INDEX.RF_SEND_PERIODIC_MSG: {"request": RFBLESendPeriodicMsgV6ToV9,
                                                             "response": RFBLESendPeriodicMsgResponseV0ToV9},
                            cls.INDEX.RF_TX_CW: {"request": RFBLETxCWV6ToV9, "response": None, },
                            cls.INDEX.RF_RX_CONTINUOUS: {"request": RFBLERxContinuousV6ToV9, "response": None, },
                            cls.INDEX.SET_RF_TX_CW_SWEEP: {"request": SetRfBLETxCWSweepV7ToV9, "response": None, },
                            cls.INDEX.SET_RF_RX_CONTINUOUS_SWEEP: {"request": SetRfBLERxContinuousSweepV7ToV9,
                                                                   "response": None, },
                            cls.INDEX.RF_SEND_PERIODIC_MSG_NO_ACK: {"request": RFBLESendPeriodicMsgNoAckV6ToV9,
                                                                    "response": None, },
                            cls.INDEX.RF_RECEIVE_PERIODIC_MSG: {"request": RFBLEReceivePeriodicMsgV3ToV9,
                                                                "response": None, },
                        }
                    },
                },
                RFTestBLEV8.VERSION: {
                    "main_cls": RFTestBLEV8,
                    "api": {
                        "functions": {
                            cls.INDEX.RF_SEND_PERIODIC_MSG: {"request": RFBLESendPeriodicMsgV6ToV9,
                                                             "response": RFBLESendPeriodicMsgResponseV0ToV9},
                            cls.INDEX.RF_TX_CW: {"request": RFBLETxCWV6ToV9, "response": None, },
                            cls.INDEX.RF_RX_CONTINUOUS: {"request": RFBLERxContinuousV6ToV9, "response": None, },
                            cls.INDEX.SET_RF_TX_CW_SWEEP: {"request": SetRfBLETxCWSweepV7ToV9, "response": None, },
                            cls.INDEX.SET_RF_RX_CONTINUOUS_SWEEP: {"request": SetRfBLERxContinuousSweepV7ToV9,
                                                                   "response": None, },
                            cls.INDEX.RF_SEND_PERIODIC_MSG_NO_ACK: {"request": RFBLESendPeriodicMsgNoAckV6ToV9,
                                                                    "response": None, },
                            cls.INDEX.RF_RECEIVE_PERIODIC_MSG: {"request": RFBLEReceivePeriodicMsgV3ToV9,
                                                                "response": None, },
                        }
                    },
                },
                RFTestBLEV9.VERSION: {
                    "main_cls": RFTestBLEV9,
                    "api": {
                        "functions": {
                            cls.INDEX.RF_SEND_PERIODIC_MSG: {"request": RFBLESendPeriodicMsgV6ToV9,
                                                             "response": RFBLESendPeriodicMsgResponseV0ToV9},
                            cls.INDEX.RF_TX_CW: {"request": RFBLETxCWV6ToV9, "response": None, },
                            cls.INDEX.RF_RX_CONTINUOUS: {"request": RFBLERxContinuousV6ToV9, "response": None, },
                            cls.INDEX.SET_RF_TX_CW_SWEEP: {"request": SetRfBLETxCWSweepV7ToV9, "response": None, },
                            cls.INDEX.SET_RF_RX_CONTINUOUS_SWEEP: {"request": SetRfBLERxContinuousSweepV7ToV9,
                                                                   "response": None, },
                            cls.INDEX.RF_SEND_PERIODIC_MSG_NO_ACK: {"request": RFBLESendPeriodicMsgNoAckV6ToV9,
                                                                    "response": None, },
                            cls.INDEX.RF_RECEIVE_PERIODIC_MSG: {"request": RFBLEReceivePeriodicMsgV3ToV9,
                                                                "response": None, },
                            cls.INDEX.RF_SEND_PERIODIC_FULL_DUTY_MSG: {
                                "request": RFBLESendPeriodicFullDutyMsgV9,
                                "response": RFBLESendPeriodicFullDutyMsgResponseV9, },
                        }
                    },
                },
            }
        }
    # end def _get_data_model
# end class RFTestBLEModel


class RFTestBLEFactory(FeatureFactory):
    """
    RF test BLE factory creates a RF test object from a given version
    """
    @staticmethod
    def create(version):
        """
        RF test BLE object creation from version number

        :param version: RF test BLE feature version
        :type version: ``int``
        :return: RF test BLE object
        :rtype: ``RFTestBLEInterface``
        """
        return RFTestBLEModel.get_main_cls(version)()
    # end def create
# end class RFTestBLEFactory


class RFTestBLEInterface(RFTestInterface, ABC):
    """
    Interface to RF test BLE feature

    Defines required interfaces for RF test classes
    """
# end class RFTestBLEInterface


class RFTestBLEV0(RFTestBLEInterface):
    """
    RF BLE Test
    This feature provides model and unit specific information

    [0] RFSendPeriodicMsg(address, channel, power, period, condition, nbmsg) -> Acked packet
    [1] RFTxCW(channel, power, timeout)
    [2] RFRxContinuous(channel, power, timeout)
    [3] SetRfTxCWSweep(channelmin, channelmax, sweepperiod, power, timeout)
    [4] SetRfRxContinuousSweep(address, channel, power, NbMessage)
    """
    VERSION = 0

    def __init__(self):
        """
        See :any:`RFTestBLEInterface.__init__`
        """
        super().__init__()
        self.rf_send_periodic_msg_cls = RFTestBLEModel.get_request_cls(
            self.VERSION, RFTestBLEModel.INDEX.RF_SEND_PERIODIC_MSG)
        self.rf_send_periodic_msg_response_cls = RFTestBLEModel.get_response_cls(
            self.VERSION, RFTestBLEModel.INDEX.RF_SEND_PERIODIC_MSG)
        self.rf_tx_cw_cls = RFTestBLEModel.get_request_cls(
            self.VERSION, RFTestBLEModel.INDEX.RF_TX_CW)
        self.rf_rx_continuous_cls = RFTestBLEModel.get_request_cls(
            self.VERSION, RFTestBLEModel.INDEX.RF_RX_CONTINUOUS)
        self.set_rf_tx_cw_sweep_cls = RFTestBLEModel.get_request_cls(
            self.VERSION, RFTestBLEModel.INDEX.SET_RF_TX_CW_SWEEP)
        self.set_rf_rx_continuous_sweep_cls = RFTestBLEModel.get_request_cls(
            self.VERSION, RFTestBLEModel.INDEX.SET_RF_RX_CONTINUOUS_SWEEP)

    # end def __init__

    def get_max_function_index(self):
        """
        See :any:`RFTestBLEInterface.get_max_function_index`
        """
        return RFTestBLEModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class RFTestBLEV0


class RFTestBLEV1(RFTestBLEV0):
    """
    RF BLE Test
    Version 1: Add RFSendPeriodicMsgNoAck

    [0] RFSendPeriodicMsg(address, channel, power, period, condition, nbmsg) -> Acked packet
    [1] RFTxCW(channel, power, timeout)
    [2] RFRxContinuous(channel, power, timeout)
    [3] SetRfTxCWSweep(channelmin, channelmax, sweepperiod, power, timeout)
    [4] SetRfRxContinuousSweep(address, channel, power, NbMessage)
    [5] RFSendPeriodicMsgNoAck(address, channel, power, period, condition, nbmsg)
    """
    VERSION = 1

    def __init__(self):
        """
        See :any:`RFTestBLEInterface.__init__`
        """
        super().__init__()
        self.rf_send_periodic_msg_no_ack_cls = RFTestBLEModel.get_request_cls(
            self.VERSION, RFTestBLEModel.INDEX.RF_SEND_PERIODIC_MSG_NO_ACK)

    # end def __init__

    def get_max_function_index(self):
        """
        See :any:`RFTestBLEInterface.get_max_function_index`
        """
        return RFTestBLEModel.get_base_cls().MAX_FUNCTION_INDEX_V1
    # end def get_max_function_index
# end class RFTestBLEV1


class RFTestBLEV2(RFTestBLEV1):
    """
    RF BLE Test
    Version 2: Add RFReceivePeriodicMsg

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
        """
        See :any:`RFTestBLEInterface.__init__`
        """
        super().__init__()
        self.rf_receive_periodic_msg_cls = RFTestBLEModel.get_request_cls(
            self.VERSION, RFTestBLEModel.INDEX.RF_RECEIVE_PERIODIC_MSG)
    # end def __init__

    def get_max_function_index(self):
        """
        See :any:`RFTestBLEInterface.get_max_function_index`
        """
        return RFTestBLEModel.get_base_cls().MAX_FUNCTION_INDEX_V2ToV8
    # end def get_max_function_index
# end class RFTestBLEV2


class RFTestBLEV3(RFTestBLEV2):
    """
    RF BLE Test
    Version 3: Add radiomode parameter to modulated TX/RX

    [0] RFSendPeriodicMsg(address, channel, power, period, condition, nbmsg, radiomode) -> Acked packet
    [1] RFTxCW(channel, power, timeout)
    [2] RFRxContinuous(channel, power, timeout)
    [3] SetRfTxCWSweep(channelmin, channelmax, power, sweepperiod)
    [4] SetRfRxContinuousSweep(channelMin, channelMax, power, sweepperiod)
    [5] RFSendPeriodicMsgNoAck(address, channel, power, period, condition, nbmsg, radiomode)
    [6] RFReceivePeriodicMsg(address, channel, power, condition, timeout, radiomode)
    """
    VERSION = 3
# end class RFTestBLEV3


class RFTestBLEV4(RFTestBLEV3):
    """
    RF BLE Test
    Version 4: Increase payload size for modulated tests to 32 bytes

    [0] RFSendPeriodicMsg(address, channel, power, period, condition, nbmsg, radiomode) -> Acked packet
    [1] RFTxCW(channel, power, timeout)
    [2] RFRxContinuous(channel, power, timeout)
    [3] SetRfTxCWSweep(channelmin, channelmax, power, sweepperiod)
    [4] SetRfRxContinuousSweep(channelMin, channelMax, power, sweepperiod)
    [5] RFSendPeriodicMsgNoAck(address, channel, power, period, condition, nbmsg, radiomode)
    [6] RFReceivePeriodicMsg(address, channel, power, condition, timeout, radiomode)
    """
    VERSION = 4
# end class RFTestBLEV4


class RFTestBLEV5(RFTestBLEV4):
    """
    RF BLE Test
    Version 5: Increase payload size for modulated tests to 33 bytes (to cover 2-byte preamble in BLE2M)

    [0] RFSendPeriodicMsg(address, channel, power, period, condition, nbmsg, radiomode) -> Acked packet
    [1] RFTxCW(channel, power, timeout)
    [2] RFRxContinuous(channel, power, timeout)
    [3] SetRfTxCWSweep(channelmin, channelmax, power, sweepperiod)
    [4] SetRfRxContinuousSweep(channelMin, channelMax, power, sweepperiod)
    [5] RFSendPeriodicMsgNoAck(address, channel, power, period, condition, nbmsg, radiomode)
    [6] RFReceivePeriodicMsg(address, channel, power, condition, timeout, radiomode)
    """
    VERSION = 5
# end class RFTestBLEV5


class RFTestBLEV6(RFTestBLEV5):
    """
    RF BLE Test
    Version 6:
    (1) Add parameters "condition" and "radiomode" to RFTxCW, RFRxContinuous, SetRfTxCWSweep, and
    SetRfRxContinuousSweep.
    (2) Add parameter "payloadSize" to RFSendPeriodicMsg and RFReceivePeriodicMsg.
    (3) Specify the call frequency of the task routine used to implement test conditions.

    [0] RFSendPeriodicMsg(address, channel, power, period, condition, nbmsg, radiomode, payloadSize) -> Acked packet
    [1] RFTxCW(channel, power, timeout, condition, radiomode)
    [2] RFRxContinuous(channel, power, timeout, condition, radiomode)
    [3] SetRfTxCWSweep(channelmin, channelmax, power, sweepperiod, condition, radiomode)
    [4] SetRfRxContinuousSweep(channelMin, channelMax, power, sweepperiod, condition, radiomode)
    [5] RFSendPeriodicMsgNoAck(address, channel, power, period, condition, nbmsg, radiomode, payloadSize)
    [6] RFReceivePeriodicMsg(address, channel, power, condition, timeout, radiomode)
    """
    VERSION = 6
# end class RFTestBLEV6


class RFTestBLEV7(RFTestBLEV6):
    """
    RF BLE Test
    Version 7: Add parameter "nbsweep" to SetRfTxCWSweep and SetRfRxContinuousSweep.

    [0] RFSendPeriodicMsg(address, channel, power, period, condition, nbmsg, radiomode, payloadSize) -> Acked packet
    [1] RFTxCW(channel, power, timeout, condition, radiomode)
    [2] RFRxContinuous(channel, power, timeout, condition, radiomode)
    [3] SetRfTxCWSweep(channelmin, channelmax, power, sweepperiod, condition, radiomode, nbsweep)
    [4] SetRfRxContinuousSweep(channelMin, channelMax, power, sweepperiod, condition, radiomode, nbsweep)
    [5] RFSendPeriodicMsgNoAck(address, channel, power, period, condition, nbmsg, radiomode, payloadSize)
    [6] RFReceivePeriodicMsg(address, channel, power, condition, timeout, radiomode)
    """
    VERSION = 7
# end class RFTestBLEV7


class RFTestBLEV8(RFTestBLEV7):
    """
    RF BLE Test
    Version 8: Add period 125us, 250us, 250us

    [0] RFSendPeriodicMsg(address, channel, power, period, condition, nbmsg, radiomode, payloadSize) -> Acked packet
    [1] RFTxCW(channel, power, timeout, condition, radiomode)
    [2] RFRxContinuous(channel, power, timeout, condition, radiomode)
    [3] SetRfTxCWSweep(channelmin, channelmax, power, sweepperiod, condition, radiomode, nbsweep)
    [4] SetRfRxContinuousSweep(channelMin, channelMax, power, sweepperiod, condition, radiomode, nbsweep)
    [5] RFSendPeriodicMsgNoAck(address, channel, power, period, condition, nbmsg, radiomode, payloadSize)
    [6] RFReceivePeriodicMsg(address, channel, power, condition, timeout, radiomode)
    """
    VERSION = 8
# end class RFTestBLEV8


class RFTestBLEV9(RFTestBLEV8):
    """
    Define ``RFTestBLEV9`` feature
    Version 9: Add 100% duty cycle test function RFSendPeriodicFullDutyMsg.

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
        index = RFTestBLEModel.INDEX

        # Requests
        self.rf_send_periodic_full_duty_msg_cls = RFTestBLEModel.get_request_cls(
            self.VERSION, index.RF_SEND_PERIODIC_FULL_DUTY_MSG)

        # Responses
        self.rf_send_periodic_full_duty_msg_response_cls = RFTestBLEModel.get_response_cls(
            self.VERSION, index.RF_SEND_PERIODIC_FULL_DUTY_MSG)
    # end def __init__

    def get_max_function_index(self):
        # See ``RFTestInterface.get_max_function_index``
        return RFTestBLEModel.get_base_cls().MAX_FUNCTION_INDEX_V9
    # end def get_max_function_index
# end class RFTestBLEV9


class RFBLESendPeriodicMsgV0ToV2(RFSendPeriodicMsgV0ToV2):
    # See ``RFSendPeriodicMsgV0ToV2``
    FEATURE_ID = RFTestBLE.FEATURE_ID
# end class RFBLESendPeriodicMsgV0ToV2


class RFBLESendPeriodicMsgV3ToV5(RFSendPeriodicMsgV3ToV5):
    # See ``RFSendPeriodicMsgV3ToV5``
    FEATURE_ID = RFTestBLE.FEATURE_ID
# end class RFBLESendPeriodicMsgV3ToV5


class RFBLESendPeriodicMsgV6ToV9(RFSendPeriodicMsgV6ToV9):
    # See ``RFSendPeriodicMsgV6ToV9``
    FEATURE_ID = RFTestBLE.FEATURE_ID
# end class RFBLESendPeriodicMsgV6ToV9


class RFBLESendPeriodicMsgResponseV0ToV9(RFSendPeriodicMsgResponseV0ToV9):
    # See ``RFSendPeriodicMsgResponseV0ToV9``
    FEATURE_ID = RFTestBLE.FEATURE_ID
    REQUEST_LIST = (RFBLESendPeriodicMsgV0ToV2, RFBLESendPeriodicMsgV3ToV5, RFBLESendPeriodicMsgV6ToV9)
# end class RFBLESendPeriodicMsgResponseV0ToV9


class RFBLETxCWV0ToV5(RFTxCWV0ToV5):
    # See ``RFTxCWV0ToV5``
    FEATURE_ID = RFTestBLE.FEATURE_ID
# end class RFBLETxCWV0ToV5


class RFBLETxCWV6ToV9(RFTxCWV6ToV9):
    # See ``RFTxCWV6ToV9``
    FEATURE_ID = RFTestBLE.FEATURE_ID
# end class RFBLETxCWV6ToV9


class RFBLERxContinuousV0ToV5(RFRxContinuousV0ToV5):
    # See ``RFRxContinuousV0ToV5``
    FEATURE_ID = RFTestBLE.FEATURE_ID
# end class RFBLERxContinuousV0ToV5


class RFBLERxContinuousV6ToV9(RFRxContinuousV6ToV9):
    # See ``RFRxContinuousV6ToV9``
    FEATURE_ID = RFTestBLE.FEATURE_ID
# end class RFBLERxContinuousV6ToV9


class SetRfBLETxCWSweepV0ToV5(SetRfTxCWSweepV0ToV5):
    # See ``SetRfTxCWSweepV0ToV5``
    FEATURE_ID = RFTestBLE.FEATURE_ID
# end class SetRfBLETxCWSweepV0ToV5


class SetRfBLETxCWSweepV6(SetRfTxCWSweepV6):
    # See ``SetRfTxCWSweepV6``
    FEATURE_ID = RFTestBLE.FEATURE_ID
# end class SetRfBLETxCWSweepV6


class SetRfBLETxCWSweepV7ToV9(SetRfTxCWSweepV7ToV9):
    # See ``SetRfTxCWSweepV7ToV9``
    FEATURE_ID = RFTestBLE.FEATURE_ID
# end class SetRfBLETxCWSweepV7ToV9


class SetRfBLERxContinuousSweepV0ToV5(SetRfRxContinuousSweepV0ToV5):
    # See ``SetRfRxContinuousSweepV0ToV5``
    FEATURE_ID = RFTestBLE.FEATURE_ID
# end class SetRfBLERxContinuousSweepV0ToV5


class SetRfBLERxContinuousSweepV6(SetRfRxContinuousSweepV6):
    # See ``SetRfRxContinuousSweepV6``
    FEATURE_ID = RFTestBLE.FEATURE_ID
# end class SetRfBLERxContinuousSweepV6


class SetRfBLERxContinuousSweepV7ToV9(SetRfRxContinuousSweepV7ToV9):
    # See ``SetRfRxContinuousSweepV7ToV9``
    FEATURE_ID = RFTestBLE.FEATURE_ID
# end class SetRfBLERxContinuousSweepV7ToV9


class RFBLESendPeriodicMsgNoAckV1ToV2(RFSendPeriodicMsgNoAckV1ToV2):
    # See ``RFSendPeriodicMsgNoAckV1ToV2``
    FEATURE_ID = RFTestBLE.FEATURE_ID
# end class RFBLESendPeriodicMsgNoAckV1ToV2


class RFBLESendPeriodicMsgNoAckV3ToV5(RFSendPeriodicMsgNoAckV3ToV5):
    # See ``RFSendPeriodicMsgNoAckV3ToV5``
    FEATURE_ID = RFTestBLE.FEATURE_ID
# end class RFBLESendPeriodicMsgNoAckV3ToV5


class RFBLESendPeriodicMsgNoAckV6ToV9(RFSendPeriodicMsgNoAckV6ToV9):
    # See ``RFBLESendPeriodicMsgNoAckV6ToV9``
    FEATURE_ID = RFTestBLE.FEATURE_ID
# end class RFBLESendPeriodicMsgNoAckV6ToV9


class RFBLEReceivePeriodicMsgV2(RFReceivePeriodicMsgV2):
    # See ``RFReceivePeriodicMsgV2``
    FEATURE_ID = RFTestBLE.FEATURE_ID
# end class RFBLEReceivePeriodicMsgV2


class RFBLEReceivePeriodicMsgV3ToV9(RFReceivePeriodicMsgV3ToV9):
    # See ``RFReceivePeriodicMsgV3ToV9``
    FEATURE_ID = RFTestBLE.FEATURE_ID
# end class RFBLEReceivePeriodicMsgV3ToV9


class RFBLESendPeriodicFullDutyMsgV9(RFSendPeriodicFullDutyMsgV9):
    # See ``RFSendPeriodicFullDutyMsgV9``
    FEATURE_ID = RFTestBLE.FEATURE_ID
# end class RFBLESendPeriodicFullDutyMsgV9


class RFBLESendPeriodicFullDutyMsgResponseV9(RFSendPeriodicFullDutyMsgResponseV9):
    # See ``RFSendPeriodicFullDutyMsgResponseV9``
    FEATURE_ID = RFTestBLE.FEATURE_ID
# end class RFSendPeriodicFullDutyMsgResponseV9

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
