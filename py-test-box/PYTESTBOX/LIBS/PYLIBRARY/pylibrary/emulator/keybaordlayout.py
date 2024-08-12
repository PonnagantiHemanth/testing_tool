#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pylibrary.emulator.keyboardlayout
:brief: Keyboard key layout definition
:author: Fred Chen <fchen7@logitech.com>
:date: 2021/03/24
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from typing import Dict
from typing import List
from typing import Tuple

from pylibrary.emulator.keyid import KEY_ID
from pyraspi.raspi import is_kosmos_setup
from pyraspi.services.mt8816 import MT8816

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
# ANSI, ISO 104, ISO 105, ISO 107 & JIS 109
LAYOUT_MAX_COUNT = 5

# A KEY_ID referencing this tuple signifies its (COL, ROW) position is undefined (like for Gtech-based Keyboard)
COL_ROW_UNDEFINED = (None, None)

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class KbdMatrix:
    if is_kosmos_setup():
        COL_0 = 0
        COL_1 = 1
        COL_2 = 2
        COL_3 = 3
        COL_4 = 4
        COL_5 = 5
        COL_6 = 6
        COL_7 = 7
        COL_8 = 8
        COL_9 = 9
        COL_10 = 10
        COL_11 = 11
        COL_12 = 12
        COL_13 = 13
        COL_14 = 14
        COL_15 = 15
        COL_16 = 16
        COL_17 = 17
        COL_18 = 18
        COL_19 = 19
        COL_20 = 20
        COL_21 = 21
        COL_22 = 22
        COL_23 = 23

        ROW_0 = 0
        ROW_1 = 1
        ROW_2 = 2
        ROW_3 = 3
        ROW_4 = 4
        ROW_5 = 5
        ROW_6 = 6
        ROW_7 = 7
        ROW_8 = 8
        ROW_9 = 9
        ROW_10 = 10
        ROW_11 = 11
        ROW_12 = 12
        ROW_13 = 13
        ROW_14 = 14
        ROW_15 = 15
        ROW_16 = 16
        ROW_17 = 17
        ROW_18 = 18
        ROW_19 = 19
        ROW_20 = 20
        ROW_21 = 21
        ROW_22 = 22
        ROW_23 = 23
    else:
        # -------- CS 0 --------
        COL_0 = MT8816.ADDRESS.Y0
        COL_1 = MT8816.ADDRESS.Y1
        COL_2 = MT8816.ADDRESS.Y2
        COL_3 = MT8816.ADDRESS.Y3
        COL_4 = MT8816.ADDRESS.Y4
        COL_5 = MT8816.ADDRESS.Y5
        COL_6 = MT8816.ADDRESS.Y6
        COL_7 = MT8816.ADDRESS.Y7
        # -------- CS 1 --------
        COL_8 = MT8816.ADDRESS.Y8
        COL_9 = MT8816.ADDRESS.Y9
        COL_10 = MT8816.ADDRESS.Y10
        COL_11 = MT8816.ADDRESS.Y11
        COL_12 = MT8816.ADDRESS.Y12
        COL_13 = MT8816.ADDRESS.Y13
        COL_14 = MT8816.ADDRESS.Y14
        COL_15 = MT8816.ADDRESS.Y15
        # -------- CS 2 --------
        COL_16 = MT8816.ADDRESS.Y16
        COL_17 = MT8816.ADDRESS.Y17
        COL_18 = MT8816.ADDRESS.Y18
        COL_19 = MT8816.ADDRESS.Y19
        COL_20 = MT8816.ADDRESS.Y20
        COL_21 = MT8816.ADDRESS.Y21
        COL_22 = MT8816.ADDRESS.Y22
        COL_23 = MT8816.ADDRESS.Y23

        ROW_0 = MT8816.ADDRESS.X0
        ROW_1 = MT8816.ADDRESS.X1
        ROW_2 = MT8816.ADDRESS.X2
        ROW_3 = MT8816.ADDRESS.X3
        ROW_4 = MT8816.ADDRESS.X4
        ROW_5 = MT8816.ADDRESS.X5
        ROW_6 = MT8816.ADDRESS.X6
        ROW_7 = MT8816.ADDRESS.X7
        ROW_8 = MT8816.ADDRESS.X8
        ROW_9 = MT8816.ADDRESS.X9
        ROW_10 = MT8816.ADDRESS.X10
        ROW_11 = MT8816.ADDRESS.X11
        ROW_12 = MT8816.ADDRESS.X12
        ROW_13 = MT8816.ADDRESS.X13
        ROW_14 = MT8816.ADDRESS.X14
        ROW_15 = MT8816.ADDRESS.X15
    # end if
# end class KbdMatrix


class CommonKeyMatrix:
    """
    Define a key matrix layout configuration
    """
    LAYOUT = 'US'
    HAS_KEYPAD = True
    IS_HYBRID = False
    IS_ANALOG = False

    KEYS: Dict[KEY_ID, Tuple[int, int]] = {}
    FN_KEYS: Dict[KEY_ID, KEY_ID] = {}
# end class CommonKeyMatrix


class HybridKeyMatrix(CommonKeyMatrix):
    """
    Define a Hybrid key matrix layout configuration
    """
    IS_HYBRID = True

    # List of switches with reversed MAKE and BREAK instructions.
    REVERSE_MAKE_LOGIC_KEYS: List[KEY_ID] = []
# end class HybridKeyMatrix


class AnalogKeyMatrix(CommonKeyMatrix):
    """
    Define a Analog key matrix layout configuration
    """
    IS_ANALOG = True

    # List of analog keys that are sensed by the Gtech chip.
    # The chain_id indicate the position in the SPI message payload.
    KEYID_2_CHAINID: Dict[KEY_ID, int] = {}
# end class AnalogKeyMatrix

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
