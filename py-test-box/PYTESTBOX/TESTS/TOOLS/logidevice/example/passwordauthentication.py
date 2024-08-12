# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: logidevice.example.passwordauthentication
:brief:   Example of logidevicehandler to do password authentication.
:author:  YY Liu  <yliu5@logitech.com>
:date:    2022/07/01
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
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)
# end if
from logidevice.logidevicehandler import LogiDeviceHandler
from pyhid.hidpp.features.common.passwordauthentication import PasswordAuthentication
from pyhid.hidpp.features.common.passwordauthentication import PasswordAuthenticationModel
from pyhid.hidpp.features.enablehidden import EnableHidden
from pyhid.hidpp.features.enablehidden import EnableHiddenModel
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


def password_auth(pid, tid):
    """
    Run Password authentication from DUT via logidevicehandler.

    :param pid: The product ID of the device. None for the default PID(HERZOG).
    :type pid: ``str`` or ``None``
    :param tid: The transpose ID of the device. None for the default TID(HERZOG).
    :type tid: ``tuple`` or ``None``
    """
    feature_id_1e00 = EnableHidden.FEATURE_ID
    feature_id_1602 = PasswordAuthentication.FEATURE_ID

    with LogiDeviceHandler(pid=pid, tid=tid) as handler:
        # Enable Hidden feature
        result = handler.send_message(feature_id=feature_id_1e00,
                                      function_id=EnableHiddenModel.INDEX.SET_ENABLE_HIDDEN_FEATURES,
                                      enable_byte=EnableHidden.ENABLED)
        stdout.write(f'0x1E00 result = {result}\n')

        # Start session x1E02_Manuf
        session_name = HexList.fromString(DevicePasswordAuthenticationTestUtils.AccountNames.MANUFACTURING.value)
        result = handler.send_message(feature_id=feature_id_1602,
                                      function_id=PasswordAuthenticationModel.INDEX.START_SESSION,
                                      name=session_name)
        stdout.write(f'x1E02_Manuf result = {result}\n')

        # Send Password 0
        result = handler.send_message(feature_id=feature_id_1602,
                                      function_id=PasswordAuthenticationModel.INDEX.PASSWD0,
                                      passwd=HexList(handler.framework_adapter.PASSWORD_MANUF))
        stdout.write(f'Password0 result = {result}\n')

        # End session x1E02_Manuf
        result = handler.send_message(feature_id=feature_id_1602,
                                      function_id=PasswordAuthenticationModel.INDEX.END_SESSION,
                                      name=session_name)
        stdout.write(f'End session result = {result}\n')

        # Start session x1E02_Compl
        session_name = HexList.fromString(DevicePasswordAuthenticationTestUtils.AccountNames.COMPLIANCE.value)
        result = handler.send_message(feature_id=feature_id_1602,
                                      function_id=PasswordAuthenticationModel.INDEX.START_SESSION,
                                      name=session_name)
        stdout.write(f'x1E02_Compl result = {result}\n')

        # Send Password 0
        result = handler.send_message(feature_id=feature_id_1602,
                                      function_id=PasswordAuthenticationModel.INDEX.PASSWD0,
                                      passwd=HexList(handler.framework_adapter.PASSWORD_COMPL))
        stdout.write(f'Password0 result = {result}\n')

        # End session x1E02_Compl
        result = handler.send_message(feature_id=feature_id_1602,
                                      function_id=PasswordAuthenticationModel.INDEX.END_SESSION,
                                      name=session_name)
        stdout.write(f'End session result = {result}\n')

        # Start session x1E02_Gothard
        session_name = HexList.fromString(DevicePasswordAuthenticationTestUtils.AccountNames.GOTHARD.value)
        result = handler.send_message(feature_id=feature_id_1602,
                                      function_id=PasswordAuthenticationModel.INDEX.START_SESSION,
                                      name=session_name)
        stdout.write(f'x1E02_Gothard result = {result}\n')

        # Send Password 0
        result = handler.send_message(feature_id=feature_id_1602,
                                      function_id=PasswordAuthenticationModel.INDEX.PASSWD0,
                                      passwd=HexList(handler.framework_adapter.PASSWORD_GOTHA))
        stdout.write(f'Password0 result = {result}\n')

        # End session x1E02_Gothard
        result = handler.send_message(feature_id=feature_id_1602,
                                      function_id=PasswordAuthenticationModel.INDEX.END_SESSION,
                                      name=session_name)
        stdout.write(f'End session result = {result}\n')
    # end with
# end def password_auth


if __name__ == '__main__':
    password_auth(pid=PID, tid=TID)
# end if

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
