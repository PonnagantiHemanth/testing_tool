#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.mouse
:brief: Device HID mouse Package
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2023/01/19
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pylibrary.emulator.keyid import KEY_ID

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
EXCLUDED_BUTTONS = [KEY_ID.CONNECT_BUTTON, KEY_ID.DPI_CYCLING_BUTTON, KEY_ID.DPI_UP_BUTTON, KEY_ID.DPI_DOWN_BUTTON,
                    KEY_ID.DPI_SHIFT_BUTTON, KEY_ID.SMART_SHIFT, KEY_ID.VIRTUAL_GESTURE_BUTTON, KEY_ID.DPI_SWITCH,
                    KEY_ID.LAUNCH_DIDOT]


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
