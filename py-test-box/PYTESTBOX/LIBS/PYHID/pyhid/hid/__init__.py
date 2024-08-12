#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyhid.hid
:brief: HID definition package
:author: christophe Roquebert
:date: 2019/01/31
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hid.hidcallstatemanagementcontrol import HidCallStateManagementControl
from pyhid.hid.hidconsumer import HidConsumer
from pyhid.hid.hiddigitizer import HidDigitizer
from pyhid.hid.hidkeyboard import HidKeyboard
from pyhid.hid.hidkeyboardbitmap import HidKeyboardBitmap
from pyhid.hid.hidmouse import HidMouse
from pyhid.hid.hidmouse import HidMouseNvidiaExtension
from pyhid.hid.hidsystemcontrol import HidSystemControl


# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
HID_REPORTS = (HidMouse, HidMouseNvidiaExtension, HidKeyboard, HidKeyboardBitmap, HidConsumer, HidSystemControl,
               HidCallStateManagementControl, HidDigitizer)


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
