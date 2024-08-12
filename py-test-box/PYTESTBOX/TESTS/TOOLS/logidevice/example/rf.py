# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: logidevice.example.rf
:brief:   Example of logidevicehandler to test rf.
:author:  Jerry Lin
:date:    2020/04/21
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import sys
from os import path
from sys import stdout

FILE_PATH = path.abspath(__file__)
WS_DIR = FILE_PATH[:FILE_PATH.rfind("TESTS")]
TOOLS_DIR = path.join(WS_DIR, "TESTS", "TOOLS")
PYTRANSPORT_DIR = path.join(WS_DIR, "LIBS", "PYTRANSPORT")
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)
# end if
if PYTRANSPORT_DIR not in sys.path:
    sys.path.insert(0, PYTRANSPORT_DIR)
# end if
from logidevice.logidevicehandler import LogiDeviceHandler
from pytransport.usb.usbconstants import LogitechReceiverProductId
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuth
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuthModel
from pyhid.hidpp.features.common.rftest import RFTest
from pyhid.hidpp.features.common.rftest import RFTestModel
from pyhid.hidpp.features.enablehidden import EnableHidden
from pyhid.hidpp.features.enablehidden import EnableHiddenModel
from pyhid.hidpp.features.common.passwordauthentication import PasswordAuthentication
from pyhid.hidpp.features.common.passwordauthentication import PasswordAuthenticationModel
from pylibrary.tools.hexlist import HexList
from pytestbox.device.base.passwordauthenticationutils import DevicePasswordAuthenticationTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# HERZOG
# PID = 'C52B'
# Herzog
# TID = '4082'
# Zaha
# TID = '4090'

# G502 Hyjal
# PID = 'C07D'
# TID = ('C07D',)

# G705 Garnet
# PID = 'C547'
# TID = ('409D',)

# Artanis
# PID = 'C547'
# TID = ('4099',)

# Bazooka2
PID = 'C54D'
TID = ('40A9',)


def rf(pid, tid):
    """
    Run RFTest from DUT via logidevicehandler.

    Before sending next command, check if DUT connects back to the receiver(i.e. finish previous test).

    :param pid: The product ID of the device. None for the default PID(HERZOG).
    :type pid: ``str`` or ``None``
    :param tid: The transpose ID of the device. None for the default TID(HERZOG).
    :type tid: ``tuple`` or ``None``
    """
    feature_id_1e00 = EnableHidden.FEATURE_ID
    feature_id_1602 = PasswordAuthentication.FEATURE_ID
    feature_id_1e02 = ManageDeactivatableFeaturesAuth.FEATURE_ID
    feature_id_1890 = RFTest.FEATURE_ID

    handler = LogiDeviceHandler(pid=pid, tid=tid)
    handler.start()

    # Enable Hidden feature
    result = handler.send_message(feature_id=feature_id_1e00,
                                  function_id=EnableHiddenModel.INDEX.SET_ENABLE_HIDDEN_FEATURES,
                                  enable_byte=EnableHidden.ENABLED)
    stdout.write(f'0x1E00 result = {result}\n')

    if int(PID, 16) == LogitechReceiverProductId.SAVITUCK:
        # Start session x1E02_Compl
        session_name = HexList.fromString(DevicePasswordAuthenticationTestUtils.AccountNames.COMPLIANCE.value)
        result = handler.send_message(feature_id=feature_id_1602,
                                      function_id=PasswordAuthenticationModel.INDEX.START_SESSION,
                                      account_name=session_name)
        stdout.write(f'x1E02_Compl result = {result}\n')

        # Send Password 0
        result = handler.send_message(feature_id=feature_id_1602,
                                      function_id=PasswordAuthenticationModel.INDEX.PASSWD0,
                                      passwd=HexList(handler.framework_adapter.PASSWORD_COMPL))
        stdout.write(f'Password0 result = {result}\n')

        # Manage deactivatable features
        result = handler.send_message(feature_id=feature_id_1e02,
                                      function_id=ManageDeactivatableFeaturesAuthModel.INDEX.ENABLE_FEATURES,
                                      enable_all_bit="False", enable_gothard="False",
                                      enable_compliance="True", enable_manufacturing="False")
        stdout.write(f'enable hidden result = {result}\n')
    # end if

    # RFSendPeriodicMsg
    result = handler.send_message(feature_id=feature_id_1890,
                                  function_id=RFTestModel.INDEX.RF_SEND_PERIODIC_MSG,
                                  channel="00", power="06", period="00",
                                  condition="00", nbmsg="0000", radio_mode="00", payload_size="00")
    stdout.write(f'RFSendPeriodicMsg result: {result}\n')

    # RFTxCW
    result = handler.send_message(feature_id=feature_id_1890,
                                  function_id=RFTestModel.INDEX.RF_TX_CW,
                                  channel="2A", power="06", timeout="0060")
    stdout.write(f'RFTxCW result: {result}\n')

    # RFRxContinuous
    result = handler.send_message(feature_id=feature_id_1890,
                                  function_id=RFTestModel.INDEX.RF_RX_CONTINUOUS,
                                  channel="2A", power="06",
                                  timeout="0032", condition='00', radio_mode='02')
    stdout.write(f'RFRxContinuous result: {result}\n')

    # SetRfTxCWSweep
    result = handler.send_message(feature_id=feature_id_1890,
                                  function_id=RFTestModel.INDEX.SET_RF_RX_CONTINUOUS_SWEEP,
                                  channel_min="05", channel_max="06", power="06",
                                  sweep_period="1E", condition="00", radio_mode="02", nb_sweep="0003")
    stdout.write(f'SetRfTxCWSweep result: {result}\n')

    # SetRfRxContinuousSweep
    result = handler.send_message(feature_id=feature_id_1890,
                                  function_id=RFTestModel.INDEX.SET_RF_RX_CONTINUOUS_SWEEP,
                                  channel_min="05", channel_max="06", power="06",
                                  sweep_period="1E", condition="00", radio_mode="02", nb_sweep="0003")
    stdout.write(f'SetRfRxContinuousSweep result: {result}\n')

    # RFSendPeriodicMsgNoAck
    result = handler.send_message(feature_id=feature_id_1890,
                                  function_id=RFTestModel.INDEX.RF_SEND_PERIODIC_MSG_NO_ACK,
                                  channel="00", power="06", period="00",
                                  condition="00", nbmsg="0000", radio_mode="00", payload_size="00")
    stdout.write(f'RFSendPeriodicMsgNoAck result: {result}\n')

    # RFReceivePeriodicMsg
    result = handler.send_message(feature_id=feature_id_1890,
                                  function_id=RFTestModel.INDEX.RF_RECEIVE_PERIODIC_MSG,
                                  channel="00", power="06",
                                  condition="00", timeout="0060", radio_mode="00")
    stdout.write(f'RFReceivePeriodicMsg result: {result}\n')

    handler.close()
# end def rf


if __name__ == '__main__':
    rf(pid=PID, tid=TID)
# end if

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
